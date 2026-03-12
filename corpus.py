"""
Backward-compatible corpus module.
Deprecated: Prefer importing from core.constants.
"""

from core.constants import (
    CONTENT_TYPES_RDF,
    CONTENT_TYPE_TO_FORMAT,
    HTTP_ACCEPT_HEADERS,
    CLASS_LIST,
    PROPERTY_LIST,
)

# Re-export with legacy names for backward compatibility
ContentTypeOfRDF = list(CONTENT_TYPES_RDF)
MapContentTypeToParserFormat = CONTENT_TYPE_TO_FORMAT.copy()
Headers = HTTP_ACCEPT_HEADERS.copy()
PropertyList = PROPERTY_LIST
OtherPropertyList = list(PROPERTY_LIST)  # Subset in original; using full list
ClassList = list(CLASS_LIST)
