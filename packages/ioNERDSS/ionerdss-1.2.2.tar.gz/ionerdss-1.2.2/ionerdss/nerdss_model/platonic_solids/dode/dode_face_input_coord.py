from .dode_face_leg_reduce_coor_gen import dode_face_leg_reduce_coor_gen
import numpy as np

def dode_face_input_coord(radius: float, sigma: float):
    """Generates the input coordinates for a dodecahedron face based on the given radius and sigma.

    Args:
        radius (float): The radius of the dodecahedron.
        sigma (float): The sigma value for the dodecahedron face.

    Returns:
        tuple: A tuple containing the following elements:
            - COM (list): Center of Mass coordinates as a list [x, y, z], where x, y, and z are floats.
            - lg1 (list): Vector coordinates for leg 1 as a list [x, y, z], where x, y, and z are floats.
            - lg2 (list): Vector coordinates for leg 2 as a list [x, y, z], where x, y, and z are floats.
            - lg3 (list): Vector coordinates for leg 3 as a list [x, y, z], where x, y, and z are floats.
            - lg4 (list): Vector coordinates for leg 4 as a list [x, y, z], where x, y, and z are floats.
            - lg5 (list): Vector coordinates for leg 5 as a list [x, y, z], where x, y, and z are floats.
            - n (list): Normal vector coordinates as a list [x, y, z], where x, y, and z are floats.
    """

    coor = dode_face_leg_reduce_coor_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = coor_[0] - coor_[0]
    lg1 = coor_[1] - coor_[0]
    lg2 = coor_[2] - coor_[0]
    lg3 = coor_[3] - coor_[0]
    lg4 = coor_[4] - coor_[0]
    lg5 = coor_[5] - coor_[0]
    n = -coor_[0]
    return COM, lg1, lg2, lg3, lg4, lg5, n


