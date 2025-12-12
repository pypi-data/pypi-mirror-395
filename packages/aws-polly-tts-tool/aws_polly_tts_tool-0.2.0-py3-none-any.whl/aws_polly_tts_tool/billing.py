"""
Cost calculation utilities for AWS Polly TTS.

Provides immediate cost estimates based on character counts to give
users transparency into Polly pricing before and after synthesis operations.
This complements the Cost Explorer integration by offering instant feedback
without requiring API calls or billing data delays.

The module uses current Polly pricing (as of 2025) and calculates costs
based on the pay-per-character model, helping users make informed decisions
about engine selection and batch processing.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from aws_polly_tts_tool.engines import get_engine_info


def calculate_cost(character_count: int, engine: str) -> float:
    """
    Calculate estimated cost for synthesizing text.

    Provides instant cost feedback based on character count and engine
    selection. This helps users understand the financial impact of their TTS
    operations and make informed choices about engine selection.

    Uses current Polly pricing per 1 million characters, prorated for the
    actual character count.

    Args:
        character_count: Number of characters to synthesize
        engine: Engine ID ('standard', 'neural', 'generative', 'long-form')

    Returns:
        Estimated cost in USD

    Raises:
        ValueError: If engine is invalid

    Example:
        >>> cost = calculate_cost(5000, 'neural')
        >>> print(f"Estimated cost: ${cost:.4f}")
        Estimated cost: $0.0800
    """
    engine_info = get_engine_info(engine)

    # Calculate cost: (characters / 1,000,000) * price_per_million
    # WHY: Polly charges per million characters, prorate for actual usage
    cost = (character_count / 1_000_000) * engine_info.pricing_per_million

    return cost


def format_cost_summary(character_count: int, engine: str) -> str:
    """
    Format a human-readable cost summary.

    Provides consistent cost display format across CLI commands,
    showing both character count and calculated cost with engine context.
    This gives users complete transparency into what they're being charged for.

    Args:
        character_count: Number of characters processed
        engine: Engine ID used for synthesis

    Returns:
        Formatted cost summary string

    Example:
        >>> summary = format_cost_summary(5000, 'neural')
        >>> print(summary)
        Characters processed: 5,000
        Engine: neural ($16.00/1M chars)
        Estimated cost: $0.0800
    """
    engine_info = get_engine_info(engine)
    cost = calculate_cost(character_count, engine)

    return (
        f"Characters processed: {character_count:,}\n"
        f"Engine: {engine} (${engine_info.pricing_per_million:.2f}/1M chars)\n"
        f"Estimated cost: ${cost:.4f}"
    )


def estimate_batch_cost(texts: list[str], engine: str) -> dict[str, float | int]:
    """
    Estimate cost for batch processing multiple texts.

    Enables cost forecasting for batch TTS operations, helping users
    plan budgets and choose optimal engines before committing to large-scale
    synthesis jobs.

    Args:
        texts: List of text strings to synthesize
        engine: Engine ID to use

    Returns:
        Dictionary with keys:
            - total_characters: Total character count
            - total_cost: Estimated total cost (USD)
            - per_text_avg: Average cost per text
            - count: Number of texts

    Example:
        >>> texts = ["Hello world", "How are you?"]
        >>> est = estimate_batch_cost(texts, 'standard')
        >>> print(f"Total: ${est['total_cost']:.4f} for {est['count']} texts")
    """
    total_chars = sum(len(text) for text in texts)
    total_cost = calculate_cost(total_chars, engine)

    return {
        "total_characters": total_chars,
        "total_cost": total_cost,
        "per_text_avg": total_cost / len(texts) if texts else 0.0,
        "count": len(texts),
    }


def compare_engine_costs(character_count: int) -> dict[str, float]:
    """
    Compare costs across all engines for a given character count.

    Helps users make informed engine selection by showing cost
    differences side-by-side. This is especially useful for large batches
    where engine choice significantly impacts total cost.

    Args:
        character_count: Number of characters to compare

    Returns:
        Dictionary mapping engine IDs to costs (USD)

    Example:
        >>> costs = compare_engine_costs(100000)
        >>> for engine, cost in sorted(costs.items(), key=lambda x: x[1]):
        ...     print(f"{engine}: ${cost:.2f}")
        standard: $0.40
        neural: $1.60
        generative: $3.00
        long-form: $10.00
    """
    from aws_polly_tts_tool.engines import AVAILABLE_ENGINES

    return {
        engine_id: calculate_cost(character_count, engine_id) for engine_id in AVAILABLE_ENGINES
    }
