import os
import re


def file_submit_to_ai(config, logger):
    """
    Return the content of the file if it requires AI processing based on path and content matching criteria.

    Parameters:
    - config (dict): Configuration dictionary containing 'current-task' and 'current-workflow'.
    - logger (Logger): Logger to log debug and warning messages.

    Returns:
    - str: The content of the file if both path and content match the specified regex patterns in
      the task.
    - None: If the content doesn't meet the regex requirements.

    The function checks if the file path and content match the given regex patterns in the task.
    """
    path = config["current-task"]["path-modify-event"]
    path_match = file_path_match(config, logger)
    content_match = file_content_match(config, logger)
    content = None
    if path_match:
        if content_match:
            with open(path, "r", encoding="utf-8") as file1:
                content = file1.read()
    logger.debug(f"file_submit_to_ai: path_match: {path_match}, content_match: {content_match}")
    return content


def regex_content_match(content, workflow, patterns_key, matches_key, logger):
    """
    Determine if the given content matches any provided regex patterns.

    Parameters:
    - content (str): The content to be validated against the regex.
    - workflow (dict): Should contain a list under 'content_patterns' with regex patterns to match
      against the content. Also updates 'content_matches' with the match object of each match.
    - patterns_key: content_patterns or path_patterns
    - matches_key: content_matches or path_matches

    Returns:
    - bool: True if the content matches any of the regex patterns, otherwise False.

    The function checks the content against each regex pattern for a match, updating the
    'content_matches' list in the workflow with the match object.
    """
    logger.debug(f"workflow: {workflow}")
    logger.debug(f"patterns_key: {patterns_key}, matches_key: {matches_key}")
    regex = workflow[patterns_key]
    workflow[matches_key] = []
    for pattern in regex:
        if isinstance(pattern, list):
            sub_patterns_all_match = True
            for sub_pattern in pattern:
                match_object = re.search(sub_pattern, content, re.IGNORECASE | re.DOTALL)
                workflow[matches_key].append(match_object)
                match = bool(match_object)
                if not match:
                    logger.debug(f"no match for sub_pattern: {sub_pattern} → sub_patterns_all_match = False")
                    sub_patterns_all_match = False
            if sub_patterns_all_match:
                logger.debug(f"regex_content_match: match True for pattern: {pattern}, content: {content}")
                return True
        else:
            match_object = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            workflow[matches_key].append(match_object)
            if match_object:
                logger.debug(f"regex_content_match: match: True for pattern: {pattern}, content: {content}")
                return True
    return False


def regex_content_match_named_group(workflow, named_group, logger):
    """
    Iterate through all "content_matches" of "workflow" and return the value of a named group if it exists in any match.

    Parameters:
    - workflow (dict): Contains 'content_matches' list with regex match results.
    - named_group (str): The named group to check within the content matches.
    - logger (Logger): Logger to log debug messages.

    Returns:
    - str: Value of the named group if found, otherwise None.
    """
    for match in workflow["content_matches"]:
        if isinstance(match, re.Match):
            if named_group in match.groupdict():
                logger.debug(f"regex_content_match_named_group: Found named group '{named_group}'")
                return match.group(named_group)
    logger.debug(f"regex_content_match_named_group: Named group '{named_group}' not found")
    return None


def file_path_match(config, logger):
    """
    Check if the file path matches the regex pattern specified in the workflow.

    Parameters:
    - config (dict): Configuration dictionary containing 'current-task' and 'current-workflow'.
    - logger (Logger): Logger to log debug and warning messages.

    Returns:
    - bool: True if the path matches the regex or if no 'path_patterns' is specified, otherwise False.
    """
    workflow = config["current-workflow"]
    path = config["current-task"]["path-modify-event"]
    if "path_patterns" in workflow:
        return regex_content_match(path, workflow, "path_patterns", "path_matches", logger)
    return True


def file_content_match(config, logger):
    """
    Check if the file content matches the regex pattern specified in the workflow configuration.

    Parameters:
    - config (dict): Configuration dictionary containing 'current-task' and 'current-workflow'.
    - logger (Logger): Logger to log debug and warning messages.

    Returns:
    - bool: True if the content matches the regex, otherwise False.
    """
    workflow = config["current-workflow"]
    path = config["current-task"]["path-modify-event"]
    if not os.path.exists(path):
        logger.warning(f"file_content_match: path {path} does not exist!")
        return False

    if "content_patterns" in workflow:
        logger.debug(f"file_content_match: content_patterns: {workflow['content_patterns']}")
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
        if regex_content_match(content, workflow, "content_patterns", "content_matches", logger):
            return True
    else:
        logger.warning(f"file_content_match: workflow has no content_patterns! So content match is false! ")
        logger.debug(f"workflow: {workflow}")
    return False


def path_new_replace(path, search, replace):
    """
    Replace a portion of the path with a new string.

    Parameters:
    - path (str): The original path string.
    - search (str): The substring to search for in the path.
    - replace (str): The string to replace the search substring with.

    Returns:
    - str: The modified path with the substitutions made.
    """
    return path.replace(search, replace)
