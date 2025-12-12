from .tetr_face_coord import tetr_face_coord
from .tetr_face_COM_leg_coord import tetr_face_COM_leg_coord


def tetr_face_COM_leg_list_gen(radius: float):
    """Generates a list of center of mass (COM) coordinates for the legs of a tetrahedron face.

    Args:
        radius (float): The radius of the circumscribed sphere of the tetrahedron.

    Returns:
        list: A list of four lists, each containing three floats representing the COM coordinates of the legs of
        a tetrahedron face. The first list contains the COM coordinates of the legs formed by the vertices at
        indices 0, 1, and 2 of the face, and subsequent lists contain the COM coordinates of the legs formed by
        the other combinations of vertices.
    """
    coord = tetr_face_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(tetr_face_COM_leg_coord(coord[0], coord[1], coord[2]))
    COM_leg_list.append(tetr_face_COM_leg_coord(coord[0], coord[2], coord[3]))
    COM_leg_list.append(tetr_face_COM_leg_coord(coord[0], coord[1], coord[3]))
    COM_leg_list.append(tetr_face_COM_leg_coord(coord[1], coord[2], coord[3]))
    return COM_leg_list


