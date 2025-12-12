"""
Core functionality for OpenAI TTS operations.

This package provides the core client functionality for interacting with
OpenAI's text-to-speech API, including synthesis, streaming, and file I/O.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from .client import get_api_info, get_openai_client, test_credentials
from .synthesize import (
    play_speech_streaming,
    read_from_stdin,
    save_speech,
    synthesize_audio,
)

__all__ = [
    "get_openai_client",
    "test_credentials",
    "get_api_info",
    "synthesize_audio",
    "play_speech_streaming",
    "save_speech",
    "read_from_stdin",
]
