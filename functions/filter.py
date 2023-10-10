
def filtering(list_of_items, filter_pattern):
    """
    Filter items by removing those containing given pattern.
    So far, only start_with operation is provided.
    :param list_of_items: list of items
    :param filter_pattern: str,
    :return: a list of filtered items that DO NOT contain filter_pattern
    """

    filtered_list = [item for item in list_of_items if not str(item).startswith(filter_pattern)]

    return filtered_list

