import math
from ..gen_platonic.distance import distance


def cube_face_leg_reduce(COM: float, leg: float, sigma: float):
    """Reduces the length of a cube face leg vector based on center of mass and sigma.

    This function takes the center of mass (COM), leg vector, and sigma as inputs, and reduces the length of the
    leg vector based on the given sigma value. The reduction is performed using the formula: 
    leg_red = (leg - COM) * ratio + COM, where ratio is calculated as 
    1 - (sigma / (2 * sin(angle / 2))) / distance(COM, leg), and angle is calculated as acos(0).

    Args:
        COM (float): The center of mass of the cube face.
        leg (float): The leg vector of the cube face.
        sigma (float): The sigma value for the reduction.

    Returns:
        List: Contains the reduced leg vector of the cube face, with each coordinate rounded to 'n' decimal places.
        'n' is determined by the value of 'n' in the function.

    Raises:
        None.

    Example:
        >>> cube_face_leg_reduce([0.0, 0.0, 0.0], [1.0, 1.0, 1.0], 0.1)
        [0.131826, 0.131826, 0.131826]
    """
     
    n = 12
    angle = math.acos(0)
    red_len = sigma/(2*math.sin(angle/2))
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], n))
    return leg_red


