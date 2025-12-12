from abc import ABC, abstractmethod
from pathlib import Path
from typing import Type, TypeVar

import numpy as np
import pandas as pd
import yaml

T = TypeVar("T", bound="SatelliteModel")


class SatelliteModel(ABC):
    @staticmethod
    def expand_config(configuration: dict) -> dict[str, dict]:
        """Expand a potential meta-configuration to a collection of concrete configurations.

        Basic case: no config 'expansion' is supported, so the configuration is
        returned in a list for datastructure consistency.

        Args:
            configuration: A configuration dictionary.

        Returns:
            configurations: The configuration wrapped in a dictionary with empty string as a key.
        """
        return {"": configuration}

    @classmethod
    def from_file(cls: Type[T], config_file: Path, **common_settings: dict) -> T:
        """Initialize a strategy from a yaml file.

        Args:
            config_file: Path to configuration file.
            common_settings: A dictionary with additional keyword arguments.
                Arguments specified in config_file take precedence over arguments
                specified in common settings.

        Any values given under keys ending in `_path` will be treated as
        relative to the given configuration file: they will be explicitly
        replaced with `<config_file.parent>/<value>`. As a result, absolute
        paths are not supported when initializing from a configuration file.

        If the config file or the common settings include a key `results_folder`,
        a setting key `output_path` is created as concatenation of the value
        of `results_folder` and the name of the config file. The `results_folder`
        key is deleted from the settings.
        """
        with config_file.open() as f:
            config_dict = yaml.safe_load(f)
        settings = common_settings | config_dict

        for key, value in settings.items():
            if key.endswith("_path"):
                settings[key] = f"{config_file.parent}/{value}"

        if "results_folder" in settings:
            settings["output_path"] = f"{settings['results_folder']}/{config_file.stem}"
            del settings["results_folder"]
        return cls(**settings)

    @abstractmethod
    def __init__(
        self,
        rolling_horizon_step: int,
        ceiling_price: float,
        start_hour: float,
        num_hours: int,
        output_path: str | None = None,
        **kwargs,
    ):
        """Base class for satellite models.

        Create a satellite model that can bid for demand between floor and
        ceiling price.

        Args:
            rolling_horizon_step: How many snapshots to advance at every
                iteration, ie, for how many snapshots bids need to be made.
            ceiling_price: Maximum price to bid at, at which demand
                will always be satisfied.
            start_hour: The starting time of the simulation.
            num_hours: The length of the simulation time horizon.
            output_path: Path to the directory to store intermediate
                values such as bids and dispatch. If given, a target directory
                is created.
            **kwargs: Any other keyword arguments are ignored.

        """
        self.rolling_horizon_step = rolling_horizon_step
        self.ceiling_price = ceiling_price
        self.start_hour = start_hour
        self.num_hours = num_hours
        self.output_path = Path(output_path) if output_path else None
        if self.output_path:
            self.output_path.mkdir(exist_ok=True, parents=True)

    @abstractmethod
    def meet_demand(self, market_price: np.ndarray | None, demand_met: np.ndarray | None) -> None:
        """Update internal state according to the amount of demand met and record market price."""
        raise NotImplementedError

    @abstractmethod
    def determine_bids(self) -> pd.DataFrame:
        """Determine the next set of bids based on the current internal state."""
        raise NotImplementedError
