"""Consistency metrics: misplaced classes/properties, misused OWL property types."""

import logging

from rdflib import Graph
from rdflib.namespace import RDF, RDFS
from rdflib.term import Literal, URIRef

from core.constants import PROPERTY_LIST

logger = logging.getLogger("assess_rdf")


def detect_misplaced_class(graph: Graph, class_uri: str) -> str:
    """
    Check if a class URI is incorrectly used as a predicate.

    Args:
        graph: RDF graph to check.
        class_uri: URI of the class.

    Returns:
        'misplaced' if used as predicate, else 'correct'.
    """
    triples = list(graph.triples((None, URIRef(class_uri), None)))
    if triples:
        for s, p, o in triples:
            logger.debug("Misplaced class %s as predicate in: %s %s %s", class_uri, s, p, o)
        return "misplaced"
    return "correct"


def detect_misplaced_property(graph: Graph, property_uri: str) -> str:
    """
    Check if a property URI is incorrectly used as a class (rdf:type or rdfs:subClassOf).

    Args:
        graph: RDF graph to check.
        property_uri: URI of the property.

    Returns:
        'error' if misused as class, 'warning for definition' if in PropertyList, else 'correct'.
    """
    triples = list(graph.triples((None, RDF.type, URIRef(property_uri))))
    triples += list(graph.triples((None, RDFS.subClassOf, URIRef(property_uri))))

    if property_uri in PROPERTY_LIST:
        return "warning for definition"

    if triples:
        for s, p, o in triples:
            logger.debug("Misplaced property %s as class in: %s %s %s", property_uri, s, p, o)
        return "error"
    return "correct"


def detect_misused_datatype_or_object_property(
    graph: Graph,
    property_uri: str,
    property_type: str,
) -> str:
    """
    Check if owl:DatatypeProperty or owl:ObjectProperty is used correctly.

    DatatypeProperty must have Literal objects; ObjectProperty must have URI objects.

    Args:
        graph: RDF graph to check.
        property_uri: URI of the property.
        property_type: 'owl_datatype_property' or 'owl_object_property'.

    Returns:
        'misused' if incorrect usage, else 'correct'.
    """
    triples = list(graph.triples((None, URIRef(property_uri), None)))

    if property_type == "owl_datatype_property":
        for subj, pred, obj in triples:
            if not isinstance(obj, Literal):
                logger.debug(
                    "DatatypeProperty %s misused: %s has non-literal object %s",
                    property_uri, subj, obj,
                )
                return "misused"

    elif property_type == "owl_object_property":
        for subj, pred, obj in triples:
            if not isinstance(obj, URIRef):
                logger.debug(
                    "ObjectProperty %s misused: %s has non-URI object %s",
                    property_uri, subj, obj,
                )
                return "misused"

    return "correct"


def run_consistency_assessment(graph: Graph, df_uris_defined: "pd.DataFrame") -> "pd.DataFrame":
    """
    Run consistency checks on classified URIs.

    Args:
        graph: RDF graph being assessed.
        df_uris_defined: DataFrame with uri type and property type columns.

    Returns:
        DataFrame with added columns: misplaced, misused owl property.
    """
    import pandas as pd

    df = df_uris_defined.copy()
    misplaced_list = []
    misused_list = []

    for _, row in df.iterrows():
        uri = row["uris"]
        uri_type = str(row["uri type"])

        if uri_type == "class":
            misplaced_list.append(detect_misplaced_class(graph, uri))
            misused_list.append("not applicable")

        elif uri_type == "property":
            misplaced_list.append(detect_misplaced_property(graph, uri))
            prop_type = str(row.get("property type", ""))
            if prop_type in ("owl_datatype_property", "owl_object_property"):
                misused_list.append(
                    detect_misused_datatype_or_object_property(graph, uri, prop_type)
                )
            else:
                misused_list.append("not applicable")

        else:
            misplaced_list.append("not applicable")
            misused_list.append("not applicable")

    df["misplaced"] = misplaced_list
    df["misused owl property"] = misused_list
    return df
