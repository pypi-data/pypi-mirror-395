from .octa_vert_write import octa_vert_write


def octa_vert(radius: float, sigma: float):
    """
    Writes octagonal vertices to a file.

    Args:
        radius (float): The radius of the octagon.
        sigma (float): The standard deviation for the Gaussian distribution.

    Returns:
        parm.inp/icos.mol: input files for NERDSS

    Example:
        octa_vert(5.0, 1.0)
    """
    octa_vert_write(radius, sigma)
    print('File writing complete!')
    return 0


