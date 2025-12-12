import os
import tempfile
from coauthor.utils.jinja import render_template
import logging
from coauthor.utils.logger import Logger
import yaml
import subprocess
from coauthor.utils.jinja_filters import (
    select_task,
    get_task_attribute,
    TaskNotFoundError,
    AttributeNotFoundError,
    dirname,
    basename,
)


def get_config(jinja_search_path, some_file_to_include):
    return yaml.safe_load(
        f"""
---
jinja:
  search_path: {jinja_search_path}
workflows:
  - name: jinja-filters-test
    tasks:
      - id: test_jinja_filter_include_file_content
        path-modify-event: {some_file_to_include}
"""
    )


def get_config2():
    return yaml.safe_load(
        f"""
---
workflows:
  - name: whatever-workflow
    tasks:
      - id: task1
        name: First Task
        priority: High
      - id: task2
        name: Second Task
        priority: Low
"""
    )


def test_jinja_filter_include_file_content():
    """
    This test verifies we include files in content we render using Jinja
    template engine using Jinja filter include_file_content
    """
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    with tempfile.TemporaryDirectory() as temp_dir:
        some_file_to_include = os.path.join(temp_dir, "some_file_to_include.md")
        with open(some_file_to_include, "w") as f:
            f.write("some_content_to_include")
        path_user_template = os.path.join(temp_dir, "templates", "user.md")
        path_templates_dir = os.path.dirname(path_user_template)
        os.makedirs(path_templates_dir)
        with open(path_user_template, "w") as f:
            f.write('{{ config["current-task"]["path-modify-event"] | include_file_content }}')
        config = get_config(path_templates_dir, some_file_to_include)
        config["current-workflow"] = config["workflows"][0]
        task = config["current-workflow"]["tasks"][0]
        config["current-task"] = task
        template = os.path.basename(path_user_template)
        content = render_template(task, template, config, logger)
        assert content == "some_content_to_include"


def test_jinja_filter_get_git_diff():
    """
    This test setups a local git repository, adds a file, makes a local change,
    and then verifies the rendering of git diff content using the Jinja filter 'get_git_diff'.
    Also checks that files not added to git do not produce a diff
    and committed files with no changes return none.
    """

    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Initialize a git repository
        subprocess.run(["git", "init"], cwd=temp_dir, check=True)

        # Add and commit a file with content
        diff_file_path = os.path.join(temp_dir, "diff_file.txt")
        with open(diff_file_path, "w") as f:
            f.write("initial content\n")
        subprocess.run(["git", "add", "diff_file.txt"], cwd=temp_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=temp_dir, check=True)

        # Modify the file that is stored in git
        with open(diff_file_path, "a") as f:
            f.write("new content\n")

        # Add a new file, do not add it to git
        not_in_git_file_path = os.path.join(temp_dir, "not_in_git.txt")
        with open(not_in_git_file_path, "w") as f:
            f.write("content outside git\n")

        # Add and commit a file but no content change
        no_change_file_path = os.path.join(temp_dir, "no_change_file.txt")
        with open(no_change_file_path, "w") as f:
            f.write("no changes here\n")
        subprocess.run(["git", "add", "no_change_file.txt"], cwd=temp_dir, check=True)
        subprocess.run(["git", "commit", "-m", "No change commit"], cwd=temp_dir, check=True)

        # Template setup for the modified file in git
        path_user_template = os.path.join(temp_dir, "templates", "diff_template.md")
        path_templates_dir = os.path.dirname(path_user_template)
        os.makedirs(path_templates_dir)
        with open(path_user_template, "w") as f:
            f.write(
                '{% set diff_output = config["current-task"]["path-modify-event"] | get_git_diff %}\n{{ diff_output }}'
            )

        # Run the renderer for the modified file
        config = get_config(path_templates_dir, diff_file_path)
        config["current-workflow"] = config["workflows"][0]
        task_diff = config["current-workflow"]["tasks"][0]
        task_diff["path-modify-event"] = diff_file_path
        config["current-task"] = task_diff
        template = os.path.basename(path_user_template)
        content_diff = render_template(task_diff, template, config, logger)

        # Check the content_diff for expected git diff
        expected_diff = (
            "--- a/diff_file.txt\n" "+++ b/diff_file.txt\n" "@@ -1 +1,2 @@\n" " initial content\n" "+new content\n"
        )
        assert expected_diff in content_diff

        config = get_config(path_templates_dir, not_in_git_file_path)
        config["current-workflow"] = config["workflows"][0]
        task_not_in_git = config["current-workflow"]["tasks"][0]
        task_not_in_git["path-modify-event"] = not_in_git_file_path
        config["current-task"] = task_not_in_git

        # Run the renderer for the not-in-git file
        content_not_in_git = render_template(task_not_in_git, template, config, logger)
        assert content_not_in_git == "\n"

        config = get_config(path_templates_dir, no_change_file_path)
        config["current-workflow"] = config["workflows"][0]
        task_no_change = config["current-workflow"]["tasks"][0]
        task_no_change["path-modify-event"] = no_change_file_path
        config["current-task"] = task_no_change

        # Run the renderer for no-change file
        content_no_change = render_template(task_no_change, template, config, logger)
        assert content_no_change == "\n"


