import math
from ..gen_platonic.distance import distance


def dode_face_leg_reduce(COM: float, leg: float, sigma: float):
    """Calculates the reduced length of a dodecahedron leg based on the given center of mass (COM), leg coordinates,
    and sigma value.

    Args:
        COM (float): The coordinates of the center of mass as a list [x, y, z], where x, y, and z are floats.
        leg (float): The coordinates of the leg as a list [x, y, z], where x, y, and z are floats.
        sigma (float): The sigma value for the dodecahedron face.

    Returns:
        list: A list containing the reduced coordinates of the leg after applying the reduction factor.
        The list contains three elements [x', y', z'], where x', y', and z' are the reduced coordinates of the leg
        rounded to 14 decimal places.
    """
    
    # calculate the recuced length when considering the sigma value
    n = 14
    m = (1+5**(0.5))/2
    angle = 2*math.atan(m)
    red_len = sigma/(2*math.sin(angle/2))
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], n))
    return leg_red


