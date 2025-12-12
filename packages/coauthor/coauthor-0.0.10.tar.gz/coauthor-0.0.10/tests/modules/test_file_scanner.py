import os
import tempfile
import pytest
from unittest import mock
from coauthor.modules.file_processor import pong
from coauthor.modules.file_scanner import scan


# Mock logger for testing
class MockLogger:
    def info(self, message):
        print(message)

    def debug(self, message):
        print(message)


def test_scan_with_pong():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set up a temporary file in the directory
        temp_file_path = os.path.join(temp_dir, "test_file.txt")
        with open(temp_file_path, "w") as temp_file:
            temp_file.write("initial content")

        # Define a mock workflow for testing
        mock_workflows = {
            "workflows": [
                {
                    "name": "pong-workflow",
                    "scan": {"filesystem": {"paths": [temp_dir]}},
                    "tasks": [{"type": "pong", "id": "task1"}],
                }
            ]
        }

        # Create a mock logger
        mock_logger = MockLogger()

        # Call the scan function with the mock workflow and logger
        scan(mock_workflows, mock_logger)

        # Check if the file contents have been changed to 'pong'
        with open(temp_file_path, "r") as temp_file:
            assert temp_file.read() == "pong"


def test_scan_with_invalid_task_type():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set up a temporary file in the directory
        temp_file_path = os.path.join(temp_dir, "test_file.txt")
        with open(temp_file_path, "w") as temp_file:
            temp_file.write("initial content")

        # Define a mock workflow for testing
        mock_workflows = {
            "workflows": [
                {
                    "name": "invalid-task-workflow",
                    "scan": {"filesystem": {"paths": [temp_dir]}},
                    "tasks": [{"type": "nonexistent_task", "id": "task1"}],
                }
            ]
        }

        # Create a mock logger
        mock_logger = MockLogger()

        # Expect the scan function to raise a ValueError due to unknown task type
        with pytest.raises(ValueError, match=r"Unsupported task_type: nonexistent_task"):
            scan(mock_workflows, mock_logger)
