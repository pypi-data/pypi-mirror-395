import logging
from itertools import groupby, product
from operator import itemgetter
from pathlib import Path

import numpy as np
import pandas as pd
import pyomo.environ as pyo
from cronian.generators import add_all_generators

logger = logging.getLogger(__name__)


def create_market_model(
    demand_bids: pd.DataFrame,
    generator_configs: dict[str, dict],
    timeseries_data: pd.DataFrame,
    snapshots: pd.DatetimeIndex,
) -> pyo.AbstractModel:
    """Create the central market clearing model.

    Args:
        demand_bids: MultiIndex DataFrame of demand bids for all consumers/prosumers.
        generator_configs: dict of configurations defining of all generators.
        timeseries_data: DataFrame containing all timeseries_data.
        snapshots: snapshots/timesteps for which the market model is created.

    Returns:
        Pyomo model representing the market-clearing optimization problem.
    """
    model = pyo.AbstractModel(name="Market-model")
    model.time = pyo.Set(initialize=snapshots, ordered=True)

    # Supply
    add_all_generators(model, generator_configs, timeseries_data)
    create_generation_cost_expression(model)

    # Demand
    encode_block_bids_into_model(model, demand_bids)
    constrain_power_balance(model)

    # Objective
    set_objective_as_social_welfare_maximization(model)

    return model


def encode_block_bids_into_model(model: pyo.Model, demand_bids: pd.DataFrame) -> None:
    """Create gross surplus expression and set mutual exclusivity constraint.

    This takes bids in the following format:

    +-----------+--------------------+------------------+-----------+----------+-------+
    | satellite | exclusive_group_id | profile_block_id | timestamp | quantity | price |
    +-----------+--------------------+------------------+-----------+----------+-------+
    | ...       | ...                | ...              | ...       | ...      | ...   |
    +-----------+--------------------+------------------+-----------+----------+-------+

    where:

    - `satellite`: indicates which satellite this bid originates from
    - `exclusive_group_id`: ID of which exclusive group this bid belongs to
    - `profile_block_id`: ID of which profile block this bid belongs to
    - `timestamp`: timestamp for this bid
    - `quantity`: quantity for this bid
    - `price`: price for this bid

    and (satellite, exclusive_group_id, profile_block_id, timestamp) are its Index.

    Multiple bids sharing the same `profile_block_id` will be encoded to be met
    together, i.e., all-or-none.
    If multiple profiles share the same `exclusive_group_id`, at most one of
    them will be satisfied.

    Every bid must have a `profile_block_id` and `exclusive_group_id`. If a bid
    does not make use of profile block or exclusive group functionality, the
    `exclusive_group_id` must be unique, while `profile_block_id` can be any value.

    Args:
        model: Pyomo model to which the gross surplus expression is added.
        demand_bids: MultiIndex DataFrame of demand bids for all consumers/prosumers.
    """
    # Index bid by `(satellite, group, profile, time)`
    model.bid_idx = pyo.Set(initialize=demand_bids.index.values)

    # Each satellite may have different numbers of groups,
    # so index each group explicitly by `(satellite, group)`
    unique_groups = demand_bids.index.droplevel(["profile_block_id", "timestamp"]).unique()
    model.exclusive_group = pyo.Set(initialize=unique_groups)

    # Each group may have a different number of profiles,
    # so index each profile explicitly by `(satellite, group, profile)`
    unique_profiles = demand_bids.index.droplevel("timestamp").unique()
    model.profile = pyo.Set(initialize=unique_profiles)
    # To efficiently only have constraints for each existing profile index, record which profiles exist in a group.
    profiles_per_group = {group: list(profiles) for group, profiles in groupby(unique_profiles, itemgetter(0, 1))}

    # Set demand quantities as parameter in the model
    model.quantity = pyo.Param(model.bid_idx, initialize=demand_bids["quantity"])
    model.bid_price = pyo.Param(model.bid_idx, initialize=demand_bids["price"])

    # Create binary decision variables for all (possible) profiles within exclusive groups.
    model.profile_choice = pyo.Var(model.profile, domain=pyo.Binary)

    # All profiles within an exclusive group are mutually exclusive: at most one can be active.
    @model.Constraint(model.exclusive_group)
    def mutual_exclusivity(model, satellite, group):
        return pyo.quicksum(model.profile_choice[profile] for profile in profiles_per_group[(satellite, group)]) <= 1

    # Intermediate: demand met expression
    @model.Expression(model.bid_idx)
    def demand_met(model, satellite, group, profile, t):
        return model.quantity[satellite, group, profile, t] * model.profile_choice[satellite, group, profile]

    # Define gross surplus, i.e., total 'value' of all dispatched power from bids.
    # NOTE: a discharging/supplying bid (with negative quantity) would reduce the gross surplus when
    #       accepted, so we have to calculate gross surplus by the absolute values. Including
    #       `abs(model.demand_met)` in the expression would make it nonlinear, so instead we take
    #       the absolute value at input time. This makes it a constant and avoids nonlinear terms.
    @model.Expression()
    def gross_surplus(model):
        return pyo.quicksum(
            quantity * model.bid_price[satellite, group, profile, t] * model.profile_choice[satellite, group, profile]
            for (satellite, group, profile, t), quantity in demand_bids["quantity"].abs().items()
        )


