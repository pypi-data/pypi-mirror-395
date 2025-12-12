"""
Prayer tab module.
"""

from shadowlib.types.gametab import GameTab, GameTabs


class Prayer(GameTabs):
    """
    Singleton prayer tab - displays available prayers and prayer points.

    Example:
        from shadowlib.tabs.prayer import prayer

        prayer.open()
    """

    TAB_TYPE = GameTab.PRAYER

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
prayer = Prayer()
