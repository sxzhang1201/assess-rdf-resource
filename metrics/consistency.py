from rdflib.graph import Graph
from corpus import PropertyList
from rdflib.namespace import RDF
from rdflib.term import URIRef, Literal

from functions.load_resource import parse_data_local_or_remote as load_resource

def detect_misplaced_class(g, class_list):

    # Initiate an empty list to store URIs of misused classes
    misused_class_list = []

    # Examine each class URI
    for class_uri in class_list:
        # Get subset of RDF graph using this class as predicate
        temp_graph = Graph()
        temp_graph += g.triples((None, URIRef(class_uri), None))

        # If zero, indicating this is no misused classes.
        if len(temp_graph) != 0:
            misused_class_list.append(class_uri)
            print("  - The class {} is not correctly used in this triple".format(class_uri))
            for s, p, o in temp_graph:
                print(s, p, o)

    if len(misused_class_list) == 0:
        print("  - No class is used as predicate")

    return misused_class_list


def detect_misplaced_property(g, property_list):

    # Initiate an empty list to store URIs of misused properties
    misplaced_property_list = []

    # Filter properties because these properties terms are both owl:Class and rdfs:Property
    test_property_list = [item for item in property_list if URIRef(item) not in PropertyList]
    print(test_property_list)

    for s, p, o in g:
        print(s, p, o)

    for property_uri in test_property_list:
        # Get subset of RDF graph using this property as the object of rdf:type triple
        temp_graph = Graph()
        temp_graph += g.triples((None, RDF.type, URIRef(property_uri)))

        for s, p, o in temp_graph:
            print(s, p, o)

        # If zero, indicating this is no misused classes.
        if len(temp_graph) != 0:
            misplaced_property_list.append(property_uri)
            print("  - The property {} is not correctly used in this triple".format(property_uri))
            for s, p, o in temp_graph:
                print(s, p, o)

    if len(misplaced_property_list) == 0:
        print("  - No property is used as the class, i.e., the object in the rdf:type triples.")

    return misplaced_property_list


def detect_misused_datatype_property(g, datatype_property_list):
    misused_datatype_property_list = []

    for datatype_property_uri in datatype_property_list:
        temp_graph = Graph()
        temp_graph += g.triples((None, datatype_property_uri, None))

        for _, _, o in temp_graph:
            if not isinstance(o, Literal):
                misused_datatype_property_list.append(datatype_property_uri)
                print("  - The owl:DatatypeProperty {} is incorrectly used because {} is not literal".
                      format(datatype_property_uri, o))

    if len(misused_datatype_property_list) == 0:
        print("  - No owl:Datatype Property is incorrectly used")

    return misused_datatype_property_list


def detect_misused_object_property(g, object_property_list):

    misused_object_property_list = []

    for object_property_uri in object_property_list:
        temp_graph = Graph()
        temp_graph += g.triples((None, object_property_uri, None))

        for _, _, o in temp_graph:
            if not isinstance(o, URIRef):
                misused_object_property_list.append(object_property_uri)
                print("  - The owl:ObjectProperty  {} is incorrectly used because {} is not an URI".
                      format(object_property_uri, o))

    if len(misused_object_property_list) == 0:
        print("  - No owl:DatatypeProperty is incorrectly used")

    return misused_object_property_list


def run_consistency(g, class_list, property_list, datatype_property_list, object_property_list):
    misplaced_class_list = detect_misplaced_class(g, class_list)
    print("misplaced class list check 1:")
    print(misplaced_class_list)
    misplaced_property_list = detect_misplaced_property(g, property_list)
    misused_datatype_property_list = detect_misused_datatype_property(g, datatype_property_list)
    misused_object_property_list = detect_misused_object_property(g, object_property_list)

    return misplaced_class_list, misplaced_property_list, \
           misused_datatype_property_list, misused_object_property_list
