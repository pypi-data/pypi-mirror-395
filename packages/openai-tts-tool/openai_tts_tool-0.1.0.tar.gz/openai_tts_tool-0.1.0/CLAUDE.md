# openai-tts-tool - Project Specification

## Goal

A CLI that provides tts using OpenAI

## What is openai-tts-tool?

`openai-tts-tool` is a command-line utility built with modern Python tooling and best practices.

## Technical Requirements

### Runtime

- Python 3.14+
- Installable globally with mise
- Cross-platform (macOS, Linux, Windows)

### Dependencies

- `click` - CLI framework

### Development Dependencies

- `ruff` - Linting and formatting
- `mypy` - Type checking
- `pytest` - Testing framework
- `bandit` - Security linting
- `pip-audit` - Dependency vulnerability scanning
- `gitleaks` - Secret detection (requires separate installation)

## CLI Commands

```bash
openai-tts-tool [GLOBAL_OPTIONS] COMMAND [COMMAND_OPTIONS]
```

### Global Options

- `-v, --verbose` - Multi-level verbosity (count flag: -v, -vv, -vvv)
  - `-v` (count=1): INFO level logging - high-level operations
  - `-vv` (count=2): DEBUG level logging - detailed debugging with line numbers
  - `-vvv` (count=3+): TRACE level - includes library internals (OpenAI, urllib3, httpx)
- `--help` / `-h` - Show help message
- `--version` - Show version

### Commands

- `synthesize TEXT` - Convert text to speech (main functionality)
- `list-voices` - Display available TTS voices with descriptions
- `list-models` - Display available TTS models with characteristics
- `info` - Show system configuration and API key status
- `completion SHELL` - Generate shell completion scripts (bash, zsh, fish)

## Project Structure

```
openai-tts-tool/
├── openai_tts_tool/
│   ├── __init__.py
│   ├── cli.py            # Click CLI entry point with logging setup
│   ├── completion.py     # Shell completion command
│   ├── logging_config.py # Multi-level verbosity logging with library support
│   ├── utils.py          # Utility functions
│   ├── commands/         # CLI command implementations
│   │   ├── __init__.py
│   │   ├── synthesize_commands.py  # Main TTS functionality
│   │   ├── voice_commands.py       # Voice listing commands
│   │   ├── model_commands.py       # Model listing commands
│   │   ├── info_commands.py        # System info command
│   │   └── completion_commands.py  # Shell completion
│   ├── core/            # Core business logic
│   │   ├── __init__.py
│   │   ├── synthesize.py  # TTS synthesis functions
│   │   ├── client.py      # OpenAI client management
│   ├── voices.py         # Voice definitions and validation
│   └── models.py         # Model definitions and validation
├── tests/
│   ├── __init__.py
│   └── test_utils.py
├── pyproject.toml        # Project configuration
├── README.md             # User documentation
├── CLAUDE.md             # This file
├── Makefile              # Development commands
├── LICENSE               # MIT License
├── .mise.toml            # mise configuration
├── .gitleaks.toml        # Gitleaks configuration
└── .gitignore
```

## Code Style

- Type hints for all functions
- Docstrings for all public functions
- Follow PEP 8 via ruff
- 100 character line length
- Strict mypy checking

## Development Workflow

```bash
# Install dependencies
make install

# Run linting
make lint

# Format code
make format

# Type check
make typecheck

# Run tests
make test

# Security scanning
make security-bandit       # Python security linting
make security-pip-audit    # Dependency CVE scanning
make security-gitleaks     # Secret detection
make security              # Run all security checks

# Run all checks (includes security)
make check

# Full pipeline (includes security)
make pipeline
```

## Security

The template includes three lightweight security tools:

1. **bandit** - Python code security linting
   - Detects: SQL injection, hardcoded secrets, unsafe functions
   - Speed: ~2-3 seconds

2. **pip-audit** - Dependency vulnerability scanning
   - Detects: Known CVEs in dependencies
   - Speed: ~2-3 seconds

3. **gitleaks** - Secret and API key detection
   - Detects: AWS keys, GitHub tokens, API keys, private keys
   - Speed: ~1 second
   - Requires: `brew install gitleaks` (macOS)

