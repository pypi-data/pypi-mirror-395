from .cube_vert_coord import cube_vert_coord
from .cube_vert_COM_leg import cube_vert_COM_leg

def cube_vert_COM_leg_gen(radius: float):
    """Generates a list of midpoints of line segments between a central point and other points on a cube.

    This function calculates the midpoints of line segments between a central point and other points on a cube, based on the given
    radius.

    Args:
        radius (float): The radius of the cube.

    Returns:
        list: A list containing eight sub-lists, each containing four floating-point values rounded to 10 decimal places,
        representing the central point and the midpoints of line segments between the central point and other points on the cube.

    Example:
        cube_vert_COM_leg_gen(1.0)
        # Generates a list of midpoints of line segments between the central point and other points on a cube with a radius of 1.0.
        # The list contains eight sub-lists, each containing four floating-point values rounded to 10 decimal places.
    """

    coord = cube_vert_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(cube_vert_COM_leg(
        coord[0], coord[1], coord[2], coord[3]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[1], coord[0], coord[4], coord[6]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[2], coord[0], coord[4], coord[5]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[3], coord[0], coord[5], coord[6]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[4], coord[1], coord[2], coord[7]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[5], coord[2], coord[3], coord[7]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[6], coord[1], coord[3], coord[7]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[7], coord[4], coord[5], coord[6]))
    return COM_leg_list


