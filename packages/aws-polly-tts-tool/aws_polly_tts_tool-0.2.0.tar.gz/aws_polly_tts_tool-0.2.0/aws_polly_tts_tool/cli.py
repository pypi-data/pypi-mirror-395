"""
CLI entry point for AWS Polly TTS tool.

Serves as the main command group that registers all CLI commands
and provides the entry point for the tool. Uses Click's group pattern
to organize commands in a flat structure for simplicity and discoverability.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import warnings

# Suppress pydub's SyntaxWarnings (invalid escape sequences in pydub's code)
warnings.filterwarnings("ignore", category=SyntaxWarning)

import click  # noqa: E402

from aws_polly_tts_tool.commands import (  # noqa: E402
    billing,
    completion,
    info,
    list_engines,
    list_voices,
    pricing,
    synthesize,
)


@click.group()
@click.version_option(version="0.2.0")
def main() -> None:
    """AWS Polly TTS CLI - Professional text-to-speech synthesis.

    Convert text to lifelike speech using Amazon Polly with support for
    multiple engines, voices, and output formats.

    \b
    Quick Start:
        aws-polly-tts-tool synthesize "Hello world"
        aws-polly-tts-tool list-voices
        aws-polly-tts-tool pricing

    \b
    Documentation:
        https://github.com/yourusername/aws-polly-tts-tool
    """
    pass


# Register commands
main.add_command(synthesize)
main.add_command(list_voices)
main.add_command(list_engines)
main.add_command(billing)
main.add_command(pricing)
main.add_command(info)
main.add_command(completion)


if __name__ == "__main__":
    main()
