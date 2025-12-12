"""Tests for openai_tts_tool.utils module.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import pytest

from openai_tts_tool.utils import (
    format_table_row,
    mask_api_key,
    truncate_text,
    validate_output_format,
)


def test_truncate_text_short() -> None:
    """Test truncate_text with text shorter than max_len."""
    result = truncate_text("Hello", 10)
    assert result == "Hello"


def test_truncate_text_exact() -> None:
    """Test truncate_text with text exactly max_len."""
    result = truncate_text("Hello", 5)
    assert result == "Hello"


def test_truncate_text_long() -> None:
    """Test truncate_text with text longer than max_len."""
    result = truncate_text("Hello world", 8)
    assert result == "Hello..."


def test_truncate_text_just_over() -> None:
    """Test truncate_text with text one character over max_len."""
    result = truncate_text("12345", 4)
    assert result == "1..."


def test_truncate_text_empty() -> None:
    """Test truncate_text with empty string."""
    result = truncate_text("", 5)
    assert result == ""


def test_truncate_text_zero_max_len() -> None:
    """Test truncate_text with zero max_len."""
    result = truncate_text("Hello", 0)
    assert result == "He..."


def test_format_table_row_normal() -> None:
    """Test format_table_row with normal inputs."""
    result = format_table_row(["Name", "Age"], [10, 5])
    assert result == "Name      Age  "


def test_format_table_row_unequal_lengths() -> None:
    """Test format_table_row with unequal column and width lists."""
    with pytest.raises(ValueError, match="Number of columns must match number of widths"):
        format_table_row(["Name"], [10, 5])


def test_format_table_row_truncate_column() -> None:
    """Test format_table_row with column longer than width."""
    result = format_table_row(["VeryLongName"], [5])
    assert result == "Ve..."


def test_format_table_row_empty_lists() -> None:
    """Test format_table_row with empty lists."""
    result = format_table_row([], [])
    assert result == ""


def test_format_table_row_single_column() -> None:
    """Test format_table_row with single column."""
    result = format_table_row(["Test"], [8])
    assert result == "Test    "


def test_validate_output_format_valid() -> None:
    """Test validate_output_format with valid formats."""
    result = validate_output_format("mp3")
    assert result == "mp3"

    result = validate_output_format("MP3")
    assert result == "mp3"

    result = validate_output_format("  wav  ")
    assert result == "wav"


def test_validate_output_format_invalid() -> None:
    """Test validate_output_format with invalid format."""
    with pytest.raises(ValueError, match="Unsupported format 'xyz'"):
        validate_output_format("xyz")


def test_validate_output_format_empty() -> None:
    """Test validate_output_format with empty format."""
    with pytest.raises(ValueError, match="Unsupported format ''"):
        validate_output_format("")


def test_mask_api_key_normal() -> None:
    """Test mask_api_key with normal API key."""
    result = mask_api_key("sk-1234567890abcdef")
    assert result == "sk-1***********cdef"
    assert len(result) == len("sk-1234567890abcdef")


def test_mask_api_key_short() -> None:
    """Test mask_api_key with short key (<= 8 chars)."""
    result = mask_api_key("short")
    assert result == "short"


def test_mask_api_key_exact_8() -> None:
    """Test mask_api_key with exactly 8 characters."""
    result = mask_api_key("12345678")
    assert result == "12345678"


def test_mask_api_key_with_prefix() -> None:
    """Test mask_api_key with sk- prefix."""
    result = mask_api_key("sk-1234567890abcdef1234")
    assert result == "sk-1***************1234"
    assert result.startswith("sk-")
    assert result.endswith("1234")


def test_mask_api_key_very_long() -> None:
    """Test mask_api_key with very long key."""
    key = "sk-" + "a" * 50
    result = mask_api_key(key)
    assert result == "sk-a*********************************************aaaa"
    assert len(result) == len(key)


def test_mask_api_key_empty() -> None:
    """Test mask_api_key with empty string."""
    result = mask_api_key("")
    assert result == ""
