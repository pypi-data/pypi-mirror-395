"""
Tests for favicon module.
"""

import pytest
from pathlib import Path


def test_web_module_imports():
    """Test that web module can be imported."""
    from super_pocket.web import convert_to_favicon, DEFAULT_FAVICON_SIZES

    assert callable(convert_to_favicon)
    assert isinstance(DEFAULT_FAVICON_SIZES, list)
    assert len(DEFAULT_FAVICON_SIZES) == 6


def test_favicon_default_sizes():
    """Test that default favicon sizes are correct."""
    from super_pocket.web import DEFAULT_FAVICON_SIZES

    expected_sizes = [
        (256, 256),
        (128, 128),
        (64, 64),
        (48, 48),
        (32, 32),
        (16, 16)
    ]

    assert DEFAULT_FAVICON_SIZES == expected_sizes


def test_favicon_converter_file_not_found(temp_dir):
    """Test that converter raises FileNotFoundError for non-existent files."""
    from super_pocket.web.favicon import convert_to_favicon

    input_file = temp_dir / "nonexistent.png"
    output_file = temp_dir / "favicon.ico"

    with pytest.raises(FileNotFoundError):
        convert_to_favicon(input_file, output_file)


def test_favicon_converter_invalid_output_extension(temp_dir):
    """Test that converter raises ValueError for non-.ico output."""
    from super_pocket.web.favicon import convert_to_favicon

    # Create a dummy input file
    input_file = temp_dir / "test.png"
    input_file.write_text("dummy", encoding='utf-8')
    output_file = temp_dir / "output.png"  # Wrong extension

    with pytest.raises(ValueError, match=".ico extension"):
        convert_to_favicon(input_file, output_file)


# Note: Full conversion tests require Pillow dependency
# These are skipped if Pillow is not installed
