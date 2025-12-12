from .tetr_vert_COM_leg_gen import tetr_vert_COM_leg_gen
from .tetr_vert_leg_reduce import tetr_vert_leg_reduce

def tetr_vert_leg_reduce_coor_gen(radius: float, sigma: float):
    """Generate the reduced leg coordinates of a regular tetrahedron given the radius and sigma.

    Args:
        radius (float): The radius of the circumsphere of the tetrahedron.
        sigma (float): The scaling factor for reducing the length of the legs.

    Returns:
        list: A list of lists containing the coordinates of the center of mass (COM) and the reduced leg vectors
        of the tetrahedron, for each of the four vertices.
    """
    # Generating all the coords of COM and legs when sigma exists
    COM_leg_list = tetr_vert_COM_leg_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 3:
            temp_list.append(tetr_vert_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


