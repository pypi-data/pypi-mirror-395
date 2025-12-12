# pylint: disable=broad-exception-caught
"""
Module for constructing AI messages based on configuration and templates.

This module provides functions to build lists of messages for AI interactions,
handling initial system and user messages, as well as additional messages
from various sources like frontmatter, files, or direct content.
"""

import os
from jinja2 import Template
from coauthor.utils.jinja import render_template, template_exists, prompt_template_path, render_content
from coauthor.utils.match_utils import file_submit_to_ai
from coauthor.utils.markdown import get_frontmatter_nested_value


def ai_messages(config, logger):
    """
    Construct and return a list of AI messages based on the configuration.

    This function initializes a list of messages, adds initial system and user
    messages, and then appends any additional messages specified in the task.

    Args:
        config (dict): Configuration dictionary containing the current task.
        logger (Logger): Logger instance for logging messages.

    Returns:
        list: A list of message dictionaries, each with 'role' and 'content'.
    """
    messages = []
    if not add_initial_messages(messages, config, logger):
        return []
    add_additional_messages(messages, config, logger)
    return messages


def add_initial_messages(messages, config, logger):
    """
    Add initial system and user messages to the messages list.

    This function retrieves and renders templates for system and user roles,
    appending them to the messages list if content is available.

    Args:
        messages (list): List to which messages will be appended.
        config (dict): Configuration dictionary containing the current task.
        logger (Logger): Logger instance for logging messages.

    Returns:
        bool: True if both messages were added successfully, False otherwise.
    """
    task = config["current-task"]
    for role in ["system", "user"]:
        path_template = prompt_template_path(config, f"{role}.md", logger)
        task[f"{role}_template_path"] = path_template
        content = ai_message_content(config, logger, path_template, role)
        if content:
            messages.append({"role": role, "content": content})
        else:
            logger.error("Message content missing!")
            return False
    return True


def add_additional_messages(messages, config, logger):
    """
    Add additional user messages to the messages list based on task configuration.

    This function processes additional messages specified in the task, rendering
    their content and appending them as user messages.

    Args:
        messages (list): List to which messages will be appended.
        config (dict): Configuration dictionary containing the current task.
        logger (Logger): Logger instance for logging messages.
    """
    task = config["current-task"]
    if "messages" not in task:
        return
    for msg in task["messages"]:
        logger.debug(f"message: {msg}")
        items = get_message_items(msg, task, config, logger)
        for item in items:
            if item is not None:
                if "frontmatter" in msg:
                    task["frontmatter-item"] = item
                elif "files" in msg:
                    task["user-message-context-file"] = item
            content = get_additional_message_content(msg, config, logger, task)
            if content:
                logger.info(f"Adding user message: {msg}")
                messages.append({"role": "user", "content": content})
            else:
                logger.error("Missing content for additional user message")


def get_message_items(msg, task, config, logger):
    """
    Retrieve items based on the message configuration.

    If the message specifies a frontmatter key, this function fetches the
    corresponding list from the task's frontmatter. If 'files' is specified,
    it renders the directory path and lists all files in that directory.

    Args:
        msg (dict): Message dictionary potentially containing 'frontmatter' or 'files' key.
        task (dict): Task dictionary containing frontmatter data.
        config (dict): Configuration dictionary.
        logger (Logger): Logger instance for logging messages.

    Returns:
        list: List of items from frontmatter or files, or [None] if not specified.
    """
    if "frontmatter" in msg:
        frontmatter_key = msg["frontmatter"]
        frontmatter_list = get_frontmatter_nested_value(task["path-modify-event"], frontmatter_key)
        if frontmatter_list is None or not frontmatter_list:
            return []
        return frontmatter_list
    if "files" in msg:
        try:
            template_path = msg["files"]
            dir_path = render_content(task, template_path, config, logger)
            logger.debug(f"Looking for files in dir_path: {dir_path}")
        except Exception as exception_error:
            logger.error(f"Failed to render files path: {exception_error}")
            return []
        if not os.path.isdir(dir_path):
            logger.error(f"Directory does not exist: {dir_path}")
            return []
        files = []
        for root, _dirs, filenames in os.walk(dir_path):
            for filename in filenames:
                full = os.path.join(root, filename)
                files.append(full)
        logger.debug(f"Files to include as user message: {', '.join(files)}")
        return files
    return [None]


def get_additional_message_content(msg, config, logger, task):
    """
    Generate content for an additional message.

    This function retrieves content either from a file template or by rendering
    a Jinja2 template string provided in the message.

    Args:
        msg (dict): Message dictionary with 'file' or 'content' for sourcing.
        config (dict): Configuration dictionary.
        logger (Logger): Logger instance for logging messages.
        task (dict): Current task dictionary.

    Returns:
        str or None: The rendered message content, or None if rendering fails.
    """
    content = None
    if "file" in msg:
        path_template = msg["file"]
        content = ai_message_content(config, logger, path_template, "user")
    elif "content" in msg:
        template_string = msg["content"]
        try:
            template = Template(template_string)
            content = template.render(task=task, config=config)
        except Exception as exception_error:
            logger.error(f"Failed to render content: {exception_error}")
            content = None
    else:
        logger.error("Message has neither 'file' nor 'content'")
    return content


def ai_message_content(config, logger, path_template, system_or_user):
    """
    Retrieve or render content for an AI message.

    This function checks for template existence and renders it, falls back to
    task data, or uses file content for user messages in modify events.

    Args:
        config (dict): Configuration dictionary containing the current task.
        logger (Logger): Logger instance for logging messages.
        path_template (str): Path to the template file.
        system_or_user (str): Role of the message ('system' or 'user').

    Returns:
        str or None: The message content, or None if not found.
    """
    task = config["current-task"]
    message_content = None
    if template_exists(task, path_template, config, logger):
        message_content = render_template(task, path_template, config, logger)
    elif system_or_user in task:
        message_content = task[system_or_user]
    elif "path-modify-event" in task and system_or_user == "user":
        logger.info(f"Using the file {task['path-modify-event']} as the user message")
        message_content = file_submit_to_ai(config, logger)
    return message_content
