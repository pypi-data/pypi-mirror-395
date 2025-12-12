# Example Usage

## Command-line interface

An annular simulation can be started from the command line by passing a configuration
file to the `annular run` command. By default, output will be written to a
folder called `results/`.

```bash
annular run simulation_config.ymmsl
```

You can specify your own folder using the optional `-o/--output` flag:

```bash
annular run simulation_config.ymmsl -o path/to/results/location
```

This will set up all the models as specified in the `simulation_config.ymmsl`,
and all results will appear in a `path/to/results/location/simulation_config/`
folder that will be created.

Note that the subfolder name `simulation_config` is taken from the configuration
filename that was passed in. If the folder already exists, the program will exit
and no simulation will be run. You will have to (re)move the old results, rename
your configuration file or specify a new results folder in order to run a new
simulation.

Finally, you can start simulations based on multiple configurations by passing
in multiple configuration files when calling `annular run`:

```bash
annular run simulation_config_1.ymmsl simulation_config_2.ymmsl simulation_config_3.ymmsl
```

which is equivalent to

```bash
annular run simulation_config_1.ymmsl
annular run simulation_config_2.ymmsl
annular run simulation_config_3.ymmsl
```

Any output path specified with `-o` will be used for all simulations.

## In a Python script

To run an annular simulation from a Python script, you can import the `run`
function, and provide it with the location of a configuration file:

```python
from pathlib import Path
from annular.coupling import run

run(Path("simulation_config.ymmsl"))
```

This is similar to running a simulation through the commandline as shown before.
A results folder can be passed in as an optional argument to `run`:

```python
run(Path("simulation_config.ymmsl"), Path("path/to/results/location"))
```

Note that this function does not support passing in multiple configuration
files, so you will have to loop over those yourself:

```python
for config_file in ["file1.ymmsl", "file2.ymmsl", "file3.ymmsl"]:
    run(Path(config_file))
```
