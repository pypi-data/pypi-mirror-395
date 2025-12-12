from .tetr_face_COM_leg_list_gen import tetr_face_COM_leg_list_gen
from .tetr_face_leg_reduce import tetr_face_leg_reduce

def tetr_face_leg_reduce_coord_gen(radius: float, sigma: float):
    """Generates a list of reduced coordinates for the center of mass (COM) and legs of a tetrahedron face given the
    radius of the tetrahedron and a scaling factor sigma.

    Args:
        radius (float): The radius of the tetrahedron.
        sigma (float): A scaling factor for reducing the length of the legs.

    Returns:
        list: A list of lists, where each inner list contains the reduced coordinates of the COM and legs of a tetrahedron
        face. The inner list has 4 elements, where the first element is the reduced coordinates of the COM, and the
        remaining 3 elements are lists of 3 floats each representing the reduced coordinates of the legs.

    Example:
        >>> tetr_face_leg_reduce_coord_gen(1.0, 0.5)
        [[[0.0, 0.0, 0.0], [-0.25, 0.0, 0.0], [0.0, 0.25, 0.0], [0.0, 0.0, 0.25]],
         [[0.0, 0.0, 0.0], [-0.25, 0.0, 0.0], [0.0, -0.25, 0.0], [0.0, 0.0, -0.25]],
         [[0.0, 0.0, 0.0], [0.25, 0.0, 0.0], [0.0, 0.25, 0.0], [0.0, 0.0, -0.25]],
         [[0.0, 0.0, 0.0], [0.25, 0.0, 0.0], [0.0, -0.25, 0.0], [0.0, 0.0, 0.25]]]

    """
    COM_leg_list = tetr_face_COM_leg_list_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 3:
            temp_list.append(tetr_face_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


