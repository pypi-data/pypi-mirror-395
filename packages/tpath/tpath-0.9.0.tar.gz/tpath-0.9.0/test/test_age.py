"""
Test file for Age functionality (_age.py).
"""

import datetime as dt
import time

import pytest

from tpath import Age, TPath


def test_age_properties():
    """Test Age class properties."""
    ("Testing Age properties...")

    # Create a test file
    test_file = TPath("test_age_file.txt")
    test_file.write_text("Testing age functionality")

    try:
        age = test_file.age
        assert isinstance(age, Age)

        # Test that all time properties exist and return numbers
        assert isinstance(age.seconds, float)
        assert isinstance(age.minutes, float)
        assert isinstance(age.hours, float)
        assert isinstance(age.days, float)
        assert isinstance(age.weeks, float)
        assert isinstance(age.months, float)
        assert isinstance(age.years, float)

        # Test relationships between units
        assert age.minutes == pytest.approx(age.seconds / 60)
        assert age.hours == pytest.approx(age.minutes / 60)
        assert age.days == pytest.approx(age.hours / 24)
        assert age.weeks == pytest.approx(age.days / 7)

        (f"Age in seconds: {age.seconds:.2f}")
        (f"Age in minutes: {age.minutes:.6f}")
        (f"Age in hours: {age.hours:.8f}")
        (f"Age in days: {age.days:.10f}")
        (f"Age in weeks: {age.weeks:.10f}")

    finally:
        # Clean up
        if test_file.exists():
            test_file.unlink()


def test_age_with_custom_base_time():
    """Test Age calculations with custom base time."""

    # Create test file
    test_file = TPath("test_age_base_file.txt")
    test_file.write_text("Testing base time")

    try:
        # Test with yesterday as base time
        yesterday = dt.datetime.now() - dt.timedelta(days=1)
        path_with_base = TPath("test_age_base_file.txt").with_base_time(
            base_time=yesterday
        )

        age = path_with_base.age
        assert isinstance(age, Age)

        # The file should appear "older" when base time is in the past
        assert age.days < 0  # Negative because file is newer than base time

        # Test with future base time
        tomorrow = dt.datetime.now() + dt.timedelta(days=1)
        path_future = TPath("test_age_base_file.txt").with_base_time(base_time=tomorrow)
        future_age = path_future.age

        # File should appear "older" (more positive) with future base time
        assert future_age.days > age.days

    finally:
        # Clean up
        if test_file.exists():
            test_file.unlink()


def test_age_time_progression():
    """Test that age increases over time."""

    # Create test file
    test_file = TPath("test_age_progression.txt")
    test_file.write_text("Testing time progression")

    try:
        # Get initial age
        initial_age = test_file.age.seconds

        # Wait a longer time to ensure measurable difference
        time.sleep(0.2)

        # Create a new TPath instance to avoid caching
        test_file_new = TPath("test_age_progression.txt")
        later_age = test_file_new.age.seconds

        # Age should have increased
        assert later_age > initial_age

    finally:
        # Clean up
        if test_file.exists():
            test_file.unlink()


def test_different_time_types():
    """Test age calculation for different time types (ctime, mtime, atime)."""

    # Create test file
    test_file = TPath("test_time_types.txt")
    test_file.write_text("Testing different time types")

    try:
        # Test that we can get age from different time properties
        ctime_age = test_file.ctime.age
        mtime_age = test_file.mtime.age
        atime_age = test_file.atime.age

        assert isinstance(ctime_age, Age)
        assert isinstance(mtime_age, Age)
        assert isinstance(atime_age, Age)

    finally:
        # Clean up
        if test_file.exists():
            test_file.unlink()
