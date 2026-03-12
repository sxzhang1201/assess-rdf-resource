#!/usr/bin/env python3
"""
RDF Resource Quality Assessment Tool.

Assesses resolvability, parsability, and consistency of RDF resources
as described in: Automated Approach for Minimal Quality Assessment of RDF Resources for Reuse.
"""

import datetime
import pickle
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from rdflib import Graph
from rdflib.term import URIRef

from config import ChunkSize, ListOfLABEL, MaxURIsForQuickTest, WhichResource
from core.logging_config import get_logger, setup_logging
from core.paths import get_output_paths, get_pickle_path
from functions.create_directory import create_directory
from functions.generate_report import build_graph
from functions.inspect_items import view_graph
from functions.load_resource import parse_data_local_or_remote as load_resource
from functions.split_list import split
from metrics.classify import get_uri_type
from metrics.consistency import run_consistency_assessment
from metrics.coverage import count_rdf_component
from metrics.parsability import assess_parsable
from metrics.resolvability import get_http_status_code_and_content_type
from quantitative_analysis import calculate_affected_triples_all, quantitative_analysis

logger = get_logger()

# Default number of triples to preview
PREVIEW_TRIPLE_LIMIT = 10


def _load_or_parse_graph(label: str) -> Graph:
    """Load RDF graph from pickle cache or parse from source."""
    pickle_path = get_pickle_path(label)
    resource_path = WhichResource[label]

    if pickle_path.exists():
        logger.info("Loading RDF graph from pickle: %s", pickle_path)
        with open(pickle_path, "rb") as f:
            return pickle.load(f)

    logger.info("Parsing RDF graph from: %s", resource_path)
    graph = load_resource(resource_path)
    pickle_path.parent.mkdir(parents=True, exist_ok=True)
    with open(pickle_path, "wb") as f:
        pickle.dump(graph, f, pickle.HIGHEST_PROTOCOL)
    return graph


def _run_resolvability_assessment(
    uris: List[str],
    paths: Dict[str, Path],
    assess: bool,
    chunk_size: int,
) -> pd.DataFrame:
    """Run resolvability tests and return results DataFrame."""
    if not assess:
        return pd.read_csv(paths["resolvable"], index_col=0)

    if len(uris) > chunk_size:
        chunks = list(split(uris, chunk_size))
        for i, chunk in enumerate(chunks):
            df_chunk = get_http_status_code_and_content_type(chunk)
            df_chunk.to_csv(
                str(paths["resolvable"]),
                mode="w" if i == 0 else "a",
                header=(i == 0),
                index=True,
            )
    else:
        df_uris = get_http_status_code_and_content_type(uris)
        df_uris.to_csv(str(paths["resolvable"]), index=True)

    return pd.read_csv(str(paths["resolvable"]), index_col=0)


