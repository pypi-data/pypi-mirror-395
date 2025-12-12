# coauthor_file_processor.py

"""
This module provides file processing functionalities such as modifying file
contents to a specific pattern, replacing content based on regex patterns,
and including external file contents within a file based on regex matches.
"""

import re
import time
import os
from coauthor.utils.match_utils import file_path_match
from coauthor.utils.jinja import render_content


def pong(config, logger):
    """
    Modifies the contents of a file referenced in the configuration, updating
    it to the string "pong" if it does not already contain that string.

    Args:
        config (dict): Configuration dictionary containing the "current-task"
            with a "path-modify-event" key denoting the file to modify.
        logger (Logger): Logger for recording informational and debug messages.
    """
    path = config["current-task"]["path-modify-event"]
    logger.info("Running pong file processor " + path)
    time.sleep(3)
    with open(path, "r") as file:
        file_contents = file.read()
    if file_contents != "pong":
        logger.info(f'Updating {path} to "pong"')
        with open(path, "w") as f:
            f.write("pong")


def regex_replace_in_file(config, logger):
    """
    Applies regex pattern replacements to the contents of a file, altering
    its content based on provided regex patterns and replacements.

    Args:
        config (dict): Configuration dictionary with "current-task" spec which
            includes file path and regex patterns for replacement.
        logger (Logger): Logger for recording informational and debug messages.

    Returns:
        bool: True if the file content was changed, False otherwise.
    """
    task = config["current-task"]
    path = task["path-modify-event"]
    path_match = file_path_match(config, logger)
    if not path_match:
        logger.debug(f"regex_replace_in_file: no path match for {path}")
        return False
    patterns = task["patterns"]

    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    original_content = content

    for pattern_set in patterns:
        logger.debug(f"regex_replace_in_file: {path}, patterns: {pattern_set}")
        pattern = pattern_set["regex"]

        internal_regex = pattern_set.get("internal_regex")
        internal_replace = pattern_set.get("internal_replace")
        if internal_regex and internal_replace:
            content = re.sub(
                pattern,
                lambda match: re.sub(
                    internal_regex,
                    internal_replace,
                    match.group(0),
                ),
                content,
            )
        else:
            replace = pattern_set["replace"]
            content = re.sub(pattern, replace, content)

    if content == original_content:
        logger.debug("regex_replace_in_file: no content was changed")
        return False

    logger.info(f"Regex patterns changed file {path}, patterns: {patterns}")
    task["content"] = content
    with open(path, "w", encoding="utf-8") as file:
        time.sleep(3)
        file.write(content)
    return True


def include_file(config, logger):
    """
    Includes content from an external file into a target file based on regex
    matches. Useful for dynamically embedding file contents.

    Args:
        config (dict): Configuration dictionary containing the task definition
            such as target file path, regex pattern, and additional parameters.
        logger (Logger): Logger for recording informational and debug messages.

    Returns:
        bool: True if the file was updated with new content, False otherwise.
    """
    task = config["current-task"]
    path = task["path-modify-event"]

    regex = re.compile(task["regex"], re.DOTALL)
    logger.debug(f"regex: {regex}")

    updated = False
    match_found = False

    with open(path, "r", encoding="utf-8") as main_file:
        content = main_file.read()

    logger.debug(f"content: {content}")
    for match in regex.finditer(content):
        match_found = True
        include_file_path = match.group("path") if "path" in match.groupdict() else match.group(1)
        logger.debug(f"Match found {include_file_path} → {path}")

        if "dir" in task:
            if os.path.isabs(task["dir"]):
                include_file_path_abs = os.path.join(task["dir"], include_file_path)
            else:
                current_dir = os.getcwd()
                include_file_path_abs = os.path.abspath(os.path.join(current_dir, task["dir"], include_file_path))
        else:
            include_file_path_abs = include_file_path
        try:
            with open(include_file_path_abs, "r", encoding="utf-8") as inc_file:
                include_file_content = inc_file.read()
        except FileNotFoundError:
            if not os.path.isabs(include_file_path):
                logger.error(
                    f"Include file not found: {include_file_path_abs}. Ensure this relative path is correct from the executing directory."
                )
            else:
                logger.error(f"Include file not found: {include_file_path_abs}")
            continue

        task["include_file_path"] = include_file_path
        task["include_file_path_abs"] = include_file_path_abs
        task["include_file_content"] = include_file_content
        task["match"] = match

        task["match_groups"] = {name: match.group(name) for name in match.groupdict() if match.group(name)}
        logger.debug(f"Match groups: {task['match_groups']}")

        new_content = render_content(task, task["template"], config, logger)

        if "indent" in match.groupdict():
            indent = match.group("indent")
            new_content = "\n".join(indent + line for line in new_content.splitlines())
            new_content = new_content.replace(f"{indent}\n", "\n")  # empty lines should have indentation
        else:
            logger.debug('Code has no indentation, there is no named capturing group "indent"')

        if new_content != match.group(0):
            updated = True
            content = content.replace(match.group(0), new_content)
            logger.debug(f"new_content: \n{new_content}")
            logger.info(f"File {include_file_path} was included in {path}")

    if not match_found:
        logger.debug(f"No match found for {path}")
        return False

    if not updated and match_found:
        logger.debug(f"Content is up to date in {path}")
        return False

    with open(path, "w", encoding="utf-8") as file:
        time.sleep(1)
        file.write(content)
    return True
