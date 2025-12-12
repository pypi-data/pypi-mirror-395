---
description: Generate shell completion scripts for bash/zsh/fish
argument-hint: shell
---

Generate shell completion script for the specified SHELL.

## Usage

```bash
openai-tts-tool completion SHELL
```

## Arguments

- `SHELL`: Shell type (bash/zsh/fish) (required)

## Examples

```bash
# Generate bash completion
openai-tts-tool completion bash

# Generate zsh completion
openai-tts-tool completion zsh

# Generate fish completion
openai-tts-tool completion fish

# Install directly (eval)
eval "$(openai-tts-tool completion bash)"
```

## Output

Returns shell-specific completion script for auto-completion support.