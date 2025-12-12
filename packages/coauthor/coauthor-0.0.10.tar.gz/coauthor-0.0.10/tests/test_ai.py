import os
import tempfile
import logging
import pytest
from coauthor.utils.logger import Logger
from unittest.mock import patch, mock_open, MagicMock
from coauthor.utils.config import get_config
from coauthor.modules.ai import process_with_openai_agent, prompt_template_path, write_response_to_yaml
import yaml
import jinja2

from coauthor.utils.jinja import prompt_template_paths


def get_pong_config():
    config_path = os.path.join(os.path.dirname(__file__), "data", "coauthor_task_pong.yml")
    with open(config_path, "r") as file:
        task = yaml.safe_load(file)
    return task


def test_process_with_openai_agent_template_location():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    config = get_pong_config()
    config["current-workflow"] = config["workflows"][0]
    config["current-task"] = config["current-workflow"]["tasks"][0]
    task = config["current-task"]
    config["agent"]["api_url"] = "https://example.com/api/v1"
    config["agent"]["api_key"] = "whatever"
    paths = prompt_template_paths(config, "system.md")
    system_message = task["system"]
    del task["system"]

    with tempfile.TemporaryDirectory() as temp_config_dir:
        config["jinja"] = {"search_path": temp_config_dir}
        for path in paths:
            path_system_template = os.path.join(temp_config_dir, path)
            os.makedirs(os.path.dirname(path_system_template), exist_ok=True)
            with open(path_system_template, "w", encoding="utf-8") as file1:
                file1.write(system_message)
            with patch("coauthor.modules.ai.create_chat_completion", return_value="pong"):
                response = process_with_openai_agent(config, logger)
            assert response == "pong"
            assert task["system_template_path"] == path
            if os.path.exists(path_system_template):
                os.remove(path_system_template)


def test_process_with_openai_agent_user_message_template():
    """
    Test the `process_with_openai_agent` function using a user message from a Jinja template file.

    This test demonstrates the flexibility of using Jinja templating to create user messages,
    with access to configuration variables that provide access to tasks within workflows.

    It simulates the OpenAI agent being set up to always respond with "pong".
    """
    config = get_pong_config()
    config["current-workflow"] = config["workflows"][0]
    config["current-task"] = config["current-workflow"]["tasks"][0]
    task = config["current-task"]

    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")

    with tempfile.TemporaryDirectory() as temp_config_dir:

        # Create user template
        config["jinja"] = {"search_path": temp_config_dir}
        path_template = prompt_template_path(config, "user.md", logger)
        path_user_message = os.path.join(temp_config_dir, path_template)
        user_message = "User template for {{ config['current-task']['id'] }}"
        os.makedirs(os.path.dirname(path_user_message), exist_ok=True)
        with open(path_user_message, "w", encoding="utf-8") as file1:
            logger.info(f"User message path: {path_user_message}")
            logger.info(f"User message: {user_message}")
            file1.write(user_message)

        # Create a file and process with AI
        with tempfile.TemporaryDirectory() as temp_watch_dir:
            task["path-modify-event"] = os.path.join(temp_watch_dir, "whatever.md")
            with open(task["path-modify-event"], "w", encoding="utf-8") as file1:
                file1.write("File content")

            with patch("coauthor.modules.ai.create_chat_completion", return_value="pong"):
                response = process_with_openai_agent(config, logger)
            assert response == "pong"


def test_process_with_openai_agent_user_message_template_missing():
    """
    Test the `process_with_openai_agent` function when the user message template is missing.

    It simulates the OpenAI agent being set up to always respond with "pong".
    """
    config = get_pong_config()
    config["current-workflow"] = config["workflows"][0]
    config["current-task"] = config["current-workflow"]["tasks"][0]

    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a user template
        config["jinja"] = {"search_path": temp_dir}
        path_user_template = os.path.join(temp_dir, prompt_template_path(config, "user.md", logger))
        user_message = "User template for {{ config['current-task']['id'] }}"
        os.makedirs(os.path.dirname(path_user_template), exist_ok=True)
        with open(path_user_template, "w", encoding="utf-8") as file1:
            logger.info(f"User message path: {path_user_template}")
            logger.info(f"User message: {user_message}")
            file1.write(user_message)
        with patch("coauthor.modules.ai.create_chat_completion", return_value="pong"):
            response = process_with_openai_agent(config, logger)
        assert response == "pong"
        with patch("coauthor.modules.ai.create_chat_completion_submit", return_value="```python\npong\n```"):
            response = process_with_openai_agent(config, logger)
        assert response == "pong"


def test_process_with_openai_agent_config_missing_system_template():
    """
    Test `process_with_openai_agent` function with configuration missing
    system template "ping-workflow/ping-task/system.md".

    Should throw a jinja2.exceptions.TemplateNotFound error.
    """
    config = get_pong_config()
    config["current-workflow"] = config["workflows"][0]
    config["current-task"] = config["current-workflow"]["tasks"][0]
    task = config["current-task"]
    del task["system"]
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    with tempfile.TemporaryDirectory() as temp_dir:
        config["jinja"] = {"search_path": temp_dir}
        with pytest.raises(ValueError) as excinfo:
            process_with_openai_agent(config, logger)

        assert (
            'An AI task should have a key "system" or a template with path "ping-workflow/ping-task/system.md"'
            in str(excinfo.value)
        )


def test_write_response_to_yaml_env_var_not_set():
    """
    Test the `write_response_to_yaml` function when the environment variable
    COAUTHOR_AI_LOG_DIR is not set.

    It should log a debug message indicating the environment variable is not set.
    """
    config = get_pong_config()
    config["current-workflow"] = config["workflows"][0]
    config["current-task"] = config["current-workflow"]["tasks"][0]
    logger = MagicMock()
    with patch.dict(os.environ, {}, clear=True):
        write_response_to_yaml(config, [], "", "", logger)
    logger.debug.assert_called_with("Environment variable COAUTHOR_AI_LOG_DIR not set")
