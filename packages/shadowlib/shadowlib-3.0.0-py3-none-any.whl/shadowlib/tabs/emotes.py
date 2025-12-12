"""
Emotes tab module.
"""

from shadowlib.types.gametab import GameTab, GameTabs


class Emotes(GameTabs):
    """
    Singleton emotes tab - displays available emotes.

    Example:
        from shadowlib.tabs.emotes import emotes

        emotes.open()
    """

    TAB_TYPE = GameTab.EMOTES

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
emotes = Emotes()
