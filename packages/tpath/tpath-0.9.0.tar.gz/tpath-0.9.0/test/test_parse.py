#!/usr/bin/env python3
"""
Test parse methods for TPath properties using pytest fixtures.

This file tests the .parse() static methods on Size, Age, and Time classes
which enable parsing configuration strings into usable values.
"""

import pytest

from tpath import Age, PathTime, Size


@pytest.fixture
def size_test_cases():
    """
    Fixture providing test cases for Size.parse.

    Returns a list of tuples with input strings and expected byte values.
    """
    return [
        # (input_string, expected_bytes)
        ("100", 100),
        ("1024", 1024),
        # Decimal units (KB, MB, etc.)
        ("1KB", 1000),
        ("1MB", 1000000),
        ("2.5MB", 2500000),
        ("1GB", 1000000000),
        # Binary units (KiB, MiB, etc.)
        ("1KiB", 1024),
        ("1MiB", 1048576),
        ("1.5GiB", int(1.5 * 1024**3)),
        ("2TiB", 2 * 1024**4),
    ]


@pytest.fixture
def age_test_cases():
    """
    Fixture providing test cases for Age.parse.

    Returns a list of tuples with input strings and expected seconds values.
    """
    return [
        # (input_string, expected_seconds)
        ("30", 30.0),
        ("60", 60.0),
        # Minutes
        ("5m", 300.0),
        ("1min", 60.0),
        ("10minutes", 600.0),
        # Hours
        ("2h", 7200.0),
        ("1hour", 3600.0),
        ("3hours", 10800.0),
        # Days
        ("3d", 259200.0),
        ("1day", 86400.0),
        ("2days", 172800.0),
        # Weeks
        ("1w", 604800.0),
        ("2weeks", 1209600.0),
        # Months (approximate)
        ("1month", 2630016.0),
        ("2months", 5260032.0),
        # Years (approximate)
        ("1y", 31557600.0),
        ("2years", 63115200.0),
    ]


@pytest.fixture
def time_test_cases():
    """
    Fixture providing test cases for PathTime.parse.

    Returns a list of tuples with input strings and expected date/time components.
    """
    return [
        # (input_string, expected_year, expected_month, expected_day, expected_hour, expected_minute)
        ("2023-12-25", 2023, 12, 25, 0, 0),
        ("2023-12-25 14:30", 2023, 12, 25, 14, 30),
        ("2023-12-25 14:30:45", 2023, 12, 25, 14, 30),
        ("2023-12-25T14:30:00", 2023, 12, 25, 14, 30),
        ("2023/01/15", 2023, 1, 15, 0, 0),
        ("01/15/2023", 2023, 1, 15, 0, 0),
        ("01/15/2023 09:30", 2023, 1, 15, 9, 30),
    ]


@pytest.fixture
def config_examples():
    """Fixture providing realistic config file examples."""
    return {
        "cache_settings": {
            "max_file_size": "100MB",
            "cache_age_limit": "7d",
            "temp_file_limit": "1GB",
        },
        "backup_settings": {
            "retention_period": "30days",
            "max_backup_size": "10GiB",
            "cleanup_interval": "2h",
        },
        "log_settings": {
            "rotation_age": "1w",
            "max_log_size": "500MB",
            "archive_after": "1month",
        },
    }


def test_size_parse_cases(size_test_cases: list[tuple[str, int]]) -> None:
    """
    Test Size.parse with various input formats.

    Args:
        size_test_cases (list[tuple[str, int]]): List of (input, expected bytes) pairs.
    """
    # Act & Assert
    """Test Size.parse with various input formats."""
    for input_str, expected_bytes in size_test_cases:
        result = Size.parse(input_str)
        assert result == expected_bytes, (
            f"Failed for input '{input_str}': expected {expected_bytes}, got {result}"
        )


def test_size_parse_case_insensitive() -> None:
    """
    Test that Size.parse is case insensitive.
    """
    # Act & Assert
    """Test that Size.parse is case insensitive."""
    assert Size.parse("1kb") == Size.parse("1KB")
    assert Size.parse("1mib") == Size.parse("1MiB")
    assert Size.parse("2.5gb") == Size.parse("2.5GB")


def test_size_parse_whitespace_handling() -> None:
    """
    Test that Size.parse handles whitespace correctly.
    """
    # Act & Assert
    """Test that Size.parse handles whitespace correctly."""
    assert Size.parse(" 1MB ") == Size.parse("1MB")
    assert Size.parse("2.5 GB") == Size.parse("2.5GB")


def test_size_parse_invalid_input() -> None:
    """
    Test that Size.parse raises ValueError for invalid input.
    """
    # Act & Assert
    """Test that Size.parse raises ValueError for invalid input."""
    with pytest.raises(ValueError, match="Invalid size format"):
        Size.parse("invalid")

    with pytest.raises(ValueError, match="Unknown unit"):
        Size.parse("1XB")


def test_age_parse_cases(age_test_cases: list[tuple[str, float]]) -> None:
    """
    Test Age.parse with various input formats.

    Args:
        age_test_cases (list[tuple[str, float]]): List of (input, expected seconds) pairs.
    """
    # Act & Assert
    """Test Age.parse with various input formats."""
    for input_str, expected_seconds in age_test_cases:
        result = Age.parse(input_str)
        assert result == expected_seconds, (
            f"Failed for input '{input_str}': expected {expected_seconds}, got {result}"
        )


def test_age_parse_decimal_values() -> None:
    """
    Test Age.parse with decimal values.
    """
    # Act & Assert
    """Test Age.parse with decimal values."""
    assert Age.parse("2.5h") == 9000.0  # 2.5 hours = 9000 seconds
    assert Age.parse("1.5d") == 129600.0  # 1.5 days = 129600 seconds


