from rdflib.graph import Graph
from rdflib.term import URIRef
import corpus


def divide_res_uri_by_content_type(resolvable_uris_with_content_type):
    """
    Divide resolvable URIs by their content type (if RDF or not)
    :param resolvable_uris_with_content_type: a dictionary {"URI": content-type}
    :return: two dictionaries
    """

    # Initiate dictionaries
    res_uri_indicate_rdf = {}
    res_uri_not_indicate_rdf = {}

    # Dividing
    for res_uri, content_type in resolvable_uris_with_content_type.items():
        if content_type in corpus.ContentTypeOfRDF:
            res_uri_indicate_rdf[res_uri] = content_type
        else:
            res_uri_not_indicate_rdf[res_uri] = content_type

    return res_uri_indicate_rdf, res_uri_not_indicate_rdf


def validate_rdf_content_type(res_uri_indicate_rdf):
    """
    Identify errors that fail one parsability metric and one consistency metric
    :param res_uri_indicate_rdf: dictionary{uri: content-type}
    :return: 2 lists and 1 dictionary, containing erroneous URIs
    """

    # Error 1: this URI (though indicated as an RDF content-type) cannot refer to any triples.
    error1_rdf_content_no_triple = {}

    # Error 2: the term (URI) is not defined in the resolved content
    error2_uri_is_not_defined = []

    # Error: this URI is not parsable (can be categorised into Error 1. (Further investigate)
    # parsability_parse_error = {}

    parsable_uri = {}

    progress_count = 1

    # Inspect each resolvable URI (note that this URI is string not URIRef)
    for res_uri_str, content_type in res_uri_indicate_rdf.items():
        # print(res_uri_str, content_type)

        print(" {}'s content-type is {} - Progress {}/{}".format(res_uri_str, content_type,
                                                                 progress_count, len(res_uri_indicate_rdf)))

        progress_count = progress_count + 1

        # Try parsing. In RDFLib, the `format` variable is different from content-type, thus needing this map.
        try:
            temp_graph = Graph().parse(res_uri_str,
                                       format=corpus.MapContentTypeToParserFormat[content_type])

            # Zero indicating that no single triple is obtained.
            if len(temp_graph) == 0:
                print("  - This URI (though indicated as an RDF content-type) cannot refer to any triples.")
                error1_rdf_content_no_triple[res_uri_str] = content_type
                continue

            # Now further test
            validate_graph = Graph()
            validate_graph += temp_graph.triples((URIRef(res_uri_str), None, None))

            # if zero, indicating such term (URI) is not defined in the resolved content.
            if len(validate_graph) == 0:
                print(" - This URI is not defined in the resolved RDF content. ")
                error2_uri_is_not_defined.append(URIRef(res_uri_str))

            else:
                parsable_uri[res_uri_str] = content_type

        except Exception as e:
            print(e)
            # Record parsing error
            error1_rdf_content_no_triple[res_uri_str] = content_type

    return error1_rdf_content_no_triple, error2_uri_is_not_defined, parsable_uri


def assess_parsable(resolvable_uris_with_content_type):
    # Note: "res_uri_not_indicate_rdf" is temporarily not used but useful for "predicate-content-type" research
    res_uri_indicate_rdf, res_uri_not_indicate_rdf = divide_res_uri_by_content_type(resolvable_uris_with_content_type)

    error1_rdf_content_no_triple, error2_uri_is_not_defined, parsable_uri = validate_rdf_content_type(res_uri_indicate_rdf)

    return res_uri_indicate_rdf, \
           res_uri_not_indicate_rdf, \
           error1_rdf_content_no_triple, \
           error2_uri_is_not_defined, \
           parsable_uri

