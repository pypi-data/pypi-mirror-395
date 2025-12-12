---
description: Generate shell completion scripts
argument-hint: shell
---

Generate shell completion script for bash, zsh, or fish to enable tab completion.

## Usage

```bash
aws-polly-tts-tool completion [bash|zsh|fish]
```

## Arguments

- `SHELL`: Shell type (bash, zsh, or fish) - required

## Examples

```bash
# Generate bash completion
aws-polly-tts-tool completion bash

# Install for bash (add to ~/.bashrc)
eval "$(aws-polly-tts-tool completion bash)"

# Install for zsh (add to ~/.zshrc)
eval "$(aws-polly-tts-tool completion zsh)"

# Install for fish
aws-polly-tts-tool completion fish > ~/.config/fish/completions/aws-polly-tts-tool.fish
```

## Output

Returns shell-specific completion script. After installation, restart shell or source config file.
