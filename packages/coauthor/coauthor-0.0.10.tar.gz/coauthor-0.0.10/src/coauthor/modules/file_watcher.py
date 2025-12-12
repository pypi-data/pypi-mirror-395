import os
import time
from inotify_simple import INotify, flags

from coauthor.utils.workflow_utils import (
    get_workflows_that_watch,
    get_all_watch_directories_from_workflows,
)
from coauthor.utils.match_utils import file_path_match, file_content_match
from coauthor.utils.inotify_utils import get_recently_modified_file
from coauthor.modules.ai import process_file_with_openai_agent
from coauthor.modules.file_processor import regex_replace_in_file, pong, include_file
from coauthor.modules.workflow_tasks import write_file, read_file
from coauthor.modules.plantuml import process_puml_file
from coauthor.modules.markdown import process_frontmatter
from coauthor.modules.web_tasks import replace_redirecting_links
from coauthor.modules.youtube import get_youtube_video_info


task_type_functions = {
    "ai": process_file_with_openai_agent,
    "regex_replace_in_file": regex_replace_in_file,
    "pong": pong,
    "write_file": write_file,
    "read_file": read_file,
    "plantuml": process_puml_file,
    "include-files": process_frontmatter,
    "include-file": include_file,  # TODO better naming
    "replace_redirecting_links": replace_redirecting_links,
    "youtube": get_youtube_video_info,
}

# Initialize a dictionary to store the last modification time of each file based
# on workflow and task
last_modification_times = {}


def add_watch_recursive(proj, inotify, directory):
    """Recursively add watches on all subdirectories,
    ignoring certain directories.

    Args:
        proj (dict): The project configuration.
        inotify (INotify): The INotify instance to add watches.
        directory (str): The root directory to begin adding watches.

    Returns:
        dict: A dictionary mapping watch descriptors to paths.
    """
    ignore_folders = proj.get("file-watcher", {}).get("ignore-folders", [])
    wd_to_path = {}
    for root, dirs, _ in os.walk(directory):
        # Ignore specific directories like __pycache__ and .obsidian
        dirs[:] = [d for d in dirs if d not in ignore_folders]
        if any(ignore in root for ignore in ignore_folders):
            continue
        watch_descriptor = inotify.add_watch(root, flags.CREATE | flags.MODIFY)
        wd_to_path[watch_descriptor] = root
    return wd_to_path


def watch(config, logger):
    """Start watching directories specified in the config and handle events.

    Args:
        config (dict): Configuration settings for the watcher.
        logger (Logger): A logger object for logging messages.
    """
    watch_directory(config, logger)


def get_project_for_path(file_path, path_to_project):
    """Find the project configuration for a given file path using longest prefix match.

    Args:
        file_path (str): The path of the file.
        path_to_project (dict): Mapping of project root paths to project configs.

    Returns:
        dict: The project configuration, or None if no match.
    """
    matches = []
    abs_path = os.path.abspath(os.path.expanduser(file_path))
    for root, proj in path_to_project.items():
        if abs_path.startswith(root):
            matches.append((len(root), proj))
    if not matches:
        return None
    matches.sort(reverse=True)
    return matches[0][1]


def handle_inotify_event(event, wd_to_path, inotify, path_to_project, logger):
    """Handle inotify events by accurately determining the file changed.

    For MODIFY events, due to some editors' behavior of replacing files rather than directly modifying them,
    this function identifies the most recently updated file in the event's directory as the file affected by the event.

    Args:
        event (Event): The inotify event object.
        wd_to_path (dict): A mapping of watch descriptors to directory paths.
        inotify (INotify): The INotify instance handling the events.
        path_to_project (dict): Mapping of project roots to configs.
        logger (Logger): A logger object for logging messages.

    Returns:
        bool: True if a stop file was detected and processed, otherwise False.
    """
    directory = wd_to_path.get(event.wd, ".")
    logger.debug(
        f"Inotify Event: directory={directory}, event_mask={event.mask}, flags.from_mask={flags.from_mask(event.mask)}"
    )

    proj = get_project_for_path(directory, path_to_project)
    if not proj:
        logger.warning(f"No project found for directory {directory}")
        return False

    file_path_inotify = os.path.join(directory, event.name)
    file_path = get_recently_modified_file(file_path_inotify, directory, logger)

    # Check if it is a directory and add watch if new directory is created
    if flags.CREATE in flags.from_mask(event.mask) and os.path.isdir(file_path_inotify):
        logger.info(f"Watching new directory: {file_path_inotify}")
        new_wd_to_path = add_watch_recursive(proj, inotify, file_path_inotify)
        wd_to_path.update(new_wd_to_path)

    if file_path_inotify != file_path:
        logger.warning(f"file_path_inotify: {file_path_inotify} is not equal to file_path: {file_path}")
        logger.debug(" this can occur depending on how editors write changes to files")
        logger.debug(" For example Gedit uses a temporary file .goutputstream-G1SHX2")
        file_path_selected = file_path
        time.sleep(2)  # allow Gedit some time to finish updating file
    else:
        file_path_selected = file_path_inotify

    if is_binary_file(file_path_selected, logger):
        logger.debug(f"Ignoring binary file: {file_path_selected}")
        return False

    ignore_extensions = proj.get("watch-ignore-file-extensions", [])
    if flags.MODIFY in flags.from_mask(event.mask) and file_path_selected:
        file_extension = os.path.splitext(file_path_selected)[1]
        if file_extension not in ignore_extensions:
            logger.info(f"MODIFY event: file_path_inotify: {file_path_selected}")
            handle_workflow_file_modify_event(file_path_selected, proj, logger)
        else:
            logger.debug(f"Ignore MODIFY event {file_path_selected} because of file extension {file_extension}")

    if os.path.basename(file_path_selected) == "stop":
        logger.info("Stop file found!")
        os.remove(file_path_selected)
        return True

    return False


