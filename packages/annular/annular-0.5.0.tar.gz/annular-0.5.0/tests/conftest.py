import logging

import numpy as np
import pandas as pd
import pyomo.environ as pyo
import pytest
from libmuscle import Grid, Message

from annular.satellite_model.simple_demo import SimpleMultiHourBiddingStrategy

# set logger; need StreamHandler because of
# https://github.com/multiscale/muscle3/blob/462231db35bfa93619fe22732939c8051cf7f2b8/libmuscle/python/libmuscle/runner.py#L138
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(logging.StreamHandler())


def compare_objects(actual, expected):
    """Compare two objects depending on their types."""
    match actual:
        case Grid():  # when `actual` is of type Grid, `expected` will be of type np.ndarray
            return np.allclose(actual.array, expected)
        case arr if isinstance(arr, np.ndarray):  # cannot directly match np.ndarray
            return np.allclose(actual, expected)
        case None:
            return actual is expected
        case float():
            return actual == pytest.approx(expected)
        case pd.DataFrame():
            pd.testing.assert_frame_equal(actual, expected)
        case obj if hasattr(obj, "__eq__"):
            return actual == expected
        case _:
            raise RuntimeError


@pytest.fixture(scope="session")
def solver():
    """Create the pyomo solver."""
    return pyo.SolverFactory("highs")


@pytest.fixture(scope="package")
def data_dir(pytestconfig):
    """Constant path to the directory for test data."""
    return pytestconfig.rootpath / "tests/data"


@pytest.fixture(scope="module")
def six_hour_index():
    """A pandas DateTimeIndex consisting of six hours."""
    return pd.date_range(start="2024-01-01 00:00", periods=6, freq="h")


@pytest.fixture(scope="module")
def demands(six_hour_index):
    """Basic demands: a base load and a 2h flexible load spanning 6h."""
    load_values = [
        [10, 0],
        [20, 0],
        [30, 10],
        [40, 20],
        [50, 30],
        [60, 40],
    ]

    loads = pd.DataFrame(
        data=load_values,
        columns=["base", "flex+2"],
        index=pd.DatetimeIndex(data=six_hour_index, name="snapshots"),
    )
    return loads


@pytest.fixture
def electricity_price_forecast(six_hour_index):
    """Base electricity price forecast to use."""
    return pd.DataFrame(
        data={"e_price": [30, 5, 20, 15, 25, 10]},
        index=pd.DatetimeIndex(data=six_hour_index, name="snapshots"),
    )


@pytest.fixture(scope="module")
def carrier_prices(six_hour_index):
    """Prices for non-electricity carriers."""
    return pd.DataFrame(
        data={"methane": [42] * len(six_hour_index), "biogas": [75] * len(six_hour_index)},
        index=pd.DatetimeIndex(data=six_hour_index, name="snapshots"),
    )


@pytest.fixture
def dummy_config_dir(tmp_path):
    """Create a directory with some (empty) dummy config files."""
    for i in range(5):
        tmp_path.joinpath(f"dummy_config_{i}.yml").touch()
    return tmp_path


@pytest.fixture(scope="module")
def sample_dataframe():
    """Example fixture: dataframe."""
    columns = ("exclusive_group_id", "profile_block_id", "timestamp", "quantity", "price")
    timestamp = pd.Timestamp("2024-01-01 00:00:00", tz="utc")
    data = (
        [1, 0, timestamp, 100, 10],
        [2, 0, timestamp, 200, 20],
        [3, 0, timestamp, 300, 30],
    )
    return pd.DataFrame.from_records(data, index=columns[:3], columns=columns)


@pytest.fixture(scope="module")
def sample_battery_bids():
    """Example fixture: bids from a battery operator.

    It wants to discharge for 10 at ceiling price (€10), and charge for 10 at
    a price of €2 or below. In between, there's an extra bid of 10 at €6 to
    indicate that below a price of €6, they are no longer interested in
    supplying power, i.e., their net demand at a price of below €6 is 0.
    """
    columns = ("satellite", "exclusive_group_id", "profile_block_id", "timestamp", "quantity", "price")
    timestamp = pd.Timestamp("2024-01-01 00:00:00")
    data = (
        ["battery", 0, 1, timestamp, -5, 10.0],
        ["battery", 1, 1, timestamp, 0, 8.0],
        ["battery", 2, 1, timestamp, 5, 6.0],
        ["battery", 3, 1, timestamp, 0, 4.0],
        ["battery", 4, 1, timestamp, 5, 2.0],
    )
    return pd.DataFrame.from_records(data, index=columns[:4], columns=columns)