def test_jinja_filter_file_exists():
    """
    Test of filter file_exists that can be used to render content in a jinja template
    conditional on the existence of a file.
    """
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    with tempfile.TemporaryDirectory() as temp_dir:
        existing_file_path = os.path.join(temp_dir, "existing_file.txt")
        non_existing_file_path = os.path.join(temp_dir, "non_existing_file.txt")

        # Create the existing file
        with open(existing_file_path, "w") as f:
            f.write("This file exists.")

        # Template for checking file existence
        path_user_template = os.path.join(temp_dir, "templates", "existence_template.md")
        path_templates_dir = os.path.dirname(path_user_template)
        os.makedirs(path_templates_dir)
        with open(path_user_template, "w") as f:
            f.write(
                '{% if config["current-task"]["path-modify-event"] | file_exists %}'
                "File exists: True"
                "{% else %}"
                "File exists: False"
                "{% endif %}"
            )

        # Run the renderer for the existing file
        # task_existing = get_task(path_templates_dir, existing_file_path)
        config = get_config(path_templates_dir, existing_file_path)
        config["current-workflow"] = config["workflows"][0]
        task_existing = config["current-workflow"]["tasks"][0]
        task_existing["path-modify-event"] = existing_file_path
        config["current-task"] = task_existing
        template = os.path.basename(path_user_template)
        content_existing = render_template(task_existing, template, config, logger)
        assert content_existing.strip() == "File exists: True"

        # Run the renderer for the non-existing file
        config = get_config(path_templates_dir, non_existing_file_path)
        config["current-workflow"] = config["workflows"][0]
        task_non_existing = config["current-workflow"]["tasks"][0]
        task_non_existing["path-modify-event"] = non_existing_file_path
        config["current-task"] = task_non_existing
        content_non_existing = render_template(task_non_existing, template, config, logger)
        assert content_non_existing.strip() == "File exists: False"


def test_jinja_filter_dirname_and_basename():
    """
    Test dirname and basename filters that process paths in Jinja templates.
    """
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    with tempfile.TemporaryDirectory() as temp_dir:
        # Test dirname
        path = os.path.join(temp_dir, "subfolder", "file.txt")
        dirname_result = dirname(path)
        assert dirname_result == os.path.join(temp_dir, "subfolder")

        # Test basename
        basename_result = basename(path)
        assert basename_result == "file.txt"


def test_select_task():
    """
    Test select_task function to retrieve tasks based on ID.
    """

    config = get_config2()
    config["current-workflow"] = config["workflows"][0]
    # Test for a valid task ID
    selected_task = select_task(config, "task1")
    assert selected_task["name"] == "First Task"

    # Test for an invalid task ID
    try:
        select_task(config, "task3")
        assert False, "Expected TaskNotFoundError was not raised."
    except Exception as err:
        assert isinstance(err, TaskNotFoundError)


def test_get_task_attribute():
    """
    Test get_task_attribute function to retrieve an attribute from a task.
    """

    config = get_config2()
    config["current-workflow"] = config["workflows"][0]
    config["current-task"] = config["current-workflow"]["tasks"][0]

    # Test retrieving an existing attribute
    priority = get_task_attribute(config, "task1", "priority")
    assert priority == "High"

    # Test retrieving a non-existing attribute
    try:
        get_task_attribute(config, "task1", "deadline")
        assert False, "Expected AttributeNotFoundError was not raised."
    except Exception as err:
        assert isinstance(err, AttributeNotFoundError)

    # Test with a non-existing task ID
    try:
        get_task_attribute(config, "task3", "priority")
        assert False, "Expected TaskNotFoundError was not raised."
    except Exception as err:
        assert isinstance(err, TaskNotFoundError)

    # template_env.filters["get_task_attribute"] = get_task_attribute
    # template_env.globals["raise"] = raise_helper

    # logger.debug(f"Get Jinja template: {template_path}")
    # template = template_env.get_template(template_path)
    # context = {"config": config, "task": task, "workflow": config["current-workflow"]}
    # return template.render(context)


def test_raise_in_jinja_template():
    """
    Test raising an error in a Jinja template using the raise_helper function.
    """
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    config = get_config2()
    config["current-workflow"] = config["workflows"][0]
    task = config["current-workflow"]["tasks"][0]
    config["current-task"] = task

    with tempfile.TemporaryDirectory() as temp_dir:
        config["jinja"] = {"search_path": temp_dir}
        path_template = os.path.join(temp_dir, "templates", "whatever.md")
        path_templates_dir = os.path.dirname(path_template)
        os.makedirs(path_templates_dir)
        template_string = '{{ raise("uh oh...") }}'
        with open(path_template, "w") as f:
            f.write(template_string)
        try:
            content = render_template(task, "whatever.md", config, logger)
            assert content == ""
            assert False, "Expected RuntimeError was not raised."
        except RuntimeError as err:
            assert str(err) == "uh oh..."