def constrain_power_balance(model):
    """Constrain that total demand must equal total generation at all times.

    Assumes `model.gen_power` and `model.demand_met` have been defined.

    Args:
        model: Pyomo model to which the power balance constraint is added.
    """

    @model.Constraint(model.time)
    def power_balance(model, time):
        return pyo.quicksum(model.gen_power[gen, time] for gen in model.gens) == pyo.quicksum(
            model.demand_met[satellite, group, profile, t]
            for satellite, group, profile, t in model.bid_idx
            if t == time
        )


def create_generation_cost_expression(model: pyo.AbstractModel) -> None:
    """Create generation cost expression to be used in the objective function.

    Args:
        model: Pyomo model to which the generation cost expression is added.
    """

    def generation_cost_rule(model):
        quadratic_cost = pyo.quicksum(
            (model.gen_marginal_cost_quadratic[g]) * model.gen_power[g, t] ** 2
            for g in model.gens
            for t in model.time
            if model.gen_marginal_cost_quadratic[g] != 0  # only add if nonzero
        )

        linear_cost = pyo.quicksum(
            model.gen_marginal_cost_linear[g] * model.gen_power[g, t]
            for g in model.gens
            for t in model.time
            if model.gen_marginal_cost_linear[g] != 0  # only add if nonzero
        )

        return quadratic_cost + linear_cost

    model.generation_cost = pyo.Expression(rule=generation_cost_rule)


def set_objective_as_social_welfare_maximization(model: pyo.AbstractModel) -> None:
    """Set the objective function as social welfare maximization.

    Social welfare is defined as: gross surplus - generation cost.

    Args:
        model: Pyomo model to which the objective is added.
    """

    def social_welfare_rule(model):
        return model.gross_surplus - model.generation_cost

    model.objective = pyo.Objective(rule=social_welfare_rule, sense=pyo.maximize)


def get_market_clearing_price_as_dual(model_instance: pyo.ConcreteModel) -> pd.DataFrame:
    """Get market price as the dual of the power balance constraint.

    Note: Market price might be determined by bids from the demand side.

    Args:
        model_instance: Solved pyomo instance of the market model (LP)

    Returns:
        DataFrame representing the market clearing price for each timestamp.
    """
    # Note: duals are negative for maximization problems. So we multiply by -1 to get the correct price.
    return pd.DataFrame(
        {"market_price": [-1 * model_instance.dual[model_instance.power_balance[t]] for t in model_instance.time]},
        index=pd.Index(model_instance.time, name="timestamp"),
    )


def fix_integer_variables(model_instance: pyo.Model) -> pyo.ConcreteModel:
    """Fix all integer variables of the solved model instance to their current values.

    Args:
        model_instance: Solved pyomo instance of the market model (MILP).

    Returns:
        Pyomo model instance with integer/binary variables fixed to their
        current values from the solved MILP instance (making it an LP).
    """
    model_instance = model_instance.clone()
    for model_var in model_instance.component_data_objects(pyo.Var, active=True):
        if not model_var.is_continuous():
            model_var.fixed = True

    return model_instance


