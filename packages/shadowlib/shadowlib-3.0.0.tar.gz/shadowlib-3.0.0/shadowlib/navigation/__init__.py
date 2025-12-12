"""Navigation module."""

from shadowlib.navigation.pathfinder import Pathfinder, pathfinder


class Navigation:
    """
    Namespace for navigation systems - returns singleton instances.

    Example:
        from shadowlib.client import client

        path = client.navigation.pathfinder.getPath(3200, 3200, 0)
        # Or directly:
        from shadowlib.navigation.pathfinder import pathfinder
        path = pathfinder.getPath(3200, 3200, 0)
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def pathfinder(self) -> Pathfinder:
        """Get pathfinder singleton."""
        return pathfinder


# Module-level singleton instance
navigation = Navigation()


__all__ = ["Navigation", "navigation", "Pathfinder", "pathfinder"]
