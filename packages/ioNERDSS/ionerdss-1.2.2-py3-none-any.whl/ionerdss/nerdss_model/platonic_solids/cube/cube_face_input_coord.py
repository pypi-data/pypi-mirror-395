from .cube_face_leg_reduce_coord_gen import cube_face_leg_reduce_coord_gen
import numpy as np

def cube_face_input_coord(radius: float, sigma: float):
    """Generates input coordinates for a cube face simulation.

    This function generates input coordinates for a cube face simulation, based on the radius and sigma values
    provided. The calculation is performed using the `cube_face_leg_reduce_coord_gen` function from the
    `.cube_face_leg_reduce_coord_gen` module to obtain reduced coordinates of the cube face, and then
    performs various calculations to derive the input coordinates.

    Args:
        radius (float): The radius of the cube.
        sigma (float): The sigma value for the simulation.

    Returns:
        List: Contains the input coordinates for the cube face simulation, in the following order:
        [COM, lg1, lg2, lg3, lg4, n], where COM is the center of mass of the cube face, lg1, lg2, lg3, and lg4 are
        the leg vectors of the cube face, and n is a vector pointing towards the center of the cube face.


    Example:
        >>> cube_face_input_coord(1.0, 0.1)
        [[0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [-0.0, -0.0, -0.0]]
    """
    
    coor = cube_face_leg_reduce_coord_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = np.around(coor_[0] - coor_[0], 7)
    lg1 = coor_[1] - coor_[0]
    lg2 = coor_[2] - coor_[0]
    lg3 = coor_[3] - coor_[0]
    lg4 = coor_[4] - coor_[0]
    n = -coor_[0]
    return [COM, lg1, lg2, lg3, lg4, n]


