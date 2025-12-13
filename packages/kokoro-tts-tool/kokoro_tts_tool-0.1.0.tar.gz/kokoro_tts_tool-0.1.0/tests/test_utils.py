"""Tests for kokoro_tts_tool.utils module.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from kokoro_tts_tool.utils import (
    expand_path,
    format_duration,
    format_file_size,
    truncate_text,
)


def test_truncate_text_short() -> None:
    """Test that short text is not truncated."""
    result = truncate_text("Hello", max_length=50)
    assert result == "Hello"


def test_truncate_text_long() -> None:
    """Test that long text is truncated with ellipsis."""
    long_text = "A" * 100
    result = truncate_text(long_text, max_length=50)
    assert len(result) == 53  # 50 + "..."
    assert result.endswith("...")


def test_truncate_text_exact() -> None:
    """Test text at exact limit is not truncated."""
    exact_text = "A" * 50
    result = truncate_text(exact_text, max_length=50)
    assert result == exact_text
    assert not result.endswith("...")


def test_expand_path_home() -> None:
    """Test that ~ is expanded to home directory."""
    from pathlib import Path

    result = expand_path("~/test")
    assert str(result).startswith(str(Path.home()))
    assert "~" not in str(result)


def test_format_duration_seconds() -> None:
    """Test duration formatting for short durations."""
    assert format_duration(1.5) == "1.5s"
    assert format_duration(30.0) == "30.0s"
    assert format_duration(59.9) == "59.9s"


def test_format_duration_minutes() -> None:
    """Test duration formatting for longer durations."""
    assert format_duration(90.0) == "1m 30s"
    assert format_duration(120.0) == "2m 0s"


def test_format_file_size_bytes() -> None:
    """Test file size formatting for small sizes."""
    assert format_file_size(500) == "500 B"


def test_format_file_size_kb() -> None:
    """Test file size formatting for kilobytes."""
    assert format_file_size(1500) == "1.5 KB"


def test_format_file_size_mb() -> None:
    """Test file size formatting for megabytes."""
    assert format_file_size(1500000) == "1.4 MB"


def test_format_file_size_gb() -> None:
    """Test file size formatting for gigabytes."""
    assert format_file_size(1500000000) == "1.4 GB"
