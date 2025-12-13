import re


def sanitize_usd_path(path: str) -> str:
    """
    Sanitize a path string to be a valid USD path.

    :param path: The path string to sanitize.
    :return: The sanitized USD path.
    """

    return re.sub(r"[^a-zA-Z0-9_/]", "_", path)
