from functions.save_or_load_report import load_object
from functions.load_resource import parse_data_local_or_remote as load_resource
from functions.inspect_items import inspect_item_in_list, inspect_item_in_dict
from config import WhichResource, WhichReport, LABEL

print("1. Load report")
assess_report = load_object(WhichReport[LABEL])

print("2. Resolvability Report")
resolvability_errors = assess_report.resolvability_errors
print(" The following {} URIs are not resolvable".format(len(resolvability_errors)))
inspect_item_in_list(resolvability_errors)

print("3. Parsability Report")
parsable_error_no_triple = assess_report.parsable_error_no_triple
print( "The following {} URIs are not parsable".format(len(parsable_error_no_triple)))
inspect_item_in_dict(parsable_error_no_triple)

print("4. Consistency Report")
consistency_error_undefined = assess_report.consistency_error_undefined
print(" The following {} URIs are not defined".format(len(consistency_error_undefined)))
inspect_item_in_list(consistency_error_undefined)

misplaced_class = assess_report.misplaced_class
print(" The following {} classes are incorrectly used as predicates".format(len(misplaced_class)))
inspect_item_in_list(misplaced_class)

misplaced_property = assess_report.misplaced_property
print(" The following {} properties are incorrectly used as classes".format(len(misplaced_property)))
inspect_item_in_list(misplaced_property)

misused_owl_datatype_property = assess_report.misused_owl_datatype_property
print(" The following {} owl:dataTypeProperty are not correctly used".format(len(misused_owl_datatype_property)))
inspect_item_in_list(misused_owl_datatype_property)

misused_owl_object_property = assess_report.misused_owl_object_property
print(" The following {} owl:objectProperty are not correctly used".format(len(misused_owl_object_property)))
inspect_item_in_list(misused_owl_object_property)

print("5. To measure effect of errors")
g = load_resource(WhichResource[LABEL])
# Resolvable Errors
overall_count, uri_effect_dict = assess_report.measure_effect(resolvability_errors, g)
print(" These non-resolvable URIs have affected {} triples out of {}".format(overall_count, len(g)))
rate = overall_count/len(g)
print(" The percentage is {}".format(rate))



