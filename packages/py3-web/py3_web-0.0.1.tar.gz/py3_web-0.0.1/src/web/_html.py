import html
from typing import Any

from htmlmin import minify


def compress(*args: Any, **kwargs: Any) -> str:
    return minify(*args, **kwargs)


def escape(text: str) -> str:
    """
    >>> escape("<")
    '&lt;'

    Args:
        text:

    Returns:

    """
    return html.escape(text)


def unescape(text: str) -> str:
    """
    >>> unescape("&lt;")
    '<'

    Args:
        text:

    Returns:

    """
    return html.unescape(text)
