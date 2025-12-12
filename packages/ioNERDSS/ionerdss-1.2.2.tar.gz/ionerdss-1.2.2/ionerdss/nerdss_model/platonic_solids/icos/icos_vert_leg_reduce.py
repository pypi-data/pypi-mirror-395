from ..gen_platonic.distance import distance


def icos_vert_leg_reduce(COM: float, leg: float, sigma: float):
    """Reduce the length of a leg vector of an icosahedron based on the center of mass (COM) and sigma.

    The function calculates the reduced length of a leg vector of an icosahedron based on the given center of mass (COM),
    leg vector, and sigma value, using mathematical formulas and rounding to 8 decimal places.

    Args:
        COM (float): The center of mass (COM) vector of the icosahedron.
        leg (float): The leg vector of the icosahedron.
        sigma (float): The sigma value for reducing the length of the leg vector.

    Returns:
        list: A list of reduced leg vector coordinates for the icosahedron, rounded to 8 decimal places.
    """
    red_len = sigma/2
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], 8))
    return leg_red


