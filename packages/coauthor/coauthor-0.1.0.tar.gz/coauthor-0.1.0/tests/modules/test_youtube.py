import tempfile
import logging
import pytest
import yaml
from unittest import mock
from coauthor.utils.logger import Logger
import os
from coauthor.modules.youtube import get_youtube_transcript, get_youtube_video_info
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from coauthor.utils.match_utils import regex_content_match, regex_content_match_named_group


def test_youtube_transcript_retrieval():
    """
    Pytest test for get_youtube_transcript function.
    Tests retrieval of a transcript for provided YouTube video ID.
    """
    video_id = "ggyMIg8uXsw"
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")

    with tempfile.TemporaryDirectory() as temp_dir:
        config = {"current-task": {"path-modify-event": f"{temp_dir}/video.transcript"}}

        result_transcript = get_youtube_transcript(config, video_id, logger)
        logger.debug(f"result_transcript: {result_transcript}")

        expected_transcript_path = config["current-task"]["path-modify-event"] + ".txt"

        assert result_transcript is not None, "Expected non-None transcript."
        assert "President Trump's 90-day" in result_transcript, "Expected text not found in the transcript."

        assert os.path.exists(expected_transcript_path), "Transcript file does not exist."
        assert os.path.getsize(expected_transcript_path) > 0, "Transcript file is empty."


def test_get_youtube_video_info():
    content = "whatever\nwhatever\nyoutube_id: ggyMIg8uXsw\n\nwhatever\n@whatever: something\n\n"
    logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")

    with tempfile.TemporaryDirectory() as temp_dir:

        workflow = {}
        workflow["content_patterns"] = [[".*@whatever:.*", ".*youtube_id:\s*(?P<video_id>\S+).*"]]
        config = {"current-task": {"path-modify-event": f"{temp_dir}/video.transcript"}}
        config["current-workflow"] = workflow
        result = regex_content_match(content, workflow, "content_patterns", "content_matches", logger)

        assert result is True, "Expected result to be True."
        assert "content_matches" in workflow, "Expected 'content_matches' key in workflow."
        logger.debug(f"content_matches: {workflow['content_matches']}")
        assert len(workflow["content_matches"]) == 2, "Expected two items in 'content_matches'."

        for match in workflow["content_matches"]:
            logger.debug(f"match: {match}")

        get_youtube_video_info(config, logger)

        assert (
            "video" in config["current-task"] and config["current-task"]["video"]["id"] == "ggyMIg8uXsw"
        ), "Expected video id to be 'ggyMIg8uXsw'."
        assert "transcript" in config["current-task"]["video"], "Expected transcript"

        transcript_yml = config["current-task"]["video"]["transcript"]
        transcript_txt = yaml.dump(transcript_yml, default_flow_style=False)
        logger.debug(f"transcript_txt: {transcript_txt}")
        assert "President Trump's 90-day" in transcript_txt, "Expected 90-day"

        get_youtube_video_info(config, logger)

        logger.debug(f"info: {config['current-task']['video']['info']}")
        assert "info" in config["current-task"]["video"], "Expected info"
        assert "snippet" in config["current-task"]["video"]["info"], "Expected snippet"
        assert "title" in config["current-task"]["video"]["info"]["snippet"], "Expected snippet"
        assert (
            "The EU just FOUND OUT." in config["current-task"]["video"]["info"]["snippet"]["title"]
        ), "Expected The EU just FOUND OUT."
