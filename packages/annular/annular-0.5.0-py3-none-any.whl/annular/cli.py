import argparse
import logging
from pathlib import Path

from annular.coupling import run


def cli_main() -> None:
    """CLI function for running an annular simulation using config files."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    run_parser = subparsers.add_parser("run")

    run_parser.add_argument(
        "config_files",
        nargs="+",
        type=Path,
        help="Configuration files to run simulations for.",
    )
    run_parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="Controls the level of verbosity in the logging output: -v for INFO, -vv for DEBUG",
    )
    run_parser.add_argument("-o", "--output", type=Path, help="Output directory", default=Path("./results/"))
    args = parser.parse_args()

    log_level = 10 * (3 - args.verbose)  # logging.WARNING = 30, logging.INFO = 20, logging.DEBUG = 10
    logging.basicConfig(level=log_level)

    for config_file in args.config_files:
        run(config_file, args.output)
