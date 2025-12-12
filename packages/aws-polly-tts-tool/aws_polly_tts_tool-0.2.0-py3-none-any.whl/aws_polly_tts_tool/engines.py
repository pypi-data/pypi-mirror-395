"""
AWS Polly voice engine metadata and validation.

Centralizes engine-specific information (pricing, features, limits) to
provide consistent validation and helpful error messages across the CLI. By
maintaining engine metadata in one place, we ensure users select appropriate
engines for their use cases and understand the cost implications.

This module serves as the source of truth for engine capabilities, enabling
the tool to guide users toward optimal engine choices based on quality,
cost, and performance requirements.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class EngineInfo:
    """
    Metadata for a Polly voice engine.

    Encapsulates all engine-specific information in a type-safe structure
    that's easy to query and display. Frozen dataclass ensures immutability
    since engine specs are fixed and should not change at runtime.

    Attributes:
        name: Display name of the engine
        engine_id: AWS API identifier
        technology: Underlying synthesis technology
        quality: Voice quality descriptor
        pricing_per_million: Cost per 1 million characters (USD)
        char_limit: Maximum characters per request
        concurrent_requests: Maximum concurrent API requests
        best_for: Recommended use cases
        features: Key capabilities
        free_tier: Free tier allocation (if applicable)
    """

    name: str
    engine_id: str
    technology: str
    quality: str
    pricing_per_million: float
    char_limit: int
    concurrent_requests: int
    best_for: str
    features: list[str]
    free_tier: str


# WHY: Define all Polly engines with current specs (as of 2025)
# This serves as the single source of truth for engine capabilities
AVAILABLE_ENGINES: dict[str, EngineInfo] = {
    "standard": EngineInfo(
        name="Standard",
        engine_id="standard",
        technology="Concatenative synthesis",
        quality="Clear, intelligible speech",
        pricing_per_million=4.00,
        char_limit=3000,
        concurrent_requests=100,
        best_for="Cost-sensitive applications, announcements, notifications",
        features=[
            "Traditional TTS quality",
            "Lowest cost option",
            "High concurrency",
            "All AWS regions",
        ],
        free_tier="5M chars/month for 12 months",
    ),
    "neural": EngineInfo(
        name="Neural",
        engine_id="neural",
        technology="Deep learning-based synthesis",
        quality="Natural, human-like speech with better prosody",
        pricing_per_million=16.00,
        char_limit=3000,
        concurrent_requests=100,
        best_for="Virtual assistants, audiobooks, e-learning, customer service",
        features=[
            "Improved intonation and rhythm",
            "Expressive delivery",
            "Better handling of complex sentences",
            "Emotions and speaking styles",
        ],
        free_tier="1M chars/month for 12 months",
    ),
    "generative": EngineInfo(
        name="Generative",
        engine_id="generative",
        technology="Amazon's latest generative TTS",
        quality="Most human-like, emotionally engaged, adaptive conversational voices",
        pricing_per_million=30.00,  # Approximate, varies by region
        char_limit=3000,
        concurrent_requests=26,
        best_for="High-quality conversational AI, premium content, brand voices",
        features=[
            "Highest naturalness",
            "Emotionally engaged",
            "Adaptive to context",
            "Best-in-class quality",
        ],
        free_tier="N/A",
    ),
    "long-form": EngineInfo(
        name="Long-Form",
        engine_id="long-form",
        technology="Specialized engine for extended narration",
        quality="Highly expressive, emotionally adept for storytelling",
        pricing_per_million=100.00,
        char_limit=100000,
        concurrent_requests=26,
        best_for="Audiobooks, long-form articles, podcast narration",
        features=[
            "Extended content support (100K chars)",
            "Consistent quality across passages",
            "Enhanced emotional range",
            "Optimized for storytelling",
        ],
        free_tier="N/A",
    ),
}

# Default engine for commands
DEFAULT_ENGINE = "neural"


def validate_engine(engine_id: str) -> str:
    """
    Validate and normalize engine ID.

    Ensures users specify valid engines before making API calls, providing
    clear, actionable error messages that list available options. Normalizes
    input to lowercase for case-insensitive matching.

    Args:
        engine_id: Engine identifier to validate (case-insensitive)

    Returns:
        Normalized engine ID (lowercase)

    Raises:
        ValueError: If engine ID is invalid with list of available engines

    Example:
        >>> validate_engine("Neural")
        'neural'
        >>> validate_engine("invalid")
        ValueError: Invalid engine ID...
    """
    normalized_id = engine_id.lower().strip()

    if normalized_id not in AVAILABLE_ENGINES:
        available = ", ".join(sorted(AVAILABLE_ENGINES.keys()))
        raise ValueError(
            f"Invalid engine ID: '{engine_id}'\n\n"
            f"Available engines:\n{available}\n\n"
            "Run 'aws-polly-tts-tool list-engines' to see all engines with details."
        )

    return normalized_id


def get_engine_info(engine_id: str) -> EngineInfo:
    """
    Get metadata for a specific engine.

    Provides type-safe access to engine information for cost calculations,
    validation, and user guidance. Validates engine ID before returning info.

    Args:
        engine_id: Engine identifier (case-insensitive)

    Returns:
        EngineInfo instance with engine metadata

    Raises:
        ValueError: If engine ID is invalid

    Example:
        >>> info = get_engine_info("neural")
        >>> print(f"Cost: ${info.pricing_per_million}/1M chars")
    """
    validated_id = validate_engine(engine_id)
    return AVAILABLE_ENGINES[validated_id]


def list_all_engines() -> list[tuple[str, EngineInfo]]:
    """
    Get all available engines sorted by quality/cost.

    Provides ordered list of engines for CLI display, sorted to present
    options from basic (standard) to premium (long-form), helping users
    understand the progression of quality and cost.

    Returns:
        List of (engine_id, EngineInfo) tuples sorted by recommendation order

    Example:
        >>> engines = list_all_engines()
        >>> for engine_id, info in engines:
        ...     print(f"{info.name}: ${info.pricing_per_million}/1M")
    """
    # WHY: Sort by pricing to show progression from basic to premium
    return sorted(AVAILABLE_ENGINES.items(), key=lambda x: x[1].pricing_per_million)
