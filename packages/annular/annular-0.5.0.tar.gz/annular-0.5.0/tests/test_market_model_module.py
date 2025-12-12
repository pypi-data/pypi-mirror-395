"""Tests for the annular market_model.py module."""

from itertools import product

import numpy as np
import pandas as pd
import pyomo.environ as pyo
import pytest
from cronian.configuration import load_configurations_subfolder
from cronian.generators import add_all_generators

from annular.market_model import (
    constrain_power_balance,
    create_market_model,
    encode_block_bids_into_model,
    extract_generator_dispatch,
    extract_scheduled_demand,
    fix_integer_variables,
    get_market_clearing_price_as_dual,
    market_results_to_df,
    run_market_model,
)


@pytest.fixture(scope="module")
def sample_generator_configs(data_dir) -> dict[str, dict]:
    """Example fixture: generator Yaml configurations."""
    return load_configurations_subfolder(data_dir / "generator_configs", "Generators")


@pytest.fixture(scope="module")
def sample_capacity_factors(data_dir):
    """Example fixture: sample_capacity_factors_dataframe."""
    capacity_factor_df = pd.read_csv(data_dir / "capacity-factors.csv", index_col=0, parse_dates=True)
    return capacity_factor_df


@pytest.fixture(scope="module")
def sample_demand_bids(data_dir):
    """Example fixture: demand_bids_dataframe."""
    return pd.read_csv(
        data_dir / "stepwise-demand.csv",
        index_col=["satellite", "exclusive_group_id", "profile_block_id", "timestamp"],
        parse_dates=["timestamp"],
    )


@pytest.fixture
def mini_model():
    """A mini Pyomo ConcreteModel that only has a time attribute."""
    model = pyo.ConcreteModel()
    model.time = pyo.Set(initialize=pd.DatetimeIndex([pd.Timestamp("2024-01-01 00:00:00")]), ordered=True)
    return model


@pytest.fixture
def sample_market_model(sample_demand_bids, sample_generator_configs, sample_capacity_factors):
    """Example fixture: market model based on example generators, capacity factors and demand bids."""
    return create_market_model(
        demand_bids=sample_demand_bids,
        generator_configs=sample_generator_configs,
        timeseries_data=sample_capacity_factors,
        snapshots=pd.DatetimeIndex([pd.Timestamp("2024-01-01 00:00:00")]),
    )


@pytest.fixture(scope="module")
def gen_with_non_zero_quadratic_cost():
    """Generators with non-zero marginal-cost-quadratic."""
    return {
        "G11": {
            "name": "Gas-1",
            "id": "G11",
            "marginal_cost_quadratic": 0.004,
            "marginal_cost_linear": 6,
            "installed_capacity": 670,
        },
        "G12": {
            "name": "Gas-2",
            "id": "G12",
            "marginal_cost_quadratic": 0.006,
            "marginal_cost_linear": 5,
            "installed_capacity": 530,
        },
    }


@pytest.fixture(scope="module")
def constant_demand_bids():
    """Constant demand bids."""
    columns = ("satellite", "exclusive_group_id", "profile_block_id", "timestamp", "quantity", "price")
    timestamp = pd.Timestamp("2024-01-01 00:00:00")
    data = (
        ["satellite1", 1, 1, timestamp, 200, 250],
        ["satellite1", 2, 1, timestamp, 200, 300],
        ["satellite1", 3, 1, timestamp, 200, 350],
        ["satellite2", 1, 1, timestamp, 200, 400],
        ["satellite2", 2, 1, timestamp, 200, 450],
        ["satellite2", 3, 1, timestamp, 200, 500],
    )
    return pd.DataFrame.from_records(data, index=columns[:4], columns=columns)


@pytest.fixture(scope="module")
def solved_block_bids_market_model(sample_block_bids, sample_generator_configs, sample_capacity_factors, solver):
    """Create and solve a market model based on several generators and block bids."""
    market_model = create_market_model(
        demand_bids=sample_block_bids,
        generator_configs=sample_generator_configs,
        timeseries_data=sample_capacity_factors,
        snapshots=sample_block_bids.index.get_level_values("timestamp").unique(),
    )
    model_instance = market_model.create_instance()
    solver.solve(model_instance, tee=False)
    return model_instance


