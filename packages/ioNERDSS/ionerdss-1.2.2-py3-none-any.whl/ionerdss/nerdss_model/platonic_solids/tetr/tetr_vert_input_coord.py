from .tetr_vert_leg_reduce_coor_gen import tetr_vert_leg_reduce_coor_gen
import numpy as np


def tetr_vert_input_coord(radius: float, sigma: float):
    """Generate the input coordinates for a regular tetrahedron given the radius and sigma.

    Args:
        radius (float): The radius of the circumsphere of the tetrahedron.
        sigma (float): The scaling factor for the coordinates.

    Returns:
        tuple: A tuple containing the center of mass (COM) and three leg vectors of the tetrahedron,
        as well as the normalized vector of the first vertex.

    Example:
        >>> tetr_vert_input_coord(1.0, 0.5)
        (array([0., 0., 0.]), array([0.5, 0., 0.]), array([0., 0.5, 0.]), array([0., 0., 0.5]), array([1., 0., 0.]))
    """
    coor = tetr_vert_leg_reduce_coor_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = np.around(coor_[0] - coor_[0], 8)
    lg1 = np.around(coor_[1] - coor_[0], 8)
    lg2 = np.around(coor_[2] - coor_[0], 8)
    lg3 = np.around(coor_[3] - coor_[0], 8)
    n = np.around(coor_[0]/np.linalg.norm(coor_[0]), 8)
    return COM, lg1, lg2, lg3, n


