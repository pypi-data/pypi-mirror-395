# Multi-Profile Bidding Strategy

The `MultiProfileBiddingStrategy` is an advanced bidding strategy that simulates multiple scenarios
to determine its bids. These scenarios cover various common ways in which the market price can
deviate from predictions, to encourage the use of available flexibility through the power bids.

## Configuration

The `MultiProfileBiddingStrategy` has various parameters to configure to perform its function. They
are listed below with an explanation.

```{admonition} Important: Relative Paths
All paths are interpreted as relative to the location of the configuration file they are specified
in. This is the recommended usage. Alternatively, paths can be given as absolute, although this is
discouraged for the sake of reproducibility across different machines.
```

### Mandatory Attributes

These attributes are mandatory: the strategy cannot function without this information.

- `cronian_config_path`

  In order to run its internal simulations, the `MultiProfileBiddingStrategy` requires an internal
  model of its operation. This model will be built using the [cronian] package, through a cronian
  configuration file. This argument should be the location of that file.

  Note: if this model does not contain any way of being flexible with how power is consumed, please
  consider using a different bidding strategy instead, as all scenarios will result in equal bids,
  wasting computational effort.

- `demands_path`

  As part of the cronian model, a demand timeseries can be specified for each asset through a name.
  The CSV file at this path will be used as the source for the timeseries specified in the
  `cronian_config_path`.

- `forecasts_path`

  This path should point to a CSV file containing an `e_price` column, that will be treated as the
  predicted electricity price during the simulation.

- `carrier_prices_path`

  This path should point to a CSV file containing prices to be used if an energy carrier other than
  electricity, such as methane or hydrogen, can be used. The column names in this file should match
  exactly the other energy carrier used in the model.

### Optional Attributes

These attributes are optional, since defaults are defined:

- `tariff_path` default: `None`

  This path should point to the folder containing only CSV files with all
  relevant tariff information for this simulation. These files are treated as
  read-only, so can be shared between multiple satellite models. The tariffs are
  detected based on their filenames, as described in further detail below. Any
  unused files are ignored. If this folder is specified, the necessary files for
  all relevant tariffs have to be provided. Any missing files will cause errors.

- `tariff_categories` default: `None`

  If the tariff files contain categorical index columns, this attribute should
  be used to select the appropriate category for this bidding strategy. If a
  category is not specified for any of the category columns present in the
  tariff data files, it will result in too much data being provided, leading to
  errors and undefined behavior. The categories should be specified nested under
  this attribute, e.g.

  ```
  tariff_categories:
    Grid level: distribution
    ...
  ```

  This attribute is ignored if `tariff_path` is not specified.

- `floor_price` default: 0

  The floor price is the minimum price used in all bids. By default, this is set to 0. Negative
  floor prices should be possible, although this has not been tested. This value should also be
  lower than the ceiling price.

- `horizon_size` default: 48

  The horizon size determines the number of timesteps for which the underlying model will be run. It
  is strongly recommended to set this value yourself rather than blindly relying on the default 48.
  Since the bidding window is fixed at 24 timesteps, this also serves as lower bound for this value.

- `cronian_storage_model` default: `simple`

  Storage assets in cronian that operate under the default `simple` storage model are easy to use,
  but may encounter simultaneous charging and discharging. If this problem occurs, this value can
  be changed to `complex`. This adds additional constraints to prevent this behavior, at the cost
  of some extra computation time.

- `forecast_scaling_factor` default: 1.5

  While the shape of the scenarios used by this strategy are fixed, this scaling factor is a
  tunable parameter that determines how aggressive the strategy should be in considering these
  alternative scenarios. For example, for some scenarios, the expected power usage at some time
  will be adjusted to 1.5x the original forecast amount at the default value of `1.5`.
  Setting this value to `1` effectively disables this scaling behavior. Values at or below 1 are
  not recommended, and may result in unexpected behavior.

### Inherited From Global Simulation Settings

Within Annular, the following attributes are inherited from the global simulation configuration by
default. By specifying them for `MultiProfileBiddingStrategy`, you overwrite the global value for
just this instance, leaving the rest of the simulation unaffected.

- `rolling_horizon_step`

  Defines the number of timesteps for the bidding window. Raises an error if anything other than 24.

- `ceiling_price`

  The maximum price per unit of power specified by the market. Reducing this value changes the
  maximum price of bids made by this bidding strategy. Note that doing so may result in some
  unshiftable or uncurtailable bids not being satisfied, leading to infeasible solutions and
  invalid intermediate states. Increasing this beyond the global ceiling price has no effect.

- `start_hour`

  If unchanged, assumes that the given timeseries for demand and prices have the same start as the
  central market data. If this data is offset differently, this parameter should be adjusted to
  match the data that should be used by this bidding strategy.

- `num_hours`

  Specifies the length of data that should be used during the simulation, and therefore also
  defines the length of the simulation. Will cause problems if set to a value lower than that of the
  global `num_hours`.

- `output_path`

  During a simulation, bids sent to the central market, and dispatch results based on power received
  from the market are logged as csv files in this output_path. This value is derived from the global
  `results_folder` setting (passed in as CLI argument, set to `results/` by default), in which a
  dedicated folder is created for this bidding strategy, using the name of the config file
  specifying these very values. If given, must be an existing path. Just like the other paths, this
  path is interpreted to be relative to the location of this config file.

## Tariffs

The `MultiProfileBiddingStrategy` has support for including various [tariffs] into its bidding
process. To enable these, the `tariff_path` and `tariff_categories` settings should be configured,
as described later. The currently supported tariffs are:
- volumetric time of use charge
- maximum capacity charge

### Volumetric
The volumetric time of use tariff should be provided in a file called `volumetric.csv`. For each
timestamp in the rolling horizon window, the appropriate value for this tariff will be retrieved
using the `TariffManager.fetch_timeseries()` functionality. As part of the cost objective, this
tariff value is multiplied with the amount of power drawn from the grid as an additional cost.

### Maximum Capacity Charge
The maximum capacity tariff should be provided in a file called `capacity_charge_yearly.csv`. These
values will be retrieved using the `TariffManager.fetch_value()` functionality, so no temporal index
columns are expected. The value retrieved will be multiplied by the maximum used capacity until now
as part of the cost objective.

```{admonition} Implementation detail
The maximum used capacity across all iterations is kept track of in an internal separate variable.
Using constraints, the maximum of this 'maximum so far' and the power draw for each timestamp in the
rolling horizon window is then determined.
```


<!-- References -->
[cronian]:  https://cronian.readthedocs.io/latest/
[tariffs]:  project:../tariffs.md