def is_binary_file(filepath, logger):
    """Check if a file is binary by reading a portion of its content.

    Args:
        filepath (str): The path to the file.
        logger (Logger): A logger object for logging errors.

    Returns:
        bool: True if the file is binary, False otherwise.
    """
    if not filepath or os.path.isdir(filepath):
        logger.debug(f"Skipping non-file or None path: {filepath}")
        return False
    try:
        with open(filepath, "rb") as file:
            # Read part of the file to determine if it's binary
            chunk = file.read(1024)
            if b"\0" in chunk:
                return True
    except OSError as os_error:
        # Log any exception that might occur while reading the file
        logger.error(f"Error reading file {filepath}: {os_error}")
    return False


def watch_directory(config, logger):
    """Continuously watch specified directories for changes and handle events.

    Args:
        config (dict): Configuration settings specifying directories to watch.
        logger (Logger): A logger object for logging messages.
    """

    project_list = []
    if "projects" in config:
        project_list = config["projects"] + [config]
    else:
        project_list = [config]

    all_watch_directories = []
    path_to_project = {}

    inotify = INotify()
    wd_to_path = {}

    for proj in project_list:
        proj_path = os.path.expanduser(proj.get("path", os.getcwd()))
        abs_proj_path = os.path.abspath(proj_path)
        path_to_project[abs_proj_path] = proj

        if "workflows" in proj:
            proj_dirs = get_all_watch_directories_from_workflows(proj, logger)
            abs_dirs = [
                (
                    os.path.abspath(os.path.join(proj_path, os.path.expanduser(d)))
                    if not os.path.isabs(os.path.expanduser(d))
                    else os.path.expanduser(d)
                )
                for d in proj_dirs
            ]
            all_watch_directories.extend(abs_dirs)

            for abs_dir in abs_dirs:
                wd_to_path.update(add_watch_recursive(proj, inotify, abs_dir))
        else:
            logger.debug(f"Skipping project {proj_path} as it has no workflows")

    # Deduplicate watch directories if necessary
    watch_directories = list(set(all_watch_directories))
    logger.info(f"Watching directories recursively: {', '.join(watch_directories)}")

    try:
        while True:
            for event in inotify.read():
                if handle_inotify_event(event, wd_to_path, inotify, path_to_project, logger):
                    return
    except KeyboardInterrupt:
        logger.info("Stopping directory watch")
    finally:
        for watch_descriptor in wd_to_path:
            inotify.rm_watch(watch_descriptor)


def handle_workflow_file_modify_event(path, proj, logger):
    """Handle file modification events by checking workflows and invoking tasks.

    Args:
        path (str): The path of the modified file triggering the event.
        proj (dict): Project configuration settings specifying workflows and tasks.
        logger (Logger): A logger object for logging messages.
    """
    workflows_that_watch = get_workflows_that_watch(proj, logger)
    logger.debug(f"get_workflows_that_watch: workflows_that_watch: {workflows_that_watch}")
    for workflow in workflows_that_watch:
        proj["current-workflow"] = workflow
        logger.debug(f"workflow: {workflow}")
        for task in workflow["tasks"]:
            proj["current-task"] = task
            task["path-modify-event"] = path
            path_match = file_path_match(proj, logger)
            if "content_patterns" in workflow:
                content_match = file_content_match(proj, logger)
            else:
                logger.debug('Workflow has no "content_patterns", so "content_match" is True')
                content_match = True
            if not path_match or not content_match:
                logger.debug(f"No path or content match on {path}")
                continue
            logger.info(f"Path and content match on {path}")
            if task["type"] in task_type_functions:
                logger.info(f"Workflow: {workflow['name']}, Task: {task['id']} → {path}")
                if not ignore_rapid_modify_event(path, proj, logger):
                    task_type_functions[task["type"]](proj, logger)
            else:
                raise ValueError(f'Unsupported task_type: {task["type"]}')


def ignore_rapid_modify_event(path, proj, logger):
    """Determine whether to ignore a rapid succession of modify events.

    Args:
        path (str): The path of the file associated with the event.
        proj (dict): Project configuration settings including workflow and task info.
        logger (Logger): A logger object for logging messages.

    Returns:
        bool: True if the event is ignored, False otherwise.
    """
    current_time = time.time()
    workflow = proj["current-workflow"]
    task = proj["current-task"]
    key = (path, workflow["name"], task["id"])
    last_time = last_modification_times.get(key, 0)

    modify_event_limit = 3
    if "modify_event_limit" in task:
        modify_event_limit = task["modify_event_limit"]

    if current_time - last_time < modify_event_limit:
        logger.info(f"  Ignoring rapid MODIFY event for (modify_event_limit: {modify_event_limit}).")
        return True
    last_modification_times[key] = current_time
    logger.debug(f"  NOT ignoring rapid MODIFY event for (modify_event_limit: {modify_event_limit}).")
    return False
