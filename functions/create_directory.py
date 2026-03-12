"""Directory creation utilities."""

import logging
from pathlib import Path
from typing import Union

logger = logging.getLogger("assess_rdf")


def create_directory(path: Union[str, Path]) -> Path:
    """
    Create a directory and any necessary parent directories.

    Args:
        path: Directory path to create.

    Returns:
        The created Path object.
    """
    path = Path(path)
    try:
        path.mkdir(parents=True, exist_ok=True)
        logger.debug("Created directory: %s", path)
        return path
    except OSError as e:
        logger.error("Failed to create directory %s: %s", path, e)
        raise