def test_block_demand_addition(mini_model, sample_block_bids):
    """Test that the necessary constraints and expressions have been added."""
    encode_block_bids_into_model(mini_model, sample_block_bids)

    assert isinstance(mini_model.mutual_exclusivity, pyo.Constraint)
    assert isinstance(mini_model.demand_met, pyo.Expression)
    assert isinstance(mini_model.gross_surplus, pyo.Expression)

    # assert that only as many constraints as unique groups exist
    unique_groups = sample_block_bids.index.droplevel(["profile_block_id", "timestamp"]).unique()
    assert len(mini_model.mutual_exclusivity) == len(unique_groups)
    assert all(mini_model.quantity[index] == quantity for index, quantity in sample_block_bids["quantity"].items())


def test_power_balance_needs_generators(mini_model, sample_block_bids):
    """Test that trying to balance power fails if no generators are present yet."""
    encode_block_bids_into_model(mini_model, sample_block_bids)
    with pytest.raises(AttributeError, match=r".* has no attribute 'gens'"):
        constrain_power_balance(mini_model)


def test_power_balance_needs_demand(mini_model, sample_generator_configs, sample_capacity_factors):
    """Test that trying to balance power fails if no bids have been encoded to define demand_met."""
    add_all_generators(mini_model, sample_generator_configs, sample_capacity_factors)
    with pytest.raises(AttributeError, match=".* has no attribute 'bid_idx'"):
        constrain_power_balance(mini_model)


def test_power_balance_constraint(mini_model, sample_generator_configs, sample_capacity_factors, sample_block_bids):
    """Test that the power balance constraint is added correctly."""
    add_all_generators(mini_model, sample_generator_configs, sample_capacity_factors)
    encode_block_bids_into_model(mini_model, sample_block_bids)
    constrain_power_balance(mini_model)
    assert isinstance(mini_model.power_balance, pyo.Constraint)


def test_gross_surplus_uses_absolute_quantities(mini_model, sample_block_bids):
    """Test that both demand and supply bids result in positive expressions for gross surplus."""
    bids = sample_block_bids.copy()
    # Set a number of bid quantities to be negative, i.e., supply bids
    for idx in [1, 6, 8, 9, 13]:
        bids.at[bids.index[idx], "quantity"] = -50
    encode_block_bids_into_model(mini_model, bids)

    assert all(coefficient >= 0 for coefficient in mini_model.gross_surplus.extract_values()[None].linear_coefs)


def test_one_profile_from_each_group_is_accepted(
    sample_block_bids, sample_generator_configs, sample_capacity_factors, solver
):
    """Test that multiple groups result in mulitple accepted profiles."""
    model = create_market_model(
        demand_bids=sample_block_bids,
        generator_configs=sample_generator_configs,
        timeseries_data=sample_capacity_factors,
        snapshots=sample_block_bids.index.get_level_values("timestamp").unique(),
    )
    model_instance = model.create_instance()

    solver.solve(model_instance, tee=False)

    assert sum(
        pyo.value(model_instance.profile_choice[profile]) for profile in model_instance.profile
    ) == pytest.approx(5)


def test_only_one_profile_from_group_is_accepted(
    sample_block_bids, sample_generator_configs, sample_capacity_factors, solver
):
    """Test that no more than 1 profile from an exclusive group is accepted.

    Specifically, by only providing a single exclusive group, and then checking that only one profile is accepted.
    """
    block_bids = sample_block_bids.iloc[:6]
    model = create_market_model(
        demand_bids=block_bids,
        generator_configs=sample_generator_configs,
        timeseries_data=sample_capacity_factors,
        snapshots=block_bids.index.get_level_values("timestamp").unique(),
    )
    model_instance = model.create_instance()

    solver.solve(model_instance, tee=False)

    assert sum(pyo.value(model_instance.profile_choice[profile]) for profile in model_instance.profile) == 1


