# Defining a basic simulation

The first step before running a simulation is defining it. For annular, this is
done as a collection of configuration and data files. Here, we will introduce
everything necessary for a basic simulation that you can expand or change to
suit your needs. You can download the example [here](example.com/download),
which contains the following folders and files:

```
energy-system-simulation/
├── simulation-configuration.ymmsl  (1)
├── generators/                     (2)
│   └── G01.yaml
├── satellite-configurations/       (3)
│   ├── battery-flexible.yml
│   └── cronian-configurations/     (4)
│       └── P01.yml
└── csv_files/
    ├── availability_factors.csv
    ├── battery-flexible-demand.csv
    └── ...
```

For each of the numbered files/folders, the corresponding section below will
give some explanation and an example of the relevant files. This folder
structure might seem excessive for a small example, but if you stick to it for
your own simulations, it will help keep your files organized. The most important
aspect of this structure is that the complete collection of files in the
top-level folder can be a self-contained configuration. The simulation run will
work no matter where on your filesystem you move the folder to, as long as the
relative references between files stay intact.

```{admonition} Paths must be relative
For the sake of consistency and ease of referring to configurations from
anywhere, whenever a path is defined in a configuration file, it is treated as
**relative to the configuration file it's defined in**. This means that as long
as all files related to a simulation are located together in a single folder,
the referred files will always be found regardless of where the simulation is
started from. This also means you can easily move all files related to a
simulation around, without having to adjust any path references to other files.
```

## 1. Annular configuration file

The base configuration of an annular simulation is given in the
`simulation_configuration.ymmsl` file. This file serves two main functions:

1. defining a few fixed parameters for the coupled simulation
2. defining any number of global settings that will be accessible to all
   satellite models unless specifically overwritten.

```{literalinclude} example-project/simulation-configuration.ymmsl
:language: yaml
:caption: simulation-configuration.ymmsl
```

The following configuration settings are expected:

- `generator_configs`: Folder containing [cronian] configurations for the generators
  to be included in the central market model. Note: only 'Generators' get loaded
  from this folder.
- `timeseries_data_path`: Path to a CSV file containing the hourly availability
  timeseries for the generators.
- `satellite_configs`: Folder containing configuration files defining the
  bidding strategies for the satellite models.

These keys are needed to set up the coupled simulation, and will not be made
available to satellite models. All remaining keys will be passed through to all
satellite models in the simulation. Of these keys, the following four are
required:

- `ceiling_price`: The market-wide ceiling price for bids. Bids at this price
  are guaranteed to be satisfied.
- `start_hour`: Integer offset of where to start in the previously specified
  `timeseries_data`.
- `num_hours`: Length of the simulation in number of hours.
- `rolling_horizon_step`: Length of the rolling horizon step, i.e., number of
  hours for which bids are exchanged at every simulation iteration. Currently,
  only `24` is supported.

The `start_hour` and `num_hours` keys can be used to run smaller simulations
from a larger data file. For example, if the `timeseries_data_path` contains
data on years 2009-2015, a simulation can be run only for the year 2011 by
specifying:

```yaml
start_hour: 17520  # skip 2 * 8760 hours
num_hours: 8760
```

## 2. Cronian generator configuration files

This folder should contain any number of [cronian] configuration files
that specify the known supply side of the energy market. Generators defined here
are modelled directly into the market clearing optimization problem.

The example contains a single generator of offshore wind power with a linear cost:

```{literalinclude} example-project/generators/G01.yml
:language: yaml
:caption: G01.yml
```

## 3. Satellite definitions & resources

This folder contains the files defining the satellite models. Each satellite
model will in turn be run in an independent process during the coupled
simulation, that behaves according to the bidding strategy defined in it.

These configuration files have only one mandatory key from annular's point of
view: `strategy`. This has to be a name that matches one of the available
bidding strategies. The remaining values in the file will be processed by the
selected strategy, so see its documentation for more information.

In this example we use a [MultiProfileBiddingStrategy], that models some demand
that can be flexibly satisfied through the use of a battery:

```{literalinclude} example-project/satellite-configurations/satellite-config.yml
:language: yaml
:caption: satellite-config.yml
```

Note that for the CSV files, we are referring to `../csv-files/`. This is
because that folder is a 'sibling' folder of the `satellite-configurations/`
folder in which this `satellite-config.yml` file is located.

## 4. Nested files for satellite models

A bidding strategy such as the MultiProfileBiddingStrategy example above
commonly depends on some further data or configuration. To keep those neatly
organized, we recommend storing that information in a dedicated folder inside
your `satellite-configurations/` folder. In this case, we store the cronian
configuration in a `cronian-configurations/` subfolder for it and any potential
other cronian configuration files for other satellites.

```{literalinclude} example-project/satellite-configurations/cronian-configurations/P01.yml
:language: yaml
:caption: P01.yml
```


<!-- References -->

[cronian]: https://cronian.readthedocs.io/stable
[MultiProfileBiddingStrategy]: annular.satellite_model.MultiProfileBiddingStrategy
