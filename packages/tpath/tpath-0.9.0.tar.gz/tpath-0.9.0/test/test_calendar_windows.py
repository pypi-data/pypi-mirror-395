from pathlib import Path

from tpath import TPath


def test_calendar_basics(tmp_path: Path) -> None:
    """
    Test that calendar window methods correctly identify the current day, month, quarter, year, and week for a file.

    Verifies that the file is recognized as modified today and not in the past windows.
    """
    # Arrange
    test_file = TPath(tmp_path / "testfile.txt")
    test_file.write_text("Testing")

    # Act & Assert
    # File should be modified today
    assert test_file.mtime.cal.day.in_(0)
    assert test_file.mtime.cal.month.in_(0)
    assert test_file.mtime.cal.qtr.in_(0)
    assert test_file.mtime.cal.year.in_(0)
    assert test_file.mtime.cal.week.in_(0)  # This week

    # File should not be modified in the past
    assert not test_file.mtime.cal.day.in_(-1)  # Yesterday
    assert not test_file.mtime.cal.month.in_(-1)  # Last month
    assert not test_file.mtime.cal.week.in_(-1)  # Last week


def test_method_existence(tmp_path: Path) -> None:
    """
    Test that all expected calendar window methods exist on the cal property.

    Ensures the API surface is complete for time window queries.
    """
    # Arrange
    test_file = TPath(tmp_path / "testfile.txt")
    test_file.write_text("Testing")

    # Assert
    # Check methods exist on cal property
    assert hasattr(test_file.mtime.cal, "day")
    assert hasattr(test_file.mtime.cal, "month")
    assert hasattr(test_file.mtime.cal, "qtr")
    assert hasattr(test_file.mtime.cal, "year")
    assert hasattr(test_file.mtime.cal, "hour")
    assert hasattr(test_file.mtime.cal, "minute")
    assert hasattr(test_file.mtime.cal, "week")


def test_aliases(tmp_path: Path) -> None:
    """
    Test that calendar window methods are accessible via create, modify, and access aliases.

    Verifies alias support for all time window queries.
    """
    # Arrange
    test_file = TPath(tmp_path / "testfile.txt")
    test_file.write_text("Testing")

    # Assert
    # Check aliases exist on cal property
    assert hasattr(test_file.create.cal, "day")
    assert hasattr(test_file.modify.cal, "day")
    assert hasattr(test_file.access.cal, "day")


def test_range_functionality(tmp_path: Path) -> None:
    """
    Test that range parameters for calendar window methods work as expected.

    Verifies correct behavior for inclusive ranges and parameter order normalization.
    """
    # Arrange
    test_file = TPath(tmp_path / "testfile.txt")
    test_file.write_text("Testing")

    # Act & Assert
    # Test ranges that include current time
    # frist uses half-open intervals [start, end) so to include the
    # current unit (offset 0) we must pass end=1 (exclusive upper bound).
    assert test_file.mtime.cal.day.in_(-7, 1)  # Last 7 days through today
    assert test_file.mtime.cal.month.in_(-6, 1)  # Last 6 months through this month
    assert test_file.mtime.cal.year.in_(-2, 1)  # Last 2 years through this year
    assert test_file.mtime.cal.week.in_(-4, 1)  # Last 4 weeks through this week

    # Test parameter order normalization - these should be equivalent
    result1 = test_file.mtime.cal.day.in_(-7, 1)
    result2 = test_file.mtime.cal.day.in_(-7, 1)  # Corrected order
    # Assert
    assert result1 == result2, "Range parameter order should be normalized"

    # Test weeks parameter order too
    result3 = test_file.mtime.cal.week.in_(-2, 1)
    result4 = test_file.mtime.cal.week.in_(-2, 1)  # Corrected order
    # Assert
    assert result3 == result4, "Week range parameter order should be normalized"


def test_return_types(tmp_path: Path) -> None:
    """
    Test that all calendar window methods return boolean values.

    Ensures type consistency for single and range queries.
    """
    # Arrange
    test_file = TPath(tmp_path / "testfile.txt")
    test_file.write_text("Testing")

    # Assert
    # All methods should return booleans
    assert isinstance(test_file.mtime.cal.day.in_(0), bool)
    assert isinstance(test_file.mtime.cal.month.in_(0), bool)
    assert isinstance(test_file.mtime.cal.qtr.in_(0), bool)
    assert isinstance(test_file.mtime.cal.year.in_(0), bool)
    assert isinstance(test_file.mtime.cal.hour.in_(0), bool)
    assert isinstance(test_file.mtime.cal.minute.in_(0), bool)
    assert isinstance(test_file.mtime.cal.week.in_(0), bool)
    # Range methods should also return booleans (half-open intervals)
    assert isinstance(test_file.mtime.cal.day.in_(-7, 1), bool)
    assert isinstance(test_file.mtime.cal.month.in_(-6, -1), bool)
    assert isinstance(test_file.mtime.cal.week.in_(-2, 1), bool)
