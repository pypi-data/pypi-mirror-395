"""
ItemContainer type for representing item containers like inventory, bank, equipment.
"""

from typing import Any, Dict, List

from shadowlib.globals import getClient
from shadowlib.types.item import Item, ItemIdentifier


class ItemContainer:
    """
    Base class for OSRS item containers (inventory, bank, equipment, etc.).

    Can be used standalone as a data container or inherited by tab classes
    for additional functionality.

    All item lookup methods accept either an item ID (int) or item name (str).

    Attributes:
        containerId: Unique identifier for this container
        slotCount: Number of slots in container (-1 if unknown)
        items: List of items in slots (None for empty slots)
    """

    def __init__(self, containerId: int = -1, slotCount: int = -1, items: List[Item | None] = None):
        """
        Initialize item container.

        Args:
            containerId: Unique identifier for this container (default -1)
            slotCount: Number of slots in container (-1 if unknown)
            items: List of items in slots (None for empty slots)
        """
        self.containerId = containerId
        self.slotCount = slotCount
        self.items = items if items is not None else []

    def fromArray(self, data: List[Dict[str, Any]]):
        """
        Populate ItemContainer from array of item dicts.
        Args:
            data: List of item dicts from Java response
        """
        parsedItems = [
            Item.fromDict(itemData) if itemData is not None else None for itemData in data
        ]

        self.items = parsedItems

    def populate(self):
        client = getClient()

        result = client.api.invokeCustomMethod(
            target="EventBusListener",
            method="getItemContainerPacked",
            signature="(I)[B",
            args=[self.containerId],
            async_exec=False,
        )

        if result:
            self.fromArray(result)

    def toDict(self) -> Dict[str, Any]:
        """
        Convert ItemContainer back to dict format.

        Returns:
            Dict with 'containerId', 'slotCount', 'items'
        """
        return {
            "containerId": self.containerId,
            "slotCount": self.slotCount,
            "items": [item.toDict() if item is not None else None for item in self.items],
        }

    def getTotalCount(self) -> int:
        """
        Get count of non-empty slots.

        Returns:
            Number of items (non-None slots)
        """
        return sum(1 for item in self.items if item is not None)

    def getTotalQuantity(self) -> int:
        """
        Get total quantity of all items (sum of stacks).

        Returns:
            Total item quantity across all slots
        """
        return sum(item.quantity for item in self.items if item is not None)

    def getItemCount(self, identifier: ItemIdentifier) -> int:
        """
        Get count of items matching the given ID or name.

        Args:
            identifier: Item ID (int) or name (str) to count

        Returns:
            Number of matching items

        Example:
            count = container.getItemCount(995)        # By ID
            count = container.getItemCount("Coins")    # By name
        """
        if isinstance(identifier, int):
            return sum(1 for item in self.items if item is not None and item.id == identifier)
        return sum(1 for item in self.items if item is not None and identifier in item.name)

    def getItems(self, identifier: ItemIdentifier) -> List[Item]:
        """
        Get all items matching the given ID or name.

        Args:
            identifier: Item ID (int) or name (str) to search for

        Returns:
            List of all matching Items

        Example:
            items = container.getItems(995)        # By ID
            items = container.getItems("Coins")    # By name
        """
        if isinstance(identifier, int):
            return [item for item in self.items if item is not None and item.id == identifier]
        return [item for item in self.items if item is not None and identifier in item.name]

    def getSlot(self, slotIndex: int) -> Item | None:
        """
        Get item at specific slot index.

        Args:
            slotIndex: Slot index (0-based)

        Returns:
            Item at slot, or None if empty or out of range
        """
        if 0 <= slotIndex < len(self.items):
            return self.items[slotIndex]
        return None

    def getSlots(self, slots: List[int]) -> List[Item | None]:
        """
        Get items at specific slot indices.

        Args:
            slots: List of slot indices (0-based)

        Returns:
            List of Items or None for each requested slot
        """
        result = []
        for slotIndex in slots:
            if 0 <= slotIndex < len(self.items):
                result.append(self.items[slotIndex])
            else:
                result.append(None)
        return result

    def findItemSlot(self, identifier: ItemIdentifier) -> int | None:
        """
        Find the first slot index containing an item matching the ID or name.

        Args:
            identifier: Item ID (int) or name (str) to search for

        Returns:
            Slot index if found, else None

        Example:
            slot = container.findItemSlot(995)        # By ID
            slot = container.findItemSlot("Coins")    # By name
        """
        if isinstance(identifier, int):
            for index, item in enumerate(self.items):
                if item is not None and item.id == identifier:
                    return index
        else:
            for index, item in enumerate(self.items):
                if item is not None and identifier in item.name:
                    return index
        return None

    def findItemSlots(self, identifier: ItemIdentifier) -> List[int]:
        """
        Find all slot indices containing items matching the ID or name.

        Args:
            identifier: Item ID (int) or name (str) to search for

        Returns:
            List of slot indices

        Example:
            slots = container.findItemSlots(995)        # By ID
            slots = container.findItemSlots("Coins")    # By name
        """
        slots = []
        if isinstance(identifier, int):
            for index, item in enumerate(self.items):
                if item is not None and item.id == identifier:
                    slots.append(index)
        else:
            for index, item in enumerate(self.items):
                if item is not None and identifier in item.name:
                    slots.append(index)
        return slots

    def containsItem(self, identifier: ItemIdentifier) -> bool:
        """
        Check if container contains an item matching the ID or name.

        Args:
            identifier: Item ID (int) or name (str) to check

        Returns:
            True if matching item exists in container

        Example:
            has_coins = container.containsItem(995)        # By ID
            has_coins = container.containsItem("Coins")    # By name
        """
        if isinstance(identifier, int):
            return any(item is not None and item.id == identifier for item in self.items)
        return any(item is not None and identifier in item.name for item in self.items)

    def containsAllItems(self, identifiers: List[ItemIdentifier]) -> bool:
        """
        Check if container contains all items matching the given IDs or names.

        Args:
            identifiers: List of item IDs (int) or names (str) to check

        Returns:
            True if all items exist in container

        Example:
            has_all = container.containsAllItems([995, 1511])           # By IDs
            has_all = container.containsAllItems(["Coins", "Logs"])     # By names
            has_all = container.containsAllItems([995, "Logs"])         # Mixed
        """
        return all(self.containsItem(identifier) for identifier in identifiers)

    def getItemQuantity(self, identifier: ItemIdentifier) -> int:
        """
        Get total quantity of items matching the given ID or name.

        Args:
            identifier: Item ID (int) or name (str) to search for

        Returns:
            Total quantity across all matching items

        Example:
            qty = container.getItemQuantity(995)        # By ID
            qty = container.getItemQuantity("Coins")    # By name
        """
        if isinstance(identifier, int):
            return sum(
                item.quantity for item in self.items if item is not None and item.id == identifier
            )
        return sum(
            item.quantity for item in self.items if item is not None and identifier in item.name
        )

    def isEmpty(self) -> bool:
        """
        Check if container has no items.

        Returns:
            True if all slots are None
        """
        return all(item is None for item in self.items)

    def isFull(self) -> bool:
        """
        Check if container is full.

        Returns:
            True if no empty slots remain (considers slotCount if known)
        """
        if self.slotCount > 0:
            return self.getTotalCount() >= self.slotCount
        return all(item is not None for item in self.items)

    def __repr__(self) -> str:
        """String representation."""
        return f"ItemContainer(id={self.containerId}, items={self.toDict()})"

    def __eq__(self, other) -> bool:
        """Check equality with another ItemContainer."""
        if not isinstance(other, ItemContainer):
            return False
        return (
            self.containerId == other.containerId
            and self.slotCount == other.slotCount
            and self.items == other.items
        )
