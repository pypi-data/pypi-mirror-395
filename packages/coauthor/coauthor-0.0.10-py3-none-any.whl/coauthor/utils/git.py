import subprocess
import os


def get_git_diff(file_path):
    """
    Given the path of a file, this function checks if the file is part of a Git repository.
    If it is, the function returns the diff of the file showing outstanding changes.
    If the file is not in a Git repository, it returns None.

    :param file_path: The path to the file.
    :return: The diff of the file or None if not in a Git repository.
    """

    # Check if the file is part of a git repository
    # try:
    # `git rev-parse --is-inside-work-tree` returns `true` if inside repository
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=os.path.dirname(file_path),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # if result.returncode != 0 or result.stdout.strip() != b"true":
    #     # Not a git repository
    #     return ""

    # Get the diff of the file
    diff_result = subprocess.run(
        ["git", "diff", file_path], cwd=os.path.dirname(file_path), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # if diff_result.returncode != 0:
    #     # Could not get a diff, possibly an error occurred
    #     return ""

    return diff_result.stdout.decode("utf-8")

    # except Exception as e:
    #     # Handle unexpected errors, possibly log this
    #     return ""


# Example usage:
# diff = get_git_diff('/path/to/your/file')
# print(diff)
