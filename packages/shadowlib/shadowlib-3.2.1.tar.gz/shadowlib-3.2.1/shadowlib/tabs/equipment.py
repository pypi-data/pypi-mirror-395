"""
Equipment tab module.
"""

from shadowlib.client import client
from shadowlib.types.gametab import GameTab, GameTabs
from shadowlib.types.itemcontainer import ItemContainer


class Equipment(GameTabs, ItemContainer):
    """
    Singleton equipment tab - displays worn equipment and stats.

    Example:
        from shadowlib.tabs.equipment import equipment

        equipment.open()
    """

    TAB_TYPE = GameTab.EQUIPMENT
    CONTAINER_ID = 94

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        """Actual initialization, runs once."""
        GameTabs.__init__(self)
        self.containerId = self.CONTAINER_ID

    @property
    def items(self):
        """Auto-sync items from cache when accessed."""
        cached = client.cache.getItemContainer(self.CONTAINER_ID)
        self._items = cached.items
        return self._items


# Module-level singleton instance
equipment = Equipment()
