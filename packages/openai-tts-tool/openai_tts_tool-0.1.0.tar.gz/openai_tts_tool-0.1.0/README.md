<p align="center">
  <img src="https://github.com/dnvriend/openai-tts-tool/blob/main/.github/assets/logo-web.png" alt="openai-tts-tool Logo" width="120"/>
</p>

# openai-tts-tool

[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://github.com/python/mypy)
[![Built with Claude Code](https://img.shields.io/badge/Built_with-Claude_Code-5A67D8.svg)](https://www.anthropic.com/claude/code)


A command-line interface for OpenAI Text-to-Speech API.

## Features

- Convert text to natural-sounding speech
- Six high-quality voices with different characteristics
- Two TTS models (tts-1 and tts-1-hd) for speed vs quality
- Multiple audio formats: mp3, opus, aac, flac
- Stream to speakers or save to files
- Adjustable speech speed (0.25 to 4.0)
- Multi-level verbosity logging
- Shell completion support

## Installation

```bash
# Prerequisites
# - Python 3.14+
# - uv package manager

# Clone and install globally
git clone https://github.com/dnvriend/openai-tts-tool.git
cd openai-tts-tool
uv tool install .

# Verify installation
openai-tts-tool --version
```

## Configuration

Set the OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key-here"

# Add to shell profile for persistence
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc  # or ~/.zshrc
source ~/.bashrc  # or ~/.zshrc
```

## Usage

```bash
# Basic synthesis (stream to speakers)
openai-tts-tool synthesize "Hello, world!"

# Save to file with specific voice
openai-tts-tool synthesize "Hello, world!" --voice nova --output hello.mp3

# High-quality synthesis with custom settings
openai-tts-tool synthesize "Welcome" \
    --voice alloy \
    --model tts-1-hd \
    --output welcome.mp3 \
    --format mp3 \
    --speed 1.2

# Read from stdin
echo "Hello from stdin" | openai-tts-tool synthesize --stdin --output hello.mp3

# List available voices and models
openai-tts-tool list-voices
openai-tts-tool list-models

# Multi-level verbosity for debugging
openai-tts-tool -v synthesize "Test"           # INFO level
openai-tts-tool -vv synthesize "Test"          # DEBUG level
openai-tts-tool -vvv synthesize "Test"         # TRACE with library logs
```

## Options

### Synthesize Command

| Option | Short | Description |
|--------|-------|-------------|
| `--voice` | `-v` | Voice to use (alloy, echo, fable, onyx, nova, shimmer) |
| `--model` | `-m` | TTS model (tts-1, tts-1-hd) |
| `--output` | `-o` | Output file path (default: stream to speakers) |
| `--format` | `-f` | Audio format (mp3, opus, aac, flac) |
| `--speed` | `-s` | Speech speed (0.25 to 4.0) |
| `--stdin` | | Read text from stdin |

### Global Options

| Option | Short | Description |
|--------|-------|-------------|
| `--verbose` | `-v` | Verbose output: -v (INFO), -vv (DEBUG), -vvv (TRACE with library logs) |
| `--version` | | Show version information |
| `--help` | `-h` | Show help message |

## Voices and Models

### Voices

| Voice | Description |
|-------|-------------|
| **alloy** | Balanced, natural voice (default) |
| **echo** | Deeper, authoritative voice |
| **fable** | Warm, engaging storyteller |
| **onyx** | Deep, confident voice |
| **nova** | Clear, professional voice |
| **shimmer** | Softer, expressive voice |

### Models

| Model | Quality | Speed | Use Case |
|-------|---------|-------|----------|
| **tts-1** | Standard | Fast | Real-time applications |
| **tts-1-hd** | High | Slower | High-quality audio production |

### Audio Formats

| Format | Quality | Use Case |
|--------|---------|----------|
| **mp3** | Good | Maximum compatibility |
| **opus** | Excellent | Streaming, low bandwidth |
| **aac** | Very Good | Apple devices |
| **flac** | Lossless | High-fidelity production |

## Library Usage

```python
from openai_tts_tool import TTSClient

client = TTSClient(api_key="your-key")

# Stream to speakers
client.synthesize("Hello, world!", voice="alloy")

# Save to file
client.synthesize(
    "Hello, world!",
    voice="nova",
    model="tts-1-hd",
    output="hello.mp3",
    speed=1.2
)
```

## Development

```bash
make install          # Install dependencies
make format           # Format code with ruff
make lint             # Run linting with ruff
make typecheck        # Run type checking with mypy
make test             # Run tests with pytest
make security         # Run all security checks
make check            # Run all checks (lint, typecheck, test, security)
make pipeline         # Run full pipeline
make build            # Build package
make run ARGS="..."   # Run openai-tts-tool locally
```

## License

MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Dennis Vriend - [GitHub](https://github.com/dnvriend)
