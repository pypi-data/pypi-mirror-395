import os
import logging
from coauthor.utils.logger import Logger
from coauthor.modules.workflow import initialize_workflows
from coauthor.utils.config import get_config
import tempfile
import pytest
import threading
import time
import argparse


class MockLogger:
    def info(self, message):
        print(message)

    def debug(self, message):
        print(message)

    def warning(self, message):
        print(message)


def test_initialize_workflows_no_workflows():
    """
    Test the initialize_workflows function when there are no workflows in the config.
    A warning should be logged and no further action taken.
    """
    # Create a mock logger
    mock_logger = MockLogger()

    config = get_config()
    if "workflows" in config:
        del config["workflows"]

    initialize_workflows(config=config, logger=mock_logger)

    # Check that the warning message was logged
    warning_logged = False
    expected_message = "No workflows found in the configuration. The program will now exit as there is nothing to do."

    # Simulate the functionality of checking logger output
    def mock_warning(message):
        nonlocal warning_logged
        if message == expected_message:
            warning_logged = True

    mock_logger.warning = mock_warning

    # Call the function
    initialize_workflows(config=config, logger=mock_logger)

    # Assert the message was logged
    assert warning_logged


def test_initialize_workflows_no_scan_directories():
    """
    Test the initialize_workflows function when there are no scan directories configured.
    Expect debug information about lack of scan directories.
    """
    # Create a mock logger
    mock_logger = MockLogger()

    path = os.path.join(os.path.dirname(__file__), "data", "coauthor_translation2.yml")
    config = get_config(path=path)

    # Ensure the scan paths are empty
    if "workflows" in config:
        config["workflows"][0]["scan"] = {"filesystem": {"paths": []}}

    initialize_workflows(config=config, logger=mock_logger, trigger_scan=True)


def test_read_file_write_file():
    """
    Test the workflow that reads a file and then writes to it using specific content patterns.

    The workflow is configured to scan files with `.md` extension, looking for content that matches
    the pattern ".*ping.*". Upon finding such files, the "read_file" task reads the content,
    and the "write_file" task modifies the content to append "=pong".
    """
    path = os.path.join(os.path.dirname(__file__), "data", "coauthor_translation2.yml")
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a temporary directory with a subdirectory
        sub_dir = os.path.join(temp_dir, "subdir")
        os.makedirs(sub_dir, exist_ok=True)

        # Define the file path and write "ping" into it
        file_path = os.path.join(sub_dir, "testfile.md")
        with open(file_path, "w") as file:
            file.write("ping")

        # Define the configuration for the workflow
        config = get_config(path=path)
        workflow = config["workflows"][0]
        workflow["scan"] = {"filesystem": {"paths": [temp_dir]}}

        # Initialize a Logger instance for debugging
        logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")

        # Call the `initialize_workflows` to process the file
        initialize_workflows(config=config, logger=logger, trigger_scan=True)

        # Check if the content of the file was updated correctly
        with open(file_path, "r") as file:
            content = file.read()

        # Assert if the content contains "ping=pong"
        assert "ping=pong" in content


# test that we can watch and stop watching
def test_initialize_workflow_watch_and_stop():
    def create_parser():
        parser = argparse.ArgumentParser(description="Process arguments to select steps")
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
        return parser

    def write_stop_file(path_stop_file, logger):
        logger.info(f"sleep 1 seconds")
        time.sleep(1)

        logger.info(f"Write stop file")
        with open(path_stop_file, "w") as f:
            f.write("stop")

    # Create a mock logger
    mock_logger = MockLogger()

    # Check that the warning message was logged
    warning_logged = False
    info_logged = True
    expected_message_1 = "Stop file found!"
    expected_message = (
        "No directories to watch specified in workflows. The program will now exit as there is nothing to do."
    )

    def mock_warning(message):
        nonlocal warning_logged
        if message == expected_message:
            warning_logged = True

    def mock_info(message):
        nonlocal info_logged
        if message == expected_message_1:
            info_logged = True

    mock_logger.warning = mock_warning
    mock_logger.info = mock_info

    with tempfile.TemporaryDirectory() as temp_dir:
        logger = Logger("test_initialize_workflow_watch", level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
        path = os.path.join(os.path.dirname(__file__), "data", "coauthor_translation2.yml")
        config = get_config(path=path)
        config["current-workflow"] = config["workflows"][0]
        config["current-workflow"]["watch"] = {"filesystem": {"paths": [temp_dir]}}
        config["current-task"] = config["current-workflow"]["tasks"][0]
        parser = create_parser()
        args = parser.parse_args(["--watch"])
        config["args"] = args
        path_stop_file = os.path.join(temp_dir, "stop")

        x = threading.Thread(target=write_stop_file, args=(path_stop_file, logger), daemon=True)
        x.start()
        initialize_workflows(config, mock_logger)
        x.join()
        assert info_logged

        config["current-workflow"]["watch"] = {"filesystem": {"paths": []}}
        x = threading.Thread(target=write_stop_file, args=(path_stop_file, logger), daemon=True)
        x.start()
        initialize_workflows(config, mock_logger)
        x.join()

        assert warning_logged
