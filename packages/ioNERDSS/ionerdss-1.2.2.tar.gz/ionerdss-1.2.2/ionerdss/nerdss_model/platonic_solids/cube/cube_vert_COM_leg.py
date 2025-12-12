import numpy as np
from ..gen_platonic.mid_pt import mid_pt


def cube_vert_COM_leg(COM: float, a: float, b: float, c: float):
    """Calculates the midpoints of three line segments between a central point and three other points.

    Args:
        COM (float): The central point of the cube.
        a (float): The first point.
        b (float): The second point.
        c (float): The third point.

    Returns:
        list: A list containing four floating-point values rounded to 10 decimal places, representing the central point
        (COM) and the midpoints (lega, legb, legc) of the three line segments.


    Example:
        cube_vert_COM_leg(0.5, 1.0, 2.0, 3.0)
        # Calculates the midpoints of the line segments between the central point 0.5 and three other points
        # (1.0, 2.0, 3.0), and returns a list containing the calculated values rounded to 10 decimal places.
    """
    
    lega = mid_pt(COM, a)
    legb = mid_pt(COM, b)
    legc = mid_pt(COM, c)
    return [np.around(COM, 10), np.around(lega, 10), np.around(legb, 10), np.around(legc, 10)]


