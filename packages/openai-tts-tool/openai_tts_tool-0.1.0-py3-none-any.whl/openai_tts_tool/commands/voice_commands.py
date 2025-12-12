"""
Voice commands for openai-tts-tool.

This module provides commands for listing and managing TTS voices.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from openai_tts_tool.logging_config import get_logger
from openai_tts_tool.voices import VOICES, list_voices

logger = get_logger(__name__)


def format_table_row(
    name: str, description: str, max_name_width: int = 10, max_desc_width: int = 50
) -> str:
    """Format a row for table display with consistent column widths."""
    # Truncate if necessary and align left
    name_col = name.ljust(max_name_width)
    desc_col = description[:max_desc_width].ljust(max_desc_width)
    return f"│ {name_col} │ {desc_col} │"


def format_table_header(max_name_width: int = 10, max_desc_width: int = 50) -> str:
    """Format table header with separator."""
    header = format_table_row("Voice", "Description", max_name_width, max_desc_width)
    separator = "─".join(["", "─" * (max_name_width + 2), "─" * (max_desc_width + 2), ""])
    separator = "├" + separator[1:-1] + "┤"
    return f"┌{'─' * (max_name_width + max_desc_width + 7)}┐\n{header}\n{separator}"


def format_table_footer(max_name_width: int = 10, max_desc_width: int = 50) -> str:
    """Format table footer."""
    return f"└{'─' * (max_name_width + max_desc_width + 7)}┘"


def get_voice_characteristics(voice_name: str) -> dict[str, str]:
    """Extract gender characteristics from voice name/description."""
    characteristics = {"gender": "Unknown", "characteristics": "Neutral"}

    voice_lower = voice_name.lower()
    desc = VOICES.get(voice_lower, "").lower()

    if any(keyword in desc for keyword in ["male", "deep", "rich"]):
        characteristics["gender"] = "Male"
    elif any(keyword in desc for keyword in ["female", "warm"]):
        characteristics["gender"] = "Female"

    if "authoritative" in desc:
        characteristics["characteristics"] = "Authoritative"
    elif "friendly" in desc:
        characteristics["characteristics"] = "Friendly"
    elif "expressive" in desc:
        characteristics["characteristics"] = "Expressive"
    elif "british" in desc:
        characteristics["characteristics"] = "British accent"

    return characteristics


@click.command("list-voices")
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Verbose output: -v (INFO), -vv (DEBUG), -vvv (TRACE with details)",
)
def list_voices_command(verbose: int) -> None:
    """List all available OpenAI TTS voices in a formatted table.

    This command displays all available voices with their descriptions and
    gender characteristics in an easy-to-read table format.

    Examples:

    \b
        # Basic voice listing
        openai-tts-tool list-voices

    \b
        # Verbose output with additional details
        openai-tts-tool list-voices -v

    \b
        # Very verbose with all voice properties
        openai-tts-tool list-voices -vvv

    \b
    Output Format:
        Displays a formatted table with columns:
        - Voice: Name of the voice (alloy, ash, coral, etc.)
        - Description: Voice characteristics and use case
        - Gender: Male/Female/Unknown
        - Characteristics: Additional voice properties
    """
    logger.info("Listing available OpenAI TTS voices")

    if verbose >= 2:
        logger.debug("Retrieved voice data from voices module")

    voices = list_voices()

    if not voices:
        click.echo("No voices available", err=True)
        return

    # Calculate optimal column widths
    max_name_width = max(len(voice["name"]) for voice in voices)
    max_name_width = max(max_name_width, len("Voice"))  # Ensure header fits

    max_desc_width = 60  # Fixed width for better readability

    if verbose >= 2:
        click.echo(f"Found {len(voices)} voices available")
        click.echo("")

    # Display table header
    if verbose < 2:
        click.echo(format_table_header(max_name_width, max_desc_width))

    # Display voice data
    for voice in voices:
        if verbose >= 2:
            # Detailed format for verbose output
            characteristics = get_voice_characteristics(voice["name"])
            click.echo(f"Voice: {voice['name']}")
            click.echo(f"  Description: {voice['description']}")
            click.echo(f"  Gender: {characteristics['gender']}")
            click.echo(f"  Characteristics: {characteristics['characteristics']}")
            click.echo("")
        else:
            # Table format for normal output
            row = format_table_row(
                voice["name"], voice["description"], max_name_width, max_desc_width
            )
            click.echo(row)

    # Display table footer
    if verbose < 2:
        click.echo(format_table_footer(max_name_width, max_desc_width))

    logger.info(f"Successfully listed {len(voices)} voices")

    if verbose >= 3:
        logger.debug("Voice listing completed successfully")
