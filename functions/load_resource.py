import os.path
from rdflib.graph import Graph
import requests
import corpus


def parse_data_local_or_remote(data_path):
    g = Graph()
    if 'http' in str(data_path):
        # print(" Parse Remote Graph!")
        r = requests.get(data_path, headers=corpus.Headers)
        content_type_this_uri = r.headers["content-type"].split(";", 1)[0]
        print(content_type_this_uri)
        parse_format = corpus.MapContentTypeToParserFormat[content_type_this_uri]
        g.parse(data_path, format=parse_format)

    else:
        # print(" Parse Local Graph!")
        # Check 1) if the file exists and 2) if RDF graphs in that file is parsable
        if os.path.exists(data_path):
            try:
                g.parse(data_path)
            except:
                raise Exception(
                    "The file {} cannot be parsed into RDF triples due to syntactical errors. ".format(data_path))
        else:
            raise OSError("The file {} is not found. ".format(data_path))

    return g
