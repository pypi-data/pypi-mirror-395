"""
Test file for TPath functionality.
"""

import datetime as dt
import os
import pathlib

import pytest

from tpath import Age, PathTime, Size, TPath


def test_tpath_file_operations(tmp_path: pathlib.Path) -> None:
    """
    Test basic TPath file operations.

    Args:
        tmp_path (Path): pytest temporary directory fixture.

    Verifies file creation, property access, and size/age calculations for TPath objects.
    """
    # Arrange
    test_content: str = "Hello, World! This is a test file for TPath."
    test_file: pathlib.Path = tmp_path / "test_file.txt"
    test_file.write_text(test_content)

    # Act
    tpath_file: TPath = TPath(test_file)
    expected_size: int = len(test_content.encode())
    actual_size: int = tpath_file.size.bytes

    # Assert
    assert tpath_file.exists()
    assert tpath_file.is_file()
    assert not tpath_file.is_dir()
    assert actual_size == expected_size
    assert tpath_file.size.kb == expected_size / 1000
    assert tpath_file.size.kib == expected_size / 1024
    assert tpath_file.age.seconds >= 0
    assert tpath_file.age.minutes >= 0
    assert tpath_file.age.hours >= 0
    assert tpath_file.age.days >= 0
    assert hasattr(tpath_file.ctime, "age")
    assert hasattr(tpath_file.mtime, "age")
    assert hasattr(tpath_file.atime, "age")


def test_tpath_with_base_time(tmp_path: pathlib.Path) -> None:
    """
    Test TPath with custom base time.

    Args:
        tmp_path (Path): pytest temporary directory fixture.

    Verifies that age calculations are correct when using a custom base time.
    """
    # Arrange
    test_file: pathlib.Path = tmp_path / "test_file.txt"
    test_file.write_text("test content")
    tpath_file: TPath = TPath(test_file)
    yesterday: dt.datetime = dt.datetime.now() - dt.timedelta(days=1)

    # Act
    old_path: TPath = tpath_file.with_base_time(yesterday)
    actual_days: float = old_path.age.days

    # Assert
    assert actual_days < 0
    assert abs(actual_days) >= 0.9  # Should be close to 1 day


@pytest.mark.parametrize(
    "size_str,expected_bytes",
    [
        ("100", 100),
        ("1KB", 1000),
        ("1KiB", 1024),
        ("2.5MB", 2500000),
        ("1.5GiB", 1610612736),  # 1.5 * 1024^3
        ("0.5TB", 500000000000),  # 0.5 * 1000^4
    ],
)
def test_size_parsing_valid(size_str: str, expected_bytes: int) -> None:
    """
    Test size string parsing with valid inputs.

    Args:
        size_str (str): Size string to parse.
        expected_bytes (int): Expected byte value.
    """
    # Act
    actual_bytes: int = Size.parse(size_str)
    # Assert
    assert actual_bytes == expected_bytes


@pytest.mark.parametrize(
    "invalid_size",
    [
        "invalid",
        "1.5.5MB",
        "5XYZ",
        "",
        "MB",
    ],
)
def test_size_parsing_invalid(invalid_size: str) -> None:
    """
    Test size string parsing with invalid inputs.

    Args:
        invalid_size (str): Invalid size string to parse.
    """
    # Act & Assert
    with pytest.raises(ValueError):
        Size.parse(invalid_size)


def test_pathlib_compatibility():
    """
    Test that TPath maintains pathlib.Path compatibility.

    Asserts that TPath and Path share core attributes and behaviors.
    """
    # Arrange
    tpath_obj: TPath = TPath(".")
    regular_path: pathlib.Path = pathlib.Path(".")

    # Assert
    assert tpath_obj.is_dir() == regular_path.is_dir()
    assert tpath_obj.absolute() == regular_path.absolute()
    assert tpath_obj.parent == regular_path.parent
    assert tpath_obj.name == regular_path.name
    assert isinstance(tpath_obj, pathlib.Path)


def test_tpath_extended_properties():
    """
    Test that TPath has extended properties not in regular Path.

    Asserts that TPath exposes additional file metadata properties.
    """
    # Arrange
    tpath_obj: TPath = TPath(".")
    regular_path: pathlib.Path = pathlib.Path(".")

    # Assert
    assert hasattr(tpath_obj, "size")
    assert hasattr(tpath_obj, "age")
    assert hasattr(tpath_obj, "ctime")
    assert hasattr(tpath_obj, "mtime")
    assert hasattr(tpath_obj, "atime")
    assert not hasattr(regular_path, "size")
    assert not hasattr(regular_path, "age")


def test_time_properties(tmp_path: pathlib.Path) -> None:
    """
    Test PathTime class properties.

    Verifies that PathTime properties exist and have correct types and age attributes.
    """

    # Arrange
    test_file: TPath = TPath(tmp_path / "test_time_file.txt")
    test_file.write_text("Testing time functionality")

    # Act
    ctime: PathTime = test_file.ctime
    mtime: PathTime = test_file.mtime
    atime: PathTime = test_file.atime

    # Assert
    assert isinstance(ctime, PathTime)
    assert isinstance(mtime, PathTime)
    assert isinstance(atime, PathTime)
    assert isinstance(ctime.age, Age)
    assert isinstance(mtime.age, Age)
    assert isinstance(atime.age, Age)


