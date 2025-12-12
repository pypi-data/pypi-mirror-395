"""
Core TPath implementation.

Main TPath class that extends pathlib.Path with age and size functionality.
"""

import os
import platform
import stat
import threading
from datetime import datetime
from pathlib import Path
from typing import Any

from frist import Age

from ._constants import (
    ACCESS_MODE_ALL,
    ACCESS_MODE_EXECUTE,
    ACCESS_MODE_READ,
    ACCESS_MODE_READ_ONLY,
    ACCESS_MODE_READ_WRITE,
    ACCESS_MODE_WRITE,
    ACCESS_MODE_WRITE_ONLY,
)
from ._size import Size
from ._time import PathTime


class TPath(Path):
    """
    Extended Path class with age and size functionality using lambdas.

    Provides first-class age functions and size utilities for file operations.

    IMPORTANT - Stat Caching Behavior:
    ===================================
    TPath objects cache their stat() result on first access and reuse it for all subsequent
    property calculations (size, age, timestamps, etc.). This creates a consistent "snapshot"
    of the file state that enforces atomic decision-making.

    Benefits:
    - Consistent decisions: All properties (size, age, existence) use the same stat snapshot
    - No race conditions: File can't change between size check and age calculation
    - Performance: Multiple property accesses only call stat() once
    - Predictable behavior: Same TPath instance always returns same values

    This matches the pattern of using a single timestamp for all files in a glob operation,
    ensuring uniform timing across batch operations.

    LIMITATION - External Race Conditions:
    =====================================
    Stat caching provides internal consistency but CANNOT prevent external file changes
    between analysis and file operations. This is a fundamental filesystem limitation
    that requires OS-level coordination (file locking, snapshots, or atomic copies).

    Example Race Condition:
        file = TPath("data.txt")
        if file.size.bytes > 1000:      # Cached as large file
            # File could be truncated/deleted HERE by external process
            data = file.read_text()      # May fail or read different content!

    Defensive Programming Recommended:
        if file.size.bytes > 1000:
            try:
                data = file.read_text()
            except (FileNotFoundError, PermissionError) as e:
                # Handle external file changes gracefully

    Example - Atomic Analysis:
        file = TPath("data.txt")
        if file.exists() and file.size.mb > 10 and file.age.hours < 1:
            # All three conditions use the same stat snapshot - no race conditions!
            process_large_recent_file(file)

    For fresh data, create a new TPath instance:
        fresh_file = TPath("data.txt")  # New snapshot with current stat data

    Examples:
        >>> path = TPath("myfile.txt")
        >>> path.age.days  # Age in days since creation
        >>> path.atime.age.hours  # Hours since last access
        >>> path.size.gb  # Size in gigabytes
        >>> path.size.gib  # Size in gibibytes
        >>> TPath.size.parse("1.5GB")  # Parse size string
    """

    _base_time: datetime
    _stat_lock: threading.Lock
    _cached_stat_result: Any

    def __init__(
        self, *args: Any, dir_entry: Any = None, cal_policy: Any = None, **kwargs: Any
    ):
        """
        Initialize TPath instance.

        Args:
            *args: Arguments for pathlib.Path.
            dir_entry: Optional directory entry for stat caching.
            cal_policy: Optional calendar policy for time-based calculations.
            **kwargs: Additional keyword arguments for pathlib.Path.
        """
        super().__init__(*args, **kwargs)
        self._base_time = getattr(self, "_base_time", datetime.now())
        self._stat_lock = getattr(self, "_stat_lock", threading.Lock())
        self._cal_policy = cal_policy
        if dir_entry is not None:
            self._cached_is_file = dir_entry.is_file(follow_symlinks=False)
            self._cached_is_dir = dir_entry.is_dir(follow_symlinks=False)
            self._cached_is_symlink = dir_entry.is_symlink()
        else:
            self._cached_is_file = None
            self._cached_is_dir = None
            self._cached_is_symlink = None

    def is_file(self) -> bool:
        if self._cached_is_file is not None:
            return self._cached_is_file
        return super().is_file()

    def is_dir(self) -> bool:
        if self._cached_is_dir is not None:
            return self._cached_is_dir
        return super().is_dir()

    def is_symlink(self) -> bool:
        if self._cached_is_symlink is not None:
            return self._cached_is_symlink
        return super().is_symlink()

    # ============================
    # This caching creates a consistent "snapshot" of file state for atomic decision-making.
    # Once stat() is called, all subsequent property accesses (size, age, timestamps) use
    # the same cached result, preventing race conditions and ensuring consistent analysis.

    def _stat_cache(self) -> Any:
        """Cache the stat result to avoid repeated filesystem calls (thread-safe)."""
        # Check if we already have a cached result (fast path, no lock needed)
        if hasattr(self, "_cached_stat_result"):
            return self._cached_stat_result

        # Use lock for thread-safe initialization
        with self._stat_lock:
            # Double-check pattern: another thread might have set it while we waited
            if hasattr(self, "_cached_stat_result"):
                return self._cached_stat_result

            try:
                original_stat = super().stat()
                # On platforms with st_birthtime, replace st_ctime with actual creation time
                if hasattr(original_stat, "st_birthtime") and hasattr(
                    original_stat, "st_ctime"
                ):
                    # Create new stat result with corrected st_ctime (using st_birthtime)
                    modified_stat = os.stat_result(
                        (
                            original_stat.st_mode,
                            original_stat.st_ino,
                            original_stat.st_dev,
                            original_stat.st_nlink,
                            original_stat.st_uid,
                            original_stat.st_gid,
                            original_stat.st_size,
                            original_stat.st_atime,
                            original_stat.st_mtime,
                            original_stat.st_birthtime,  # Use birthtime for ctime
                        )
                    )
                    result = modified_stat
                else:
                    result = original_stat
            except (OSError, FileNotFoundError):
                result = None

            # Cache the result
            object.__setattr__(self, "_cached_stat_result", result)
            return result

    def stat(self, *, follow_symlinks: bool = True) -> os.stat_result:
        """Override stat() to use cached result when possible."""
        if not follow_symlinks:
            # For symlinks with follow_symlinks=False, don't use cache
            return super().stat(follow_symlinks=False)

        # Use cached result for normal stat() calls
        cached_result = self._stat_cache()
        if cached_result is None:
            # File doesn't exist, call parent to get proper exception
            return super().stat(follow_symlinks=follow_symlinks)
        return cached_result

    @property
    def age(self) -> Age:
        """Get age property based on creation time."""
        return PathTime(
            self,
            "ctime",
            self._base_time,
            cal_policy=self._cal_policy,
        ).age

    @property
    def ctime(self) -> PathTime:
        """Get creation time property."""
        return PathTime(
            self,
            "ctime",
            self._base_time,
            cal_policy=self._cal_policy,
        )

    @property
    def mtime(self) -> PathTime:
        """Get modification time property."""
        return PathTime(
            self,
            "mtime",
            self._base_time,
            cal_policy=self._cal_policy,
        )

    @property
    def atime(self) -> PathTime:
        """Get access time property."""
        return PathTime(
            self,
            "atime",
            self._base_time,
            cal_policy=self._cal_policy,
        )

    @property
    def create(self) -> PathTime:
        """Get creation time property (alias for ctime)."""
        return PathTime(
            self,
            "create",
            self._base_time,
            cal_policy=self._cal_policy,
        )

    @property
    def modify(self) -> PathTime:
        """Get modification time property (alias for mtime)."""
        return PathTime(
            self,
            "modify",
            self._base_time,
            cal_policy=self._cal_policy,
        )

    @property
    def access(self) -> PathTime:
        """Get access time property (alias for atime)."""
        return PathTime(
            self,
            "access",
            self._base_time,
            cal_policy=self._cal_policy,
        )

    @property
    def size(self) -> Size:
        """Get size property."""
        return Size(self)

    # File Access Properties
    # ======================
    # These properties use the cached stat result for consistent permission checking

    @property
    def readable(self) -> bool:
        """True if the file has read permission."""
        return os.access(self, os.R_OK)

    @property
    def writable(self) -> bool:
        """True if the file has write permission."""
        return os.access(self, os.W_OK)

    @property
    def executable(self) -> bool:
        """True if the file has execute permission.

        Note: On Windows, this always returns True for existing files
        since Windows handles executable permissions differently.
        """
        # On Windows, executable permission is handled differently
        if platform.system() == "Windows":
            # Check if file exists first
            return os.access(self, os.F_OK)
        return os.access(self, os.X_OK)  # pragma: no cover # Testing on windows now

    @property
    def read_only(self) -> bool:
        """True if the file is readable but not writable."""
        return self.readable and not self.writable

    @property
    def write_only(self) -> bool:
        """True if the file is writable but not readable."""
        return self.writable and not self.readable

    @property
    def read_write(self) -> bool:
        """True if the file is both readable and writable."""
        return self.readable and self.writable

    def access_mode(self, spec: str) -> bool:
        """Check if file matches the specified access mode.

        Args:
            spec: Access mode specification. Supported formats:
                - ACCESS_MODE_READ ("R") - readable
                - ACCESS_MODE_WRITE ("W") - writable
                - ACCESS_MODE_EXECUTE ("X") - executable
                - ACCESS_MODE_READ_ONLY ("RO") - read-only (readable but not writable)
                - ACCESS_MODE_WRITE_ONLY ("WO") - write-only (writable but not readable)
                - ACCESS_MODE_READ_WRITE ("RW") - read-write (both readable and writable)
                - ACCESS_MODE_ALL ("RWX") - all permissions
                Case-insensitive. Also accepts long form aliases like "READ", "WRITE", etc.

        Returns:
            bool: True if file matches the specified mode

        Examples:
            file.access_mode("RO")    # Read-only check
            file.access_mode("RW")    # Read-write check
            file.access_mode("X")     # Executable check
        """
        spec = spec.upper().strip()

        if spec in (ACCESS_MODE_READ, "READ"):
            return self.readable
        elif spec in (ACCESS_MODE_WRITE, "WRITE"):
            return self.writable
        elif spec in (ACCESS_MODE_EXECUTE, "EXEC", "EXECUTABLE"):
            return self.executable
        elif spec in (ACCESS_MODE_READ_ONLY, "READONLY", "READ_ONLY"):
            return self.read_only
        elif spec in (ACCESS_MODE_WRITE_ONLY, "WRITEONLY", "WRITE_ONLY"):
            return self.write_only
        elif spec in (ACCESS_MODE_READ_WRITE, "READWRITE", "READ_WRITE"):
            return self.read_write
        elif spec in (ACCESS_MODE_ALL, "ALL"):
            return self.readable and self.writable and self.executable
        else:
            valid_specs = [
                ACCESS_MODE_READ,
                ACCESS_MODE_WRITE,
                ACCESS_MODE_EXECUTE,
                ACCESS_MODE_READ_ONLY,
                ACCESS_MODE_WRITE_ONLY,
                ACCESS_MODE_READ_WRITE,
                ACCESS_MODE_ALL,
            ]
            raise ValueError(
                f"Invalid mode specification: '{spec}'. Valid options: {valid_specs}"
            )

    @property
    def owner_readable(self) -> bool:
        """True if the owner has read permission."""
        try:
            stat_result = self.stat()
            return bool(stat_result.st_mode & stat.S_IRUSR)
        except (OSError, FileNotFoundError):
            return False

    @property
    def owner_writable(self) -> bool:
        """True if the owner has write permission."""
        try:
            stat_result = self.stat()
            return bool(stat_result.st_mode & stat.S_IWUSR)
        except (OSError, FileNotFoundError):
            return False

    @property
    def owner_executable(self) -> bool:
        """True if the owner has execute permission."""
        try:
            stat_result = self.stat()
            # On Windows, always return True for existing files
            if platform.system() == "Windows":
                return True
            return bool(stat_result.st_mode & stat.S_IXUSR)
        except (OSError, FileNotFoundError):
            return False

    def with_base_time(self, base_time: datetime) -> "TPath":
        """Create a new TPath with a different base time for age calculations."""
        new_path = TPath(str(self))
        object.__setattr__(new_path, "_base_time", base_time)
        return new_path


__all__ = ["TPath"]
