import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd


from corpus import Headers


def get_http_status_code_and_content_type(uris):
    """

    :param uris: a list of strings, each as a URI.
    :return: a pandas data frame with two columns: 'uris' and 'status_code'.
    """
    # get a list of status code
    # r = [*map(lambda x: str(requests.get(x, headers=Headers).status_code), uris)]

    code_list = []
    type_list = []

    count = 1

    for uri in uris:
        print("Analyzing URIs (" + "{}/{}".format(count, len(uris)) + ') :' + str(uri))

        s = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        s.mount('http://', adapter)
        s.mount('https://', adapter)

        try:
            r = s.get(uri, headers=Headers)
            status_code = str(r.status_code)
            print(status_code)

        except Exception as e:
            print(" - There is exception here: {}".format(e))
            print(e)
            status_code = 'RequestError'

        if str(status_code).startswith('4') or str(status_code).startswith('5') or \
                str(status_code).startswith('RequestError'):
            content_type = 'Not applicable because non-resolvable.'
        else:
            try:
                # status_code = str(r.status_code)
                content_type = r.headers["content-type"].split(";", 1)[0]
            except Exception as error:
                print(" - Resolvable but unable to get content-type for {}. ".format(str(uri)))
                content_type = error

        # get items (i.e., status-code and content-type) to lists
        code_list.append(status_code)
        type_list.append(content_type)

        print(" - Status code is: {}".format(status_code))
        print(" - Content type is: {}".format(content_type))

        count = count + 1

    # put URIs with their status codes into a data frame
    df_uris = pd.DataFrame({'uris': uris,
                            'status_code': code_list,
                            'content-type': type_list})

    return df_uris


def divide_uris_by_resolvability(df_uris):
    """
    Category URIs based on their status code: 2XX and 3XX as resolvable while 4XX and 5XX as non-resolvable
    :param df_uris: a two-column data frame.
                    'uris": a list of URIs as string;
                    'status_code": a list of status code as string;
    :return: two lists, respectively containing URIs with "2XX + 3XX" and "4XX + 5XX".
    """
    uris_status_23 = df_uris[df_uris['status_code'].str.startswith(('2', '3'))]
    uris_status_45 = df_uris[df_uris['status_code'].str.startswith(('4', '5'))]

    return uris_status_23, uris_status_45


def group_uris_by_resolvability(uris):
    """
    A function getting a list of URIs as input and returning two lists of URIs. Besides, a CSV file
    is generated containing all URIs with their status codes.
    :param uris: a list of strings, each as a URI.
    :return: two lists, respectively containing URIs with "2XX + 3XX" and "4XX + 5XX".
    """
    # get a data frame containing all URIs with status-code and content-type
    df_uris = get_http_status_code_and_content_type(uris)

    # divide URIs into two group lists, based on status-code
    uris_status_23, uris_status_45 = divide_uris_by_resolvability(df_uris)

    return uris_status_23, uris_status_45

