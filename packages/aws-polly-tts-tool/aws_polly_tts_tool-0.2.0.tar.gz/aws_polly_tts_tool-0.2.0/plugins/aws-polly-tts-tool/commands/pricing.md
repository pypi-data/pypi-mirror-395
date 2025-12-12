---
description: Show Polly pricing and cost examples
argument-hint:
---

Display AWS Polly pricing information for all engines with cost examples.

## Usage

```bash
aws-polly-tts-tool pricing
```

## Examples

```bash
# Show pricing table
aws-polly-tts-tool pricing
```

## Output

Returns pricing table with:
- Engine name and cost per 1M characters
- Technology type (Concatenative/Neural/Generative)
- Quality level
- Character limit per request
- Concurrent request limits
- Free tier information
- Best use cases
- Cost examples (1,000 words, audiobooks)
