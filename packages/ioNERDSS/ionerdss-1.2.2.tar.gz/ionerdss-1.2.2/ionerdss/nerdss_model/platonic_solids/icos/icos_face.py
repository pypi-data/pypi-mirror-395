from .icos_face_write import icos_face_write


def icos_face(radius: float, sigma: float):
    """Write an icosahedron face with given radius and sigma to a file.

    This function writes an icosahedron face with the given radius and sigma values
    to a file using the `icos_face_write()` function from the `icos_face_write` module.

    Args:
        radius (float): The radius of the icosahedron face.
        sigma (float): The sigma value for the icosahedron face.

    Returns:
        parm.inp/icos.mol: input files for NERDSS
    """
    icos_face_write(radius, sigma)
    print('File writing complete!')
    return 0


