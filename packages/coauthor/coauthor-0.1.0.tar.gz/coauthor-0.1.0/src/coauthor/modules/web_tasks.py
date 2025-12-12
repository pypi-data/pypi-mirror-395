import os
import re
import requests
import time


def replace_redirecting_links(config, logger):
    task = config["current-task"]
    path = task["path-modify-event"]

    regex = re.compile(task["regex"], re.DOTALL)
    logger.debug(f"regex: {regex}")

    updated = False
    match_found = False

    with open(path, "r", encoding="utf-8") as main_file:
        content = main_file.read()

    # logger.debug(f"content: {content}")
    for match in regex.finditer(content):
        match_found = True
        link = match.group(1)
        logger.debug(f"Match found {link}")

        redirect, new_link = check_redirection(link)
        if redirect:
            updated = True
            content = content.replace(link, new_link)
            logger.info(f"Updated link {link} → {new_link}")

    if not match_found:
        logger.debug(f"No redirect links found")
        return False

    if not updated and match_found:
        logger.debug(f"Content is up to date. No links redirected")
        return False

    with open(path, "w", encoding="utf-8") as file:
        time.sleep(3)
        file.write(content)

    return True


def check_redirection(url):
    try:
        response = requests.get(
            url, allow_redirects=False, timeout=10
        )  # Added a timeout of 10 seconds to prevent hanging indefinitely

        # Check if the status code is a redirection (3xx)
        if 300 <= response.status_code < 400:
            return True, response.headers["Location"]
        return False, url

    except requests.RequestException as request_exception:
        raise Exception(f"An error occurred: {request_exception}") from request_exception
