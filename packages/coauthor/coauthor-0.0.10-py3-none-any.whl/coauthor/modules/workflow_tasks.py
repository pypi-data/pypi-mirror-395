from coauthor.utils.jinja import render_content
import os


def read_file(config, logger):
    logger.debug(f"config: {config}")
    task = config["current-task"]
    path = task["path-modify-event"]
    logger.info(f"Reading file from {path}")
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    task["content"] = content


def write_file(config, logger):
    logger.debug(f"config: {config}")
    task = config["current-task"]
    if "path" in task:
        path = render_content(task, task["path"], config, logger)
    else:
        path = task["path-modify-event"]

    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.warning(f"Directory {directory} did not exist, created it.")

    logger.info(f"Writing to file at {path}")

    content = render_content(task, task["content"], config, logger)
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)
