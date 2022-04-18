
def count_rdf_component(g, rdf_component_type):
    """
    Get counts of RDF components in the input graph.
    :param rdf_graph: RdfLib Graph object;
    :param rdf_component_type: RdfLib.term: URIRef, Literal, or BNode
    :return: list, including all components of specified type in this graph.
    """

    count_list = []

    for s, p, o in g:
        if isinstance(s, rdf_component_type):
            count_list.append(s)
        if isinstance(p, rdf_component_type):
            count_list.append(p)
        if isinstance(o, rdf_component_type):
            count_list.append(o)

    count_list = list(set(count_list))

    return count_list

