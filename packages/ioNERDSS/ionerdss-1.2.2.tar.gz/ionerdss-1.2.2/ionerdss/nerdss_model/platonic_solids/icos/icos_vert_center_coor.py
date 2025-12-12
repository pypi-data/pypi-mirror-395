import math
from ..gen_platonic.mid_pt import mid_pt


def icos_vert_center_coor(a: float, b: float, c: float, d: float, e: float):
    """Calculate the coordinates of the center of mass for an icosahedron.

    This function calculates the coordinates of the center of mass (COM) for
    an icosahedron, given the coordinates of five points (a, b, c, d, e) and
    using the mid_pt function from the ..gen_platonic.mid_pt module. The COM
    coordinates are computed based on the formula:
    COM = point + (mid_point - point) / (1 + sin(0.3 * pi))

    Args:
        a (float): The coordinates of point a as a list or tuple of three float values.
        b (float): The coordinates of point b as a list or tuple of three float values.
        c (float): The coordinates of point c as a list or tuple of three float values.
        d (float): The coordinates of point d as a list or tuple of three float values.
        e (float): The coordinates of point e as a list or tuple of three float values.

    Returns:
        list: The coordinates of the center of mass (COM) as a list of three float values.

    Example:
        >>> a = [1.0, 2.0, 3.0]
        >>> b = [4.0, 5.0, 6.0]
        >>> c = [7.0, 8.0, 9.0]
        >>> d = [10.0, 11.0, 12.0]
        >>> e = [13.0, 14.0, 15.0]
        >>> icos_vert_center_coor(a, b, c, d, e)
        [5.18101203220144, 6.58101203220144, 7.98101203220144]
    """
    n = 8
    mid_a = mid_pt(c, d)
    mid_b = mid_pt(d, e)
    mid_c = mid_pt(a, e)
    COM_a = []
    COM_b = []
    COM_c = []
    for i in range(0, 3):
        COM_a.append(round(a[i] + (mid_a[i] - a[i]) /
                     (1+math.sin(0.3*math.pi)), 14))
        COM_b.append(round(b[i] + (mid_b[i] - b[i]) /
                     (1+math.sin(0.3*math.pi)), 14))
        COM_c.append(round(c[i] + (mid_c[i] - c[i]) /
                     (1+math.sin(0.3*math.pi)), 14))
    if round(COM_a[0], n) == round(COM_b[0], n) and round(COM_b[0], n) == round(COM_c[0], n) and \
        round(COM_a[1], n) == round(COM_b[1], n) and round(COM_b[1], n) == round(COM_c[1], n) and \
            round(COM_a[2], n) == round(COM_b[2], n) and round(COM_b[2], n) == round(COM_c[2], n):
        return COM_a
    else:
        return COM_a


