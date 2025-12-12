import subprocess
import os
import tempfile
import pytest
from coauthor.utils.git import get_git_diff


@pytest.fixture
def setup_git_repo():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Initialize a new git repository
        subprocess.run(["git", "init"], cwd=temp_dir)

        # Create a new file in this directory
        file_path = os.path.join(temp_dir, "test_file.txt")
        with open(file_path, "w") as f:
            f.write("Initial content\n")

        # Add and commit the new file
        subprocess.run(["git", "add", "test_file.txt"], cwd=temp_dir)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=temp_dir)

        yield temp_dir, file_path


def test_get_git_diff(setup_git_repo):
    temp_dir, file_path = setup_git_repo

    # Modify the file to create a change
    with open(file_path, "a") as f:
        f.write("Added content\n")

    # Get the diff
    diff = get_git_diff(file_path)

    # Verify that the diff is not None
    assert diff is not None
    # Verify that the diff contains the expected change
    assert "Added content" in diff
    assert "Initial content" in diff
