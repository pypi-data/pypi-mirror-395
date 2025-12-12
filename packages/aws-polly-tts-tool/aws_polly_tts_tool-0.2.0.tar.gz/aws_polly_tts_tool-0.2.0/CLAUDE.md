# AWS Polly TTS Tool - Developer Guide

## Overview

Professional AWS Polly TTS CLI and library with agent-friendly design, Code-RAG optimized documentation, and production-quality code.

**Tech Stack**: Python 3.12+, boto3, click, pydub, uv, mise

## Architecture

### Project Structure

```
aws-polly-tts-tool/
├── aws_polly_tts_tool/
│   ├── __init__.py           # Public API exports for library usage
│   ├── cli.py                # Click CLI entry point
│   ├── voices.py             # VoiceManager - dynamic API fetching
│   ├── engines.py            # Engine metadata, validation, pricing
│   ├── billing.py            # Cost calculation utilities
│   ├── utils.py              # Shared utilities (formatting, validation)
│   ├── logging_config.py     # Multi-level verbosity logging (NEW in v0.2.0)
│   ├── core/                 # Core library (CLI-independent)
│   │   ├── __init__.py
│   │   ├── client.py         # boto3 client initialization
│   │   ├── synthesize.py     # TTS synthesis functions
│   │   └── cost_explorer.py  # AWS Cost Explorer integration
│   └── commands/             # CLI command implementations (Click wrappers)
│       ├── __init__.py
│       ├── synthesize_commands.py
│       ├── voice_commands.py
│       ├── engine_commands.py
│       ├── billing_commands.py
│       └── info_commands.py
├── tests/
│   ├── test_engines.py       # Engine validation tests
│   └── test_utils.py         # Utility function tests
├── pyproject.toml            # Project config, dependencies
├── Makefile                  # Development commands
├── README.md                 # User documentation
└── CLAUDE.md                 # This file
```

### Key Design Principles

1. **Separation of Concerns**
   - `core/`: Pure business logic, raises exceptions
   - `commands/`: CLI wrappers, handle Click decorators and sys.exit
   - `core/` functions are importable and usable as a library

2. **Exception-Based Error Handling**
   - Core functions raise exceptions with helpful messages
   - CLI catches exceptions, formats output, and exits with appropriate codes

