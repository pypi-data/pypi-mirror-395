import yaml


def parse_frontmatter(content):
    """
    Parse frontmatter from markdown content without using frontmatter library
    because it depends on older pyyaml==5.3.1.

    Returns a dictionary with 'data' (parsed frontmatter) and 'content'.
    """
    if "---" not in content:
        return {"frontmatter": {}, "content": content}

    frontmatter_end = content.find("---", 3)
    if frontmatter_end == -1:
        frontmatter_end = 3

    frontmatter_str = content[3:frontmatter_end].strip()
    frontmatter_data = yaml.safe_load(frontmatter_str)

    if frontmatter_end + 1 < len(content):
        content_str = content[frontmatter_end + 1 :].lstrip()
    else:
        content_str = ""

    return {"frontmatter": frontmatter_data, "content": content_str, "frontmatter_str": frontmatter_str}


def get_frontmatter(path):
    """
    Reads a Markdown file and parses its frontmatter.

    :param path: Path to the Markdown file.
    :return: Tuple containing the frontmatter dictionary, frontmatter string, and original content.
    """
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    parsed = parse_frontmatter(content)
    frontmatter = parsed["frontmatter"]
    frontmatter_str = parsed["frontmatter_str"]
    return frontmatter, frontmatter_str, content


def get_frontmatter_attribute(path, attr_name):
    """
    Retrieves a specific attribute from the frontmatter of a Markdown file.

    :param path: Path to the Markdown file.
    :param attr_name: The name of the attribute to retrieve.
    :return: The value of the specified attribute, or None if not found.
    """
    frontmatter, _, _ = get_frontmatter(path)
    return (frontmatter or {}).get(attr_name)


def get_frontmatter_nested_value(path, frontmatter_context_path):
    """
    Retrieves a nested value from the frontmatter of a Markdown file using a path.

    :param path: Path to the Markdown file.
    :param frontmatter_context_path: The nested path to the attribute (e.g., "key1/key2").
    :return: The value as a list if it is a list, otherwise an empty list.
    """
    frontmatter, _, _ = get_frontmatter(path)
    keys = frontmatter_context_path.replace("/", ".").split(".")
    value = frontmatter
    for key in keys:
        value = value.get(key, {})
    return value if isinstance(value, list) else []
