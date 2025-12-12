"""
Progress tab module (Quest/Achievement Diaries).
"""

from shadowlib.types.gametab import GameTab, GameTabs


class Progress(GameTabs):
    """
    Singleton progress tab - displays quests and achievement diaries.

    Example:
        from shadowlib.tabs.progress import progress

        progress.open()
    """

    TAB_TYPE = GameTab.PROGRESS

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
progress = Progress()
