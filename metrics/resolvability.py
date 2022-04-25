import requests


def get_http_status_code(list_of_uri):
    """

    :param list_of_uri: list of RDFLib.URIRef objects
    :return: 2 lists and 1 dictionary
    """

    # Define headers for content-negotiation
    headers = {"Accept": "text/turtle, application/x-turtle,"  # Turtle
                         "application/rdf+xml;q=0.9, "          # RDF/XML
                         "application/ld+json;q=0.8, "          # JSON-LD
                         "text/n3;q=0.7"                        # Notion 3
                         "*/*;q=0.1"}                           # Others

    # Initiate 5 lists
    res_uri_list = []

    # here we regard unofficial ones as non-resolvable (discussion?)
    non_res_uri_list = []
    # code_unofficial_list = []

    # Initiate a dictionary
    content_type_for_resolvable_uris = {}

    progress_count = 1

    for single_uri in list_of_uri:

        print(" Getting status code of {} - Progress {}/{}".format(single_uri, progress_count, len(list_of_uri)))

        progress_count = progress_count + 1

        try:
            # Get HTTP Status Code and append URI to corresponding lists
            # Bug fixed: do not use request.head(URI), which is outdated.
            r = requests.get(single_uri, headers=headers)
            status_code = str(r.status_code)

            if status_code.startswith("2"):
                res_uri_list.append(single_uri)
                content_type_for_resolvable_uris[str(single_uri)] = r.headers["content-type"].split(";", 1)[0]
                continue
            if status_code.startswith("3"):
                res_uri_list.append(single_uri)
                content_type_for_resolvable_uris[str(single_uri)] = r.headers["content-type"].split(";", 1)[0]
                continue
            if status_code.startswith("4"):
                non_res_uri_list.append(single_uri)
                print(" This URI is not resolvable with status code: {}".format(status_code))
                continue
            if status_code.startswith("5"):
                non_res_uri_list.append(single_uri)
                print(" This URI is not resolvable with status code: {}".format(status_code))
                continue

            # If HTTP status code is not any of above types, add it to "others"
            non_res_uri_list.append(single_uri)

        except Exception as e:
            non_res_uri_list.append(single_uri)
            print(e)

    # Consolidate all together for output

    return res_uri_list, non_res_uri_list, content_type_for_resolvable_uris