def run_assessment(
    label: str,
    *,
    assess_resolvable: bool = True,
    test_parsable: bool = True,
    re_classify: bool = True,
    assess_consistency: bool = True,
) -> Dict[str, List[str]]:
    """
    Run quality assessment on an RDF resource.

    Args:
        label: Resource identifier (must exist in config.WhichResource).
        assess_resolvable: If True, run resolvability tests; else load cached results.
        test_parsable: If True, run parsability tests; else load cached results.
        re_classify: If True, re-classify URIs; else load cached results.
        assess_consistency: If True, run consistency tests; else load cached results.

    Returns:
        Dictionary with assessment results (non_resolvable_uris, undefined_uris, etc.).
    """
    setup_logging()

    if label not in WhichResource:
        raise ValueError(
            f"Unknown resource label '{label}'. "
            f"Available: {list(WhichResource.keys())}"
        )

    logger.info("Starting quality assessment for resource: %s", label)
    paths = get_output_paths(label)
    create_directory(str(paths["resolvable"].parent))

    # Load or parse RDF graph
    graph = _load_or_parse_graph(label)
    view_graph(graph, PREVIEW_TRIPLE_LIMIT)

    uris = count_rdf_component(rdf_graph=graph, rdf_term=URIRef)
    total_uris = len(uris)
    if MaxURIsForQuickTest is not None and total_uris > MaxURIsForQuickTest:
        uris = uris[:MaxURIsForQuickTest]
        logger.info("Quick test: assessing %d of %d URIs (set MaxURIsForQuickTest=None for full run)", len(uris), total_uris)
    else:
        logger.info("Resource has %d unique URIs", total_uris)

    # Step I: Resolvability
    logger.info("Step I: Testing resolvability of all URIs")
    df_uris = _run_resolvability_assessment(
        uris, paths, assess_resolvable, ChunkSize
    )
    df_uris.drop_duplicates(inplace=True)

    # Step II: Parsability
    logger.info("Step II: Testing parsability of resolvable URIs")
    if test_parsable:
        df_parsable = assess_parsable(df_uris)
        df_parsable.to_csv(str(paths["parsable"]), index=True)
    df_parsable = pd.read_csv(str(paths["parsable"]), index_col=0)

    # Step III & IV: Classification
    logger.info("Step III: Classifying parsable URIs")
    if re_classify:
        uris_defined = get_uri_type(df_parsable)
        uris_defined.to_csv(str(paths["intermediate"]), index=True)
    uris_defined = pd.read_csv(str(paths["intermediate"]), index_col=0)

    # Step V: Consistency
    logger.info("Step V: Testing consistency")
    if assess_consistency:
        uris_consistent = run_consistency_assessment(graph, uris_defined)
        uris_consistent.to_csv(str(paths["consistent"]), index=True)
    uris_consistent = pd.read_csv(str(paths["consistent"]), index_col=0)

    # Step VI: Quantitative analysis
    logger.info("Step VI: Computing statistics")
    assessment_result = quantitative_analysis(label)

    # Step VII: Generate report
    logger.info("Step VII: Generating assessment report")
    num_uris = len(uris)
    num_classes = len(uris_consistent[uris_consistent["uri type"] == "class"])
    num_properties = len(uris_consistent[uris_consistent["uri type"] == "property"])

    report_graph = build_graph(
        resource_uri=WhichResource[label],
        report_label=label,
        assessment_result=assessment_result,
        num_of_uris=num_uris,
        num_of_classes=num_classes,
        num_of_properties=num_properties,
    )
    report_graph.serialize(destination=str(paths["report"]))

    return assessment_result


def _format_affected_triples(affected: int, total: int) -> str:
    """Format affected triples count as 'n/total (pct%)'."""
    if total == 0:
        return "0/0 (0%)"
    pct = affected / total
    return f"{affected}/{total} ({pct:.1%})"


def execution(
    re_run: Optional[Dict[str, bool]] = None,
) -> None:
    """
    Execute assessment for all resources in ListOfLABEL.

    Args:
        re_run: Optional dict to control which steps to re-run. Keys:
            assess_resolvable, test_parsable, re_classify, assess_consistency.
    """
    setup_logging()
    re_run = re_run or {
        "assess_resolvable": True,
        "test_parsable": True,
        "re_classify": True,
        "assess_consistency": True,
    }

    coat_non_resolvable: Dict[str, str] = {}
    coat_undefined: Dict[str, str] = {}

    for label in ListOfLABEL:
        logger.info("Processing resource: %s", label)
        start_time = time.time()

        assessment_result = run_assessment(label, **re_run)

        with open(get_pickle_path(label), "rb") as f:
            graph = pickle.load(f)

        total_triples = len(graph)

        # Affected triples: non-resolvable URIs
        non_resolvable = assessment_result["non_resolvable_uris"]
        coat_nr = calculate_affected_triples_all(non_resolvable, graph)
        coat_non_resolvable[label] = _format_affected_triples(coat_nr, total_triples)

        # Affected triples: undefined URIs
        undefined = assessment_result["undefined_uris"]
        coat_ud = calculate_affected_triples_all(undefined, graph)
        coat_undefined[label] = _format_affected_triples(coat_ud, total_triples)

        elapsed = int(time.time() - start_time)
        logger.info("Time elapsed: %s", datetime.timedelta(seconds=elapsed))

    logger.info("Affected triples (non-resolvable URIs): %s", coat_non_resolvable)
    logger.info("Affected triples (undefined URIs): %s", coat_undefined)


if __name__ == "__main__":
    execution()
