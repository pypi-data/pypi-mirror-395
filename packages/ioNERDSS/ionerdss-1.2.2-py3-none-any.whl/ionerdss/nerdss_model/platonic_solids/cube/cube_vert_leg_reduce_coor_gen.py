from .cube_vert_COM_leg_gen import cube_vert_COM_leg_gen
from .cube_vert_leg_reduce import cube_vert_leg_reduce

def cube_vert_leg_reduce_coor_gen(radius: float, sigma: float):
    """Generates a list of reduced center of mass (COM) and leg coordinates for a cube vertex based on radius and sigma.

    This function generates a list of reduced center of mass (COM) and leg coordinates for a cube vertex based on the
    given radius and sigma values, using the `cube_vert_COM_leg_gen` and `cube_vert_leg_reduce` functions from the
    respective modules. The reduction is applied to each leg coordinate by calling the `cube_vert_leg_reduce` function
    with the appropriate arguments.

    Args:
        radius (float): The radius of the cube vertex, represented as a float value.
        sigma (float): The sigma value for the cube vertex, used to calculate the reduction ratio, represented as a float value.

    Returns:
        list: A list of lists, where each inner list contains four elements: the reduced center of mass (COM) coordinate
        and the reduced leg coordinates (leg1, leg2, and leg3) of a cube vertex, after applying the reduction ratio
        based on the given radius and sigma values.


    Example:
        cube_vert_leg_reduce_coor_gen(1.0, 0.2)
        # Generates a list of reduced center of mass (COM) and leg coordinates for a cube vertex with a radius of 1.0 and
        # a sigma value of 0.2.
        # Returns a list of lists, where each inner list contains four elements: the reduced center of mass (COM) coordinate
        # and the reduced leg coordinates (leg1, leg2, and leg3) of a cube vertex, after applying the reduction ratio
        # based on the given radius and sigma values.
    """
    
    COM_leg_list = cube_vert_COM_leg_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 3:
            temp_list.append(cube_vert_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


