import numpy as np
from ..gen_platonic.mid_pt import mid_pt


def dode_vert_COM_leg(COM: float, a: float, b: float, c: float):
    """
    Calculates and returns the vertices of a dodecahedron leg based on the center of mass (COM) and three reference points.

    Args:
        COM (float): Center of mass of the dodecahedron.
        a (float): First reference point.
        b (float): Second reference point.
        c (float): Third reference point.

    Returns:
        list: List of vertices as [COM, lega, legb, legc], rounded to 10 decimal places.

    Example:
        >>> dode_vert_COM_leg(1.0, 2.0, 3.0, 4.0)
        [1.0, 1.5, 2.5, 3.5]
    """
    
    lega = mid_pt(COM, a)
    legb = mid_pt(COM, b)
    legc = mid_pt(COM, c)
    return [np.around(COM, 10), np.around(lega, 10), np.around(legb, 10), np.around(legc, 10)]


