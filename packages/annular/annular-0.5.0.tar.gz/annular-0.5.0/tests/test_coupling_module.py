"""Tests for the annular coupling.py module."""

from pathlib import Path

import numpy as np
import pandas as pd
import parse
import pytest
from libmuscle import Grid, Message
from ymmsl import Model

from annular.coupling import prepare_results_folder, run, summarize_scheduled_demand
from annular.coupling_components import (
    compact_bids_to_msg,
    compact_market_info_to_msg,
    extract_bids_from_msg,
    extract_market_info_from_msg,
    get_coupling_setup,
)
from tests.conftest import compare_objects


@pytest.mark.parametrize("market_info", ["sample_market_info", "empty_market_info"])
def test_compact_market_info_to_msg(market_info, request):
    """Test compact_market_info_to_msg returns message with right keys."""
    market_info = request.getfixturevalue(market_info)
    msg = compact_market_info_to_msg(*market_info)
    assert isinstance(msg, Message)
    assert isinstance(msg.data, dict)
    for i, (key, grid) in enumerate(msg.data.items()):
        if grid is not None:
            assert isinstance(grid, Grid)
            assert isinstance(grid.array, np.ndarray)
        if key in ["price", "scheduled_demand"]:
            expected = market_info[i]
            assert compare_objects(msg.data[key], expected)


@pytest.mark.parametrize(
    "market_info_msg,market_info",
    [
        ("sample_market_info_msg", "sample_market_info"),
        ("empty_market_info_msg", "empty_market_info"),
    ],
)
def test_extract_market_info_from_msg(market_info_msg, market_info, request):
    """Test extract_market_info_from_msg returns the right data and types."""
    market_info = request.getfixturevalue(market_info)
    market_info_msg = request.getfixturevalue(market_info_msg)
    extracted = extract_market_info_from_msg(market_info_msg)
    assert isinstance(extracted, type(market_info))
    for expected, actual in zip(market_info, extracted):
        assert compare_objects(actual, expected)


@pytest.mark.parametrize("market_info", ["sample_market_info", "empty_market_info"])
def test_market_info_inversion(market_info, request):
    """Test market_info compacting and extracting are inverse of each other."""
    market_info = request.getfixturevalue(market_info)
    msg = compact_market_info_to_msg(*market_info)
    inverted = extract_market_info_from_msg(msg)
    for actual, expected in zip(inverted, market_info):
        assert isinstance(actual, type(expected))
        assert compare_objects(actual, expected)


@pytest.mark.parametrize("num_satellites", [1, 3, 11])
def test_coupling_configuration(num_satellites):
    """Test the standard model coupling configuration."""
    coupling_config = get_coupling_setup("test_config", num_satellites)
    assert isinstance(coupling_config, Model)
    assert len(coupling_config.conduits) == 2
    assert len(coupling_config.components) == 2
    assert coupling_config.components[1].multiplicity[0] == num_satellites


def test_compact_bids_to_msg(sample_message, sample_dataframe):
    """Test compact_bids_to_msg."""
    msg = compact_bids_to_msg(sample_dataframe, timestamp=0)
    assert isinstance(msg, Message)
    assert isinstance(msg.data, dict)
    for key, grid in msg.data.items():
        assert isinstance(grid, Grid)
        assert isinstance(grid.array, np.ndarray)
        if key in ["price", "quantity"]:
            assert np.allclose(grid.array, sample_message.data[key].array)


def test_extract_bids_from_msg(sample_message, sample_dataframe):
    """Test extract_bids_from_msg."""
    df = extract_bids_from_msg(sample_message)
    assert isinstance(df, pd.DataFrame)
    assert df.equals(sample_dataframe)


def test_bids_inversion(sample_message, sample_dataframe):
    """Test compacting and extracting bids are inverse of each other."""
    assert sample_dataframe.equals(extract_bids_from_msg(compact_bids_to_msg(sample_dataframe, timestamp=0)))
    msg = compact_bids_to_msg(extract_bids_from_msg(sample_message), timestamp=0)
    assert sample_message.timestamp == msg.timestamp
    for col in ["price", "quantity"]:
        assert np.allclose(sample_message.data[col].array, msg.data[col].array)


def test_summarize_scheduled_demand(sample_block_bids):
    """Test that demand bids are summarized to the correct format.

    Specifically:
    - separated per satellite model
    - entries for every timestamp
    - ordered by timestamp
    """
    window_length = 24
    scheduled_bids = sample_block_bids.copy()
    # arbitrary 'scheduled' values that are sorted high->low per satellite,
    # since the rest of the inserted values should be 0.
    scheduled_bids["scheduled"] = [30, 20, 10, 0, 0, 0, 15, 10, 5, 0, 0, 0, 3, 2, 1]
    window = pd.date_range(start=scheduled_bids.index.get_level_values("timestamp")[0], periods=window_length, freq="h")

    summarized = summarize_scheduled_demand(scheduled_bids, window)

    assert len(summarized) == len(scheduled_bids.index.get_level_values("satellite").unique())
    for summarized_per_satellite in summarized.values():
        assert len(summarized_per_satellite) == window_length
        assert (sorted(summarized_per_satellite, reverse=True) == summarized_per_satellite).all()


@pytest.mark.parametrize(
    "config_file",
    ["test_multi_hour.ymmsl", "test_reading_bids.ymmsl"],
    ids=["multi-hour", "reading-bids"],
)
def test_results_folder_creation(config_file, data_dir, tmp_path):
    """Test that the correct results folder is created."""
    settings = prepare_results_folder(data_dir / config_file, tmp_path)
    results_folder = settings["results_folder"]
    assert results_folder.startswith(str(tmp_path))
    assert results_folder.endswith(config_file.split(".")[0])


@pytest.mark.integration
@pytest.mark.xdist_group("muscle3")
@pytest.mark.gurobi
@pytest.mark.parametrize(
    "config_file,expected_names",
    [
        (Path("test_multi_profile.ymmsl"), {"hydrogen"}),
        (Path("test_reading_bids.ymmsl"), {"consumer"}),
    ],
    ids=["multi-profile", "reading-bids"],
)
def test_main(config_file, expected_names, data_dir, tmp_path):
    """Test main in coupling.py."""
    run(data_dir / config_file, results_path=tmp_path)
    file_path_1 = Path("muscle3.central.log")
    with open(file_path_1, "r") as file:
        lines = file.read().splitlines()
    assert "done" in lines

    template = "market_price and demand_met for satellite {satellite} at timestep: {}"
    found_names = set()
    for idx in range(len(expected_names)):
        file_path_2 = Path(f"muscle3.satellite[{idx}].log")
        with open(file_path_2, "r") as file:
            lines = file.read().splitlines()

        matches = [match for line in lines if (match := parse.parse(template, line))]
        assert any(matches)
        found_names.add(matches[0]["satellite"])

    assert found_names == expected_names
