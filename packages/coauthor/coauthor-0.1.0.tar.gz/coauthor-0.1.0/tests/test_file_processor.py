import os
import yaml
import logging
from unittest.mock import patch, mock_open, MagicMock
from coauthor.modules.file_processor import regex_replace_in_file, pong, include_file
from coauthor.utils.logger import Logger
from unittest import mock
import tempfile


def get_config(config_file="coauthor-regex-replace.yml"):
    config_path = os.path.join(os.path.dirname(__file__), "data", config_file)
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config


def test_regex_replace_in_file_changes_content():
    config = get_config()
    config["current-workflow"] = config["workflows"][0]
    task = config["current-workflow"]["tasks"][0]
    config["current-task"] = task
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    task["path-modify-event"] = "test.txt"
    test_content = "This is a test string with -> to be replaced."
    updated_content = "This is a test string with → to be replaced."
    with patch("builtins.open", mock_open(read_data=test_content)) as mock_file:
        assert open(task["path-modify-event"]).read() == test_content
        result = regex_replace_in_file(config, logger)
        assert result == True
        assert task["content"] == updated_content
        mock_file().write.assert_called()


def test_regex_replace_in_file_no_change():
    config = get_config()
    config["current-workflow"] = config["workflows"][0]
    task = config["current-workflow"]["tasks"][0]
    config["current-task"] = task
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    task["path-modify-event"] = "test.txt"
    test_content = "This is a test string with → already replaced."
    with patch("builtins.open", mock_open(read_data=test_content)) as mock_file:
        assert open(task["path-modify-event"]).read() == test_content
        result = regex_replace_in_file(config, logger)
        assert result == False
        assert "content" not in task
        mock_file().write.assert_not_called()


def test_regex_replace_in_file_no_path_match():
    logger = MagicMock()
    config = get_config()
    config["current-workflow"] = config["workflows"][0]
    task = config["current-workflow"]["tasks"][0]
    config["current-task"] = task
    task["path-modify-event"] = "test.md"
    test_content = "Whatever"
    with patch("builtins.open", mock_open(read_data=test_content)) as mock_file:
        assert open(task["path-modify-event"]).read() == test_content
        result = regex_replace_in_file(config, logger)
        assert result == False
        logger.debug.assert_called_with("regex_replace_in_file: no path match for test.md")


def test_regex_replace_in_file_with_capturing_groups():
    config = get_config()
    config["current-workflow"] = config["workflows"][0]
    task = config["current-workflow"]["tasks"][0]
    config["current-task"] = task
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    task["path-modify-event"] = "test.txt"
    test_content = "User: John_Doe, User: Jane_Doe"
    updated_content = "User: John Doe, User: Jane Doe"
    with patch("builtins.open", mock_open(read_data=test_content)) as mock_file:
        assert open(task["path-modify-event"]).read() == test_content
        result = regex_replace_in_file(config, logger)
        assert result == True
        assert task["content"] == updated_content
        mock_file().write.assert_called_once_with(updated_content)


def test_regex_replace_in_file_with_capturing_groups2():
    config = get_config()
    config["current-workflow"] = config["workflows"][0]
    task = config["current-workflow"]["tasks"][0]
    config["current-task"] = task
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    task["path-modify-event"] = "test.txt"
    test_content = "User: John_Doe, User: Jane_Doe"
    updated_content = "User: John Doe, User: Jane Doe"
    regex_replacements = [{"regex": r"User: (\w+)_(\w+)", "replace": r"User: \1 \2"}]
    with patch("builtins.open", mock_open(read_data=test_content)) as mock_file:
        assert open(task["path-modify-event"]).read() == test_content
        result = regex_replace_in_file(config, logger)
        assert result == True
        assert task["content"] == updated_content
        mock_file().write.assert_called_once_with(updated_content)


def test_pong():
    config = get_config()
    config["current-workflow"] = config["workflows"][0]
    task = config["current-workflow"]["tasks"][0]
    config["current-task"] = task
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    task["path-modify-event"] = "test.txt"
    test_content = "pong"
    mocked_open = mock_open(read_data=test_content)
    with mock.patch("builtins.open", mocked_open):
        pong(config, logger)
    mocked_open().write.not_called
    # mock_logger.info.assert_any_call("Running the pong file processor" + "mock_path")


