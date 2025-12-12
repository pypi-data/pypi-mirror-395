"""
Billing and pricing CLI commands.

Provides dual cost tracking through immediate estimates and actual AWS
billing queries. This module enables users to understand TTS costs before
synthesis (via pricing command) and track actual spending afterward (via
billing command with Cost Explorer integration).

The immediate cost estimation helps users make engine selection decisions,
while the billing history tracking enables budget monitoring and cost attribution
across different TTS use cases.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys

import click

from aws_polly_tts_tool.core.cost_explorer import get_polly_costs
from aws_polly_tts_tool.engines import list_all_engines
from aws_polly_tts_tool.logging_config import get_logger, setup_logging

logger = get_logger(__name__)


@click.command()
@click.option("--days", "-d", default=30, help="Number of days to query (default: 30)")
@click.option("--start-date", help="Custom start date (YYYY-MM-DD)")
@click.option("--end-date", help="Custom end date (YYYY-MM-DD)")
@click.option("--region", "-r", help="AWS region for Cost Explorer")
@click.option(
    "-V",
    "--verbose",
    count=True,
    help="Enable verbose output (-V INFO, -VV DEBUG, -VVV TRACE with AWS SDK details)",
)
def billing(
    days: int,
    start_date: str | None,
    end_date: str | None,
    region: str | None,
    verbose: int,
) -> None:
    """
    Query AWS billing data for Polly usage.

    \b
    Examples:

    \b
        # Last 30 days of Polly costs
        aws-polly-tts-tool billing

    \b
        # Last 7 days
        aws-polly-tts-tool billing --days 7

    \b
        # Custom date range
        aws-polly-tts-tool billing --start-date 2025-01-01 --end-date 2025-01-31
    """
    # Setup logging at the start
    setup_logging(verbose)

    try:
        logger.info("Querying AWS Cost Explorer for Polly costs")
        if start_date and end_date:
            logger.debug(f"Date range: {start_date} to {end_date}")
        else:
            logger.debug(f"Last {days} days")

        click.echo("Querying AWS Cost Explorer...", err=True)
        costs = get_polly_costs(days=days, start_date=start_date, end_date=end_date, region=region)

        logger.debug(f"Retrieved cost data: total=${costs['total_cost']:.2f}")

        click.echo(f"\nPolly Costs ({costs['start_date']} to {costs['end_date']})")
        click.echo("=" * 60)
        click.echo(f"Total Cost: ${costs['total_cost']:.2f} {costs['currency']}")
        click.echo("\nBy Engine:")
        for engine, cost in costs["by_engine"].items():
            if cost > 0:
                click.echo(f"  {engine:12} ${cost:.2f}")
                logger.debug(f"Engine {engine}: ${cost:.2f}")

        logger.info("Successfully retrieved billing data")

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        logger.debug("Full traceback:", exc_info=True)
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error querying Cost Explorer: {e}")
        logger.debug("Full traceback:", exc_info=True)
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@click.command()
def pricing() -> None:
    """
    Show Polly pricing information.

    \b
    Examples:

    \b
        # Display pricing table
        aws-polly-tts-tool pricing
    """
    engines = list_all_engines()

    click.echo("AWS Polly Pricing (Per 1 Million Characters)")
    click.echo("=" * 80)

    for engine_id, info in engines:
        click.echo(f"\n{info.name} Engine (${info.pricing_per_million:.2f}/1M characters)")
        click.echo(f"  Technology: {info.technology}")
        click.echo(f"  Quality: {info.quality}")
        click.echo(f"  Character Limit: {info.char_limit:,} chars per request")
        click.echo(f"  Concurrent Requests: {info.concurrent_requests}")
        if info.free_tier != "N/A":
            click.echo(f"  Free Tier: {info.free_tier}")
        click.echo(f"  Best For: {info.best_for}")

    click.echo("\n" + "=" * 80)
    click.echo("\nCost Examples:")
    click.echo("  1,000 words (~5,000 chars) with Standard:  $0.02")
    click.echo("  1,000 words (~5,000 chars) with Neural:    $0.08")
    click.echo("  50,000 word audiobook with Neural:         $4.00")
    click.echo("  50,000 word audiobook with Long-form:     $25.00")
