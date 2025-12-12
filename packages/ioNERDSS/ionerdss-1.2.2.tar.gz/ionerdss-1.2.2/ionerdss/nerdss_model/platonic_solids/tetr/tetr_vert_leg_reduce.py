from ..gen_platonic.distance import distance


def tetr_vert_leg_reduce(COM: float, leg: float, sigma: float):
    """Reduce the length of a leg vector of a regular tetrahedron by a scaling factor sigma, with respect to the center of mass (COM).

    Args:
        COM (float): The 3-dimensional coordinate vector of the center of mass of the tetrahedron.
        leg (float): The 3-dimensional coordinate vector of the original leg.
        sigma (float): The scaling factor for reducing the length of the leg.

    Returns:
        list: A list of 3-dimensional coordinate vectors representing the reduced leg vector of the tetrahedron.

    Example:
        >>> tetr_vert_leg_reduce([0.0, 0.0, 0.0], [1.0, 0.0, 0.0], 0.5)
        [0.25, 0.0, 0.0]
    """
    red_len = sigma/2
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], 8))
    return leg_red


