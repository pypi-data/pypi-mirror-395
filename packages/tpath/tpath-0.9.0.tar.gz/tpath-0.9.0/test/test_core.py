"""
Test file for TPath core functionality (_core.py).
"""

import datetime as dt
from pathlib import Path

from tpath import Age, PathTime, Size, TPath


def test_tpath_creation():
    """
    Test TPath object creation and initialization.

    Verifies that TPath can be created and initialized with default and custom base times.
    """

    # Arrange
    path1 = TPath("test_file.txt")
    custom_time = dt.datetime(2023, 1, 1)

    # Act
    path2 = TPath("test_file.txt").with_base_time(custom_time)

    # Assert
    assert isinstance(path1, TPath)
    assert str(path1) == "test_file.txt"
    assert path2._base_time == custom_time


def test_pathlib_compatibility():
    """
    Test that TPath maintains pathlib.Path compatibility.

    Verifies that TPath supports common Path methods and properties.
    """

    # Arrange
    tpath_obj = TPath(".")
    regular_path = Path(".")

    # Assert
    assert tpath_obj.is_dir() == regular_path.is_dir()
    assert str(tpath_obj.absolute()) == str(regular_path.absolute())
    assert tpath_obj.name == regular_path.name
    assert tpath_obj.suffix == regular_path.suffix


def test_property_access():
    """
    Test that TPath properties are accessible and have correct types.

    Verifies that TPath exposes age, size, and time properties with expected types.
    """

    # Arrange
    test_file = TPath("test_file.txt")
    test_file.write_text("Hello, World!")

    try:
        # Assert
        assert hasattr(test_file, "age")
        assert hasattr(test_file, "size")
        assert hasattr(test_file, "ctime")
        assert hasattr(test_file, "mtime")
        assert hasattr(test_file, "atime")

        assert isinstance(test_file.age, Age)
        assert isinstance(test_file.size, Size)
        assert isinstance(test_file.ctime, PathTime)
        assert isinstance(test_file.mtime, PathTime)
        assert isinstance(test_file.atime, PathTime)

    finally:
        # Clean up
        if test_file.exists():
            test_file.unlink()
