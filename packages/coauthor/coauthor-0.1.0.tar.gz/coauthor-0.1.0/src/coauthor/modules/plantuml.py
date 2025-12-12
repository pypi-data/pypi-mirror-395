"""
This module provides functions to download PlantUML jar files and process PUML files.
"""

import os
import subprocess
import requests


def download_plantuml_jar(config, logger):
    """
    Downloads the PlantUML jar file from a specified URL if it does not exist
    in the configured path. The URL and path can be set in the configuration
    with default values provided. Download timeout can also be configured.

    :param config: Configuration dictionary which includes optional 'plantuml'
                   configuration with 'url', 'path', and 'timeout'.
    :param logger: Logger object for logging information and debug messages.
    """
    default_url = "https://github.com/plantuml/plantuml/releases/download/v1.2024.0/plantuml-1.2024.0.jar"

    plantuml_config = config.get("plantuml", {})
    plantuml_jar_url = plantuml_config.get("url", default_url)
    plantuml_jar_path = plantuml_config.get("path", os.path.join("/tmp", os.path.basename(plantuml_jar_url)))

    if not os.path.exists(plantuml_jar_path):
        timeout = plantuml_config.get("timeout", 30)  # 30 second default timeout
        response = requests.get(plantuml_jar_url, timeout=timeout)
        with open(plantuml_jar_path, "wb") as jar_file:
            jar_file.write(response.content)
            logger.info(f"Downloaded PlantUML jar to {plantuml_jar_path}")
    logger.debug(f"PlantUML jar is {plantuml_jar_path}")


def process_puml_file(config, logger):
    """
    Processes a PUML file by exporting it to specified formats using the PlantUML jar.
    The PlantUML jar is downloaded if not present. Export formats are configured
    in the configuration file.

    :param config: Configuration dictionary which includes 'current-task' with
                   'path-modify-event' and optional 'plantuml' configurations
                   with 'path' and 'export'.
    :param logger: Logger object for logging information about the exports.
    """
    download_plantuml_jar(config, logger)
    task = config["current-task"]
    path = task["path-modify-event"]

    plantuml_jar_path = config.get("plantuml", {}).get("path", "/tmp/plantuml-1.2024.0.jar")

    plantuml_config = config.get("plantuml", {})
    plantuml_exports = plantuml_config.get("export", ["svg", "png"])

    for export in plantuml_exports:
        subprocess.run(["java", "-jar", plantuml_jar_path, f"-t{export}", path], check=True)

    logger.info(f"Exported {path} to {', '.join(plantuml_exports)}")
