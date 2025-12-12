"""
Core text-to-speech synthesis functions for OpenAI TTS.

This module provides the fundamental TTS operations - converting text
to audio, playing through speakers, and saving to files. By keeping these
functions pure and CLI-independent, we enable both command-line and
programmatic usage while maintaining testability.

The streaming approach minimizes latency by processing audio data in memory
without disk I/O, making the tool responsive for interactive use cases like
voice assistants and real-time narration.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys
from pathlib import Path
from typing import Literal

import pyaudio
from openai import APIStatusError, OpenAI, OpenAIError

from openai_tts_tool.logging_config import get_logger

logger = get_logger(__name__)

# Valid OpenAI TTS response formats
ResponseFormat = Literal["mp3", "opus", "aac", "flac", "wav", "pcm"]


def synthesize_audio(
    client: OpenAI,
    text: str,
    voice: str,
    model: str = "tts-1",
    response_format: ResponseFormat = "mp3",
) -> bytes:
    """
    Synthesize text to audio using OpenAI's TTS API.

    This is the core TTS operation that streams audio directly from OpenAI
    without disk I/O for optimal performance. Returns audio bytes for
    immediate playback or processing.

    The function supports all OpenAI response formats and models, providing
    flexibility for different use cases from real-time streaming (pcm)
    to web streaming (opus) to general purpose (mp3).

    Args:
        client: OpenAI client instance
        text: Text to synthesize
        voice: Voice name (e.g., 'alloy', 'nova', 'echo')
        model: TTS model to use ('tts-1' or 'tts-1-hd')
        response_format: Audio format ('mp3', 'opus', 'aac', 'flac', 'pcm')

    Returns:
        Audio bytes for playback or processing

    Raises:
        ValueError: If text is empty or exceeds limits, or invalid parameters
        APIStatusError: If OpenAI API call fails
        OpenAIError: For other OpenAI-related errors

    Example:
        >>> client = get_openai_client()
        >>> audio = synthesize_audio(client, "Hello world", "alloy")
        >>> # Play or save audio
    """
    # Validate input parameters
    if not text or not text.strip():
        raise ValueError("Text cannot be empty. Please provide text to synthesize.")

    if not voice.strip():
        raise ValueError("Voice cannot be empty. Please provide a valid voice name.")

    # Validate text length (OpenAI has practical limits around 4096 characters)
    max_chars = 4096
    if len(text) > max_chars:
        raise ValueError(
            f"Text length ({len(text)}) exceeds OpenAI TTS limit ({max_chars} characters).\n\n"
            f"Solutions:\n"
            f"  1. Split text into chunks under {max_chars} characters\n"
            f"  2. Process content in batches with multiple API calls"
        )

    logger.debug(
        "Calling OpenAI TTS API: model=%s, voice=%s, format=%s, text_length=%d",
        model, voice, response_format, len(text)
    )

    try:
        # Call OpenAI TTS API
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
            response_format=response_format,
        )

        # Read audio stream from response
        audio_bytes = response.content

        if not audio_bytes:
            raise OpenAIError("Received empty audio response from OpenAI.")

        logger.debug("Successfully synthesized %d bytes of audio", len(audio_bytes))
        return audio_bytes

    except APIStatusError as e:
        logger.debug("OpenAI API error: %s", e)
        raise APIStatusError(
            message=f"OpenAI TTS API error: {e}. "
            f"Verify your API key, quota, and parameters (voice={voice}, model={model}).",
            response=e.response,
            body=e.body,
        ) from e
    except OpenAIError as e:
        logger.debug("OpenAI error: %s", e)
        raise OpenAIError(
            f"TTS synthesis failed: {e}\n\n"
            f"Parameters: voice={voice}, model={model}, format={response_format}\n"
            f"Verify voice and model are supported by OpenAI."
        ) from e
    except Exception as e:
        logger.debug("Unexpected error during synthesis: %s", e)
        logger.debug("Full traceback:", exc_info=True)
        raise OpenAIError(
            f"Unexpected error during TTS synthesis: {e}. "
            "Please check your network connection and try again."
        ) from e


def play_speech_streaming(
    client: OpenAI,
    text: str,
    voice: str,
    model: str = "tts-1",
) -> int:
    """
    Synthesize text and play through system speakers with streaming.

    Provides immediate audio feedback for interactive TTS use cases
    using OpenAI's streaming API. Uses PyAudio for low-latency playback
    with PCM format for real-time streaming.

    Args:
        client: OpenAI client instance
        text: Text to synthesize and play
        voice: Voice name
        model: TTS model to use

    Returns:
        Number of characters processed (for cost tracking)

    Raises:
        ValueError: If text is invalid or exceeds limits
        Exception: If synthesis or playback fails

    Example:
        >>> client = get_openai_client()
        >>> chars = play_speech_streaming(client, "Hello world", "alloy")
    """
    # Validate input parameters
    if not text or not text.strip():
        raise ValueError("Text cannot be empty. Please provide text to synthesize.")

    # Track character count for cost tracking
    char_count = len(text)

    try:
        # Initialize PyAudio
        audio = pyaudio.PyAudio()

        # Configure audio stream (OpenAI uses 24kHz, 16-bit PCM)
        sample_rate = 24000
        channels = 1
        format = pyaudio.paInt16
        chunk_size = 1024

        # Open audio stream for playback
        stream = audio.open(
            format=format,
            channels=channels,
            rate=sample_rate,
            output=True,
            frames_per_buffer=chunk_size,
        )

        try:
            # Use OpenAI's streaming API with PCM format for real-time playback
            with client.audio.speech.with_streaming_response.create(
                model=model,
                voice=voice,
                input=text,
                response_format="pcm",
            ) as response:
                # Stream audio chunks directly to speakers
                for chunk in response.iter_bytes(chunk_size=1024):
                    stream.write(chunk)

        finally:
            # Clean up audio stream
            stream.stop_stream()
            stream.close()
            audio.terminate()

        return char_count

    except APIStatusError as e:
        raise APIStatusError(
            message=f"OpenAI TTS streaming error: {e}. "
            f"Verify your API key, quota, and parameters (voice={voice}, model={model}).",
            response=e.response,
            body=e.body,
        ) from e
    except Exception as e:
        # Handle PyAudio-specific errors with helpful messages
        if "NoDefaultOutputDevice" in str(e):
            raise Exception(
                "No audio output device found. Please check your audio system.\n\n"
                "Solutions:\n"
                "  1. Connect speakers or headphones\n"
                "  2. Check system audio settings\n"
                "  3. Verify audio drivers are installed"
            ) from e
        elif "Invalid sample rate" in str(e):
            raise Exception(
                "Audio system doesn't support 24kHz sample rate.\n\n"
                "This is unusual for modern systems. Please check your audio configuration."
            ) from e
        else:
            raise Exception(
                f"Audio playback failed: {e}\n\n"
                "Verify audio system is configured and PyAudio is properly installed."
            ) from e


def save_speech(
    client: OpenAI,
    text: str,
    voice: str,
    model: str,
    output_path: str | Path,
    response_format: ResponseFormat = "mp3",
) -> int:
    """
    Synthesize text and save audio to file.

    Enables caching synthesized audio for reuse, reducing API costs
    and latency for frequently played content. Creates parent directories
    automatically to simplify file management.

    Args:
        client: OpenAI client instance
        text: Text to synthesize
        voice: Voice name
        model: TTS model to use
        output_path: File path to save audio
        response_format: Audio format (mp3, opus, aac, flac, pcm)

    Returns:
        Number of characters processed (for cost tracking)

    Raises:
        ValueError: If text is invalid or path is not writable
        Exception: If synthesis or file write fails

    Example:
        >>> client = get_openai_client()
        >>> chars = save_speech(client, "Hello", "alloy", "tts-1", "output.mp3")
    """
    # Convert string path to Path object
    output_path = Path(output_path)

    # Validate output path
    if not output_path.suffix:
        # Add file extension based on format if not present
        output_path = output_path.with_suffix(f".{response_format}")

    logger.debug(
        "Saving speech to file: voice=%s, model=%s, format=%s, output=%s",
        voice, model, response_format, output_path
    )

    # Synthesize audio
    audio_bytes = synthesize_audio(client, text, voice, model, response_format)

    # Track character count for cost tracking
    char_count = len(text)

    try:
        # Create parent directories if needed
        # WHY: Simplify file management - don't require users to mkdir first
        output_path.parent.mkdir(parents=True, exist_ok=True)
        logger.debug("Created directory: %s", output_path.parent)

        # Write audio to file
        output_path.write_bytes(audio_bytes)
        logger.info("Saved audio to: %s (%d bytes)", output_path, len(audio_bytes))

        return char_count

    except PermissionError as e:
        logger.error("Permission denied writing to %s: %s", output_path, e)
        raise ValueError(
            f"Permission denied writing to: {output_path}\n\n"
            f"Solutions:\n"
            f"  1. Check file permissions: ls -la {output_path.parent}\n"
            f"  2. Choose a different output directory\n"
            f"  3. Run with appropriate permissions"
        )
    except Exception as e:
        logger.error("Failed to save audio to %s: %s", output_path, e)
        raise Exception(f"Failed to save audio to {output_path}: {e}") from e


def read_from_stdin() -> str:
    """
    Read text from stdin with validation.

    Enables piping text from other commands and tools, supporting
    Unix-style composability. Validates that stdin is being piped (not
    interactive terminal) and that content is non-empty, providing clear
    error messages for common mistakes.

    Returns:
        Text read from stdin

    Raises:
        ValueError: If stdin is a terminal or input is empty

    Example:
        >>> # From command line:
        >>> # echo "Hello world" | openai-tts-tool synthesize --stdin
    """
    # Check if stdin is being piped or is an interactive terminal
    # WHY: Fail fast with helpful message if user forgets to pipe input
    if sys.stdin.isatty():
        raise ValueError(
            "No input provided via stdin.\n\n"
            "Usage:\n"
            "  echo 'text' | openai-tts-tool synthesize --stdin\n"
            "  cat file.txt | openai-tts-tool synthesize --stdin --voice nova\n\n"
            "Or provide text as argument:\n"
            "  openai-tts-tool synthesize 'your text here'"
        )

    # Read and strip whitespace
    text = sys.stdin.read().strip()

    # Validate non-empty
    if not text:
        raise ValueError(
            "Empty input received from stdin.\n\n"
            "Ensure piped content is not empty:\n"
            "  echo 'Hello world' | openai-tts-tool synthesize --stdin"
        )

    return text
