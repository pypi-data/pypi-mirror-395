"""
GameTabs package - contains all game tab modules for OSRS.

Each tab inherits from the base GameTabs class and provides
tab-specific functionality for the Old School RuneScape interface.
"""

from shadowlib.types.gametab import GameTab, GameTabs

from .account import Account, account
from .combat import Combat, combat
from .emotes import Emotes, emotes
from .equipment import Equipment, equipment
from .friends import Friends, friends
from .grouping import Grouping, grouping
from .inventory import Inventory, inventory
from .logout import Logout, logout
from .magic import Magic, magic
from .music import Music, music
from .prayer import Prayer, prayer
from .progress import Progress, progress
from .settings import Settings, settings
from .skills import Skills, skills


class Tabs:
    """
    Namespace for game tabs - returns singleton instances.

    Example:
        from shadowlib.client import client

        client.tabs.inventory.getItems()
        # Or directly:
        from shadowlib.tabs.inventory import inventory
        inventory.getItems()
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def combat(self) -> Combat:
        """Get combat tab singleton."""
        return combat

    @property
    def skills(self) -> Skills:
        """Get skills tab singleton."""
        return skills

    @property
    def progress(self) -> Progress:
        """Get progress tab singleton."""
        return progress

    @property
    def inventory(self) -> Inventory:
        """Get inventory tab singleton."""
        return inventory

    @property
    def equipment(self) -> Equipment:
        """Get equipment tab singleton."""
        return equipment

    @property
    def prayer(self) -> Prayer:
        """Get prayer tab singleton."""
        return prayer

    @property
    def magic(self) -> Magic:
        """Get magic tab singleton."""
        return magic

    @property
    def grouping(self) -> Grouping:
        """Get grouping tab singleton."""
        return grouping

    @property
    def friends(self) -> Friends:
        """Get friends tab singleton."""
        return friends

    @property
    def account(self) -> Account:
        """Get account tab singleton."""
        return account

    @property
    def settings(self) -> Settings:
        """Get settings tab singleton."""
        return settings

    @property
    def logout(self) -> Logout:
        """Get logout tab singleton."""
        return logout

    @property
    def emotes(self) -> Emotes:
        """Get emotes tab singleton."""
        return emotes

    @property
    def music(self) -> Music:
        """Get music tab singleton."""
        return music

    def getOpenTab(self) -> GameTab | None:
        """
        Get the currently open tab.

        Returns:
            The currently open GameTab, or None if unknown

        Example:
            >>> from shadowlib.client import client
            >>> tab = client.tabs.getOpenTab()
            >>> if tab == GameTab.INVENTORY:
            ...     print("Inventory is open")
        """
        from shadowlib.client import client

        index = client.cache.getVarc(client.VarClientID.TOPLEVEL_PANEL)
        return GameTab(index) if index in GameTab._value2member_map_ else None


# Module-level singleton instance
tabs = Tabs()


__all__ = [
    "GameTab",
    "GameTabs",
    "Tabs",
    "tabs",
    "Combat",
    "combat",
    "Skills",
    "skills",
    "Progress",
    "progress",
    "Inventory",
    "inventory",
    "Equipment",
    "equipment",
    "Prayer",
    "prayer",
    "Magic",
    "magic",
    "Grouping",
    "grouping",
    "Friends",
    "friends",
    "Account",
    "account",
    "Settings",
    "settings",
    "Logout",
    "logout",
    "Emotes",
    "emotes",
    "Music",
    "music",
]
