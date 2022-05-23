def inspect_item_in_list(list_of_items, f):

    for item in list_of_items:
        print(item, file=f)


def inspect_item_in_dict(dict_of_items, f):

    for key, value in dict_of_items.items():
        # print(key, value)
        print(key, file=f)


def view_graph(graph, limit_triple_num):

    # Initiate a count
    triple_num = 0

    # View triples
    for s, p, o in graph:
        print(s, p, o)
        triple_num += 1

        if triple_num == limit_triple_num:
            break
