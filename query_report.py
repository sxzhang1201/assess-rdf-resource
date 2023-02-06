from rdflib import Graph
from config import ListOfLabelsForRareDiseaseResources, QUERY1, QUERY2, QUERY3


def load_report(list_of_labels):

    # initiate a graph for loading all reports, to be prepared for querying demo
    graph_all_reports = Graph()

    # iterate each resource by using labels (see config.ListOfLabelsForRareDiseaseResources)
    for label in list_of_labels:
        # get path of a report
        report_path = 'output/{}/report-{}.ttl'.format(label, label)

        # load report
        temp_graph = Graph().parse(report_path)
        print('length of {} report is: '.format(label) + str(len(temp_graph)))

        # append report
        graph_all_reports += temp_graph

    print("\nlength of all report is " + str(len(graph_all_reports)))

    return graph_all_reports


def run_query1(query_graph):

    # Execute query based on the SPARQL as defined in QUERY1
    query1_result = query_graph.query(QUERY1)

    for row in query1_result:
        print(row.rname, row.value)


def run_query2(query_graph):

    # Execute query based on the SPARQL as defined in QUERY2
    query2_result = query_graph.query(QUERY2)
    for row in query2_result:
        print(row.resource, row.undefined_uris)


def run_query3(query_graph):

    # Execute query based on the SPARQL as defined in QUERY2
    query3_result = query_graph.query(QUERY3)

    for row in query3_result:
        print(row.measure, row.metric, row.definition)


def run_query():
    graph_all_reports = load_report(ListOfLabelsForRareDiseaseResources)
    print("\nThe result of 1st query use case: ")
    run_query1(graph_all_reports)

    print("\nThe result of 2nd query use case: ")
    run_query2(graph_all_reports)

    print("\nThe result of 3rd query use case: ")
    vocab_graph = Graph().parse('metrics/fqm.ttl')

    graph_all_reports += vocab_graph

    run_query3(graph_all_reports)


if __name__ == '__main__':
    run_query()

