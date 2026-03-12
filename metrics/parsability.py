"""Parsability metric: check if resolvable RDF URIs can be parsed and contain definitions."""

import logging
from typing import List, Union

import numpy as np
import pandas as pd
import requests
from rdflib import Graph
from rdflib.term import URIRef

from core.constants import (
    COL_CONTENT_TYPE,
    COL_PARSING,
    COL_STATUS_CODE,
    COL_URIS,
    COL_WHETHER_DEFINED,
    COL_WHETHER_RDF,
    CONTENT_TYPES_RDF,
    CONTENT_TYPE_TO_FORMAT,
    HTTP_ACCEPT_HEADERS,
    STATUS_RESOLVABLE,
)

PARSE_TIMEOUT = 15  # seconds per URI

logger = logging.getLogger("assess_rdf")


def _parse_uri(uri: str, content_type: str) -> tuple:
    """
    Parse a URI and check if it defines the URI itself.

    Returns:
        Tuple of (triple_count_or_error, defined_status).
        defined_status: 'defined' | 'undefined' | 'not applicable' | exception
    """
    if content_type not in CONTENT_TYPES_RDF:
        return "not applicable", "not applicable"

    try:
        parse_format = CONTENT_TYPE_TO_FORMAT.get(
            content_type, CONTENT_TYPE_TO_FORMAT.get("text/plain", "xml")
        )
        # Fetch with timeout to avoid hanging on slow servers
        resp = requests.get(uri, headers=HTTP_ACCEPT_HEADERS, timeout=PARSE_TIMEOUT)
        resp.raise_for_status()
        temp_graph = Graph().parse(data=resp.content, format=parse_format)
        triple_count = len(temp_graph)

        # Check if the URI is defined in the resolved content
        validate_graph = Graph()
        validate_graph += temp_graph.triples((URIRef(uri), None, None))
        defined_status = "undefined" if len(validate_graph) == 0 else "defined"

        return triple_count, defined_status

    except Exception as e:
        logger.warning("Parse failed for %s: %s", uri, e)
        return e, e


def assess_parsable(df_uris: pd.DataFrame) -> pd.DataFrame:
    """
    Assess parsability of resolvable URIs.

    Args:
        df_uris: DataFrame with resolvability results (uris, status_code, content-type).

    Returns:
        DataFrame with columns: uris, status_code, content-type, whether RDF type,
        parsing, whether defined.
    """
    df_uris = df_uris.copy()
    df_uris[COL_STATUS_CODE] = df_uris[COL_STATUS_CODE].astype(str)

    # Only assess URIs with 2xx or 3xx status
    resolvable = df_uris[df_uris[COL_STATUS_CODE].str.startswith(STATUS_RESOLVABLE)]

    resolvable = resolvable.copy()
    resolvable[COL_WHETHER_RDF] = np.where(
        resolvable[COL_CONTENT_TYPE].isin(CONTENT_TYPES_RDF),
        "RDF",
        "not RDF",
    )

    total_rdf = (resolvable[COL_WHETHER_RDF] == "RDF").sum()
    logger.info("Parsability: %d resolvable URIs, %d with RDF content-type to parse", len(resolvable), total_rdf)

    parsed_content: List[Union[int, str, Exception]] = []
    uri_defined: List[Union[str, Exception]] = []
    rdf_count = 0

    for idx, row in resolvable.iterrows():
        uri = row[COL_URIS]
        content_type = row[COL_CONTENT_TYPE]

        if row[COL_WHETHER_RDF] == "RDF":
            rdf_count += 1
            if total_rdf <= 20 or rdf_count <= 1 or rdf_count == total_rdf or rdf_count % 50 == 0:
                logger.info("Parsability: parsing URI %d/%d (RDF)", rdf_count, total_rdf)

        parsed, defined = _parse_uri(uri, content_type)
        parsed_content.append(parsed)
        uri_defined.append(defined)

    resolvable = resolvable.copy()
    resolvable[COL_PARSING] = parsed_content
    resolvable[COL_WHETHER_DEFINED] = uri_defined

    return resolvable
