def join_with_spaces_and_truncate(text, max_length=100):
    """
    Joins multiline content into a single line using spaces, truncating to the specified max length.

    :param text: The input string with possible newlines.
    :param max_length: The maximum length of the output string (default 100).
    :return: The joined and truncated string.
    """
    lines = text.split("\n")
    joined = " ".join(line.strip() for line in lines if line.strip())
    return joined[:max_length]
