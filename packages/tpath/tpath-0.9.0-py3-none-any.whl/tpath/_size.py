"""
Size property implementation for TPath.

Handles file size operations with various units.
"""

import re
from pathlib import Path

from ._constants import (
    BYTES_PER_GB,
    BYTES_PER_GIB,
    BYTES_PER_KB,
    BYTES_PER_KIB,
    BYTES_PER_MB,
    BYTES_PER_MIB,
    BYTES_PER_PB,
    BYTES_PER_PIB,
    BYTES_PER_TB,
    BYTES_PER_TIB,
)


class Size:
    """Property class for handling file size operations with various units."""

    def __init__(self, path: Path):
        self.path = path

    @property
    def bytes(self) -> int:
        """Get file size in bytes."""
        return self.path.stat().st_size if self.path.exists() else 0

    @property
    def b(self) -> int:
        """Get file size in bytes (alias for .bytes)."""
        return self.bytes

    @property
    def kb(self) -> float:
        """Get file size in kilobytes (1000 bytes)."""
        return self.bytes / BYTES_PER_KB

    @property
    def mb(self) -> float:
        """Get file size in megabytes (1000^2 bytes)."""
        return self.bytes / BYTES_PER_MB

    @property
    def gb(self) -> float:
        """Get file size in gigabytes (1000^3 bytes)."""
        return self.bytes / BYTES_PER_GB

    @property
    def tb(self) -> float:
        """Get file size in terabytes (1000^4 bytes)."""
        return self.bytes / BYTES_PER_TB

    @property
    def pb(self) -> float:
        """Get file size in petabytes (1000^5 bytes)."""
        return self.bytes / BYTES_PER_PB

    @property
    def kib(self) -> float:
        """Get file size in kibibytes (1024 bytes)."""
        return self.bytes / BYTES_PER_KIB

    @property
    def mib(self) -> float:
        """Get file size in mebibytes (1024^2 bytes)."""
        return self.bytes / BYTES_PER_MIB

    @property
    def gib(self) -> float:
        """Get file size in gibibytes (1024^3 bytes)."""
        return self.bytes / BYTES_PER_GIB

    @property
    def tib(self) -> float:
        """Get file size in tebibytes (1024^4 bytes)."""
        return self.bytes / BYTES_PER_TIB

    @property
    def pib(self) -> float:
        """Get file size in pebibytes (1024^5 bytes)."""
        return self.bytes / BYTES_PER_PIB

    @staticmethod
    def parse(size_str: str) -> int:
        """
        Parse a size string and return the size in bytes.

        Examples:
            "100" -> 100 bytes
            "1KB" -> 1000 bytes
            "1KiB" -> 1024 bytes
            "2.5MB" -> 2500000 bytes
            "1.5GiB" -> 1610612736 bytes
        """
        size_str = size_str.strip().upper()

        # Handle plain numbers (bytes)
        if size_str.isdigit():
            return int(size_str)

        # Regular expression to parse size with unit
        match = re.match(r"^(\d+(?:\.\d+)?)\s*([A-Za-z]+)$", size_str)
        if not match:
            raise ValueError(f"Invalid size format: {size_str}")

        value = float(match.group(1))
        unit = match.group(2).upper()

        # Define multipliers
        binary_units = {
            "B": 1,
            "KB": BYTES_PER_KB,
            "MB": BYTES_PER_MB,
            "GB": BYTES_PER_GB,
            "TB": BYTES_PER_TB,
            "PB": BYTES_PER_PB,
            "KIB": BYTES_PER_KIB,
            "MIB": BYTES_PER_MIB,
            "GIB": BYTES_PER_GIB,
            "TIB": BYTES_PER_TIB,
            "PIB": BYTES_PER_PIB,
        }

        if unit not in binary_units:
            raise ValueError(f"Unknown unit: {unit}")

        return int(value * binary_units[unit])


__all__ = ["Size"]