All security checks run automatically in `make check` and `make pipeline`.

## Multi-Level Verbosity Logging

The template includes a centralized logging system with progressive verbosity levels.

### Implementation Pattern

1. **logging_config.py** - Centralized logging configuration
   - `setup_logging(verbose_count)` - Configure logging based on -v count
   - `get_logger(name)` - Get logger instance for module
   - Maps verbosity to Python logging levels (WARNING/INFO/DEBUG)
   - Configures library logging at TRACE level (-vvv)

2. **CLI Integration** - Centralized in main CLI group
   ```python
   # Main CLI group handles logging setup
   @click.group()
   @click.option("-v", "--verbose", count=True)
   def main(verbose: int):
       setup_logging(verbose)  # Single point of logging setup

   # Individual commands just use the logger
   from openai_tts_tool.logging_config import get_logger

   logger = get_logger(__name__)

   @click.command()
   def command():
       logger.info("Operation started")
       logger.debug("Detailed info")
   ```

3. **Logging Levels**
   - **0 (no -v)**: WARNING only - production/quiet mode
   - **1 (-v)**: INFO - high-level operations (module names only)
   - **2 (-vv)**: DEBUG - detailed debugging with line numbers
   - **3+ (-vvv)**: TRACE - includes OpenAI, urllib3, httpx library internals

4. **Best Practices**
   - Always log to stderr (keeps stdout clean for piping)
   - Use structured messages with placeholders: `logger.info("Found %d items", count)`
   - Call `setup_logging()` first in every command
   - Use `get_logger(__name__)` at module level
   - For TRACE level, enable third-party library loggers in `logging_config.py`

5. **Customizing Library Logging**
   Edit `logging_config.py` to add project-specific libraries:
   ```python
   if verbose_count >= 3:
       logging.getLogger("requests").setLevel(logging.DEBUG)
       logging.getLogger("urllib3").setLevel(logging.DEBUG)
   ```

## Shell Completion

The template includes shell completion for bash, zsh, and fish following the Click Shell Completion Pattern.

### Implementation

1. **completion.py** - Separate module for completion command
   - Uses Click's `BashComplete`, `ZshComplete`, `FishComplete` classes
   - Generates shell-specific completion scripts
   - Includes installation instructions in help text

2. **CLI Integration** - Added as subcommand
   ```python
   from openai_tts_tool.completion import completion_command

   @click.group(invoke_without_command=True)
   def main(ctx: click.Context):
       # Default behavior when no subcommand
       if ctx.invoked_subcommand is None:
           # Main command logic here
           pass

   # Add completion subcommand
   main.add_command(completion_command)
   ```

3. **Usage Pattern** - User-friendly command
   ```bash
   # Generate completion script
   openai-tts-tool completion bash
   openai-tts-tool completion zsh
   openai-tts-tool completion fish

   # Install (eval or save to file)
   eval "$(openai-tts-tool completion bash)"
   ```

4. **Supported Shells**
   - **Bash** (≥ 4.4) - Uses bash-completion
   - **Zsh** (any recent) - Uses zsh completion system
   - **Fish** (≥ 3.0) - Uses fish completion system
   - **PowerShell** - Not supported by Click

5. **Installation Methods**
   - **Temporary**: `eval "$(openai-tts-tool completion bash)"`
   - **Permanent**: Add eval to ~/.bashrc or ~/.zshrc
   - **File-based** (recommended): Save to dedicated completion file

### Adding More Commands

The CLI uses `@click.group()` for extensibility. To add new commands:

1. Create new command module in `openai_tts_tool/`
2. Import and add to CLI group:
   ```python
   from openai_tts_tool.new_command import new_command
   main.add_command(new_command)
   ```

3. Completion will automatically work for new commands and their options

## Installation Methods

### Global installation with mise

```bash
cd /path/to/openai-tts-tool
mise use -g python@3.14
uv sync
uv tool install .
```

After installation, `openai-tts-tool` command is available globally.

### Local development

```bash
uv sync
uv run openai-tts-tool [args]
```
