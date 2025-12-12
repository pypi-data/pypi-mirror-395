"""
Account Management tab module.
"""

from shadowlib.types.gametab import GameTab, GameTabs


class Account(GameTabs):
    """
    Singleton account management tab - displays account settings and info.

    Example:
        from shadowlib.tabs.account import account

        account.open()
    """

    TAB_TYPE = GameTab.ACCOUNT

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
account = Account()
