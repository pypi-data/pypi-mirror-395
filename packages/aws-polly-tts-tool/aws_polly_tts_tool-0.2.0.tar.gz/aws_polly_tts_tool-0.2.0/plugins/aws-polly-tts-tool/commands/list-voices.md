---
description: List available Polly voices with filters
argument-hint:
---

List all available AWS Polly voices with optional filtering by engine, language, and gender.

## Usage

```bash
aws-polly-tts-tool list-voices [OPTIONS]
```

## Options

- `--engine TEXT` / `-e TEXT`: Filter by engine (standard, neural, generative, long-form)
- `--language TEXT` / `-l TEXT`: Filter by language code (e.g., en-US, es-ES)
- `--gender TEXT` / `-g TEXT`: Filter by gender (Female, Male)
- `--region TEXT` / `-r TEXT`: AWS region override
- `-V/-VV/-VVV`: Verbosity (INFO/DEBUG/TRACE)

## Examples

```bash
# List all voices
aws-polly-tts-tool list-voices

# Filter by engine
aws-polly-tts-tool list-voices --engine neural

# Filter by language
aws-polly-tts-tool list-voices --language en-US

# Combine filters
aws-polly-tts-tool list-voices --engine neural --language en --gender Female

# Search with grep
aws-polly-tts-tool list-voices | grep British
```

## Output

Returns table with Voice, Gender, Language, Engines, Description.
