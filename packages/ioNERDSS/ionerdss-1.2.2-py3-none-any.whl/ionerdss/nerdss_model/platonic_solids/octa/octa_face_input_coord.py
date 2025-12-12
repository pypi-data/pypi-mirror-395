from .octa_face_leg_reduce_coord_gen import octa_face_leg_reduce_coord_gen
import numpy as np

def octa_face_input_coord(radius: float, sigma: float):
    """Generates input coordinates for an octahedron face reduction algorithm.

    Args:
        radius (float): The radius of the octahedron.
        sigma (float): The sigma value for the reduction algorithm.

    Returns:
        List: A list of input coordinates for the octahedron face reduction algorithm.
            The list contains the following:
            - COM (numpy.array): The center of mass (COM) coordinates for the octahedron face.
            - lg1 (numpy.array): The first leg vector from COM to vertex 1.
            - lg2 (numpy.array): The second leg vector from COM to vertex 2.
            - lg3 (numpy.array): The third leg vector from COM to vertex 3.
            - n (numpy.array): The normal vector of the octahedron face.

    Example:
        radius = 1.0
        sigma = 0.5
        input_coord = octa_face_input_coord(radius, sigma)
        print(input_coord)

    Note:
        The octahedron is assumed to be centered at the origin (0,0,0) and aligned with the
        coordinate axes. The function uses the octa_face_leg_reduce_coord_gen() function to generate
        the input coordinates for the face reduction algorithm. The input coordinates include the
        center of mass (COM) coordinates, leg vectors, and normal vector of the octahedron face.
    """

    coor = octa_face_leg_reduce_coord_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = coor_[0] - coor_[0]
    lg1 = coor_[1] - coor_[0]
    lg2 = coor_[2] - coor_[0]
    lg3 = coor_[3] - coor_[0]
    n = -coor_[0]
    return [COM, lg1, lg2, lg3, n]


