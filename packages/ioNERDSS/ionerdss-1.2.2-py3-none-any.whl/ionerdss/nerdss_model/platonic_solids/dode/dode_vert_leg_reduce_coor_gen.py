from .dode_vert_COM_leg_gen import dode_vert_COM_leg_gen
from .dode_vert_leg_reduce import dode_vert_leg_reduce

def dode_vert_leg_reduce_coor_gen(radius: float, sigma: float):
    """
    Generates reduced center of mass (COM) and leg vectors for a dodecahedron vertex based on radius and sigma values.

    This function generates a list of reduced center of mass (COM) and leg vectors for a dodecahedron vertex based on the
    provided radius and sigma values. The reduced COM and leg vectors are obtained by calling the dode_vert_COM_leg_gen
    function to generate the original COM and leg vectors, and then passing them to the dode_vert_leg_reduce function to
    reduce their lengths. The reduced COM and leg vectors are stored in a list and returned.

    Args:
        radius (float): The radius of the dodecahedron.
        sigma (float): The sigma value for the dodecahedron vertex.

    Returns:
        list: A list of lists, where each inner list contains the reduced center of mass (COM) and leg vectors for a
        dodecahedron vertex.
    """

    COM_leg_list = dode_vert_COM_leg_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 3:
            temp_list.append(dode_vert_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


