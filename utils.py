"""
Maybe needed in the future for dynamic inital value selection:
"""


def bit_to_number(n_qubits):
    bit_string = ""
    for i in range(n_qubits):
        bit_string += "1"
    return int(bit_string, 2)


def number_to_bit(number):
    return f"{number:b}"


"""
Disclaimer: This function is taken by the Google Tutorial about Random Walks
"""


def get_values_from_dict(final):

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
