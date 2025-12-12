from .vert_coord import vert_coord
from .COM_leg_coord import COM_leg_coord


def COM_leg_list_gen(radius: float):
    """Generate Center of Mass (COM) and Leg Coordinates List for an Icosahedron Face.
    This function generates the Center of Mass (COM) and Leg Coordinates List for each face of an icosahedron given the radius of the circumscribed sphere.

    Args:
        radius (float): The radius of the circumscribed sphere of the icosahedron.

    Returns:
        list: A list containing the Center of Mass (COM) and Leg Coordinates for each face of the icosahedron. The list contains 19 tuples, where each tuple contains three numpy arrays representing the COM and two leg coordinates of a face.
    """

    coord = vert_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(COM_leg_coord(coord[0], coord[2], coord[8]))
    COM_leg_list.append(COM_leg_coord(coord[0], coord[8], coord[4]))
    COM_leg_list.append(COM_leg_coord(coord[0], coord[4], coord[6]))
    COM_leg_list.append(COM_leg_coord(coord[0], coord[6], coord[10]))
    COM_leg_list.append(COM_leg_coord(coord[0], coord[10], coord[2]))
    COM_leg_list.append(COM_leg_coord(coord[3], coord[7], coord[5]))
    COM_leg_list.append(COM_leg_coord(coord[3], coord[5], coord[9]))
    COM_leg_list.append(COM_leg_coord(coord[3], coord[9], coord[1]))
    COM_leg_list.append(COM_leg_coord(coord[3], coord[1], coord[11]))
    COM_leg_list.append(COM_leg_coord(coord[3], coord[11], coord[7]))
    COM_leg_list.append(COM_leg_coord(coord[7], coord[2], coord[5]))
    COM_leg_list.append(COM_leg_coord(coord[2], coord[5], coord[8]))
    COM_leg_list.append(COM_leg_coord(coord[5], coord[8], coord[9]))
    COM_leg_list.append(COM_leg_coord(coord[8], coord[9], coord[4]))
    COM_leg_list.append(COM_leg_coord(coord[9], coord[4], coord[1]))
    COM_leg_list.append(COM_leg_coord(coord[4], coord[1], coord[6]))
    COM_leg_list.append(COM_leg_coord(coord[1], coord[6], coord[11]))
    COM_leg_list.append(COM_leg_coord(
        coord[6], coord[11], coord[10]))
    COM_leg_list.append(COM_leg_coord(
        coord[11], coord[10], coord[7]))
    COM_leg_list.append(COM_leg_coord(coord[10], coord[7], coord[2]))
    return COM_leg_list


