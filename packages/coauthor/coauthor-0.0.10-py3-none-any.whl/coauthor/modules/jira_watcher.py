import os
import re
import time
import yaml
import json
from threading import Thread
from collections import defaultdict
from jira import JIRA, JIRAError
from coauthor.utils.workflow_utils import (
    get_workflows_that_watch,
)
from coauthor.utils.jira_utils import (
    jira_unanswered_comments,
    execute_jira_query,
    get_jira_connection,
    jira_add_comment,
    get_assigned_tickets,
    jira_update_description_summary,
    jira_assign_to_creator,
)
from coauthor.modules.ai import process_file_with_openai_agent


def parse_ai_response(response, logger):
    log_message = re.sub(r"[\r\n]+", " ", str(response))[:100]
    logger.info(f"AI response → {log_message}")
    try:
        response_json = json.loads(response)
    except (json.JSONDecodeError, TypeError) as exception_error:
        logger.error(f"Error parsing JSON response: {exception_error}")
        response_json = response if isinstance(response, dict) else None
    return response_json


task_type_functions = {
    "ai": process_file_with_openai_agent,
}


def watch(config, logger):
    logger.info("Watching Jira workflows")
    # watch_jira(config, logger)
    new_thread = Thread(target=watch_jira, args=(config, logger))
    new_thread.start()


def watch_jira(config, logger):
    workflows_that_watch_jira = get_workflows_that_watch(config, logger, "jira")
    while True:
        for workflow in workflows_that_watch_jira:
            config["current-workflow"] = workflow
            jira_config = workflow["watch"]["jira"]
            sleep_time = jira_config.get("sleep", 15)
            logger.debug(f"Starting thread for workflow {workflow['name']}, sleep {sleep_time} seconds")
            process_jira_comments(config, logger)
            process_jira_tickets(config, logger)
            time.sleep(sleep_time)


def process_jira_comments(config, logger):
    workflow = config["current-workflow"]
    jira_config = workflow["watch"]["jira"]
    jira_url = jira_config.get("url") or os.environ.get("COAUTHOR_JIRA_URL")
    logger.debug(f"Checking Jira in workflow {workflow['name']}")
    jira_query = jira_config.get("query", "updated >= -0.3h OR created >= -0.3h")
    if not jira_url or not jira_query:
        logger.error(f"JIRA configuration missing. Skipping. jira_config: {jira_config}")
        return
    jira_instance = get_jira_connection(jira_url, logger)
    config["current-jira-instance"] = jira_instance
    if not jira_instance:
        return
    all_tickets = execute_jira_query(jira_instance, jira_query, logger)
    if not all_tickets:
        logger.debug("No Jira tickets found")
        return
    tickets = jira_unanswered_comments(config, logger, all_tickets)
    if not tickets:
        logger.debug("No Jira tickets with a content match found")
        return
    ticket_list = [f"{ticket['ticket'].key} - {ticket['ticket'].fields.summary}" for ticket in tickets]
    logger.info(f"Found tickets with unanswered comments: {', '.join(ticket_list)}")
    for ticket in tickets:
        config["current-ticket"] = ticket["ticket"]
        config["current-comment"] = ticket["comment"]
        get_related_tickets(config, logger, ticket["ticket"])
        handle_jira_comments(config, logger)


def handle_jira_comments(config, logger):
    comment = config["current-comment"]
    ticket = config["current-ticket"]
    workflow = config["current-workflow"]
    logger.info(f"Processing ticket {ticket.key}")
    for task in workflow["tasks"]:
        task["current-ticket"] = ticket
        task["related-tickets"] = config["related-tickets"]
        task["current-comment"] = comment
        logger.debug(f"task: {task}")
        if task["type"] in task_type_functions:
            config["current-task"] = task
            task["json"] = True
            logger.debug(f"Workflow: {workflow['name']}, Task: {task['id']} → {ticket.key}")
            config["current-task"] = task
            task_type_functions[task["type"]](config, logger)
            response = task["response"]
            response_json = parse_ai_response(response, logger)
            if response_json and isinstance(response_json, dict):
                if "comment" in response_json:
                    comment_text = response_json["comment"]
                    labels = response_json.get("labels", None)
                    labels_remove = response_json.get("labels_remove", None)
                    jira_add_comment(config, logger, ticket, comment_text, labels, labels_remove)
                else:
                    logger.error("Response JSON missing 'comment' key")
            else:
                logger.error("Invalid response for comment processing")
        else:
            raise ValueError(f'Unsupported task_type: {task["type"]}')


