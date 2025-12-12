from .cube_face_vert_coord import cube_face_vert_coord
from .cube_face_COM_coord import cube_face_COM_coord


def cube_face_COM_list_gen(radius: float):
    """Generates a list of center of mass (COM) coordinates for cube faces.

    This function generates a list of COM coordinates for the cube faces, based on the radius of the
    cube. The calculation is performed using the `cube_face_vert_coord` function from the `.cube_face_vert_coord` module
    to obtain the vertex coordinates of the cube, and the `cube_face_COM_coord` function from the `.cube_face_COM_coord`
    module to calculate the COM coordinates for each cube face.

    Args:
        radius (float): The radius of the cube.

    Returns:
        List: contains COM coordinates for all cube faces, in the following order:
        [COM_list_abcd, COM_list_adhe, COM_list_efgh, COM_list_befg, COM_list_cdgh, COM_list_aehd].

    Raises:
        None.

    Example:
        >>> cube_face_COM_list_gen(1.0)
        [[0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, 0.5]]
    """
    
    coord = cube_face_vert_coord(radius)
    COM_list = []
    COM_list.append(cube_face_COM_coord(
        coord[0], coord[3], coord[5], coord[2]))
    COM_list.append(cube_face_COM_coord(
        coord[0], coord[3], coord[6], coord[1]))
    COM_list.append(cube_face_COM_coord(
        coord[0], coord[1], coord[4], coord[2]))
    COM_list.append(cube_face_COM_coord(
        coord[7], coord[4], coord[1], coord[6]))
    COM_list.append(cube_face_COM_coord(
        coord[7], coord[4], coord[2], coord[5]))
    COM_list.append(cube_face_COM_coord(
        coord[7], coord[6], coord[3], coord[5]))
    return COM_list


