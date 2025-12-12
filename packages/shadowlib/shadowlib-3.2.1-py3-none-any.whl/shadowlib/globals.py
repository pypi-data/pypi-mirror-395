"""
Global access to Client singleton.

Deprecated: Prefer importing directly from shadowlib.client

    from shadowlib.client import client

This module is kept for backwards compatibility.
"""


def getClient():
    """
    Get the singleton Client instance.

    Deprecated: Use `from shadowlib.client import client` instead.

    Returns:
        Client: The singleton client instance
    """
    from shadowlib.client import client

    return client


def getApi():
    """
    Get the singleton RuneLiteAPI instance.

    Returns:
        RuneLiteAPI: The singleton API instance
    """
    from shadowlib._internal.api import RuneLiteAPI

    return RuneLiteAPI()


# Convenience exports
__all__ = [
    "getApi",
    "getClient",
]
