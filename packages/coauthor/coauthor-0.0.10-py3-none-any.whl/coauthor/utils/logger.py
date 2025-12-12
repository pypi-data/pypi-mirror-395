import logging
import os
import inspect


class Logger:
    def __init__(self, name, level=logging.INFO, log_file=None):
        if not log_file:
            log_file = os.path.join(os.getcwd(), "coauthor.log")
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        self.log_file = log_file
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def clean_log_file(self):
        if self.log_file and os.path.exists(self.log_file):
            os.remove(self.log_file)
            print(f"Log file '{self.log_file}' has been removed.")

    def debug(self, msg):
        frame = inspect.currentframe().f_back
        caller_module = frame.f_globals["__name__"]
        caller_function = frame.f_code.co_name
        self.logger.debug(f"[{caller_module}.{caller_function}] {msg}")

    def info(self, msg):
        frame = inspect.currentframe().f_back
        caller_module = frame.f_globals["__name__"]
        caller_function = frame.f_code.co_name
        self.logger.info(f"[{caller_module}.{caller_function}] {msg}")

    def warning(self, msg):
        frame = inspect.currentframe().f_back
        caller_module = frame.f_globals["__name__"]
        caller_function = frame.f_code.co_name
        self.logger.warning(f"[{caller_module}.{caller_function}] {msg}")

    def error(self, msg):
        frame = inspect.currentframe().f_back
        caller_module = frame.f_globals["__name__"]
        caller_function = frame.f_code.co_name
        self.logger.error(f"[{caller_module}.{caller_function}] {msg}")
