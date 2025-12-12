from .icos_vert_COM_leg_gen import icos_vert_COM_leg_gen
from .icos_vert_leg_reduce import icos_vert_leg_reduce

def icos_vert_leg_reduce_coor_gen(radius: float, sigma: float):
    """Generate reduced leg coordinates for an icosahedron based on the center of mass (COM) and sigma.

    The function generates a list of reduced leg coordinates for an icosahedron based on the given radius, sigma value,
    and the center of mass (COM) and leg vectors calculated using the icos_vert_COM_leg_gen function. The leg coordinates
    are reduced using the icos_vert_leg_reduce function, and the resulting coordinates are returned in a list.

    Args:
        radius (float): The radius of the icosahedron.
        sigma (float): The sigma value for reducing the length of the leg vectors.

    Returns:
        list: A list of reduced leg coordinates for the icosahedron, containing lists of coordinates for each leg,
        rounded to 8 decimal places.
    """
    COM_leg_list = icos_vert_COM_leg_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 5:
            temp_list.append(icos_vert_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


