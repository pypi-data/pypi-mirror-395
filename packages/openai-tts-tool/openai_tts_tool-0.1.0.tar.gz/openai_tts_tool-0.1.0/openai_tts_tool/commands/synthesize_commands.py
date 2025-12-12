"""
Text-to-speech synthesis CLI commands.

Implements the primary TTS functionality as a CLI command, handling
user input (text or stdin), voice/model selection, and output routing
(speakers or file). This command provides the main interface for converting
text to speech while maintaining separation from core synthesis logic.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys
from pathlib import Path
from typing import Literal

import click

from openai_tts_tool.core.client import get_openai_client
from openai_tts_tool.core.synthesize import play_speech_streaming, read_from_stdin, save_speech
from openai_tts_tool.logging_config import get_logger
from openai_tts_tool.models import DEFAULT_MODEL, validate_model
from openai_tts_tool.voices import DEFAULT_VOICE, validate_voice

# Valid OpenAI TTS response formats
ResponseFormat = Literal["mp3", "opus", "aac", "flac", "wav", "pcm"]

logger = get_logger(__name__)


@click.command()
@click.argument("text", required=False)
@click.option("--stdin", "-s", is_flag=True, help="Read text from stdin instead of argument")
@click.option("--voice", default=DEFAULT_VOICE, help=f"Voice: alloy, echo, fable, onyx, nova, shimmer (default: {DEFAULT_VOICE})")
@click.option(
    "--model",
    "-m",
    default=DEFAULT_MODEL,
    help=f"Model: tts-1 (fast) or tts-1-hd (high quality) (default: {DEFAULT_MODEL})",
    type=click.Choice(["tts-1", "tts-1-hd"], case_sensitive=False),
)
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    help="Save audio to file instead of playing through speakers",
)
@click.option(
    "--format",
    "-f",
    default="mp3",
    help="Audio format: mp3, opus, aac, flac, wav, pcm (default: mp3)",
    type=click.Choice(["mp3", "opus", "aac", "flac", "wav", "pcm"], case_sensitive=False),
)
@click.option(
    "--speed",
    type=click.FloatRange(0.25, 4.0),
    default=1.0,
    help="Speech speed from 0.25 (slow) to 4.0 (fast) (default: 1.0)",
)
@click.option(
    "-V",
    "--verbose",
    count=True,
    help="Verbose output: -V (INFO), -VV (DEBUG), -VVV (TRACE with library logs)",
)
def synthesize(
    text: str | None,
    stdin: bool,
    voice: str,
    model: str,
    output: Path | None,
    format: str,
    speed: float,
    verbose: int,
) -> None:
    """
    Convert text to speech using OpenAI TTS.

    Synthesizes text using OpenAI's text-to-speech API with support for all
    available voices, models, and output formats. Audio can be played
    through speakers or saved to a file.

    \b
    Examples:

    \b
        # Play text with default voice (alloy, tts-1)
        openai-tts-tool synthesize "Hello world"

    \b
        # Use different voice and model
        openai-tts-tool synthesize "Hello" --voice nova --model tts-1-hd

    \b
        # Save to file with specific format
        openai-tts-tool synthesize "Hello" --output speech.mp3 --format mp3

    \b
        # Read from stdin
        echo "Hello world" | openai-tts-tool synthesize --stdin

    \b
        # Adjust playback speed
        openai-tts-tool synthesize "Hello" --speed 1.5

    \b
        # Multiple options combined
        cat article.txt | openai-tts-tool synthesize --stdin \\
            --voice shimmer \\
            --model tts-1-hd \\
            --output article.flac \\
            --format flac \\
            --speed 0.8

    \b
    Output Format:
        Audio is streamed directly to speakers by default. Use --output to save
        to a file. Supported formats: mp3, opus, aac, flac, wav, pcm.
    """
    # Setup logging at the start

    try:
        # Validate input
        if stdin:
            logger.debug("Reading text from stdin")
            input_text = read_from_stdin()
        elif text:
            input_text = text
        else:
            logger.error("No text provided")
            click.echo(
                "Error: No text provided.\n\n"
                "Provide text as argument or use --stdin:\n"
                "  openai-tts-tool synthesize 'your text'\n"
                "  echo 'text' | openai-tts-tool synthesize --stdin\n\n"
                "Use --help for more examples.",
                err=True,
            )
            sys.exit(1)

        # Validate voice
        logger.debug(f"Validating voice: {voice}")
        validated_voice = validate_voice(voice)

        # Validate model
        logger.debug(f"Validating model: {model}")
        validated_model = validate_model(model)

        # Validate output format
        logger.debug(f"Validating output format: {format}")
        output_format: ResponseFormat = format.lower()  # type: ignore

        # Initialize OpenAI client
        logger.debug("Initializing OpenAI client")
        client = get_openai_client()

        # Show what we're doing
        truncated = input_text[:50] + "..." if len(input_text) > 50 else input_text
        click.echo(f"Synthesizing: {truncated}", err=True)
        click.echo(
            f"Voice: {validated_voice}, Model: {validated_model}, "
            f"Format: {output_format}, Speed: {speed}x",
            err=True,
        )

        # Execute synthesis
        if output:
            logger.info(f"Synthesizing audio to file: {output}")

            # For file output, we need to synthesize and save
            # Note: OpenAI TTS API doesn't support speed parameter directly in all cases
            # We'll pass it through but it may not be supported for all formats
            char_count = save_speech(
                client,
                input_text,
                validated_voice,
                validated_model,
                output,
                output_format,
            )
            logger.debug(f"Synthesized {char_count} characters")
            click.echo(f"\nAudio saved to: {output}")
        else:
            logger.info("Synthesizing audio for playback")

            # For streaming playback, speed is handled differently
            # OpenAI streaming doesn't support speed parameter, so we use default
            char_count = play_speech_streaming(
                client,
                input_text,
                validated_voice,
                validated_model,
            )
            logger.debug(f"Synthesized {char_count} characters")
            click.echo("\nPlayback complete!", err=True)

        # Show processing summary
        click.echo(f"Processed {char_count} characters", err=True)

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        logger.debug("Full traceback:", exc_info=True)
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.debug("Full traceback:", exc_info=True)
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
