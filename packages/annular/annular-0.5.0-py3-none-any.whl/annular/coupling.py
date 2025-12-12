"""coupling.py: core model coupling functionality using MUSCLE3.

This file contains the creation of the coupling structure, and the MUSCLE3
instance definitions for both the central market model and the (arbitrary)
number of satellite models.

The standard coupling structure is one central market model linked to many
individual satellite models. The market model receives bid tables from the
satellite models, and after market clearing sends back the amount of satisfied
power and cleared market price.
"""

import logging
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import yaml
from cronian.configuration import load_configurations_subfolder
from libmuscle import Instance
from libmuscle.runner import run_simulation
from more_itertools import chunked
from ymmsl import Configuration, Operator, Settings

from .coupling_components import (
    compact_bids_to_msg,
    compact_market_info_to_msg,
    extract_bids_from_msg,
    extract_market_info_from_msg,
    get_coupling_setup,
)
from .market_model import create_market_model, run_market_model
from .satellite_model import strategies
from .utils import read_csv_with_utc_timestamps

logger = logging.getLogger(__name__)


def satellite_model() -> None:
    """A simple satellite model to determine demand bids."""
    instance = Instance(
        {
            Operator.F_INIT: ["market_info_in"],
            Operator.O_F: ["bids_out"],
        }
    )

    strategy = None
    while instance.reuse_instance():
        # F_INIT
        settings = instance.list_settings()
        coupling_level_settings = ["generator_configs", "timeseries_data_path", "satellite_configs"]
        common_settings = {k: instance.get_setting(k) for k in settings if k not in coupling_level_settings}

        config_file = Path(instance.get_setting("config", "str"))

        if strategy is None:
            with open(config_file) as f:
                strategy_name = yaml.safe_load(f)["strategy"]
            strategy = strategies[strategy_name].from_file(Path(config_file), **common_settings)

        msg = instance.receive("market_info_in")
        market_price, demand_met, t_cur = extract_market_info_from_msg(msg)
        timestamp = pd.Timestamp.fromtimestamp(t_cur)

        logger.info("Market_price and demand_met for satellite %s at timestep: %s", config_file.stem, timestamp)
        logger.info("market_price: %s, demand_met: %s", market_price, demand_met)
        strategy.meet_demand(market_price, demand_met)

        # O_F
        demand_bids = strategy.determine_bids()
        demand_bids_msg = compact_bids_to_msg(demand_bids, timestamp=t_cur)
        instance.send("bids_out", demand_bids_msg)


def central_market_model() -> None:
    """The central market model."""
    instance = Instance(
        {
            Operator.O_I: ["market_info_out[]"],
            Operator.S: ["bids_in[]"],
        }
    )

    while instance.reuse_instance():
        # F_INIT
        base_folder = Path(instance.get_setting("simulation_config_file")).parent
        output_path = Path(instance.get_setting("results_folder")) / "market.csv"

        start_hour = instance.get_setting("start_hour", "int")
        end_hour = start_hour + instance.get_setting("num_hours", "int")
        rolling_horizon_step = instance.get_setting("rolling_horizon_step", "int")
        timeseries_data = read_csv_with_utc_timestamps(
            base_folder / instance.get_setting("timeseries_data_path", "str")
        )
        snapshots = timeseries_data.index[start_hour:end_hour]

        generator_configs = load_configurations_subfolder(
            base_folder / instance.get_setting("generator_configs"), "Generators"
        )
        satellite_configs = list((base_folder / instance.get_setting("satellite_configs", "str")).iterdir())
        satellites = [config.stem for config in satellite_configs]

        market_price, scheduled_demand = None, {satellite: None for satellite in satellites}
        for window in chunked(snapshots, n=rolling_horizon_step):
            snapshot = window[0]
            utc_timestamp = snapshot.timestamp()
            # O_I
            for slot, satellite in enumerate(satellites):
                cur_state_msg = compact_market_info_to_msg(market_price, scheduled_demand[satellite], utc_timestamp)
                instance.send("market_info_out", cur_state_msg, slot=slot)

                logger.info("Sent to satellite %s:", satellite)
                logger.info("market price: %s", market_price)
                logger.info("scheduled demand: %s", scheduled_demand[satellite])

            # S
            satellite_demand_bids = {}
            for slot, satellite in enumerate(satellites):
                msg = instance.receive("bids_in", slot=slot)
                bids = extract_bids_from_msg(msg)
                satellite_demand_bids[satellite] = bids

                logger.info("Demand bids recieved from satellite %s for timestep %s", satellite, snapshot)
                logger.info(bids)

            demand_bids = pd.concat(satellite_demand_bids, names=["satellite"])
            model = create_market_model(demand_bids, generator_configs, timeseries_data, window)
            market_price, scheduled_bids = run_market_model(model, output_path)
            demand_bids["scheduled"] = scheduled_bids

            logger.debug("Market model has been run.")
            logger.debug("market_price: %s", market_price)
            logger.debug("demand_bids: %s", demand_bids)

            scheduled_demand = summarize_scheduled_demand(demand_bids, window)
            logger.info("scheduled_demand: %s", scheduled_demand)

        #### One final "iteration" to finish the process by forcing satellite to meet demand
        # O_I
        utc_timestamp += 1  # some 'fake' next timestep
        for slot, satellite in enumerate(satellites):
            cur_state_msg = compact_market_info_to_msg(market_price, scheduled_demand[satellite], utc_timestamp)
            instance.send("market_info_out", cur_state_msg, slot=slot)

            logger.info("Sending to satellite %s:", satellite)
            logger.info("market price: %s", market_price)
            logger.info("scheduled demand: %s", scheduled_demand[satellite])

        # S
        for slot in range(len(satellite_configs)):
            _ = instance.receive("bids_in", slot=slot)

        logger.info("done")


