import logging
import os
import argparse

import yaml
import time
import tempfile
from coauthor.utils.config import get_config, get_config_path, read_config, get_jinja_config
from coauthor.utils.logger import Logger


def test_get_config_path_returns_correct_coauthor_file():
    """
    Test that the `get_config_path` function correctly returns the file path
    of the '.coauthor.yml' file located in the current project root directory.
    """
    file_path = get_config_path()
    file_path_expected = os.path.join(os.getcwd(), ".coauthor.yml")
    assert file_path[0] == file_path_expected


def test_get_config_path_returns_none():
    config_path = get_config_path("whatever.yml")
    assert config_path[0] is None


def test_get_config_path_returns_file_in_home_directory():
    home_directory = os.path.expanduser("~")
    file_name = "whatever.yml"
    file_path = os.path.join(home_directory, file_name)
    with open(file_path, "w") as file:
        file.write("This is a test file created using Python.")
    config_path = get_config_path("whatever.yml", "/tmp")
    os.remove(file_path)
    assert config_path[0] == file_path


def test_get_config():
    config = get_config()  # this return the config of this project
    assert config["workflows"][0]["name"] == "coauthor"
    assert config["workflows"][0]["tasks"][0]["id"] == "python"


def test_get_config_with_logger():
    logger = Logger(__name__, level=logging.DEBUG, log_file="debug.log")
    config = get_config(None, logger)  # this return the config of this project
    assert config["workflows"][0]["name"] == "coauthor"
    assert config["workflows"][0]["tasks"][0]["id"] == "python"


def test_get_config_whatever_profile():
    path = os.path.join(os.path.dirname(__file__), "data", "coauthor.yml")
    config = get_config(path)
    assert config["profile"] == "whatever"


def test_get_config_not_found_with_logger():
    logger = Logger(__name__, level=logging.INFO, log_file="coauthor.log")
    tmp_config_file = ".coauthor_test_get_config_not_found_with_logger.yml"
    if os.path.exists(tmp_config_file):
        os.remove(tmp_config_file)
    config = get_config(logger=logger, config_filename=tmp_config_file, search_dir="/tmp")
    assert config is not None
    os.remove(tmp_config_file)


def test_config_agent_model():
    path = os.path.join(os.path.dirname(__file__), "data", "coauthor-markdown2.yml")
    config = get_config(path)
    assert config["agent"]["model"] == "llama2:latest"


def test_config_watch_directory():
    path = os.path.join(os.path.dirname(__file__), "data", "coauthor-markdown2.yml")
    config = get_config(path)
    assert config["watch_directory"] == "/whatever"


def test_config_callback():
    path = os.path.join(os.path.dirname(__file__), "data", "coauthor-markdown2.yml")
    config = get_config(path)
    assert config["callback"] == "whatever_callback"


def test_config_api_url_var():
    path = os.path.join(os.path.dirname(__file__), "data", "coauthor-markdown2.yml")
    config = get_config(path)
    assert config["agent"]["api_url_var"] == "WHATEVER_URL"


def test_config_api_key_var():
    path = os.path.join(os.path.dirname(__file__), "data", "coauthor-markdown2.yml")
    config = get_config(path)
    assert config["agent"]["api_key_var"] == "WHATEVER_KEY"


def test_config_defaults():
    cwd = os.getcwd()
    tmp_config_file = ".coauthor_test_config_defaults.yml"
    config_path = os.path.join(cwd, tmp_config_file)
    if os.path.exists(tmp_config_file):
        os.remove(tmp_config_file)
    with open(config_path, "w") as file:
        yaml.safe_dump({}, file)
    config = get_config(config_filename=tmp_config_file)

    assert config["agent"]["api_url_var"] == "OPENAI_API_URL"
    assert config["agent"]["api_key_var"] == "OPENAI_API_KEY"
    # assert config["agent"]["model"] == "openai/gpt-4o"
    assert config["agent"]["model"] == "gpt-4o-mini"
    assert config["jinja"]["search_path"] == ".coauthor/templates"
    assert config["file-watcher"]["ignore-folders"] == ["__pycache__", ".obsidian", ".git"]
    os.remove(tmp_config_file)


def test_get_config_creates_default_file_if_not_exists():

    def create_parser():
        parser = argparse.ArgumentParser(description="Process arguments to select steps")
        parser.add_argument(
            "--config_path",
            type=str,
            help="Path to the configuration file",
        )
        return parser

    cwd = os.getcwd()
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{cwd}/debug.log")
    tmp_config_file = ".coauthor_test_get_config_creates_default_file_if_not_exists.yml"
    if os.path.exists(tmp_config_file):
        os.remove(tmp_config_file)
    config_path = os.path.join(cwd, tmp_config_file)
    # config = get_config(logger=logger, config_filename=tmp_config_file)
    config = get_config(config_filename=tmp_config_file)
    assert os.path.exists(config_path)

    assert config["agent"]["api_key_var"] == "OPENAI_API_KEY"
    assert config["agent"]["api_url_var"] == "OPENAI_API_URL"
    # assert config["agent"]["model"] == "openai/gpt-4o"
    assert config["agent"]["model"] == "gpt-4o-mini"

    parser = create_parser()
    args = parser.parse_args(["--config_path", config_path])
    config = get_config(args=args)
    assert os.path.exists(config_path)
    os.remove(tmp_config_file)


def test_get_jinja_config_defaults():
    config = {}
    config_jinja = get_jinja_config(config)
    assert config_jinja == {"search_path": ".coauthor/templates"}
