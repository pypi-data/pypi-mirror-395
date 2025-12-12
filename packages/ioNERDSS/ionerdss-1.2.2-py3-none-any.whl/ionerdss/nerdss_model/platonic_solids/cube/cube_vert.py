from .cube_vert_write import cube_vert_write


def cube_vert(radius: float, sigma: float):
    """Generates a cube mesh with vertex data and writes it to a file.

    Args:
        radius (float): The radius of the cube.
        sigma (float): The sigma value for vertex generation.

    Returns:
        parm.inp/cube.mol file: inputs for NERDSS

    Example:
        cube_vert(1.0, 0.1)  # Generates a cube mesh with radius 1.0 and sigma 0.1,
                             # writes it to a file, and returns 0.
    """
        
    cube_vert_write(radius, sigma)
    print('File writing complete!')
    return 0


