"""
Settings tab module.
"""

from shadowlib.types.gametab import GameTab, GameTabs


class Settings(GameTabs):
    """
    Singleton settings tab - displays game settings and controls.

    Example:
        from shadowlib.tabs.settings import settings

        settings.open()
    """

    TAB_TYPE = GameTab.SETTINGS

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
settings = Settings()
