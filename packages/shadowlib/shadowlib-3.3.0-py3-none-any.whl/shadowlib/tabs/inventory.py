"""
Inventory tab module.
"""

from typing import List

from shadowlib.types.box import Box, createGrid
from shadowlib.types.gametab import GameTab, GameTabs
from shadowlib.types.item import ItemIdentifier
from shadowlib.types.itemcontainer import ItemContainer


class Inventory(GameTabs, ItemContainer):
    """
    Singleton inventory operations class combining GameTab and ItemContainer functionality.

    Example:
        from shadowlib.tabs.inventory import inventory

        items = inventory.getItems()
        inventory.clickItem(1511)
    """

    TAB_TYPE = GameTab.INVENTORY  # This tab represents the inventory
    INVENTORY_ID = 93  # RuneLite inventory container ID

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        """Actual initialization, runs once."""
        # Initialize GameTabs (which sets up tab areas)
        GameTabs.__init__(self)
        # Set ItemContainer attributes directly (can't call __init__ because items is a property)
        self.containerId = self.INVENTORY_ID
        self.slotCount = 28
        self._items = []

        # Create inventory slot grid (4 columns x 7 rows, 28 slots total)
        # Slot 0 starts at (563, 213), each slot is 36x32 pixels with 6px horizontal spacing
        # 2px padding on all sides to avoid misclicks on edges
        self.slots = createGrid(
            startX=563,
            startY=213,
            width=36,
            height=32,
            columns=4,
            rows=7,
            spacingX=6,
            spacingY=4,  # Vertical spacing between rows
            padding=1,  # 2px padding on all sides to avoid edge misclicks
        )

    @property
    def items(self):
        """Auto-sync items from cache when accessed."""
        from shadowlib.client import client

        cached = client.cache.getItemContainer(self.INVENTORY_ID)
        self._items = cached.items
        return self._items

    def getSlotBox(self, slot_index: int) -> Box:
        """
        Get the Box area for a specific inventory slot.

        Args:
            slot_index: Slot index (0-27)
        Returns:
            Box area of the specified slot
        """
        return self.slots[slot_index]

    def hoverSlot(self, slot_index: int) -> bool:
        """
        Hover over a specific inventory slot regardless of contents.

        Args:
            slot_index: Slot index (0-27) to hover

        Returns:
            True if slot index is valid, False otherwise

        Example:
            # Hover over slot 0 (top-left)
            inventory.hoverSlot(0)

            # Hover over slot 27 (bottom-right)
            inventory.hoverSlot(27)
        """
        if 0 <= slot_index < 28:
            self.slots[slot_index].hover()
            return True
        return False

    def hoverItem(self, identifier: ItemIdentifier) -> bool:
        """
        Hover over an item in the inventory.

        Args:
            identifier: Item ID (int) or name (str) to hover over

        Returns:
            True if item was found and hovered, False otherwise

        Example:
            inventory.hoverItem(1511)        # By ID
            inventory.hoverItem("Logs")      # By name
        """
        from shadowlib.client import client

        found_slots = self.findItemSlots(identifier)
        if not found_slots:
            return False

        # Hover the first found slot
        if self.hoverSlot(found_slots[0]):
            return client.interactions.menu.waitHasOption("Examine")

    def clickSlot(
        self, slot_index: int, option: str | None = None, type: str | None = None
    ) -> bool:
        """
        Click a specific inventory slot.

        Args:
            slot_index: Slot index (0-27) to click
            option: Specific menu option to click (if any)
            type: Specific menu type to click (if any)

        Returns:
            True if slot was clicked successfully, False otherwise

        Example:
            # Click slot 0 (top-left)
            inventory.clickSlot(0)

            # Click "Use" option on slot 5
            inventory.clickSlot(5, option="Use")
        """
        from shadowlib.client import client

        if not self.hoverSlot(slot_index):
            return False

        if option:
            return client.interactions.menu.clickOption(option)
        if type:
            return client.interactions.menu.clickOptionType(type)

        client.input.mouse.leftClick()
        return True

    def clickItem(
        self,
        identifier: ItemIdentifier,
        option: str | None = None,
        type: str | None = None,
    ) -> bool:
        """
        Click an item in the inventory.

        Args:
            identifier: Item ID (int) or name (str) to click
            option: Specific menu option to click (if any)
            type: Specific menu type to click (if any)

        Returns:
            True if item was found and clicked, False otherwise

        Example:
            inventory.clickItem(1511)                 # By ID
            inventory.clickItem("Logs")               # By name
            inventory.clickItem(1511, option="Use")   # With menu option
        """
        slot = self.findItemSlot(identifier)
        if slot is None:
            return False

        return self.clickSlot(slot, option=option, type=type)

    def isShiftDropEnabled(self) -> bool:
        """
        Check if shift-click drop is enabled in game settings.

        Returns:
            True if shift-drop is enabled, False otherwise

        Example:
            if inventory.isShiftDropEnabled():
                print("Shift-drop is enabled!")
        """
        from shadowlib._internal.resources import varps

        varbit_value = varps.getVarbitByName("DESKTOP_SHIFTCLICKDROP_ENABLED")
        return varbit_value == 1

    def waitDropOption(self, timeout: float = 0.5) -> bool:
        """
        Wait until the right-click menu contains the "Drop" option.

        Args:
            timeout: Maximum time to wait (seconds)

        Returns:
            True if "Drop" option appeared within timeout, False otherwise

        Example:
            if inventory.waitDropOption(2.0):
                print("Drop option is now available!")
        """
        import time

        from shadowlib.client import client

        start_time = time.time()

        while time.time() - start_time < timeout:
            if client.interactions.menu.hasOption("Drop"):
                return True
            time.sleep(0.001)  # Small delay before checking again

        return False

    def dropItem(self, identifier: ItemIdentifier, force_shift: bool = False) -> int:
        """
        Drop ALL occurrences of an item from the inventory.

        Automatically uses shift-drop if enabled in game settings,
        otherwise falls back to right-click menu.

        Args:
            identifier: Item ID (int) or name (str) to drop (drops ALL matching slots)
            force_shift: If True, forces shift-drop even if setting is disabled

        Returns:
            Number of items dropped

        Example:
            count = inventory.dropItem(1511)           # By ID
            count = inventory.dropItem("Logs")         # By name
            count = inventory.dropItem(1511, force_shift=True)

        Note:
            To drop a specific slot, use dropSlots([slot_index]) instead.
        """
        # Find all slots containing this item
        slots = self.findItemSlots(identifier)
        if not slots:
            return 0

        # Use drop_slots for the actual dropping logic
        return self.dropSlots(slots, force_shift=force_shift)

    def dropItems(self, identifiers: List[ItemIdentifier], force_shift: bool = False) -> int:
        """
        Drop ALL occurrences of multiple items from inventory.

        If shift-drop is enabled, holds shift for all drops (more efficient).

        Args:
            identifiers: List of item IDs (int) or names (str) to drop
            force_shift: If True, forces shift-drop even if setting is disabled

        Returns:
            Total number of items dropped

        Example:
            count = inventory.dropItems([1511, 590])           # By IDs
            count = inventory.dropItems(["Logs", "Tinderbox"]) # By names
            count = inventory.dropItems([1511, "Tinderbox"])   # Mixed

        Note:
            This drops ALL slots containing each item.
            To drop specific slots, use dropSlots([slot1, slot2, ...]) instead.
        """
        # Collect all slots to drop (all occurrences of all items)
        all_slots = []
        for identifier in identifiers:
            slots = self.findItemSlots(identifier)
            all_slots.extend(slots)

        if not all_slots:
            return 0

        # Use drop_slots for the actual dropping logic
        return self.dropSlots(all_slots, force_shift=force_shift)

    def dropSlots(self, slot_indices: List[int], force_shift: bool = False) -> int:
        """
        Drop items from specific inventory slots.

        If shift-drop is enabled, holds shift for all drops (more efficient).

        Args:
            slot_indices: List of slot indices (0-27) to drop
            force_shift: If True, forces shift-drop even if setting is disabled

        Returns:
            Number of slots successfully dropped

        Example:
            # Drop items in slots 12, 13, 14
            count = inventory.dropSlots([12, 13, 14])
            print(f"Dropped {count} items")

            # Drop entire inventory (all 28 slots)
            inventory.dropSlots(list(range(28)))
        """
        from time import perf_counter, sleep

        from shadowlib.client import client

        if not slot_indices:
            return 0

        # Check if shift-drop is enabled or forced
        use_shift_drop = force_shift or self.isShiftDropEnabled()

        dropped_count = 0
        keyboard = client.input.keyboard

        if use_shift_drop:
            # Hold shift for all drops
            keyboard.hold("shift")
            sleep(0.025)

        try:
            for slot_index in slot_indices:
                # Hover over the slot
                start_time = perf_counter()
                self.hoverSlot(slot_index)
                end_time = perf_counter()
                print(f"Hovered slot {slot_index} in {end_time - start_time:.6f} seconds")

                # Wait for Drop option to appear in menu
                start_wait = perf_counter()
                if not self.waitDropOption():
                    print("Drop option not found in menu, skipping item.")
                    continue  # Skip if Drop option not available
                end_wait = perf_counter()
                print(f"Waited for Drop option in {end_wait - start_wait:.6f} seconds")

                # Click Drop option with fresh cache
                start_click = perf_counter()
                if client.interactions.menu.clickOption("Drop"):
                    dropped_count += 1
                end_click = perf_counter()
                print(f"Clicked Drop option in {end_click - start_click:.6f} seconds")
        finally:
            if use_shift_drop:
                # Always release shift
                keyboard.release("shift")

        return dropped_count

    def selectSlot(self, slot_index: int) -> bool:
        """
        Select a specific inventory slot (for 'Use item on...' actions).

        Verifies the slot was successfully selected using cache validation.

        Args:
            slot_index: Slot index (0-27) to select

        Returns:
            True if slot was selected successfully, False otherwise

        Example:
            # Select item in slot 0 for use
            if inventory.selectSlot(0):
                print("Item in slot 0 selected!")
        """
        import shadowlib.utilities.timing as timing
        from shadowlib.client import client

        if not (0 <= slot_index < 28):
            return False

        # Click the item to select it
        if not self.hoverSlot(slot_index):
            return False
        if not client.interactions.menu.waitHasType("WIDGET_TARGET"):
            print("WIDGET_TARGET type not found in menu")
            return False
        print("WIDGET_TARGET type found in menu")
        if client.interactions.menu.clickOptionType("WIDGET_TARGET"):
            return timing.waitUntil(self.isItemSelected, 1, 0.01)

    def isItemSelected(self) -> bool:
        """
        Check if an item is currently selected in the inventory (for 'Use item on...' actions).

        Returns:
            True if an item is selected, False otherwise
        Example:
            if inventory.isItemSelected():
                print("An item is currently selected!")
        """
        from shadowlib.client import client

        widget = client.cache.getLastSelectedWidget()
        id = widget.get("selected_widget_id", -1)
        return id == client.InterfaceID.Inventory.ITEMS

    def getSelectedItemSlot(self) -> int:
        """
        Get the slot index of the currently selected item in the inventory.

        Returns:
            Slot index if an item is selected, else None

        Example:
            slot = inventory.getSelectedItemSlot()
            if slot is not None:
                print(f"Item in slot {slot} is currently selected!")
        """
        from shadowlib.client import client

        widget = client.cache.getLastSelectedWidget()
        selected_index = widget.get("index", -1)
        return selected_index

    def unselectItem(self) -> bool:
        """
        Unselect the currently selected item in the inventory.

        Returns:
            True if an item was unselected, False otherwise

        Example:
            if inventory.unselectItem():
                print("Item unselected successfully!")
        """
        from shadowlib.client import client

        if not self.isItemSelected():
            return True

        # Click outside the inventory to unselect
        client.interactions.menu.clickOptionType("CANCEL")

    def selectItem(self, identifier: ItemIdentifier) -> bool:
        """
        Select an item in the inventory (for 'Use item on...' actions).

        Verifies the item was successfully selected using cache validation.

        Args:
            identifier: Item ID (int) or name (str) to select

        Returns:
            True if item was selected successfully, False otherwise

        Example:
            inventory.selectItem(590)           # By ID
            inventory.selectItem("Tinderbox")   # By name
        """
        # Find the slot to click
        target_slot = self.findItemSlot(identifier)

        if target_slot is not None:
            return self.selectSlot(target_slot)
        return False

    def useSlotOnSlot(
        self,
        slot_1: int,
        slot_2: int,
    ) -> bool:
        """
        Use one inventory slot on another (e.g. use item on item).
        """
        if self.selectSlot(slot_1):
            return self.clickSlot(slot_2, type="WIDGET_TARGET_ON_WIDGET")

        return False

    def useItemOnItem(self, item_1: ItemIdentifier, item_2: ItemIdentifier) -> bool:
        """
        Use one inventory item on another (e.g. use item on item).

        Args:
            item_1: First item ID (int) or name (str) to select
            item_2: Second item ID (int) or name (str) to use on

        Returns:
            True if action was performed, False otherwise

        Example:
            inventory.useItemOnItem(590, 1511)               # By IDs (tinderbox on logs)
            inventory.useItemOnItem("Tinderbox", "Logs")     # By names
            inventory.useItemOnItem(590, "Logs")             # Mixed
        """
        slot_1 = self.findItemSlot(item_1)
        slot_2 = self.findItemSlot(item_2)

        if slot_1 is not None and slot_2 is not None:
            return self.useSlotOnSlot(slot_1, slot_2)

        return False


# Module-level singleton instance
inventory = Inventory()
