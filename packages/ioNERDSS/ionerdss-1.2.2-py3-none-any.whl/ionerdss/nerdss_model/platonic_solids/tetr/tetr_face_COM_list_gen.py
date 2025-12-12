from .tetr_face_coord import tetr_face_coord
from .tetr_face_COM_coord import tetr_face_COM_coord


def tetr_face_COM_list_gen(radius: float):
    """Generates a list of center of mass (COM) coordinates for a tetrahedron's faces.

    Args:
        radius (float): The radius of the circumscribed sphere of the tetrahedron.

    Returns:
        list: A list of COM coordinates for the tetrahedron's faces. The list contains 4 tuples,
        each representing the COM coordinates of one face. Each tuple contains 3 floats representing
        the x, y, and z coordinates of the COM.

    Example:
        >>> tetr_face_COM_list_gen(1.0)
        [(-0.5, -0.5, -0.5), (0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, -0.5)]
    """
    coord = tetr_face_coord(radius)
    COM_list = []
    COM_list.append(tetr_face_COM_coord(coord[0], coord[1], coord[2]))
    COM_list.append(tetr_face_COM_coord(coord[0], coord[2], coord[3]))
    COM_list.append(tetr_face_COM_coord(coord[0], coord[1], coord[3]))
    COM_list.append(tetr_face_COM_coord(coord[1], coord[2], coord[3]))
    return COM_list


