"""OS-level input handling - mouse and keyboard."""

from shadowlib.input.keyboard import Keyboard, keyboard
from shadowlib.input.mouse import Mouse, mouse
from shadowlib.input.runelite import RuneLite, runelite


class Input:
    """
    Namespace for input controls - returns singleton instances.

    Example:
        from shadowlib.client import client

        client.input.mouse.leftClick(100, 200)
        # Or directly:
        from shadowlib.input.mouse import mouse
        mouse.leftClick(100, 200)
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def runelite(self) -> RuneLite:
        """Get RuneLite window manager singleton."""
        return runelite

    @property
    def mouse(self) -> Mouse:
        """Get mouse controller singleton."""
        return mouse

    @property
    def keyboard(self) -> Keyboard:
        """Get keyboard controller singleton."""
        return keyboard


# Module-level singleton instance
input = Input()


__all__ = ["Input", "input", "Keyboard", "keyboard", "Mouse", "mouse", "RuneLite", "runelite"]
