import os
import tempfile
import logging
import pytest
from coauthor.utils.logger import Logger
from unittest.mock import patch, mock_open, MagicMock
from coauthor.utils.config import get_config
from coauthor.modules.ai import process_file_with_openai_agent, process_with_openai_agent

import yaml
import jinja2
import openai
from tempfile import TemporaryDirectory


def get_pong_config():
    config_path = os.path.join(os.path.dirname(__file__), "data", "coauthor_task_pong.yml")
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
        config["current-workflow"] = config["workflows"][0]
        config["current-task"] = config["current-workflow"]["tasks"][0]
    return config


def test_process_file_with_openai_agent():
    """
    Test the `process_file_with_openai_agent` function by creating a temporary
    file with a specific pattern, processing it, and verifying that the content
    changes as expected. This test also verifies that task dict is updated by
    process_file_with_openai_agent with the path of the file.

    The function should transform the content from a placeholder string (ai-test: ping)
    to 'pong' using the OpenAI agent.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        config = get_pong_config()
        config["jinja"] = {"search_path": temp_dir}
        logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
        task = config["current-task"]
        logger.debug(f"task:{task}")
        file_path = os.path.join(temp_dir, "whatever.md")

        with open(file_path, "w") as f:
            f.write("(ai-test: ping)")

        process_file_with_openai_agent(config, logger)
        assert task["response"] == "pong"


def test_process_with_openai_agent():
    logger = Logger(__name__, level=logging.INFO)
    with tempfile.TemporaryDirectory() as temp_dir:
        config = get_pong_config()
        config["jinja"] = {"search_path": temp_dir}
        task = config["current-task"]
        task["user"] = "(ai-test: ping)"
        response = process_with_openai_agent(config, logger)
        assert response == "pong"


def test_process_with_openai_agent_write_response_to_yaml():
    logger = Logger(__name__, level=logging.INFO)
    with tempfile.TemporaryDirectory() as temp_dir:
        config = get_pong_config()
        config["jinja"] = {"search_path": temp_dir}
        task = config["current-task"]
        task["user"] = "(ai-test: ping)"

        coauthor_ai_log_dir = tempfile.mkdtemp()  # Create a temporary directory to act as COAUTHOR_AI_LOG_DIR
        os.environ["COAUTHOR_AI_LOG_DIR"] = coauthor_ai_log_dir  # Set environment variable

        response = process_with_openai_agent(config, logger)

        assert response == "pong"

        # Assert that the ai-log-file exists and is updated in the task
        assert "ai-log-file" in task
        assert os.path.exists(task["ai-log-file"])


def test_process_with_wrong_openai_agent_config_raises_exception():
    # Define the sample content and agent
    logger = Logger(__name__, level=logging.INFO)
    with tempfile.TemporaryDirectory() as temp_dir:
        config = get_pong_config()
        config["jinja"] = {"search_path": temp_dir}
        task = config["current-task"]
        task["user"] = "whatever"
        workflow = config["current-workflow"]
        del config["agent"]["api_key_var"]
        del config["agent"]["api_url_var"]
        config["agent"]["api_key_var"] = "NOKEYATALL"
        config["agent"]["api_url"] = "http://9554090.com"

        with pytest.raises(openai.APIConnectionError) as excinfo:
            process_with_openai_agent(config, logger)

        assert "Connection error" in str(excinfo.value)
