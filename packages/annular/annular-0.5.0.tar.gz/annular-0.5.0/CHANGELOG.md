# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
-

### Changed
-

### Removed
-

## [0.5.0] - 2025-12-04

### Added
- Add implementation of two basic tariffs in the MultiProfileBiddingStrategy: volumetric time of use and a capacity tariff ([!115](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/115))
- Add documentation: installation instructions, example usage, and user-facing bidding strategy explanations ([!114](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/114))
- Add `TariffManager` class to handle tariff data loading and addressing based on preselected category and timestamps ([!113](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/113#note_352972))
- Add `OptimizationModelManager` class to handle model instantiation and solving. ([!97](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/97))


## [0.4.0] - 2025-09-25

### Added
- Add CLI option to set verbosity. ([!90](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/90) & [!102](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/102))
- Add ReadingBidsStrategy that reads bids from a CSV file. If the simulation horizon is longer than the data in the CSV, the strategy simply cycles through the exhausted data. ([!86](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/86))
- Add CLI script entry: after installing, you can now call `annular run [CONFIG FILES]` in your terminal to run simulations. ([!84](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/84))

### Changed
- Market prices are now calculated as the dual of the power balance constraint. This implies that market prices can be determined by either the generation or demand side. [!105](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/105))
- Bugfix: the `scheduled_demand` reported to each satellite model is now indexed by the entire bidding window. ([!102](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/102))
- Bugfix: `market.csv` output now correctly contains market price, generator dispatch and satellite consumption. ([!96](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/96))
- Bugfix: MultiProfileBiddingStrategy was creating 'supply' bids instead of 'demand' bids and vice versa. ([!90](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/90))
- Any paths specified in configuration files are now assumed to be relative to the configuration file they are specified in. ([!88](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/88))
- Results folder creation has changed: now based on config file name, no longer includes datetimestamp, and raises error if it already exists. ([!87](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/87))
- The folder with satellite results has been renamed from
  `f"results_folder/satellite_{config_name}_results"` to `"results_folder/config_name"`. ([!85](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/85))
- Initialization of the bidding strategies.
  - Argument names changed to be consistent with configuration file keys:
    - "carrier_prices" to "carrier_prices_path"
    - "electricity_price_forecast" to "forecasts_path"
    - "demands" to "demands_path"
  - By default, it expects strings pointing to `.csv`
    files with data.
  - A classmethod `from_file` has been added to initialize with a strategy-specific
    configuration file and a dictionary of common settings instead.

### Removed
- Configuration files for simulation, generators, and satellites are no longer copied into the results folder. Automatic satellite config file expansion has been disabled. ([!87](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/87))
- The `OptimizerBiddingStrategy` and `HeuristicBiddingStrategy` are no longer
available ([!85](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/85)).


## [0.3.0] - 2025-07-30

### Added
- Add MultiProfileBiddingStrategy that takes a price forecast, derives multiple scenarios from it, determines a demand profile for each, and submits those profiles in an exclusive group. ([!71](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/71))
- Add support for profile block bids and exclusive groups thereof. ([!76](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/76))
  - A profile block is a collection of bids for multiple timestamps that have the same `profile_block_id`. All bids in a profile block are accepted or rejected together, based on their weighted average price.
  - An exclusive group is a collection of profile blocks of which at most one is accepted. Exclusive groups are encoded by sharing an `exclusive_group_id`. Note: a profile block must exist in a single exclusive group to be treated as such, otherwise they are treated as individual bids.
- Add SimpleMultiHourBiddingStrategy that can submit bids for multiple timestamps in one go, by picking one timestamp per flexible demand. ([!61](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/61))

### Changed
- Renamed package from 'demoses-coupling' to 'annular' ([!80](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/80))
- OptimizerBiddingStrategy no longer calculates bids for prices above ceiling price. ([!77](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/77))
- When exchanging bids, the index is no longer expected to be `timestamps, demand`, but is now `exclusive_group_id, profile_block_id, timestamp`. The `bid_price` column has also been renamed to just `price`. ([!76](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/76))
  - All bidding strategies have been updated to match this new format.
  - As part of this change, all submitted bids are no longer treated as being 100% curtailable. For individual bids that are not submitted as part of a profile block, this means they are individually non-curtailable.

### Removed
- Removed all obsolete ISGT files. ([!81](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/81))
- Paths given through configuration files are no longer assumed relative to the project's root. Instead, the paths should either be specified as absolute, or should be valid relative to the process' working directory.
- The `pyprojroot` package has been moved to be only a dev dependency. ([!78](https://gitlab.tudelft.nl/demoses/demoses-coupling/-/merge_requests/78))


## [0.2.0] - 2025-04-19

### Added
- OptimizerBiddingStrategy now takes in separate dataframes for electricity price forecasts
  and fixed prices for other energy carriers such as methane ([!49](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/49))
- Satellite models now support 'expanding' a generic configuration into multiple specific configurations:
  Optimizer-bidding-strategy can now specify a folder as `model_config_path`, where a specific configuration will be
  made for each model configuration in that folder. The original configuration remains unchanged, and specific configs
  are stored in the `results_path` location. ([!46](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/46))
- Migrate market model implementation from pypsa/linopy to pyomo ([!44](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/44))
- Add support for arbitrary numbers of satellite models ([!43](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/43))
- Add satellite model based on (simple) optimization model, works for 1h rolling step ([!38](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/38))
- Add consumer model that solves using rolling horizon
- Add logistic price scaling function for HeuristicBiddingStrategy
- Add shift parameter for price scaling functions for HeuristicBiddingStrategy
- Add code style preferences to README.dev.md

### Changed
- Bid prices are no longer determined naively based on linear interpolation from ceiling to floor price. Instead, bid prices are now determined based on the opportunity costs of shifting to a different time or different energy carrier. ([!62](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/62))
- Simulations are no longer restricted to a rolling step size of 1 timestamp, but can now be run for
  arbitrary window sizes, with 24h being the intended (but not hardcoded) size.
  ([!54](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/54))
- The Market clearing price is now determined solely by the marginal cost of generators. That is, only the generation side (but not the demand side) sets the market price. ([!56](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/56))
- Optimizer-bidding-strategy is now updated to be compatible with the latest version of `Cronian`([!45](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/45))
- Expected model coupling settings (ymmsl) file adjusted: only 'settings' part is expected.
  Components and Ports now hardcoded specified as part of `main()`.
  Satellite models are now specified through a "satellite_configs" key, pointing to a folder containing separate yml files per satellite. ([!43](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/43))
- Optimizer-bidding-strategy can now use a co_optimization specified model instead of built-in hardcoded model ([!40](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/40))
- make satellite_model subpackage
- specify SatelliteModel interface as ABC with abstractmethods
- Flexible demand given to HeuristicBiddingStrategy is now interpreted as ahead-shiftable instead of delay-shiftable ([!39](https://gitlab.tudelft.nl/demoses/annular/-/merge_requests/39))

### Removed
- Removed Constant and Repeating bidding strategies


## [0.1.1]

### Added
- Add CLI argument to specify output format
- Add ymax argument to plot_simulation_results
- automatically transform input timeseries to valid for queue strategy

### Changed
- fix: list complete co-optimization results path in README instructions
- results stored with timestamp
- replace renewable_capacity file with calculation based on supply and capacity factors files
- reduce and simplify plot output files
- update figure sizes for ISGT paper
- update README instructions

### Removed
- remove examples folder: use input/ and tests/data/;


## [0.1.0] - 2024-07-31

- initial release


[Unreleased]: https://gitlab.tudelft.nl/demoses/annular/compare/v0.5.0...HEAD
[0.5.0]: https://gitlab.tudelft.nl/demoses/annular/-/releases/v0.5.0
[0.4.0]: https://gitlab.tudelft.nl/demoses/annular/-/releases/v0.4.0
[0.3.0]: https://gitlab.tudelft.nl/demoses/annular/-/releases/v0.3.0
[0.2.0]: https://gitlab.tudelft.nl/demoses/annular/-/releases/v0.2.0
[0.1.1]: https://gitlab.tudelft.nl/demoses/annular/-/releases/v0.1.1
[0.1.0]: https://gitlab.tudelft.nl/demoses/annular/-/releases/v0.1.0
