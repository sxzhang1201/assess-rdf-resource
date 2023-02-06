from rdflib.graph import Graph
from rdflib.term import URIRef
import corpus
import numpy as np


def assess_parsable(df_uris):
    """

    :param df_uris:
    :return:
    """
    # subset resolvable URIs to be analyzed for the parsability metric
    df_uris['status_code'] = df_uris['status_code'].astype(str)
    uris_status_23 = df_uris[df_uris['status_code'].str.startswith(('2', '3'))]

    # add new column "rdf_type" to indicate whether this URI is of RDF content-type as "RDF" and "not RDF".
    uris_status_23.loc[:, 'whether RDF type'] = \
        np.where(uris_status_23['content-type'].isin(corpus.ContentTypeOfRDF), 'RDF', 'not RDF')

    parsed_content = []
    uri_undefined = []

    # iterate each URI and examine its parsed content
    for index, row in uris_status_23.iterrows():
        uri = row['uris']
        print(str(index) + '. ' + uri + ", " + row['content-type'])

        # if not RDF content-type, add "not applicable" to data frame, and skip the current loop
        if row['content-type'] not in corpus.ContentTypeOfRDF:
            parsed_content.append('not applicable')
            uri_undefined.append('not applicable')
            continue

        # parse URIs of RDF content-type
        try:
            temp_graph = Graph().parse(uri,
                                       format=corpus.MapContentTypeToParserFormat[row['content-type']])

            # get length of parsed graph
            parsed_content.append(len(temp_graph))

            validate_graph = Graph()
            validate_graph += temp_graph.triples((URIRef(uri), None, None))

            # if zero, indicating such term (URI) is not defined in the resolved content.
            if len(validate_graph) == 0:
                uri_undefined.append("undefined")
            else:
                uri_undefined.append("defined")

        # add the very special case if any parsing error occurs
        except Exception as e:
            # print(e)
            parsed_content.append(e)
            uri_undefined.append(e)

    # add parsing content to the data frame as the output
    uris_status_23.loc[:, 'parsing'] = parsed_content
    uris_status_23.loc[:, 'whether defined'] = uri_undefined

    return uris_status_23


if __name__ == '__main__':
    # g = Graph().parse('http://purl.obolibrary.org/obo/IAO_0000120')
    g = Graph().parse('http://purl.obolibrary.org/obo/IAO_0000102')

    # g = Graph().parse('http://purl.obolibrary.org/obo/IAO_0000708')
    # g = Graph().parse('http://www.w3.org/2002/07/owl#NamedIndividual')

    for s, p, o in g:
        print(s, p, o)