def test_time_timestamp_access(tmp_path: pathlib.Path) -> None:
    """Test Time timestamp property."""

    # Arrange
    test_file: TPath = TPath(tmp_path / "test_timestamp_file.txt")
    test_file.write_text("Testing timestamp access")

    # Act
    ctime: PathTime = test_file.ctime
    mtime: PathTime = test_file.mtime
    atime: PathTime = test_file.atime
    now: float = dt.datetime.now().timestamp()

    # Assert
    assert isinstance(ctime.timestamp, float)
    assert isinstance(mtime.timestamp, float)
    assert isinstance(atime.timestamp, float)
    assert abs(ctime.timestamp - now) < 60  # Within 1 minute
    assert abs(mtime.timestamp - now) < 60
    assert abs(atime.timestamp - now) < 60


def test_time_datetime_access(tmp_path: pathlib.Path) -> None:
    """Test Time datetime property."""

    # Arrange
    test_file: TPath = TPath(tmp_path / "test_datetime_file.txt")
    test_file.write_text("Testing datetime access")

    # Act
    ctime: PathTime = test_file.ctime
    mtime: PathTime = test_file.mtime
    atime: PathTime = test_file.atime
    now: dt.datetime = dt.datetime.now()
    time_diff: float = abs((ctime.target_dt - now).total_seconds())

    # Assert
    assert isinstance(ctime.target_dt, dt.datetime)
    assert isinstance(mtime.target_dt, dt.datetime)
    assert isinstance(atime.target_dt, dt.datetime)
    assert time_diff < 60  # Within 1 minute


def test_time_with_custom_base(tmp_path: pathlib.Path) -> None:
    """Test Time with custom base time."""

    # Arrange
    yesterday: dt.datetime = dt.datetime.now() - dt.timedelta(days=1)
    test_file: TPath = TPath(tmp_path / "test_base_time_file.txt").with_base_time(
        yesterday
    )
    test_file.write_text("Testing custom base time")

    # Act
    age: Age = test_file.ctime.age
    mtime_age: Age = test_file.mtime.age
    atime_age: Age = test_file.atime.age

    # Assert
    assert isinstance(age, Age)
    assert age.days < 0
    assert mtime_age.days < 0
    assert atime_age.days < 0


def test_time_nonexistent_file() -> None:
    """Test Time behavior with nonexistent files."""

    # Arrange
    nonexistent: TPath = TPath("nonexistent_file.txt")
    if nonexistent.exists():
        nonexistent.unlink()

    # Act
    ctime: PathTime = nonexistent.ctime
    mtime: PathTime = nonexistent.mtime
    atime: PathTime = nonexistent.atime

    # Assert
    assert isinstance(ctime, PathTime)
    assert isinstance(mtime, PathTime)
    assert isinstance(atime, PathTime)
    assert isinstance(ctime.age, Age)
    assert isinstance(mtime.age, Age)
    assert isinstance(atime.age, Age)
    assert ctime.timestamp == 0
    assert mtime.timestamp == 0
    assert atime.timestamp == 0


def test_target_dt_uses_ref_dt_for_nonexistent_file(tmp_path: pathlib.Path):
    """When the file doesn't exist timestamp == 0 and target_dt falls back to ref_dt."""

    # Arrange
    ref = dt.datetime(2025, 1, 1, 12, 0, 0)
    missing = tmp_path / "does_not_exist.txt"
    assert not missing.exists()

    # Act
    pt = PathTime(missing, "mtime", ref)

    # Assert
    assert pt.timestamp == 0
    assert pt.target_dt == ref
    # age should also reflect the ref time for nonexistent files
    assert pt.age.start_time == ref
    assert pt.age.end_time == ref


def test_tpath_with_real_dir_entry_scandir(tmp_path: pathlib.Path) -> None:
    """
    Supply real os.DirEntry objects via os.scandir to TPath and verify cached flags.

    Verifies that when dir_entry is provided TPath uses the cached values produced
    by the DirEntry methods (is_file, is_dir, is_symlink).
    """

    # Arrange
    file_path = tmp_path / "real.txt"
    file_path.write_text("content")
    dir_path = tmp_path / "adir"
    dir_path.mkdir()
    target = tmp_path / "target.txt"
    target.write_text("t")
    link = tmp_path / "alink"
    symlink_created = True
    try:
        link.symlink_to(target)
    except (OSError, NotImplementedError):
        symlink_created = False

    # Act
    with os.scandir(tmp_path) as it:
        entries = {entry.name: entry for entry in it}
    file_entry = entries[file_path.name]
    dir_entry = entries[dir_path.name]
    link_entry = entries.get(link.name) if symlink_created else None

    tp_file = TPath(file_path, dir_entry=file_entry)
    tp_dir = TPath(dir_path, dir_entry=dir_entry)
    tp_link = TPath(link, dir_entry=link_entry) if link_entry is not None else None

    # Assert - file entry
    assert tp_file.is_file() is file_entry.is_file(follow_symlinks=False)
    assert tp_file.is_dir() is file_entry.is_dir(follow_symlinks=False)
    assert tp_file.is_symlink() is file_entry.is_symlink()

    # Assert - dir entry
    assert tp_dir.is_dir() is dir_entry.is_dir(follow_symlinks=False)
    assert tp_dir.is_file() is dir_entry.is_file(follow_symlinks=False)
    assert tp_dir.is_symlink() is dir_entry.is_symlink()

    # Assert - symlink entry (only if created)
    if tp_link is not None:
        assert tp_link.is_symlink() is link_entry.is_symlink()
        assert tp_link.is_file() is link_entry.is_file(follow_symlinks=False)
        assert tp_link.is_dir() is link_entry.is_dir(follow_symlinks=False)
