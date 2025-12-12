import math
from ..gen_platonic.distance import distance


def tetr_face_leg_reduce(COM: float, leg: float, sigma: float):
    """Reduces the length of a leg of a tetrahedron face given its center of mass (COM), the original length of the leg,
    and a scaling factor sigma.

    Args:
        COM (float): The coordinates of the center of mass of the tetrahedron face as a list of 3 floats representing
        the x, y, and z coordinates.
        leg (float): The coordinates of the original leg of the tetrahedron face as a list of 3 floats representing
        the x, y, and z coordinates.
        sigma (float): A scaling factor for reducing the length of the leg.

    Returns:
        list: A list of 3 floats representing the reduced coordinates of the leg after applying the scaling factor.

    Example:
        >>> tetr_face_leg_reduce([0.0, 0.0, 0.0], [-0.5, 0.0, 0.0], 0.5)
        [-0.25, 0.0, 0.0]
    """
    n = 12
    angle = math.acos(1/3)
    red_len = sigma/(2*math.sin(angle/2))
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], n))
    return leg_red


