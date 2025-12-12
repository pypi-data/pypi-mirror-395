from .icos_face_vert_coord import icos_face_vert_coord
from .icos_face_COM_coord import icos_face_COM_coord


def icos_face_COM_list_gen(radius: float):
    """Generates a list of coordinates representing the centers of mass (COM) of the faces of an icosahedron,
    given the radius of the icosahedron.

    Args:
        radius (float): The radius of the icosahedron.

    Returns:
        list: A list of 20 COM coordinates, each representing the center of mass of a face of the icosahedron.
    """
    coord = icos_face_vert_coord(radius)
    COM_list = []
    COM_list.append(icos_face_COM_coord(coord[0], coord[2], coord[8]))
    COM_list.append(icos_face_COM_coord(coord[0], coord[8], coord[4]))
    COM_list.append(icos_face_COM_coord(coord[0], coord[4], coord[6]))
    COM_list.append(icos_face_COM_coord(coord[0], coord[6], coord[10]))
    COM_list.append(icos_face_COM_coord(coord[0], coord[10], coord[2]))
    COM_list.append(icos_face_COM_coord(coord[3], coord[7], coord[5]))
    COM_list.append(icos_face_COM_coord(coord[3], coord[5], coord[9]))
    COM_list.append(icos_face_COM_coord(coord[3], coord[9], coord[1]))
    COM_list.append(icos_face_COM_coord(coord[3], coord[1], coord[11]))
    COM_list.append(icos_face_COM_coord(coord[3], coord[11], coord[7]))
    COM_list.append(icos_face_COM_coord(coord[7], coord[2], coord[5]))
    COM_list.append(icos_face_COM_coord(coord[2], coord[5], coord[8]))
    COM_list.append(icos_face_COM_coord(coord[5], coord[8], coord[9]))
    COM_list.append(icos_face_COM_coord(coord[8], coord[9], coord[4]))
    COM_list.append(icos_face_COM_coord(coord[9], coord[4], coord[1]))
    COM_list.append(icos_face_COM_coord(coord[4], coord[1], coord[6]))
    COM_list.append(icos_face_COM_coord(coord[1], coord[6], coord[11]))
    COM_list.append(icos_face_COM_coord(coord[6], coord[11], coord[10]))
    COM_list.append(icos_face_COM_coord(coord[11], coord[10], coord[7]))
    COM_list.append(icos_face_COM_coord(coord[10], coord[7], coord[2]))
    return COM_list