3. **Composable Output**
   - Data → stdout (for piping)
   - Logs/errors → stderr (doesn't interfere with pipes)
   - Enables Unix-style composition: `aws-polly-tts-tool list-voices | grep British`

4. **Agent-Friendly Design**
   - Self-documenting help with inline examples
   - Structured error messages with solutions
   - Predictable command patterns
   - Designed for ReAct loops (agents can self-correct)

5. **Code-RAG Optimization**
   - WHY-focused docstrings at all levels (module, class, function)
   - Explains reasoning, not just what the code does
   - Enables semantic code search and AI-assisted development

6. **Multi-Level Verbosity** (v0.2.0+)
   - Progressive logging detail: `-V` (INFO), `-VV` (DEBUG), `-VVV` (TRACE)
   - Logs to stderr, data to stdout (Unix-style composability)
   - Enables debugging without code changes
   - Full AWS SDK visibility at TRACE level

## Development Commands

### Quick Start

```bash
# Clone and setup
git clone <repo>
cd aws-polly-tts-tool
mise use python@3.12
uv sync

# Run checks
make check
```

### Available Commands

```bash
make install              # Install dependencies with uv sync
make format               # Format code with ruff
make lint                 # Lint with ruff
make typecheck            # Type check with mypy (strict mode)
make test                 # Run pytest
make security-bandit      # Run bandit security linter
make security-pip-audit   # Run pip-audit for vulnerabilities
make security-gitleaks    # Run gitleaks secret scanner
make security             # Run all security checks
make check                # Run all checks (lint + typecheck + test + security)
make pipeline             # Full pipeline (format + check + build + install-global)
make build                # Build wheel and source dist
make install-global       # Install globally with uv tool
make clean                # Remove build artifacts
```

### Quality Checks

All code must pass:
- ✅ `ruff format .` - Auto-formatting
- ✅ `ruff check .` - Linting
- ✅ `mypy aws_polly_tts_tool --strict` - Type checking
- ✅ `pytest tests/` - Unit tests
- ✅ `bandit -r aws_polly_tts_tool` - Security linting
- ✅ `pip-audit` - Dependency vulnerability scanning
- ✅ `gitleaks detect` - Secret detection (requires separate install)

## CLI Commands

### synthesize
Main TTS command with full feature support.

**Arguments**:
- `TEXT` (optional positional) - Text to synthesize

**Options**:
- `--stdin / -s` - Read from stdin (enables piping)
- `--voice / -v` - Voice ID (default: Joanna)
- `--output / -o` - Output file path
- `--format / -f` - Audio format (mp3, ogg_vorbis, pcm)
- `--engine / -e` - Engine (standard, neural, generative, long-form)
- `--ssml` - Treat input as SSML markup
- `--show-cost` - Display character count and cost estimate
- `--region / -r` - AWS region override

### list-voices
Dynamic voice listing from Polly API.

**Options**:
- `--engine / -e` - Filter by engine
- `--language / -l` - Filter by language code
- `--gender / -g` - Filter by gender

### list-engines
Display all engines with pricing and features.

### billing
Query AWS Cost Explorer for actual Polly costs.

**Options**:
- `--days / -d` - Number of days (default: 30)
- `--start-date` - Custom start (YYYY-MM-DD)
- `--end-date` - Custom end (YYYY-MM-DD)

### pricing
Show static pricing information and examples.

### info
Display AWS credentials status and tool configuration.

## Library Usage

The tool can be imported and used programmatically:

```python
from aws_polly_tts_tool import (
    get_polly_client,
    synthesize_audio,
    save_speech,
    play_speech,
    VoiceManager,
    calculate_cost,
)

# Initialize
client = get_polly_client()

# Synthesize
audio_bytes, char_count = synthesize_audio(
    client=client,
    text="Hello world",
    voice_id="Joanna",
    engine="neural"
)

# Voice management
vm = VoiceManager(client)
voices = vm.list_voices(engine="neural")

# Cost tracking
cost = calculate_cost(char_count, "neural")
```

## Logging Architecture (v0.2.0+)

### Overview

Multi-level verbosity implementation using Python's standard `logging` module, enabling progressive debug detail without code changes.

### Logging Module: `logging_config.py`

**Location**: `aws_polly_tts_tool/logging_config.py`

**Key Functions**:
- `setup_logging(verbose_count: int)` - Configure logging based on verbosity level
- `get_logger(name: str)` - Get logger instance for a module

**Verbosity Mapping**:
```python
verbose_count == 0  → WARNING  # Quiet (errors/warnings only)
verbose_count == 1  → INFO     # High-level operations
verbose_count >= 2  → DEBUG    # Detailed operations
verbose_count >= 3  → DEBUG    # + boto3/botocore logging (TRACE)
```

### CLI Integration

All commands accept `-V`/`--verbose` with `count=True`:

```python
@click.option(
    "-V",
    "--verbose",
    count=True,
    help="Enable verbose output (-V INFO, -VV DEBUG, -VVV TRACE)",
)
def command(..., verbose: int) -> None:
    setup_logging(verbose)  # First line in command
    logger.info("High-level operation")
    logger.debug("Detailed step")
```

**Note**: We use `-V` (uppercase) instead of `-v` because `-v` conflicts with the `--voice` option in the synthesize command.

### Logging Best Practices

**When to use each level**:
- `logger.warning()` - Critical issues, always shown
- `logger.info()` - High-level operations (voice selection, file operations)
- `logger.debug()` - Detailed steps (validation, character counts, API calls)
- `logger.error()` - Error messages (always shown)
- `logger.debug("...", exc_info=True)` - Full tracebacks (only at DEBUG+)

**Example**:
```python
logger = get_logger(__name__)

def synthesize(...):
    logger.info(f"Using voice: {voice_id} ({engine} engine)")
    logger.debug(f"Validating engine: {engine}")
    logger.debug(f"Synthesized {char_count} characters")

    try:
        # operation
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        logger.debug("Full traceback:", exc_info=True)
```

### Output Streams

**Critical design principle**:
- **Logs → stderr** (`logging.basicConfig(stream=sys.stderr)`)
- **Data → stdout** (`click.echo()` without `err=True`)

**Why**: Enables Unix-style composition:
```bash
aws-polly-tts-tool list-voices -V | grep British  # Logs to stderr, data to stdout
```

### AWS SDK Logging

At `-VVV` (TRACE level), boto3/botocore loggers are enabled:

```python
if verbose_count >= 3:
    logging.getLogger("boto3").setLevel(logging.DEBUG)
    logging.getLogger("botocore").setLevel(logging.DEBUG)
    logging.getLogger("botocore.credentials").setLevel(logging.DEBUG)
```

Shows:
- AWS credential resolution
- HTTP requests/responses
- API operation details
- Service endpoint resolution

## Code Standards

### Type Hints

Required for all functions:

```python
def function(param: str, optional: int | None = None) -> dict[str, Any]:
    """Docstring here."""
    pass
```

### Docstrings (Code-RAG Format)

**Code-RAG Optimized**: All docstrings explain reasoning and design decisions in natural language for semantic code search and AI-assisted development.

```python
"""
Module/function description.

Explain the reasoning and design decisions here in natural language.
This helps with semantic code search and AI-assisted development by
providing context about WHY the code exists and HOW it fits into the
broader architecture.

Args:
    param: Description

Returns:
    Description

Raises:
    ValueError: When...
"""
```

**Key principles**:
- Natural language (no "WHY:" prefix - removed in v0.2.0)
- Explain intent and reasoning, not just implementation
- Focus on architectural context and design decisions
- Support semantic search and AI code understanding
- All 17 modules have comprehensive Code-RAG docstrings

### Error Messages

Include problem + solution + reference:

```python
raise ValueError(
    "Voice 'invalid' not found.\n\n"
    "Available voices: joanna, matthew, ...\n\n"
    "Use 'aws-polly-tts-tool list-voices' to see all voices."
)
```

## Important Notes

### Dependencies

- **boto3**: AWS SDK for Polly API calls
- **pydub**: Audio playback (Python 3.12 only - see Known Issues)
- **click**: CLI framework with decorators

### AWS Authentication

Uses standard AWS credential chain:
1. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
2. `~/.aws/credentials` file
3. IAM role (when running on EC2/ECS/Lambda)

### Voice Management

- **Always fetches from API** (no local caching)
- Ensures latest voices without tool updates
- Session-level cache to avoid redundant API calls

### Cost Tracking

**Dual approach**:
1. **Immediate estimates**: Calculate from character count + engine pricing
2. **Actual billing**: Query Cost Explorer API for real AWS charges

### Engine Compatibility

Not all voices support all engines. The tool validates:
- Voice exists
- Engine is valid
- Voice supports specified engine

### Version Syncing

Keep version consistent across:
- `pyproject.toml` `[project] version`
- `cli.py` `@click.version_option(version="...")`
- `__init__.py` `__version__ = "..."`

## Security

### Integrated Security Tools

The project integrates three security tools into the development pipeline:

1. **bandit** - Python security linter
   - Scans code for common security issues (SQL injection, hardcoded passwords, unsafe functions)
   - Configuration in `pyproject.toml` excludes test directories and skips B101 (assert_used)
   - Run with: `make security-bandit`

2. **pip-audit** - Dependency vulnerability scanner
   - Checks Python dependencies for known CVEs from PyPI
   - No configuration needed (uses uv's dependency resolution)
   - Run with: `make security-pip-audit`

3. **gitleaks** - Secret detection
   - Scans git history for leaked credentials, API keys, and secrets
   - Configuration in `.gitleaks.toml` with allowlist for false positives
   - **Requires separate installation**: `brew install gitleaks` (macOS) or from [GitHub releases](https://github.com/gitleaks/gitleaks/releases)
   - Run with: `make security-gitleaks`

### Running Security Checks

```bash
# Run individual security tools
make security-bandit
make security-pip-audit
make security-gitleaks

# Run all security checks
make security

# Security checks are included in pipeline
make check      # Includes security
make pipeline   # Includes security
```

### Security Configuration Files

- `pyproject.toml` - Bandit configuration
  - Excludes: tests, .venv, venv directories
  - Skips: B101 (assert_used - common in tests)

- `.gitleaks.toml` - Gitleaks configuration
  - Uses default gitleaks rules
  - Allowlist for test fixtures and example values
  - Excludes test files, markdown, and documentation

### Handling Security Findings

**False Positives**:
- Bandit: Add `# nosec` comment to suppress, or update `pyproject.toml` to skip checks
- Gitleaks: Update `.gitleaks.toml` allowlist with regex patterns

**Real Issues**:
- Address security findings before committing
- Pipeline will fail if security checks detect issues
- Review and fix issues, then re-run `make security`

## Known Issues & Future Fixes

### pydub Python 3.13+ Incompatibility

**Issue**: pydub depends on `audioop` module, removed in Python 3.13.

**Current workaround**:
- Use Python 3.12: `mise use python@3.12`
- Use `--output` flag (file saving works on any version)

**Future fix**:
Replace pydub with Python 3.13+ compatible library:
1. **pygame** - Cross-platform, mature, good docs
2. **sounddevice** - Lower-level, more control
3. **simpleaudio** - Lightweight alternative

**Implementation steps** (when fixed):
```python
# Remove pydub import
from pydub import AudioSegment  # DELETE
from pydub.playback import play  # DELETE

# Add pygame
import pygame

# Update play_speech function
def play_speech(...):
    audio_bytes, char_count = synthesize_audio(...)

    # pygame implementation
    pygame.mixer.init()
    audio_stream = BytesIO(audio_bytes)
    pygame.mixer.music.load(audio_stream)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    return char_count
```

## Testing

### Running Tests

```bash
# All tests
make test

# With verbose output
uv run pytest tests/ -v

# Specific test file
uv run pytest tests/test_engines.py -v
```

### Test Structure

- `test_engines.py` - Engine validation without AWS/pydub dependencies
- `test_utils.py` - Utility functions (formatting, validation)
- **Note**: Core TTS functions require AWS credentials and pydub (manual testing)

### Manual Testing

With AWS credentials configured:

```bash
# Test synthesis (file output)
aws-polly-tts-tool synthesize "Hello world" --output test.mp3

# Test voice listing
aws-polly-tts-tool list-voices --engine neural | head -10

# Test cost tracking
aws-polly-tts-tool synthesize "Hello" --show-cost
```

## Build & Deploy

```bash
# Build distribution
uv build

# Install globally
uv tool install dist/aws_polly_tts_tool-0.1.0-py3-none-any.whl --force

# Verify
aws-polly-tts-tool --version
aws-polly-tts-tool --help
```

## Contributing

When making changes:

1. Create feature branch
2. Make changes with WHY-focused docstrings
3. Run `make pipeline` (must pass)
4. Test manually with AWS credentials
5. Update README.md and CLAUDE.md if needed
6. Commit with descriptive message
7. Create PR

## Resources

### External Documentation
- [Amazon Polly Docs](https://docs.aws.amazon.com/polly/)
- [Boto3 Polly Reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html)
- [Click Documentation](https://click.palletsprojects.com/)
- [uv Documentation](https://github.com/astral-sh/uv)

### Internal References
- [TTS Pipeline Architecture](references/tts-pipeline.md) - Detailed explanation of how text-to-speech processing works, including dependencies (boto3, pydub, ffmpeg) and their roles

---

**Note**: This code was generated with assistance from AI coding tools (Claude Code) and has been reviewed and tested by a human.
