"""
OSRS ground item handling using event cache.
"""

from ..types.ground_item import GroundItem
from ..types.ground_item_list import GroundItemList
from ..types.packed_position import PackedPosition


class GroundItems:
    """
    Singleton access to ground items from cache.

    Example:
        from shadowlib.world.ground_items import groundItems

        items = groundItems.getAllItems()
        coins = items.filterByItem(995)        # By ID
        coins = items.filterByItem("Coins")    # By name
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        """Actual initialization, runs once."""
        self._cached_list: GroundItemList = GroundItemList([])
        self._cached_tick: int = -1

    def getAllItems(self) -> GroundItemList:
        """
        Get all ground items from cache.

        Cached per tick (items only change once per tick).

        Returns:
            GroundItemList with all items

        Example:
            >>> from shadowlib.world.ground_items import groundItems
            >>>
            >>> # Get all items
            >>> items = groundItems.getAllItems()
            >>>
            >>> # Filter coins (by ID or name)
            >>> coins = items.filterByItem(995)
            >>> coins = items.filterByItem("Coins")
            >>>
            >>> # Filter nearby items
            >>> nearby = items.filterNearby(player.x, player.y, player.plane, 5)
            >>>
            >>> # Chain filters
            >>> my_nearby_coins = items.filterByItem(995).filterYours().filterNearby(
            ...     player.x, player.y, player.plane, 10
            ... )
            >>>
            >>> # Get closest coin
            >>> nearest_coin = items.filterByItem("Coins").sortByDistance(
            ...     player.x, player.y, player.plane
            ... ).first()
        """
        from shadowlib.client import client

        current_tick = client.cache.tick

        # Return cached if same tick
        if self._cached_tick == current_tick and self._cached_list.count() > 0:
            return self._cached_list

        # Refresh cache
        ground_items_dict = client.cache.getGroundItems()
        result = []

        for packed_coord, items_list in ground_items_dict.items():
            position = PackedPosition.fromPacked(packed_coord)
            for item_data in items_list:
                result.append(GroundItem(data=item_data, position=position, client=client))

        self._cached_list = GroundItemList(result)
        self._cached_tick = current_tick

        return self._cached_list


# Module-level singleton instance
groundItems = GroundItems()