def get_related_tickets(config, logger, ticket):
    jira_instance = config["current-jira-instance"]
    related = {}

    if hasattr(ticket.fields, "parent") and ticket.fields.parent:
        try:
            related["parent"] = jira_instance.issue(ticket.fields.parent.key, fields="summary,description")
        except JIRAError as jira_error:
            logger.error(f"Failed to fetch parent for {ticket.key}: {jira_error}")

    # See Jira Settings > Issues > Custom fields
    possible_epic_fields = ["customfield_10011"]
    epic_key = None
    for field in possible_epic_fields:
        epic_key = getattr(ticket.fields, field, None)
        if epic_key:
            break
    if epic_key:
        try:
            related["epic"] = jira_instance.issue(epic_key, fields="summary,description")
        except JIRAError as jira_error:
            logger.error(f"Failed to fetch epic {epic_key} for {ticket.key}: {jira_error}")

    # Fetch linked issues
    linked_issues = []
    if hasattr(ticket.fields, "issuelinks") and ticket.fields.issuelinks:
        for link in ticket.fields.issuelinks:
            if hasattr(link, "outwardIssue") and link.outwardIssue:
                try:
                    linked_ticket = jira_instance.issue(link.outwardIssue.key, fields="summary,description")
                    linked_issues.append({"type": link.type.outward.lower(), "ticket": linked_ticket})
                except JIRAError as jira_error:
                    logger.error(f"Failed to fetch outward link {link.outwardIssue.key} for {ticket.key}: {jira_error}")
            elif hasattr(link, "inwardIssue") and link.inwardIssue:
                try:
                    linked_ticket = jira_instance.issue(link.inwardIssue.key, fields="summary,description")
                    linked_issues.append({"type": link.type.inward.lower(), "ticket": linked_ticket})
                except JIRAError as jira_error:
                    logger.error(f"Failed to fetch inward link {link.inwardIssue.key} for {ticket.key}: {jira_error}")
    related["linked"] = linked_issues

    # Now group dynamically
    grouped = defaultdict(list)
    for link in related["linked"]:
        grouped[link["type"]].append({"ticket": link["ticket"]})
    related["grouped_linked"] = dict(grouped)

    config["related-tickets"] = related


def process_jira_tickets(config, logger):
    workflow = config["current-workflow"]
    jira_config = workflow["watch"]["jira"]
    jira_url = jira_config.get("url") or os.environ.get("COAUTHOR_JIRA_URL")
    logger.debug(f"Checking assigned Jira tickets in workflow {workflow['name']}")
    if not jira_url:
        logger.error(f"JIRA URL missing. Skipping. jira_config: {jira_config}")
        return
    if "current-jira-instance" in config:
        jira_instance = config["current-jira-instance"]
    else:
        jira_instance = get_jira_connection(jira_url, logger)
        config["current-jira-instance"] = jira_instance
    if not jira_instance:
        return
    tickets = get_assigned_tickets(jira_instance, logger)
    if not tickets:
        logger.debug("No assigned Jira tickets found")
        return
    ticket_list = [f"{ticket.key} - {ticket.fields.summary}" for ticket in tickets]
    logger.info(f"Found assigned tickets: {', '.join(ticket_list)}")
    for ticket in tickets:
        config["current-ticket"] = ticket
        get_related_tickets(config, logger, ticket)
        handle_jira_tickets(config, logger)


def handle_jira_tickets(config, logger):
    ticket = config["current-ticket"]
    workflow = config["current-workflow"]
    logger.info(f"Processing assigned ticket {ticket.key}")
    for task in workflow["tasks"]:
        task["current-ticket"] = ticket
        task["related-tickets"] = config["related-tickets"]
        if "current-comment" in task:
            del task["current-comment"]
        logger.debug(f"task: {task}")
        if task["type"] in task_type_functions:
            logger.debug(f"Workflow: {workflow['name']}, Task: {task['id']} → {ticket.key}")
            config["current-task"] = task
            task["json"] = True
            task_type_functions[task["type"]](config, logger)
            response = task["response"]
            response_json = parse_ai_response(response, logger)
            if response_json and isinstance(response_json, dict):
                if "summary" in response_json and "description" in response_json:
                    summary = response_json["summary"]
                    description = response_json["description"]
                    labels = response_json.get("labels", None)
                    labels_remove = response_json.get("labels_remove", None)
                    story_points = response_json.get("story_points", None)
                    jira_update_description_summary(
                        config, logger, ticket, summary, description, story_points, labels, labels_remove
                    )
                else:
                    logger.error("Response JSON missing 'summary' or 'description' key")
            else:
                logger.error("Invalid response for ticket update")
            try:
                jira_assign_to_creator(logger, ticket)
            except Exception as exception_error:
                logger.error(f"Failed to assign ticket {ticket.key} to creator: {exception_error}")
                raise ValueError(f"Assignment failed for {ticket.key}: {exception_error}") from exception_error
        else:
            raise ValueError(f'Unsupported task_type: {task["type"]}')
