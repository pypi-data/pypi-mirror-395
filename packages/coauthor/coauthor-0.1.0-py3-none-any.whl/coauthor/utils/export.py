"""Module for exporting coauthor profiles.

This module provides functions to export predefined profiles, including configuration files and templates,
to the current working directory. It handles file copying, checks for existing files, and displays differences
if conflicts are found.
"""

import importlib.resources
import pathlib
import shutil
from difflib import unified_diff


def export(config, logger):
    """Export a coauthor profile based on the provided configuration.

    This function checks if a profile is specified in the configuration arguments. If not, it lists available
    profiles and returns early. Otherwise, it calls the export_profile function to perform the export.

    Args:
        config (dict): Configuration dictionary containing command-line arguments.
        logger (logging.Logger): Logger instance for logging messages.

    Returns:
        None: If no profile is provided or on successful export.
    """
    args = config["args"]

    if not args.profile:
        profiles_path = importlib.resources.files("coauthor.profiles")
        profiles = [p.name for p in profiles_path.iterdir() if p.is_dir()]
        logger.info("Please provide a profile using --profile, for example --profile <profile-name>")
        logger.info("Available profiles: " + ", ".join(profiles))
        return

    profile = args.profile
    export_profile(profile, logger)


def is_files_equal(source, target):
    """Check if two files have identical content.

    This function compares the content of two files by reading them in chunks of 8192 bytes.
    It returns True if the files are identical, False otherwise.

    Args:
        source (pathlib.Path): Path to the source file.
        target (pathlib.Path): Path to the target file.

    Returns:
        bool: True if the files are equal, False otherwise.
    """
    with source.open("rb") as fsrc, target.open("rb") as ftgt:
        while True:
            buffer1 = fsrc.read(8192)
            buffer2 = ftgt.read(8192)
            if buffer1 != buffer2:
                return False
            if not buffer1:
                return True


def export_file(source, target, logger):
    """Export a file from source to target, handling existing files.

    If the target file does not exist, it creates the necessary directories and copies the file.
    If the target exists, it checks if the content is identical. If identical, logs a message.
    If different, logs the differences using unified diff.

    Args:
        source (pathlib.Path): Path to the source file.
        target (pathlib.Path): Path to the target file.
        logger (logging.Logger): Logger instance for logging messages.
    """
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        with source.open("rb") as fsrc, target.open("wb") as ftgt:
            shutil.copyfileobj(fsrc, ftgt)
        logger.info(f"Created {target}")
    else:
        if is_files_equal(source, target):
            logger.info(f"Already exported: {target}")
        else:
            logger.info(f"File exists but is different: {target}")
            with source.open() as fsrc, target.open() as ftgt:
                source_lines = fsrc.readlines()
                target_lines = ftgt.readlines()
            diff = unified_diff(target_lines, source_lines, fromfile=str(target), tofile=str(source))
            logger.info("Diff:\n" + "\n".join(diff))


def export_config(profile_path, logger):
    """Export the configuration file (config.yml) from the profile to the current directory.

    Copies config.yml to .coauthor.yml in the current working directory if it exists in the profile.
    Uses export_file to handle the copying and logging.

    Args:
        profile_path (pathlib.Path): Path to the profile directory.
        logger (logging.Logger): Logger instance for logging messages.
    """
    config_source = profile_path / "config.yml"
    if not config_source.is_file():
        logger.warning(f"config.yml not found in profile {profile_path.name}")
        return

    config_target = pathlib.Path.cwd() / ".coauthor.yml"
    export_file(config_source, config_target, logger)


def export_templates(profile_path, logger):
    """Export the templates directory from the profile to the current directory.

    Recursively walks through the templates directory, ignoring specified folders like __pycache__,
    and exports each file to .coauthor/templates in the current working directory.
    Uses export_file for individual file handling.

    Args:
        profile_path (pathlib.Path): Path to the profile directory.
        logger (logging.Logger): Logger instance for logging messages.
    """
    templates_source = profile_path / "templates"
    if not templates_source.is_dir():
        logger.warning(f"templates directory not found in profile {profile_path.name}")
        return

    ignored_folders = ["__pycache__"]

    def walk(trav):
        yield trav
        if trav.is_dir():
            for sub in trav.iterdir():
                if sub.is_dir() and sub.name in ignored_folders:
                    continue
                yield from walk(sub)

    target_base = pathlib.Path.cwd() / ".coauthor" / "templates"
    for source_path in walk(templates_source):
        if source_path.is_file():
            rel_path = source_path.relative_to(templates_source)
            target_path = target_base / rel_path
            export_file(source_path, target_path, logger)


def export_profile(profile, logger):
    """Export a specific coauthor profile.

    This function exports the configuration file (config.yml) and templates directory from the specified
    profile to the current working directory. It handles creation of new files, skips ignored folders,
    checks for file equality, and logs differences using unified diff if files differ.

    Args:
        profile (str): Name of the profile to export.
        logger (logging.Logger): Logger instance for logging messages.
    """
    logger.info(f"Exporting profile {profile}")

    profile_path = importlib.resources.files("coauthor.profiles") / profile
    if not profile_path.is_dir():
        logger.error(f"Profile {profile} not found")
        return

    export_config(profile_path, logger)
    export_templates(profile_path, logger)
