#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Console script for geogravL3."""


from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
import sys
import os

from geogravl3 import __version__
from geogravl3.config import load_configuration, path_testdata
from geogravl3.pipeline import run_pipeline
from geogravl3.data_downloads.downloads import download_resources
from geogravl3.utils.utils import get_resource_dir

default_config_file = os.path.join(path_testdata, "default_config.json")


def get_argparser():
    """Get a console argument parser for geogravL3."""
    parser = ArgumentParser(
        prog='geogravL3',
        description='geogravL3 command line argument parser',
        epilog="use '>>> geogravL3 -h' for detailed documentation and usage hints."
    )

    parser.add_argument('--version', action='version', version=__version__)

    # --- subparsers ---
    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        required=True
    )

    # ---- run_pipeline CLI command ----
    parser_run = subparsers.add_parser(
        'run_pipeline',
        formatter_class=ArgumentDefaultsHelpFormatter,
        description='Run the geogravL3 processing pipeline.',
        help='Run the geogravL3 processing pipeline.'
    )
    parser_run.add_argument(
        'path_config',
        type=str,
        help='Path to the configuration file (JSON or XML format).'
    )
    parser_run.set_defaults(func=get_config_and_run_pipeline)

    # ---- download_resources CLI command ----
    parser_dl = subparsers.add_parser(
        'download_resources',
        formatter_class=ArgumentDefaultsHelpFormatter,
        description='Download required resource files explicitly. If resources are not '
                    'downloaded prior to the execution of "run_pipeline", resources are '
                    'downloaded automatically.',
        help='Download required resource files explicitly. If resources are not '
                    'downloaded prior to the execution of "run_pipeline", resources are '
                    'downloaded automatically.'
    )
    parser_dl.add_argument(
        '-d', '--resources_dir',
        type=str,
        default=get_resource_dir().as_posix(),
        nargs='?',
        help='Custom directory where to store the downloaded resource files.'
    )
    parser_dl.set_defaults(func=run_download_resources)

    return parser


def get_config_and_run_pipeline(args: Namespace):
    """
    Entry point for the 'run_pipeline' CLI command.

    Parameters
    ----------
    args : Namespace
        argparse.Namespace instance of already parsed arguments

    Raises
    ------
    OSError
        Failed to load the configuration JSON/XML file.
    ValueError
        Wrong file extension of the configuration file.
    """
    # check the current directory
    print(f"Current Directory: {os.getcwd()}")

    # download resource files if not already downloaded or running within a local repository
    download_resources()

    config = load_configuration(args.path_config)

    # run the pipeline (only if not running in CI test mode)
    if os.environ.get('IS_CI_TEST', 'False') != 'True':
        run_pipeline(config_dict=config)


def run_download_resources(args: Namespace = None):
    """Entry point for the 'download_resources' CLI command."""
    download_resources(args.resources_dir)
    print("Resource download completed.")


def main(parsed_args: Namespace = None) -> int:
    """Run the argument parser and forward the arguments to the linked functions.

    Parameters
    ----------
    parsed_args : Namespace
        argparse.Namespace instance of already parsed arguments
        (allows to call main() from test_cli_parser.py while passing specific arguments)

    Returns
    -------
    int : exitcode (0: all fine, >=1: failed)

    Raises
    ------
    SystemExit
        If the geogravL3 main process fails to run.
    """
    if not parsed_args:
        parsed_args: Namespace = get_argparser().parse_args()

    parsed_args.func(parsed_args)

    print("geogravL3 succeeded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
