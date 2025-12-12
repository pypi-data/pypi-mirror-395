from ..gen_platonic.mid_pt import mid_pt
from .dode_face_COM_coor import dode_face_COM_coor


def dode_face_COM_leg_coor(a: float, b: float, c: float, d: float, e: float):
    """Calculates the center of mass (COM) and the coordinates of the five legs
    of a protein based on five input coordinates on the same face of a dodecahedron.

    Args:
        a (float): The first coordinate on the face.
        b (float): The second coordinate on the face.
        c (float): The third coordinate on the face.
        d (float): The fourth coordinate on the face.
        e (float): The fifth coordinate on the face.

    Returns:
        list: A list of six lists, where the first element is a list of three
        float values representing the X, Y, and Z coordinates of the center of mass (COM),
        and the remaining five elements represent the coordinates of the five legs of
        the protein, calculated as midpoints between the input coordinates.

    Raises:
        None.

    Example:
        >>> dode_face_COM_leg_coor([0.0, 0.0, 0.0], [1.0, 1.0, 1.0],
        ...                        [2.0, 2.0, 2.0], [3.0, 3.0, 3.0], [4.0, 4.0, 4.0])
        [[0.29389262614624, 0.29389262614624, 0.29389262614624],
         [0.5, 0.5, 0.5],
         [1.5, 1.5, 1.5],
         [2.5, 2.5, 2.5],
         [3.5, 3.5, 3.5],
         [4.0, 4.0, 4.0]]

    Note:
        - The function returns a list of six lists, where the first element is the
          COM coordinates and the remaining five elements represent the coordinates
          of the five legs of the protein.
    """
    
    # calculate COM and 5 legs of one protein, 6 coords in total [COM, lg1, lg2, lg3, lg4, lg5]
    COM_leg = []
    COM_leg.append(dode_face_COM_coor(a, b, c, d, e))
    COM_leg.append(mid_pt(a, b))
    COM_leg.append(mid_pt(b, c))
    COM_leg.append(mid_pt(c, d))
    COM_leg.append(mid_pt(d, e))
    COM_leg.append(mid_pt(e, a))
    return COM_leg


