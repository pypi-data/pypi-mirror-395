from .octa_vert_leg_reduce_coor_gen import octa_vert_leg_reduce_coor_gen
import numpy as np


def octa_vert_input_coord(radius: float, sigma: float):
    """ Calculates the input coordinates of an octagonal vertex based on a given radius and sigma.

    The input coordinates are derived from the reduced coordinates of the octagonal vertex, which are generated
    using the `octa_vert_leg_reduce_coor_gen` function. The input coordinates include the center of mass (COM)
    of the vertex, as well as four leg vectors (lg1, lg2, lg3, and lg4) and a normal vector (n) with respect to
    the center of mass.

    Args:
        radius (float): The radius of the octagonal vertex.
        sigma (float): The sigma value used for generating the reduced coordinates of the vertex.

    Returns:
        tuple: A tuple containing the following input coordinates:
            - COM (float): The center of mass of the vertex.
            - lg1 (float): The first leg vector of the vertex.
            - lg2 (float): The second leg vector of the vertex.
            - lg3 (float): The third leg vector of the vertex.
            - lg4 (float): The fourth leg vector of the vertex.
            - n (float): The normal vector of the vertex.

    Example:
        radius = 2.0
        sigma = 0.5
        result = octa_vert_input_coord(radius, sigma)
        print(result)
    """
    coor = octa_vert_leg_reduce_coor_gen(radius, sigma)
    coor_ = np.array(coor[4])
    COM = np.around(coor_[0] - coor_[0], 8)
    lg1 = np.around(coor_[1] - coor_[0], 8)
    lg2 = np.around(coor_[2] - coor_[0], 8)
    lg3 = np.around(coor_[3] - coor_[0], 8)
    lg4 = np.around(coor_[4] - coor_[0], 8)
    n = np.around(coor_[0]/np.linalg.norm(coor_[0]), 8)
    return COM, lg1, lg2, lg3, lg4, n


