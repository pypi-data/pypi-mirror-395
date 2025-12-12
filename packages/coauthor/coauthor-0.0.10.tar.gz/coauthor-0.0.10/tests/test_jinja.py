import pytest
import jinja2
from tempfile import TemporaryDirectory
from unittest import mock
from coauthor.utils.jinja import render_template_to_file, render_template
from coauthor.modules.ai import prompt_template_path
from coauthor.utils.logger import Logger
import logging
import os

# Sample custom delimiters for testing
custom_delimiters = {
    "block_start_string": "{%",
    "block_end_string": "%}",
    "variable_start_string": "{{{",
    "variable_end_string": "}}}",
}


def get_config(temp_dir):
    return {
        "jinja": {"search_path": temp_dir},
        "current-task": {"id": "ai-file-update"},
        "current-workflow": {"name": "workflow-name"},
    }


def test_render_template():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    with TemporaryDirectory() as temp_dir:
        template_content = "id: {{ config['current-task']['id'] }}"
        config = get_config(temp_dir)
        task = config["current-task"]
        template_name = "template.txt"
        template_path = f"{temp_dir}/{template_name}"

        # Write a template file in the temporary directory
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(template_content)

        # Create path_to_write for render_template_to_file to write to
        path_to_write = f"{temp_dir}/output.txt"

        # Call the function to test
        content = render_template(task, template_name, config, logger)

        assert content == f"id: {task['id']}"


def test_render_template_to_file():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    with TemporaryDirectory() as temp_dir:
        template_content = "id: {{ config['current-task']['id'] }}"
        config = get_config(temp_dir)
        task = config["current-task"]
        template_name = "template.txt"
        template_path = f"{temp_dir}/{template_name}"

        # Write a template file in the temporary directory
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(template_content)

        # Create path_to_write for render_template_to_file to write to
        path_to_write = f"{temp_dir}/output.txt"

        # Call the function to test
        render_template_to_file(task, template_name, path_to_write, config, logger)

        # Read the written content and assert it is as expected
        with open(path_to_write, "r", encoding="utf-8") as f:
            written_content = f.read()

        assert written_content == f"id: {task['id']}"


def test_render_template_custom_delimiters():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    with TemporaryDirectory() as temp_dir:
        template_content = "id: {{{ config['current-task']['id'] }}}"
        config = get_config(temp_dir)
        task = config["current-task"]
        config["jinja"]["custom_delimiters"] = custom_delimiters
        template_name = "template.txt"
        template_path = f"{temp_dir}/{template_name}"

        # Write a template file in the temporary directory
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(template_content)

        # Create path_to_write for render_template_to_file to write to
        path_to_write = f"{temp_dir}/output.txt"

        # Call the function to test
        content = render_template(task, template_name, config, logger)

        assert content == f"id: {task['id']}"


def test_render_template_to_file_subdirs():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    with TemporaryDirectory() as temp_dir:
        template_content = "id: {{ config['current-task']['id'] }}"
        config = get_config(temp_dir)
        task = config["current-task"]
        template_name = "template.txt"
        template_path = f"{temp_dir}/dir1/dir2/{template_name}"
        os.makedirs(os.path.dirname(template_path), exist_ok=True)

        # Write a template file in the temporary directory
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(template_content)

        # Create path_to_write for render_template_to_file to write to
        path_to_write = f"{temp_dir}/output.txt"

        # Call the function to test
        render_template_to_file(task, f"dir1/dir2/{template_name}", path_to_write, config, logger)
        render_template_to_file(task, f"dir2/{template_name}", path_to_write, config, logger)
        render_template_to_file(task, f"{template_name}", path_to_write, config, logger)

        # Read the written content and assert it is as expected
        with open(path_to_write, "r", encoding="utf-8") as f:
            written_content = f.read()

        assert written_content == f"id: {task['id']}"


def test_render_template_to_file_template_non_default_location():
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    with TemporaryDirectory() as temp_dir:
        template_content = "id: {{ config['current-task']['id'] }}"
        config = get_config(temp_dir)
        task = config["current-task"]
        template_name = "template.txt"
        template_name_default = prompt_template_path(config, "system.md", logger)
        template_path = f"{temp_dir}/{template_name}"

        # Write a template file in the temporary directory
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(template_content)

        # Create path_to_write for render_template_to_file to write to
        path_to_write = f"{temp_dir}/output.txt"

        with pytest.raises(jinja2.exceptions.TemplateNotFound) as excinfo:
            # Call the function to test
            render_template_to_file(task, template_name_default, path_to_write, config, logger)

        assert "workflow-name/ai-file-update/system.md" in str(excinfo.value)
