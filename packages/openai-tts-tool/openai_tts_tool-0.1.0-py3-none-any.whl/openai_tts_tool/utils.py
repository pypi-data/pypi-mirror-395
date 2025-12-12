"""Utility functions for openai-tts-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""


def truncate_text(text: str, max_len: int) -> str:
    """Truncate text to a maximum length for CLI display.

    Args:
        text: The input text to truncate
        max_len: Maximum length of the output string

    Returns:
        Truncated text with ellipsis if longer than max_len, otherwise original text

    Examples:
        >>> truncate_text("Hello world", 8)
        'Hello...'
        >>> truncate_text("Short", 10)
        'Short'
    """
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def format_table_row(columns: list[str], widths: list[int]) -> str:
    """Format a table row with specified column widths.

    Args:
        columns: List of column values
        widths: List of column widths

    Returns:
        Formatted table row string with proper spacing

    Raises:
        ValueError: If columns and widths lists have different lengths

    Examples:
        >>> format_table_row(["Name", "Age"], [10, 5])
        'Name       Age  '
        >>> format_table_row(["John", "25"], [10, 5])
        'John       25   '
    """
    if len(columns) != len(widths):
        raise ValueError("Number of columns must match number of widths")

    formatted_parts = []
    for col, width in zip(columns, widths):
        # Truncate column content if longer than width
        if len(col) > width:
            formatted_parts.append(col[: width - 3] + "...")
        else:
            formatted_parts.append(col.ljust(width))

    return "".join(formatted_parts)


def validate_output_format(format: str) -> str:
    """Validate and normalize audio output format.

    Args:
        format: Input format string to validate

    Returns:
        Normalized format string in lowercase

    Raises:
        ValueError: If format is not one of the supported formats

    Examples:
        >>> validate_output_format("MP3")
        'mp3'
        >>> validate_output_format("wav")
        'wav'
    """
    supported_formats = {"mp3", "opus", "aac", "flac", "wav", "pcm"}
    normalized_format = format.lower().strip()

    if normalized_format not in supported_formats:
        raise ValueError(
            f"Unsupported format '{format}'. Supported formats: "
            f"{', '.join(sorted(supported_formats))}"
        )

    return normalized_format


def mask_api_key(key: str) -> str:
    """Mask an API key by showing only first 4 and last 4 characters.

    Args:
        key: The API key to mask

    Returns:
        Masked API key with asterisks in middle

    Examples:
        >>> mask_api_key("sk-1234567890abcdef")
        'sk-1****cdef'
        >>> mask_api_key("short")
        'short'
    """
    if len(key) <= 8:
        # If key is too short, return as-is
        return key

    first_part = key[:4]
    last_part = key[-4:]
    middle_len = len(key) - 8

    return f"{first_part}{'*' * middle_len}{last_part}"
