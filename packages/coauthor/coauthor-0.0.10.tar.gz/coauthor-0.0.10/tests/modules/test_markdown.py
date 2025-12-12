import tempfile
import logging
import pytest
from coauthor.utils.logger import Logger
import os
from coauthor.modules.markdown import process_frontmatter


class MockLogger:
    def info(self, message):
        print(message)

    def debug(self, message):
        print(message)

    def error(self, message):
        print(message)


def test_process_frontmatter():
    """
    Pytest test for process_frontmatter function.
    Tests inclusion of multiple files into the main content.
    """

    with tempfile.TemporaryDirectory() as temp_dir:

        # Create temporary files
        include_file1 = os.path.join(temp_dir, "include1.md")
        with open(include_file1, "w") as f:
            f.write("Content from include1\n\n")

        include_file2 = os.path.join(temp_dir, "include2.md")
        with open(include_file2, "w") as f:
            f.write("Content from include2\n\n")

        frontmatter = f"""---
title: whatever
a:
  b: whatever
include-files: [./include1.md, {include_file2}]
---
"""
        main_file = os.path.join(temp_dir, "main.md")
        with open(main_file, "w") as f:
            f.write(frontmatter + "\nwhatever")

        logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")

        config = {"current-task": {"path-modify-event": str(main_file), "content": ""}}

        process_frontmatter(config, logger)

        # Verify combined content
        expected_content = f"""{frontmatter}
Content from include1


Content from include2


"""
        logger.debug(f"expected_content: \n{expected_content}")
        logger.debug(f"content: \n{config['current-task']['content']}")
        # TODO remove debug
        # TODO remove debug
        import yaml

        with open("expected_content.txt", "w") as file:
            file.write(expected_content)
        with open("content.txt", "w") as file:
            file.write(config["current-task"]["content"])

        assert config["current-task"]["content"] == expected_content


def test_process_frontmatter_no_include_files():
    """
    Pytest test for process_frontmatter function.
    Tests file with no .
    """

    with tempfile.TemporaryDirectory() as temp_dir:

        frontmatter = """---
title: whatever
a:
  b: whatever
---
"""
        main_file = os.path.join(temp_dir, "main.md")
        with open(main_file, "w") as f:
            f.write(frontmatter + "\nwhatever")

        logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")

        config = {"current-task": {"path-modify-event": str(main_file), "content": ""}}

        process_frontmatter(config, logger)

        # Verify combined content
        expected_content = f"{frontmatter}\nwhatever"
        logger.debug(f"expected_content: \n{expected_content}")
        logger.debug(f"content: \n{config['current-task']['content']}")
        import yaml

        with open("expected_content.txt", "w") as file:
            file.write(expected_content)
        with open("content.txt", "w") as file:
            file.write(config["current-task"]["content"])

        assert config["current-task"]["content"] == expected_content
