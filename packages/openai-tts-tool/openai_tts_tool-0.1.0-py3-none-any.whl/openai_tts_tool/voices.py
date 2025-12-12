"""
Voice configuration and validation for OpenAI TTS.

This module provides voice definitions and validation functions for the OpenAI
Text-to-Speech API, including all available voices with their descriptions.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

# OpenAI TTS voices with descriptions
VOICES: dict[str, str] = {
    "alloy": "Versatile neutral voice suitable for most content",
    "ash": "Conversational and friendly voice",
    "coral": "Clear and articulate voice with precise pronunciation",
    "echo": "Authoritative male voice with deep tones",
    "fable": "Expressive British voice with character",
    "onyx": "Deep male voice with rich resonant tones",
    "nova": "Warm female voice with natural delivery",
    "sage": "Wise mature voice with experienced tone",
    "shimmer": "Warm female expressive voice with emotional range",
}

# Default voice for general use
DEFAULT_VOICE: str = "alloy"


def validate_voice(voice: str) -> str:
    """
    Validate voice name and return normalized lowercase voice name.

    Args:
        voice: Voice name to validate (case-insensitive)

    Returns:
        Normalized lowercase voice name

    Raises:
        ValueError: If voice is not supported
    """
    if not voice:
        raise ValueError("Voice name cannot be empty")

    normalized_voice = voice.lower().strip()

    if normalized_voice not in VOICES:
        available_voices = ", ".join(sorted(VOICES.keys()))
        raise ValueError(f"Unsupported voice '{voice}'. Available voices: {available_voices}")

    return normalized_voice


def list_voices() -> list[dict[str, str]]:
    """
    Get list of available voices with descriptions.

    Returns:
        List of dictionaries containing voice names and descriptions
    """
    return [
        {"name": voice, "description": description} for voice, description in sorted(VOICES.items())
    ]


def get_voice_description(voice: str) -> str:
    """
    Get description for a specific voice.

    Args:
        voice: Voice name (case-insensitive)

    Returns:
        Voice description

    Raises:
        ValueError: If voice is not supported
    """
    normalized_voice = validate_voice(voice)
    return VOICES[normalized_voice]