@pytest.fixture(scope="module")
def sample_block_bids():
    """Example of a new set of demand (block) bids."""
    columns = ("satellite", "exclusive_group_id", "profile_block_id", "timestamp", "quantity", "price")
    timestamps = (
        pd.Timestamp("2024-01-01 00:00:00"),
        pd.Timestamp("2024-01-01 01:00:00"),
        pd.Timestamp("2024-01-01 02:00:00"),
    )
    data = (
        ["A", 1, 1, timestamps[0], 30, 100.0],
        ["A", 1, 1, timestamps[1], 20, 100.0],
        ["A", 1, 1, timestamps[2], 10, 100.0],
        ["A", 1, 2, timestamps[0], 10, 100.0],
        ["A", 1, 2, timestamps[1], 20, 100.0],
        ["A", 1, 2, timestamps[2], 30, 100.0],
        ["B", 2, 1, timestamps[0], 30, 100.0],
        ["B", 2, 1, timestamps[1], 20, 100.0],
        ["B", 2, 1, timestamps[2], 10, 100.0],
        ["B", 2, 2, timestamps[0], 10, 100.0],
        ["B", 2, 2, timestamps[1], 20, 100.0],
        ["B", 2, 2, timestamps[2], 30, 100.0],
        ["C", 3, 1, timestamps[0], 10, 100.0],
        ["C", 4, 1, timestamps[1], 20, 100.0],
        ["C", 5, 1, timestamps[2], 30, 100.0],
    )
    return pd.DataFrame.from_records(data, index=columns[:4], columns=columns)


@pytest.fixture
def sample_message(sample_dataframe):
    """Example fixture: message."""
    msg = Message(
        timestamp=0,
        data={
            "quantity": Grid(sample_dataframe["quantity"].to_numpy()),
            "price": Grid(sample_dataframe["price"].to_numpy()),
            "exclusive_group_id": Grid(sample_dataframe.index.get_level_values("exclusive_group_id").to_numpy()),
            "profile_block_id": Grid(sample_dataframe.index.get_level_values("profile_block_id").to_numpy()),
            "timestamp": Grid((sample_dataframe.index.get_level_values("timestamp").astype(np.int64) / 1e9).to_numpy()),
        },
    )
    return msg


@pytest.fixture(scope="module")
def base_load_values():
    """Provide some sample load values."""
    return [10, 20, 30, 40, 50]


@pytest.fixture
def simple_demo_bid_strategy(tmp_path):
    """Initialization of the simple demo bid strategy for 24h bids."""
    DAY_LENGTH = 4
    hours = pd.date_range(start="2024-01-01 00:00", periods=4 * DAY_LENGTH, freq="h")
    hour_index = pd.DatetimeIndex(data=hours, name="snapshots")
    flex_load = pd.DataFrame(
        # [0, ..., 1, 0, ..., 2, ...]
        data=[i if x == 3 else 0 for i in range(1, 1 + DAY_LENGTH) for x in range(DAY_LENGTH)],
        columns=[f"flex+{DAY_LENGTH}"],
        index=hour_index,
    )
    # define a 'default' predicted price for 4 days
    prices = [10] * 4 * DAY_LENGTH
    # create 4 'dips' in price at different moments during each day
    prices[1 + 0 * DAY_LENGTH] = 7.5
    prices[3 + 1 * DAY_LENGTH] = 6
    prices[0 + 2 * DAY_LENGTH] = 5
    prices[2 + 3 * DAY_LENGTH] = 8

    forecast = pd.DataFrame(
        data=prices,
        columns=["e_price"],
        index=hour_index,
    )

    forecast_file = tmp_path / "forecast.csv"
    demands_file = tmp_path / "demands.csv"

    forecast.to_csv(forecast_file)
    flex_load.to_csv(demands_file)

    common_settings = {
        "ceiling_price": 100,
        "start_hour": 0,
        "num_hours": 120,
        "rolling_horizon_step": DAY_LENGTH,
    }

    config_dict = {
        "strategy": "simple",
        "floor_price": 0,
        "forecasts_path": forecast_file,
        "demands_path": demands_file,
        "bid_margin": 0.05,
        "horizon_size": 2 * DAY_LENGTH,
        "results_folder": tmp_path / "test_satellite",
    }

    input_args = common_settings | config_dict
    return SimpleMultiHourBiddingStrategy(**input_args)


@pytest.fixture(scope="module")
def sample_market_info():
    """Sample market information passed from central market to satellites."""
    price = np.array([4.5, 6])
    scheduled_demand = np.array([10, 2])
    timestamp = 1.0
    return price, scheduled_demand, timestamp


@pytest.fixture(scope="module")
def sample_market_info_msg(sample_market_info):
    """Sample market info, converted to message."""
    data = {"price": Grid(sample_market_info[0]), "scheduled_demand": Grid(sample_market_info[1])}
    return Message(timestamp=sample_market_info[2], data=data)


@pytest.fixture(scope="module")
def empty_market_info():
    """Empty market information passed from central market to satellites at the start of the simulation."""
    price = None
    scheduled_demand = None
    timestamp = 1.0
    return price, scheduled_demand, timestamp


@pytest.fixture(scope="module")
def empty_market_info_msg(empty_market_info):
    """Sample market info, converted to message."""
    data = {"price": empty_market_info[0], "scheduled_demand": empty_market_info[1]}
    return Message(timestamp=empty_market_info[2], data=data)
