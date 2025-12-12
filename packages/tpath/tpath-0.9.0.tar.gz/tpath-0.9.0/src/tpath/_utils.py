"""
Utility functions for TPath, including pattern matching.
"""

import fnmatch
from collections.abc import Sequence
from pathlib import Path
from typing import TypeAlias

from ._core import TPath

__all__ = ["matches"]

# Type aliases for better readability and IDE support
PathLike: TypeAlias = str | Path | TPath
PathSequence: TypeAlias = Sequence[PathLike]
# PathInput represents what from_() accepts: single paths or sequences of paths
PathInput: TypeAlias = PathLike | PathSequence


def matches(
    path: PathLike,
    *patterns: str,
    case_sensitive: bool = True,
    full_path: bool = False,
) -> bool:
    """
    Check if a file path matches any of the given shell-style patterns.

    Args:
        path: File path to check (string, Path, or TPath)
        *patterns: One or more shell-style patterns (*, ?, [seq], [!seq])
        case_sensitive: Whether matching should be case-sensitive (default: True)
        full_path: Whether to match against full path or just filename (default: False)

    Returns:
        bool: True if path matches any pattern, False otherwise

    Examples:
        # Basic pattern matching
        matches("app.log", "*.log")  # True
        matches("backup.zip", "*.log")  # False

        # Multiple patterns (OR logic)
        matches("report.pdf", "*.pdf", "*.docx")  # True

        # Case-insensitive matching
        matches("IMAGE.JPG", "*.jpg", case_sensitive=False)  # True

        # Character classes and wildcards
        matches("data_2024.csv", "*202[3-4]*")  # True
        matches("config.ini", "*config*")  # True

        # Match against full path
        from pathlib import Path
        p = Path("/tmp/cache/temp.log")
        matches(p, "*/cache/*", full_path=True)  # True


    Patterns:
        *        Matches any sequence of characters
        ?        Matches any single character
        [seq]    Matches any character in seq
        [!seq]   Matches any character not in seq

    Note:
        This function uses Python's fnmatch module internally, which provides
        Unix shell-style wildcards. On case-insensitive filesystems, you may
        want to use case_sensitive=False for more predictable behavior.
    """
    if not patterns:
        raise ValueError("At least one pattern must be provided")

    # Convert to TPath if needed to ensure we have consistent behavior
    if not isinstance(path, TPath):
        path = TPath(path)

    # Determine what to match against
    target = str(path) if full_path else path.name

    # Check if any pattern matches
    for pattern in patterns:
        if case_sensitive:
            # For case-sensitive matching, we need to check both the pattern match
            # and that the actual case matches (since fnmatch may be case-insensitive on Windows)
            if fnmatch.fnmatch(target, pattern):
                # On case-insensitive systems, fnmatch might match regardless of case
                # So we need an additional exact check for the matching parts
                import re  # noqa: F401 # Lazy import - only needed for case-sensitive regex validation

                # Convert fnmatch pattern to regex for exact case checking
                regex_pattern = fnmatch.translate(pattern)
                if re.match(regex_pattern, target):
                    return True
        else:
            # Case-insensitive: convert both to lowercase
            if fnmatch.fnmatch(target.lower(), pattern.lower()):
                return True

    return False
