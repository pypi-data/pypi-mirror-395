from typing import Dict


def sort_dict_by_list(
        input_dict: Dict[str, any],
        order_list: list[str]
) -> Dict[str, any]:
    """
    Sorts a dictionary based on a custom order specified in a list.

    This function takes an input dictionary and a list of keys that represent the desired order
    of keys in the resulting dictionary. It returns a new dictionary with the keys from the input
    dictionary sorted according to the order specified in the 'order_list' list.

    Args:
        input_dict (dict): The input dictionary to be sorted.
        order_list (list): A list of keys specifying the desired order of keys.

    Returns:
        dict: A new dictionary with keys sorted based on the 'order_list' list.

    Examples:
        >>> unsorted_dict = {'b': 2, 'a': 1, 'c': 3}
        >>> order_list = ['a', 'b', 'c']
        >>> sort_dict_by_list(unsorted_dict, order_list)
        {'a': 1, 'b': 2, 'c': 3}

        >>> unsorted_dict = {'apple': 3, 'banana': 1, 'cherry': 2}
        >>> order_list = ['banana', 'cherry', 'apple']
        >>> sort_dict_by_list(unsorted_dict, order_list)
        {'banana': 1, 'cherry': 2, 'apple': 3}

    Raises:
        ValueError: If 'order_list' contains duplicate keys or keys not present in 'input_dict'.
    """
    # Check for duplicate keys or keys not present in the input dictionary
    if len(set(order_list)) != len(order_list) or not all(key in input_dict for key in order_list):
        raise ValueError("The 'order_list' list should contain unique keys present in the input dictionary.")

    # Create a sorted dictionary based on the 'order_list' list
    sorted_dict = {key: input_dict[key] for key in order_list}

    return sorted_dict
