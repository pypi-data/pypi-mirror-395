import os
import time
import tempfile
import logging
import threading
from unittest.mock import patch, Mock, MagicMock, call

from coauthor.utils.logger import Logger
import pytest
from coauthor.modules.file_watcher import (
    watch_directory,
    add_watch_recursive,
    handle_inotify_event,
    handle_workflow_file_modify_event,
)
from inotify_simple import flags
import yaml


def get_config(config_file="coauthor_task_pong.yml"):
    config_path = os.path.join(os.path.dirname(__file__), "data", config_file)
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
        config["current-workflow"] = config["workflows"][0]
        config["current-task"] = config["current-workflow"]["tasks"][0]
    return config


class TestWatchDirectory:
    @pytest.fixture
    def setup_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    def test_watch_directory(self, setup_directory):

        def test(file_path, temp_dir):
            time.sleep(3)
            with open(file_path, "w") as f:
                f.write("@ai-test: ping")
            pytest.helpers.wait_file_content(file_path, "pong", retries=10, delay=1)
            with open(os.path.join(temp_dir, "stop"), "w") as f:
                f.write("stop")

        temp_dir = setup_directory
        logger = Logger("test_watch_directory", level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
        config = get_config()
        config["current-workflow"] = config["workflows"][0]
        config["current-workflow"]["watch"] = {"filesystem": {"paths": [temp_dir]}}
        config["current-task"] = config["current-workflow"]["tasks"][0]
        file_path = os.path.join(temp_dir, "test_file.md")
        config["current-task"]["path-modify-event"] = file_path
        with open(file_path, "w") as f:
            f.write("whatever")
        x = threading.Thread(target=test, args=(file_path, temp_dir), daemon=True)
        x.start()

        watch_directory(config, logger)
        with open(file_path) as f:
            file_contents = f.read()
        assert file_contents == "pong"

    def test_watch_and_multiple_files_in_subdir(self, setup_directory):
        temp_dir = setup_directory
        logger = Logger("test_watch_directory", level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
        config = get_config()
        config["current-workflow"] = config["workflows"][0]
        config["current-workflow"]["watch"] = {"filesystem": {"paths": [temp_dir]}}
        config["current-task"] = config["current-workflow"]["tasks"][0]
        file_path_1 = os.path.join(temp_dir, "test_file.md")
        with open(file_path_1, "w") as f:
            f.write("whatever")
        new_dir = os.path.join(temp_dir, "new_directory")
        os.makedirs(new_dir)
        file_path_2 = os.path.join(new_dir, "test_file.md")
        with open(file_path_2, "w") as f:
            f.write("whatever")

        x = threading.Thread(target=watch_directory, args=(config, logger), daemon=True)
        x.start()
        assert x.is_alive(), "The thread for watching the directory did not start successfully"
        time.sleep(3)

        with open(file_path_1, "w") as f:
            f.write("@ai-test: ping")
        file_contents = pytest.helpers.wait_file_content(file_path_1, "pong", retries=10, delay=1)
        assert file_contents == "pong"

        with open(file_path_2, "w") as f:
            f.write("@ai-test: ping")
        file_contents = pytest.helpers.wait_file_content(file_path_2, "pong", retries=10, delay=1)
        assert file_contents == "pong"

        with open(os.path.join(temp_dir, "stop"), "w") as f:
            f.write("stop")

        x.join()

    def test_watch_and_multiple_regex_callbacks(self, setup_directory):

        def test(test_item, temp_dir, logger):
            time.sleep(4)

            with open(test_item["path"], "w") as f:
                logger.debug(f"Write {test_item['content']} to {test_item['path']}")
                f.write(test_item["content"])
            logger.debug(f"Wait for {test_item['content_after']}")
            file_contents = pytest.helpers.wait_file_content(
                test_item["path"], test_item["content_after"], retries=10, delay=1
            )
            logger.debug(f"Write stop file")
            with open(os.path.join(temp_dir, "stop"), "w") as f:
                f.write("stop")

        temp_dir = setup_directory
        logger = Logger("test_watch_directory", level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
        config = get_config("coauthor-regex-replace.yml")
        config["current-workflow"] = config["workflows"][0]
        config["current-workflow"]["watch"] = {"filesystem": {"paths": [temp_dir]}}
        config["current-task"] = config["current-workflow"]["tasks"][0]

        new_dir = os.path.join(temp_dir, "new_directory")
        new_dir_2 = os.path.join(new_dir, "new_directory")
        new_file_path = os.path.join(new_dir, "new_test_file.txt")
        new_file_path2 = os.path.join(new_dir_2, "new_test_file.txt")

        os.makedirs(new_dir)
        os.makedirs(new_dir_2)

        tests = []
        tests.append({"path": new_file_path, "content": "a -> b", "content_after": "a → b"})
        tests.append({"path": new_file_path2, "content": "a <- b", "content_after": "a ← b"})

        for test_item in tests:
            x = threading.Thread(target=test, args=(test_item, temp_dir, logger), daemon=True)
            x.start()
            assert x.is_alive(), "The thread for watching the directory did not start successfully"
            watch_directory(config, logger)
            with open(test_item["path"], "r") as file:
                file_contents = file.read()
            assert file_contents == test_item["content_after"]


class TestWatchUtils:
    @pytest.fixture
    def mock_inotify(self):
        with patch("coauthor.modules.file_watcher.INotify") as MockINotify:
            yield MockINotify()

    @pytest.fixture
    def setup_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    def test_add_watch_recursive(self, setup_directory, mock_inotify):
        temp_dir = setup_directory
        config = get_config()
        wd_to_path = add_watch_recursive(config, mock_inotify, temp_dir)

        mock_inotify.add_watch.assert_any_call(temp_dir, flags.CREATE | flags.MODIFY)

        for root, dirs, _ in os.walk(temp_dir):
            for subdir in dirs:
                subdir_path = os.path.join(root, subdir)
                mock_inotify.add_watch.assert_any_call(subdir_path, flags.CREATE | flags.MODIFY)

        expected_wd_to_path = {mock_inotify.add_watch.return_value: path for path in wd_to_path.values()}
        assert wd_to_path == expected_wd_to_path

    def test_watch_directory_keyboard_interrupt(self, setup_directory):
        temp_dir = setup_directory
        logger = Logger("test_watch_directory", level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
        config = get_config()
        config["current-workflow"]["watch"] = {"filesystem": {"paths": [temp_dir]}}

        class MockLogger:
            def info(self, message):
                print(message)

        def mock_info(message):
            nonlocal info_logged
            if message == expected_message:
                info_logged = True

        mock_logger = MockLogger()
        info_logged = False
        expected_message = "Stopping directory watch"
        mock_logger.info = mock_info

        with patch("coauthor.modules.file_watcher.INotify") as MockINotify:
            mock_inotify = MockINotify.return_value

            def simulate_keyboard_interrupt(*args, **kwargs):
                raise KeyboardInterrupt

            mock_inotify.read.side_effect = simulate_keyboard_interrupt

            watch_directories = [temp_dir]
            for directory in watch_directories:
                mock_inotify.add_watch(directory, flags.CREATE | flags.MODIFY)

            watch_directory(config, mock_logger)
            assert info_logged


class TestHandleInotifyEvent:
    @pytest.fixture
    def setup_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    @pytest.fixture
    def mock_inotify_and_logger(self):
        with patch("coauthor.modules.file_watcher.INotify") as MockINotify:
            mock_logger = MagicMock()
            yield MockINotify(), mock_logger

    def test_handle_create_event_for_directory(self, setup_directory, mock_inotify_and_logger):
        logger = Logger("test_watch_directory", level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
        temp_dir = setup_directory
        mock_inotify, _ = mock_inotify_and_logger
        wd_to_path = {}
        config = get_config()

        new_dir = os.path.join(temp_dir, "new_directory")
        os.makedirs(new_dir)

        event = Mock()
        event.wd = 1
        event.name = "new_directory"
        event.mask = flags.CREATE

        def from_mask(mask):
            return [flags.CREATE]

        with patch("os.path.isdir", return_value=True), patch("inotify_simple.flags.from_mask", from_mask):
            handle_inotify_event(event, wd_to_path, mock_inotify, config, logger)

        assert mock_inotify.add_watch.called_once_with(new_dir, flags.CREATE | flags.MODIFY | flags.CLOSE_WRITE)

    def test_handle_event_when_file_path_mismatch(self, setup_directory, mock_inotify_and_logger):
        temp_dir = setup_directory
        mock_inotify, logger = mock_inotify_and_logger
        wd_to_path = {}
        config = get_config()

        event = Mock()
        event.wd = 1
        event.name = "file.txt"
        event.mask = flags.MODIFY

        def from_mask(mask):
            return [flags.MODIFY]

        file_path_inotify = os.path.join(temp_dir, "file.txt")
        file_path = os.path.join(temp_dir, "actual_file.txt")

        with patch("os.path.join", return_value=file_path_inotify), patch("inotify_simple.flags.from_mask", from_mask):
            with patch("coauthor.modules.file_watcher.get_recently_modified_file", return_value=file_path):
                handle_inotify_event(event, wd_to_path, mock_inotify, config, logger)

        logger.warning.assert_called_with(
            f"file_path_inotify: {file_path_inotify} is not equal to file_path: {file_path}"
        )

    def test_modify_event_with_ignore_extensions(self, setup_directory, mock_inotify_and_logger):
        temp_dir = setup_directory
        logger = Logger("test_watch_directory", level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
        mock_inotify, _ = mock_inotify_and_logger
        wd_to_path = {}
        config = get_config()
        config["watch-ignore-file-extensions"] = [".txt"]

        event = Mock()
        event.wd = 1
        event.name = "file.txt"
        event.mask = flags.MODIFY

        def from_mask(mask):
            return [flags.MODIFY]

        file_path_inotify = os.path.join(temp_dir, "file.txt")
        with open(file_path_inotify, "w") as file:
            file.write("whatever")

        logger = MagicMock()

        with patch("os.path.join", return_value=file_path_inotify), patch("inotify_simple.flags.from_mask", from_mask):
            with patch("os.path.splitext", return_value=("file", ".txt")):
                result = handle_inotify_event(event, wd_to_path, mock_inotify, config, logger)

        assert result is False
        logger.debug.assert_called_with(f"Ignore MODIFY event {file_path_inotify} because of file extension .txt")

    def test_handle_inotify_event_with_binary_file(self, setup_directory, mock_inotify_and_logger):
        temp_dir = setup_directory
        logger = Logger("test_watch_directory", level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
        mock_inotify, _ = mock_inotify_and_logger
        wd_to_path = {}
        config = get_config()

        event = Mock()
        event.wd = 1
        event.name = "file.bin"
        event.mask = flags.MODIFY

        def from_mask(mask):
            return [flags.MODIFY]

        file_path_inotify = os.path.join(temp_dir, "file.bin")
        # Simulating a binary file by writing binary data
        with open(file_path_inotify, "wb") as file:
            file.write(b"\x00\x01\x02\x03\x04\x05")

        with patch("os.path.join", return_value=file_path_inotify), patch("inotify_simple.flags.from_mask", from_mask):
            with patch("os.path.splitext", return_value=("file", ".bin")):
                result = handle_inotify_event(event, wd_to_path, mock_inotify, config, logger)

        assert result is False


class TestHandleWorkflowFileModifyEvent:
    @pytest.fixture
    def setup_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    @pytest.fixture
    def mock_logger(self):
        return MagicMock()

    def test_unsupported_task_type(self, setup_directory, mock_logger):
        temp_dir = setup_directory
        config = get_config()
        config["current-workflow"]["watch"] = {"filesystem": {"paths": [temp_dir]}}
        file_path = os.path.join(temp_dir, "file.md")
        config["current-task"]["type"] = "unsupported_type"
        with open(file_path, "w") as file:
            file.write("@ai-test: whatever")

        with pytest.raises(ValueError) as e:
            handle_workflow_file_modify_event(file_path, config, mock_logger)

        assert str(e.value) == f"Unsupported task_type: unsupported_type"

    def test_ignore_rapid_modify_event(self, setup_directory, mock_logger):
        config = get_config()
        temp_dir = setup_directory
        config["current-workflow"]["watch"] = {"filesystem": {"paths": [temp_dir]}}
        file_path = os.path.join(temp_dir, "file.md")
        task_function = Mock()
        with open(file_path, "w") as file:
            file.write("@ai-test: whatever")

        with patch.dict("coauthor.modules.file_watcher.task_type_functions", {"supported_type": task_function}):
            config["current-task"]["type"] = "supported_type"
            handle_workflow_file_modify_event(file_path, config, mock_logger)

        task_function.assert_called_once_with(config, mock_logger)

        # first request not ignored
        mock_logger.info.assert_has_calls(
            [
                call(
                    f"Workflow: {config['current-workflow']['name']}, Task: {config['current-task']['id']} → {file_path}"
                )
            ]
        )

        with patch.dict("coauthor.modules.file_watcher.task_type_functions", {"supported_type": task_function}):
            config["current-task"]["type"] = "supported_type"
            handle_workflow_file_modify_event(file_path, config, mock_logger)

        # second request ignored
        mock_logger.info.assert_has_calls([call(f"  Ignoring rapid MODIFY event for (modify_event_limit: 3).")])

        with patch.dict("coauthor.modules.file_watcher.task_type_functions", {"supported_type": task_function}):
            config["current-task"]["type"] = "supported_type"
            config["current-task"]["modify_event_limit"] = 3
            handle_workflow_file_modify_event(file_path, config, mock_logger)

        # second request ignored
        mock_logger.info.assert_has_calls([call(f"  Ignoring rapid MODIFY event for (modify_event_limit: 3).")])
