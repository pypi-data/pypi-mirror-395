"""
Grouping tab module (Clan/Group activities).
"""

from shadowlib.types.gametab import GameTab, GameTabs


class Grouping(GameTabs):
    """
    Singleton grouping tab - displays clan chat and group activities.

    Example:
        from shadowlib.tabs.grouping import grouping

        grouping.open()
    """

    TAB_TYPE = GameTab.GROUPING

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
grouping = Grouping()
