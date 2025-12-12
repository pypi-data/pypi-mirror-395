---
description: Convert text to speech using AWS Polly
argument-hint: text
---

Convert text to speech using Amazon Polly with support for multiple engines and voices.

## Usage

```bash
aws-polly-tts-tool synthesize "TEXT" [OPTIONS]
```

## Arguments

- `TEXT`: Text to synthesize (required, or use `--stdin`)
- `--stdin` / `-s`: Read text from stdin (for piping)
- `--voice TEXT`: Voice ID (default: Joanna)
- `--output PATH` / `-o PATH`: Save to file instead of playing
- `--format TEXT` / `-f TEXT`: Audio format (mp3, ogg_vorbis, pcm)
- `--engine TEXT` / `-e TEXT`: Engine (standard, neural, generative, long-form)
- `--ssml`: Treat input as SSML markup
- `--show-cost`: Display character count and cost estimate
- `--region TEXT` / `-r TEXT`: AWS region override
- `-V/-VV/-VVV`: Verbosity (INFO/DEBUG/TRACE)

## Examples

```bash
# Play with default voice (Joanna, neural)
aws-polly-tts-tool synthesize "Hello world"

# Use different voice and engine
aws-polly-tts-tool synthesize "Hello" --voice Matthew --engine generative

# Save to file
aws-polly-tts-tool synthesize "Hello world" --output speech.mp3

# Read from stdin
echo "Hello world" | aws-polly-tts-tool synthesize --stdin

# SSML with pause
aws-polly-tts-tool synthesize '<speak>Hello <break time="500ms"/> world</speak>' --ssml
```

## Output

Audio played through speakers or saved to file with character count.
