from .tetr_vert_write import tetr_vert_write


def tetr_vert(radius: float, sigma: float):
    """Writes tetrahedron vertices to a file.
    
    Args:
        radius (float): The radius of the tetrahedron's circumsphere.
        sigma (float): The height of the tetrahedron.
        
    Returns:
        parm.inp/icos.mol: input files for NERDSS
                
    Example:
        >>> tetr_vert(1.0, 0.5)
        File writing complete!
    """
    tetr_vert_write(radius, sigma)
    print('File writing complete!')
    return 0


