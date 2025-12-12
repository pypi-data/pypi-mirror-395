from ..gen_platonic.mid_pt import mid_pt
from .octa_face_COM_coord import octa_face_COM_coord


def octa_face_COM_leg_coord(a: float, b: float, c: float):
    """Calculate the coordinates of the center of mass (COM) and midpoints of the legs
    of an octahedron face.

    Given the coordinates of three vertices of an octahedron face (a, b, c), this function
    calculates the coordinates of the center of mass (COM) and the midpoints of the legs of
    that face using the 'octa_face_COM_coord' and 'mid_pt' functions from the respective
    modules.

    Args:
        a (float): The coordinates of the first vertex of the octahedron face as a list or tuple
                   of three floats representing the x, y, and z coordinates, respectively.
        b (float): The coordinates of the second vertex of the octahedron face as a list or tuple
                   of three floats representing the x, y, and z coordinates, respectively.
        c (float): The coordinates of the third vertex of the octahedron face as a list or tuple
                   of three floats representing the x, y, and z coordinates, respectively.

    Returns:
        list: A list of four elements:
            - A list of three floats representing the x, y, and z coordinates of the center of mass (COM)
              for the octahedron face.
            - A list of three floats representing the x, y, and z coordinates of the midpoint of the leg
              connecting vertices a and b.
            - A list of three floats representing the x, y, and z coordinates of the midpoint of the leg
              connecting vertices b and c.
            - A list of three floats representing the x, y, and z coordinates of the midpoint of the leg
              connecting vertices c and a.

    Example:
        To calculate the coordinates of the center of mass and midpoints of the legs for an octahedron
        face with vertices a = [1.0, 2.0, 3.0], b = [4.0, 5.0, 6.0], and c = [7.0, 8.0, 9.0]:
        >>> octa_face_COM_leg_coord([1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0])
        [[3.5, 4.5, 5.5], [2.5, 3.5, 4.5], [5.5, 6.5, 7.5], [4.0, 5.0, 6.0]]

    """
    COM_leg = []
    COM_leg.append(octa_face_COM_coord(a, b, c))
    COM_leg.append(mid_pt(a, b))
    COM_leg.append(mid_pt(b, c))
    COM_leg.append(mid_pt(c, a))
    return COM_leg


