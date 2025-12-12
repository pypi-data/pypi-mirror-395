"""
Shared utility functions for AWS Polly TTS tool.

Provides common functionality used across multiple modules,
including output formatting, validation, and helper functions.
Centralizing these utilities ensures consistency and reduces code
duplication across CLI commands and core modules.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""


def validate_output_format(format_name: str) -> str:
    """
    Validate and normalize audio output format.

    Ensures users specify valid Polly output formats before making
    API calls, providing clear error messages with available options.
    Normalizes input to lowercase for case-insensitive matching.

    Args:
        format_name: Output format to validate (case-insensitive)

    Returns:
        Normalized format name (lowercase with underscores)

    Raises:
        ValueError: If format is invalid with list of valid formats

    Example:
        >>> validate_output_format("MP3")
        'mp3'
        >>> validate_output_format("ogg-vorbis")
        'ogg_vorbis'
    """
    # WHY: Map user-friendly names to AWS API format identifiers
    format_map = {
        "mp3": "mp3",
        "ogg": "ogg_vorbis",
        "ogg_vorbis": "ogg_vorbis",
        "ogg-vorbis": "ogg_vorbis",
        "oggvorbis": "ogg_vorbis",
        "pcm": "pcm",
    }

    normalized = format_name.lower().strip().replace("-", "_")

    if normalized in format_map:
        return format_map[normalized]

    # Format not recognized
    valid_formats = "mp3, ogg_vorbis, pcm"
    raise ValueError(
        f"Invalid output format: '{format_name}'\n\n"
        f"Valid formats: {valid_formats}\n\n"
        f"Examples:\n"
        f"  --format mp3          # MP3 audio (default)\n"
        f"  --format ogg_vorbis   # Ogg Vorbis (open format)\n"
        f"  --format pcm          # Raw PCM audio (low latency)"
    )


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text for display with ellipsis.

    Provides consistent text truncation for log messages and output,
    preventing long texts from cluttering terminal display while still
    showing enough context to identify content.

    Args:
        text: Text to truncate
        max_length: Maximum length before truncation (default: 50)

    Returns:
        Truncated text with ellipsis if needed

    Example:
        >>> truncate_text("This is a very long sentence that needs truncating", 20)
        'This is a very lo...'
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def format_table_row(columns: list[str], widths: list[int]) -> str:
    """
    Format a table row with fixed column widths.

    Provides consistent table formatting across CLI output,
    ensuring aligned columns for readable voice/engine listings.

    Args:
        columns: List of column values
        widths: List of column widths (must match columns length)

    Returns:
        Formatted row string

    Example:
        >>> format_table_row(["Name", "Age", "City"], [15, 5, 10])
        'Name            Age   City      '
    """
    if len(columns) != len(widths):
        raise ValueError("Number of columns must match number of widths")

    # WHY: Left-align text in fixed-width columns for readability
    formatted = []
    for col, width in zip(columns, widths):
        formatted.append(f"{col:<{width}}")

    return " ".join(formatted)


def format_file_size(bytes_count: int) -> str:
    """
    Format byte count as human-readable file size.

    Makes audio file sizes easier to understand by converting
    bytes to appropriate units (KB, MB) for user display.

    Args:
        bytes_count: Number of bytes

    Returns:
        Formatted size string (e.g., "1.5 MB")

    Example:
        >>> format_file_size(1536000)
        '1.5 MB'
        >>> format_file_size(512)
        '512 B'
    """
    if bytes_count < 1024:
        return f"{bytes_count} B"
    elif bytes_count < 1024 * 1024:
        return f"{bytes_count / 1024:.1f} KB"
    else:
        return f"{bytes_count / (1024 * 1024):.1f} MB"
