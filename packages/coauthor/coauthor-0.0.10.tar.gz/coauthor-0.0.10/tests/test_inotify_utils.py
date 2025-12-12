import os
import pytest
from unittest import mock
from coauthor.utils.inotify_utils import get_recently_modified_file
from logging import Logger


def test_get_recently_modified_file_with_inotify_file():
    # Setup
    logger = mock.Mock(Logger)
    dir_path = "/mocked/path"
    inotify_file = "/mocked/path/file.txt"

    mocked_files = {"file.txt": 1, "another_file.txt": 0}  # File has been modified recently

    def mock_isfile(path):
        return path.split("/")[-1] in mocked_files

    def mock_listdir(path):
        return list(mocked_files.keys())

    def mock_getmtime(path):
        filename = path.split("/")[-1]
        return mocked_files[filename]

    with mock.patch("os.listdir", mock_listdir), mock.patch("os.path.isfile", mock_isfile), mock.patch(
        "os.path.getmtime", mock_getmtime
    ):
        # Execute
        result = get_recently_modified_file(inotify_file, dir_path, logger)

    # Verify
    assert result == inotify_file
    logger.debug.assert_called()


def test_get_recently_modified_file_without_inotify_file():
    # Setup
    logger = mock.Mock(Logger)
    dir_path = "/mocked/path"
    inotify_file = "/mocked/path/nonexistent.txt"

    mocked_files = {"file.txt": 1, "another_file.txt": 2}  # This one is the most recently modified

    def mock_isfile(path):
        return path.split("/")[-1] in mocked_files

    def mock_listdir(path):
        return list(mocked_files.keys())

    def mock_getmtime(path):
        filename = path.split("/")[-1]
        return mocked_files[filename]

    with mock.patch("os.listdir", mock_listdir), mock.patch("os.path.isfile", mock_isfile), mock.patch(
        "os.path.getmtime", mock_getmtime
    ):
        # Execute
        result = get_recently_modified_file(inotify_file, dir_path, logger)

    # Verify
    assert result == "/mocked/path/another_file.txt"
    logger.debug.assert_called()


def test_get_recently_modified_file_empty_directory():
    # Setup
    logger = mock.Mock(Logger)
    dir_path = "/mocked/path"
    inotify_file = "/mocked/path/nonexistent.txt"

    def mock_isfile(path):
        return False

    def mock_listdir(path):
        return []

    with mock.patch("os.listdir", mock_listdir), mock.patch("os.path.isfile", mock_isfile):
        # Execute
        result = get_recently_modified_file(inotify_file, dir_path, logger)

    # Verify
    assert result is None
    logger.debug.assert_called()
