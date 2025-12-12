"""Overlay windows - bank, GE, shop, dialogue, etc."""

from shadowlib.interfaces.bank import Bank, bank


class Interfaces:
    """
    Namespace for overlay interfaces - returns singleton instances.

    Example:
        from shadowlib.client import client

        client.interfaces.bank.depositAll()
        # Or directly:
        from shadowlib.interfaces.bank import bank
        bank.depositAll()
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def bank(self) -> Bank:
        """Get bank interface singleton."""
        return bank


# Module-level singleton instance
interfaces = Interfaces()


__all__ = ["Interfaces", "interfaces", "Bank", "bank"]
