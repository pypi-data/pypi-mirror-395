import math
from ..gen_platonic.distance import distance


def icos_face_leg_reduce(COM: float, leg: float, sigma: float):
    """ Generates a list of reduced leg coordinates for each center of mass (COM) of an icosahedron face.

    Args:
        radius (float): Radius of the icosahedron.
        sigma (float): Sigma value for leg reduction.

    Returns:
        list: A list of reduced leg coordinates for each COM.

    Example:
        >>> icos_face_leg_reduce_coord_gen(1.0, 0.5)
        [[COM1, leg1_red_x, leg1_red_y, leg1_red_z],
         [COM2, leg2_red_x, leg2_red_y, leg2_red_z],
         ...
        ]
    """
    n = 12
    angle = math.acos(-5**0.5/3)
    red_len = sigma/(2*math.sin(angle/2))
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], n))
    return leg_red


