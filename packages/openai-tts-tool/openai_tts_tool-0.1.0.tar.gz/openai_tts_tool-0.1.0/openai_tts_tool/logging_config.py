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

    Args:
        verbose_count: Number of -v flags (0-3+)
            0: WARNING level (quiet mode)
            1: INFO level (normal verbose)
            2: DEBUG level (detailed debugging)
            3+: DEBUG + enable dependent library logging (trace mode)
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

    # Configure format - all levels include module name for traceability
    if verbose_count >= 2:
        # Detailed format for DEBUG (includes line number)
        fmt = "[%(levelname)s] %(name)s:%(lineno)d - %(message)s"
    else:
        # Standard format for INFO/WARNING (module name, no line number)
        fmt = "[%(levelname)s] %(name)s - %(message)s"

    # Configure root logger
    logging.basicConfig(
        level=level,
        format=fmt,
        stream=sys.stderr,
        force=True,
    )

    # Configure dependent library loggers at TRACE level (-vvv)
    if verbose_count >= 3:
        # Add project-specific libraries here
        logging.getLogger("openai").setLevel(logging.DEBUG)
        logging.getLogger("urllib3").setLevel(logging.DEBUG)
        logging.getLogger("httpx").setLevel(logging.DEBUG)
    else:
        # Suppress noisy libraries at lower verbosity levels
        logging.getLogger("openai").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("httpx").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module.

    This is a convenience wrapper around logging.getLogger() that
    ensures consistent logger naming across your application.

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
