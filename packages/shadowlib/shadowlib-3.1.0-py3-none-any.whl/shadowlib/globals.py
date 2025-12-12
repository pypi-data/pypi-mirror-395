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
    Get the API instance from the singleton Client.

    Deprecated: Use `from shadowlib.client import client; client.api` instead.

    Returns:
        RuneLiteAPI: The API instance
    """
    from shadowlib.client import client

    return client.api


# Convenience exports
__all__ = [
    "getApi",
    "getClient",
]
