---
description: Convert text to speech using OpenAI TTS
argument-hint: text
---

Convert TEXT to speech using OpenAI's text-to-speech API.

## Usage

```bash
openai-tts-tool synthesize TEXT [OPTIONS]
```

## Arguments

- `TEXT`: Text to convert to speech (required)
- `--voice VOICE` / `-V VOICE`: Voice model (default: alloy)
- `--model MODEL` / `-m MODEL`: TTS model (default: tts-1)
- `--output FILE` / `-o FILE`: Output file path (default: output.mp3)
- `--speed SPEED` / `-s SPEED`: Speech speed 0.25-4.0 (default: 1.0)
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

## Examples

```bash
# Basic synthesis
openai-tts-tool synthesize "Hello world"

# With specific voice and output
openai-tts-tool synthesize "Hello world" --voice nova --output hello.mp3

# Slow speed with HD model
openai-tts-tool synthesize "This is important" --model tts-1-hd --speed 0.8
```

## Output

Generates MP3 audio file with the synthesized speech.