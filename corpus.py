from rdflib.term import URIRef
"""
# Class
"http://www.w3.org/2002/07/owl#Class"

# Property
"http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"

# DatatypeProperty
"http://www.w3.org/2002/07/owl#DatatypeProperty"

# ObjectProperty
"http://www.w3.org/2002/07/owl#ObjectProperty"

"""

OtherPropertyList = [
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property",
    "http://www.w3.org/2002/07/owl#InverseFunctionalProperty",
    "http://www.w3.org/2002/07/owl#FunctionalProperty",
    "http://www.w3.org/2002/07/owl#TransitiveProperty",
    "http://www.w3.org/2002/07/owl#SymmetricProperty",
    "http://www.w3.org/2002/07/owl#AnnotationProperty",
    "http://www.w3.org/2002/07/owl#DeprecatedProperty",
    "http://www.w3.org/2002/07/owl#OntologyProperty"
]

ClassList = [
    "http://www.w3.org/2000/01/rdf-schema#Class",
    "http://www.w3.org/2002/07/owl#Class"
]

PropertyList = [
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
    "http://www.w3.org/2002/07/owl#IrreflexiveProperty"
]

ContentTypeOfRDF = [
    "text/turtle",
    "application/rdf+xml",
    "application/ld+json",
    "text/n3",
    "application/x-turtle"]

MapContentTypeToParserFormat = {
    "text/turtle": 'turtle',
    "application/rdf+xml": 'xml',
    "application/ld+json": 'json-ld',
    "text/n3": 'n3',
    "application/x-turtle": 'turtle',
    'text/plain': 'xml'
}


Headers = {"Accept": "text/turtle, application/x-turtle,"   # Turtle
                     "application/rdf+xml;q=0.9, "          # RDF/XML
                     "application/ld+json;q=0.8, "          # JSON-LD
                     "text/n3;q=0.7,"                       # Notion 3
                     "*/*;q=0.1"}                           # Others

