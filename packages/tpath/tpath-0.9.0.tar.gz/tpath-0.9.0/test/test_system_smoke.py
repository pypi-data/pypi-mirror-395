"""
Comprehensive end-to-end system test for TPath.

This test creates diverse files and validates TPath functionality
across multiple dimensions: file types, sizes, ages, and time scenarios.
"""

import os
import time
from pathlib import Path
from typing import Any

from tpath import TPath


def test_comprehensive_system_smoke(tmp_path: Path) -> None:
    """
    Comprehensive system smoke test covering multiple TPath features.

    Args:
        tmp_path (Path): pytest temporary directory fixture.

    Creates files with different extensions, sizes, and timestamps, then validates filtering and property access across all scenarios.
    """
    # Arrange
    test_dir: Path = tmp_path
    created_files: list[TPath] = []
    extensions: list[str] = [".txt", ".py", ".json", ".md", ".log"]
    sizes: list[int] = [0, 100, 1024, 10240]  # 0B, 100B, 1KB, 10KB
    time_offsets: list[int] = [0, -3600, -86400]  # now, 1hr ago, 1day ago
    file_specs: list[dict[str, Any]] = []

    # Act
    for ext in extensions:
        for size in sizes:
            for offset in time_offsets:
                file_name: str = f"test_{len(file_specs):03d}{ext}"
                file_path: TPath = TPath(test_dir / file_name)
                if size == 0:
                    file_path.touch()
                else:
                    content: str = "x" * size
                    file_path.write_text(content)
                timestamp: float = time.time() + offset
                os.utime(file_path, (timestamp, timestamp))
                created_files.append(file_path)
                file_specs.append(
                    {
                        "path": file_path,
                        "extension": ext,
                        "size": size,
                        "offset": offset,
                    }
                )

    # Assert
    # --- Size-based filtering ---
    empty_files: list[TPath] = [f for f in created_files if f.size.bytes == 0]
    small_files: list[TPath] = [f for f in created_files if 0 < f.size.bytes <= 1024]
    large_files: list[TPath] = [f for f in created_files if f.size.bytes > 1024]

    expected_empty: int = len([s for s in file_specs if s["size"] == 0])
    expected_small: int = len([s for s in file_specs if 0 < s["size"] <= 1024])
    expected_large: int = len([s for s in file_specs if s["size"] > 1024])

    assert len(empty_files) == expected_empty
    assert len(small_files) == expected_small
    assert len(large_files) == expected_large

    expected_empty: int = len([s for s in file_specs if s["size"] == 0])
    expected_small: int = len([s for s in file_specs if 0 < s["size"] <= 1024])
    expected_large: int = len([s for s in file_specs if s["size"] > 1024])

    assert len(empty_files) == expected_empty
    assert len(small_files) == expected_small
    assert len(large_files) == expected_large

    # Test 3: Extension-based filtering
    for ext in extensions:
        ext_files: list[TPath] = [f for f in created_files if f.suffix == ext]
        expected_count: int = len([s for s in file_specs if s["extension"] == ext])
        assert len(ext_files) == expected_count

    # Test 4: Time property access
    for file_path in created_files:
        # All time properties should be accessible
        assert isinstance(file_path.ctime.timestamp, float)
        assert isinstance(file_path.mtime.timestamp, float)
        assert isinstance(file_path.atime.timestamp, float)

        # Aliases should work
        assert file_path.create.timestamp == file_path.ctime.timestamp
        assert file_path.modify.timestamp == file_path.mtime.timestamp
        assert file_path.access.timestamp == file_path.atime.timestamp

    # Test 5: Age calculations
    for file_path in created_files:
        age = file_path.age
        assert isinstance(age.seconds, float)
        assert isinstance(age.minutes, float)
        assert isinstance(age.hours, float)
        assert isinstance(age.days, float)
        # Age can be slightly negative due to clock precision, so allow small negative values
        assert age.seconds >= -1  # Should be approximately positive (file age)

    # Test 6: Calendar filtering
    for file_path in created_files:
        # All files should be in current time periods
        assert file_path.mtime.cal.year.in_(0)  # This year
        assert file_path.mtime.cal.month.in_(0)  # This month

        # Today check depends on when files were created
        # (Some might be from "yesterday" due to offset)
        calendar_result: bool = file_path.mtime.cal.day.in_(0)
        assert isinstance(calendar_result, bool)

    # Test 7: Size conversions
    for file_path in created_files:
        size = file_path.size
        assert size.kb == size.bytes / 1000
        assert size.mb == size.bytes / 1000000
        assert size.gb == size.bytes / 1000000000
        assert size.kib == size.bytes / 1024
        assert size.mib == size.bytes / (1024 * 1024)

    # Test 8: Complex filtering combinations
    python_files: list[TPath] = [f for f in created_files if f.suffix == ".py"]

    # Verify combinations work
    assert len(python_files) > 0
    # Test 9: Calendar range filtering
    for file_path in created_files:
        # Test range functionality (frist uses half-open intervals)
        last_week: bool = file_path.mtime.cal.day.in_(
            -7, 1
        )  # Last 7 days through today (exclusive end)
        last_month: bool = file_path.mtime.cal.month.in_(
            -1, 1
        )  # Last month through this month (exclusive end)

        assert isinstance(last_week, bool)
        assert isinstance(last_month, bool)

    # Test 10: Access control properties (Windows and Unix compatible)
    for file_path in created_files:
        # Basic access properties should always be accessible
        assert isinstance(file_path.readable, bool)
        assert isinstance(file_path.writable, bool)
        assert isinstance(file_path.executable, bool)

        # Derived access properties
        assert isinstance(file_path.read_only, bool)
        assert isinstance(file_path.write_only, bool)
        assert isinstance(file_path.read_write, bool)

        # Files we created should be readable and writable
        assert file_path.readable is True
        assert file_path.writable is True

        # Read-write check (should be True since we can read and write)
        assert file_path.read_write is True

        # Read-only and write-only should be False for our test files
        assert file_path.read_only is False
        assert file_path.write_only is False

    # Test 11: Access mode method
    for file_path in created_files:
        # Test various access mode specifications
        assert file_path.access_mode("R") is True  # Should be readable
        assert file_path.access_mode("W") is True  # Should be writable
        assert file_path.access_mode("RW") is True  # Should be read-write
        assert file_path.access_mode("RO") is False  # Should not be read-only
        assert file_path.access_mode("WO") is False  # Should not be write-only

        # Test case insensitive
        assert file_path.access_mode("r") is True
        assert file_path.access_mode("rw") is True

        # Executable depends on platform
        executable_result: bool = file_path.access_mode("X")
        assert isinstance(executable_result, bool)

        # On Windows, files are typically executable if they exist
        # On Unix, depends on actual permissions
        if os.name == "nt":  # Windows
            assert executable_result is True
        # On Unix, we don't assert a specific value since it depends on umask

    # Test 12: Owner permission properties (Unix-specific but safe on Windows)
    for file_path in created_files:
        # These should return boolean values on all platforms
        assert isinstance(file_path.owner_readable, bool)
        assert isinstance(file_path.owner_writable, bool)
        assert isinstance(file_path.owner_executable, bool)

        # Files we created should have owner read/write permissions
        assert file_path.owner_readable is True
        assert file_path.owner_writable is True

        # Owner executable depends on platform and file type
        owner_exec: bool = file_path.owner_executable
        assert isinstance(owner_exec, bool)

        # On Windows, should be True for existing files
        if os.name == "nt":
            assert owner_exec is True

    # Test 14: Stat property access and ctime fix validation
    for file_path in created_files:
        stat_result: os.stat_result = file_path.stat()

        # Basic stat properties should be accessible
        assert hasattr(stat_result, "st_size")
        assert hasattr(stat_result, "st_mtime")
        assert hasattr(stat_result, "st_atime")
        assert hasattr(stat_result, "st_ctime")

        # Size should match
        assert stat_result.st_size == file_path.size.bytes

        # Times should be accessible (using mtime which is universally supported)
        mtime_from_stat: float = stat_result.st_mtime
        mtime_from_property: float = file_path.mtime.timestamp
        assert isinstance(mtime_from_stat, float)
        assert isinstance(mtime_from_property, float)
