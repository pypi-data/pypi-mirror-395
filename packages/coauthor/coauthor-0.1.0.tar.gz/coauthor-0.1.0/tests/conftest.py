#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""
This is a configuration file for pytest containing customizations and fixtures.

In VSCode, Code Coverage is recorded in config.xml. Delete this file to reset reporting.
"""

from __future__ import annotations

from typing import List

import pytest
from _pytest.nodes import Item
import os
import time

pytest_plugins = ["helpers_namespace"]


def pytest_collection_modifyitems(items: list[Item]):
    for item in items:
        if "spark" in item.nodeid:
            item.add_marker(pytest.mark.spark)
        elif "_int_" in item.nodeid:
            item.add_marker(pytest.mark.integration)


@pytest.fixture
def unit_test_mocks(monkeypatch: None):
    """Include Mocks here to execute all commands offline and fast."""
    pass


# @pytest.fixture
# def load_test_data():
#     data_file = os.path.join(os.path.dirname(__file__), 'data', 'test_data.json')
#     with open(data_file, 'r') as f:
#         return json.load(f)


@pytest.helpers.register
def wait_file_content(file_path: str, expected_content: str, retries: int = 5, delay: int = 1):
    """
    Wait for a file's content to match the expected content.

    Args:
        file_path (str): Path to the file whose content needs to be checked.
        expected_content (str): The content that we expect the file to have.
        retries (int): Number of retries before giving up. Defaults to 5.
        delay (int): Delay in seconds between each retry. Defaults to 1 second.

    Returns:
        str: The actual content of the file after all retries.
    """
    actual_content = ""
    for _ in range(retries):
        with open(file_path, "r") as file:
            actual_content = file.read()
            if actual_content == expected_content:
                return actual_content
        time.sleep(delay)
    return actual_content
