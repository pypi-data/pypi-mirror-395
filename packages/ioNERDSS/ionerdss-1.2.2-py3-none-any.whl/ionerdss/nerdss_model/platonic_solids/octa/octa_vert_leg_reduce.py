from ..gen_platonic.distance import distance


def octa_vert_leg_reduce(COM: float, leg: float, sigma: float):
    """Reduces the length of an octagonal vertex leg based on a given center of mass (COM), leg vector, and sigma.

    The reduction of the leg length is calculated using the formula: leg_red = (leg - COM) * ratio + COM, where ratio
    is calculated as 1 minus half of the sigma divided by the distance between COM and leg, as given by the `distance`
    function from the `gen_platonic` module.

    Args:
        COM (float): The center of mass (COM) of the octagonal vertex.
        leg (float): The leg vector of the octagonal vertex.
        sigma (float): The sigma value used for reducing the length of the leg.

    Returns:
        list: A list containing the reduced leg vector (leg_red) of the octagonal vertex, with rounded values
        to 8 decimal places.

    Example:
        COM = [0, 0, 0]
        leg = [1, 1, 1]
        sigma = 0.5
        result = octa_vert_leg_reduce(COM, leg, sigma)
        print(result)
    """
    red_len = sigma/2
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], 8))
    return leg_red