def test_age_parse_case_insensitive() -> None:
    """
    Test that Age.parse is case insensitive.
    """
    # Act & Assert
    """Test that Age.parse is case insensitive."""
    assert Age.parse("1H") == Age.parse("1h")
    assert Age.parse("2DAYS") == Age.parse("2days")


def test_age_parse_invalid_input() -> None:
    """
    Test that Age.parse raises ValueError for invalid input.
    """
    # Act & Assert
    """Test that Age.parse raises ValueError for invalid input."""
    with pytest.raises(ValueError, match="Invalid age format"):
        Age.parse("invalid")

    with pytest.raises(ValueError, match="Unknown unit"):
        Age.parse("1x")


def test_time_parse_cases(
    time_test_cases: list[tuple[str, int, int, int, int, int]],
) -> None:
    """
    Test PathTime.parse with various date formats.

    Args:
        time_test_cases (list[tuple[str, int, int, int, int, int]]): List of (input, year, month, day, hour, minute) tuples.
    """
    # Act & Assert
    """Test PathTime.parse with various date formats."""
    for (
        input_str,
        expected_year,
        expected_month,
        expected_day,
        expected_hour,
        expected_minute,
    ) in time_test_cases:
        result = PathTime.parse(input_str)
        assert result.year == expected_year, f"Year mismatch for '{input_str}'"
        assert result.month == expected_month, f"Month mismatch for '{input_str}'"
        assert result.day == expected_day, f"Day mismatch for '{input_str}'"
        assert result.hour == expected_hour, f"Hour mismatch for '{input_str}'"
        assert result.minute == expected_minute, f"Minute mismatch for '{input_str}'"


def test_time_parse_unix_timestamp() -> None:
    """
    Test PathTime.parse with Unix timestamps.
    """
    # Act & Assert
    """Test PathTime.parse with Unix timestamps."""
    result = PathTime.parse("1640995200")  # Dec 31, 2021 16:00:00 local time
    assert result.year == 2021
    assert result.month == 12
    assert result.day == 31


def test_time_parse_invalid_input() -> None:
    """
    Test that PathTime.parse raises ValueError for invalid input.
    """
    # Act & Assert
    """Test that PathTime.parse raises ValueError for invalid input."""
    with pytest.raises(ValueError, match="Unable to parse time string"):
        PathTime.parse("invalid-date")

    with pytest.raises(ValueError, match="Unable to parse time string"):
        PathTime.parse("2023-13-40")  # Invalid month/day


def test_cache_config_parsing(config_examples: dict[str, dict[str, str]]) -> None:
    """
    Test parsing cache configuration values.

    Args:
        config_examples (dict): Example config dictionary.
    """
    # Act & Assert
    """Test parsing cache configuration values."""
    cache_config = config_examples["cache_settings"]

    max_size = Size.parse(cache_config["max_file_size"])
    age_limit = Age.parse(cache_config["cache_age_limit"])
    temp_limit = Size.parse(cache_config["temp_file_limit"])

    assert max_size == 100_000_000  # 100MB
    assert age_limit == 604_800.0  # 7 days in seconds
    assert temp_limit == 1_000_000_000  # 1GB


def test_backup_config_parsing(config_examples: dict[str, dict[str, str]]) -> None:
    """
    Test parsing backup configuration values.

    Args:
        config_examples (dict): Example config dictionary.
    """
    # Act & Assert
    """Test parsing backup configuration values."""
    backup_config = config_examples["backup_settings"]

    retention = Age.parse(backup_config["retention_period"])
    max_backup = Size.parse(backup_config["max_backup_size"])
    cleanup_interval = Age.parse(backup_config["cleanup_interval"])

    assert retention == 2_592_000.0  # 30 days in seconds
    assert max_backup == 10 * 1024**3  # 10 GiB
    assert cleanup_interval == 7200.0  # 2 hours in seconds


def test_log_config_parsing(config_examples: dict[str, dict[str, str]]) -> None:
    """
    Test parsing log configuration values.

    Args:
        config_examples (dict): Example config dictionary.
    """
    # Act & Assert
    """Test parsing log configuration values."""
    log_config = config_examples["log_settings"]

    rotation_age = Age.parse(log_config["rotation_age"])
    max_log_size = Size.parse(log_config["max_log_size"])
    archive_after = Age.parse(log_config["archive_after"])

    assert rotation_age == 604_800.0  # 1 week in seconds
    assert max_log_size == 500_000_000  # 500MB
    assert archive_after == 2_630_016.0  # 1 month in seconds


def test_mixed_config_scenarios() -> None:
    """
    Test various real-world config scenarios.
    """
    # Act & Assert
    """Test various real-world config scenarios."""
    scenarios = [
        # File cleanup scenarios
        ("1KB", "1h", 1000, 3600.0),
        ("50MB", "3d", 50_000_000, 259_200.0),
        ("2GiB", "1w", 2 * 1024**3, 604_800.0),
        # Backup scenarios
        ("100GB", "30days", 100_000_000_000, 2_592_000.0),
        ("5TiB", "1y", 5 * 1024**4, 31_557_600.0),
    ]

    for size_str, age_str, expected_size, expected_age in scenarios:
        parsed_size = Size.parse(size_str)
        parsed_age = Age.parse(age_str)

        assert parsed_size == expected_size, f"Size parsing failed for {size_str}"
        assert parsed_age == expected_age, f"Age parsing failed for {age_str}"
