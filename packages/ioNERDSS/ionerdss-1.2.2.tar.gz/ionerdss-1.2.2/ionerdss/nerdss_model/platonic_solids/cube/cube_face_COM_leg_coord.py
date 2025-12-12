from ..gen_platonic.mid_pt import mid_pt
from .cube_face_COM_coord import cube_face_COM_coord


def cube_face_COM_leg_coord(a: float, b: float, c: float, d: float):
    """Calculates the center of mass (COM) coordinates for a cube face and its legs.

    This function calculates the COM coordinates for a cube face and its legs, based on four input points (a, b, c, d),
    where a, b, c, and d are the coordinates of the vertices of the cube face. The calculation is performed using the
    `cube_face_COM_coord` function from the `.cube_face_COM_coord` module and the `mid_pt` function from the
    `..gen_platonic.mid_pt` module.

    Args:
        a (float): The x-coordinate of the first vertex of the cube face.
        b (float): The x-coordinate of the second vertex of the cube face.
        c (float): The x-coordinate of the third vertex of the cube face.
        d (float): The x-coordinate of the fourth vertex of the cube face.

    Returns:
        List: he COM coordinates for the cube face and its legs, in the following order:
        [COM_face, COM_leg_ab, COM_leg_bc, COM_leg_cd, COM_leg_da].

    Example:
        >>> cube_face_COM_leg_coord(0.0, 1.0, 1.0, 0.0)
        [0.5, 0.5, 0.5, 0.5, 0.5]
    """
    COM_leg = []
    COM_leg.append(cube_face_COM_coord(a, b, c, d))
    COM_leg.append(mid_pt(a, b))
    COM_leg.append(mid_pt(b, c))
    COM_leg.append(mid_pt(c, d))
    COM_leg.append(mid_pt(d, a))
    return COM_leg


