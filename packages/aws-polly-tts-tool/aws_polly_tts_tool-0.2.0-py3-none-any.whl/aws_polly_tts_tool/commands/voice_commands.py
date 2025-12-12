"""
Voice listing CLI commands.

Provides CLI interface for discovering and filtering AWS Polly voices.
This module wraps the VoiceManager class to enable command-line voice discovery
with filtering by engine, language, and gender. The output is formatted as a
table for human readability while remaining grep-friendly for automation.

By exposing voice discovery as a CLI command, users can explore available
voices without writing code, and AI agents can query voice capabilities
programmatically.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys

import click

from aws_polly_tts_tool.core import get_polly_client
from aws_polly_tts_tool.logging_config import get_logger, setup_logging
from aws_polly_tts_tool.utils import format_table_row
from aws_polly_tts_tool.voices import VoiceManager

logger = get_logger(__name__)


@click.command(name="list-voices")
@click.option("--engine", "-e", help="Filter by engine (standard, neural, generative, long-form)")
@click.option("--language", "-l", help="Filter by language code (e.g., en-US, es-ES)")
@click.option("--gender", "-g", help="Filter by gender (Female, Male)")
@click.option("--region", "-r", help="AWS region (default: from AWS config)")
@click.option(
    "-V",
    "--verbose",
    count=True,
    help="Enable verbose output (-V INFO, -VV DEBUG, -VVV TRACE with AWS SDK details)",
)
def list_voices(
    engine: str | None,
    language: str | None,
    gender: str | None,
    region: str | None,
    verbose: int,
) -> None:
    """
    List all available Polly voices.

    \b
    Examples:

    \b
        # List all voices
        aws-polly-tts-tool list-voices

    \b
        # Filter by engine
        aws-polly-tts-tool list-voices --engine neural

    \b
        # Filter by language
        aws-polly-tts-tool list-voices --language en-US

    \b
        # Combine filters
        aws-polly-tts-tool list-voices --engine neural --language en --gender Female

    \b
        # Use with grep for searching
        aws-polly-tts-tool list-voices | grep British
    """
    # Setup logging at the start
    setup_logging(verbose)

    try:
        logger.debug("Initializing AWS Polly client")
        client = get_polly_client(region)
        voice_manager = VoiceManager(client)

        # Log applied filters
        filters_applied = []
        if engine:
            filters_applied.append(f"engine={engine}")
        if language:
            filters_applied.append(f"language={language}")
        if gender:
            filters_applied.append(f"gender={gender}")

        if filters_applied:
            logger.info(f"Fetching voices with filters: {', '.join(filters_applied)}")
        else:
            logger.info("Fetching all available voices")

        voices = voice_manager.list_voices(engine=engine, language=language, gender=gender)

        if not voices:
            logger.warning("No voices found matching filters")
            click.echo("No voices found matching filters.", err=True)
            sys.exit(1)

        logger.debug(f"Retrieved {len(voices)} voices from Polly API")

        # Print header
        widths = [15, 10, 12, 20, 40]
        click.echo(
            format_table_row(["Voice", "Gender", "Language", "Engines", "Description"], widths)
        )
        click.echo("=" * sum(widths))

        # Print voices
        for name, profile in voices:
            engines_str = ", ".join(profile.supported_engines)
            desc = (
                profile.description[:37] + "..."
                if len(profile.description) > 40
                else profile.description
            )
            click.echo(
                format_table_row(
                    [profile.name, profile.gender, profile.language_code, engines_str, desc], widths
                )
            )

        click.echo(f"\nTotal: {len(voices)} voices")
        logger.info(f"Listed {len(voices)} voices successfully")

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        logger.debug("Full traceback:", exc_info=True)
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.debug("Full traceback:", exc_info=True)
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
