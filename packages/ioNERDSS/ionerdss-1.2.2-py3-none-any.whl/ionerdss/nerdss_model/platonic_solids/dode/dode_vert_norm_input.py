from ..gen_platonic.distance import distance
from .dode_vert_input_coord import dode_vert_input_coord
import numpy as np

def dode_vert_norm_input(radius: float, sigma: float):
    """
    Calculates normalized input values for a dodecahedron vertex based on radius and sigma values.

    This function calculates the normalized center of mass (COM) and leg vectors for a dodecahedron vertex based on the
    provided radius and sigma values. The normalized COM and leg vectors are obtained by calling the dode_vert_input_coord
    function to calculate the original COM and leg vectors, and then performing various calculations to normalize their
    values. The normalized COM and leg vectors are stored in numpy arrays and returned.

    Args:
        radius (float): The radius of the dodecahedron.
        sigma (float): The sigma value for the dodecahedron vertex.

    Returns:
        numpy.ndarray: A numpy array representing the normalized center of mass (COM) vector.
        numpy.ndarray: A numpy array representing the normalized first leg (lg1) vector.
        numpy.ndarray: A numpy array representing the normalized second leg (lg2) vector.
        numpy.ndarray: A numpy array representing the normalized third leg (lg3) vector.
        numpy.ndarray: A numpy array representing the normalized normal (n) vector.
    """
    
    COM, lg1, lg2, lg3, n = dode_vert_input_coord(radius, sigma)
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


