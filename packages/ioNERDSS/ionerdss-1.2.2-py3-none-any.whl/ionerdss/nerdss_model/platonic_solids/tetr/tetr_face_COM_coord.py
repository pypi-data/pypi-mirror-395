import math
from ..gen_platonic.mid_pt import mid_pt


def tetr_face_COM_coord(a: float, b: float, c: float):
    """Calculates the center of mass (COM) coordinates for a tetrahedron face.

    Args:
        a (float): The coordinates of the first vertex of the tetrahedron face, as a list or tuple of three floats.
        b (float): The coordinates of the second vertex of the tetrahedron face, as a list or tuple of three floats.
        c (float): The coordinates of the third vertex of the tetrahedron face, as a list or tuple of three floats.

    Returns:
        list: A list of three floats representing the center of mass (COM) coordinates of the tetrahedron face.

    Examples:
        >>> a = [0.0, 0.0, 0.0]
        >>> b = [1.0, 0.0, 0.0]
        >>> c = [0.0, 1.0, 0.0]
        >>> tetr_face_COM_coord(a, b, c)
        [0.5, 0.5, 0.0]

    Note:
        This function relies on the 'mid_pt' function from the '..gen_platonic.mid_pt' module.
        The 'mid_pt' function is responsible for calculating the midpoint between two points.
        The center of mass (COM) coordinates are calculated using the formula:
        COM = Vertex + (Midpoint - Vertex) / (1 + sin(30 degrees)) for each vertex of the tetrahedron face.
    """
    n = 10
    mid_a = mid_pt(b, c)
    mid_b = mid_pt(a, c)
    mid_c = mid_pt(a, b)
    COM_a = []
    COM_b = []
    COM_c = []
    for i in range(0, 3):
        COM_a.append(round(a[i] + (mid_a[i] - a[i]) /
                     (1+math.sin(30/180*math.pi)), 12))
        COM_b.append(round(b[i] + (mid_b[i] - b[i]) /
                     (1+math.sin(30/180*math.pi)), 12))
        COM_c.append(round(c[i] + (mid_c[i] - c[i]) /
                     (1+math.sin(30/180*math.pi)), 12))

    if COM_a == COM_b and COM_b == COM_c:
        return COM_a
    else:
        return COM_a


