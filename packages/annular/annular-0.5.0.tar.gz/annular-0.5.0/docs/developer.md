# Development

This page contains instructions for how to work with this repository as a
developer. Please read the [CONTRIBUTING.md] and
[README.dev.md], so you are aware of the contribution process and
style guide before contributing any code to this repository.

## Installation instructions

If you want to actively develop on Annular, it is recommended to clone the
repository, and do an editable installation with the developer requirements:

```bash
git clone git@gitlab.tudelft.nl:demoses/annular.git
cd annular
# create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Use `source .venv/Scripts/activate` on Windows
python3 -m pip install -e ".[dev]"
```

### Pre-commit

We recommend activating the included pre-commit configuration to run linting,
formatting and tests before committing.

```bash
pre-commit install  # install the git hooks to run before committing
pre-commit run  # test if pre-commit is configured correctly
```

Note that the pre-commit configuration omits a number of longer running
tests marked as `integration` to keep the commit iteration loop fast.

### Tests

Tests are run through pytest:

```bash
pytest  # run all tests
```

#### Run with coverage

To get an in-terminal overview of the current state of test coverage, you can
run pytest with `--cov`:

```bash
pytest --cov --cov-report term-missing
```

#### Run in parallel

Using the `pytest-xdist` plugin, tests can be run in parallel which may speed up
longer runs, especially when the integration tests are included. Note that all
tests using MUSCLE3 should be run in their own group, since multiple MUSCLE3
processes will otherwise conflict on trying to write to the same performance
database file. The `worksteal` option is recommended to more equally divide the
remaining tests over the other workers.

```bash
# At the time of writing, 3 groups works best
pytest -n 3 --dist loadgroup --dist worksteal
```

<!-- References -->

[CONTRIBUTING.md]: https://gitlab.tudelft.nl/demoses/annular/CONTRIBUTING.md
[README.dev.md]:   https://gitlab.tudelft.nl/demoses/annular/README.dev.md
