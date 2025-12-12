import numpy as np
from ..gen_platonic.mid_pt import mid_pt


def icos_vert_COM_leg(COM: float, a: float, b: float, c: float, d: float, e: float):
    """Calculate center of mass (COM) and legs from COM to each point.

    Args:
        COM (float): The center of mass point.
        a (float): Point A.
        b (float): Point B.
        c (float): Point C.
        d (float): Point D.
        e (float): Point E.

    Returns:
        list: A list containing the center of mass and legs coordinates, rounded to 10 decimal places.
    """
    lega = mid_pt(COM, a)
    legb = mid_pt(COM, b)
    legc = mid_pt(COM, c)
    legd = mid_pt(COM, d)
    lege = mid_pt(COM, e)
    result = [np.around(COM, 10), np.around(lega, 10), np.around(
        legb, 10), np. around(legc, 10), np.around(legd, 10), np.around(lege, 10)]
    return result


