from .cube_face_vert_coord import cube_face_vert_coord
from .cube_face_COM_leg_coord import cube_face_COM_leg_coord


def cube_face_COM_leg_list_gen(radius: float):
    """Generates a list of center of mass (COM) coordinates for cube faces and their legs.

    This function generates a list of COM coordinates for the cube faces and their legs, based on the radius of the
    cube. The calculation is performed using the `cube_face_vert_coord` function from the `.cube_face_vert_coord` module
    to obtain the vertex coordinates of the cube, and the `cube_face_COM_leg_coord` function from the `.cube_face_COM_leg_coord`
    module to calculate the COM coordinates for each cube face and its legs.

    Args:
        radius (float): The radius of the cube.

    Returns:
        List: contains COM coordinates for all cube faces and their legs, in the following order:
        [COM_leg_list_abcd, COM_leg_list_adhe, COM_leg_list_efgh, COM_leg_list_befg, COM_leg_list_cdgh, COM_leg_list_aehd].


    Example:
        >>> cube_face_COM_leg_list_gen(1.0)
        [[0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5]]
    """
        
    coord = cube_face_vert_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(cube_face_COM_leg_coord(
        coord[0], coord[3], coord[5], coord[2]))
    COM_leg_list.append(cube_face_COM_leg_coord(
        coord[0], coord[3], coord[6], coord[1]))
    COM_leg_list.append(cube_face_COM_leg_coord(
        coord[0], coord[1], coord[4], coord[2]))
    COM_leg_list.append(cube_face_COM_leg_coord(
        coord[7], coord[4], coord[1], coord[6]))
    COM_leg_list.append(cube_face_COM_leg_coord(
        coord[7], coord[4], coord[2], coord[5]))
    COM_leg_list.append(cube_face_COM_leg_coord(
        coord[7], coord[6], coord[3], coord[5]))
    return COM_leg_list


