"""Utility functions for kokoro-tts-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from pathlib import Path


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text for display with ellipsis.

    Args:
        text: Text to truncate
        max_length: Maximum length before truncation

    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def expand_path(path_str: str) -> Path:
    """Expand ~ and environment variables in paths.

    Args:
        path_str: Path string with potential ~ or env vars

    Returns:
        Resolved absolute path
    """
    return Path(path_str).expanduser().resolve()


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string like "1.5s" or "1m 30s"
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes}m {secs:.0f}s"


def format_file_size(size_bytes: int) -> str:
    """Format file size to human readable string.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted string like "1.5 MB" or "350 KB"
    """
    if size_bytes >= 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    if size_bytes >= 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes} B"
