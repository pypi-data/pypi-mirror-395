from .octa_vert_COM_leg_gen import octa_vert_COM_leg_gen
from .octa_vert_leg_reduce import octa_vert_leg_reduce

def octa_vert_leg_reduce_coor_gen(radius: float, sigma: float):
    """Generates a list of center of mass (COM) and reduced leg vectors for an octagonal vertex based on a given radius
    and sigma value.

    This function uses the `octa_vert_COM_leg_gen` function to generate a list of COM and leg vectors for an octagonal
    vertex with the given radius. Then, it applies the `octa_vert_leg_reduce` function to reduce the length of the leg
    vectors based on the given sigma value, and stores the reduced COM and leg vectors in a list.

    Args:
        radius (float): The radius of the octagonal vertex.
        sigma (float): The sigma value used for reducing the length of the leg vectors.

    Returns:
        list: A list of lists, where each sublist contains the reduced COM and leg vectors for an octagonal vertex.
        The structure of the list is as follows:
        [
            [COM1, leg_red1_1, leg_red1_2, leg_red1_3, leg_red1_4],
            [COM2, leg_red2_1, leg_red2_2, leg_red2_3, leg_red2_4],
            ...
        ]

    Example:
        radius = 1.0
        sigma = 0.5
        result = octa_vert_leg_reduce_coor_gen(radius, sigma)
        print(result)
    """
    COM_leg_list = octa_vert_COM_leg_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 4:
            temp_list.append(octa_vert_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


