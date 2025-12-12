"""
Centralized logging configuration with multi-level verbosity support.

Provides progressive logging detail levels (-v, -vv, -vvv) to give users
control over output verbosity without code changes. Enables debugging of both
application logic and dependent AWS libraries (boto3/botocore) at different
detail levels.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import logging
import sys


def setup_logging(verbose_count: int = 0) -> None:
    """Configure logging based on verbosity level.

    Maps CLI verbosity flags to logging levels and configures both
    application and dependent library loggers. Outputs to stderr to keep
    stdout clean for data/audio output.

    Args:
        verbose_count: Number of -v flags (0-3+)
            0: WARNING level (quiet mode - errors/warnings only)
            1: INFO level (normal verbose - high-level operations)
            2: DEBUG level (detailed debugging - all operations)
            3+: DEBUG + enable boto3/botocore logging (trace mode - AWS API details)
    """
    # Map verbosity count to logging levels
    if verbose_count == 0:
        level = logging.WARNING
    elif verbose_count == 1:
        level = logging.INFO
    elif verbose_count >= 2:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    # Configure root logger
    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(message)s",
        stream=sys.stderr,
        force=True,  # Override any existing configuration
    )

    # Configure AWS SDK loggers
    if verbose_count >= 3:
        # Enable full AWS SDK logging at trace level (-vvv)
        logging.getLogger("boto3").setLevel(logging.DEBUG)
        logging.getLogger("botocore").setLevel(logging.DEBUG)
        logging.getLogger("botocore.credentials").setLevel(logging.DEBUG)
        logging.getLogger("botocore.auth").setLevel(logging.DEBUG)
    else:
        # Suppress noisy AWS libraries at lower verbosity levels
        logging.getLogger("boto3").setLevel(logging.WARNING)
        logging.getLogger("botocore").setLevel(logging.WARNING)
        logging.getLogger("botocore.credentials").setLevel(logging.WARNING)
        logging.getLogger("botocore.auth").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module.

    Provides consistent logger creation pattern across all modules.
    Using __name__ ensures logger hierarchy matches module structure.

    Args:
        name: Module name (typically __name__)

    Returns:
        Logger instance for the specified module
    """
    return logging.getLogger(name)
