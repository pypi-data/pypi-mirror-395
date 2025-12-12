import math
from pathlib import Path

import numpy as np
import pandas as pd

from .satellite_model import SatelliteModel


class ReadingBidsStrategy(SatelliteModel):
    def __init__(self, bids_csv_path: Path | str, **kwargs):
        """Bidding strategy that reads bids from a CSV file.

        This strategy loads bids from a CSV file once during initialization.
        When its `determine_bids` method is called, it identifies the next set
        of timestamps to provide bids for, shifting by `rolling_horizon_step`
        timestamps every iteration. It then reads bids for this set of
        timestamps from the loaded bids.

        When it reaches the end of the data, it cycles back to the beginning
        and starts serving the same bids again, but with the timestamps
        adjusted forward by however many time increments have passed.

        The data in the CSV does not need to span a perfect multiple of e.g. 24
        hours. If the data ends at a shorter time (e.g., 11:00:00), the strategy
        will only serve the available bids and then reset to the beginning for
        the next cycle.

        The strategy expects the CSV file to have the following columns:

        +--------------------+------------------+-----------+----------+-------+
        | exclusive_group_id | profile_block_id | timestamp | quantity | price |
        +--------------------+------------------+-----------+----------+-------+
        | ...                | ...              | ...       | ...      | ...   |
        +--------------------+------------------+-----------+----------+-------+

        Args:
            bids_csv_path: Path to the CSV file containing the bids.
            rolling_horizon_step: How many snapshots to advance at every
                iteration, ie, for how many snapshots bids need to be made.
            **kwargs: Additional keyword arguments, which are currently ignored.
        """
        super().__init__(**kwargs)

        self.bids = self.read_multi_index_csv_with_utc_timestamps(bids_csv_path)

        self.timestamps = self.bids.index.get_level_values("timestamp")
        self.start_time = self.FIRST_TIMESTAMP = self.timestamps.min()
        self.LAST_TIMESTAMP = self.timestamps.max()
        self.increment = pd.Timedelta(hours=self.rolling_horizon_step)
        self.num_cycles = 0
        self.cycle_length = math.ceil((self.LAST_TIMESTAMP - self.start_time) / self.increment)

    def determine_bids(self) -> pd.DataFrame:
        """Returns the bids from next timestamp."""
        horizon = self._get_horizon()
        mask = self.timestamps.isin(horizon)
        bids_table = self.bids[mask].copy()

        bids_table = self.adjust_timestamps(bids_table)

        return bids_table

    def meet_demand(self, market_price: np.ndarray | None, demand_met: np.ndarray | None) -> None:
        """No model for processing the demand_met, but forwards internal current timestep by 24 hours."""
        self.start_time += self.increment
        if self.LAST_TIMESTAMP < self.start_time:
            self._reset_cycle()

    def _get_horizon(self) -> pd.Index:
        """Select the relevant horizon index values at the current timestep.

        Returns:
            Pandas Index object of the selected horizon values.
        """
        end_time = self.start_time + self.increment
        mask = (self.start_time <= self.timestamps) & (self.timestamps < end_time)
        return self.timestamps[mask].unique()

    def _reset_cycle(self) -> None:
        """Starting a new cycle."""
        self.num_cycles += 1
        self.start_time = self.FIRST_TIMESTAMP

    def adjust_timestamps(self, bids_table: pd.DataFrame) -> pd.DataFrame:
        """Adjusts the timestamps in the bids table based on the current cycle.

        Args:
            bids_table: DataFrame containing the bids with timestamps to adjust.

        Returns:
            DataFrame containing the bids with adjusted timestamps.
        """
        time_shift = self.increment * self.num_cycles * self.cycle_length
        new_timestamps = bids_table.index.get_level_values("timestamp") + time_shift

        index_tuples = [
            (exclusive_group_id, profile_block_id, timestamp)
            for exclusive_group_id, profile_block_id, timestamp in zip(
                bids_table.index.get_level_values("exclusive_group_id"),
                bids_table.index.get_level_values("profile_block_id"),
                new_timestamps,
            )
        ]

        bids_table.index = pd.MultiIndex.from_tuples(
            index_tuples, names=["exclusive_group_id", "profile_block_id", "timestamp"]
        )

        return bids_table

    @staticmethod
    def read_multi_index_csv_with_utc_timestamps(bids_csv_path) -> pd.DataFrame:
        """Reads a multi-index CSV file with UTC timestamps."""
        bids = pd.read_csv(bids_csv_path, parse_dates=["timestamp"])
        bids["timestamp"] = pd.to_datetime(bids["timestamp"], utc=True)
        bids = bids.set_index(["exclusive_group_id", "profile_block_id", "timestamp"])
        return bids
