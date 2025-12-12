"""
Core library for AWS Polly TTS operations.

This package contains the core TTS functionality independent of CLI
concerns. By separating business logic from command-line interface code,
we enable programmatic usage of the library while maintaining a clean
architecture that's easy to test and extend.

The core modules handle AWS client initialization, speech synthesis,
and cost tracking - all designed to raise exceptions rather than exit,
allowing CLI commands to control error formatting and exit codes.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from aws_polly_tts_tool.core.client import get_polly_client, test_aws_credentials
from aws_polly_tts_tool.core.synthesize import (
    play_speech,
    read_from_stdin,
    save_speech,
    synthesize_audio,
)

__all__ = [
    "get_polly_client",
    "test_aws_credentials",
    "synthesize_audio",
    "play_speech",
    "save_speech",
    "read_from_stdin",
]
