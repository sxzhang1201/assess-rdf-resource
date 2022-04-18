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
    URIRef("http://www.w3.org/2002/07/owl#ObjectProperty"),
    URIRef("http://www.w3.org/2002/07/owl#DatatypeProperty"),
    URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"),
    URIRef("http://www.w3.org/2002/07/owl#InverseFunctionalProperty"),
    URIRef("http://www.w3.org/2002/07/owl#FunctionalProperty"),
    URIRef("http://www.w3.org/2002/07/owl#TransitiveProperty"),
    URIRef("http://www.w3.org/2002/07/owl#SymmetricProperty"),
    URIRef("http://www.w3.org/2002/07/owl#AnnotationProperty"),
    URIRef("http://www.w3.org/2002/07/owl#DeprecatedProperty"),
    URIRef("http://www.w3.org/2002/07/owl#OntologyProperty"),
    URIRef("http://www.w3.org/2002/07/owl#IrreflexiveProperty")
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
    "application/x-turtle": 'turtle'
}
