"""
Module for initializing and managing workflows in the coauthor system.

This module handles the setup and execution of scan and watch operations
based on the provided configuration. It integrates with file scanning,
watching, and Jira watching functionalities.
"""

import os
import copy
from coauthor.utils.config import get_projects
from coauthor.modules.file_scanner import scan
from coauthor.modules.file_watcher import watch
from coauthor.modules.jira_watcher import watch as watch_jira
from coauthor.utils.workflow_utils import (
    get_all_scan_directories_from_workflows,
    get_all_watch_directories_from_workflows,
    get_workflows_that_watch,
)


def initialize_workflows(config, logger, trigger_scan=False):
    """
    Initialize and execute workflows based on the provided configuration.

    This function checks for workflows in the config, handles scan and watch modes,
    and triggers the appropriate scanning or watching operations. It logs warnings
    and information as necessary.

    Args:
        config (dict): The configuration dictionary containing workflows and args.
        logger (Logger): The logger instance for logging messages.
        trigger_scan (bool, optional): Whether to trigger a scan regardless of args. Defaults to False.
    """
    if not "workflows" in config and not "projects" in config:
        logger.warning("No workflows or projects found in the configuration. The program will now exit as there is nothing to do.")
        return
    args = config.get("args", None)
    if (args and args.scan) or trigger_scan:
        logger.info("Scan mode enabled with --scan")
        projects = get_projects(config)
        for proj in projects:
            if "workflows" in proj:
                scan_directories = get_all_scan_directories_from_workflows(proj, logger)
                logger.info(f"Project {proj.get('name', 'main')}: scan_directories: {', '.join(scan_directories)}")
                if len(scan_directories) > 0:
                    scan(proj, logger)
                else:
                    logger.debug("No scan directories specified in workflows!")
    if args and args.watch:
        logger.info("Watch mode enabled with --watch")
        projects = get_projects(config)
        for proj in projects:
            project_path = proj.get("path", os.getcwd())
            logger.info(f"Initializing workflows for project {proj.get('name', 'unnamed')} at {project_path}")
            workflows_that_watch_jira = get_workflows_that_watch(proj, logger, "jira")
            if workflows_that_watch_jira:
                logger.debug("Jira workflows found")
                watch_jira(copy.deepcopy(proj), logger)
            else:
                logger.debug("There are NO workflows with Jira in this project")
        watch(config, logger)  # watch handles multi-project internally
