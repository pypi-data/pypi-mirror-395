"""
CLI command implementations for OpenAI TTS tool.

This package contains all Click command definitions that wrap the core
library functions with CLI-specific concerns like argument parsing, error
formatting, and user output. By separating command implementations from core
logic, we maintain a clean architecture where business logic remains testable
and reusable outside the CLI context.

Commands handle user interaction, format output for terminal display, and
translate exceptions into helpful error messages with exit codes.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from .completion_commands import completion
from .info_commands import info_command
from .model_commands import list_models_command
from .synthesize_commands import synthesize
from .voice_commands import list_voices_command

__all__ = [
    "synthesize",
    "list_voices_command",
    "list_models_command",
    "info_command",
    "completion",
]
