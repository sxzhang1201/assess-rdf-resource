import logging

import pandas as pd
from rdflib import Graph
from rdflib.term import URIRef

from core.paths import get_output_paths

logger = logging.getLogger("assess_rdf")


def quantitative_analysis(label: str) -> dict:
    """
    Aggregate assessment results from CSV files into a single result dictionary.

    Args:
        label: Resource identifier.

    Returns:
        Dictionary with keys: non_resolvable_uris, non_parsable_uris, undefined_uris,
        misplaced_class, misplaced_property, misused_owl_datatype, misused_owl_object.
    """
    paths = get_output_paths(label)

    # Metric 1 - Resolvability: status code 4xx or 5xx
    df_uris_status_code = pd.read_csv(str(paths['resolvable']), index_col=0)
    # set 'status_code' as string (rather than int)
    df_uris_status_code['status_code'] = df_uris_status_code['status_code'].astype(str)

    # subset URIs according to status code
    df_uris_resolvable = df_uris_status_code[df_uris_status_code['status_code'].str.startswith(('2', '3'))]
    df_uris_non_resolvable = df_uris_status_code[df_uris_status_code['status_code'].str.startswith(('4', '5'))]

    result_resolvability = df_uris_non_resolvable['uris'].values.tolist()

    count_of_all_uris = len(df_uris_non_resolvable) + len(df_uris_resolvable)

    if result_resolvability:
        logger.info("Non-resolvable URIs: %s", result_resolvability)

    # Metric 2 - Parsability: RDF content-type but no triples parsed
    df_uris_parsable = pd.read_csv(str(paths['parsable']), index_col=0)
    uris_rdf = df_uris_parsable.loc[df_uris_parsable["whether RDF type"] == 'RDF']

    # Non-parsable: RDF type but parsing returned 0 triples (stored as '0' or 0)
    parsing_col = uris_rdf['parsing'].astype(str)
    result_parsability = uris_rdf.loc[parsing_col == '0']['uris'].values.tolist()

    if result_parsability:
        logger.info("Non-parsable URIs: %s", result_parsability)

    # Metric 3 - Consistency - Undefined URIs - 'whether defined' --> 'undefined'
    undefined_uris = uris_rdf.loc[uris_rdf['whether defined'] == 'undefined']['uris'].values.tolist()

    if undefined_uris:
        logger.info("Undefined URIs: %s", undefined_uris)

    # Metric 4 - Consistency: misplaced classes and properties
    df_uris_consistent = pd.read_csv(str(paths['consistent']), index_col=0)
    class_uris = df_uris_consistent.loc[df_uris_consistent["uri type"] == "class"]
    property_uris = df_uris_consistent.loc[df_uris_consistent["uri type"] == "property"]

    # Classes use 'misplaced', properties use 'error' (from consistency module)
    misplaced_class = class_uris.loc[class_uris['misplaced'] == 'misplaced']['uris'].values.tolist()
    misplaced_property = property_uris.loc[property_uris['misplaced'] == 'error']['uris'].values.tolist()

    if misplaced_class:
        logger.info("Misplaced classes: %s", misplaced_class)
    if misplaced_property:
        logger.info("Misplaced properties: %s", misplaced_property)

    # Metric 5 - Consistency - misuse of owl:dataTypeProperty or owl:objectProperty
    owl_datatype_property = property_uris.loc[property_uris['property type'] == 'owl_datatype_property']
    owl_object_property = property_uris.loc[property_uris['property type'] == 'owl_object_property']
    misused_owl_datatype_property = \
        owl_datatype_property.loc[owl_datatype_property['misused owl property'] == 'misused']['uris'].values.tolist()
    misused_owl_object_property = \
        owl_object_property.loc[owl_object_property['misused owl property'] == 'misused']['uris'].values.tolist()

    if misused_owl_datatype_property:
        logger.info("Misused owl:DatatypeProperty: %s", misused_owl_datatype_property)
    if misused_owl_object_property:
        logger.info("Misused owl:ObjectProperty: %s", misused_owl_object_property)

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
