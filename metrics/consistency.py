from rdflib.graph import Graph
from corpus import PropertyList
from rdflib.namespace import RDF, RDFS
from rdflib.term import URIRef, Literal


def detect_misplaced_class(graph, class_uri):
    """

    :param graph: rdflib graph object, i.e., the target graph that each URI is being used.
    :param class_uri: pandas data frame, containing all URIs of 'class' type.
    :return: updated pandas data frame having an additional column describing the results of misplaced class metric.
    """

    temp_graph = Graph()
    temp_graph += graph.triples((None, URIRef(class_uri), None))

    # If zero, indicating this is no misused classes.
    if len(temp_graph) != 0:

        print("The URI {} as a class is incorrectly used as a predicate in this triple: ".format(class_uri))
        for s, p, o in temp_graph:
            print(s, p, o)
        return 'misplaced'

    else:
        return 'correct'


def detect_misplaced_property(graph, property_uri):
    """

    :param graph:
    :param property_uri:
    :return:
    """

    temp_graph = Graph()
    temp_graph += graph.triples((None, RDF.type, URIRef(property_uri)))
    temp_graph += graph.triples((None, RDFS.subClassOf, URIRef(property_uri)))

    # for s, p, o in temp_graph:
    #     print(s, p, o)

    # if in, meaning that this triple is the one to define a new property, thus not regarded as an error
    if property_uri in PropertyList:
        return "warning for definition"

    # If not zero, meaning that this property is
    if len(temp_graph) != 0:
        print("The property {} is incorrectly used as a class in this triple: ".format(property_uri))
        for s, p, o in temp_graph:
            print(s, p, o)
        return 'error'

    else:
        return 'correct'


def detect_misused_datatype_or_object_property(graph, property_uri, property_type):
    """

    :param graph: rdflib graph
    :param property_uri:
    :param  property_type:
    :return:
    """

    # subset all triples using this property
    temp_graph = Graph()
    temp_graph += graph.triples((None, URIRef(property_uri), None))

    if str(property_type) == 'owl_datatype_property':

        for subj, pred, obj in temp_graph:
            if not isinstance(obj, Literal):
                print(" The owl:DatatypeProperty {} is incorrectly used in {} {} {} \n because {} is not literal. ".
                      format(property_uri, subj, pred, obj, obj))

                return 'misused'

    if str(property_type) == 'owl_object_property':
        for subj, pred, obj in temp_graph:
            if not isinstance(obj, URIRef):
                print(" The owl:ObjectProperty {} is incorrectly used in {} {} {} \n because {} is not a URI. ".
                      format(property_uri, subj, pred, obj, obj))

                return 'misused'

    # print(" The property {} is correctly used.".format(property_uri))

    return 'correct'


def run_consistency_assessment(graph, df_uris_defined):

    # Initiate an empty list to store results of consistency checking
    misplaced_list = []
    misused_owl_property_list = []

    # Examine each URI
    for index, row in df_uris_defined.iterrows():
        uri = row['uris']
        uri_type = row['uri type']

        # assess metric: misplaced classes
        if str(uri_type) == 'class':
            misplaced_list.append(detect_misplaced_class(graph, uri))
            misused_owl_property_list.append('not applicable')

        elif str(uri_type) == 'property':
            misplaced_list.append(detect_misplaced_property(graph, uri))

            # get the type of a property: whether datatype or object property (owl)
            property_type = row['property type']

            if str(property_type) == 'owl_datatype_property' or str(property_type) == 'owl_object_property':
                misused_owl_property_list.append(detect_misused_datatype_or_object_property(graph, uri, property_type))
            else:
                misused_owl_property_list.append('not applicable')

        else:
            misplaced_list.append('not applicable')
            misused_owl_property_list.append('not applicable')

    # add results of detecting misplaced classes or properties to the original data frame
    df_uris_defined.loc[:, 'misplaced'] = misplaced_list

    # add results of misused owl:datatypeProperty or owl:objectProperty
    df_uris_defined.loc[:, 'misused owl property'] = misused_owl_property_list

    return df_uris_defined
