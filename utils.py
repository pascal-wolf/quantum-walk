def get_values_from_dict(final):
    """
    Disclaimer: This function is taken by the Google Tutorial about Random Walks

    Extracts keys and values from a dictionary and returns them as sorted lists.

    This function takes a dictionary as input, extracts the keys and values, and sorts them based on the keys.
    The sorted keys and corresponding values are returned as two separate lists. The function is originally taken
    from the Google Tutorial about Random Walks.

    Args:
        final (dict): The input dictionary from which keys and values are to be extracted.

    Returns:
        tuple: Two lists, the first containing the sorted keys and the second containing the corresponding values.
    """

    x_arr = list(final.keys())
    y_arr = [dict(final)[j] for j in dict(final).keys()]

    x_arr_final = []
    y_arr_final = []

    while len(x_arr) > 0:

        x_arr_final.append(min(x_arr))
        y_arr_final.append(y_arr[x_arr.index(min(x_arr))])
        holder = x_arr.index(min(x_arr))
        del x_arr[holder]
        del y_arr[holder]
    return x_arr_final, y_arr_final
