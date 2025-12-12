import numpy as np
from ..gen_platonic.mid_pt import mid_pt


def octa_vert_COM_leg(COM: float, a: float, b: float, c: float, d: float):
    """Calculates the center of mass and leg vectors for an octagon.

    Args:
        COM (float): The center of mass vector of the octagon, given as a tuple (x, y, z).
        a (float): The position of vertex A of the octagon, given as a tuple (x, y, z).
        b (float): The position of vertex B of the octagon, given as a tuple (x, y, z).
        c (float): The position of vertex C of the octagon, given as a tuple (x, y, z).
        d (float): The position of vertex D of the octagon, given as a tuple (x, y, z).

    Returns:
        list: A list of the center of mass and leg vectors for the octagon. The list contains
        5 elements, each rounded to 10 decimal places, in the following order:
        [COM, lega, legb, legc, legd], where COM is the center of mass vector and lega, legb,
        legc, legd are the leg vectors.

    Example:
        COM = (0.5, 0.5, 0.5)
        a = (1.0, 0.0, 0.0)
        b = (0.0, 1.0, 0.0)
        c = (-1.0, 0.0, 0.0)
        d = (0.0, -1.0, 0.0)
        result = octa_vert_COM_leg(COM, a, b, c, d)
        print(result)
    """
    lega = mid_pt(COM, a)
    legb = mid_pt(COM, b)
    legc = mid_pt(COM, c)
    legd = mid_pt(COM, d)
    return [np.around(COM, 10), np.around(lega, 10), np.around(legb, 10), np.around(legc, 10), np.around(legd, 10)]


