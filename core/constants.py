"""
Central constants for RDF resource assessment.
"""

from pathlib import Path

# Directory structure
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
PICKLE_DIR = PROJECT_ROOT / "pickle"

# RDF content types and parser mappings
CONTENT_TYPES_RDF = frozenset([
    "text/turtle",
    "application/rdf+xml",
    "application/ld+json",
    "text/n3",
    "application/x-turtle",
])

CONTENT_TYPE_TO_FORMAT = {
    "text/turtle": "turtle",
    "application/rdf+xml": "xml",
    "application/ld+json": "json-ld",
    "text/n3": "n3",
    "application/x-turtle": "turtle",
    "text/plain": "xml",
}

# HTTP headers for content negotiation
HTTP_ACCEPT_HEADERS = {
    "Accept": (
        "text/turtle, application/x-turtle, "
        "application/rdf+xml;q=0.9, "
        "application/ld+json;q=0.8, "
        "text/n3;q=0.7, "
        "*/*;q=0.1"
    )
}

# OWL/RDF type URIs for classification
OWL_CLASS = "http://www.w3.org/2002/07/owl#Class"
RDFS_CLASS = "http://www.w3.org/2000/01/rdf-schema#Class"
OWL_DATATYPE_PROPERTY = "http://www.w3.org/2002/07/owl#DatatypeProperty"
OWL_OBJECT_PROPERTY = "http://www.w3.org/2002/07/owl#ObjectProperty"
RDF_PROPERTY = "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"

PROPERTY_TYPE_URIS = frozenset([
    RDF_PROPERTY,
    "http://www.w3.org/2002/07/owl#InverseFunctionalProperty",
    "http://www.w3.org/2002/07/owl#FunctionalProperty",
    "http://www.w3.org/2002/07/owl#TransitiveProperty",
    "http://www.w3.org/2002/07/owl#SymmetricProperty",
    "http://www.w3.org/2002/07/owl#AnnotationProperty",
    "http://www.w3.org/2002/07/owl#DeprecatedProperty",
    "http://www.w3.org/2002/07/owl#OntologyProperty",
    "http://www.w3.org/2002/07/owl#IrreflexiveProperty",
])

# HTTP status code prefixes
STATUS_RESOLVABLE = ("2", "3")
STATUS_NON_RESOLVABLE = ("4", "5")
REQUEST_ERROR_STATUS = "RequestError"

# DataFrame column names
COL_URIS = "uris"
COL_STATUS_CODE = "status_code"
COL_CONTENT_TYPE = "content-type"
COL_WHETHER_RDF = "whether RDF type"
COL_PARSING = "parsing"
COL_WHETHER_DEFINED = "whether defined"
COL_URI_TYPE = "uri type"
COL_PROPERTY_TYPE = "property type"
COL_MISPLACED = "misplaced"
COL_MISUSED_OWL = "misused owl property"

# OWL/RDFS type lists for consistency checks
CLASS_LIST = frozenset([
    "http://www.w3.org/2000/01/rdf-schema#Class",
    "http://www.w3.org/2002/07/owl#Class",
])

PROPERTY_LIST = frozenset([
    "http://www.w3.org/2002/07/owl#ObjectProperty",
    "http://www.w3.org/2002/07/owl#DatatypeProperty",
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property",
    "http://www.w3.org/2002/07/owl#InverseFunctionalProperty",
    "http://www.w3.org/2002/07/owl#FunctionalProperty",
    "http://www.w3.org/2002/07/owl#TransitiveProperty",
    "http://www.w3.org/2002/07/owl#SymmetricProperty",
    "http://www.w3.org/2002/07/owl#AnnotationProperty",
    "http://www.w3.org/2002/07/owl#DeprecatedProperty",
    "http://www.w3.org/2002/07/owl#OntologyProperty",
    "http://www.w3.org/2002/07/owl#IrreflexiveProperty",
])
