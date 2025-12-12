"""Interaction systems - menu, clicking, hovering, widgets."""

from shadowlib.interactions.menu import Menu, menu


class Interactions:
    """
    Namespace for interaction systems - returns singleton instances.

    Example:
        from shadowlib.client import client

        client.interactions.menu.clickOption("Take")
        # Or directly:
        from shadowlib.interactions.menu import menu
        menu.clickOption("Take")
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def menu(self) -> Menu:
        """Get menu interaction handler singleton."""
        return menu


# Module-level singleton instance
interactions = Interactions()


__all__ = ["Interactions", "interactions", "Menu", "menu"]
