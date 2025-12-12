"""
Test file for TPath access properties.
"""

import platform
from pathlib import Path

from tpath import TPath


def test_basic_access_properties(tmp_path: Path) -> None:
    """Test basic access properties (readable, writable, executable)."""
    # Arrange
    test_file_path = tmp_path / "test_basic_access.txt"
    test_file_path.write_text("Test content")
    test_file = TPath(test_file_path)

    # Assert
    assert isinstance(test_file.readable, bool)
    assert isinstance(test_file.writable, bool)
    assert isinstance(test_file.executable, bool)
    assert test_file.readable is True
    assert test_file.writable is True
    if platform.system() == "Windows":
        assert test_file.executable is True


def test_derived_access_properties(tmp_path: Path) -> None:
    """Test derived access properties (read_only, write_only, read_write)."""
    # Arrange
    test_file_path = tmp_path / "test_derived_access.txt"
    test_file_path.write_text("Test content")
    test_file = TPath(test_file_path)

    # Assert
    assert isinstance(test_file.read_only, bool)
    assert isinstance(test_file.write_only, bool)
    assert isinstance(test_file.read_write, bool)
    assert test_file.read_write is True
    assert test_file.read_only is False
    assert test_file.write_only is False


def test_access_mode_method(tmp_path: Path) -> None:
    """Test the access_mode method."""
    # Arrange
    test_file_path = tmp_path / "test_access_mode.txt"
    test_file_path.write_text("Test content")
    test_file = TPath(test_file_path)

    # Assert
    assert test_file.access_mode("R") is True
    assert test_file.access_mode("W") is True
    assert test_file.access_mode("RW") is True
    assert test_file.access_mode("RO") is False  # Not read-only
    assert test_file.access_mode("WO") is False  # Not write-only
    assert test_file.access_mode("r") is True
    assert test_file.access_mode("rw") is True
    exec_result = test_file.access_mode("X")
    assert isinstance(exec_result, bool)
    if platform.system() == "Windows":
        assert exec_result is True
    try:
        test_file.access_mode("INVALID")
        raise AssertionError("Should have raised ValueError")
    except ValueError:
        pass  # Expected


def test_nonexistent_file_access():
    """Test access properties on nonexistent files."""
    ("Testing access properties on nonexistent files...")

    # Create a path to a file that doesn't exist
    nonexistent = TPath("nonexistent_file_for_access_testing.txt")

    # Make sure it doesn't exist
    if nonexistent.exists():
        nonexistent.unlink()

    # Access properties should all return False for nonexistent files
    assert nonexistent.readable is False
    assert nonexistent.writable is False
    assert nonexistent.executable is False
    assert nonexistent.read_only is False
    assert nonexistent.write_only is False
    assert nonexistent.read_write is False

    ("✅ Nonexistent file access tests passed")


def test_access_stat_caching(tmp_path: Path) -> None:
    """Test that access properties work with stat caching."""
    # Arrange
    test_file_path = tmp_path / "test_access_stat.txt"
    test_file_path.write_text("Test content")
    test_file = TPath(test_file_path)

    # Act
    readable1 = test_file.readable
    writable1 = test_file.writable
    readable2 = test_file.readable
    writable2 = test_file.writable

    # Assert
    assert readable1 == readable2
    assert writable1 == writable2


def test_property_access(tmp_path: Path) -> None:
    """Test that all access properties are accessible."""
    # Arrange
    test_file_path = tmp_path / "test_access.txt"
    test_file_path.write_text("Test content")

    test_file = TPath(test_file_path)

    # Assert
    assert hasattr(test_file, "readable")
    assert hasattr(test_file, "writable")
    assert hasattr(test_file, "executable")
    assert hasattr(test_file, "read_only")
    assert hasattr(test_file, "write_only")
    assert hasattr(test_file, "read_write")
    assert hasattr(test_file, "owner_readable")
    assert hasattr(test_file, "owner_writable")
    assert hasattr(test_file, "owner_executable")
    assert callable(test_file.access_mode)
