#!/usr/bin/env python3
import os
import time
import datetime
import pandas as pd
from rdflib.term import URIRef, BNode, Literal

# Import metrics
from metrics.coverage import count_rdf_component
from metrics.resolvability import get_http_status_code_and_content_type
from metrics.parsability import assess_parsable
from metrics.classify import get_uri_type
from metrics.consistency import run_consistency_assessment

# Import basic functions
from functions.load_resource import parse_data_local_or_remote as load_resource
from functions.inspect_items import view_graph
from functions.generate_report import build_graph
from functions.create_directory import create_directory
from identify_errors import quantitative_analysis

# Import human-configurable
from config import WhichResource, ListOfLabelsForRareDiseaseResources


def run_assessment(label, assess_resolvable=True, test_parsable=True, re_classify=True, assess_consistency=True):
    """
    Decide whether run-assess a metric (True) or load existing results (False)
    :param label: string.
    :param assess_resolvable: Boolean. If true, this process will be run again. Else, load existing results.
    :param test_parsable: Boolean. If true, this process will be run again. Else, load existing results.
    :param re_classify: Boolean. If true, this process will be run again. Else, load existing results.
    :param assess_consistency: Boolean. If true, this process will be run again. Else, load existing results.
    :return:
    """

    # Calculate Time Cost
    print("Start quality assessment on the resource: {}: ".format(label))

    # create a directory for storing results
    create_directory("output/{}".format(label))

    # Load resource with path based on a label
    g = load_resource(WhichResource[label])

    # Preview part of triples
    view_number_of_triples = 5
    print("View the first " + str(view_number_of_triples) + " triples: ")
    view_graph(g, view_number_of_triples)

    # get a list of unique URIs in the test resource
    uris = count_rdf_component(rdf_graph=g, rdf_term=URIRef)
    print("\nThis RDF resource has {} unique URIs. ".format(len(uris)))

    path_dic = {
        'resolvable': 'output/{}/uri-resolvable-{}.csv'.format(label, label),
        'parsable': 'output/{}/uri-parsable-{}.csv'.format(label, label),
        'consistent': 'output/{}/uri-consistent-{}.csv'.format(label, label),
        'intermediate': 'output/{}/uri-intermediate-{}.csv'.format(label, label),
        'report': 'output/{}/report-{}.ttl'.format(label, label),
    }

    print("\nStep I. Test Resolvability of all URIs. ")
    if assess_resolvable:
        # run resolvable test
        df_uris = get_http_status_code_and_content_type(uris)

        # export results
        print("Resolvability results stored.")
        df_uris.to_csv(path_dic['resolvable'])

    print("Resolvability results loaded.")
    df_uris = pd.read_csv(path_dic['resolvable'], index_col=0)

    print("\nStep II. Test Parsability of resolvable URIs.")

    # run Parsable test and export as csv
    if test_parsable:
        df_uris_parsable = assess_parsable(df_uris)
        print("Parsability results stored.")
        df_uris_parsable.to_csv(path_dic['parsable'])

    print("Parsability results loaded.")
    df_uris_parsable = pd.read_csv(path_dic['parsable'], index_col=0)

    print("\nStep III. Classify Parsable URIs.")
    if re_classify:
    # classify those parsable URIs
        uris_defined = get_uri_type(df_uris_parsable)
        print("Classification finishes. "
              "URIs are categorized into 'class', 'property', and 'unknown'. ")

        print("\nStep IV. Test Consistency - Undefined URIs ")
        print("Intermediate results stored.")
        uris_defined.to_csv(path_dic['intermediate'])

    print("Intermediate results loaded.")
    uris_defined = pd.read_csv(path_dic['intermediate'], index_col=0)

    # Run consistency
    print("\nStep V. Test Consistency ")
    if assess_consistency:
        uris_consistency_check = run_consistency_assessment(graph=g, df_uris_defined=uris_defined)
        print("Consistency results stored.")
        uris_consistency_check.to_csv(path_dic['consistent'])

    print("Consistency results loaded.")
    uris_consistency_check = pd.read_csv(path_dic['consistent'], index_col=0)

    # extract errors from df
    print("\nStep VI: Get errors and calculate statistics from stored results.")
    assessment_result = quantitative_analysis(label)

    print("Step VII: Generate assessment report. ")
    # get some baseline numbers
    num_of_uris = len(uris)
    num_of_classes = len(uris_consistency_check.loc[uris_consistency_check['uri type'] == 'class'])
    num_of_properties = len(uris_consistency_check.loc[uris_consistency_check['uri type'] == 'property'])

    report_graph = build_graph(resource_uri=WhichResource[label],
                               report_label=label,
                               assessment_result=assessment_result,
                               num_of_uris=num_of_uris,
                               num_of_classes=num_of_classes,
                               num_of_properties=num_of_properties)

    report_graph.serialize(destination=path_dic['report'])

    # # Remove unneeded files
    # if os.path.exists(path_dic['intermediate']):
    #     os.remove(path_dic['intermediate'])
    # else:
    #     print("The file does not exist")


def execution():

    # decide whether run-assess a metric (True) or load existing results (False)
    whether_re_run = {'assess_resolvable': False,
                      'test_parsable': False,
                      're_classify': False,
                      'assess_consistency': False}

    for label in ListOfLabelsForRareDiseaseResources[14:]:
        print(label)
        # set start time
        label = 'test'
        start_time = time.time()

        run_assessment(label, **whether_re_run)

        # set end time
        end_time = time.time()

        # calculate running time for each resource
        time_cost = int(end_time - start_time)
        print('Time Cost (hh:mm:ss) is: \n {}'.format(str(datetime.timedelta(seconds=time_cost))))


if __name__ == '__main__':

    execution()
