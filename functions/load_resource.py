"""Load RDF resources from local paths or remote URIs."""

import logging
from pathlib import Path
from typing import Union

import requests
from rdflib import Graph

from core.constants import CONTENT_TYPE_TO_FORMAT, HTTP_ACCEPT_HEADERS

logger = logging.getLogger("assess_rdf")


def _is_remote_path(path: Union[str, Path]) -> bool:
    """Check if path appears to be a remote URI."""
    return "http" in str(path)


def parse_data_local_or_remote(data_path: Union[str, Path]) -> Graph:
    """
    Parse RDF from a local file or remote URI.

    Args:
        data_path: Local file path or HTTP(S) URI.

    Returns:
        RDFlib Graph containing the parsed triples.

    Raises:
        OSError: If local file does not exist.
        Exception: If parsing fails.
    """
    graph = Graph()
    path_str = str(data_path)

    if _is_remote_path(data_path):
        logger.info("Loading resource from %s", path_str)
        response = requests.get(path_str, headers=HTTP_ACCEPT_HEADERS, timeout=60)
        response.raise_for_status()

        content_type = response.headers.get("content-type", "").split(";", 1)[0]
        logger.info("Content-Type: %s", content_type)

        parse_format = CONTENT_TYPE_TO_FORMAT.get(
            content_type,
            CONTENT_TYPE_TO_FORMAT.get("text/plain", "xml"),
        )
        try:
            graph.parse(data=response.content, format=parse_format)
        except Exception as e:
            raise ValueError(
                f"Cannot parse resource from {path_str}: {e}"
            ) from e
    else:
        path = Path(data_path)
        if not path.exists():
            raise OSError(f"Resource not found: {path}")

        logger.info("Parsing local resource: %s", path_str)
        try:
            graph.parse(path)
        except Exception as e:
            raise ValueError(
                f"Cannot parse local resource from {path_str}: {e}"
            ) from e

    if len(graph) == 0:
        logger.warning("Resource has no triples loaded")
    else:
        logger.info("Successfully loaded %d triples", len(graph))

    return graph
