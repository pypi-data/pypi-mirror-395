# Annular

| fair-software.eu recommendations | [![fair-software badge][badge-howfairis]][fair-software]             |
|:---------------------------------|:---------------------------------------------------------------------|
| (1/5) code repository            | [![gitlab repo badge][badge-gitlab]][repo-url]                       |
| (2/5) license                    | [![gitlab license badge][badge-license]][repo-url]                   |
| (3/5) community registry         | [![RSD][badge-rsd]][demoses-rsd]                                     |
| (4/5) citation                   | [![DOI][badge-Zenodo]][Zenodo-url]                                   |
| (5/5) checklist                  | [![FAIR checklist badge][badge-fair-software]][software-checklist]   |
| **Other best practices**         |                                                                      |
| Software Version                 | ![Software Version][badge-repo]                                      |
| Supported Python versions        | ![Supported Python Versions][badge-py-versions]                      |
| Continuous Integration           | ![CI result][badge-ci] [![pre-commit][badge-pre-commit]][pre-commit] |
| Documentation                    | [![Docs Status][badge-docs]][docs]                                   |

## Introduction

Annular is a setup for running coupled energy system models with the aim of
modeling flexibility scheduling and the policy regulations that affect the
behavior of flexibility providers.

Documentation can be found at [annular.readthedocs.io][docs].

### Name
**Why the name 'annular'?**

'Annular' means 'in the shape of a ring', with which we specifically think of
the rings of Saturn, containing many moons or in other words satellites, just
like the satellite models interacting with the central market model.

## Installation

You can install `annular` directly from [PyPI]:

```bash
# Best practice: install in a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Use `source .venv/Scripts/activate` on Windows

python3 -m pip install annular
```

Then you can use annular on the command line to run coupled simulations
specified by config files.

```bash
annular run examples/data/energy_model_coupling.ymmsl
```

Result files will appear in a `results/<CONFIG_FILE_NAME>/` folder, where
`<CONFIG_FILE_NAME>` is the name of the given configuration file.

See the built-in help for further details:

```bash
$ annular run --help
usage: annular run [-h] [--verbose] [-o OUTPUT] config_files [config_files ...]

positional arguments:
  config_files         Configuration files to run simulations for.

options:
  -h, --help           show this help message and exit
  --verbose, -v        Controls the level of verbosity in the logging output: -v for INFO, -vv for DEBUG
  -o, --output OUTPUT  Output directory
```

See the [documentation][docs] for further explanation and examples.

## Contributing

If you want to contribute to the development of annular,
have a look at the [contribution guidelines](CONTRIBUTING.md).

Further instructions can be found in[`README.dev.md`](README.dev.md)

## Citation

For citation information, see [`CITATION.cff`](CITATION.cff)

## Credits

Annular was developed as part of the DEMOSES project, funded by NWO under Grant
ID: ESI.2019.004.

This package was created with [Cookiecutter] and the [NLeSC/python-template][template].

<!-- URLs -->
[Cookiecutter]:         https://github.com/audreyr/cookiecutter
[demoses-rsd]:          https://www.research-software.nl/projects/demoses
[docs]:                 https://annular.readthedocs.io/en/latest/?badge=latest
[fair-software]:        https://fair-software.eu
[pre-commit]:           https://github.com/pre-commit/pre-commit
[PyPI]:                 https://pypi.org/project/annular/
[repo-url]:             https://gitlab.tudelft.nl/demoses/annular
[software-checklist]:   https://fairsoftwarechecklist.net/v0.2?f=31&a=32113&i=32100&r=133
[template]:             https://github.com/NLeSC/python-template
[Zenodo-url]:           https://doi.org/10.5281/zenodo.13144649

<!-- Badges -->
[badge-ci]:             https://gitlab.tudelft.nl/demoses/annular/badges/main/pipeline.svg
[badge-docs]:           https://readthedocs.org/projects/annular/badge/?version=latest
[badge-gitlab]:         https://img.shields.io/badge/gitlab-repo-000.svg?logo=gitlab&labelColor=gray&color=blue
[badge-fair-software]:  https://fairsoftwarechecklist.net/badge.svg
[badge-howfairis]:      https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F-green
[badge-license]:        https://img.shields.io/gitlab/license/demoses/annular?gitlab_url=https://gitlab.tudelft.nl
[badge-pre-commit]:     https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit
[badge-py-versions]:    https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue
[badge-repo]:           https://img.shields.io/badge/version-0.5.0-green
[badge-rsd]:            https://img.shields.io/badge/rsd-annular-00a3e3.svg
[badge-Zenodo]:         https://zenodo.org/badge/DOI/10.5281/zenodo.13144649.svg
