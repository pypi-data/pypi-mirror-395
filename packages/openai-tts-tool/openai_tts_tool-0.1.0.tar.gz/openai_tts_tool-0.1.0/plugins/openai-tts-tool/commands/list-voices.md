---
description: Display available TTS voices with descriptions
argument-hint:
---

List all available OpenAI TTS voices with their descriptions.

## Usage

```bash
openai-tts-tool list-voices [OPTIONS]
```

## Options

- `--format FORMAT` / `-f FORMAT`: Output format (table/json)
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

## Examples

```bash
# Table format (default)
openai-tts-tool list-voices

# JSON format for scripting
openai-tts-tool list-voices --format json

# Pipe to jq for filtering
openai-tts-tool list-voices --format json | jq '.[] | select(.language == "en")'
```

## Output

Returns list of available voices with name, description, and language support.