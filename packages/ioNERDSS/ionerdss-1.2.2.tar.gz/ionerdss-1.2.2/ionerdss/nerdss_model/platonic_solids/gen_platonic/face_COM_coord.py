import math
from .mid_pt import mid_pt


def face_COM_coord(a: float, b: float, c: float):
    """Calculate the center of mass (COM) coordinates for an icosahedron face.

    This function calculates the center of mass (COM) coordinates for an icosahedron face
    with three given coordinates `a`, `b`, and `c` using the `mid_pt()` function from the
    `mid_pt` module. The COM coordinates are calculated based on the formula:
    COM = original_coordinate + (mid_point_coordinate - original_coordinate) / (1 + sin(30 degrees))

    Args:
        a (float): The first coordinate of the icosahedron face.
        b (float): The second coordinate of the icosahedron face.
        c (float): The third coordinate of the icosahedron face.

    Returns:
        List[float]: The center of mass (COM) coordinates as a list of three floats.

    Examples:
        >>> a = [0, 0, 0]
        >>> b = [1, 1, 1]
        >>> c = [2, 2, 2]
        >>> icos_face_COM_coord(a, b, c)
        [1.3660254037847, 1.3660254037847, 1.3660254037847]

    Notes:
        - The COM coordinates are calculated based on the formula mentioned above, where `sin()` function takes
          angle in radians. The angle is calculated as 30 degrees converted to radians using `math.pi`.
        - The calculated COM coordinates are rounded to 12 decimal places using the `round()` function.
        - The function returns the COM coordinates as a list of three floats.
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


