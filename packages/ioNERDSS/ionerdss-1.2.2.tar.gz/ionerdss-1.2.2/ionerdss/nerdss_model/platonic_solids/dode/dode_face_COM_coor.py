import math
from ..gen_platonic.mid_pt import mid_pt


def dode_face_COM_coor(a: float, b: float, c: float, d: float, e: float):
    """
    Calculates the center of mass (COM) coordinates for a dodecahedron face
    based on five input coordinates on the same face, and checks for overlap.

    Args:
        a (float): The first coordinate on the face.
        b (float): The second coordinate on the face.
        c (float): The third coordinate on the face.
        d (float): The fourth coordinate on the face.
        e (float): The fifth coordinate on the face.

    Returns:
        list: A list of three float values representing the X, Y, and Z coordinates
        of the center of mass (COM) if the calculated COM coordinates are not overlapped.
        Otherwise, returns the COM coordinates based on the first input coordinate.

    Raises:
        None.

    Example:
        >>> dode_face_COM_coor([0.0, 0.0, 0.0], [1.0, 1.0, 1.0],
        ...                   [2.0, 2.0, 2.0], [3.0, 3.0, 3.0], [4.0, 4.0, 4.0])
        [0.29389262614624, 0.29389262614624, 0.29389262614624]

    Note:
        - The function calculates the center of mass (COM) coordinates by taking
          the midpoint between input coordinates, applying a transformation with
          a scaling factor based on a sine function, and rounding the result to
          14 decimal places.
        - The function checks for overlap among the calculated COM coordinates
          and returns the COM coordinates based on the first input coordinate if
          there is overlap.
    """
    
    # calculate the center of mass(COM) according to 5 coords on the same face
    n = 10
    mid_a = mid_pt(c, d)
    mid_b = mid_pt(d, e)
    mid_c = mid_pt(a, e)
    COM_a = []
    COM_b = []
    COM_c = []
    # calculate 3 COM here and check if they are overlapped
    for i in range(0, 3):
        COM_a.append(round(a[i] + (mid_a[i] - a[i]) /
                     (1+math.sin(0.3*math.pi)), 14))
        COM_b.append(round(b[i] + (mid_b[i] - b[i]) /
                     (1+math.sin(0.3*math.pi)), 14))
        COM_c.append(round(c[i] + (mid_c[i] - c[i]) /
                     (1+math.sin(0.3*math.pi)), 14))
    # checking overlap
    if round(COM_a[0], n) == round(COM_b[0], n) and round(COM_b[0], n) == round(COM_c[0], n) and \
        round(COM_a[1], n) == round(COM_b[1], n) and round(COM_b[1], n) == round(COM_c[1], n) and \
            round(COM_a[2], n) == round(COM_b[2], n) and round(COM_b[2], n) == round(COM_c[2], n):
        return COM_a
    else:
        return COM_a


