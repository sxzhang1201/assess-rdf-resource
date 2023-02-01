def count_rdf_component(rdf_graph, rdf_term):
    """
    Get counts of RDF components in the input graph: IRI, Literal, and Bland nodes
    :param rdf_graph: RdfLib Graph object;
    :param rdf_term: RdfLib.term: URIRef, Literal, or BNode
    :return: list, including all components of specified type in this graph.
    """

    count_list = []

    for s, p, o in rdf_graph:
        if isinstance(s, rdf_term):
            count_list.append(s)
        if isinstance(p, rdf_term):
            count_list.append(p)
        if isinstance(o, rdf_term):
            count_list.append(o)

    # Remove duplicates by set()
    count_list = list(set(count_list))

    return count_list

