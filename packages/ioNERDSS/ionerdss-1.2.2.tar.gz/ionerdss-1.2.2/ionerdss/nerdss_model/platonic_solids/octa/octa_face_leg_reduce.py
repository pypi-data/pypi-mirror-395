import math
from ..gen_platonic.distance import distance


def octa_face_leg_reduce(COM: float, leg: float, sigma: float):
    """Reduces the length of an octahedron face leg by a given reduction factor sigma.

    Args:
        COM (float): The center of mass (COM) coordinate of the octahedron face.
        leg (float): The leg vector of the octahedron face.
        sigma (float): The reduction factor for the leg length.

    Returns:
        List[float]: A list of reduced leg coordinates after applying the reduction factor.
            The list contains three floating point values representing the x, y, and z coordinates
            of the reduced leg vector.

    Example:
        COM = [0.0, 0.0, 0.0]
        leg = [1.0, 2.0, 3.0]
        sigma = 0.5
        leg_red = octa_face_leg_reduce(COM, leg, sigma)
        print(leg_red)

    Note:
        The function uses the math module to perform mathematical calculations. The reduction factor
        sigma determines how much the length of the leg vector should be reduced. The leg vector is
        reduced by scaling it with a ratio calculated based on the reduction factor and the distance
        between the center of mass (COM) and the leg vector. The resulting reduced leg coordinates are
        rounded to a given number of decimal places (n) before being returned as a list of floating
        point values.
    """
    n = 12
    angle = math.acos(-1/3)
    red_len = sigma/(2*math.sin(angle/2))
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], n))
    return leg_red


