import os


def get_recently_modified_file(file_path_inotify, dir_path, logger):
    """
    Retrieves the most recently modified file in a specified directory,
    excluding hidden files. This function is primarily used to address
    an issue with gedit, where the editor uses a temporary hidden file
    that complicates direct file modification detection.

    Args:
        file_path_inotify (str): The file path detected by inotify or similar mechanism.
        dir_path (str): The directory path to search for modified files.
        logger (Logger): A logger instance for logging debug information.

    Returns:
        str: The path to the most recently modified file in the specified directory.
             Returns None if no suitable files are found in the directory.

    Notes:
        - If `file_path_inotify` is found in the directory's non-hidden files,
          it will be returned immediately.
        - For gedit and potentially other applications that use hidden temporary
          files upon saving, this method helps identify the correct file by
          checking the last modified time.
    """
    all_files = list(
        set(
            os.path.join(dir_path, f)
            for f in os.listdir(dir_path)
            if os.path.isfile(os.path.join(dir_path, f)) and not f.startswith(".")
        )
    )
    logger.debug(f"all_files: {', '.join(all_files)}")
    if file_path_inotify in all_files:
        return file_path_inotify
    return max(all_files, key=os.path.getmtime) if all_files else None
