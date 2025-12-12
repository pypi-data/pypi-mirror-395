from jira import JIRA, JIRAError
from coauthor.utils.notify import notification
import os

import re


def get_jira_connection(jira_url, logger):
    jira_username = os.getenv("COAUTHOR_JIRA_USERNAME")
    jira_password = os.getenv("COAUTHOR_JIRA_PASSWORD")

    try:
        jira_instance = JIRA(jira_url, basic_auth=(jira_username, jira_password))
        logger.debug(f"Connected to JIRA at {jira_url}")
        return jira_instance
    except JIRAError as jira_error:
        logger.error(f"Failed to connect to JIRA at {jira_url}: {jira_error}")
        return


def execute_jira_query(jira_instance, query, logger):
    try:
        issues = jira_instance.search_issues(query)
        logger.debug(f"Found {len(issues)} issues for query: {query}")
        return issues
    except (JIRAError, ValueError) as exception_error:
        logger.error(f"Error executing JIRA query: {exception_error}")
        return


def jira_ticket_unanswered_comment(ticket, content_patterns, jira_username, logger):
    comments = ticket.fields.comment.comments
    if not comments:
        return None

    last_match_index = -1
    for i, comment in enumerate(comments):
        body = comment.body
        log_message = re.sub(r"[\r\n]+", " ", body)[:100]
        logger.debug(f"{comment.author.name} → {log_message}")
        if not comment.author.name == jira_username:  # don't answer coauthor own comments
            for pattern in content_patterns:
                if re.search(pattern, body):
                    log_message = re.sub(r"[\r\n]+", " ", body)[:100]
                    logger.debug(f'{ticket.key} matches pattern "{pattern}": {log_message}')
                    last_match_index = i
                    break

    if last_match_index == -1:
        return None

    # Check if there's any comment after the last matched one by jira_username
    answered = False
    for i in range(last_match_index + 1, len(comments)):
        comment = comments[i]
        if comment.author.name == jira_username:
            answered = True
            break

    if answered:
        return None

    return comments[last_match_index]


def jira_unanswered_comments(config, logger, tickets):
    """Check Jira tickets for unanswered content matches against defined patterns in comments."""
    jira_username = os.getenv("COAUTHOR_JIRA_USERNAME")
    workflow = config.get("current-workflow", {})
    content_patterns = workflow.get("content_patterns")
    if not content_patterns:
        logger.debug("No content patterns defined in workflow.")
        return []

    matching_tickets = []
    for ticket in tickets:
        unanswered_comment = jira_ticket_unanswered_comment(ticket, content_patterns, jira_username, logger)
        if unanswered_comment is not None:
            matching_tickets.append({"ticket": ticket, "comment": unanswered_comment})

    return matching_tickets


def get_updated_labels(current_labels, labels=None, labels_remove=None, logger=None, ticket_key=None):
    current_labels = current_labels[:]  # copy
    changed = False

    if labels_remove:
        removed_labels = [l for l in labels_remove if l in current_labels]
        if removed_labels:
            current_labels = [l for l in current_labels if l not in labels_remove]
            logger.info(f"{ticket_key} removed labels → {', '.join(removed_labels)}")
            changed = True

    if labels:
        added_labels = [l for l in labels if l not in current_labels]
        if added_labels:
            current_labels.extend(added_labels)
            logger.info(f"{ticket_key} labels → {', '.join(added_labels)}")
            changed = True

    return current_labels, changed


def jira_add_comment(config, logger, ticket, content, labels=None, labels_remove=None):
    jira_instance = config["current-jira-instance"]
    try:
        comment = jira_instance.add_comment(ticket, content)
        logger.debug(f"Added comment to {ticket.key} → {comment.id}")

        updated_fields = []

        current_labels = ticket.fields.labels or []
        new_labels, changed = get_updated_labels(current_labels, labels, labels_remove, logger, ticket.key)
        if changed:
            ticket.update(fields={"labels": new_labels})
            updated_fields.append("labels")

        args = config.get("args", None)
        if args and args.notify:
            notification(f"Coauthor updated {ticket.key}", "Coauthor added a comment to the Jira ticket")
        if updated_fields:
            logger.info(f"Updated {', '.join(updated_fields)} for {ticket.key}")
        return comment
    except JIRAError as error:
        logger.error(f"Failed to add comment to {ticket.key}: {error}")
        return None


def get_assigned_tickets(jira_instance, logger):
    jira_username = os.getenv("COAUTHOR_JIRA_USERNAME")
    if not jira_username:
        logger.error("Jira username/COAUTHOR_JIRA_USERNAME not set")
        return []
    query = f'assignee = "{jira_username}"'
    return execute_jira_query(jira_instance, query, logger) or []


def jira_update_description_summary(
    config, logger, ticket, summary, description, story_points=None, labels=None, labels_remove=None
):
    try:
        update_kwargs = {"summary": summary, "description": description}
        custom_fields = {}
        updated_fields = ["summary", "description"]

        if story_points is not None and ticket.fields.issuetype.name == "Story":
            story_point_field = "customfield_10007"  # TODO configure
            current_sp = getattr(ticket.fields, story_point_field, None)
            if current_sp != story_points:
                logger.info(f"{ticket.key} story_points → {story_points}")
                custom_fields[story_point_field] = story_points

        current_labels = ticket.fields.labels or []
        new_labels, changed = get_updated_labels(current_labels, labels, labels_remove, logger, ticket.key)
        if changed:
            custom_fields["labels"] = new_labels
            updated_fields.append("labels")

        ticket.update(**update_kwargs, fields=custom_fields)
        args = config.get("args", None)
        if args and args.notify:
            notification(f"Coauthor updated {ticket.key}", "Coauthor updated the Jira ticket")
        logger.info(f"Updated {', '.join(updated_fields)} for {ticket.key}")
        return True
    except JIRAError as error:
        logger.error(f"Failed to update summary and description for {ticket.key}: {error}")
        return False


def jira_assign_to_creator(logger, ticket):
    reporter = ticket.fields.reporter.name
    try:
        ticket.update(assignee={"name": reporter})
        logger.info(f"Assigned {ticket.key} to creator {reporter}")
        return True
    except JIRAError as error:
        logger.error(f"Failed to assign {ticket.key} to creator: {error}")
        return False
