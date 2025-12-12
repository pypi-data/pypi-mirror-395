"""
Model commands for openai-tts-tool.

This module provides commands for listing and managing TTS models.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from openai_tts_tool.logging_config import get_logger
from openai_tts_tool.models import list_models

logger = get_logger(__name__)


def format_table_row(
    name: str,
    description: str,
    quality: str,
    latency: str,
    max_name_width: int = 12,
    max_desc_width: int = 40,
    max_quality_width: int = 10,
    max_latency_width: int = 10,
) -> str:
    """Format a row for table display with consistent column widths."""
    # Truncate if necessary and align left
    name_col = name.ljust(max_name_width)
    desc_col = description[:max_desc_width].ljust(max_desc_width)
    quality_col = quality.ljust(max_quality_width)
    latency_col = latency.ljust(max_latency_width)
    return f"│ {name_col} │ {desc_col} │ {quality_col} │ {latency_col} │"


def format_table_header(
    max_name_width: int = 12,
    max_desc_width: int = 40,
    max_quality_width: int = 10,
    max_latency_width: int = 10,
) -> str:
    """Format table header with separator."""
    header = format_table_row(
        "Model",
        "Description",
        "Quality",
        "Latency",
        max_name_width,
        max_desc_width,
        max_quality_width,
        max_latency_width,
    )
    total_width = max_name_width + max_desc_width + max_quality_width + max_latency_width + 13
    separator = "─".join(
        [
            "",
            "─" * (max_name_width + 2),
            "─" * (max_desc_width + 2),
            "─" * (max_quality_width + 2),
            "─" * (max_latency_width + 2),
            "",
        ]
    )
    separator = "├" + separator[1:-1] + "┤"
    return f"┌{'─' * total_width}┐\n{header}\n{separator}"


def format_table_footer(
    max_name_width: int = 12,
    max_desc_width: int = 40,
    max_quality_width: int = 10,
    max_latency_width: int = 10,
) -> str:
    """Format table footer."""
    total_width = max_name_width + max_desc_width + max_quality_width + max_latency_width + 13
    return f"└{'─' * total_width}┘"


def get_model_characteristics(model_info: dict[str, str]) -> dict[str, str]:
    """Extract detailed characteristics from model information."""
    characteristics = {
        "use_case": "General",
        "performance": "Standard",
        "recommendation": "Suitable for most applications",
    }

    quality = model_info.get("quality", "").lower()
    speed = model_info.get("speed", "").lower()

    if quality == "high":
        characteristics["use_case"] = "Professional content"
        characteristics["performance"] = "Premium"
        characteristics["recommendation"] = "Best for high-quality audio production"
    elif quality == "standard":
        characteristics["use_case"] = "Interactive applications"
        characteristics["performance"] = "Optimized"
        characteristics["recommendation"] = "Ideal for real-time responses"

    if speed == "fast":
        characteristics["performance"] += " (Fast)"
    elif speed == "slow":
        characteristics["performance"] += " (Detailed)"

    return characteristics


@click.command("list-models")
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Verbose output: -v (INFO), -vv (DEBUG), -vvv (TRACE with details)",
)
def list_models_command(verbose: int) -> None:
    """List all available OpenAI TTS models in a formatted table.

    This command displays all available TTS models with their descriptions,
    quality levels, and latency characteristics in an easy-to-read table format.

    Examples:

    \b
        # Basic model listing
        openai-tts-tool list-models

    \b
        # Verbose output with additional details
        openai-tts-tool list-models -v

    \b
        # Very verbose with all model properties and recommendations
        openai-tts-tool list-models -vvv

    \b
    Output Format:
        Displays a formatted table with columns:
        - Model: Name of the model (tts-1, tts-1-hd)
        - Description: Model characteristics and use case
        - Quality: Audio quality level (standard/high)
        - Latency: Response time characteristics (low/higher)
    """
    logger.info("Listing available OpenAI TTS models")

    if verbose >= 2:
        logger.debug("Retrieved model data from models module")

    models = list_models()

    if not models:
        click.echo("No models available", err=True)
        return

    # Calculate optimal column widths
    max_name_width = max(len(model["name"]) for model in models)
    max_name_width = max(max_name_width, len("Model"))  # Ensure header fits

    max_desc_width = 40  # Fixed width for better readability
    max_quality_width = max(len(model["quality"]) for model in models)
    max_quality_width = max(max_quality_width, len("Quality"))
    max_latency_width = max(len(model["latency"]) for model in models)
    max_latency_width = max(max_latency_width, len("Latency"))

    if verbose >= 2:
        click.echo(f"Found {len(models)} models available")
        click.echo("")

    # Display table header
    if verbose < 2:
        click.echo(
            format_table_header(
                max_name_width, max_desc_width, max_quality_width, max_latency_width
            )
        )

    # Display model data
    for model in models:
        if verbose >= 2:
            # Detailed format for verbose output
            characteristics = get_model_characteristics(model)
            click.echo(f"Model: {model['name']}")
            click.echo(f"  Description: {model['description']}")
            click.echo(f"  Quality: {model['quality']}")
            click.echo(f"  Latency: {model['latency']}")
            click.echo(f"  Speed: {model.get('speed', 'N/A')}")
            click.echo(f"  Use Case: {characteristics['use_case']}")
            click.echo(f"  Performance: {characteristics['performance']}")
            click.echo(f"  Recommendation: {characteristics['recommendation']}")
            click.echo("")
        else:
            # Table format for normal output
            row = format_table_row(
                model["name"],
                model["description"],
                model["quality"],
                model["latency"],
                max_name_width,
                max_desc_width,
                max_quality_width,
                max_latency_width,
            )
            click.echo(row)

    # Display table footer
    if verbose < 2:
        click.echo(
            format_table_footer(
                max_name_width, max_desc_width, max_quality_width, max_latency_width
            )
        )

    logger.info(f"Successfully listed {len(models)} models")

    if verbose >= 3:
        logger.debug("Model listing completed successfully")
        for model in models:
            logger.debug(
                f"Model {model['name']}: {model['quality']} quality, {model['latency']} latency"
            )
