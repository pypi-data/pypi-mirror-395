"""
Player state middleware.

Provides clean access to player properties via cache.
"""

from typing import Any, Dict


class Player:
    """
    Singleton player state accessor.

    Example:
        from shadowlib.player.player import player

        print(f"Player at ({player.x}, {player.y})")
        print(f"Run energy: {player.energy / 100}%")
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        """Actual initialization, runs once."""
        self._cached_state: Dict[str, Any] = {}
        self._cached_tick: int = -1

    def _getState(self) -> Dict[str, Any]:
        """
        Get cached player state (refreshed per tick).

        Returns:
            Player state dict
        """
        from shadowlib.client import client

        current_tick = client.cache.tick

        # Return cached if same tick
        if self._cached_tick == current_tick and self._cached_state:
            return self._cached_state

        # Refresh from cache
        self._cached_state = client.cache.position.copy()
        self._cached_tick = current_tick

        return self._cached_state

    @property
    def position(self) -> Dict[str, int]:
        """
        Get player position.

        Returns:
            Dict with 'x', 'y', 'plane' keys

        Example:
            >>> from shadowlib.player.player import player
            >>> pos = player.position
            >>> print(f"Player at ({pos['x']}, {pos['y']}, {pos['plane']})")
        """
        return self._getState()

    @property
    def x(self) -> int:
        """Get player X coordinate."""
        return self._getState().get("x", 0)

    @property
    def y(self) -> int:
        """Get player Y coordinate."""
        return self._getState().get("y", 0)

    @property
    def plane(self) -> int:
        """Get player plane level."""
        return self._getState().get("plane", 0)

    @property
    def energy(self) -> int:
        """
        Get run energy (0-10000).

        Returns:
            Run energy value

        Example:
            >>> from shadowlib.player.player import player
            >>> energy = player.energy
            >>> print(f"Run energy: {energy / 100}%")
        """
        from shadowlib.client import client

        return client.cache.energy

    @property
    def tick(self) -> int:
        """
        Get current game tick.

        Returns:
            Current tick number

        Example:
            >>> from shadowlib.player.player import player
            >>> tick = player.tick
        """
        from shadowlib.client import client

        return client.cache.tick

    def distanceTo(self, x: int, y: int) -> int:
        """
        Calculate distance from player to coordinates.

        Args:
            x: Target X coordinate
            y: Target Y coordinate

        Returns:
            Chebyshev distance in tiles

        Example:
            >>> from shadowlib.player.player import player
            >>> distance = player.distanceTo(3200, 3200)
        """
        dx = abs(self.x - x)
        dy = abs(self.y - y)
        return max(dx, dy)

    def isAt(self, x: int, y: int, plane: int | None = None) -> bool:
        """
        Check if player is at specific coordinates.

        Args:
            x: X coordinate
            y: Y coordinate
            plane: Optional plane (if None, ignores plane)

        Returns:
            True if player is at position

        Example:
            >>> from shadowlib.player.player import player
            >>> if player.isAt(3200, 3200):
            ...     print("At Grand Exchange")
        """
        if self.x != x or self.y != y:
            return False

        return not (plane is not None and self.plane != plane)

    def isNearby(self, x: int, y: int, radius: int, plane: int | None = None) -> bool:
        """
        Check if player is within radius of coordinates.

        Args:
            x: X coordinate
            y: Y coordinate
            radius: Maximum distance in tiles
            plane: Optional plane (if None, ignores plane)

        Returns:
            True if within radius

        Example:
            >>> from shadowlib.player.player import player
            >>> if player.isNearby(3200, 3200, radius=10):
            ...     print("Near Grand Exchange")
        """
        if plane is not None and self.plane != plane:
            return False

        return self.distanceTo(x, y) <= radius


# Module-level singleton instance
player = Player()
