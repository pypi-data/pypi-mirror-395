"""
CLI command implementations for AWS Polly TTS tool.

This package contains all Click command definitions that wrap the core
library functions with CLI-specific concerns like argument parsing, error
formatting, and user output. By separating command implementations from core
logic, we maintain a clean architecture where business logic remains testable
and reusable outside the CLI context.

Commands handle user interaction, format output for terminal display, and
translate exceptions into helpful error messages with exit codes.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from aws_polly_tts_tool.commands.billing_commands import billing, pricing
from aws_polly_tts_tool.commands.completion_commands import completion
from aws_polly_tts_tool.commands.engine_commands import list_engines
from aws_polly_tts_tool.commands.info_commands import info
from aws_polly_tts_tool.commands.synthesize_commands import synthesize
from aws_polly_tts_tool.commands.voice_commands import list_voices

__all__ = [
    "synthesize",
    "list_voices",
    "list_engines",
    "billing",
    "pricing",
    "info",
    "completion",
]
