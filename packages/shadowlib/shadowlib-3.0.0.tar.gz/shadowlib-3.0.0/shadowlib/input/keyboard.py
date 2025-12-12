"""Keyboard control with human-like typing."""

import random
import time
from typing import List, Optional

try:
    import pyautogui as pag
except ImportError:
    pag = None


class Keyboard:
    """
    Singleton keyboard controller with human-like typing.
    Uses pyautogui for cross-platform keyboard control.
    Requires RuneLite window focus for input.

    Example:
        from shadowlib.input.keyboard import keyboard

        keyboard.type("Hello world")
        keyboard.pressEnter()
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self, speed: float = 1.0):
        """
        Actual initialization, runs once.

        Args:
            speed: Typing speed multiplier (1.0 = ~50ms per keystroke)
        """
        from shadowlib.input.runelite import runelite

        if pag is None:
            raise ImportError("pyautogui is required. Install with: pip install pyautogui")

        # Configure pyautogui
        pag.PAUSE = 0
        pag.FAILSAFE = False

        self.runelite = runelite
        self.speed = speed

    def _ensureFocus(self) -> None:
        """
        Ensure RuneLite window is ready for input.
        Refreshes window position (respects 10s cache).
        """
        self.runelite.refreshWindowPosition()

    def _press(self, key: str) -> None:
        """
        Core press function - ONLY access point to pyautogui.press().

        Args:
            key: Key to press (e.g., 'enter', 'space', 'a', 'f1')
        """
        self._ensureFocus()
        pag.press(key, _pause=False)

    def _keyDown(self, key: str) -> None:
        """
        Core key down function - ONLY access point to pyautogui.keyDown().

        Args:
            key: Key to hold down
        """
        self._ensureFocus()
        pag.keyDown(key, _pause=False)

    def _keyUp(self, key: str) -> None:
        """
        Core key up function - ONLY access point to pyautogui.keyUp().

        Args:
            key: Key to release
        """
        self._ensureFocus()
        pag.keyUp(key, _pause=False)

    def _typeChar(self, char: str) -> None:
        """
        Core type function - ONLY access point to pyautogui.write() for single char.

        Args:
            char: Single character to type
        """
        self._ensureFocus()
        pag.write(char, interval=0, _pause=False)

    def type(self, text: str, humanize: bool = True) -> None:
        """
        Type text with optional human-like delays.

        Args:
            text: Text to type
            humanize: If True, adds random delays between keystrokes

        Example:
            >>> keyboard.type("Hello world")
            >>> keyboard.type("fast typing", humanize=False)
        """
        if not text:
            return

        self._ensureFocus()

        # Base delay: ~50ms per keystroke at speed=1.0
        base_delay = 0.05 / self.speed

        for char in text:
            self._typeChar(char)

            if humanize:
                # Random delay with variation (±40%)
                delay = base_delay * random.uniform(0.6, 1.4)

                # Occasionally add longer pause (simulates thinking)
                if random.random() < 0.05:
                    delay += random.uniform(0.1, 0.3)

                time.sleep(delay)

    def press(self, key: str) -> None:
        """
        Press and release a key.

        Args:
            key: Key to press (e.g., 'enter', 'space', 'escape', 'f1')

        Example:
            >>> keyboard.press('enter')
            >>> keyboard.press('escape')
            >>> keyboard.press('f1')
        """
        self._press(key)

        # Small delay after key press (human-like)
        time.sleep(random.uniform(0.02, 0.05))

    def hold(self, key: str) -> None:
        """
        Hold a key down (must call release() to let go).

        Args:
            key: Key to hold

        Example:
            >>> keyboard.hold('shift')
            >>> keyboard.type('hello')  # Types 'HELLO'
            >>> keyboard.release('shift')
        """
        self._keyDown(key)

    def release(self, key: str) -> None:
        """
        Release a held key.

        Args:
            key: Key to release

        Example:
            >>> keyboard.hold('ctrl')
            >>> keyboard.press('a')  # Ctrl+A
            >>> keyboard.release('ctrl')
        """
        self._keyUp(key)

        # Small delay after release (human-like)
        time.sleep(random.uniform(0.02, 0.05))

    def hotkey(self, *keys: str) -> None:
        """
        Press a key combination (hotkey).

        Args:
            *keys: Keys to press together

        Example:
            >>> keyboard.hotkey('ctrl', 'a')      # Select all
            >>> keyboard.hotkey('ctrl', 'shift', 'escape')  # Task manager
            >>> keyboard.hotkey('alt', 'f4')     # Close window
        """
        self._ensureFocus()

        # Press keys in order
        for key in keys:
            self._keyDown(key)
            time.sleep(random.uniform(0.01, 0.03))

        # Release in reverse order
        for key in reversed(keys):
            self._keyUp(key)
            time.sleep(random.uniform(0.01, 0.03))

        # Small delay after hotkey (human-like)
        time.sleep(random.uniform(0.03, 0.08))

    def pressEnter(self) -> None:
        """
        Press Enter key.

        Example:
            >>> keyboard.type("search query")
            >>> keyboard.pressEnter()
        """
        self.press("enter")

    def pressEscape(self) -> None:
        """
        Press Escape key.

        Example:
            >>> keyboard.pressEscape()  # Close menu/dialog
        """
        self.press("escape")

    def pressSpace(self) -> None:
        """
        Press Space key.

        Example:
            >>> keyboard.pressSpace()  # Continue dialogue
        """
        self.press("space")

    def pressTab(self) -> None:
        """
        Press Tab key.

        Example:
            >>> keyboard.pressTab()  # Next field
        """
        self.press("tab")

    def pressFKey(self, num: int) -> None:
        """
        Press a function key (F1-F12).

        Args:
            num: Function key number (1-12)

        Raises:
            ValueError: If num is not between 1 and 12

        Example:
            >>> keyboard.pressFKey(1)   # Press F1
            >>> keyboard.pressFKey(5)   # Press F5
        """
        if not 1 <= num <= 12:
            raise ValueError(f"Function key must be between 1 and 12, got {num}")

        self.press(f"f{num}")

    def pressNumber(self, num: int) -> None:
        """
        Press a number key (0-9).

        Args:
            num: Number to press (0-9)

        Raises:
            ValueError: If num is not between 0 and 9

        Example:
            >>> keyboard.pressNumber(1)  # Press '1' key
            >>> keyboard.pressNumber(5)  # Press '5' key
        """
        if not 0 <= num <= 9:
            raise ValueError(f"Number must be between 0 and 9, got {num}")

        self.press(str(num))


# Module-level singleton instance
keyboard = Keyboard()
