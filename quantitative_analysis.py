import pandas as pd
from rdflib.graph import Graph
from rdflib.term import URIRef


def quantitative_analysis(label):

    # directory for storing results
    path_dic = {
        'resolvable': 'output/{}/uri-resolvable-{}.csv'.format(label, label),
        'parsable': 'output/{}/uri-parsable-{}.csv'.format(label, label),
        'intermediate': 'output/{}/uri-intermediate-{}.csv'.format(label, label),
        'consistent': 'output/{}/uri-consistent-{}.csv'.format(label, label),
    }

    # Metric 1 - Resolvability Dimension - uriNonResolvableMetric - status code 4xx or 5xx
    df_uris_status_code = pd.read_csv(path_dic['resolvable'], index_col=0)
    # set 'status_code' as string (rather than int)
    df_uris_status_code['status_code'] = df_uris_status_code['status_code'].astype(str)

    # subset URIs according to status code
    df_uris_resolvable = df_uris_status_code[df_uris_status_code['status_code'].str.startswith(('2', '3'))]
    df_uris_non_resolvable = df_uris_status_code[df_uris_status_code['status_code'].str.startswith(('4', '5'))]

    result_resolvability = df_uris_non_resolvable['uris'].values.tolist()

    count_of_all_uris = len(df_uris_non_resolvable) + len(df_uris_resolvable)

    if len(result_resolvability) != 0:
        print("\nThe result of non-resolvable URIs: ")
        print(result_resolvability)

    # Metric 2 - Parsability - uriNonParsableMetric - RDF content-type but no triples parsed
    df_uris_parsable = pd.read_csv(path_dic['parsable'], index_col=0)
    uris_rdf = df_uris_parsable.loc[df_uris_parsable["whether RDF type"] == 'RDF']

    # get result
    result_parsability = uris_rdf.loc[uris_rdf['parsing'] == '0']['uris'].values.tolist()

    if len(result_parsability) != 0:
        print("\nThe result of non-parsable URIs: ")
        print(result_parsability)

    # Metric 3 - Consistency - Undefined URIs - 'whether defined' --> 'undefined'
    undefined_uris = uris_rdf.loc[uris_rdf['whether defined'] == 'undefined']['uris'].values.tolist()

    if len(undefined_uris) != 0:
        print("\nThe result of undefined URIs: ")
        print(undefined_uris)

    # Metric 4 - Consistency - misplaced classes and properties
    df_uris_consistent = pd.read_csv(path_dic['consistent'], index_col=0)
    class_uris = df_uris_consistent.loc[df_uris_consistent["uri type"] == "class"]
    property_uris = df_uris_consistent.loc[df_uris_consistent["uri type"] == "property"]

    misplaced_class = class_uris.loc[class_uris['misplaced'] == 'error']['uris'].values.tolist()
    misplaced_property = property_uris.loc[property_uris['misplaced'] == 'error']['uris'].values.tolist()

    if len(misplaced_class) != 0:
        print("\nThe result of misplaced classes: ")
        print(misplaced_class)

    if len(misplaced_property) != 0:
        print("\nThe result of misplaced properties: ")
        print(misplaced_property)

    # Metric 5 - Consistency - misuse of owl:dataTypeProperty or owl:objectProperty
    owl_datatype_property = property_uris.loc[property_uris['property type'] == 'owl_datatype_property']
    owl_object_property = property_uris.loc[property_uris['property type'] == 'owl_object_property']
    misused_owl_datatype_property = \
        owl_datatype_property.loc[owl_datatype_property['misused owl property'] == 'misused']['uris'].values.tolist()
    misused_owl_object_property = \
        owl_object_property.loc[owl_object_property['misused owl property'] == 'misused']['uris'].values.tolist()

    if len(misused_owl_datatype_property) != 0:
        print("\nThe result of misused owl:dataTypeProperty: ")
        print(misused_owl_datatype_property)

    if len(misused_owl_object_property) != 0:
        print("\nThe result of misused owl:objectProperty: ")
        print(misused_owl_object_property)

    assessment_result = {
        'non_resolvable_uris': result_resolvability,
        'non_parsable_uris': result_parsability,
        'undefined_uris': undefined_uris,
        'misplaced_class': misplaced_class,
        'misplaced_property': misplaced_property,
        'misused_owl_datatype': misused_owl_datatype_property,
        'misused_owl_object': misused_owl_object_property,
    }

    return assessment_result


def calculate_affected_triples_per_uri(bad_uri, target_graph):
    """
    Get the count of triples affected by the bad URI. This count is fitting to resolvable and parsable issues, but
    it is NOT suitable for classes and properties.
    :param bad_uri: string.
    :param target_graph: rdflib graph.
    :return: int. The count of triples that are affected by this URI.
    """

    # initiate an empty graph for storing affected triples
    temp_graph = Graph()

    # collect all triples using this URI
    temp_graph = temp_graph + target_graph.triples((URIRef(bad_uri), None, None))
    temp_graph = temp_graph + target_graph.triples((None, URIRef(bad_uri), None))
    temp_graph = temp_graph + target_graph.triples((None, None, URIRef(bad_uri)))

    return len(temp_graph)


def calculate_affected_triples_all(list_of_bad_uris, target_graph):
    """

    :param list_of_bad_uris:
    :param target_graph:
    :return:
    """

    # initiate an empty graph for storing affected triples
    overall_graph = Graph()

    for bad_uri in list_of_bad_uris:

        # collect all triples using this URI
        overall_graph += target_graph.triples((URIRef(bad_uri), None, None))
        overall_graph += target_graph.triples((None, URIRef(bad_uri), None))
        overall_graph += target_graph.triples((None, None, URIRef(bad_uri)))

    return len(overall_graph)
