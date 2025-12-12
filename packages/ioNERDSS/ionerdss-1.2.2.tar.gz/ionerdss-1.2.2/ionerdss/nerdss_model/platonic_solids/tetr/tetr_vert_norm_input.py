from ..gen_platonic.distance import distance
from .tetr_vert_input_coord import tetr_vert_input_coord
import numpy as np


def tetr_vert_norm_input(radius: float, sigma: float):
    """Generate the normalized input coordinates for a regular tetrahedron given the radius and sigma.

    Args:
        radius (float): The radius of the circumsphere of the tetrahedron.
        sigma (float): The scaling factor for reducing the length of the legs.

    Returns:
        tuple: A tuple containing the 3-dimensional coordinate vectors of the center of mass (COM), and the
        normalized leg and normal vectors of the tetrahedron, respectively.

    Example:
        >>> tetr_vert_norm_input(1.0, 0.5)
        (array([0., 0., 0.]),
         array([-0.5      , -0.2886751, -0.8164966]),
         array([0.5      , -0.2886751, -0.8164966]),
         array([0.       , 0.5773503, -0.8164966]),
         array([0., 0., 1.]))
    """

    COM, lg1, lg2, lg3, n = tetr_vert_input_coord(radius, sigma)
    length = distance(lg1, lg2)
    dis1 = ((-length/2)**2+(-((length/2)*(3**0.5))/3)**2)**0.5
    dis2 = distance(COM, lg1)
    height = (dis2**2-dis1**2)**0.5
    lg1_ = np.array([-length/2, -((length/2)*(3**0.5))/3, -height])
    lg2_ = np.array([length/2, -((length/2)*(3**0.5))/3, -height])
    lg3_ = np.array([0, ((length/2)*(3**0.5))/3*2, -height])
    COM_ = np.array([0, 0, 0])
    n_ = np.array([0, 0, 1])
    return COM_, lg1_, lg2_, lg3_, n_


