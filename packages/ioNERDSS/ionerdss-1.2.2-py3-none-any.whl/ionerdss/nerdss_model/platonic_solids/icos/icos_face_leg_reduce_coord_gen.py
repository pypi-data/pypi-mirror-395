from ..gen_platonic.COM_leg_list_gen import COM_leg_list_gen
from .icos_face_leg_reduce import icos_face_leg_reduce

def icos_face_leg_reduce_coord_gen(radius: float, sigma: float):
    """Reduces the length of a leg of an icosahedron face.

    Args:
        COM (float): Center of Mass (COM) coordinate.
        leg (float): Leg coordinate.
        sigma (float): Sigma value for leg reduction.

    Returns:
        list: A list of reduced leg coordinates.

    Example:
        >>> icos_face_leg_reduce([0.0, 0.0, 0.0], [1.0, 1.0, 1.0], 0.5)
        [leg_red_x, leg_red_y, leg_red_z]
    """
    COM_leg_list = COM_leg_list_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 3:
            temp_list.append(icos_face_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


