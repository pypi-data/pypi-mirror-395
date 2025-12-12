from ..gen_platonic.distance import distance


def dode_vert_leg_reduce(COM: float, leg: float, sigma: float):
    """
    Reduces the length of a dodecahedron leg based on the center of mass (COM), leg vector, and sigma value.

    This function reduces the length of a dodecahedron leg based on the provided center of mass (COM), leg vector, and
    sigma value. The reduction is performed by calculating a ratio based on the sigma value and the distance between the
    center of mass and the leg vector. The leg vector is then scaled by this ratio and added to the center of mass to
    obtain the reduced leg vector.

    Args:
        COM (float): The center of mass (COM) of the dodecahedron vertex.
        leg (float): The leg vector of the dodecahedron vertex.
        sigma (float): The sigma value for the dodecahedron vertex.

    Returns:
        list: A list containing the three reduced leg vector coordinates.
    """
    
    red_len = sigma/2
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], 8))
    return leg_red


