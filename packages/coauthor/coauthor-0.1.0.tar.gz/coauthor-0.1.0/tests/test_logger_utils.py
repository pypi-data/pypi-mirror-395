from coauthor.utils.logger import Logger
import logging
import os


def test_logger_default_log_file():
    """
    Test that the Logger class creates a default log file named 'coauthor.log' in the current working directory.

    The test initializes the Logger with INFO level logging. It then cleans up any preexisting log file named
    'coauthor.log'. The test asserts that the logger's log file is correctly set to 'coauthor.log' located in the current
    working directory.
    """
    logger = Logger(__name__, level=logging.INFO)
    log_file = os.path.join(os.getcwd(), "coauthor.log")
    logger.clean_log_file()
    assert logger.log_file == log_file


def test_logger_default_log_file_removed():
    """
    Test the Logger class behavior when a default log file is missing.

    This test initializes the Logger with INFO level logging, removes any existing 'coauthor.log' file from the
    current working directory, and invokes the clean_log_file method on the logger. It asserts that the logger
    correctly identifies and sets the log file to 'coauthor.log' after cleaning.
    """
    logger = Logger(__name__, level=logging.INFO)
    log_file = os.path.join(os.getcwd(), "coauthor.log")
    os.remove(log_file)
    logger.clean_log_file()
    assert logger.log_file == log_file


def test_logger_log_file():
    """
    Test the Logger with a custom log file path.

    The test checks whether the logger correctly logs messages to a specified file path. It initializes the
    Logger with INFO level logging and a custom log file located at '/tmp/coauthor.log'. After logging a test
    message, it verifies the existence of the log file and asserts that the Logger's log file path is set as
    specified and that the file exists.
    """
    log_file = "/tmp/coauthor.log"
    logger = Logger(__name__, level=logging.INFO, log_file=log_file)
    logger.info("hi ho")
    file_exists = os.path.exists(log_file)
    os.remove(log_file)
    assert [logger.log_file, file_exists] == [log_file, True]


def test_logger_log_file_debug():
    """
    Test the Logger's capability to handle DEBUG level logs to a specified file path.

    This test initializes the Logger with DEBUG level logging and a custom log file at '/tmp/coauthor.log'. It sends
    debug and error level messages to the logger, checks for the existence of the log file, and then asserts
    that the logger's file path configuration and file creation are correct without removing it.
    """
    log_file = "/tmp/coauthor.log"
    logger = Logger(__name__, level=logging.DEBUG, log_file=log_file)
    logger.debug("hi ho")
    logger.error("hi ho")
    file_exists = os.path.exists(log_file)
    # os.remove(log_file)
    assert [logger.log_file, file_exists] == [log_file, True]
