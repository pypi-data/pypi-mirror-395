---
description: Display AWS credentials and tool config
argument-hint:
---

Display AWS Polly tool configuration, credentials status, and helpful command references.

## Usage

```bash
aws-polly-tts-tool info
```

## Examples

```bash
# Show configuration and verify credentials
aws-polly-tts-tool info
```

## Output

Returns:
- AWS credential status (Valid/Invalid)
- AWS Account ID, User ID, ARN
- Available engines (standard, neural, generative, long-form)
- Output formats (mp3, ogg_vorbis, pcm)
- Useful command examples

Use this to verify AWS authentication and discover tool capabilities.
