"""
Equipment tab module.
"""

from shadowlib.types.gametab import GameTab, GameTabs


class Equipment(GameTabs):
    """
    Singleton equipment tab - displays worn equipment and stats.

    Example:
        from shadowlib.tabs.equipment import equipment

        equipment.open()
    """

    TAB_TYPE = GameTab.EQUIPMENT

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        """Actual initialization, runs once."""
        GameTabs.__init__(self)


# Module-level singleton instance
equipment = Equipment()
