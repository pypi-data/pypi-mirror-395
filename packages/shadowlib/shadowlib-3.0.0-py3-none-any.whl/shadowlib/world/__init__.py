"""Game viewport entities - NPCs, objects, players, items visible in 3D world."""

from shadowlib.world.ground_items import GroundItems, groundItems


class World:
    """
    Namespace for 3D world entities - returns singleton instances.

    Example:
        from shadowlib.client import client

        items = client.world.groundItems.getAllItems()
        # Or directly:
        from shadowlib.world.ground_items import groundItems
        items = groundItems.getAllItems()
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def groundItems(self) -> GroundItems:
        """Get ground items accessor singleton."""
        return groundItems


# Module-level singleton instance
world = World()


__all__ = ["World", "world", "GroundItems", "groundItems"]