def test_no_profile_from_group_may_be_accepted(
    sample_block_bids, sample_generator_configs, sample_capacity_factors, solver
):
    """Test that no profiles from a group is accepted when price is not right."""
    bids = sample_block_bids.copy()
    bids["price"] = 0.5
    model = create_market_model(
        demand_bids=bids,
        generator_configs=sample_generator_configs,
        timeseries_data=sample_capacity_factors,
        snapshots=bids.index.get_level_values("timestamp").unique(),
    )
    model_instance = model.create_instance()

    solver.solve(model_instance, tee=False)

    assert sum(pyo.value(model_instance.profile_choice[profile]) for profile in model_instance.profile) == 0


def test_profile_accepted_on_average_price(
    sample_block_bids, sample_generator_configs, sample_capacity_factors, solver
):
    """Test that a profile is accepted on average price.

    The market price for a particular hour of the profile might be above the bid
    price, as long as the weighted average price over the whole profile is below
    the bid price.

    Note: usually, prices for a profile would be constant, and whether a bid has
    a positive social welfare contribution would depend on the market price.
    For testing purposes though, it is equivalent to have the bid price be below
    the market price instead for a certain timestamp.
    """
    block_bids = sample_block_bids.copy().iloc[:3]
    # individual bids for t=0 and t=1 would be accepted, while individual bid for
    # t=2 would not be accepted. However, combined, their average price is good enough
    block_bids.loc[:, "price"] = [4, 4, 0.5]
    model = create_market_model(
        demand_bids=block_bids,
        generator_configs=sample_generator_configs,
        timeseries_data=sample_capacity_factors,
        snapshots=block_bids.index.get_level_values("timestamp").unique(),
    )
    model_instance = model.create_instance()

    solver.solve(model_instance, tee=False)

    assert sum(pyo.value(model_instance.profile_choice[profile]) for profile in model_instance.profile) == 1


def test_paradoxical_rejection(sample_block_bids, sample_generator_configs, sample_capacity_factors, solver):
    """Test paradoxical rejection of a profile bid.

    In paradoxical rejection, the final market price is below the bid price, but
    accepting the bid would cause the market price to end up above bid price.

    Specifically: bid ("B", 2, 1, timestamps[0], 5, 4) is rejected, because
    the market price is 3.5, but accepting this bid would make the market price
    4.5 instead.
    """
    block_bids = sample_block_bids.copy().iloc[[0, 1, 2, 6]]
    block_bids.at[block_bids.index[3], "quantity"] = 5
    block_bids.at[block_bids.index[3], "price"] = 4
    model = create_market_model(
        demand_bids=block_bids,
        generator_configs=sample_generator_configs,
        timeseries_data=sample_capacity_factors,
        snapshots=block_bids.index.get_level_values("timestamp").unique(),
    )
    model_instance = model.create_instance()

    solver.solve(model_instance, tee=False)

    model_instance.pprint()

    assert pyo.value(model_instance.profile_choice[("A", 1, 1)]) == 1
    assert pyo.value(model_instance.profile_choice[("B", 2, 1)]) == 0


def test_paradoxically_accepted(sample_block_bids, sample_generator_configs, sample_capacity_factors, solver):
    """Test a case of paradoxically accepted bids.

    Relevant generator availability for this test case:
    - 5 capacity at cost 1
    - 12 capacity at cost 3
    - 13 capacity at cost 2.5

    `generation_cost` expression for 30 + 20 demand:
        (5*1 + 12*3 + 13*3.5) + (5*1 + 12*3 + 3*3.5)
        = 5+36+45.5 + 5+36+10.5
        = 86.5 + 51.5 = 138

    Market price: 3.5

    `gross_surplus` expression for 30 + 20 demand at bid price of 3:
        30*3 + 20*3 = 90 + 60 = 150

    In this case, `gross_surplus` > `generation_cost`, but the bid price is not
    actually high enough. That the market model clears this profile bid is
    expected behavior, a post-processing step has to reject it later.
    """
    block_bids = sample_block_bids.copy().iloc[:2]
    block_bids.loc[:, "price"] = 3
    model = create_market_model(
        demand_bids=block_bids,
        generator_configs=sample_generator_configs,
        timeseries_data=sample_capacity_factors,
        snapshots=block_bids.index.get_level_values("timestamp").unique(),
    )
    model_instance = model.create_instance()

    solver.solve(model_instance, tee=False)

    assert sum(pyo.value(model_instance.profile_choice[profile]) for profile in model_instance.profile) == 1


