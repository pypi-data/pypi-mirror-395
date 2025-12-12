from .tetr_face_write import tetr_face_write


def tetr_face(radius: float, sigma: float):
    """Draws a tetrahedron face with the given radius and sigma.

    Args:
        radius (float): The radius of the tetrahedron.
        sigma (float): The sigma value for drawing the tetrahedron face.

    Returns:
        parm.inp/icos.mol: input files for NERDSS

    Examples:
        >>> tetr_face(1.0, 0.5)
        File writing complete!

    Note:
        This function relies on the 'tetr_face_write' function from the '.tetr_face_write' module.
        The 'tetr_face_write' function is responsible for writing the tetrahedron face to a file.
    """
    tetr_face_write(radius, sigma)
    print('File writing complete!')
    return 0


