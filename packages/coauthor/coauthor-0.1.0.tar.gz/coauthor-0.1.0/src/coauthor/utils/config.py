import yaml
import os
import importlib.resources
import copy


def deep_merge(d1, d2):
    for key, value in d2.items():
        if key in d1 and isinstance(d1[key], dict) and isinstance(value, dict):
            deep_merge(d1[key], value)
        else:
            d1[key] = value
    return d1


def read_config(file_path, logger=None):
    if logger:
        logger.info(f"Reading configuration from {file_path}")
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def get_config_path(config_filename=".coauthor.yml", search_dir=os.getcwd()):
    traversed_paths = []
    while True:
        potential_path = os.path.join(search_dir, config_filename)
        if os.path.exists(potential_path):
            return potential_path, traversed_paths
        traversed_paths.append(search_dir)
        parent_dir = os.path.dirname(search_dir)
        if parent_dir == search_dir:
            break
        search_dir = parent_dir

    home_dir = os.path.expanduser("~")
    home_path = os.path.join(home_dir, config_filename)
    if os.path.exists(home_path):
        traversed_paths.append(home_dir)
        return home_path, traversed_paths

    return None, traversed_paths


def get_default_config():
    config = {
        "jinja": {"search_path": ".coauthor/templates"},
        "agent": {
            "api_key_var": "OPENAI_API_KEY",
            "api_url_var": "OPENAI_API_URL",
            "model": "x-ai/grok-4",
        },
        "file-watcher": {"ignore-folders": ["__pycache__", ".obsidian", ".git"]},
    }
    return config


def get_projects(config):
    projects = config.get("projects", [])
    projects += [config]
    return projects


def expand_paths(conf):
    if "path" in conf:
        conf["path"] = os.path.expanduser(conf["path"])
    if "projects" in conf:
        for proj in conf["projects"]:
            expand_paths(proj)


def save_config_dump(config, logger=None):
    dump_path = os.path.join(os.getcwd(), ".coauthor_dump.yml")
    with open(dump_path, "w", encoding="utf-8") as dump_file:
        yaml.safe_dump(config, dump_file, default_flow_style=False)
        if logger:
            logger.info(f"Dumped configuration to {dump_path}")


def get_config(path=None, logger=None, config_filename=".coauthor.yml", search_dir=os.getcwd(), args=None):
    config = {}
    config_path = None
    if args and hasattr(args, "config_path") and args.config_path:
        config_path = args.config_path
    elif args and hasattr(args, "profile") and args.profile:
        profile = args.profile
        profile_path = importlib.resources.files("coauthor.profiles").joinpath(profile).joinpath("config.yml")
        config = get_default_config()
        deep_merge(config, read_config(profile_path, logger))
        expand_paths(config)
        return config
    if not config_path:
        if path:
            config_path = path
        else:
            config_path, searched_paths = get_config_path(config_filename, search_dir)
            if not config_path:
                if logger:
                    logger.warning(f"Configuration file not found. Searched directories: {', '.join(searched_paths)}")
                config_path = os.path.join(os.getcwd(), config_filename)
                config = get_default_config()
                with open(config_path, "w", encoding="utf-8") as file:
                    if logger:
                        logger.debug(f"Dump config to YAML file {config_path}")
                    yaml.safe_dump(config, file)

                if logger:
                    logger.info(f"Created default configuration file at {config_path}")
    config = get_default_config()
    deep_merge(config, read_config(config_path, logger))
    expand_paths(config)
    if "projects" in config:
        for proj in config["projects"]:
            if "profile" in proj:
                profile = proj["profile"]
                profile_path = importlib.resources.files("coauthor.profiles").joinpath(profile).joinpath("config.yml")
                profile_config = read_config(profile_path, logger)
                local = copy.deepcopy(proj)
                proj.clear()
                default = get_default_config()
                deep_merge(proj, default)
                deep_merge(proj, profile_config)
                deep_merge(proj, local)
        expand_paths(config)
        all_projects = get_projects(config)
        for proj in config["projects"]:
            proj["all_projects"] = all_projects
    return config


def get_jinja_config(config):
    if "jinja" in config:
        return config["jinja"]
    config_jinja = {"search_path": ".coauthor/templates"}
    return config_jinja
