"""
System information CLI commands.

Provides CLI interface for displaying AWS Polly tool configuration and
credential status. This module offers a diagnostic command to verify AWS
authentication, display available engines and formats, and show helpful
command examples.

The info command serves as a health check and quick reference, particularly
useful for troubleshooting authentication issues and discovering tool
capabilities without consulting external documentation.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys

import click

from aws_polly_tts_tool.core import test_aws_credentials


@click.command()
def info() -> None:
    """
    Show AWS Polly tool configuration.

    \b
    Examples:

    \b
        # Display AWS credentials and configuration
        aws-polly-tts-tool info
    """
    try:
        click.echo("AWS Polly TTS Tool - Configuration")
        click.echo("=" * 60)

        # Test AWS credentials
        identity = test_aws_credentials()
        click.echo("\nAWS Credentials: ✓ Valid")
        click.echo(f"  Account: {identity['Account']}")
        click.echo(f"  User ID: {identity['UserId']}")
        click.echo(f"  ARN: {identity['Arn']}")

        click.echo("\nAvailable Engines:")
        click.echo("  - standard (lowest cost)")
        click.echo("  - neural (recommended)")
        click.echo("  - generative (highest quality)")
        click.echo("  - long-form (audiobooks)")

        click.echo("\nOutput Formats:")
        click.echo("  - mp3 (default)")
        click.echo("  - ogg_vorbis")
        click.echo("  - pcm")

        click.echo("\nUseful Commands:")
        click.echo("  aws-polly-tts-tool list-voices       # Show all voices")
        click.echo("  aws-polly-tts-tool list-engines      # Show all engines")
        click.echo("  aws-polly-tts-tool pricing           # Show pricing")
        click.echo("  aws-polly-tts-tool billing           # Query AWS costs")

    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
