"""
Text-to-speech synthesis CLI commands.

Implements the primary TTS functionality as a CLI command, handling
user input (text or stdin), voice/engine selection, and output routing
(speakers or file). This command provides the main interface for converting
text to speech while maintaining separation from core synthesis logic.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys
from pathlib import Path

import click

from aws_polly_tts_tool.billing import format_cost_summary
from aws_polly_tts_tool.core import get_polly_client, play_speech, read_from_stdin, save_speech
from aws_polly_tts_tool.engines import DEFAULT_ENGINE, validate_engine
from aws_polly_tts_tool.logging_config import get_logger, setup_logging
from aws_polly_tts_tool.utils import truncate_text, validate_output_format
from aws_polly_tts_tool.voices import VoiceManager

logger = get_logger(__name__)


@click.command()
@click.argument("text", required=False)
@click.option("--stdin", "-s", is_flag=True, help="Read text from stdin")
@click.option("--voice", default="Joanna", help="Voice ID (default: Joanna)")
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    help="Save audio to file instead of playing",
)
@click.option(
    "--format",
    "-f",
    default="mp3",
    help="Output format: mp3, ogg_vorbis, pcm (default: mp3)",
)
@click.option(
    "--engine",
    "-e",
    default=DEFAULT_ENGINE,
    help=f"Voice engine: standard, neural, generative, long-form (default: {DEFAULT_ENGINE})",
)
@click.option("--ssml", is_flag=True, help="Treat input as SSML markup")
@click.option("--show-cost", is_flag=True, help="Display character count and cost estimate")
@click.option("--region", "-r", help="AWS region (default: from AWS config)")
@click.option(
    "-V",
    "--verbose",
    count=True,
    help="Enable verbose output (-V INFO, -VV DEBUG, -VVV TRACE with AWS SDK details)",
)
def synthesize(
    text: str | None,
    stdin: bool,
    voice: str,
    output: Path | None,
    format: str,
    engine: str,
    ssml: bool,
    show_cost: bool,
    region: str | None,
    verbose: int,
) -> None:
    """
    Convert text to speech using AWS Polly.

    Synthesizes text using Amazon Polly TTS service with support for all
    voice engines, output formats, and SSML markup. Audio can be played
    through speakers or saved to a file.

    \b
    Examples:

    \b
        # Play text with default voice (Joanna, neural)
        aws-polly-tts-tool synthesize "Hello world"

    \b
        # Use different voice and engine
        aws-polly-tts-tool synthesize "Hello" --voice Matthew --engine generative

    \b
        # Save to file with specific format
        aws-polly-tts-tool synthesize "Hello" --output speech.mp3 --format mp3

    \b
        # Read from stdin
        echo "Hello world" | aws-polly-tts-tool synthesize --stdin

    \b
        # Use SSML for advanced control
        aws-polly-tts-tool synthesize '<speak>Hello <break time="500ms"/> world</speak>' --ssml

    \b
        # Show cost estimate after synthesis
        aws-polly-tts-tool synthesize "Hello" --show-cost

    \b
        # Multiple options combined
        cat article.txt | aws-polly-tts-tool synthesize --stdin \\
            --voice Joanna \\
            --engine neural \\
            --output article.mp3 \\
            --show-cost

    \b
    Cost Tracking:
        Use --show-cost to display character count and estimated cost.
        For actual AWS billing data, use: aws-polly-tts-tool billing
    """
    # Setup logging at the start
    setup_logging(verbose)

    try:
        # Validate input
        if stdin:
            logger.debug("Reading text from stdin")
            input_text = read_from_stdin()
        elif text:
            input_text = text
        else:
            logger.error("No text provided")
            click.echo(
                "Error: No text provided.\n\n"
                "Provide text as argument or use --stdin:\n"
                "  aws-polly-tts-tool synthesize 'your text'\n"
                "  echo 'text' | aws-polly-tts-tool synthesize --stdin\n\n"
                "Use --help for more examples.",
                err=True,
            )
            sys.exit(1)

        # Validate engine
        logger.debug(f"Validating engine: {engine}")
        engine_id = validate_engine(engine)

        # Validate output format
        logger.debug(f"Validating output format: {format}")
        output_format = validate_output_format(format)

        # Initialize client and voice manager
        logger.debug("Initializing AWS Polly client")
        client = get_polly_client(region)
        voice_manager = VoiceManager(client)

        # Resolve voice ID (handles case-insensitive names)
        logger.debug(f"Resolving voice ID for: {voice}")
        voice_id = voice_manager.get_voice_id(voice)
        logger.info(f"Using voice: {voice_id} ({engine_id} engine)")

        # Determine text type
        text_type = "ssml" if ssml else "text"
        if ssml:
            logger.debug("Input text will be treated as SSML")

        # Show what we're doing
        truncated = truncate_text(input_text, 50)
        click.echo(f"Synthesizing: {truncated}", err=True)
        click.echo(f"Voice: {voice_id}, Engine: {engine_id}, Format: {output_format}", err=True)

        # Execute synthesis
        if output:
            logger.info(f"Synthesizing audio to file: {output}")
            char_count = save_speech(
                client, input_text, voice_id, output, output_format, engine_id, text_type
            )
            logger.debug(f"Synthesized {char_count} characters")
            click.echo(f"\nAudio saved to: {output}")
        else:
            logger.info("Synthesizing audio for playback")
            char_count = play_speech(
                client, input_text, voice_id, output_format, engine_id, text_type
            )
            logger.debug(f"Synthesized {char_count} characters")
            click.echo("\nPlayback complete!", err=True)

        # Show cost if requested
        if show_cost:
            logger.debug("Calculating cost estimate")
            click.echo(f"\n{format_cost_summary(char_count, engine_id)}")

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
