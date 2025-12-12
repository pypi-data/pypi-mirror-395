import os
import yaml
import re


class TaskNotFoundError(Exception):
    """Exception raised when a task with the specified ID is not found."""

    def __init__(self, task_id):
        self.task_id = task_id
        super().__init__(f"Task with ID {self.task_id} not found.")


class AttributeNotFoundError(Exception):
    """Exception raised when a specified attribute is not found in a task."""

    def __init__(self, attribute):
        self.attribute = attribute
        super().__init__(f"Attribute '{self.attribute}' not found in task.")


def select_task(config, task_id):
    """
    Select and return a task from a list of tasks based on its id.

    :param config: a dictionary containing the configuration with a list of tasks
    :param task_id: the id of the task to find
    :return: The task dictionary with the matching id
    :raises TaskNotFoundError: If no task with the given id is found
    """
    workflow = config["current-workflow"]
    for task in workflow["tasks"]:
        if task.get("id") == task_id:
            return task
    raise TaskNotFoundError(task_id)


def get_task_attribute(config, id, attribute):
    """
    Get a specific attribute from a task identified by id.

    :param config: a dictionary containing the configuration with a list of tasks
    :param id: the id of the task from which to get the attribute
    :param attribute: the attribute to retrieve from the task
    :return: The value of the specified attribute in the task
    :raises TaskNotFoundError: If no task with the given id is found
    :raises AttributeNotFoundError: If the attribute does not exist in the task
    """
    task = select_task(config, id)
    if attribute in task:
        return task[attribute]
    else:
        raise AttributeNotFoundError(attribute)


def basename(path):
    """
    Retrieve the base name of the given file path.

    :param path: The file path from which to retrieve the base name
    :return: The base name of the file path
    """
    return os.path.basename(path)


def dirname(path):
    """
    Retrieve the directory name of the given file path.

    :param path: The file path from which to retrieve the directory name
    :return: The directory name of the file path
    """
    return os.path.dirname(path)


def extname(path):
    """
    Retrieve the file extension from the given file path.

    :param path: The file path from which to retrieve the file extension
    :return: The file extension of the path.
             If no extension, returns an empty string.
    """
    _, file_extension = os.path.splitext(path)
    return file_extension.strip().replace(".", "")


def to_nice_yaml(data):
    return yaml.dump(data, sort_keys=False)


def list_files(relative_dir):
    """
    Return a list of file paths in the specified directory relative to the working directory.

    :param relative_dir: The relative path of the directory
    :return: A list of strings representing the file paths
    """
    files = []
    for item in os.listdir(relative_dir):
        full_path = os.path.join(relative_dir, item)
        if os.path.isfile(full_path):
            files.append(full_path)
    return files


def read_file(filename, remove_frontmatter=False):
    with open(filename, "r", encoding="utf-8") as f:
        contents = f.read()
        if remove_frontmatter:
            contents = re.sub(r"^---.*?---\s*", "", contents, flags=re.DOTALL)
        return contents


def find_up(start_path, filename):
    """
    Find a file by going up the directory tree from the start path.

    :param start_path: The starting directory path
    :param filename: The name of the file to find
    :return: The full path of the file if found, otherwise None
    """
    current = os.path.abspath(start_path)
    while True:
        candidate = os.path.join(current, filename)
        if os.path.exists(candidate):
            return candidate
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent


def find_down(start_path, filename):
    """
    Find a file by going down the directory tree from the start path.

    :param start_path: The starting directory path
    :param filename: The name of the file to find
    :return: The full path of the file if found, otherwise None
    """
    for root, dirs, files in os.walk(start_path):
        if filename in files:
            return os.path.join(root, filename)
    return None
