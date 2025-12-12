"""Text manipulation utilities for RuneScape text."""

import re


def stripColorTags(text: str) -> str:
    """
    Remove RuneScape color and image tags from text.

    Tags include:
    - Color tags: <col=RRGGBB> and </col>
    - Image tags: <img=NUMBER>
    - Any other tags in angle brackets

    Args:
        text: Text with potential tags

    Returns:
        Text with all tags removed

    Example:
        >>> stripColorTags("Follow <col=ffffff>Player</col>  (level-99)")
        "Follow Player  (level-99)"
        >>> stripColorTags("<img=54> Drop Logs")
        " Drop Logs"
        >>> stripColorTags("Cast Confuse</col>")
        "Cast Confuse"
    """
    # Remove all tags in angle brackets (opening and closing)
    text = re.sub(r"<[^>]+>", "", text)
    return text