def test_ping():
    config = get_config()
    config["current-workflow"] = config["workflows"][0]
    task = config["current-workflow"]["tasks"][0]
    config["current-task"] = task
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    test_content = "ping"
    mocked_open = mock_open(read_data=test_content)
    with mock.patch("builtins.open", mocked_open):
        task["path-modify-event"] = "mock_path"
        pong(config, logger)
    mocked_open().write.assert_called_once_with("pong")


def test_regex_replace_in_file_with_internal_regex():
    config = get_config()
    config["current-workflow"] = config["workflows"][0]
    task = config["current-workflow"]["tasks"][0]
    config["current-task"] = task
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    task["path-modify-event"] = "test.txt"
    test_content = "{{< line1\nline2>}}"
    updated_content = "{{< line1 line2>}}"
    with patch("builtins.open", mock_open(read_data=test_content)) as mock_file:
        assert open(task["path-modify-event"]).read() == test_content
        result = regex_replace_in_file(config, logger)
        assert result == True
        assert task["content"] == updated_content
        mock_file().write.assert_called_once_with(updated_content)


def test_file_open_mock():
    with patch("builtins.open", mock_open(read_data="data")) as mock_file:
        assert open("path/to/open").read() == "data"


def test_include_file():
    config = get_config("coauthor-include-file.yml")
    config["current-workflow"] = config["workflows"][0]
    task = config["current-workflow"]["tasks"][0]
    config["current-task"] = task
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    task["path-modify-event"] = "main.txt"
    task["regex"] = "<!--\s*start-code-sample\s+([^ \t\n]+)\s*-->\s*(.*?)<!--\s*end-code-sample\s*-->"
    main_content = config["test"]["main-content"]
    include_content = config["test"]["include-content"]
    expected_main_content = config["test"]["expected-main-content"]

    with tempfile.TemporaryDirectory() as temp_dir:
        task["dir"] = temp_dir
        main_file_path = os.path.join(temp_dir, "main.txt")
        include_file_path = os.path.join(temp_dir, "include.txt")

        # Write main content to the main file
        with open(main_file_path, "w", encoding="utf-8") as main_file:
            main_file.write(main_content)

        # Write include content to the include file
        with open(include_file_path, "w", encoding="utf-8") as inc_file:
            inc_file.write(include_content)

        task["path-modify-event"] = main_file_path

        result = include_file(config, logger)
        assert result == True

        # Verify the content of the main file has been updated
        with open(main_file_path, "r", encoding="utf-8") as main_file:
            main_file_content = main_file.read()
            logger.debug(f"main_file_content: {main_file_content}")
            logger.debug(f"expected_main_content: {expected_main_content}")
            assert main_file_content == expected_main_content

        # Running second time does not result in update
        result = include_file(config, logger)
        assert result == False

        # Test case where include file is not found
        main_content = main_content.replace("include.txt", "does-not-exist.txt")
        with open(main_file_path, "w", encoding="utf-8") as main_file:
            main_file.write(main_content)

        result = include_file(config, logger)
        assert result == False

        with open(main_file_path, "r", encoding="utf-8") as main_file:
            main_file_content = main_file.read()
            assert main_file_content != expected_main_content

        # Test absolute path
        del task["dir"]
        main_content = main_content.replace("does-not-exist.txt", "/tmp/does-not-exist.txt")
        with open(main_file_path, "w", encoding="utf-8") as main_file:
            main_file.write(main_content)
        result = include_file(config, logger)
        assert result == False

        # Test relative path
        task["dir"] = "whatever"
        main_content = main_content.replace("does-not-exist.txt", "/tmp/does-not-exist.txt")
        with open(main_file_path, "w", encoding="utf-8") as main_file:
            main_file.write(main_content)
        result = include_file(config, logger)
        assert result == False

        # logger.debug.assert_any_call("Content is up to date in main.txt")
