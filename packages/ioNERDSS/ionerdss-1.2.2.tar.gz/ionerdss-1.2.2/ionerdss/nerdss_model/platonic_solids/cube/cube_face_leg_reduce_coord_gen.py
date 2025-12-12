import numpy as np
from ..gen_platonic.COM_leg_list_gen import COM_leg_list_gen
from .cube_face_COM_leg_list_gen import cube_face_COM_leg_list_gen
from .cube_face_leg_reduce import cube_face_leg_reduce

def cube_face_leg_reduce_coord_gen(radius: float, sigma: float):
    """Generates a list of reduced center of mass and leg vectors for cube faces.

    This function takes the radius and sigma value as inputs, and generates a list of reduced center of mass (COM) and leg
    vectors for the cube faces of a platonic solid. The reduction is performed using the 'cube_face_leg_reduce' function
    from the 'cube_face_leg_reduce' module, and the original COM and leg vectors are obtained from the 'cube_face_COM_leg_list_gen'
    and 'cube_face_COM_leg_list_gen' functions respectively.

    Args:
        radius (float): The radius of the platonic solid.
        sigma (float): The sigma value for the reduction.

    Returns:
        List: Contains reduced COM and leg vectors for the cube faces. Each element in the list is a sublist containing the reduced
        COM vector followed by the reduced leg vectors for each face. The coordinates in the vectors are rounded to 8 decimal places.

    Raises:
        None.

    Example:
        >>> cube_face_leg_reduce_coord_gen(1.0, 0.1)
        [[0.0, [0.131826, 0.131826, 0.131826], [0.131826, 0.131826, -0.131826], [-0.131826, 0.131826, -0.131826], [-0.131826, 0.131826, 0.131826]],
         [0.0, [-0.131826, 0.131826, 0.131826], [-0.131826, -0.131826, 0.131826], [-0.131826, -0.131826, -0.131826], [-0.131826, 0.131826, -0.131826]],
         ...
        ]

    """
    COM_leg_list = cube_face_COM_leg_list_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(np.around(elements[0], 8))
        i = 1
        while i <= 4:
            temp_list.append(np.around(cube_face_leg_reduce(
                elements[0], elements[i], sigma), 8))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


