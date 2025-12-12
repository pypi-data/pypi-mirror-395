---
description: Show system configuration and API key status
argument-hint:
---

Display system configuration and OpenAI API key status.

## Usage

```bash
openai-tts-tool info [OPTIONS]
```

## Options

- `--format FORMAT` / `-f FORMAT`: Output format (table/json)
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

## Examples

```bash
# Show basic info
openai-tts-tool info

# JSON format for automation
openai-tts-tool info --format json

# Check API key status
openai-tts-tool info | grep "API Key"
```

## Output

Returns system configuration including API key status, version info, and available resources.