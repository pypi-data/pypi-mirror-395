---
description: Display voice engines with pricing and features
argument-hint:
---

Display all available AWS Polly voice engines with technology, pricing, and use cases.

## Usage

```bash
aws-polly-tts-tool list-engines
```

## Examples

```bash
# Show all engines with details
aws-polly-tts-tool list-engines
```

## Output

Returns table with Engine, Technology, Price/1M chars, Char Limit, and Best For columns.

Includes:
- Standard ($4/1M) - Traditional TTS
- Neural ($16/1M) - Natural voices
- Generative ($30/1M) - Highest quality
- Long-form ($100/1M) - Audiobooks
