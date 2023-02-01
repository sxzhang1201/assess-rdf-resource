from rdflib.graph import Graph
from rdflib.term import URIRef, Literal
from rdflib.namespace import RDF, RDFS, DCTERMS, DCAT
from rdflib import Namespace


def populate_report_with_results(report_graph,
                                 measure_uri_ref,
                                 bad_uris_list,
                                 num_of_uris,
                                 resource_uri_ref,
                                 metric_uri_ref):

    DQV = Namespace("http://www.w3.org/ns/dqv#")

    report_graph.add((
        resource_uri_ref,
        DQV.hasQualityMeasurement,
        measure_uri_ref))

    report_graph.add((
        measure_uri_ref,
        RDF.type,
        DQV.QualityMeasurement))

    report_graph.add((
        measure_uri_ref,
        DQV.computedOn,
        resource_uri_ref))

    report_graph.add((
        measure_uri_ref,
        DQV.isMeasurementOf,
        metric_uri_ref))

    # add percentage
    report_graph.add((
        measure_uri_ref,
        DQV.value,
        Literal("{}/{}".format(len(bad_uris_list), num_of_uris))))

    for bad_uri in bad_uris_list:
        report_graph.add((
            measure_uri_ref,
            DCTERMS.relation,
            URIRef(bad_uri)))


def build_graph(resource_uri, report_label, assessment_result, num_of_uris=0, num_of_classes=0, num_of_properties=0):
    # specify namespaces
    resource_report = Namespace("http://example.org/{}-report#".format(report_label))

    FQM = Namespace("http://purl.org/fqm#")

    report_graph = Graph()

    # enable prefixes, otherwise ns1 ns2 ...
    # report_graph.bind("ar", "http://example.org/assessment-report-{}#".format(report_label))
    report_graph.bind("dqv", "http://www.w3.org/ns/dqv#")
    report_graph.bind("fqm", "http://purl.org/fqm#")

    resource_uri_ref = URIRef(resource_uri)

    # Part 1: Describe resource
    # <resource uri>    rdf:type    dcat:Dataset
    report_graph.add((resource_uri_ref, RDF.type, DCAT.Resource))
    # <resource uri>    dct:title    'title'
    report_graph.add((resource_uri_ref, DCTERMS.title, Literal(report_label)))

    # Part 2: Link resource to measurements
    # Load results
    result_resolvability = assessment_result['non_resolvable_uris']
    result_parsability = assessment_result['non_parsable_uris']
    undefined_uris = assessment_result['undefined_uris']
    misplaced_class = assessment_result['misplaced_class']
    misplaced_property = assessment_result['misplaced_property']
    misused_owl_datatype_property = assessment_result['misused_owl_datatype']
    misused_owl_object_property = assessment_result['misused_owl_object']

    # Part 3: Describe each measurement
    # <resource uri>    dqv:hasQualityMeasurement   resource.resolvabilityMeasurement
    # Measurement 1 - Resolvability metric
    if len(result_resolvability) != 0:
        populate_report_with_results(report_graph=report_graph,
                                     measure_uri_ref=resource_report.resolvabilityMeasurement,
                                     bad_uris_list=result_resolvability,
                                     num_of_uris=num_of_uris,
                                     resource_uri_ref=resource_uri_ref,
                                     metric_uri_ref=FQM.uriNonResolvableMetric)

    if len(result_parsability) != 0:
        populate_report_with_results(report_graph=report_graph,
                                     measure_uri_ref=resource_report.parsabilityMeasurement,
                                     bad_uris_list=result_parsability,
                                     num_of_uris=num_of_uris,
                                     resource_uri_ref=resource_uri_ref,
                                     metric_uri_ref=FQM.uriNonParsableMetric)

    if len(undefined_uris) != 0:
        populate_report_with_results(report_graph=report_graph,
                                     measure_uri_ref=resource_report.undefinedURIsMeasurement,
                                     bad_uris_list=undefined_uris,
                                     num_of_uris=num_of_uris,
                                     resource_uri_ref=resource_uri_ref,
                                     metric_uri_ref=FQM.uriUndefinedMetric)

    if len(misplaced_class) != 0:
        populate_report_with_results(report_graph=report_graph,
                                     measure_uri_ref=resource_report.misplacedClassesMeasurement,
                                     bad_uris_list=misplaced_class,
                                     num_of_uris=num_of_classes,
                                     resource_uri_ref=resource_uri_ref,
                                     metric_uri_ref=FQM.misplacedClassesOrPropertiesMetric)

    if len(misplaced_property) != 0:
        populate_report_with_results(report_graph=report_graph,
                                     measure_uri_ref=resource_report.misplacedPropertiesMeasurement,
                                     bad_uris_list=misplaced_property,
                                     num_of_uris=num_of_properties,
                                     resource_uri_ref=resource_uri_ref,
                                     metric_uri_ref=FQM.misplacedClassesOrPropertiesMetric)

    if len(misused_owl_datatype_property) != 0:
        populate_report_with_results(report_graph=report_graph,
                                     measure_uri_ref=resource_report.misusedOwlDatatypePropertyMeasurement,
                                     bad_uris_list=misused_owl_datatype_property,
                                     num_of_uris=num_of_properties,
                                     resource_uri_ref=resource_uri_ref,
                                     metric_uri_ref=FQM.misusedOwlDatatypeOrObjectPropertiesMetric)

    if len(misused_owl_object_property) != 0:
        populate_report_with_results(report_graph=report_graph,
                                     measure_uri_ref=resource_report.misusedOwlObjectPropertyMeasurement,
                                     bad_uris_list=misused_owl_object_property,
                                     num_of_uris=num_of_properties,
                                     resource_uri_ref=resource_uri_ref,
                                     metric_uri_ref=FQM.misusedOwlDatatypeOrObjectPropertiesMetric)

    print(report_graph.serialize())

    return report_graph

# :measurement1
#     a dqv:QualityMeasurement ;
#     dqv:computedOn :myDatasetDistribution ;
#     dqv:isMeasurementOf :downloadURLAvailabilityMetric ;
#     dqv:value "true"^^xsd:boolean
#     .
#
# :measurement2
#     a dqv:QualityMeasurement ;
#     dqv:computedOn :myDatasetDistribution ;
#     dqv:isMeasurementOf :csvCompletenessMetric ;
#     dqv:value "0.5"^^xsd:double
#     .
#
# #definition of dimensions and metrics
# :availability
#     a dqv:Dimension ;
#     skos:prefLabel "Availability"@en ;
#     skos:definition "Availability of a dataset is the extent to which data (or some
#     portion of it) is present, obtainable and ready for use."@en ;
#     dqv:inCategory :accessibility


def generate_report_graph():
    resource_uri_ref = URIRef('http://example.org/test.ttl')
    report_label = 'test'
    # assessment_result =

    # report_graph = build_graph(resource_uri=resource_uri_ref,
    #                            report_label=report_label,
    #                            assessment_result=)

    # print(report_graph.serialize())


if __name__ == '__main__':
    generate_report_graph()
