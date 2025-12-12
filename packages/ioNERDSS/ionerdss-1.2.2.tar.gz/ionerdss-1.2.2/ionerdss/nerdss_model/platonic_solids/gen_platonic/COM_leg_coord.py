from .mid_pt import mid_pt
from .face_COM_coord import face_COM_coord


def COM_leg_coord(a: float, b: float, c: float):
    """Calculate the center of mass (COM) leg coordinates for an icosahedron face.

    This function calculates the center of mass (COM) leg coordinates for an icosahedron face
    with three given coordinates `a`, `b`, and `c` using the `icos_face_COM_coord()` and `mid_pt()`
    functions from the `icos_face_COM_coord` and `mid_pt` modules respectively. The COM leg coordinates
    are calculated as follows:
    - The COM of the face using `icos_face_COM_coord()` function
    - The mid-point of each pair of vertices using `mid_pt()` function

    Args:
        a (float): The first coordinate of the icosahedron face.
        b (float): The second coordinate of the icosahedron face.
        c (float): The third coordinate of the icosahedron face.

    Returns:
        List[list[float]]: The center of mass (COM) leg coordinates as a list of lists of three floats.
            The list has four sub-lists, each containing the COM leg coordinates for a pair of vertices.

    Examples:
        >>> a = [0, 0, 0]
        >>> b = [1, 1, 1]
        >>> c = [2, 2, 2]
        >>> icos_face_COM_leg_coord(a, b, c)
        [[1.3660254037847, 1.3660254037847, 1.3660254037847],
         [0.5, 0.5, 0.5],
         [1.5, 1.5, 1.5],
         [1.0, 1.0, 1.0]]

    Notes:
        - The COM leg coordinates are calculated using the `icos_face_COM_coord()` function for the face
          and `mid_pt()` function for the mid-points of pairs of vertices.
        - The calculated COM leg coordinates are returned as a list of lists, where each sub-list contains
          three floats representing the COM leg coordinates for a pair of vertices.
    """
    COM_leg = []
    COM_leg.append(face_COM_coord(a, b, c))
    COM_leg.append(mid_pt(a, b))
    COM_leg.append(mid_pt(b, c))
    COM_leg.append(mid_pt(c, a))
    return COM_leg


