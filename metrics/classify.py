from rdflib.graph import Graph
from rdflib.namespace import RDF, RDFS
import corpus
from rdflib.term import URIRef


def get_uri_type(uris_rdf):
    """

    :param uris_rdf: a data frame with six columns:
    'uris',
    'status_code', all should be 2xx or 3xx
    'content-type',
    'if_rdf_content',
    'parsing',
    'undefined',
    :return:
    """

    uri_type = []
    property_type = []

    # only focus on defined URIs, so subset:
    uris_defined = uris_rdf.loc[uris_rdf["whether defined"] == "defined"]

    # Investigate an URI
    for index, row in uris_defined.iterrows():

        uri = row['uris']

        print(str(index) + '. ' + uri + ", " + row['content-type'])

        # get parsing content of the URI
        g = Graph().parse(uri, format=corpus.MapContentTypeToParserFormat[row['content-type']])

        # 'contains' checking
        if (URIRef(uri), RDF.type, URIRef("http://www.w3.org/2002/07/owl#DatatypeProperty")) in g or \
                (URIRef(uri), RDFS.range, RDFS.Literal) in g:
            uri_type.append("property")
            property_type.append('owl_datatype_property')
            continue

        elif (URIRef(uri), RDF.type, URIRef("http://www.w3.org/2002/07/owl#ObjectProperty")) in g:
            uri_type.append("property")
            property_type.append('owl_object_property')
            continue

        elif (URIRef(uri), RDF.type, URIRef("http://www.w3.org/2002/07/owl#InverseFunctionalProperty")) in g \
                or (URIRef(uri), RDF.type, URIRef("http://www.w3.org/2002/07/owl#FunctionalProperty")) in g:
            uri_type.append("property")
            property_type.append('other_property')
            continue

        elif (URIRef(uri), RDF.type, URIRef("http://www.w3.org/2002/07/owl#TransitiveProperty")) in g:
            uri_type.append("property")
            property_type.append('other_property')
            continue

        elif (URIRef(uri), RDF.type, URIRef("http://www.w3.org/2002/07/owl#SymmetricProperty")) in g:
            uri_type.append("property")
            property_type.append('other_property')
            continue

        elif (URIRef(uri), RDF.type, URIRef("http://www.w3.org/2002/07/owl#AnnotationProperty")) in g:
            uri_type.append("property")
            property_type.append('other_property')
            continue

        elif (URIRef(uri), RDF.type, URIRef("http://www.w3.org/2002/07/owl#OntologyProperty")) in g:
            uri_type.append("property")
            property_type.append('other_property')
            continue

        elif (URIRef(uri), RDF.type, URIRef("http://www.w3.org/2002/07/owl#DeprecatedProperty")) in g:
            uri_type.append("property")
            property_type.append('other_property')
            continue

        elif (URIRef(uri), RDF.type, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#Property")) in g:
            uri_type.append("property")
            property_type.append('other_property')
            continue

        elif (URIRef(uri), RDF.type, URIRef("http://www.w3.org/2000/01/rdf-schema#Class")) in g or \
                (URIRef(uri), RDF.type, URIRef("http://www.w3.org/2002/07/owl#Class")) in g:
            uri_type.append("class")
            property_type.append('not applicable')
            continue
        else:
            uri_type.append("unknown")
            property_type.append('not applicable')

    # add URI type to a new column
    uris_defined.loc[:, 'uri type'] = uri_type
    uris_defined.loc[:, 'property type'] = property_type

    return uris_defined
