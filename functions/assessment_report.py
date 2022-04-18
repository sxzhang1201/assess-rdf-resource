from rdflib.graph import Graph


class AssessReport:
    """
    For all "uri" in this class, they refers to the rdflib.URIRef() object, not string or n3 format.
    But in dictionary, the URI key are all strings.
    """

    def __init__(self):
        # Coverage
        self.uri_list = []
        self.class_list = []
        self.property_list = []
        self.owl_datatype_property = []
        self.owl_object_property = []
        self.other_property_list = []
        self.others_list = []
        # Resolvability
        self.resolvability_errors = []
        # Parsability
        self.parsable_error_no_triple = {}
        # Consistency
        self.consistency_error_undefined = []
        self.misplaced_class = []
        self.misplaced_property = []
        self.misused_owl_datatype_property = []
        self.misused_owl_object_property = []

    # Functions to populate report
    # Coverage
    def add_uri_list(self, uri_list):
        self.uri_list = uri_list

    def add_class_list(self, class_list):
        self.class_list = class_list

    def add_property_list(self, property_list):
        self.property_list = property_list

    def add_owl_datatype_property(self, owl_datatype_property):
        self.owl_datatype_property = owl_datatype_property

    def add_owl_object_property(self, owl_object_property):
        self.owl_object_property = owl_object_property

    def add_other_property_list(self, other_property_list):
        self.other_property_list = other_property_list

    def add_others_list(self, others_list):
        self.others_list = others_list

    # Resolvability
    def add_non_res_uri(self, non_resolvable_uri_list):
        if len(non_resolvable_uri_list) == 0:
            print("Warning: no non-resolvable URI added")
        self.resolvability_errors = non_resolvable_uri_list

    # Parsability
    def add_parsability_errors(self, non_parsable_uri_dict):
        self.parsable_error_no_triple = non_parsable_uri_dict

    # Consistency
    def add_undefined_uri(self, undefined_uri_list):
        self.consistency_error_undefined = undefined_uri_list

    def add_misplaced_class(self, misplaced_class_list):
        self.misplaced_class = misplaced_class_list

    def add_misplaced_property(self, misplaced_property_list):
        self.misplaced_property = misplaced_property_list

    def add_misused_owl_datatype_property(self, misused_owl_datatype_property):
        self.misplaced_class = misused_owl_datatype_property

    def add_misused_owl_object_property(self, misused_owl_object_property):
        self.misused_owl_object_property = misused_owl_object_property

    # Calculate statistics
    def resolvability_statistics(self):
        non_res_rate = len(self.resolvability_errors)/len(self.uri_list)

        return non_res_rate

    def parsability_statistics(self):
        non_par_rate = len(self.parsable_error_no_triple)/len(self.uri_list)

        return non_par_rate

    # Calculate effect
    def measure_effect(self, error_list, target_graph):
        """

        :param error_list: the list of erroneous URIs to be measured
        :param target_graph: the test graph
        :return: int, overall count of affected triples; dict, [str(uri), int]
        """

        overall_count = 0

        uri_effect_dict = {}

        for bad_uri in error_list:
            temp_graph = Graph()

            # Be aware that one URI may be used correctly and incorrectly in the same dataset
            temp_graph += target_graph.triples((bad_uri, None, None))
            temp_graph += target_graph.triples((None, bad_uri, None))
            temp_graph += target_graph.triples((None, None, bad_uri))

            overall_count = overall_count + len(temp_graph)

            # Get affected triples per URI
            uri_effect_dict[str(bad_uri)] = len(temp_graph)

        return overall_count, uri_effect_dict

