from ..gen_platonic.distance import distance


def cube_vert_leg_reduce(COM: float, leg: float, sigma: float):
    """Reduces the length of a cube vertex leg based on the center of mass (COM) and sigma value.

    This function reduces the length of a cube vertex leg based on the given center of mass (COM) and sigma value, using
    the `distance` function from the `gen_platonic` module to calculate the initial leg length, and then applying a
    reduction ratio based on the calculated length and the specified sigma value.

    Args:
        COM (float): The center of mass (COM) coordinate of the cube vertex, represented as a float value.
        leg (float): The original leg coordinate of the cube vertex, represented as a float value.
        sigma (float): The sigma value for the cube vertex, used to calculate the reduction ratio, represented as a float value.

    Returns:
        list: A list containing three floating-point values representing the reduced leg coordinates of the cube vertex,
        after applying the reduction ratio to each coordinate.


    Example:
        cube_vert_leg_reduce([0.5, 0.5, 0.5], [1.0, 1.0, 1.0], 0.2)
        # Reduces the length of the leg coordinate of a cube vertex with a center of mass (COM) of [0.5, 0.5, 0.5], an
        # original leg coordinate of [1.0, 1.0, 1.0], and a sigma value of 0.2.
        # Returns a list containing three floating-point values representing the reduced leg coordinates of the cube vertex
        # after applying the reduction ratio to each coordinate.
    """
        
    red_len = sigma/2
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], 8))
    return leg_red