def test_create_market_model(sample_market_model, sample_demand_bids):
    """Test create_market_model."""
    assert isinstance(sample_market_model, pyo.AbstractModel)

    model_instance = sample_market_model.create_instance()
    assert isinstance(model_instance, pyo.ConcreteModel)

    assert hasattr(model_instance, "gen_power")
    assert hasattr(model_instance, "demand_met")
    assert hasattr(model_instance, "generation_cost")
    assert hasattr(model_instance, "gross_surplus")
    assert hasattr(model_instance, "power_balance")
    assert hasattr(model_instance, "objective")
    assert isinstance(model_instance.objective, pyo.Objective)
    assert model_instance.objective.sense == pyo.maximize


@pytest.mark.gurobi
def test_run_market_model(sample_market_model, tmp_path, solver):
    """Test run_market_model."""
    # TODO: This test should be rewritten to actually test `run_market_model`. Currently, it is testing other
    # functions (get_market_clearing_price_as_dual and extract_scheduled_demand) inside `run_market_model`.
    # See https://gitlab.tudelft.nl/demoses/annular/-/issues/130
    market_price, scheduled_demand = run_market_model(sample_market_model, tmp_path / "market.csv")

    assert isinstance(market_price, np.ndarray)
    assert len(market_price.shape) == 1
    assert market_price == pytest.approx(4.5)

    assert isinstance(scheduled_demand, np.ndarray)
    assert len(scheduled_demand.shape) == 1
    assert sum(scheduled_demand) == pytest.approx(33.0)

    model_instance = sample_market_model.create_instance()
    solver.solve(model_instance, tee=False)

    assert pyo.value(model_instance.objective) == pytest.approx(404.0)


@pytest.mark.gurobi
def test_market_clearing_price(
    constant_demand_bids, gen_with_non_zero_quadratic_cost, sample_capacity_factors, tmp_path
):
    """Test that the market price is correct for a case where generators have non-zero marginal-cost-quadratic."""
    model = create_market_model(
        demand_bids=constant_demand_bids,
        generator_configs=gen_with_non_zero_quadratic_cost,
        timeseries_data=sample_capacity_factors,
        snapshots=pd.DatetimeIndex([pd.Timestamp("2024-01-01 00:00:00")]),
    )

    market_price, scheduled_demand = run_market_model(model, tmp_path / "market.csv")

    # All demand should be met since bid-prices for all demands are greater than generator marginal costs.
    assert sum(scheduled_demand) == pytest.approx(constant_demand_bids["quantity"].sum())

    # Can be solved analytically using the Lagrange multiplier to get the market price as 11.36 €/MWh.
    assert market_price == pytest.approx(11.36)


@pytest.mark.gurobi
def test_market_clearing_battery(sample_battery_bids, sample_generator_configs, sample_capacity_factors, tmp_path):
    """Test that the market dispatches correctly when given bids of a battery."""
    model = create_market_model(
        demand_bids=sample_battery_bids,
        generator_configs=sample_generator_configs,
        timeseries_data=sample_capacity_factors,
        snapshots=pd.DatetimeIndex([pd.Timestamp("2024-01-01 00:00:00")]),
    )
    market_price, scheduled_demand = run_market_model(model, tmp_path / "market.csv")
    assert np.allclose(market_price, [1])
    assert np.allclose(scheduled_demand, [-5, 0, 5, 0, 5])


def test_extract_generator_dispatch(solved_block_bids_market_model):
    """Test that dispatch is extracted correctly and has the right index."""
    generator_dispatch = extract_generator_dispatch(solved_block_bids_market_model)

    dispatch_values = [5, 5, 5, 12, 12, 12, 13, 13, 13, 8, 0, 0, 8, 8, 0, 9, 9, 9, 10, 10, 10, 5, 3, 1, 0, 0, 0]
    dispatch_index = pd.MultiIndex.from_tuples(
        product(sorted(solved_block_bids_market_model.gens), solved_block_bids_market_model.time),
        names=["generator", "timestamp"],
    )
    expected_dispatch = pd.DataFrame({"dispatch": dispatch_values}, index=dispatch_index, dtype=float)

    pd.testing.assert_frame_equal(generator_dispatch, expected_dispatch)


