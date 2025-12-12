"""Script to profile the running time of bid determination."""

import argparse
import cProfile
import tempfile
from pathlib import Path

from annular.satellite_model import MultiProfileBiddingStrategy


def common_args() -> dict[str, int]:
    """Provides arguments for `SatelliteModel` that are common across subclasses."""
    common_args = {
        "rolling_horizon_step": 24,
        "ceiling_price": 200,
        "start_hour": 1,
        "num_hours": 2400,
    }

    return common_args


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", default="output", type=str, help="Store profiling output in *outout.prof")

    args = parser.parse_args()

    data_dir = Path("tests/data/")

    with tempfile.TemporaryDirectory() as output_path:
        multi_profile_args = {
            "demands_path": str(data_dir / "multi_profile/loads_generators_timeseries.csv"),
            "forecasts_path": str(data_dir / "multi_profile/forecast-prices.csv"),
            "carrier_prices_path": str(data_dir / "multi_profile/price_other_carriers.csv"),
            "cronian_config_path": str(data_dir / "multi_profile/prosumers/P01.yaml"),
            "floor_price": 0,
            "horizon_size": 48,
            "output_path": str(output_path),
        }

        input_args = common_args() | multi_profile_args

        strategy = MultiProfileBiddingStrategy(**input_args)

        filename = f"{args.output}.prof"
        cProfile.run("strategy.determine_bids()", filename)
