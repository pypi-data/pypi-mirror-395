"""
Friends tab module.
"""

from shadowlib.types.gametab import GameTab, GameTabs


class Friends(GameTabs):
    """
    Singleton friends tab - displays friends list and ignore list.

    Example:
        from shadowlib.tabs.friends import friends

        friends.open()
    """

    TAB_TYPE = GameTab.FRIENDS

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
friends = Friends()
