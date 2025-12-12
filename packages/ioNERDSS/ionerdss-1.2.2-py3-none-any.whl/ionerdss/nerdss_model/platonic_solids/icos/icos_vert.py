from .icos_vert_write import icos_vert_write


def icos_vert(radius: float, sigma: float):
    """Generate vertices for an icosahedron and write to a file.

    This function generates the vertices of an icosahedron with the given
    radius and sigma, and writes them to a file using the icos_vert_write
    function from the .icos_vert_write module. After writing is complete,
    it prints a message indicating the file writing status.

    Args:
        radius (float): The radius of the icosahedron.
        sigma (float): The sigma value used in the generation of vertices.

    Returns:
        parm.inp/icos.mol: input files for NERDSS

    Example:
        >>> icos_vert(2.0, 0.5)
        File writing complete!
    """
    icos_vert_write(radius, sigma)
    print('File writing complete!')
    return 0


# -----------------------------------Data Visualization------------------------------

# Analysis tools for 'histogram_complexes_time.dat' file


