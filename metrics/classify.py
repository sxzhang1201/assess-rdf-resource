"""URI classification: determine if URIs are classes, properties, or unknown."""

import logging
from typing import Tuple

import pandas as pd
from rdflib import Graph
from rdflib.namespace import RDF, RDFS
from rdflib.term import URIRef

from core.constants import COL_CONTENT_TYPE, COL_PROPERTY_TYPE, COL_URI_TYPE, CONTENT_TYPE_TO_FORMAT

logger = logging.getLogger("assess_rdf")

# OWL/RDF type URIs for classification
OWL_DATATYPE_PROPERTY = "http://www.w3.org/2002/07/owl#DatatypeProperty"
OWL_OBJECT_PROPERTY = "http://www.w3.org/2002/07/owl#ObjectProperty"
OWL_CLASS = "http://www.w3.org/2002/07/owl#Class"
RDFS_CLASS = "http://www.w3.org/2000/01/rdf-schema#Class"
RDF_PROPERTY = "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"

PROPERTY_TYPES = [
    OWL_DATATYPE_PROPERTY,
    "http://www.w3.org/2002/07/owl#InverseFunctionalProperty",
    "http://www.w3.org/2002/07/owl#FunctionalProperty",
    "http://www.w3.org/2002/07/owl#TransitiveProperty",
    "http://www.w3.org/2002/07/owl#SymmetricProperty",
    "http://www.w3.org/2002/07/owl#AnnotationProperty",
    "http://www.w3.org/2002/07/owl#OntologyProperty",
    "http://www.w3.org/2002/07/owl#DeprecatedProperty",
]


def _classify_uri(uri: str, content_type: str) -> Tuple[str, str]:
    """
    Classify a single URI as class, property (with subtype), or unknown.

    Returns:
        Tuple of (uri_type, property_type).
    """
    parse_format = CONTENT_TYPE_TO_FORMAT.get(content_type, "xml")
    graph = Graph().parse(uri, format=parse_format)
    uri_ref = URIRef(uri)

    # Check for DatatypeProperty (or rdfs:range Literal)
    if (uri_ref, RDF.type, URIRef(OWL_DATATYPE_PROPERTY)) in graph:
        return "property", "owl_datatype_property"
    if (uri_ref, RDFS.range, RDFS.Literal) in graph:
        return "property", "owl_datatype_property"

    # Check for ObjectProperty
    if (uri_ref, RDF.type, URIRef(OWL_OBJECT_PROPERTY)) in graph:
        return "property", "owl_object_property"

    # Check for other property types
    for prop_uri in PROPERTY_TYPES:
        if (uri_ref, RDF.type, URIRef(prop_uri)) in graph:
            return "property", "other_property"

    # Check for rdf:Property
    if (uri_ref, RDF.type, URIRef(RDF_PROPERTY)) in graph:
        return "property", "other_property"

    # Check for class
    if (uri_ref, RDF.type, URIRef(OWL_CLASS)) in graph:
        return "class", "not applicable"
    if (uri_ref, RDF.type, URIRef(RDFS_CLASS)) in graph:
        return "class", "not applicable"

    return "unknown", "not applicable"


def get_uri_type(uris_rdf: pd.DataFrame) -> pd.DataFrame:
    """
    Classify parsable URIs as class, property, or unknown.

    Args:
        uris_rdf: DataFrame with parsability results. Must include 'whether defined' == 'defined'.

    Returns:
        DataFrame with added columns: uri type, property type.
    """
    defined = uris_rdf[uris_rdf["whether defined"] == "defined"].copy()
    uri_types = []
    property_types = []

    for index, row in defined.iterrows():
        uri = row["uris"]
        content_type = row[COL_CONTENT_TYPE]
        logger.debug("Classifying URI: %s", uri)

        uri_type, prop_type = _classify_uri(uri, content_type)
        uri_types.append(uri_type)
        property_types.append(prop_type)

    defined[COL_URI_TYPE] = uri_types
    defined[COL_PROPERTY_TYPE] = property_types
    return defined
