"""
Test file for Size functionality (_size.py).
"""

from pathlib import Path

import pytest

from tpath import Size, TPath


def test_size_properties(tmp_path: Path) -> None:
    """
    Test Size class properties and conversions.

    Verifies that Size properties and unit conversions are correct for a test file.
    """
    # Arrange
    test_file: TPath = TPath(tmp_path / "test_size_file.txt")
    content: str = "Hello, World! This is a test file for size testing."
    test_file.write_text(content)

    # Act
    size: Size = test_file.size
    expected_bytes: int = len(content.encode("utf-8"))
    actual_bytes: int = size.bytes

    # Assert
    assert isinstance(size, Size), (
        f"Expected size to be Size instance, got {type(size)}"
    )
    assert isinstance(size.bytes, int), (
        f"Expected size.bytes to be int, got {type(size.bytes)}"
    )
    assert actual_bytes > 0, f"Expected size.bytes to be positive, got {actual_bytes}"
    assert isinstance(size.b, int), f"Expected size.b to be int, got {type(size.b)}"
    assert size.b == actual_bytes, (
        f"Expected size.b ({size.b}) to equal size.bytes ({actual_bytes})"
    )
    assert actual_bytes == expected_bytes, (
        f"Expected size.bytes ({actual_bytes}) to equal content length ({expected_bytes})"
    )
    assert isinstance(size.kb, float), (
        f"Expected size.kb to be float, got {type(size.kb)}"
    )
    assert isinstance(size.mb, float), (
        f"Expected size.mb to be float, got {type(size.mb)}"
    )
    assert isinstance(size.gb, float), (
        f"Expected size.gb to be float, got {type(size.gb)}"
    )
    assert isinstance(size.tb, float), (
        f"Expected size.tb to be float, got {type(size.tb)}"
    )
    assert isinstance(size.pb, float), (
        f"Expected size.pb to be float, got {type(size.pb)}"
    )
    assert isinstance(size.kib, float), (
        f"Expected size.kib to be float, got {type(size.kib)}"
    )
    assert isinstance(size.mib, float), (
        f"Expected size.mib to be float, got {type(size.mib)}"
    )
    assert isinstance(size.gib, float), (
        f"Expected size.gib to be float, got {type(size.gib)}"
    )
    assert isinstance(size.tib, float), (
        f"Expected size.tib to be float, got {type(size.tib)}"
    )
    assert isinstance(size.pib, float), (
        f"Expected size.pib to be float, got {type(size.pib)}"
    )
    assert abs(size.kb - actual_bytes / 1000) < 1e-10, (
        f"KB conversion incorrect: {size.kb} vs {actual_bytes / 1000}"
    )
    assert abs(size.mb - actual_bytes / (1000 * 1000)) < 1e-10, (
        f"MB conversion incorrect: {size.mb} vs {actual_bytes / (1000 * 1000)}"
    )
    assert abs(size.kib - actual_bytes / 1024) < 1e-10, (
        f"KiB conversion incorrect: {size.kib} vs {actual_bytes / 1024}"
    )
    assert abs(size.mib - actual_bytes / (1024 * 1024)) < 1e-10, (
        f"MiB conversion incorrect: {size.mib} vs {actual_bytes / (1024 * 1024)}"
    )


@pytest.mark.parametrize(
    "size_str,expected_bytes",
    [
        ("100", 100),
        ("1KB", 1000),
        ("1KiB", 1024),
        ("2.5MB", 2_500_000),
        ("1.5GiB", int(1.5 * 1024 * 1024 * 1024)),
        ("0.5TB", 500_000_000_000),
        ("2TiB", 2 * 1024 * 1024 * 1024 * 1024),
        ("0.001PB", 1_000_000_000_000),
        ("1PIB", 1024 * 1024 * 1024 * 1024 * 1024),
    ],
)
def test_size_string_parsing(size_str: str, expected_bytes: int) -> None:
    """Test Size.parse() method for parsing size strings."""
    # Arrange - parameters provided by pytest

    # Act
    result = Size.parse(size_str)

    # Assert
    assert result == expected_bytes, (
        f"Expected {expected_bytes}, got {result} for {size_str}"
    )


@pytest.mark.parametrize(
    "invalid_str",
    [
        "invalid",
        "123XB",
        "",
        "1.2.3MB",
        "-100MB",
    ],
)
def test_size_string_parsing_errors(invalid_str: str) -> None:
    """Test Size.parse() error handling."""
    # Arrange - parameter provided by pytest

    # Act & Assert
    with pytest.raises(ValueError):
        Size.parse(invalid_str)


def test_size_edge_cases(tmp_path: Path) -> None:
    """Test Size class with edge cases."""
    # Arrange - Test zero size file
    zero_file: TPath = TPath(tmp_path / "zero_size_test.txt")
    zero_file.write_text("")  # Empty file

    # Act
    zero_size: Size = zero_file.size

    # Assert
    assert zero_size.bytes == 0, (
        f"Expected zero size file to have 0 bytes, got {zero_size.bytes}"
    )
    assert zero_size.kb == 0, (
        f"Expected zero size file to have 0 KB, got {zero_size.kb}"
    )
    assert zero_size.mb == 0, (
        f"Expected zero size file to have 0 MB, got {zero_size.mb}"
    )

    # Arrange - Test large size calculation
    large_content: str = "x" * 1000000  # 1MB of content
    large_file: TPath = TPath(tmp_path / "large_size_test.txt")
    large_file.write_text(large_content)

    # Act
    large_size: Size = large_file.size

    # Assert
    assert large_size.bytes == 1000000, (
        f"Expected large file to have 1000000 bytes, got {large_size.bytes}"
    )
    assert abs(large_size.mb - 1.0) < 0.001, (
        f"Expected large file to be close to 1MB, got {large_size.mb:.3f} MB"
    )

    # Arrange - Test parse method with large values
    huge_tb_str: str = "5TB"

    # Act
    huge_size: int = Size.parse(huge_tb_str)

    # Assert
    assert huge_size > 4 * 1024**4, (
        f"Expected huge size to be > 4TB in bytes, got {huge_size} bytes"
    )


def test_size_comparison(tmp_path: Path) -> None:
    """Test Size comparison functionality."""
    # Arrange - Create files of different sizes
    small_file: TPath = TPath(tmp_path / "test_small.txt")
    large_file: TPath = TPath(tmp_path / "test_large.txt")

    small_file.write_text("small")
    large_file.write_text("This is a much larger file with more content")

    # Act
    small_size: Size = small_file.size
    large_size: Size = large_file.size
    min_size_bytes: int = Size.parse("3")  # 3 bytes (smaller than our test files)

    # Assert
    assert large_size.bytes > small_size.bytes, (
        f"Expected large file ({large_size.bytes} bytes) to be larger than small file ({small_size.bytes} bytes)"
    )
    assert large_size.bytes > min_size_bytes, (
        f"Expected large file ({large_size.bytes} bytes) to be larger than minimum size ({min_size_bytes} bytes)"
    )
    assert small_size.bytes > min_size_bytes, (
        f"Expected small file ({small_size.bytes} bytes) to be larger than minimum size ({min_size_bytes} bytes)"
    )
