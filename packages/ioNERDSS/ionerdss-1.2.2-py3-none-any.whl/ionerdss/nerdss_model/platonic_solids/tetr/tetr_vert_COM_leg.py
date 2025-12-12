import numpy as np
from ..gen_platonic.mid_pt import mid_pt


def tetr_vert_COM_leg(COM: float, a: float, b: float, c: float):
    """Calculates the center of mass (COM) and midpoints of three edges of a tetrahedron.
    
    Args:
        COM (float): The center of mass of the tetrahedron.
        a (float): The first vertex of the tetrahedron.
        b (float): The second vertex of the tetrahedron.
        c (float): The third vertex of the tetrahedron.
        
    Returns:
        list: A list of four values, [COM, lega, legb, legc], rounded to 10 decimal places.
        
    Example:
        >>> tetr_vert_COM_leg(0.5, 1.0, 2.0, 3.0)
        [0.5, 0.75, 1.5, 2.25]
    """

    lega = mid_pt(COM, a)
    legb = mid_pt(COM, b)
    legc = mid_pt(COM, c)
    return [np.around(COM, 10), np.around(lega, 10), np.around(legb, 10), np.around(legc, 10)]


