from pathlib import Path

import pandas as pd


def read_csv_with_utc_timestamps(path: Path | str) -> pd.DataFrame:
    """Load a CSV file, using column 0 as index, and converting the index to UTC timestamps.

    Args:
        path: Path to the CSV file.

    Returns:
        DataFrame of the CSV file with index as UTC timestamps.
    """
    df = pd.read_csv(path, index_col=0)
    df.index = pd.to_datetime(df.index, utc=True)
    return df


def patch_expected_price(base_forecast: pd.DataFrame, horizon: pd.Index, forecast: pd.DataFrame) -> list[float]:
    """Create a list of expected prices.

    For the specified horizon, replaces the base forecast with the given forecast.

    Args:
        base_forecast: The base forecast.
        horizon: Time horizon to use.
        forecast: Dataframe with to-be-used forecast.

    Returns:
        A list of expected prices.
    """
    e_price_df = base_forecast.loc[horizon]
    e_price_df.loc[: forecast.index[-1], "e_price"] = forecast["e_price"].values
    return e_price_df["e_price"].tolist()
