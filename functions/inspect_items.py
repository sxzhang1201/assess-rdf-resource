"""Inspection utilities for RDF graphs and assessment results."""

import logging
from typing import Iterator

from rdflib import Graph

logger = logging.getLogger("assess_rdf")


def view_graph(graph: Graph, limit: int = 10) -> None:
    """
    Log a preview of triples from the graph.

    Args:
        graph: RDF graph to preview.
        limit: Maximum number of triples to show.
    """
    count = 0
    for s, p, o in graph:
        logger.info("  %s %s %s", s, p, o)
        count += 1
        if count >= limit:
            break
    if limit > 0:
        logger.info("  ... (showing first %d of %d triples)", limit, len(graph))


def inspect_item_in_list(items: list, file_handle) -> None:
    """Write each item to a file."""
    for item in items:
        print(item, file=file_handle)


def inspect_item_in_dict(mapping: dict, file_handle) -> None:
    """Write each key to a file."""
    for key in mapping:
        print(key, file=file_handle)
