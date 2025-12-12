"""
This module serves as the entry point for processing command-line arguments
related to configuration and workflow initialization. It configures logging,
retrieves configuration details, and initializes workflows based on the parsed
command-line arguments.
"""

import argparse
import logging
import os
import sys
import yaml
from coauthor.utils.logger import Logger
from coauthor.utils.config import get_config, save_config_dump
from coauthor.modules.workflow import initialize_workflows
from coauthor.utils.export import export
from coauthor import __version__


def main():
    """
    Parses command-line arguments, sets up logging, retrieves configuration,
    and initializes workflows.

    The function uses argparse to handle command-line arguments, sets up a logger based
    on the provided or default log level and log file path, and retrieves configuration
    details. It then initializes workflows using the collected configuration and logger.

    Command-line arguments:

    --config_path: Path to the configuration file.

    --profile: Name of profile (e.g., obsidian, python, hugo).

    --watch: Flag to enable watch mode.
    --scan: Flag to enable scan mode.
    --debug: Flag to set log level to DEBUG.
    --log_file: Path to the log file.
    --export: Flag to enable export mode.
    """
    parser = argparse.ArgumentParser(description="Process arguments to select steps")
    parser.add_argument(
        "--config_path",
        type=str,
        help="Path to the configuration file",
    )
    version_str = f"coauthor {__version__}"
    parser.add_argument("--version", action="version", version=version_str)
    parser.add_argument(
        "--profile",
        type=str,
        help="Name of profile e.g. obsidian, python, hugo, ansible-collection",
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Flag to enable watch mode",
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Flag to enable scan mode",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Flag to set log level to DEBUG",
    )
    parser.add_argument(
        "--log_file",
        type=str,
        help="Path to the log file",
    )
    parser.add_argument(
        "--notify",
        action="store_true",
        help="Flag to enable desktop notifications",
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help="Flag to enable export mode",
    )
    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    if args.log_file:
        log_file = args.log_file
    else:
        log_file = f"{os.getcwd()}/coauthor.log"
    logger = Logger(__name__, log_file=log_file, level=log_level)
    config = get_config(logger=logger, args=args)
    if args.debug:
        save_config_dump(config, logger)
    config["args"] = args
    if args.export:
        export(config=config, logger=logger)
    else:
        initialize_workflows(config, logger)


if __name__ == "__main__":  # pragma: no cover
    main()