def summarize_scheduled_demand(demand_bids: pd.DataFrame, window: Iterable[pd.Timestamp]) -> dict[str, np.ndarray]:
    """Summarize explicitly scheduled demand per bid to amounts per timestamp.

    Bids do not have to be submitted for the entire bidding window, but
    scheduled demand does have to be reported per satellite model per timestamp.

    Args:
        demand_bids: Bids table with a `scheduled` column to be summarized.
        window: Bidding window over which to summarize.

    Returns:
        A dictionary with satellite names as keys, and an array of scheduled
        demand as values. This array is the same length as the given window,
        with `0` value if no demand is scheduled.
    """
    satellites = demand_bids.index.get_level_values("satellite").unique()
    # Explicitly create an index with entries for all timestamps of the current window
    new_index = pd.MultiIndex.from_product([satellites, window], names=["satellite", "timestamp"])

    summed = demand_bids["scheduled"].groupby(level=["satellite", "timestamp"]).sum()
    summed = summed.reindex(index=new_index, fill_value=0)

    return {satellite: summed.loc[satellite].to_numpy() for satellite in satellites}


def prepare_results_folder(config_file: Path, results_path: Path) -> dict:
    """Prepare the results folder to contain copies of the settings files to be used.

    Set up a unique folder for the model coupling run being executed.
    This folder will be the default location for any generated output by central
    or satellite models.

    Args:
        config_file: Initial configuration file from which settings for the
            model coupling run will be loaded.
        results_path: Path where a new folder for the results can be created.

    Returns:
        Finalized settings dictionary for the model coupling run.

    Raises:
        RuntimeError: if the given `results_path` already contains a results
            folder for this configuration file.
    """
    # Load the settings section of the given config file as regular yaml
    with open(config_file) as f:
        settings = yaml.safe_load(f)["settings"]

    # Arrange results are stored in a clean, config-specific folder
    results_folder = results_path / config_file.stem
    if results_folder.exists():
        raise RuntimeError(f"Results folder already exists: {results_folder}")
    results_folder.mkdir(parents=True)  # create fresh output path
    settings["results_folder"] = str(results_folder)

    return settings


def run(config_file: Path, results_path: Path = Path("results/")) -> None:
    """Run the coupled simulation.

    Args:
        config_file: configuration file for the simulation to run.
        results_path: location where a folder can be created for output files.
            Defaults to "results/".
    """
    logging.getLogger("yatiml").setLevel(logging.WARNING)

    settings = prepare_results_folder(config_file, results_path)
    satellite_configs_path = config_file.parent / settings["satellite_configs"]

    satellite_config_files = list(satellite_configs_path.iterdir())
    num_satellites = len(satellite_config_files)

    # Add the paths to the satellite configs to settings.
    # This means, for each satellite, the respective config file is dispatched
    # when called by `instance.get_settings("config").
    # The index in brackets needs to start at 0, and corresponds
    # to the satellite IDs maintained by muscle3.
    # At the time of writing, this was an undocumented feature in muscle3.
    settings |= {f"satellite[{i}].config": str(filepath) for i, filepath in enumerate(satellite_config_files)}
    settings["simulation_config_file"] = str(config_file)

    model = get_coupling_setup(config_file.stem, num_satellites)
    implementations = {"central": central_market_model, "satellite": satellite_model}
    configuration = Configuration(model, Settings(settings))

    # And run the coupled simulation!
    run_simulation(configuration, implementations)
