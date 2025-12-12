from .cube_vert_leg_reduce_coor_gen import cube_vert_leg_reduce_coor_gen
import numpy as np

def cube_vert_input_coord(radius: float, sigma: float):
    """Calculates input coordinates for a cube vertex based on the given radius and sigma.

    This function calculates the input coordinates for a cube vertex based on the given radius and sigma, using the
    `cube_vert_leg_reduce_coor_gen` function to generate the coordinates and then performing various calculations on the
    generated coordinates using NumPy.

    Args:
        radius (float): The radius of the cube.
        sigma (float): The sigma value for the cube vertex.

    Returns:
        tuple: A tuple containing five NumPy arrays, each containing three floating-point values representing the x, y,
        and z coordinates of the input coordinates for the cube vertex. The first array represents the center of mass (COM)
        coordinate, the next three arrays represent the three leg coordinates (lg1, lg2, lg3), and the last array
        represents the normalized vector (n) coordinate.


    Example:
        cube_vert_input_coord(1.0, 0.5)
        # Calculates the input coordinates for a cube vertex with a radius of 1.0 and a sigma value of 0.5.
        # Returns a tuple containing five NumPy arrays, each containing three floating-point values representing the x, y,
        # and z coordinates of the input coordinates for the cube vertex.
    """
        
    coor = cube_vert_leg_reduce_coor_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = np.around(coor_[0] - coor_[0], 8)
    lg1 = np.around(coor_[1] - coor_[0], 8)
    lg2 = np.around(coor_[2] - coor_[0], 8)
    lg3 = np.around(coor_[3] - coor_[0], 8)
    n = np.around(coor_[0]/np.linalg.norm(coor_[0]), 8)
    return COM, lg1, lg2, lg3, n


