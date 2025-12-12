"""
TPath - A pathlib extension with time-based age and size utilities.

This package provides enhanced pathlib functionality with lambda-based
age and size operations. Users can import directly from tpath without
needing to know the internal package structure.

Examples:
    >>> from tpath import TPath, Size
    >>> path = TPath("myfile.txt")
    >>> path.age.days
    >>> path.size.gb
    >>> Size.parse("1.5GB")
"""

__version__ = "0.9.0"
__author__ = "Chuck Bass"

# Core exports - always available
from frist import Age, Biz, Cal, Chrono

from ._core import TPath
from ._size import Size
from ._time import PathTime, TimeType
from ._utils import PathInput, PathLike, PathSequence, matches

# All exports
__all__ = [
    # Core classes
    "TPath",
    "Size",
    "PathTime",
    "TimeType",
    # Frist utilities
    "Age",
    "Cal",
    "Biz",
    "Chrono",
    # Type aliases for type hints
    "PathLike",
    "PathInput",
    "PathSequence",
    # Utility functions
    "matches",
]
