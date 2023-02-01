import os.path
from rdflib.graph import Graph
import requests
import corpus


def parse_data_local_or_remote(data_path):

    # initiate a graph
    g = Graph()

    if 'http' in str(data_path):
        print("Loading resource from " + str(data_path))
        r = requests.get(data_path, headers=corpus.Headers)
        content_type_this_uri = r.headers["content-type"].split(";", 1)[0]

        print("The Content-type of this resource is " + str(content_type_this_uri))
        parse_format = corpus.MapContentTypeToParserFormat[content_type_this_uri]
        try:
            g.parse(data_path, format=parse_format)
        except:
            raise Exception(
                print("The resource from " + str(data_path) + " cannot be parsed. Please check. ")
            )

    else:
        print("Parse resource from local path: " + str(data_path))

        # Check if the resource exists, otherwise it returns error
        if os.path.exists(data_path):
            try:
                # Note that local resource we cannot specify parse type
                g.parse(data_path)
            except:
                raise Exception(
                    "The local resource from {} cannot be parsed. Please check. ".format(data_path))
        else:
            raise OSError("The resource at {} is not found. ".format(data_path))

    if len(g) == 0:
        print("The resource has no triples loaded. Please check! ")
    else:
        print("The resource is successfully loaded. \n")

    return g


# if __name__ == '__main__':
#     path_list = ['https://ejp-rd-dev1.vm.cesnet.cz/fdps/orphanet-catalog-fdp/?format=ttl',
#                  '../resources/rd-resources/ordo-catalog-fdp/A multicenter registry for nasopharyngeal cancer in children.ttl']
#
#     for path in path_list:
#
#         g = parse_data_local_or_remote(path)
#
#         print("Graph has those triples: " + str(len(g)))
