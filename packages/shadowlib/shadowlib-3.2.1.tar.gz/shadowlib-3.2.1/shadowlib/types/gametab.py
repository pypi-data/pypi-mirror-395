"""
Base GameTab class - parent class for all game tab modules.
"""

from enum import Enum

from shadowlib.types.box import Box
from shadowlib.utilities.timing import waitUntil


class GameTab(Enum):
    """Enum representing all game tab types in OSRS."""

    COMBAT = 0
    SKILLS = 1
    PROGRESS = 2
    INVENTORY = 3
    EQUIPMENT = 4
    PRAYER = 5
    MAGIC = 6
    GROUPING = 7
    ACCOUNT = 8
    FRIENDS = 9
    LOGOUT = 10
    SETTINGS = 11
    EMOTES = 12
    MUSIC = 13


class GameTabs:
    """
    Base class for all game tabs in Old School RuneScape.

    Each game tab (Combat, Skills, Inventory, etc.) should inherit from this class.
    Subclasses must set the TAB_TYPE class attribute to their corresponding GameTab enum.
    """

    # Subclasses must override this
    TAB_TYPE: GameTab | None = None

    def __init__(self):
        """
        Initializes a GameTab instance, setting up the bounds and tab areas.

        Attributes:
            bounds (Box): The bounding Box for the GameTab.
            tab_box_array (List[Box]): A list of Box objects representing the clickable regions for each tab.
        """
        x = 547
        y = 205
        w = 190
        h = 261
        self.bounds = Box(x, y, x + w, y + h)
        # init as list of Boxes for each tab
        self.tab_box_array: list[Box] = []

        for i in range(7):
            tab_x = 530 + (i * 33)
            tab_y = 170
            tab_w = 27
            tab_h = 32
            self.tab_box_array.append(Box(tab_x, tab_y, tab_x + tab_w, tab_y + tab_h))

        for i in range(7):
            tab_x = 530 + (i * 33)
            tab_y = 470
            tab_w = 27
            tab_h = 32
            self.tab_box_array.append(Box(tab_x, tab_y, tab_x + tab_w, tab_y + tab_h))

        # Swap index 8 and 9 because the game is weird
        self.tab_box_array[8], self.tab_box_array[9] = self.tab_box_array[9], self.tab_box_array[8]

    def isOpen(self) -> bool:
        """
        Check if this specific game tab is currently open.

        Returns:
            True if this tab is open, False otherwise.
        """
        from shadowlib.client import client

        current_tab = client.tabs.getOpenTab()
        return current_tab == self.TAB_TYPE

    def hover(self) -> bool:
        """
        Hover over this specific game tab.

        Returns:
            True if the tab area was hovered, False if TAB_TYPE not set.

        Example:
            # Hover over the inventory tab
            inventory = Inventory()
            inventory.hover()
        """
        if self.TAB_TYPE is None:
            raise NotImplementedError("Subclass must set TAB_TYPE class attribute")

        # Hover over the tab's area
        tab_area = self.tab_box_array[self.TAB_TYPE.value]
        tab_area.hover()

        return True

    def open(self) -> bool:
        """
        Open this specific game tab.

        This method hovers over the tab before clicking, then forces
        a cache update to get fresh tab state immediately.

        Returns:
            True if the tab was successfully opened (or already open), False otherwise.

        Example:
            # Open the inventory tab
            inventory = Inventory()
            if inventory.open():
                print("Inventory tab is now open!")
        """
        if self.TAB_TYPE is None:
            raise NotImplementedError("Subclass must set TAB_TYPE class attribute")

        if self.isOpen():
            return True  # Already open

        # Click on the tab's area (which automatically hovers first)
        tab_area = self.tab_box_array[self.TAB_TYPE.value]
        tab_area.click()

        return waitUntil(self.isOpen, timeout=0.1, poll_interval=0.001)
