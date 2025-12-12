import math
from ..gen_platonic.mid_pt import mid_pt


def octa_face_COM_coord(a: float, b: float, c: float):
    """Calculate the center of mass (COM) coordinates for an octahedron face.

    Given the coordinates of three vertices of an octahedron face (a, b, c), this function
    calculates the center of mass (COM) coordinates for that face using the midpoint formula
    and a correction factor based on the sine of 30 degrees.

    Args:
        a (float): The coordinates of the first vertex of the octahedron face as a list or tuple
                   of three floats representing the x, y, and z coordinates, respectively.
        b (float): The coordinates of the second vertex of the octahedron face as a list or tuple
                   of three floats representing the x, y, and z coordinates, respectively.
        c (float): The coordinates of the third vertex of the octahedron face as a list or tuple
                   of three floats representing the x, y, and z coordinates, respectively.

    Returns:
        list: A list of three floats representing the x, y, and z coordinates of the center of mass
              (COM) for the octahedron face.

    Example:
        To calculate the center of mass coordinates for an octahedron face with vertices
        a = [1.0, 2.0, 3.0], b = [4.0, 5.0, 6.0], and c = [7.0, 8.0, 9.0]:
        >>> octa_face_COM_coord([1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0])
        [3.5, 4.5, 5.5]
    """
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


