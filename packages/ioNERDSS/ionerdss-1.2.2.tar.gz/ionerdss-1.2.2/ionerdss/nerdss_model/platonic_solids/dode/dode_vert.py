from .dode_vert_write import dode_vert_write


def dode_vert(radius: float, sigma: float):
    """
    Generates and writes vertex coordinates for a dodecahedron to a file.

    Args:
        radius (float): Radius of the dodecahedron.
        sigma (float): Sigma value for generating vertex coordinates.

    Returns:
        parm.inp/cube.mol file: inputs for NERDSS
    """
    
    dode_vert_write(radius, sigma)
    print('File writing complete!')
    return 0


