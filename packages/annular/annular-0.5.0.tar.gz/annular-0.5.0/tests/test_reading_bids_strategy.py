from unittest.mock import Mock

import numpy as np
import pandas as pd
import pytest

from annular.satellite_model import ReadingBidsStrategy


@pytest.fixture(scope="module")
def bids_table(data_dir):
    """Fixture to load the bids table from a CSV file."""
    bids = pd.read_csv(data_dir / "reading_bids/bids_table.csv", parse_dates=["timestamp"])
    bids["timestamp"] = pd.to_datetime(bids["timestamp"], utc=True)
    bids = bids.set_index(["exclusive_group_id", "profile_block_id", "timestamp"])
    return bids


@pytest.fixture
def reading_bids_strategy(data_dir):
    """Initialization of the ReadingBidsStrategy."""
    return ReadingBidsStrategy(
        bids_csv_path=data_dir / "reading_bids/bids_table.csv",
        ceiling_price=100,
        rolling_horizon_step=24,
        start_hour=0,
        num_hours=24,
    )


def test_reading_bids_strategy_initialization(reading_bids_strategy):
    """Test that the ReadingBidsStrategy initializes correctly."""
    assert isinstance(reading_bids_strategy, ReadingBidsStrategy)
    assert isinstance(reading_bids_strategy.bids, pd.DataFrame)
    assert len(reading_bids_strategy.timestamps) == 168
    assert (
        reading_bids_strategy.start_time
        == reading_bids_strategy.FIRST_TIMESTAMP
        == pd.Timestamp("2024-01-01 00:00:00", tz="UTC")
    )
    assert reading_bids_strategy.increment == pd.Timedelta(hours=24)
    assert reading_bids_strategy.cycle_length == 3  # 3 days in the bids table
    assert reading_bids_strategy.num_cycles == 0
    assert reading_bids_strategy.LAST_TIMESTAMP == pd.Timestamp("2024-01-03 23:00:00", tz="UTC")


def test_reading_bids_strategy_meet_demand(reading_bids_strategy):
    """Test that `meet_demand` correctly updates start time and does not care about given values."""
    assert reading_bids_strategy.start_time == pd.Timestamp("2024-01-01 00:00:00", tz="UTC")
    reading_bids_strategy.meet_demand(market_price=None, demand_met=None)
    assert reading_bids_strategy.start_time == pd.Timestamp("2024-01-02 00:00:00", tz="UTC")
    reading_bids_strategy.meet_demand(market_price=np.array([0] * 24), demand_met=np.array([0] * 24))
    assert reading_bids_strategy.start_time == pd.Timestamp("2024-01-03 00:00:00", tz="UTC")


def test_reading_bids_strategy_determine_bids(reading_bids_strategy, bids_table):
    """Test that the ReadingBidsStrategy returns the correct bids each time determine_bids is called."""
    timestamps = bids_table.index.get_level_values("timestamp")
    days = pd.date_range(start="2024-01-01", periods=4, freq="D", tz="UTC")
    mask_day_1 = (days[0] <= timestamps) & (timestamps < days[1])
    mask_day_2 = (days[1] <= timestamps) & (timestamps < days[2])
    mask_day_3 = (days[2] <= timestamps) & (timestamps < days[3])

    # Day 1
    bids_first_day = reading_bids_strategy.determine_bids()
    assert isinstance(bids_first_day, pd.DataFrame)
    pd.testing.assert_frame_equal(bids_table[mask_day_1], bids_first_day)
    reading_bids_strategy.meet_demand(None, None)

    # Day 2
    bids_second_day = reading_bids_strategy.determine_bids()
    assert isinstance(bids_second_day, pd.DataFrame)
    pd.testing.assert_frame_equal(bids_table[mask_day_2], bids_second_day)
    reading_bids_strategy.meet_demand(None, None)

    # Day 3
    bids_third_day = reading_bids_strategy.determine_bids()
    assert isinstance(bids_third_day, pd.DataFrame)
    pd.testing.assert_frame_equal(bids_table[mask_day_3], bids_third_day)


def test_reading_bids_strategy_cycle_reset_and_timestamp_update(reading_bids_strategy, bids_table):
    """Test the bidding strategy cycles correctly and updates timestamps when data is exhausted."""
    # Run through the entire bids table to exhaust the data twice so that the num_cycles is incremented 2 times.
    for _ in range(6):
        reading_bids_strategy.determine_bids()
        reading_bids_strategy.meet_demand(None, None)

    # At this point, the number of cycles should be 2, and the start time should be back to the beginning.
    assert reading_bids_strategy.num_cycles == 2
    assert reading_bids_strategy.start_time == reading_bids_strategy.FIRST_TIMESTAMP

    # Get the expected bids as the original bids for the first day but with modified timestamps
    timestamps = bids_table.index.get_level_values("timestamp")
    mask_day_1 = (timestamps >= "2024-01-01") & (timestamps < "2024-01-02")
    expected_bids = bids_table[mask_day_1].copy()

    # Rebuild the index with the expected_timestamps (day 7)
    expected_timestamps = np.tile(pd.date_range(start="2024-01-07 00:00:00", periods=24, freq="h", tz="UTC"), 2)
    expected_bids.index = pd.MultiIndex.from_tuples(
        zip(
            expected_bids.index.get_level_values("exclusive_group_id"),
            expected_bids.index.get_level_values("profile_block_id"),
            expected_timestamps,
        ),
        names=["exclusive_group_id", "profile_block_id", "timestamp"],
    )

    # Test day 7
    bids_day_seven = reading_bids_strategy.determine_bids()
    assert isinstance(bids_day_seven, pd.DataFrame)
    pd.testing.assert_frame_equal(expected_bids, bids_day_seven)


def test_adjust_timestamps():
    """Test adjust_timestamps method."""
    bids = pd.DataFrame(
        {
            "exclusive_group_id": [1] * 24,
            "profile_block_id": [1] * 24,
            "timestamp": pd.date_range(start="2025-01-01 00:00:00", periods=24, freq="h"),
            "quantity": [10] * 24,
            "price": [10] * 24,
        }
    )

    bids = bids.set_index(["exclusive_group_id", "profile_block_id", "timestamp"])

    mock_strategy = Mock()
    mock_strategy.increment = pd.Timedelta(hours=24)
    mock_strategy.num_cycles = 10  # Cycle through the entire dataset 10 times
    mock_strategy.cycle_length = 1  # Number of days for which we have bids that span 24 hours

    # Get new bids after cycling 10 times throught the dataset
    new_bids = ReadingBidsStrategy.adjust_timestamps(mock_strategy, bids)
    new_timestamps = new_bids.index.get_level_values("timestamp")

    expected_timestamps = pd.date_range(start="2025-01-11 00:00:00", periods=24, freq="h")
    expected_timestamps.name = "timestamp"

    pd.testing.assert_index_equal(new_timestamps, expected_timestamps)
