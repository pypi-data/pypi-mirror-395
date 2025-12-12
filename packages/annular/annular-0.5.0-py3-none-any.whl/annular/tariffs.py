import datetime
from collections.abc import Mapping
from functools import reduce
from numbers import Real
from operator import and_, attrgetter
from pathlib import Path
from typing import Type, TypeVar

import pandas as pd
from dateutil.easter import easter

T = TypeVar("T", bound="TariffManager")


class TariffManager:
    def __init__(self, tariff_data: dict[str, pd.Series]):
        """A manager object for energy network tariffs.

        Includes support for intelligently parsing timestamps to various
        time-based indexing options. Tariffs are retrievable by
        (case-insensitive) name through various `fetch_*` methods.

        Args:
            tariff_data: Dictionary where keys are tariff names and
                values are series of tariff values and indices.
        """
        self.data = {key.casefold(): value for key, value in tariff_data.items()}

    @classmethod
    def from_folder(cls: Type[T], path: Path, preselect: Mapping[str, str | Real]) -> T:
        """Create a TariffManager from csv files in a folder.

        Args:
            path: Path to the folder with tariff data in csv format.
            preselect: Dictionary specifying the category within the tariff.
                Any tariff may be indexed both categorically and temporally.
                This `preselect` argument should at least specify a value for
                each categorical index, i.e., column in the tariff file.
                E.g.: `{"grid level": "distribution", "consumer type": "small"}`.
                If any of the categories given to `preselect` are not present in
                the tariff data, they are silently ignored.
        """
        data = {}
        for file in path.iterdir():
            tariff_name = file.stem
            tariff_table = pd.read_csv(file)
            tariff_table = filter_dataframe(tariff_table, preselect)
            data[tariff_name] = tariff_table

        return cls(data)

    def fetch_value(self, name: str) -> Real:
        """Fetch a single-valued tariff.

        Args:
            name: Name of the tariff.

        Returns:
            Value for a specific tariff.
        """
        tariff = self.data[name.casefold()]
        if not isinstance(tariff, Real):
            raise ValueError("Specified tariff is not a single value.")
        return tariff

    def fetch_timeseries(self, name: str, timestamps: pd.DatetimeIndex) -> pd.Series:
        """Fetch tariff value for each given timestamp.

        Args:
            name: Name of the tariff.
            timestamps: Datetime to use for selecting temporal index levels.

        Returns:
            Series of values for the specified tariff, indexed by the given timestamps.
        """
        tariff = self.data[name.casefold()]

        temporal_indexers = {
            "year": attrgetter("year"),
            "month": attrgetter("month"),
            "weekday/weekend": parse_weekday_weekend,
            "hour": attrgetter("hour"),
        }

        # Prepare parsed versions of the timestamps as columns that can be JOIN-ed to match the tariff values
        timestamp_series = timestamps.to_series()
        timestamps_to_join_to = pd.DataFrame(
            {key: timestamp_series.apply(parser) for key, parser in temporal_indexers.items()}, index=timestamps
        )
        return timestamps_to_join_to.join(tariff, on=tariff.index.names)["value"]

    def fetch_indexed(self, name: str, timestamps: pd.DatetimeIndex) -> pd.Series:
        """Fetch collection of tariff values, relevant to the given timestamps.

        Args:
            name: Name of the tariff.
            timestamps: Datetime to use for selecting temporal index levels.

        Returns:
            Series of tariff values, maintaining its original index, pre-selected with only the relevant values .
        """
        tariff = self.data[name.casefold()]

        temporal_indexers = {
            "year": attrgetter("year"),
            "month": attrgetter("month"),
            "weekday/weekend": parse_weekday_weekend,
            "hour": attrgetter("hour"),
        }

        # Get the unique set of temporal index values from the timestamps
        unique_values = {
            level: {temporal_indexers[level](timestamp) for timestamp in timestamps} for level in tariff.index.names
        }
        # Make a selection mask for each index level
        masks = [tariff.index.isin(unique_values[level], level) for level in tariff.index.names]
        # Combine all masks per level using logical AND
        mask = reduce(and_, masks)
        return tariff[mask]


def filter_dataframe(data: pd.DataFrame, select: Mapping[str, str | int]) -> pd.Series | Real:
    """Filter a dataframe by multiple columns.

    Example:
        Preselect ``{"A": "high", "B": "old"}`` with data =

        ==== === === =====
        A    B   C   value
        ==== === === =====
        high new yes 1
        high new no  2
        high old yes 3
        high old no  4
        low  new yes 5
        low  new no  6
        low  old yes 7
        low  old no  8
        ==== === === =====

        Result:

        === =====
        C   value
        === =====
        yes 3
        no  4
        === =====

    Args:
        data: pandas DataFrame to filter. Must have at least one column named 'value'.
        select: Dictionary where keys are strings or integers, used to select
            only the desired rows from the given data. If a key is present as
            a column name, then only those rows are kept where that column
            matches the matching value from this dictionary.

    Returns:
        A pd.Series of the ``value`` column, where rows are filtered based on
        matching values in `select`. Any columns that were filtered on are
        removed, and any remaining columns are used as a pd.MultiIndex. If the
        series only consists of a single row, then it only returns the value.
    """
    index_cols = [x for x in data.columns if x != "value"]
    data = data.set_index(index_cols)

    selector_values, selector_levels = [], []
    for colname, value in select.items():
        if colname not in data.index.names:
            continue
        selector_values.append(value)
        selector_levels.append(colname)

    if selector_levels:
        data = data.xs(tuple(selector_values), level=selector_levels)
    data = data["value"]
    if len(data) == 1:
        return data.iloc[0]
    return data


def parse_weekday_weekend(date: datetime.date) -> str:
    """Parse the weekday weekend from a date.

    Args:
        date: Date to parse.

    Returns:
        Whether the given date is a weekday or a weekend day.
    """
    # monday is 1, sunday is 7
    if date.isoweekday() in (6, 7) or is_dutch_holiday(date):
        return "weekend"
    else:
        return "weekday"


def is_dutch_holiday(date: datetime.date) -> bool:
    """Check if date is a Dutch holiday, if not already a weekend by definition.

    As of 2013, Dutch holidays are:
    - New Year's Day
    - Good Friday
    - Easter (Sunday and Monday)
    - King's Day
    - Ascension Day
    - Pentecost (sunday and Monday)
    - Christmas (25th and 26th)

    Args:
        date: Date to check.

    Returns:
        True if the given date is a Dutch holiday, False otherwise.
    """
    # New Year's Day, King's Day and Christmas
    # NB: While King's day is moved to the 26th if the 27th is a Sunday, this
    # doesn't matter for us since the 26th is then a Saturday, still weekend.
    fixed_holidays = {(1, 1), (4, 27), (12, 25), (12, 26)}

    # Good Friday, Second Easter day, Ascension day and Pentecost respectively
    easter_adjustments = [datetime.timedelta(days=days) for days in (-2, 1, 39, 50)]
    easter_date = easter(date.year)
    easter_dates = set()
    for adjustment in easter_adjustments:
        adjusted_date = easter_date + adjustment
        easter_dates.add((adjusted_date.month, adjusted_date.day))

    return (date.month, date.day) in fixed_holidays | easter_dates
