"""Logging configuration for the assessment tool."""

import logging
import sys


def setup_logging(
    level: int = logging.INFO,
    format_string: str = "%(asctime)s - %(levelname)s - %(message)s",
) -> logging.Logger:
    """Configure and return the application logger."""
    logger = logging.getLogger("assess_rdf")
    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(format_string))
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


def get_logger() -> logging.Logger:
    """Get the application logger."""
    return logging.getLogger("assess_rdf")
