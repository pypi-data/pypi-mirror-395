from .dode_face_dodecahedron_coord import dode_face_dodecahedron_coord
from .dode_face_COM_leg_coor import dode_face_COM_leg_coor


def dode_face_COM_leg_list_gen(radius: float):
    """Generate the Center of Mass (COM) and leg coordinates of 12 faces of a dodecahedron.

    Args:
        radius (float): The radius of the dodecahedron.

    Returns:
        list: A list containing the COM and leg coordinates of 12 faces as a large list.

    """
    
    # generate all COM and leg coords of 12 faces as a large list
    coord = dode_face_dodecahedron_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[6], coord[18], coord[2], coord[14], coord[4]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[6], coord[4], coord[12], coord[0], coord[16]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[4], coord[14], coord[9], coord[8], coord[12]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[6], coord[18], coord[11], coord[10], coord[16]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[14], coord[2], coord[3], coord[15], coord[9]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[18], coord[11], coord[19], coord[3], coord[2]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[16], coord[10], coord[17], coord[1], coord[0]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[12], coord[0], coord[1], coord[13], coord[8]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[7], coord[17], coord[10], coord[11], coord[19]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[5], coord[13], coord[8], coord[9], coord[15]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[3], coord[19], coord[7], coord[5], coord[15]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[1], coord[17], coord[7], coord[5], coord[13]))
    return COM_leg_list


