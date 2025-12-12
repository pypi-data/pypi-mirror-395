import pytest
from unittest import mock
from unittest.mock import mock_open
import os

# import subprocess
# import requests
from coauthor.utils.logger import Logger
import logging
from coauthor.modules.plantuml import download_plantuml_jar, process_puml_file


@pytest.fixture
def mock_config():
    return {
        "plantuml": {"url": "https://example.com/plantuml.jar", "path": "/tmp/plantuml.jar"},
        "current-task": {"path-modify-event": "/tmp/sample.puml"},
    }


@pytest.fixture
def mock_logger():
    return mock.Mock()
    # return Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")


def test_download_plantuml_jar(mock_config, mock_logger):
    with mock.patch("requests.get") as mock_get, mock.patch("builtins.open", mock_open()) as mock_file, mock.patch(
        "os.path.exists", return_value=False
    ):

        mock_response = mock.Mock()
        mock_response.content = b"jar content"
        mock_get.return_value = mock_response

        download_plantuml_jar(mock_config, mock_logger)

        mock_get.assert_called_once_with("https://example.com/plantuml.jar", timeout=30)
        mock_file().write.assert_called_once_with(b"jar content")
        mock_logger.info.assert_called_once_with("Downloaded PlantUML jar to /tmp/plantuml.jar")


def test_download_plantuml_jar_file_exists(mock_config, mock_logger):
    with mock.patch("os.path.exists", return_value=True):
        download_plantuml_jar(mock_config, mock_logger)

        mock_logger.info.assert_not_called()


def test_process_puml_file(mock_config, mock_logger):
    with mock.patch("subprocess.run") as mock_subproc_run, mock.patch("os.path.exists", return_value=True):

        process_puml_file(mock_config, mock_logger)

        mock_subproc_run.assert_any_call(["java", "-jar", "/tmp/plantuml.jar", "-tsvg", "/tmp/sample.puml"], check=True)
        mock_subproc_run.assert_any_call(["java", "-jar", "/tmp/plantuml.jar", "-tpng", "/tmp/sample.puml"], check=True)
        mock_logger.info.assert_any_call("Exported /tmp/sample.puml to svg, png")
