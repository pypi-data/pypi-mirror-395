"""
Magic tab module.
"""

from shadowlib.types.gametab import GameTab, GameTabs


class Magic(GameTabs):
    """
    Singleton magic tab - displays spellbook and available spells.

    Example:
        from shadowlib.tabs.magic import magic

        magic.open()
    """

    TAB_TYPE = GameTab.MAGIC

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
magic = Magic()
