"""Tests for openai_tts_tool.voices module.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import pytest

from openai_tts_tool.voices import (
    DEFAULT_VOICE,
    VOICES,
    get_voice_description,
    list_voices,
    validate_voice,
)


def test_validate_voice_valid() -> None:
    """Test validate_voice with valid voice names."""
    result = validate_voice("alloy")
    assert result == "alloy"

    result = validate_voice("ALLOY")
    assert result == "alloy"

    result = validate_voice("  echo  ")
    assert result == "echo"


def test_validate_voice_invalid() -> None:
    """Test validate_voice with invalid voice name."""
    with pytest.raises(ValueError, match="Unsupported voice 'invalid-voice'"):
        validate_voice("invalid-voice")


def test_validate_voice_empty() -> None:
    """Test validate_voice with empty string."""
    with pytest.raises(ValueError, match="Voice name cannot be empty"):
        validate_voice("")


def test_validate_voice_whitespace() -> None:
    """Test validate_voice with whitespace only."""
    with pytest.raises(ValueError, match="Unsupported voice '   '"):
        validate_voice("   ")


def test_list_voices() -> None:
    """Test list_voices returns all voices with descriptions."""
    voices = list_voices()
    assert len(voices) == len(VOICES)

    # Check that it's a list of dictionaries
    assert all(isinstance(voice, dict) for voice in voices)

    # Check that each voice has name and description
    for voice in voices:
        assert "name" in voice
        assert "description" in voice
        assert voice["name"] in VOICES
        assert voice["description"] == VOICES[voice["name"]]

    # Check that voices are sorted alphabetically
    voice_names = [voice["name"] for voice in voices]
    assert voice_names == sorted(voice_names)


def test_list_voices_contains_default() -> None:
    """Test that list_voices contains the default voice."""
    voices = list_voices()
    voice_names = [voice["name"] for voice in voices]
    assert DEFAULT_VOICE in voice_names


def test_get_voice_description_valid() -> None:
    """Test get_voice_description with valid voice."""
    description = get_voice_description("alloy")
    assert description == VOICES["alloy"]

    description = get_voice_description("ALLOY")
    assert description == VOICES["alloy"]


def test_get_voice_description_invalid() -> None:
    """Test get_voice_description with invalid voice."""
    with pytest.raises(ValueError, match="Unsupported voice 'invalid-voice'"):
        get_voice_description("invalid-voice")


def test_get_voice_description_empty() -> None:
    """Test get_voice_description with empty string."""
    with pytest.raises(ValueError, match="Voice name cannot be empty"):
        get_voice_description("")


def test_voices_constants() -> None:
    """Test that voices constants are properly defined."""
    assert isinstance(VOICES, dict)
    assert len(VOICES) > 0
    assert isinstance(DEFAULT_VOICE, str)
    assert DEFAULT_VOICE in VOICES

    # Check that all voices have descriptions
    for voice, description in VOICES.items():
        assert isinstance(voice, str)
        assert isinstance(description, str)
        assert len(voice.strip()) > 0
        assert len(description.strip()) > 0


def test_voice_names_lowercase() -> None:
    """Test that all voice names are lowercase."""
    for voice in VOICES.keys():
        assert voice == voice.lower()


def test_validate_voice_case_insensitive() -> None:
    """Test that validate_voice works with different cases."""
    test_cases = ["ALLOY", "Alloy", "aLlOy", "alloy"]
    for case in test_cases:
        result = validate_voice(case)
        assert result == "alloy"


def test_list_voices_immutability() -> None:
    """Test that list_voices doesn't modify internal state."""
    voices1 = list_voices()
    voices2 = list_voices()
    assert voices1 == voices2

    # Modify returned list and ensure original is unchanged
    voices1.append({"name": "fake", "description": "fake"})
    voices3 = list_voices()
    assert len(voices3) == len(VOICES)
    assert "fake" not in [voice["name"] for voice in voices3]
