import os
from unittest.mock import patch
import tempfile
from coauthor.modules.file_scanner import scan
import logging
from coauthor.utils.logger import Logger
from coauthor.utils.config import get_config


def get_content():
    return f"""
---
categories: [Whatever]
tags: [Whatever, Whatever, Whatever]
title: Whatever
linkTitle: Whatever
translate: true
weight: 2
description: >
  Whatever
---
Whatever
"""


def get_content_nl():
    return f"""
---
categories: [Wat-dan-ook]
tags: [Wat-dan-ook, Wat-dan-ook, Wat-dan-ook]
title: Wat-dan-ook
linkTitle: Wat-dan-ook
weight: 2
description: >
  Wat-dan-ook
---
Wat-dan-ook
"""


def test_process_file_with_openai_agent_translation():
    """
    This test verifies that the translation task can support translations
    using AI, utilizing the 'path_new_replace' attribute to write AI
    content responses to a different file. The functionality is particularly
    suitable for Hugo-based websites, which store translations in distinct
    folders for each language, such as 'en' for English and 'nl' for Dutch.
    """
    path = os.path.join(os.path.dirname(__file__), "data", "coauthor_translation.yml")
    config = get_config(path=path)
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
    with tempfile.TemporaryDirectory() as temp_dir:
        path_content = os.path.join(temp_dir, "content")
        path = os.path.join(path_content, "en", "whatever", "whatever.md")
        path_nl = os.path.join(path_content, "nl", "whatever", "whatever.md")
        config["workflows"][0]["scan"] = {"filesystem": {"paths": [path_content]}}
        os.makedirs(os.path.dirname(path))
        with open(path, "w") as f:
            f.write(get_content())
        with patch("coauthor.modules.ai.create_chat_completion", return_value=get_content_nl()):
            scan(config, logger)
            task1 = config["workflows"][0]["tasks"][0]
            task2 = config["workflows"][0]["tasks"][1]
            assert task1["id"] == "ai-translate"
            assert task1["response"] == get_content_nl()
            assert task2["id"] == "write-file"

            # Assert that the translated file exists
            assert os.path.exists(path_nl)
            # Assert that the content of the translated file matches expected content
            with open(path_nl, "r") as f:
                content_nl = f.read()
            assert content_nl == get_content_nl()
