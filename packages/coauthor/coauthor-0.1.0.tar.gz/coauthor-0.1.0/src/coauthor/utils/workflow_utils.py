def get_all_watch_directories_from_workflows(config, logger):
    return get_all_directories_from_workflows(config, logger, "watch")


def get_all_scan_directories_from_workflows(config, logger):
    return get_all_directories_from_workflows(config, logger, "scan")


def get_all_directories_from_workflows(config, logger, watch_or_scan_key):
    dirs = set()  # Use a set to ensure that directories are unique
    for workflow in config["workflows"]:
        if "filesystem" in workflow[watch_or_scan_key]:
            dirs.update(workflow[watch_or_scan_key]["filesystem"]["paths"])
    return list(dirs)  # Convert the set back to a list for the return value


def get_workflows_that_watch(config, logger, watch_filesystem_or="filesystem"):
    wtw = []
    workflows = config.get("workflows", [])  # Default naar een lege lijst
    for workflow in workflows:
        if "watch" in workflow:
            if watch_filesystem_or in workflow["watch"]:
                wtw.append(workflow)
    logger.debug(f"get_workflows_that_watch: workflows_that_watch: {wtw}")
    return wtw


def get_workflows_that_scan(config, logger):
    workflows_that_scan = []
    workflows = config.get("workflows", [])

    for workflow in workflows:
        if "scan" in workflow:
            workflows_that_scan.append(workflow)
    logger.debug(f"get_workflows_that_scan: workflows_that_scan: {workflows_that_scan}")
    return workflows_that_scan
