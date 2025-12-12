"""Contains all generic build utils."""

import re
import urllib.parse


def sanitize_branch_name(branch_name: str) -> str:
    """Sanitizes the given branch name by url-decoding it and replacing invalid characters with dashes.

    Args:
        branch_name: The input branch name.

    Returns:
        The sanitized branch name.
    """
    decoded_name = urllib.parse.unquote(branch_name, encoding="utf-8")
    sanitized_name = re.sub(r"[^a-zA-Z0-9-_\.]", "-", decoded_name)
    return sanitized_name