def test_extract_scheduled_demand(solved_block_bids_market_model):
    """Test that scheduled demand is extracted correctly."""
    scheduled_demand = extract_scheduled_demand(solved_block_bids_market_model)

    bids_index = pd.MultiIndex.from_tuples(
        solved_block_bids_market_model.bid_idx,
        names=["satellite", "exclusive_group_id", "profile_block_id", "timestamp"],
    )
    expected = pd.DataFrame(
        {"scheduled": [30, 20, 10, 0, 0, 0, 30, 20, 10, 0, 0, 0, 10, 20, 30]},
        index=bids_index,
        dtype=float,
    )

    pd.testing.assert_frame_equal(scheduled_demand, expected)


@pytest.mark.gurobi
def test_market_results_df(solved_block_bids_market_model):
    """Test that the market model prepares the correct data."""
    # Prepare the input to the market_results_to_df function and call it
    lp_model = fix_integer_variables(solved_block_bids_market_model)
    lp_model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
    # TODO: Investigate why using 'highs' here complains about not finding a dual while 'gurobi' works fine.
    solver = pyo.SolverFactory("gurobi")
    solver.solve(lp_model, tee=False)

    market_price = get_market_clearing_price_as_dual(lp_model)
    generator_dispatch = extract_generator_dispatch(solved_block_bids_market_model)
    scheduled_demand = extract_scheduled_demand(solved_block_bids_market_model)
    market_results = market_results_to_df(generator_dispatch, market_price, scheduled_demand)

    # Test that index and columns are as expected
    pd.testing.assert_index_equal(market_results.index, pd.Index(solved_block_bids_market_model.time, name="timestamp"))
    generators = list(sorted(solved_block_bids_market_model.gens))
    satellites = list(set(satellite for satellite, _ in solved_block_bids_market_model.exclusive_group))
    assert {*generators, *satellites, "market_price"} == set(market_results.columns)

    # Test market price and generator dispatch values match input data
    pd.testing.assert_series_equal(market_results["market_price"], market_price["market_price"])
    pd.testing.assert_frame_equal(
        market_results[generators], generator_dispatch["dispatch"].unstack(level="generator"), check_names=False
    )

    # Test that generator dispatch and scheduled demand match up per timestamp
    generation_per_timestamp = market_results[generators].sum(axis=1)
    demand_per_timestamp = market_results[satellites].sum(axis=1)
    pd.testing.assert_series_equal(generation_per_timestamp, demand_per_timestamp)


def test_fix_integer_variables(solved_block_bids_market_model):
    """Test fix_integer_variables function."""
    model_instance_lp = fix_integer_variables(solved_block_bids_market_model)

    # Test that integer variables are fixed
    integer_vars = [var for var in model_instance_lp.component_data_objects(pyo.Var) if not var.is_continuous()]
    assert all(var.is_fixed() for var in integer_vars), "Some integer variables have not been fixed."

    # Test that non-integer variables are not fixed
    continuous_vars = [var for var in model_instance_lp.component_data_objects(pyo.Var) if var.is_continuous()]
    assert all(not var.is_fixed() for var in continuous_vars), "Some continuous variables are fixed but should not be."


@pytest.mark.gurobi
def test_get_market_clearing_price_as_dual(sample_market_model):
    """Test that get_market_clearing_price_as_dual correctly extracts the market price."""
    # TODO: Investigate why using 'highs' here complains about not finding a dual why 'gurobi' works fine.
    solver = pyo.SolverFactory("gurobi")
    model_instance_milp = sample_market_model.create_instance()
    solver.solve(model_instance_milp, tee=False)

    model_instance_lp = fix_integer_variables(model_instance_milp)
    model_instance_lp.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
    solver.solve(model_instance_lp, tee=False)

    market_price = get_market_clearing_price_as_dual(model_instance_lp)

    assert isinstance(market_price, pd.DataFrame)
    assert len(market_price) == len(model_instance_lp.time)
    assert market_price["market_price"].values[0] == pytest.approx(4.5)
