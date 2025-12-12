"""
Music tab module.
"""

from shadowlib.types.gametab import GameTab, GameTabs


class Music(GameTabs):
    """
    Singleton music tab - displays music tracks and player.

    Example:
        from shadowlib.tabs.music import music

        music.open()
    """

    TAB_TYPE = GameTab.MUSIC

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
music = Music()
