import numpy as np
import pandas as pd
import pytest

from annular.utils import patch_expected_price


@pytest.fixture
def sample_horizon():
    """Fixture providing a 48-hour horizon starting from 2024-01-01."""
    return pd.date_range(start="2024-01-01 00:00:00+00:00", periods=48, freq="h", tz="UTC")


@pytest.fixture
def scenario_forecast(sample_horizon):
    """Fixture for a specific scenario forecast."""
    rng = np.random.default_rng(seed=987654321)
    forecast = rng.integers(low=90, high=110, size=sample_horizon.shape[0])
    return pd.DataFrame({"e_price": forecast}, index=sample_horizon)


@pytest.fixture
def base_forecast():
    """Fixture providing a base forecast with 72 hours of data."""
    timestamps = pd.date_range(start="2024-01-01 00:00:00+00:00", periods=72, freq="h", tz="UTC")
    base_prices = [100.0 + i * 0.5 for i in range(72)]

    forecast = pd.DataFrame({"e_price": base_prices}, index=timestamps)
    return forecast


def test_patch_expected_price(base_forecast, scenario_forecast):
    """Test that forecast is correctly replaced by scenario forecast."""
    result = patch_expected_price(base_forecast, base_forecast.index, scenario_forecast)
    assert len(result) == base_forecast.shape[0]
    scenario_length = scenario_forecast.shape[0]
    expected = (
        scenario_forecast["e_price"].tolist()[:scenario_length] + base_forecast["e_price"].tolist()[scenario_length:]
    )
    assert np.array_equal(np.array(result), np.array(expected)), "Forecast not constructed correctly"
