from .dode_face_COM_leg_list_gen import dode_face_COM_leg_list_gen
from .dode_face_leg_reduce import dode_face_leg_reduce


def dode_face_leg_reduce_coor_gen(radius: float, sigma: float):
    """Generates the reduced coordinates for the center of mass (COM) and legs of a dodecahedron face
    based on the given radius and sigma.

    Args:
        radius (float): The radius of the dodecahedron.
        sigma (float): The sigma value for the dodecahedron face.

    Returns:
        list: A list of lists containing the reduced coordinates for the COM and legs of each dodecahedron face.
        Each element in the outer list represents a dodecahedron face, and contains a list with the following elements:
            - COM (list): Center of Mass coordinates as a list [x, y, z], where x, y, and z are floats.
            - leg1 (list): Vector coordinates for leg 1 after reduction as a list [x, y, z], where x, y, and z are floats.
            - leg2 (list): Vector coordinates for leg 2 after reduction as a list [x, y, z], where x, y, and z are floats.
            - leg3 (list): Vector coordinates for leg 3 after reduction as a list [x, y, z], where x, y, and z are floats.
            - leg4 (list): Vector coordinates for leg 4 after reduction as a list [x, y, z], where x, y, and z are floats.
            - leg5 (list): Vector coordinates for leg 5 after reduction as a list [x, y, z], where x, y, and z are floats.
    """

    # Generating all the coords of COM and legs when sigma exists
    COM_leg_list = dode_face_COM_leg_list_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 5:
            temp_list.append(dode_face_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


