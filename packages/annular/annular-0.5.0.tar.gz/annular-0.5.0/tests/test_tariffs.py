import datetime
from numbers import Real
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from annular.tariffs import TariffManager, filter_dataframe, is_dutch_holiday


@pytest.fixture(scope="module")
def preselect():
    """A collection of preselection parameters for the sample_tariff test files."""
    return {
        "Grid level": "distribution",
        "Consumer type": "small",
        "Connected capacity": "1x6A",
        "Connection category": "LS",
    }


@pytest.fixture(scope="module")
def tariff_manager(data_dir, preselect):
    """A sample tariff manager based on the sample_tariff test files directory."""
    tariff_dir = Path(data_dir, "sample_tariffs")
    return TariffManager.from_folder(tariff_dir, preselect=preselect)


def test_init_from_folder(data_dir, preselect):
    """Test class init from a folder."""
    tariff_dir = Path(data_dir, "sample_tariffs")
    manager = TariffManager.from_folder(tariff_dir, preselect=preselect)
    file_names = [f.stem for f in tariff_dir.iterdir()]
    assert set(file_names) ^ set(manager.data.keys()) == set(), "Tariffs do not have the correct names"

    for name in file_names:
        tariff = manager.data[name.casefold()]
        if isinstance(tariff, Real):
            # can't check `.name` of a series when tariff is just a single value.
            continue
        assert isinstance(tariff, pd.Series)
        assert tariff.name == "value"


@pytest.mark.parametrize(
    "select",
    [
        ({"c": "x", "a": 0}),
        ({"c": "x", "a": 1}),
        ({"c": "x"}),
    ],
)
def test_filter_dataframe(select):
    """Test dataframe filtering."""
    rng = np.random.default_rng(123)
    data = {
        "a": list(range(4)) + list(range(4)),
        "b": list(range(8)),
        "c": ["x", "y", "x", "y", "x", "y", "x", "y"],
        "value": rng.random(8),
    }
    data = pd.DataFrame(data)
    result = filter_dataframe(data, select)

    expected_mask = data["c"].isin([select["c"]])
    expected_idx = ["a", "b"]
    if "a" in select:
        expected_mask = expected_mask & data["a"].isin([select["a"]])
        expected_idx.remove("a")

    expected = data.loc[expected_mask].drop(columns=list(select.keys()))
    expected = expected.set_index(expected_idx)["value"]

    pd.testing.assert_series_equal(expected, result)


def test_fetch_single_value(data_dir, tariff_manager):
    """Test that singular tariff values are correctly returned, regardless of temporal indexing."""
    name = "capacity_charge_yearly"

    tariff_df = pd.read_csv(data_dir / f"sample_tariffs/{name}.csv", header=0)
    expected_value = tariff_df["value"].iloc[0]  # we know the first row to be preselected

    assert tariff_manager.fetch_value(name) == expected_value
    # tariff name used should be case-insensitive
    assert tariff_manager.fetch_value(name.upper()) == expected_value
    assert tariff_manager.fetch_value(name.title()) == expected_value


@pytest.mark.parametrize("tariff_name", ["capacity_charge_monthly", "volumetric"])
def test_fetch_value_errors_for_series(tariff_manager, tariff_name):
    """Test that fetch_value gives a ValueError if the fetched tariff is not a single value."""
    with pytest.raises(ValueError):
        tariff_manager.fetch_value(tariff_name)


@pytest.mark.parametrize(
    ["timestamps", "expected_sizes"],
    [
        [pd.date_range(start="2025-01-02", end="2025-01-03", periods=2), (1, 1)],
        [pd.date_range(start="2025-01-01", end="2025-01-02", periods=2), (1, 2)],
        [pd.date_range(start="2025-01-01", end="2025-02-01", periods=2), (2, 1)],
        [pd.date_range(start="2025-01-01", end="2025-04-01", periods=2), (2, 2)],
    ],
)
def test_fetch_single_value_after_temporal_indexing(tariff_manager, timestamps, expected_sizes):
    """Test that a tariff that differs by date, but not by hour is correctly selected."""
    name = "capacity_charge_monthly"
    monthly = tariff_manager.fetch_indexed(name, timestamps=timestamps)
    assert isinstance(monthly, pd.Series)

    expected_level_names = ["month", "weekday/weekend"]
    assert monthly.index.names == expected_level_names

    num_values_per_level = tuple(len(monthly.index.unique(level=name)) for name in expected_level_names)
    assert num_values_per_level == expected_sizes

    # tariff name used should be case-insensitive
    pd.testing.assert_series_equal(monthly, tariff_manager.fetch_indexed(name.upper(), timestamps=timestamps))
    pd.testing.assert_series_equal(monthly, tariff_manager.fetch_indexed(name.title(), timestamps=timestamps))


def test_fetch_hourly_tariff(data_dir, tariff_manager):
    """Test that a tariff that varies hourly can be correctly selected."""
    name = "volumetric"
    timestamps = pd.date_range(start="2025-01-01 00:00", periods=24, freq="h")
    hourly = tariff_manager.fetch_timeseries(name, timestamps)

    tariff_df = pd.read_csv(data_dir / f"sample_tariffs/{name}.csv", header=0)
    # rows 0-576 preselected, of those rows 25-48 are actually relevant for the given timestamps
    expected_value: np.ndarray = tariff_df["value"].iloc[24:48]
    assert np.all(hourly.values == expected_value)

    assert isinstance(hourly, pd.Series)
    assert len(timestamps) == len(hourly)
    assert hourly.name == "value"

    # tariff name used should be case-insensitive
    pd.testing.assert_series_equal(hourly, tariff_manager.fetch_timeseries(name.upper(), timestamps=timestamps))
    pd.testing.assert_series_equal(hourly, tariff_manager.fetch_timeseries(name.title(), timestamps=timestamps))


@pytest.mark.parametrize(
    "date",
    [
        # 2013:
        datetime.date(2013, 3, 29),  # Good Friday
        datetime.date(2013, 4, 1),  # 2nd Easter day
        datetime.date(2013, 5, 9),  # Ascension day
        datetime.date(2013, 5, 20),  # 2nd Pentecost
        # 2019
        datetime.date(2019, 4, 19),  # Good Friday
        datetime.date(2019, 4, 22),  # 2nd Easter day
        datetime.date(2019, 5, 30),  # Ascension day
        datetime.date(2019, 6, 10),  # 2nd Pentecost
        # 2025
        datetime.date(2025, 4, 18),  # Good Friday
        datetime.date(2025, 4, 21),  # 2nd Easter day
        datetime.date(2025, 5, 29),  # Ascension day
        datetime.date(2025, 6, 9),  # 2nd Pentecost
    ],
)
def test_dutch_easter_related_holidays(date):
    """Test that holidays related to Easter are correctly classified as such."""
    assert is_dutch_holiday(date)


def test_dutch_fixed_holidays():
    """Test that fixed holidays are correctly classified as such."""
    for year in range(2013, 2025):
        assert is_dutch_holiday(datetime.date(year, 1, 1))
        assert is_dutch_holiday(datetime.date(year, 4, 27))
        assert is_dutch_holiday(datetime.date(year, 12, 25))
        assert is_dutch_holiday(datetime.date(year, 12, 26))
