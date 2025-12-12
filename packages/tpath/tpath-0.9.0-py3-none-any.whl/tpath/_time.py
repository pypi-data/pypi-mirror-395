"""
Time property implementation for TPath.

Handles different time types (ctime, mtime, atime) with age calculation.
Uses Chronos internally for datetime operations while maintaining the same API.
"""

import datetime as dt
from pathlib import Path
from typing import Literal

from frist import Age, Biz, BizPolicy, Cal

TimeType = Literal["ctime", "mtime", "atime", "create", "modify", "access"]


class PathTime:
    """
    Property class for handling different time types (ctime, mtime, atime) with age calculation.

    NOTE: Calendar policy can be used for business based calendar filtering for fiscal calendars, business days, etc.
          The default is None which uses M-F, 9-5, workweek with fiscal year starting on Jan 1.

    """

    def __init__(
        self,
        path: Path,
        time_type: TimeType,
        ref_dt: dt.datetime,
        cal_policy: BizPolicy | None = None,
    ) -> None:
        self.path = path
        # Normalize time_type aliases to standard names
        self.time_type = self._normalize_time_type(time_type)
        self._ref_dt: dt.datetime = ref_dt
        self._cal_policy: BizPolicy | None = cal_policy
        self._target_dt: dt.datetime | None = None  # Lazy loading

    @staticmethod
    def _normalize_time_type(time_type: TimeType) -> Literal["ctime", "mtime", "atime"]:
        """Normalize time_type aliases to standard names."""
        if time_type in ("create", "ctime"):
            return "ctime"
        elif time_type in ("modify", "mtime"):
            return "mtime"
        elif time_type in ("access", "atime"):
            return "atime"
        else:
            # This should never happen with proper typing, but provide a fallback
            return "ctime"  # pragma: no cover

    def _get_stat(self):
        """Get stat result."""
        return self.path.stat()

    @property
    def age(self) -> Age:
        """Get age property for this time type."""
        # Handle nonexistent files
        if not self.path.exists():
            # For nonexistent files, return current time as the target
            # This means age will be 0 (file is "as old as now")
            return Age(
                start_time=self._ref_dt,
                end_time=self._ref_dt,
            )

        # Use Chronos for consistent datetime handling
        return Age(
            start_time=self.target_dt,
            end_time=self._ref_dt,
        )

    @property
    def cal(self) -> Cal:
        """Get calendar filtering functionality for this time object."""
        return Cal(
            self.target_dt,
            self.ref_dt,
        )

    @property
    def biz(self) -> Biz:
        """Get business logic filtering functionality for this time object."""
        return Biz(
            self.target_dt,
            self.ref_dt,
            self._cal_policy,
        )

    @property
    def timestamp(self) -> float:
        """Get the raw timestamp for this time type."""
        if not self.path.exists():
            return 0

        stat = self._get_stat()

        if self.time_type == "ctime":
            # Try st_birthtime first (newer), fall back to st_mtime for compatibility
            birthtime = getattr(stat, "st_birthtime", None)
            return birthtime if birthtime is not None else stat.st_mtime
        elif self.time_type == "mtime":
            return stat.st_mtime
        elif self.time_type == "atime":
            return stat.st_atime
        else:  # pragma: no cover
            # Should never happen??
            birthtime = getattr(stat, "st_birthtime", None)
            return birthtime if birthtime is not None else stat.st_mtime

    @property
    def target_dt(self) -> dt.datetime:
        """Get the target datetime for TimeSpan compatibility."""
        if self._target_dt is None:
            # Lazy load the target datetime
            timestamp = self.timestamp
            if timestamp == 0:  # Handle nonexistent files
                self._target_dt = self._ref_dt
            else:
                self._target_dt = dt.datetime.fromtimestamp(timestamp)
        return self._target_dt

    @property
    def ref_dt(self) -> dt.datetime:
        """Get the reference datetime for TimeSpan compatibility."""
        return self._ref_dt

    @staticmethod
    def parse(time_str: str) -> dt.datetime:
        """
        Parse a time string and return a datetime object.

        Examples:
            "2023-12-25" -> datetime object for Dec 25, 2023
            "2023-12-25 14:30" -> datetime object for Dec 25, 2023 2:30 PM
            "2023-12-25T14:30:00" -> ISO format datetime
            "1640995200" -> datetime from Unix timestamp
        """
        time_str = time_str.strip()

        # Handle Unix timestamp (all digits)
        if time_str.isdigit():
            return dt.datetime.fromtimestamp(float(time_str))

        # Try common datetime formats
        formats = [
            "%Y-%m-%d",  # 2023-12-25
            "%Y-%m-%d %H:%M",  # 2023-12-25 14:30
            "%Y-%m-%d %H:%M:%S",  # 2023-12-25 14:30:00
            "%Y-%m-%dT%H:%M:%S",  # 2023-12-25T14:30:00 (ISO)
            "%Y-%m-%dT%H:%M:%SZ",  # 2023-12-25T14:30:00Z (ISO with Z)
            "%Y/%m/%d",  # 2023/12/25
            "%Y/%m/%d %H:%M",  # 2023/12/25 14:30
            "%m/%d/%Y",  # 12/25/2023
            "%m/%d/%Y %H:%M",  # 12/25/2023 14:30
        ]

        for fmt in formats:
            try:
                return dt.datetime.strptime(time_str, fmt)
            except ValueError:
                continue

        raise ValueError(f"Unable to parse time string: {time_str}")


__all__ = ["PathTime", "TimeType"]
