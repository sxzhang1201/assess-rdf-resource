#!/usr/bin/env python3

import time
from rdflib.term import URIRef

# Import metrics
from metrics.coverage import count_rdf_component as count_uri
from metrics.resolvability import get_http_status_code as assess_resolvability
from metrics.parsability import assess_parsable
from metrics.classify import extract_type as classify_uri
from metrics.consistency import run_consistency as assess_consistency

# Import basic functions
from functions.load_resource import parse_data_local_or_remote as load_resource
from functions.assessment_report import AssessReport
from functions.save_or_load_report import save_object
from functions.inspect_items import view_graph

# Import human-configurable
from config import WhichResource, WhichReport, LABEL

# Calculate Time Cost
print("Start assessment!")
start_time = time.time()

# Load data
path = WhichResource[LABEL]
g = load_resource(path)

# Quick view of first {10} triples
view_graph(g, 10)

# Run coverage and get basic characteristics
uri_list = count_uri(g=g, rdf_component_type=URIRef)
print("0. There are {} URIs in the test RDF graph".format(len(uri_list)))

print("1. Test Resolvability ")
# Run resolvable test
res_uri_list, non_res_uri_list, resolvable_uris_with_content_type = assess_resolvability(uri_list)

print("2. Test Parsability ")
# Run Parsable test
res_uri_rdf, res_uri_not_rdf, error1_rdf_no_triple, error2_uri_undefined, parsable_uri = \
    assess_parsable(resolvable_uris_with_content_type)

print("2.5 Classify URIs ")
# Run pre-consistency - classify URIs
class_list, property_list, owl_datatype_property, owl_object_property, other_property_list, others_list = \
    classify_uri(parsable_uri)

# Run consistency
print("3. Test Consistency")
misplaced_class_list, misplaced_property_list, misused_datatype_property_list, misused_object_property_list = \
    assess_consistency(g=g, class_list=class_list,
                       property_list=property_list,
                       datatype_property_list=owl_datatype_property,
                       object_property_list=owl_object_property)

print("4. Generate Report")
# Populate reports
r = AssessReport()

# Populate basics
r.add_uri_list(uri_list)
r.add_class_list(class_list)
r.add_property_list(property_list)
r.add_owl_datatype_property(owl_datatype_property)
r.add_owl_object_property(owl_object_property)
r.add_other_property_list(other_property_list)
r.add_others_list(others_list)

r.add_misplaced_class(misplaced_class_list)
r.add_misplaced_property(misplaced_property_list)
r.add_misused_owl_datatype_property(misused_datatype_property_list)
r.add_misused_owl_object_property(misused_object_property_list)

# Populate Resolvability test result
r.add_non_res_uri(non_res_uri_list)

# Populate Parsability test result
r.add_parsability_errors(error1_rdf_no_triple)

# Populate Consistency test result
r.add_undefined_uri(error2_uri_undefined)

# Save Report
save_object(obj=r, filename=WhichReport[LABEL])

# Calculate affected triples of non-resolvable URIs
non_res_rate = r.resolvability_statistics()
print('The proportion of affected triples is {}.'.format(non_res_rate))

# End Time
print("\nThe Processing Time is {}min".format(
    format((time.time() - start_time) / 60, ".2f")))

