#!/usr/bin/env python3
from rdflib.graph import Graph
from functions.save_or_load_report import load_object
from functions.load_resource import parse_data_local_or_remote as load_resource
from functions.inspect_items import inspect_item_in_list, inspect_item_in_dict
from config import WhichResource, WhichReport, LABEL

print(" Assessing {} ".format(LABEL))

f = open('report/{}.txt'.format(LABEL), "a")

print("# !! Assessment Report of {} !! #".format(LABEL))

print("# 1. Load report labelled by '{}' ".format(LABEL), file=f)
assess_report = load_object(WhichReport[LABEL])
g = load_resource(WhichResource[LABEL])
print("# In the test RDF resource:", file=f)
print("# - There are {} triples".format(len(g)), file=f)
print("# - There are {} URIs".format(len(assess_report.uri_list)), file=f)

print("# 2. Resolvability Report", file=f)
resolvability_errors = assess_report.resolvability_errors
print("# - The following {} URI(s) are not resolvable".format(len(resolvability_errors)), file=f)
inspect_item_in_list(resolvability_errors, f=f)

print("# 3. Parsability Report", file=f)
parsable_error_no_triple = assess_report.parsable_error_no_triple
print("# - The following {} URI(s) are not parsable".format(len(parsable_error_no_triple)), file=f)
inspect_item_in_dict(parsable_error_no_triple, f=f)

print("# 4. Consistency Report", file=f)
consistency_error_undefined = assess_report.consistency_error_undefined
print("# - The following {} URI(s) are not defined".format(len(consistency_error_undefined)), file=f)
inspect_item_in_list(consistency_error_undefined, f=f)

misplaced_class = assess_report.misplaced_class
print("# - The following {} classes are incorrectly used as predicates".format(len(misplaced_class)), file=f)
inspect_item_in_list(misplaced_class, f=f)

misplaced_property = assess_report.misplaced_property
print("# - The following {} properties are incorrectly used as classes".format(len(misplaced_property)), file=f)
inspect_item_in_list(misplaced_property, f=f)

misused_owl_datatype_property = assess_report.misused_owl_datatype_property
print("# - The following {} owl:dataTypeProperty are not correctly used".format(len(misused_owl_datatype_property)), file=f)
inspect_item_in_list(misused_owl_datatype_property, f=f)

misused_owl_object_property = assess_report.misused_owl_object_property
print("# - The following {} owl:objectProperty are not correctly used".format(len(misused_owl_object_property)), file=f)
inspect_item_in_list(misused_owl_object_property, f=f)

print("# 5. To measure the effect of errors on the graph", file=f)
# Resolvable Errors
overall_count, uri_effect_dict = assess_report.measure_effect(resolvability_errors, g)
print("# - These non-resolvable URIs have affected {} triples out of {}".format(overall_count, len(g)), file=f)
rate = overall_count/len(g)
print("# - The percentage is {}".format(rate), file=f)

f.close()
