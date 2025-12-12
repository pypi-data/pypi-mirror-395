from .octa_face_vert_coord import octa_face_vert_coord
from .octa_face_COM_coord import octa_face_COM_coord


def octa_face_COM_list_gen(radius: float):
    """Generates a list of center of mass (COM) coordinates for the faces of an octahedron.

    Args:
        radius (float): The radius of the octahedron.

    Returns:
        List: A list of COM coordinates for the faces of the octahedron.

    Example:
        coord = octa_face_vert_coord(radius)
        COM_list = octa_face_COM_list_gen(radius)
        print(COM_list)

    Note:
        The octahedron is assumed to be centered at the origin (0,0,0) and aligned with the
        coordinate axes. The function uses the octa_face_vert_coord() function to generate
        the vertex coordinates of the octahedron, and then calculates the center of mass
        coordinates for the faces using the octa_face_COM_coord() function.
    """
    coord = octa_face_vert_coord(radius)
    COM_list = []
    COM_list.append(octa_face_COM_coord(coord[0], coord[2], coord[4]))
    COM_list.append(octa_face_COM_coord(coord[0], coord[3], coord[4]))
    COM_list.append(octa_face_COM_coord(coord[0], coord[3], coord[5]))
    COM_list.append(octa_face_COM_coord(coord[0], coord[2], coord[5]))
    COM_list.append(octa_face_COM_coord(coord[1], coord[2], coord[4]))
    COM_list.append(octa_face_COM_coord(coord[1], coord[3], coord[4]))
    COM_list.append(octa_face_COM_coord(coord[1], coord[3], coord[5]))
    COM_list.append(octa_face_COM_coord(coord[1], coord[2], coord[5]))
    return COM_list


