from ..gen_platonic.distance import distance
from .cube_vert_input_coord import cube_vert_input_coord
import numpy as np

def cube_vert_norm_input(radius: float, sigma: float):
    """Generates normalized input coordinates for a cube vertex based on radius and sigma.

    This function generates normalized input coordinates for a cube vertex based on the given radius and sigma values.
    The generated coordinates include the center of mass (COM) coordinate, leg1, leg2, and leg3 coordinates, and a
    normal vector (n), which represents the direction of the normal to the plane of the vertex. The function uses the
    `cube_vert_input_coord` function to generate the initial input coordinates, and then calculates and returns the
    normalized versions of these coordinates.

    Args:
        radius (float): The radius of the cube vertex, represented as a float value.
        sigma (float): The sigma value for the cube vertex, used to calculate the initial input coordinates, represented
            as a float value.

    Returns:
        tuple: A tuple containing the following five elements:
            - COM_ (numpy array): The normalized center of mass (COM) coordinate of the cube vertex, represented as a
                numpy array of shape (3,) and dtype float64.
            - lg1_ (numpy array): The normalized leg1 coordinate of the cube vertex, represented as a numpy array of
                shape (3,) and dtype float64.
            - lg2_ (numpy array): The normalized leg2 coordinate of the cube vertex, represented as a numpy array of
                shape (3,) and dtype float64.
            - lg3_ (numpy array): The normalized leg3 coordinate of the cube vertex, represented as a numpy array of
                shape (3,) and dtype float64.
            - n_ (numpy array): The normalized normal vector (n) of the cube vertex, represented as a numpy array of
                shape (3,) and dtype float64.


    Example:
        cube_vert_norm_input(1.0, 0.2)
        # Generates normalized input coordinates for a cube vertex with a radius of 1.0 and a sigma value of 0.2.
        # Returns a tuple containing the normalized center of mass (COM) coordinate, leg1, leg2, leg3 coordinates, and
        # normal vector (n) of the cube vertex.
    """
        
    COM, lg1, lg2, lg3, n = cube_vert_input_coord(radius, sigma)
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


