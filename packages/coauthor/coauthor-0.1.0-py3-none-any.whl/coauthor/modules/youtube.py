import googleapiclient.discovery
import yaml
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import PrettyPrintFormatter
from coauthor.utils.match_utils import regex_content_match_named_group
import os


def get_youtube_video_info(config, logger):
    """
    Retrieves and updates the task configuration with the YouTube video's
    transcript information.

    :param config: Configuration object containing task details
    :param logger: Logger for logging information
    :return: None
    """
    workflow = config["current-workflow"]
    task = config["current-task"]
    video_id = regex_content_match_named_group(workflow, "video_id", logger)
    task["video"] = {}
    task["video"]["id"] = video_id
    logger.debug(f"video_id: {video_id}")
    task["video"]["transcript"] = get_youtube_transcript(config, video_id, logger)
    task["video"]["info"] = get_youtube_metadata(config, video_id, logger)


def get_youtube_transcript(config, video_id, logger):
    """
    Retrieves the transcript of a YouTube video based on the video ID. If a
    transcript file already exists, it uses the contents of this file instead of
    calling the YouTube API.

    :param config: Configuration object containing task details
    :param video_id: The YouTube video ID
    :param logger: Optional logger for logging information
    :return: The transcript of the video as a YAML object
    """
    task = config["current-task"]
    path = task["path-modify-event"]
    path_transcript = path.rsplit(".", 1)[0] + ".transcript.yml"

    if not os.path.exists(path_transcript):
        logger.info(f'Fetching transcript for video ID: "{video_id}"')
        ytt_api = YouTubeTranscriptApi()
        languages = task.get("languages", ["en"])

        try:
            logger.debug(f"Fetching transcript for video {video_id} in languages: {languages}")
            transcript = ytt_api.fetch(video_id, languages=languages)
            formatter = PrettyPrintFormatter()

            text_formatted = formatter.format_transcript(transcript)

            # Now we can write it out to a file.
            with open(path_transcript, "w", encoding="utf-8") as yaml_file:
                yaml.dump(yaml.safe_load(text_formatted), yaml_file)

            logger.info(f"Transcript successfully retrieved for video {video_id} and written to {path_transcript}")

        except Exception as exception_error:  # pylint: disable=broad-exception-caught
            logger.error(f"Error retrieving transcript for video {video_id}: {exception_error}")
            return None

    logger.info(f"Reading video {video_id} transcript file {path_transcript}")
    with open(path_transcript, "r", encoding="utf-8") as transcript_file:
        return yaml.safe_load(transcript_file)


def get_youtube_metadata(config, video_id, logger):
    """
    Retrieves metadata for a YouTube video based on its video ID and updates the task configuration.
    If a metadata file already exists, it uses the contents of this file instead of calling the YouTube API.

    :param config: Configuration object containing task details
    :param video_id: The YouTube video ID
    :param logger: Logger for logging information
    :return: Dictionary containing video metadata
    """
    task = config["current-task"]
    path = task["path-modify-event"]
    path_info = path.rsplit(".", 1)[0] + ".info.yml"

    if not os.path.exists(path_info):
        logger.info(f'Fetching metadata for video ID: "{video_id}"')

        api_key = os.getenv("COAUTHOR_YOUTUBE_API_KEY")
        if not api_key:
            logger.error("COAUTHOR_YOUTUBE_API_KEY environment variable not set. No video info will be available.")
            return {}

        api_service_name = "youtube"
        api_version = "v3"

        youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

        request = youtube.videos().list(
            part="contentDetails,id,liveStreamingDetails,player,recordingDetails,snippet,statistics,status,topicDetails",
            id=video_id,
        )

        response = request.execute()

        with open(path_info, "w", encoding="utf-8") as info_file:
            yaml.dump(response["items"][0], info_file)

        logger.info(f"Metadata for video {video_id} successfully retrieved and written to {path_info}")

    logger.info(f"Reading metadata for video {video_id} from file {path_info}")
    with open(path_info, "r", encoding="utf-8") as info_file:
        return yaml.safe_load(info_file) or {}
