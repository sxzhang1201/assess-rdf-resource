from rdflib.graph import Graph
from rdflib.namespace import RDF, RDFS
import corpus
from rdflib.term import URIRef


def extract_type(content_type_for_resolvable_uris):
    """

    :param content_type_for_resolvable_uris: a dictionary with URIs as keys (str) corresponding to their content-type as values (str)
    :return: 6 lists, respectively containing URIs of different types
    """
    # Initiate 4 lists
    class_list = []
    owl_datatype_property = []
    owl_object_property = []
    other_property_list = []

    # New list (August 22)
    no_parsed_content_uri_list = {}

    # print(" To get rdf:type information of {} parsable URIs".format(len(content_type_for_resolvable_uris)))

    # Investigate an URI
    for res_uri, content_type in content_type_for_resolvable_uris.items():
        print(" To get rdf:type information of {}".format(res_uri))
        print(res_uri)

        temp_graph = Graph().parse(res_uri, format=corpus.MapContentTypeToParserFormat[content_type])

        if len(temp_graph) == 0:
            no_parsed_content_uri_list[res_uri] = content_type

        # Get a list of "type" for that URI
        all_rdf_type_triples = Graph()
        all_rdf_type_triples += temp_graph.triples((URIRef(res_uri), RDF.type, None))
        # Get a list of "subClassOf" for that URI
        all_subclass_of_triples = Graph()
        all_subclass_of_triples += temp_graph.triples((URIRef(res_uri), RDFS.subClassOf, None))

        all_types_graph = all_rdf_type_triples + all_subclass_of_triples

        # All types of one URI
        for s, p, o in all_types_graph:
            print(s, p, o)
            # owl:DatatypeProperty
            if str(o) == "http://www.w3.org/2002/07/owl#DatatypeProperty":
                owl_datatype_property.append(res_uri)
                break

            # owl:ObjectProperty
            if str(o) == "http://www.w3.org/2002/07/owl#ObjectProperty":
                owl_object_property.append(res_uri)
                break

            # Other property
            if str(o) in corpus.OtherPropertyList:
                other_property_list.append(res_uri)
                break

            if str(o) in corpus.ClassList:
                class_list.append(res_uri)
                break

    property_list = owl_datatype_property + owl_object_property + other_property_list
    others_list = [item for item in content_type_for_resolvable_uris.keys() if item not in property_list + class_list]

    # Update tempoary August 22nd
    for this_uri, this_content_type in no_parsed_content_uri_list.items():
        print('{},{}'.format(this_uri, this_content_type))

    return class_list, property_list, owl_datatype_property, owl_object_property, other_property_list, others_list
