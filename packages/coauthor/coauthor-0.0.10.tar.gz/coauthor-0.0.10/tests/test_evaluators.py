import logging
import os
import argparse

import yaml
import time
import tempfile
from coauthor.utils.config import get_config, get_config_path, read_config
from coauthor.utils.logger import Logger
from coauthor.utils.evaluators import compare_semantic_similarity


def test_compare_semantic_similarity():
    inputs = {"question": "Is LangSmith natively integrated with LangChain?"}
    reference_outputs = {"output": "Yes, LangSmith is natively integrated with LangChain, as well as LangGraph."}
    outputs = {"output": "No, LangSmith is NOT integrated with LangChain."}

    similarity_score = compare_semantic_similarity(inputs, reference_outputs, outputs)
    assert similarity_score["score"] <= 2

    outputs = {"output": "Yes, LangSmith is natively integrated with LangChain"}
    similarity_score = compare_semantic_similarity(inputs, reference_outputs, outputs)
    assert similarity_score["score"] >= 9