def run_market_model(model: pyo.AbstractModel, output_path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Run market model and return market_price and demand_met.

    Args:
        model: Pyomo model to run/solve.
        output_path: path to save the results to.

    Returns:
        tuple: market clearing price and demand met by the market.

    Raises:
        RuntimeError: if the optimization problem is infeasible or unbounded.
    """
    model_instance_milp = model.create_instance()
    solver = pyo.SolverFactory("gurobi")
    results = solver.solve(model_instance_milp, tee=False)

    if results.solver.termination_condition != pyo.TerminationCondition.optimal:
        raise RuntimeError(f"Solver did not converge. Termination condition: {results.solver.termination_condition}")

    # Fix integer variables to their current values, making the model an LP
    model_instance_lp = fix_integer_variables(model_instance_milp)

    # Add suffix to import duals
    model_instance_lp.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

    # Re-solve as LP to get duals
    solver.solve(model_instance_lp, tee=False)

    market_price = get_market_clearing_price_as_dual(model_instance_lp)
    generator_dispatch = extract_generator_dispatch(model_instance_lp)
    scheduled_demand = extract_scheduled_demand(model_instance_lp)

    logger.debug("Inside market_model, market price: %s", market_price)
    logger.debug("Scheduled_demand: %s", scheduled_demand)
    logger.debug("generator_dispatch: %s", generator_dispatch)

    market_results = market_results_to_df(generator_dispatch, market_price, scheduled_demand)
    market_results.to_csv(output_path, mode="a", header=not output_path.exists())

    return market_price.to_numpy().flatten(), scheduled_demand.to_numpy().flatten()


def extract_scheduled_demand(model_instance: pyo.ConcreteModel) -> pd.DataFrame:
    """Extract scheduled demand from market model.

    Args:
        model_instance: solved market-clearning pyomo model.

    Returns:
        amount of scheduled demand per bid.
    """
    scheduled_demand = [pyo.value(model_instance.demand_met[q]) for q in model_instance.bid_idx]
    # Prepare scheduled bids as a dataframe indexed by the 4-level bids_index
    bids_index = pd.MultiIndex.from_tuples(
        model_instance.bid_idx,
        names=["satellite", "exclusive_group_id", "profile_block_id", "timestamp"],
    )
    return pd.DataFrame({"scheduled": scheduled_demand}, index=bids_index)


def extract_generator_dispatch(model_instance: pyo.ConcreteModel) -> pd.DataFrame:
    """Extract generator dispatch from market model.

    Args:
        model_instance: solved market-clearing pyomo model.

    Returns:
        amount of generator dispatch per timestamp.
    """
    # Prepare generator dispatch as a dataframe indexed by generator and time
    generator_dispatch = [
        (gen, t, model_instance.gen_power[gen, t].value)
        for gen, t in product(sorted(model_instance.gens), model_instance.time)
    ]
    return pd.DataFrame.from_records(
        generator_dispatch, columns=["generator", "timestamp", "dispatch"], index=["generator", "timestamp"]
    )


def market_results_to_df(
    generator_dispatch: pd.DataFrame, market_price: pd.DataFrame, scheduled_demand: pd.DataFrame
) -> pd.DataFrame:
    """Prepare the relevant market clearing results that should be logged.

    The market results are returned as one row per timestamp. Columns are market
    price, dispatch per generator, and scheduled demand per satellite. I.e.,

    +-----------+--------------+-------------+-------------+-----+-------------+-------------+-----+
    | timestamp | market_price | Generator 1 | Generator 2 | ... | Satellite 1 | Satellite 2 | ... |
    +-----------+--------------+-------------+-------------+-----+-------------+-------------+-----+
    | ...       | ...          | ...         | ...         |     | ...         | ...         |     |
    +-----------+--------------+-------------+-------------+-----+-------------+-------------+-----+

    with 'Generator N' and 'Satellite N' replaced by their actual provided names.

    Args:
        generator_dispatch: dataframe of generator dispatch per generator and timestamp.
        market_price: dataframe of market clearing price per timestamp.
        scheduled_demand: dataframe of demand scheduled per bid table entry.

    Returns:
        combined table of market price, generator dispatch and satellite supply per timestamp.
    """
    # Explicitly select the "scheduled" column, so it doesn't become a column multi-index level after unstacking
    supplied = scheduled_demand["scheduled"].unstack(level="satellite")  # unstack each satellite as a separate column
    supplied_summed = supplied.groupby(level="timestamp").sum()  # sum per timestamp, dropping group/block id

    unstacked_generator_dispatch = generator_dispatch["dispatch"].unstack(level="generator")

    logger.debug("supplied_per_prosumer: %s", supplied_summed)

    # concatenate the three time-indexed dataframes next to each other, sharing the time index
    market_results = pd.concat([market_price, unstacked_generator_dispatch, supplied_summed], axis=1)

    return market_results
