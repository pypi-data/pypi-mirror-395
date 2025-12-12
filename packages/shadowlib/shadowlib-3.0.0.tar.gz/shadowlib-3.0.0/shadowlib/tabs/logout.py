"""
Logout tab module.
"""

from shadowlib.types.gametab import GameTab, GameTabs


class Logout(GameTabs):
    """
    Singleton logout tab - displays logout options and world switcher.

    Example:
        from shadowlib.tabs.logout import logout

        logout.open()
    """

    TAB_TYPE = GameTab.LOGOUT

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
logout = Logout()
