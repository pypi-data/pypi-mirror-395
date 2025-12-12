---
description: Display available TTS models with characteristics
argument-hint:
---

List all available OpenAI TTS models with their characteristics.

## Usage

```bash
openai-tts-tool list-models [OPTIONS]
```

## Options

- `--format FORMAT` / `-f FORMAT`: Output format (table/json)
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

## Examples

```bash
# Table format (default)
openai-tts-tool list-models

# JSON format for scripting
openai-tts-tool list-models --format json

# Pipe to jq for filtering HD models
openai-tts-tool list-models --format json | jq '.[] | select(.name | contains("hd"))'
```

## Output

Returns list of available TTS models with name, description, and capabilities.