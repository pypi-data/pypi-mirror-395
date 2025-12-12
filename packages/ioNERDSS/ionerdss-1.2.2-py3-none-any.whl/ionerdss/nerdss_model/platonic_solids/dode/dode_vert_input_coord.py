from .dode_vert_leg_reduce_coor_gen import dode_vert_leg_reduce_coor_gen
import numpy as np

def dode_vert_input_coord(radius: float, sigma: float):
    """Generates input coordinates for a dodecahedron vertex.

    This function generates input coordinates for a dodecahedron vertex, given the radius and sigma values. The input
    coordinates are calculated based on the radius and sigma values using the dode_vert_leg_reduce_coor_gen function
    from the .dode_vert_leg_reduce_coor_gen module.

    Args:
        radius (float): The radius of the dodecahedron vertex.
        sigma (float): The sigma value for the dodecahedron vertex.

    Returns:
        tuple: A tuple containing the following five numpy arrays:
            - COM: The center of mass (COM) of the dodecahedron vertex.
            - lg1: The first leg vector of the dodecahedron vertex.
            - lg2: The second leg vector of the dodecahedron vertex.
            - lg3: The third leg vector of the dodecahedron vertex.
            - n: The normalized vector of the dodecahedron vertex.
    """
    
    coor = dode_vert_leg_reduce_coor_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = np.around(coor_[0] - coor_[0], 12)
    lg1 = np.around(coor_[1] - coor_[0], 12)
    lg2 = np.around(coor_[2] - coor_[0], 12)
    lg3 = np.around(coor_[3] - coor_[0], 12)
    n = np.around(coor_[0]/np.linalg.norm(coor_[0]), 12)
    return COM, lg1, lg2, lg3, n


