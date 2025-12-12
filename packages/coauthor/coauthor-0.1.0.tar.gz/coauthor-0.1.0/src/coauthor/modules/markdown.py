import os
import logging
import yaml
import re
from coauthor.utils.markdown import get_frontmatter
import time


def process_frontmatter(config, logger):
    """
    Processes a Markdown file's frontmatter and includes content from specified files.

    This function uses get_frontmatter to parse the specified Markdown file. If the frontmatter
    contains an `include-files` property (a list of markdown files), it reads and concatenates
    the content of these files into the task's content.

    :param config: Configuration dictionary containing:
        - 'current-task': contains the current task details.
        - 'current-task'['path-modify-event']: path to the markdown file to process.
    :param logger: Logger instance for logging messages and errors.
    :return: Updated config dictionary with modified content.
    """
    task = config["current-task"]
    path = task["path-modify-event"]

    try:
        frontmatter, frontmatter_str, original_content = get_frontmatter(path)
        include_files = frontmatter.get("include-files", [])

        if include_files:
            combined_content = "---\n"
            combined_content += frontmatter_str + "\n---\n\n"

            current_dir = os.path.dirname(os.path.abspath(path))
            for include_path in include_files:
                full_path = include_path
                if include_path.startswith("./"):
                    full_path = os.path.join(current_dir, include_path[2:])

                try:
                    with open(full_path, "r", encoding="utf-8") as include_file:
                        combined_content += include_file.read() + "\n"
                except FileNotFoundError:
                    logger.warning(f"Include file not found: {full_path}")

            # combined_content = combined_content.rstrip("\n") + "\n"
            task["content"] = combined_content
        else:
            task["content"] = original_content

    except Exception as e:
        logger.error(f"Error processing frontmatter: {str(e)}")
        raise

    time.sleep(3)
    return config
