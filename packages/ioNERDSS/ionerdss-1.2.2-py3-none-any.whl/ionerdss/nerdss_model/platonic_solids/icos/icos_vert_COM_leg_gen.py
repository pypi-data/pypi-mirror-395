from .icos_vert_coord import icos_vert_coord
from .icos_vert_COM_leg import icos_vert_COM_leg

def icos_vert_COM_leg_gen(radius: float):
    """Generate a list of center of mass (COM) and legs coordinates for an icosahedron.

    The function calculates the center of mass and legs coordinates for an icosahedron
    with the given radius, using the `icos_vert_coord` and `icos_vert_COM_leg` functions.

    Args:
        radius (float): The radius of the icosahedron.

    Returns:
        list: A list of center of mass and legs coordinates for the icosahedron.
    """
    coord = icos_vert_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(icos_vert_COM_leg(
        coord[0], coord[2], coord[8], coord[4], coord[6], coord[10]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[1], coord[4], coord[6], coord[11], coord[3], coord[9]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[2], coord[0], coord[10], coord[7], coord[5], coord[8]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[3], coord[1], coord[11], coord[7], coord[5], coord[9]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[4], coord[0], coord[6], coord[1], coord[9], coord[8]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[5], coord[2], coord[8], coord[7], coord[3], coord[9]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[6], coord[0], coord[10], coord[11], coord[1], coord[4]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[7], coord[3], coord[11], coord[10], coord[2], coord[5]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[8], coord[0], coord[2], coord[5], coord[9], coord[4]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[9], coord[8], coord[4], coord[1], coord[3], coord[5]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[10], coord[0], coord[2], coord[7], coord[11], coord[6]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[11], coord[10], coord[7], coord[3], coord[1], coord[6]))
    return COM_leg_list


