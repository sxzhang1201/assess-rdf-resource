"""Resolvability metric: check if URIs return valid HTTP responses."""

import logging
from typing import List

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from core.constants import (
    COL_CONTENT_TYPE,
    COL_STATUS_CODE,
    COL_URIS,
    HTTP_ACCEPT_HEADERS,
    REQUEST_ERROR_STATUS,
    STATUS_NON_RESOLVABLE,
)

logger = logging.getLogger("assess_rdf")


def _create_session() -> requests.Session:
    """Create a requests session with retry logic."""
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def _check_uri(uri: str, session: requests.Session, index: int, total: int) -> tuple:
    """
    Check a single URI for resolvability.

    Returns:
        Tuple of (status_code, content_type).
    """
    # Log progress: every 50 for large runs, or every 5 for small runs, plus first/last
    if index <= 1 or index == total:
        logger.info("Resolvability: checking URI %d/%d", index, total)
    elif total > 20 and index % 50 == 0:
        logger.info("Resolvability: checking URI %d/%d", index, total)
    elif total <= 20 and index % 5 == 0:
        logger.info("Resolvability: checking URI %d/%d", index, total)

    try:
        response = session.get(uri, headers=HTTP_ACCEPT_HEADERS, timeout=15)
        status_code = str(response.status_code)

        if (
            status_code.startswith(STATUS_NON_RESOLVABLE)
            or status_code == REQUEST_ERROR_STATUS
        ):
            content_type = "Not applicable because non-resolvable."
        else:
            try:
                content_type = response.headers["content-type"].split(";", 1)[0]
            except (KeyError, AttributeError) as e:
                logger.warning("Could not get content-type for %s: %s", uri, e)
                content_type = str(e)

        return status_code, content_type

    except Exception as e:
        logger.warning("Request failed for %s: %s", uri, e)
        return REQUEST_ERROR_STATUS, "Not applicable because non-resolvable."


def get_http_status_code_and_content_type(uris: List[str]) -> pd.DataFrame:
    """
    Check resolvability of URIs via HTTP GET.

    Args:
        uris: List of URI strings to check.

    Returns:
        DataFrame with columns: uris, status_code, content-type.
    """
    session = _create_session()
    code_list = []
    type_list = []

    for i, uri in enumerate(uris, 1):
        status_code, content_type = _check_uri(uri, session, i, len(uris))
        code_list.append(status_code)
        type_list.append(content_type)

    return pd.DataFrame({
        COL_URIS: uris,
        COL_STATUS_CODE: code_list,
        COL_CONTENT_TYPE: type_list,
    })
