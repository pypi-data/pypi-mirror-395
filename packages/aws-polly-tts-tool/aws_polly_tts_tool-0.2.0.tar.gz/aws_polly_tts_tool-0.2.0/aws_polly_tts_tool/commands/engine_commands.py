"""
Engine listing CLI commands.

Provides CLI interface for discovering AWS Polly voice engines and their
characteristics. This module displays engine metadata including pricing,
technology type, character limits, and recommended use cases to help users
select the appropriate engine for their TTS needs.

The tabular output format enables both human readability and programmatic
parsing, supporting informed decision-making about cost-quality tradeoffs.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from aws_polly_tts_tool.engines import list_all_engines
from aws_polly_tts_tool.utils import format_table_row


@click.command(name="list-engines")
def list_engines() -> None:
    """
    List all available Polly voice engines.

    \b
    Examples:

    \b
        # Show all engines with pricing and features
        aws-polly-tts-tool list-engines
    """
    engines = list_all_engines()

    # Print header
    widths = [12, 15, 12, 15, 50]
    click.echo(
        format_table_row(["Engine", "Technology", "Price/1M", "Char Limit", "Best For"], widths)
    )
    click.echo("=" * sum(widths))

    # Print engines
    for engine_id, info in engines:
        click.echo(
            format_table_row(
                [
                    info.name,
                    info.technology[:13],
                    f"${info.pricing_per_million:.2f}",
                    f"{info.char_limit:,}",
                    info.best_for[:48],
                ],
                widths,
            )
        )

    click.echo("\n" + "=" * sum(widths))
    click.echo(f"\nTotal: {len(engines)} engines available")
    click.echo("\nUse 'aws-polly-tts-tool pricing' for detailed pricing information.")
