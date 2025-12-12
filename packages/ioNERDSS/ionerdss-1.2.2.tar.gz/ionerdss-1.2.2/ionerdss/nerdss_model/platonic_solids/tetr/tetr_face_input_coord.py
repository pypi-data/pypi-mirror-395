from .tetr_face_leg_reduce_coord_gen import tetr_face_leg_reduce_coord_gen
import numpy as np

def tetr_face_input_coord(radius: float, sigma: float):
    """"Generates input coordinates for a tetrahedral face given the radius of its circumscribed sphere
    and a scaling factor sigma.

    Args:
        radius (float): The radius of the circumscribed sphere of the tetrahedron.
        sigma (float): A scaling factor for reducing the coordinates of the tetrahedral face.

    Returns:
        list: A list of input coordinates for the tetrahedral face. The list contains 5 sub-lists,
        each representing the coordinates of one input vector. Each sub-list contains 3 floats
        representing the x, y, and z coordinates of the vector.

    Example:
        >>> tetr_face_input_coord(1.0, 0.5)
        [[0.0, 0.0, 0.0], [-0.5, 0.0, 0.0], [0.0, -0.5, 0.0], [0.0, 0.0, -0.5], [0.0, 0.0, 0.0]]
    """
    coor = tetr_face_leg_reduce_coord_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = coor_[0] - coor_[0]
    lg1 = coor_[1] - coor_[0]
    lg2 = coor_[2] - coor_[0]
    lg3 = coor_[3] - coor_[0]
    n = -coor_[0]
    return [COM, lg1, lg2, lg3, n]


