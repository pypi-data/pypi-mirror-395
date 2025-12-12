from ..gen_platonic.mid_pt import mid_pt
from .tetr_face_COM_coord import tetr_face_COM_coord


def tetr_face_COM_leg_coord(a: float, b: float, c: float):
    """Calculates the center of mass (COM) coordinates of the legs of a tetrahedron face.

    Args:
        a (float): The coordinates of the first vertex of the tetrahedron face, as a list or tuple of three floats.
        b (float): The coordinates of the second vertex of the tetrahedron face, as a list or tuple of three floats.
        c (float): The coordinates of the third vertex of the tetrahedron face, as a list or tuple of three floats.

    Returns:
        list: A list of four lists, each containing three floats representing the center of mass (COM) coordinates of
        one of the legs of the tetrahedron face. The first list contains the COM coordinates of the face itself, and the
        subsequent lists contain the COM coordinates of each leg formed by the midpoints of the edges of the face.

    Examples:
        >>> a = [0.0, 0.0, 0.0]
        >>> b = [1.0, 0.0, 0.0]
        >>> c = [0.0, 1.0, 0.0]
        >>> tetr_face_COM_leg_coord(a, b, c)
        [[0.5, 0.5, 0.0], [0.5, 0.0, 0.0], [0.5, 0.5, 0.0], [0.0, 0.5, 0.0]]

    Note:
        This function relies on the 'mid_pt' function from the '..gen_platonic.mid_pt' module.
        The 'mid_pt' function is responsible for calculating the midpoint between two points.
        The center of mass (COM) coordinates of the legs are calculated using the 'tetr_face_COM_coord' function,
        which in turn uses the formula:
        COM = Vertex + (Midpoint - Vertex) / (1 + sin(30 degrees)) for each vertex of the tetrahedron face.
    """
    COM_leg = []
    COM_leg.append(tetr_face_COM_coord(a, b, c))
    COM_leg.append(mid_pt(a, b))
    COM_leg.append(mid_pt(b, c))
    COM_leg.append(mid_pt(c, a))
    return COM_leg


