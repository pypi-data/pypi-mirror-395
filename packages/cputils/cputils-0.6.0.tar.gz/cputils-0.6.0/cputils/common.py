import os


def ensure_dir_exists(path):
    """
    Ensure a directory exists, creating it if needed.
    Args:
        path (str): The path to the directory.
    """
    if path:  # Empty dir (cwd) always exists
        try:
            # Will fail either if exists or unable to create it
            os.makedirs(path)
        except OSError:
            # Also raised if the path exists
            pass

        if not os.path.exists(path):
            # There was an error on creation, so make sure we know about it
            raise OSError("Unable to create directory " + path)
