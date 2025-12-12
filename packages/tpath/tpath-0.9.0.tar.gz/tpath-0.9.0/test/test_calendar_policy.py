"""
test_calendar_policy.py

Tests for TPath calendar policy integration, including custom workweek, fiscal year start, and holidays.

Follows AAA pattern, Google-style docstrings, and type hints.
"""

import os
from datetime import datetime
from pathlib import Path

import pytest
from frist import Biz, BizPolicy

from tpath import TPath


@pytest.mark.parametrize(
    "filename, atime, expected_fiscal_year, expected_fiscal_quarter, expected_is_business_day, expected_is_holiday",
    [
        (
            "file_2025-01-01.txt",
            datetime(2025, 1, 1, 12, 0, 0),
            2024,
            4,
            False,
            True,
        ),  # Jan 1, 2025: New Year's Day, holiday, Q4
        (
            "file_2025-04-07.txt",
            datetime(2025, 4, 7, 12, 0, 0),
            2025,
            1,
            True,
            False,
        ),  # Apr 7, 2025: Monday, Q1, business day
        (
            "file_2025-04-11.txt",
            datetime(2025, 4, 11, 12, 0, 0),
            2025,
            1,
            False,
            False,
        ),  # Apr 11, 2025: Friday, not business day
        (
            "file_2025-07-01.txt",
            datetime(2025, 7, 1, 12, 0, 0),
            2025,
            2,
            True,
            False,
        ),  # Jul 1, 2025: Tuesday, Q2, business day
        (
            "file_2025-12-31.txt",
            datetime(2025, 12, 31, 12, 0, 0),
            2025,
            3,
            True,
            False,
        ),  # Dec 31, 2025: Wednesday, Q3, business day
    ],
)
def test_calendar_policy_integration(
    tmp_path: Path,
    filename: str,
    atime: datetime,
    expected_fiscal_year: int,
    expected_fiscal_quarter: int,
    expected_is_business_day: bool,
    expected_is_holiday: bool,
) -> None:
    """
    Test TPath and BizPolicy integration for custom calendar logic.

    Args:
        tmp_path: pytest fixture for temporary directory.
        filename: Name of the file to create.
        atime: Simulated access time (epoch seconds).
        expected_fiscal_quarter: Expected fiscal quarter for the date.
        expected_is_business_day: Whether the date is a business day.
        expected_is_holiday: Whether the date is a holiday.
    """
    # Arrange

    # Arrange: Custom calendar policy (Mon–Thu workweek, fiscal year starts in April, New Year's Day holiday)
    custom_policy = BizPolicy(
        workdays=[0, 1, 2, 3],  # Mon–Thu (0=Mon)
        fiscal_year_start_month=4,  # April
        holidays={"2025-01-01"},  # New Year's Day as YYYY-MM-DD string
    )

    file_path = tmp_path / filename
    file_path.write_text("test")

    # Use atime as a datetime object, convert to timestamp for os.utime
    atime_ts = atime.timestamp()
    os.utime(file_path, (atime_ts, atime_ts))

    # Act
    tpath_file: TPath = TPath(file_path, cal_policy=custom_policy)

    biz: Biz = tpath_file.atime.biz

    actual_fiscal_year: int = biz.fiscal_year
    actual_fiscal_quarter: int = biz.fiscal_quarter
    actual_is_business_day: bool = custom_policy.is_business_day(biz.target_dt)
    actual_is_holiday: bool = biz.holiday

    # Assert
    assert actual_fiscal_year == expected_fiscal_year, (
        f"Fiscal year mismatch for {filename}: expected {expected_fiscal_year}, got {actual_fiscal_year}"
    )
    assert actual_fiscal_quarter == expected_fiscal_quarter, (
        f"Fiscal quarter mismatch for {filename}: expected {expected_fiscal_quarter}, got {actual_fiscal_quarter}"
    )
    assert actual_is_business_day is expected_is_business_day, (
        f"Business day mismatch for {filename}: expected {expected_is_business_day}, got {actual_is_business_day}"
    )
    assert actual_is_holiday is expected_is_holiday, (
        f"Holiday mismatch for {filename}: expected {expected_is_holiday}, got {actual_is_holiday}"
    )
