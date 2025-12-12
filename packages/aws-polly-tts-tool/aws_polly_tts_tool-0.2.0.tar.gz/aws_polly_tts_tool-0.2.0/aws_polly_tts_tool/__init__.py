"""
AWS Polly TTS Tool - Professional text-to-speech CLI and library.

This package provides both CLI and programmatic access to AWS Polly
text-to-speech capabilities. By exporting core functions and classes, we
enable users to integrate Polly TTS into their own applications while
maintaining the convenience of a command-line interface.

The public API exposes essential functions for client initialization,
synthesis operations, voice management, and cost tracking - all designed
to work independently of the CLI for maximum flexibility.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import warnings

# Suppress pydub's SyntaxWarnings before any imports
# WHY: pydub has invalid escape sequences in regex patterns that trigger warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

__version__ = "0.2.0"

# Core functionality
# Billing/cost utilities
from aws_polly_tts_tool.billing import (  # noqa: E402
    calculate_cost,
    compare_engine_costs,
    estimate_batch_cost,
    format_cost_summary,
)
from aws_polly_tts_tool.core import (  # noqa: E402
    get_polly_client,
    play_speech,
    read_from_stdin,
    save_speech,
    synthesize_audio,
    test_aws_credentials,
)

# Engine metadata
from aws_polly_tts_tool.engines import (  # noqa: E402
    EngineInfo,
    get_engine_info,
    list_all_engines,
    validate_engine,
)

# Voice management
from aws_polly_tts_tool.voices import VoiceManager, VoiceProfile  # noqa: E402

__all__ = [
    "__version__",
    # Core
    "get_polly_client",
    "test_aws_credentials",
    "synthesize_audio",
    "play_speech",
    "save_speech",
    "read_from_stdin",
    # Voices
    "VoiceManager",
    "VoiceProfile",
    # Engines
    "EngineInfo",
    "validate_engine",
    "get_engine_info",
    "list_all_engines",
    # Billing
    "calculate_cost",
    "format_cost_summary",
    "estimate_batch_cost",
    "compare_engine_costs",
]
