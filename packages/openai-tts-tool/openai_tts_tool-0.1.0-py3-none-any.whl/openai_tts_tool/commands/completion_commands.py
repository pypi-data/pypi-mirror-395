"""
Shell completion command for openai-tts-tool.

Provides user-friendly shell completion generation following the industry-standard
pattern used by kubectl, helm, and docker. Users can generate completion scripts
for bash, zsh, or fish shells using an intuitive command interface instead of
environment variables.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click
from click.shell_completion import BashComplete, FishComplete, ZshComplete


@click.command()
@click.argument("shell", type=click.Choice(["bash", "zsh", "fish"]))
def completion(shell: str) -> None:
    """Generate shell completion script.

    Outputs a completion script for the specified shell that can be sourced
    to enable tab completion for all openai-tts-tool commands, options,
    and arguments. This follows the familiar pattern used by major CLI tools.

    SHELL: The shell type (bash, zsh, or fish)

    \b
    Installation Instructions:

    \b
    # Bash (add to ~/.bashrc for persistent completion):
    eval "$(openai-tts-tool completion bash)"

    \b
    # Zsh (add to ~/.zshrc for persistent completion):
    eval "$(openai-tts-tool completion zsh)"

    \b
    # Fish (one-time installation to completions directory):
    openai-tts-tool completion fish > ~/.config/fish/completions/openai-tts-tool.fish

    \b
    # File-based installation (recommended for better performance):
    openai-tts-tool completion bash > ~/.openai-tts-tool-complete.bash
    echo 'source ~/.openai-tts-tool-complete.bash' >> ~/.bashrc

    \b
    After installation, restart your shell or source the config file:
        source ~/.bashrc  # for bash
        source ~/.zshrc   # for zsh

    \b
    Examples:

    \b
        # Generate bash completion script
        openai-tts-tool completion bash

    \b
        # Generate and install zsh completion immediately
        eval "$(openai-tts-tool completion zsh)"

    \b
        # Save fish completion to file
        openai-tts-tool completion fish > ~/.config/fish/completions/openai-tts-tool.fish
    """
    ctx = click.get_current_context()

    # Map shell names to completion classes
    completion_classes = {
        "bash": BashComplete,
        "zsh": ZshComplete,
        "fish": FishComplete,
    }

    completion_class = completion_classes.get(shell)

    if completion_class:
        # Create completer instance with current CLI context
        completer = completion_class(
            cli=ctx.find_root().command,
            ctx_args={},
            prog_name=ctx.find_root().info_name or "openai-tts-tool",
            complete_var="_OPENAI_TTS_TOOL_COMPLETE",
        )
        # Output the completion script
        click.echo(completer.source())
    else:
        raise click.BadParameter(
            f"Unsupported shell: {shell}\n\n"
            "Supported shells: bash, zsh, fish\n\n"
            "Use 'openai-tts-tool completion --help' for installation instructions."
        )
