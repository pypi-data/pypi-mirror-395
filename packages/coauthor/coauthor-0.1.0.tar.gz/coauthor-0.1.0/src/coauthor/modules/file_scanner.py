"""
This module provides functionality to scan directories and process files according to defined workflows and tasks.
It uses various utility functions and modules to handle file processing, including integration with OpenAI agents,
regex replacements, file read/write operations, and PlantUML processing. The main operations are facilitated
through the 'scan' method, which iterates over configured workflows and their associated tasks, performing necessary
file manipulations as specified.
"""

import os
from coauthor.modules.ai import process_file_with_openai_agent
from coauthor.utils.workflow_utils import get_workflows_that_scan
from coauthor.modules.file_processor import regex_replace_in_file, pong, include_file
from coauthor.modules.workflow_tasks import write_file, read_file
from coauthor.modules.plantuml import process_puml_file
from coauthor.modules.markdown import process_frontmatter
from coauthor.modules.web_tasks import replace_redirecting_links
from coauthor.modules.youtube import get_youtube_video_info

# from coauthor.modules.langgraph import process_file_with_langgraph

task_type_functions = {
    "ai": process_file_with_openai_agent,
    # "langgraph": process_file_with_langgraph,
    "regex_replace_in_file": regex_replace_in_file,
    "pong": pong,
    "write_file": write_file,
    "read_file": read_file,
    "plantuml": process_puml_file,
    "include-files": process_frontmatter,
    "include-file": include_file,
    "replace_redirecting_links": replace_redirecting_links,
    "youtube": get_youtube_video_info,
}


def scan(config, logger):
    """
    Scans directories according to workflows specified in the configuration.

    For each workflow that includes a scan operation, this function identifies
    directories to be scanned, and for each file within these directories, it performs
    the tasks defined in the workflow. Supported tasks include file processing with
    OpenAI agents, regex replacements, reading, and writing files, among others.

    Args:
        config (dict): Configuration dictionary containing scanning and workflow definitions.
        logger (Logger): Logging object for recording debug and info messages.
    """

    workflows_that_scan = get_workflows_that_scan(config, logger)
    logger.debug(f"workflows_that_scan: {workflows_that_scan}")
    base_path = config.get("path", os.getcwd())
    for workflow in workflows_that_scan:
        scan_directories = workflow["scan"]["filesystem"]["paths"]
        abs_scan_directories = [
            (
                os.path.abspath(os.path.join(base_path, os.path.expanduser(d)))
                if not os.path.isabs(os.path.expanduser(d))
                else os.path.expanduser(d)
            )
            for d in scan_directories
        ]
        logger.info(f"Workflow {workflow['name']}: scan directories {', '.join(abs_scan_directories)}")

        wd_to_path = {}
        for directory in abs_scan_directories:
            for root, _, files in os.walk(directory):
                for filename in files:
                    path = os.path.join(root, filename)
                    handle_workflow_scan_file(path, workflow, config, logger)


def handle_workflow_scan_file(path, workflow, config, logger):
    """
    Processes a file as part of a workflow task execution.

    For each file that is subject to a workflow's tasks, this function executes the
    specified tasks. It checks if the task type is supported and if so, performs the
    task using appropriate utility functions. An exception is raised for unsupported tasks.

    Args:
        path (str): The path to the file being processed.
        workflow (dict): The workflow definition containing tasks to be executed.
        config (dict): Configuration dictionary for current task and workflow context.
        logger (Logger): Logging object for recording debug and info messages.

    Raises:
        ValueError: If the task type specified in the workflow is not supported.
    """

    logger.info(f"Processing file {path}")
    for task in workflow["tasks"]:
        logger.debug(f"task: {task}")
        if task["type"] in task_type_functions:
            logger.debug(f"Workflow: {workflow['name']}, Task: {task['id']} → {path}")
            task["path-modify-event"] = path
            config["current-task"] = task
            config["current-workflow"] = workflow
            task_type_functions[task["type"]](config, logger)
        else:
            raise ValueError(f'Unsupported task_type: {task["type"]}')
