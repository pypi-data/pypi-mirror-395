"""
Info command for displaying tool configuration information.

This module provides the info command that shows current configuration
including API key status, default voice, model, and output formats.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import os

import click

from openai_tts_tool.core.client import test_credentials
from openai_tts_tool.logging_config import get_logger
from openai_tts_tool.models import DEFAULT_MODEL, MODELS
from openai_tts_tool.voices import DEFAULT_VOICE, VOICES

logger = get_logger(__name__)


def mask_api_key(api_key: str | None) -> str:
    """Mask API key for display by showing only first and last 4 characters.

    Args:
        api_key: The API key to mask

    Returns:
        Masked API key string or 'Not set' if None
    """
    if not api_key:
        return "Not set"

    if len(api_key) <= 8:
        return "*" * len(api_key)

    return f"{api_key[:4]}{'*' * (len(api_key) - 8)}{api_key[-4:]}"


def get_api_key_status() -> tuple[str, str]:
    """Check and return API key status information.

    Returns:
        Tuple of (status, masked_key) where status is one of:
        - 'configured' - API key is set and valid format
        - 'not_configured' - API key not set
        - 'invalid_format' - API key doesn't start with 'sk-'
        - 'test_failed' - API key format looks good but test failed
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return "not_configured", "Not set"

    if not api_key.strip():
        return "invalid_format", "Empty"

    if not api_key.startswith("sk-"):
        return "invalid_format", mask_api_key(api_key)

    # Try to test the credentials
    try:
        test_credentials()
        return "configured", mask_api_key(api_key)
    except Exception as e:
        logger.debug(f"API key test failed: {e}")
        return "test_failed", mask_api_key(api_key)


@click.command("info")
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Verbose output: -v (INFO), -vv (DEBUG), -vvv (TRACE with details)",
)
def info_command(verbose: int) -> None:
    """Display tool configuration and status information.

    Shows current configuration including OpenAI API key status,
    default voice, default model, and available output formats.

    Examples:

    \b
        # Basic configuration info
        openai-tts-tool info

    \b
        # Verbose output with additional details
        openai-tts-tool info -v

    \b
        # Very verbose output with debug information
        openai-tts-tool info -vvv

    \b
    Output Format:
        Displays configuration sections:
        - OpenAI API: Key status and validation results
        - Defaults: Default voice and model settings
        - Available Voices: List of supported TTS voices
        - Available Models: List of supported TTS models
        - Output Formats: Supported audio formats for synthesis
    """

    click.echo("OpenAI TTS Tool Configuration")
    click.echo("=" * 40)

    # API Key Status
    click.echo("\n🔑 OpenAI API:")
    api_status, masked_key = get_api_key_status()

    status_symbols = {
        "configured": "✅",
        "not_configured": "❌",
        "invalid_format": "⚠️",
        "test_failed": "❌",
    }

    status_messages = {
        "configured": "Configured and working",
        "not_configured": "Not configured",
        "invalid_format": "Invalid format",
        "test_failed": "Format OK but test failed",
    }

    symbol = status_symbols.get(api_status, "❓")
    message = status_messages.get(api_status, "Unknown status")

    click.echo(f"   Status: {symbol} {message}")
    click.echo(f"   API Key: {masked_key}")

    if verbose >= 1:
        if api_status == "not_configured":
            click.echo("   Setup: export OPENAI_API_KEY='sk-...'")
        elif api_status == "invalid_format":
            click.echo("   Help: API keys should start with 'sk-'")
        elif api_status == "test_failed":
            click.echo("   Help: Check if key is active and has credits")

    # Default Settings
    click.echo("\n⚙️  Defaults:")
    click.echo(f"   Voice: {DEFAULT_VOICE}")
    click.echo(f"   Model: {DEFAULT_MODEL}")

    # Available Voices
    click.echo(f"\n🎙️  Available Voices ({len(VOICES)}):")
    for voice in sorted(VOICES.keys()):
        marker = " (default)" if voice == DEFAULT_VOICE else ""
        click.echo(f"   {voice}{marker}")

    if verbose >= 2:
        click.echo("\n   Voice Descriptions:")
        for voice, description in sorted(VOICES.items()):
            click.echo(f"   {voice}: {description}")

    # Available Models
    click.echo(f"\n🤖 Available Models ({len(MODELS)}):")
    for model_name in sorted(MODELS.keys()):
        model_info = MODELS[model_name]
        marker = " (default)" if model_name == DEFAULT_MODEL else ""
        quality = model_info.get("quality", "unknown")
        click.echo(f"   {model_name} - {quality}{marker}")

    if verbose >= 2:
        click.echo("\n   Model Details:")
        for model_name in sorted(MODELS.keys()):
            model_info = MODELS[model_name]
            click.echo(f"   {model_name}:")
            for key, value in model_info.items():
                if key != "name":
                    click.echo(f"     {key}: {value}")

    # Output Formats
    output_formats = ["mp3", "opus", "aac", "flac", "wav", "pcm"]
    click.echo(f"\n📄 Output Formats ({len(output_formats)}):")
    click.echo(f"   {', '.join(output_formats)}")

    if verbose >= 2:
        click.echo("\n   Format Notes:")
        click.echo("   mp3: Most compatible, good compression")
        click.echo("   opus: Better compression than mp3")
        click.echo("   aac: Good quality, widely supported")
        click.echo("   flac: Lossless compression")
        click.echo("   wav: Uncompressed, highest quality")
        click.echo("   pcm: Raw audio data")

    if verbose >= 3:
        click.echo("\n🐛 Debug Information:")
        click.echo(f"   Verbosity Level: {verbose}")
        click.echo("   Environment:")
        click.echo(f"     OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not set'}")

        # Try to get live API info if credentials work
        if api_status == "configured":
            try:
                from openai_tts_tool.core.client import get_api_info

                api_info = get_api_info()
                click.echo("   API Connection:")
                click.echo(f"     Status: {api_info.get('api_status', 'unknown')}")
                click.echo(f"     Total Models: {api_info.get('models_count', 0)}")
                tts_models = api_info.get("available_tts_models", [])
                # Handle different types for tts_models
                if isinstance(tts_models, list):
                    tts_models_str = ", ".join(str(model) for model in tts_models)
                else:
                    tts_models_str = str(tts_models)
                click.echo(f"     TTS Models: {tts_models_str}")
            except Exception as e:
                logger.debug(f"Failed to get API info: {e}")
                click.echo("   API Connection: Failed to retrieve info")

    click.echo()  # Final newline for better spacing
