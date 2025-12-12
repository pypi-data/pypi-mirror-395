"""Tests for aws_polly_tts_tool.utils module.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from aws_polly_tts_tool.utils import (
    format_file_size,
    format_table_row,
    truncate_text,
    validate_output_format,
)


def test_validate_output_format() -> None:
    """Test output format validation and normalization."""
    assert validate_output_format("mp3") == "mp3"
    assert validate_output_format("MP3") == "mp3"
    assert validate_output_format("ogg_vorbis") == "ogg_vorbis"
    assert validate_output_format("ogg-vorbis") == "ogg_vorbis"
    assert validate_output_format("pcm") == "pcm"

    # Test invalid format
    try:
        validate_output_format("invalid")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Invalid output format" in str(e)


def test_truncate_text() -> None:
    """Test text truncation."""
    assert truncate_text("short") == "short"
    assert truncate_text("a" * 100, 20) == "a" * 20 + "..."
    assert len(truncate_text("a" * 100, 50)) == 53  # 50 + "..."


def test_format_table_row() -> None:
    """Test table row formatting."""
    result = format_table_row(["Name", "Age"], [10, 5])
    assert "Name" in result
    assert "Age" in result


def test_format_file_size() -> None:
    """Test file size formatting."""
    assert format_file_size(512) == "512 B"
    assert "KB" in format_file_size(2048)
    assert "MB" in format_file_size(2 * 1024 * 1024)
