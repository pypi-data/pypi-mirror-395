from .octa_vert_coord import octa_vert_coord
from .octa_vert_COM_leg import octa_vert_COM_leg

def octa_vert_COM_leg_gen(radius: float):
    """
    Generates center of mass and leg vectors for an octagon.

    Args:
        radius (float): The radius of the octagon.

    Returns:
        list: A list of center of mass and leg vectors for the octagon.
            Each element in the list is a tuple of the form (COM, leg1, leg2, leg3, leg4),
            where COM is the center of mass vector and leg1, leg2, leg3, leg4 are the leg vectors.

    Example:
        coord = octa_vert_COM_leg_gen(5.0)
        print(coord)
    """
    
    coord = octa_vert_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(octa_vert_COM_leg(
        coord[0], coord[2], coord[4], coord[3], coord[5]))
    COM_leg_list.append(octa_vert_COM_leg(
        coord[1], coord[2], coord[4], coord[3], coord[5]))
    COM_leg_list.append(octa_vert_COM_leg(
        coord[2], coord[1], coord[5], coord[0], coord[4]))
    COM_leg_list.append(octa_vert_COM_leg(
        coord[3], coord[1], coord[5], coord[0], coord[4]))
    COM_leg_list.append(octa_vert_COM_leg(
        coord[4], coord[1], coord[2], coord[0], coord[3]))
    COM_leg_list.append(octa_vert_COM_leg(
        coord[5], coord[1], coord[2], coord[0], coord[3]))
    return COM_leg_list


