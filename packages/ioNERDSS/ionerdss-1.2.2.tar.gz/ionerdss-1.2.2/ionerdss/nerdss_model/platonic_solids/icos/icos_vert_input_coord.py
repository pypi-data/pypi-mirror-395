from .icos_vert_leg_reduce_coor_gen import icos_vert_leg_reduce_coor_gen
import numpy as np


def icos_vert_input_coord(radius: float, sigma: float):
    """Generate input vertex coordinates for an icosahedron with the given radius and sigma.

    The function calculates the input vertex coordinates for an icosahedron with the given radius and sigma,
    using mathematical formulas and numpy operations.

    Args:
        radius (float): The radius of the icosahedron.
        sigma (float): The sigma value for generating the vertex coordinates.

    Returns:
        tuple: A tuple of input vertex coordinates for the icosahedron, including the center of mass (COM),
        and the leg vectors (lg1, lg2, lg3, lg4, lg5) and the normalized normal vector (n).
    """
    coor = icos_vert_leg_reduce_coor_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = np.around(coor_[0] - coor_[0], 12)
    lg1 = np.around(coor_[1] - coor_[0], 12)
    lg2 = np.around(coor_[2] - coor_[0], 12)
    lg3 = np.around(coor_[3] - coor_[0], 12)
    lg4 = np.around(coor_[4] - coor_[0], 12)
    lg5 = np.around(coor_[5] - coor_[0], 12)
    n = np.around(coor_[0]/np.linalg.norm(coor_[0]), 12)
    return COM, lg1, lg2, lg3, lg4, lg5, n


