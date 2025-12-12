from .octa_face_vert_coord import octa_face_vert_coord
from .octa_face_COM_leg_coord import octa_face_COM_leg_coord


def octa_face_COM_leg_list_gen(radius: float):
    """Generate a list of center of mass (COM) and midpoints of legs for all octahedron faces.

    Given the radius of an octahedron, this function generates a list of center of mass (COM)
    and midpoints of legs for all eight faces of the octahedron using the 'octa_face_vert_coord'
    and 'octa_face_COM_leg_coord' functions from the respective modules.

    Args:
        radius (float): The radius of the octahedron.

    Returns:
        list: A list of eight elements, each element containing a list of four sub-elements:
            - A list of three floats representing the x, y, and z coordinates of the center of mass (COM)
              for a particular octahedron face.
            - A list of three floats representing the x, y, and z coordinates of the midpoint of the leg
              connecting vertices of that face.
            - A list of three floats representing the x, y, and z coordinates of the midpoint of the leg
              connecting vertices of that face.
            - A list of three floats representing the x, y, and z coordinates of the midpoint of the leg
              connecting vertices of that face.
    """
    coord = octa_face_vert_coord(radius)
    COM_leg_list = []

    COM_leg_list.append(octa_face_COM_leg_coord(coord[0], coord[2], coord[4]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[0], coord[3], coord[4]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[0], coord[3], coord[5]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[0], coord[2], coord[5]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[1], coord[2], coord[4]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[1], coord[3], coord[4]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[1], coord[3], coord[5]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[1], coord[2], coord[5]))
    return COM_leg_list


