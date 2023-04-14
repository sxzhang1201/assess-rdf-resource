#!/usr/bin/env python3
import os
import time
import datetime
import pandas as pd
import pickle
import os
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
from functions.split_list import split
from quantitative_analysis import quantitative_analysis, calculate_affected_triples_all

# Import human-configurable
from config import WhichResource, ListOfLabelsForRareDiseaseResources, ListOfLABEL


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

    print("Start quality assessment on the resource: {}: ".format(label))

    # Create a directory for storing results
    create_directory("output/{}".format(label))

    # If target RDF graph exists in pickle, load it.
    if os.path.isfile('pickle/{}_graph.pickle'.format(label)):
        print("The RDF graph already exists in Pickle format, thus loading the graph. ")
        with open('pickle/{}_graph.pickle'.format(label), 'rb') as f:
            g = pickle.load(f)

    # Else, parse it based on the path provided
    else:
        # Load resource with path based on a label
        print("Parsing RDF graph from the given path, then storing it into Pickle file. ")
        g = load_resource(WhichResource[label])

        # Store the RDF graph as a pickle file
        with open('pickle/{}_graph.pickle'.format(label), 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(g, f, pickle.HIGHEST_PROTOCOL)

    # Preview part of triples (here we set 10)
    view_number_of_triples = 10
    print("View the first " + str(view_number_of_triples) + " triples: ")
    view_graph(g, view_number_of_triples)

    # Get a list of unique URIs in the test resource
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
        # Set chunks for a large list (so far 500)
        if len(uris) > 500:
            split_uris = list(split(list_a=uris, chunk_size=500))

            for i in range(len(split_uris)):
                # run resolvable test
                df_uris = get_http_status_code_and_content_type(split_uris[i])

                # Only add header for the first iteration
                if i == 0:
                    df_uris.to_csv(path_dic['resolvable'], mode='a', header=True)

                df_uris.to_csv(path_dic['resolvable'], mode='a', header=False)

        else:
            # Run resolvable test
            df_uris = get_http_status_code_and_content_type(uris)

            # Export results
            print("Resolvability results stored.")
            df_uris.to_csv(path_dic['resolvable'])

    print("Resolvability results loaded.")
    df_uris = pd.read_csv(path_dic['resolvable'], index_col=0)

    # Remove duplicates
    df_uris.drop_duplicates(inplace=True)

    print("\nStep II. Test Parsability of resolvable URIs.")

    # Run Parsable test and export as csv
    if test_parsable:
        df_uris_parsable = assess_parsable(df_uris)
        print("Parsability results stored.")
        df_uris_parsable.to_csv(path_dic['parsable'])

    print("Parsability results loaded.")
    df_uris_parsable = pd.read_csv(path_dic['parsable'], index_col=0)

    print("\nStep III. Classify Parsable URIs.")
    if re_classify:
        # To classify the parsable URIs
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

    # Now having obtained all the errors in different lists, it is time to start analyzing them.
    print("\nStep VI: Get errors and calculate statistics from stored results.")
    assessment_result = quantitative_analysis(label)

    print("Step VII: Generate assessment report. ")
    # Get some baseline numbers
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

    return assessment_result


def execution():
    # decide whether run-assess a metric (True) or load existing results (False)
    whether_re_run = {'assess_resolvable': True,
                      'test_parsable': True,
                      're_classify': True,
                      'assess_consistency': True}

    coat_non_resolvable_dict = {}
    coat_undefined_dict = {}

    for label in ListOfLABEL:
        print(label)
        # calculate time cost: set start time first
        start_time = time.time()

        # run assessment
        assessment_result = run_assessment(label, **whether_re_run)

        with open('pickle/{}_graph.pickle'.format(label), 'rb') as f:
            g = pickle.load(f)

        # get affected triples (optional)
        # for non-resolvable URIs
        result_resolvability = assessment_result['non_resolvable_uris']
        coat_non_resolvability = calculate_affected_triples_all(list_of_bad_uris=result_resolvability,
                                                                target_graph=g)

        # get count of affected triples (coat) due to non-resolvable URIs
        coat_non_resolvable_text = "{}/{}".format(coat_non_resolvability, len(g)) + \
                                   " (" + f"{coat_non_resolvability / len(g):.1%}" + ")"
        coat_non_resolvable_dict[label] = coat_non_resolvable_text

        # for undefined URIs
        undefined_uris = assessment_result['undefined_uris']
        coat_undefined = calculate_affected_triples_all(list_of_bad_uris=undefined_uris,
                                                        target_graph=g)

        coat_undefined_text = "{}/{}".format(coat_undefined,
                                             len(g)) + " (" + f"{coat_undefined / len(g):.1%}" + ")"
        coat_undefined_dict[label] = coat_undefined_text

        # set end time
        end_time = time.time()

        # calculate running time for each resource
        time_cost = int(end_time - start_time)
        print('Time Cost (hh:mm:ss) is: \n {}'.format(str(datetime.timedelta(seconds=time_cost))))

    # Here only print two errors, more can be looked up in the RDF report (.ttl)
    print("The Count of Affected Triples due to non-resolvable URIs: ")
    print(coat_non_resolvable_dict)

    print("The Count of Affected Triples due to undefined URIs: ")
    print(coat_undefined_dict)


if __name__ == '__main__':
    execution()
