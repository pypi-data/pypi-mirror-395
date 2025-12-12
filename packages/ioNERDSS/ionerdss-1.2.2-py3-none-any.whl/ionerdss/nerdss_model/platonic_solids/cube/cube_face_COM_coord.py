from ..gen_platonic.mid_pt import mid_pt


def cube_face_COM_coord(a: float, b: float, c: float, d: float):
    """Calculates the center of mass (COM) coordinate for a cube face.

    This function calculates the COM coordinate for a cube face defined by four input points (a, b, c, d), where a, b, c,
    and d are the coordinates of the vertices of the cube face. The calculation is based on the mid-point coordinates
    of the input points, as well as the mid-point coordinates of the pairs of input points. The `mid_pt` function from
    the `..gen_platonic.mid_pt` module is used for the mid-point calculations.

    Args:
        a (float): The x-coordinate of the first vertex of the cube face.
        b (float): The x-coordinate of the second vertex of the cube face.
        c (float): The x-coordinate of the third vertex of the cube face.
        d (float): The x-coordinate of the fourth vertex of the cube face.

    Returns:
        Float: The x-coordinate of the calculated COM coordinate of the cube face.

    Example:
        >>> cube_face_COM_coord(0.0, 1.0, 1.0, 0.0)
        0.5
    """
    mid_a = mid_pt(a, b)
    mid_b = mid_pt(b, c)
    mid_c = mid_pt(c, d)
    mid_d = mid_pt(d, a)
    COM_a = mid_pt(mid_a, mid_c)
    COM_b = mid_pt(mid_b, mid_d)
    if COM_a == COM_b:
        return COM_a
    else:
        return COM_a


