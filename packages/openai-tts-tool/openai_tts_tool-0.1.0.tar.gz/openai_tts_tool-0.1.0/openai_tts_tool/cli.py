"""CLI entry point for openai-tts-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from openai_tts_tool.commands import (
    completion,
    info_command,
    list_models_command,
    list_voices_command,
    synthesize,
)
from openai_tts_tool.logging_config import get_logger, setup_logging

logger = get_logger(__name__)


@click.group()
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Verbose output: -v (INFO), -vv (DEBUG), -vvv (TRACE with library logs)",
)
@click.version_option(version="0.1.0")
def main(verbose: int) -> None:
    """OpenAI Text-to-Speech CLI Tool.

    A powerful command-line interface for converting text to speech using OpenAI's
    advanced TTS models. Supports multiple voices, languages, and output formats.

    Quick Start:

    \b
        # Basic text-to-speech conversion
        openai-tts-tool synthesize "Hello, world!" output.mp3

    \b
        # List available voices
        openai-tts-tool list-voices

    \b
        # List available models
        openai-tts-tool list-models

    \b
        # Show system information
        openai-tts-tool info

    \b
    Examples:

        # Synthesize with specific voice
        openai-tts-tool synthesize "Hello world" hello.mp3 --voice alloy --speed 1.2

        # Different output formats
        openai-tts-tool synthesize text.txt speech.mp3
        openai-tts-tool synthesize text.txt speech.opus --model tts-1-hd

        # Verbose output for debugging
        openai-tts-tool -vv synthesize "Test" test.mp3

        # Pipe input from other commands
        echo "Hello" | openai-tts-tool synthesize - output.mp3
    """
    # Setup logging based on verbosity count
    setup_logging(verbose)


# Register all commands
main.add_command(synthesize)
main.add_command(list_voices_command, name="list-voices")
main.add_command(list_models_command, name="list-models")
main.add_command(info_command, name="info")
main.add_command(completion)


if __name__ == "__main__":
    main()
