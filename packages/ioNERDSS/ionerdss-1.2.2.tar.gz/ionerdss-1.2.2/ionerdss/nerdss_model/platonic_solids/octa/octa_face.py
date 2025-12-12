from .octa_face_write import octa_face_write


def octa_face(radius: float, sigma: float):
    """Generate an octagonal face image.

    Args:
        radius (float): The radius of the octagonal face.
        sigma (float): The sigma value for generating the face.

    Returns:
        parm.inp/icos.mol: input files for NERDSS

    Raises:
        ValueError: If radius or sigma are not valid (e.g., negative values).

    Example:
        To generate an octagonal face with a radius of 10 and a sigma of 1.5:
        >>> octa_face(10, 1.5)
        File writing complete!
    """
    octa_face_write(radius, sigma)
    print('File writing complete!')
    return 0


