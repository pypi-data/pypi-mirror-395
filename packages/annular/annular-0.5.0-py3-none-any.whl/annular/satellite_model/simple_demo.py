import logging
from collections import namedtuple
from operator import itemgetter
from pathlib import Path

import numpy as np
import pandas as pd
from cronian.feasible_consumption import parse_flex_amount
from more_itertools import bucket

from annular.utils import read_csv_with_utc_timestamps
from .satellite_model import SatelliteModel

logger = logging.getLogger(__name__)


class SimpleMultiHourBiddingStrategy(SatelliteModel):
    def __init__(
        self,
        demands_path: str,
        forecasts_path: str,
        floor_price: int = 0,
        bid_margin: float = 0.05,
        horizon_size: int = 48,
        **kwargs,
    ):
        """Simple multi-hour bidding strategy to bid for the lowest expected price at the cheapest expected hour.

        Demand is specified at its deadline. Any specified flexibility means it
        can be satisfied in any of the `n` earlier timesteps.

        Args:
            demands_path (str): Path to csv file with demand values per timestamp,
                with different flexibility as
                separate columns named 'flex+N'.
            forecasts_path (str): Path to csv file with electricity price
                forecast information. If multiple forecasts columns are given,
                each is used in parallel to determine the bid curves. If
                only a single forecast is given, it will be adjusted using the
                `bid_curve_resolution` parameter to generate multiple forecasts
                in place.
            floor_price (int): Minimum price to bid at, defaults to 0.
            bid_margin (float): [0, ...) Amount of margin as a fraction to bid over the
                lowest found price within the look-ahead window. Example: 0.05
                is interpreted as bidding 5% on top of the lowest found price.
            horizon_size (int): full length of the horizon to use for an optimization
                iteration, i.e., bidding window + look ahead period, in number
                of snapshots.
            kwargs: Any other keyword arguments are passed to the initialization of
                the base class.
        """
        super().__init__(**kwargs)

        self._last_bids: list[Bid] = []
        self.cur_timestamp_idx = 0

        self.floor_price = floor_price
        self.bid_margin = bid_margin
        self.horizon_size = horizon_size

        self.demands = read_csv_with_utc_timestamps(Path(demands_path))
        self.forecasts = read_csv_with_utc_timestamps(Path(forecasts_path))

        # Assumption: no flexibility beyond look-ahead horizon
        assert max(parse_flex_amount(d) for d in self.demands.columns) + self.rolling_horizon_step <= self.horizon_size

    def determine_bids(self) -> pd.DataFrame:
        """Determine when in the next bidding window we bid, and at what price.

        A bid is roughly determined as follows for each listed demand quantity:

        - Find the time of the cheapest expected price in the bidding window,
          i.e., the period for which bids have to be submitted.
        - If the flexibility extends _beyond_ the current bidding window, find
          the cheapest expected price within the available flexibility, and
          place a bid at that price + margin.
        - If there is no flexibility beyond the current bidding window, bid at
          the ceiling price instead.

        Returns:
            A collection of bids covering the next bid window.
        """
        logger.debug("Determining bids")
        bidding_window = self._get_horizon(self.rolling_horizon_step)
        if len(bidding_window) == 0:
            # Return a valid-to-unpack empty dataframe since the run has ended.
            return pd.DataFrame(
                data=np.zeros((1, 2)),
                columns=["quantity", "price"],
                index=pd.MultiIndex.from_tuples(
                    [(1, 1, self.demands.index[-1])], names=["exclusive_group_id", "profile_block_id", "timestamp"]
                ),
            )

        horizon_forecast = self.forecasts.loc[self._get_horizon()]
        bids = []
        group_idx = AutoIncrement()
        for demand_name, demand_column in self.demands.items():
            if demand_name in {"base", "flex+0"}:  # base case: bid at ceiling price
                bids.extend(
                    Bid(group_idx(), 0, time, q, self.ceiling_price, demand_name, time_idx)
                    for time_idx, (time, q) in enumerate(demand_column.loc[bidding_window].items())
                    if q != 0
                )
                continue

            flexibility = parse_flex_amount(demand_name)
            # Look at any demand that may be satisfied within current bidding window
            # I.e., rolling horizon step size + maximum amount of flexibility
            demand_horizon = self._get_horizon(self.rolling_horizon_step + flexibility)
            for time_idx, q in enumerate(demand_column.loc[demand_horizon]):
                if q == 0:
                    continue
                bid_time, bid_price = self._make_bid(time_idx, flexibility, horizon_forecast)
                bids.append(Bid(group_idx(), 0, bid_time, q, bid_price, demand_name, time_idx))

        # Remember which bids were made for when meeting demand later.
        self._last_bids = bids

        # Make sure there's at least a 0-bid for every timestamp, which don't have to be remembered
        timestamps_with_bids = {bid.timestamp for bid in bids}
        bids = bids + [
            Bid(group_idx(), 0, bid_time, 0, 0, 0, 0)
            for bid_time in bidding_window
            if bid_time not in timestamps_with_bids
        ]
        bids.sort(key=itemgetter(2))  # sort by timestamp
        bids_table = pd.DataFrame.from_records(
            bids, columns=Bid._fields, index=["exclusive_group_id", "profile_block_id", "timestamp"]
        )

        if self.output_path:
            bids_csv_file_name = self.output_path / "bids.csv"
            bids_table.to_csv(bids_csv_file_name, mode="a", header=not bids_csv_file_name.exists())

        # Don't return any additional columns that are only used for internal bookkeeping
        return bids_table[["quantity", "price"]]

    def meet_demand(self, market_price: np.ndarray | None, demand_met: np.ndarray | None) -> None:
        """Update the internal state to record the amount of demand that was met.

        Ensures all demand met is removed from the 'demand yet to be satisfied',
        and advances the internal 'clock' by one rolling horizon step.

        Args:
            market_price: Price of electricity as provided per timestep.
            demand_met: Amount of demand that was met at the market price per timestep.

        Raises:
            AssertionError: if any of the provided demand is under- or over-used.
            ValueError: if any mandatory demand has not been satisfied by the given demand.
        """
        logger.debug("Meeting demand")
        if demand_met is None:
            return

        demand_horizon = self._get_horizon()

        # Group by timestamp of the bid
        groups = bucket(self._last_bids, key=lambda x: x.timestamp)
        for timestamp, price, demand in zip(demand_horizon, market_price, demand_met):
            # Sort bids per timestamp from highest to lowest bid_price
            group = sorted(groups[timestamp], key=lambda x: x.price, reverse=True)
            if not group:
                continue
            for bid in group:
                if abs(demand) <= 1e-8 or bid.price < price:
                    break
                self.demands.at[demand_horizon[bid.time_idx], bid.demand_name] -= min(demand, bid.quantity)
                demand -= min(demand, bid.quantity)
            assert abs(demand) <= 1e-8

        # Confirm that all mandatory demand has been met
        if self.demands.loc[demand_horizon[: self.rolling_horizon_step]].sum(axis=1).sum() > 0:
            raise ValueError("Demand with deadline in this bidding window has not been met")

        if self.output_path:
            # Filter for non-zero supplied demand
            horizon = self._get_horizon()
            supplied_demand = [
                (t, price, demand) for t, price, demand in zip(horizon, market_price, demand_met) if demand > 1e-8
            ]

            # Save dispatch output
            dispatch_csv_file_name = self.output_path / "dispatch.csv"
            pd.DataFrame.from_records(supplied_demand, columns=["timestamp", "price", "demand"]).to_csv(
                dispatch_csv_file_name, mode="a", header=not dispatch_csv_file_name.exists(), index=False
            )

        self.cur_timestamp_idx += self.rolling_horizon_step

    def _get_horizon(self, length: int = None) -> pd.Index:
        """Select the relevant horizon index values at the current timestamp index.

        Args:
            length: length of the desired horizon in number of timestamps.
                Uses `self.horizon_size` when `None` is given.

        Returns:
            Pandas Index object of the selected horizon values.
        """
        if length is None:
            length = self.horizon_size
        end_idx = self.cur_timestamp_idx + length
        horizon = pd.Index(self.demands.index[self.cur_timestamp_idx : end_idx])
        return horizon

    def _make_bid(self, time_idx: int, flexibility: int, prices_forecast: pd.DataFrame) -> tuple[pd.Timestamp, float]:
        """Give bid time and price for demand at given time and flexibility.

        Args:
            time_idx: integer index of the demand that could be fulfilled within
                this bidding window
            flexibility: how many timesteps early this demand could be satisfied
            prices_forecast: forecast of electricity prices for the whole
                horizon in which the demand might be satisfied.

        Returns:
            tuple: Expected best timestamp for the bid (always
            within current bidding window) and the price for the bid.
        """
        # What is the earliest time at which can be bid for this demand?
        earliest_bid_index = max(0, time_idx - flexibility)

        # Determine bid_time:
        if time_idx <= self.rolling_horizon_step:
            bid_price = self.ceiling_price  # bids for demand within bidding window are at ceiling price
        else:
            # What is the minimum price within the window in which we can consume this demand?
            bid_price = prices_forecast.iloc[earliest_bid_index : time_idx + 1].min().item()
            bid_price *= 1 + self.bid_margin

        # Determine bid_price:
        # At what time-index in the *current rolling horizon window* are prices cheapest?
        tmp = prices_forecast.iloc[earliest_bid_index : self.rolling_horizon_step]
        bid_time_idx = tmp["e_price"].argmin()
        # Get the actual timestamp value for use in the bids table.
        bid_time = prices_forecast.index[earliest_bid_index + bid_time_idx]
        return bid_time, bid_price


Bid = namedtuple(
    "Bid",
    [
        # Bids table index
        "exclusive_group_id",
        "profile_block_id",
        "timestamp",
        # Bids table values
        "quantity",
        "price",
        # Bookkeeping: which original demand did this bid come from?
        "demand_name",
        "time_idx",
    ],
)


class AutoIncrement:
    def __init__(self):
        """An auto-incrementing index counter starting at 0."""
        self.value = -1  # value is incremented before use, so -1 becomes 0 at first call.

    def __call__(self):
        """When called, increment the value by 1 and return."""
        self.value += 1
        return self.value
