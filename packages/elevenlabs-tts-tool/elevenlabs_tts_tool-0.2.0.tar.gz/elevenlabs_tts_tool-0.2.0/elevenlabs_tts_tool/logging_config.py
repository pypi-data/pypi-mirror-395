"""Centralized logging configuration with multi-level verbosity support.

This module provides setup_logging() for configuring logging based on
verbosity count from CLI arguments (-v, -vv, -vvv).

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import logging
import sys


def setup_logging(verbose_count: int = 0) -> None:
    """Configure logging based on verbosity level.

    Maps CLI verbosity count to Python logging levels and configures
    both application and dependent library loggers.

    Args:
        verbose_count: Number of -v flags (0-3+)
            0: WARNING level (quiet mode - only critical issues)
            1: INFO level (normal verbose - operations and events)
            2: DEBUG level (detailed debugging - API calls, validation)
            3+: DEBUG + enable dependent library logging (trace mode)

    Example:
        >>> setup_logging(0)  # No -v flag: WARNING only
        >>> setup_logging(1)  # -v: INFO level
        >>> setup_logging(2)  # -vv: DEBUG level
        >>> setup_logging(3)  # -vvv: DEBUG + library internals
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

    # Configure dependent library loggers at TRACE level (-vvv)
    if verbose_count >= 3:
        # ElevenLabs SDK internals
        logging.getLogger("elevenlabs").setLevel(logging.DEBUG)

        # HTTP client libraries (used by ElevenLabs SDK)
        logging.getLogger("httpx").setLevel(logging.DEBUG)
        logging.getLogger("httpcore").setLevel(logging.DEBUG)
        logging.getLogger("urllib3").setLevel(logging.DEBUG)
    else:
        # Suppress noisy libraries at lower verbosity levels
        logging.getLogger("elevenlabs").setLevel(logging.WARNING)
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("httpcore").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module.

    This is a convenience wrapper around logging.getLogger() that
    ensures consistent logger naming across the application.

    Args:
        name: Module name (typically __name__)

    Returns:
        Logger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Operation started")
        >>> logger.debug("Detailed operation info")
    """
    return logging.getLogger(name)
