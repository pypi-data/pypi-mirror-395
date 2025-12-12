"""
Combat tab module.
"""

from shadowlib.types.gametab import GameTab, GameTabs


class Combat(GameTabs):
    """
    Singleton combat tab - displays combat stats and special attack.

    Example:
        from shadowlib.tabs.combat import combat

        combat.open()
    """

    TAB_TYPE = GameTab.COMBAT

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
combat = Combat()
