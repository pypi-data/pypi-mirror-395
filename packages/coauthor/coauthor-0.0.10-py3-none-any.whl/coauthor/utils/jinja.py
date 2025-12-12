import jinja2
import os
import importlib.resources
from coauthor.utils.config import get_jinja_config
from coauthor.utils.git import get_git_diff
from coauthor.utils.jinja_filters import (
    select_task,
    get_task_attribute,
    dirname,
    basename,
    extname,
    to_nice_yaml,
    list_files,
    read_file,
    find_up,
    find_down,
)
from coauthor.utils.file import get_url
from coauthor.utils.markdown import get_frontmatter_attribute


def render_template_to_file(task, template, path, config, logger):
    content = render_template(task, template, config, logger)
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)


def search_path_directories(search_path):
    # Return a list of directory search_path and all its subdirectories
    directories = []
    for root, dirs, files in os.walk(search_path):
        directories.append(root)
    return directories


def template_exists(task, template, config, logger):
    args = config.get("args", None)
    profile = getattr(args, "profile", None) if args else None
    if not profile:
        profile = config.get("profile", None)
    jinja_config = get_jinja_config(config)
    base_path = config.get("path", os.getcwd())
    local_search_path = os.path.join(base_path, jinja_config["search_path"])
    search_paths = search_path_directories(local_search_path)
    if profile:
        templates_path = importlib.resources.files("coauthor.profiles") / profile / "templates"
        search_paths.extend(search_path_directories(str(templates_path)))
    template_loader = jinja2.FileSystemLoader(searchpath=search_paths)
    templates = template_loader.list_templates()
    if template in templates:
        return True
    logger.debug(f"Template {template} not found!")
    return False


def render_template(task, template_path, config, logger):
    logger.info(f"Render template {template_path} for task {task['id']}")
    jinja_config = get_jinja_config(config)
    base_path = config.get("path", os.getcwd())
    local_search_path = os.path.join(base_path, jinja_config["search_path"])
    search_paths = search_path_directories(local_search_path)
    args = config.get("args", None)
    profile = getattr(args, "profile", None) if args else None
    if not profile:
        profile = config.get("profile", None)
    if profile:
        logger.info(f'Using Jinja2 templates for profile "{profile}"')
        templates_path = importlib.resources.files("coauthor.profiles") / profile / "templates"
        search_paths.extend(search_path_directories(str(templates_path)))
    template_loader = jinja2.FileSystemLoader(searchpath=search_paths)
    templates = template_loader.list_templates()
    logger.debug(f"templates: {templates}")
    if "custom_delimiters" in jinja_config:
        logger.debug("Creating Jinja environment using custom delimiters")
        custom_delimiters = jinja_config["custom_delimiters"]
        template_env = jinja2.Environment(
            loader=template_loader,
            block_start_string=custom_delimiters.get("block_start_string", "{%"),
            block_end_string=custom_delimiters.get("block_end_string", "%}"),
            variable_start_string=custom_delimiters.get("variable_start_string", "{{"),
            variable_end_string=custom_delimiters.get("variable_end_string", "}}"),
            comment_start_string=custom_delimiters.get("comment_start_string", "{#"),
            comment_end_string=custom_delimiters.get("comment_end_string", "#}"),
        )
    else:
        template_env = jinja2.Environment(loader=template_loader)
    template_env.filters["include_file_content"] = include_file_content
    template_env.filters["get_git_diff"] = get_git_diff
    template_env.filters["file_exists"] = file_exists
    template_env.filters["select_task"] = select_task
    template_env.filters["get_task_attribute"] = get_task_attribute
    template_env.filters["dirname"] = dirname
    template_env.filters["basename"] = basename
    template_env.filters["extname"] = extname
    template_env.filters["to_nice_yaml"] = to_nice_yaml
    template_env.filters["get_frontmatter_attribute"] = get_frontmatter_attribute
    template_env.filters["list_files"] = list_files
    template_env.filters["read_file"] = read_file
    template_env.filters["get_url"] = get_url
    template_env.filters["find_up"] = find_up
    template_env.filters["find_down"] = find_down
    template_env.globals["raise"] = raise_helper

    logger.debug(f"Get Jinja template: {template_path}")
    template = template_env.get_template(template_path)
    context = {"config": config, "task": task, "workflow": config["current-workflow"]}
    return template.render(context)


def render_content(task, template_string, config, logger):
    logger.debug(f"Render content for task {task['id']}")
    jinja_config = get_jinja_config(config)

    if "custom_delimiters" in jinja_config:
        logger.debug("Creating Jinja environment using custom delimiters")
        custom_delimiters = jinja_config["custom_delimiters"]
        template_env = jinja2.Environment(
            block_start_string=custom_delimiters.get("block_start_string", "{%"),
            block_end_string=custom_delimiters.get("block_end_string", "%}"),
            variable_start_string=custom_delimiters.get("variable_start_string", "{{"),
            variable_end_string=custom_delimiters.get("variable_end_string", "}}"),
            comment_start_string=custom_delimiters.get("comment_start_string", "{#"),
            comment_end_string=custom_delimiters.get("comment_end_string", "#}"),
        )
    else:
        template_env = jinja2.Environment()

    template_env.filters["include_file_content"] = include_file_content
    template_env.filters["get_git_diff"] = get_git_diff
    template_env.filters["file_exists"] = file_exists
    template_env.filters["select_task"] = select_task
    template_env.filters["get_task_attribute"] = get_task_attribute
    template_env.filters["dirname"] = dirname
    template_env.filters["basename"] = basename
    template_env.filters["extname"] = extname
    template_env.filters["get_frontmatter_attribute"] = get_frontmatter_attribute
    template_env.filters["list_files"] = list_files
    template_env.filters["read_file"] = read_file
    template_env.filters["get_url"] = get_url
    template_env.filters["find_up"] = find_up
    template_env.filters["find_down"] = find_down
    template_env.globals["raise"] = raise_helper

    template = template_env.from_string(template_string)
    context = {"config": config, "task": task, "workflow": config["current-workflow"]}
    return template.render(context)


def include_file_content(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def file_exists(path):
    return os.path.exists(path)


def prompt_template_paths(config, filename):
    task = config["current-task"]
    workflow = config["current-workflow"]
    return [f"{workflow['name']}/{task['id']}/{filename}", f"{workflow['name']}/{filename}", f"{filename}"]


def prompt_template_path(config, filename, logger):
    """Returns the most specific path for a template that exists."""

    task = config["current-task"]

    # Check each path in order of specificity and return the first existing one
    paths = prompt_template_paths(config, filename)
    logger.debug(f"Looking for templates: {', '.join(paths)}")

    for path in paths:
        if template_exists(task, path, config, logger):
            return path

    # Return the most specific path if none exist
    return paths[0]


# def user_template_path(config, filename="user.md"):
#     return prompt_template_path(config, filename)


# def system_template_path(config, filename="system.md"):
#     return prompt_template_path(config, filename)


def raise_helper(msg):
    raise RuntimeError(msg)
