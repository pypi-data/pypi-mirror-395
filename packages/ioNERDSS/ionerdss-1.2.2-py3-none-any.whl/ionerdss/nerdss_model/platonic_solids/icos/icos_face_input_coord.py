from .icos_face_leg_reduce_coord_gen import icos_face_leg_reduce_coord_gen
import numpy as np

def icos_face_input_coord(radius: float, sigma: float):
    """Generates input coordinates for an icosahedron face.

    Args:
        radius (float): Radius of the icosahedron.
        sigma (float): Sigma value for leg reduction.

    Returns:
        list: A list of coordinates including Center of Mass (COM), leg1 vector, leg2 vector,
        leg3 vector, and negative of COM.

    Example:
        >>> icos_face_input_coord(1.0, 0.5)
        [COM, lg1, lg2, lg3, n]
    """
    coor = icos_face_leg_reduce_coord_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = coor_[0] - coor_[0]
    lg1 = coor_[1] - coor_[0]
    lg2 = coor_[2] - coor_[0]
    lg3 = coor_[3] - coor_[0]
    n = -coor_[0]
    return [COM, lg1, lg2, lg3, n]


