from ..gen_platonic.COM_leg_list_gen import COM_leg_list_gen
from .octa_face_COM_leg_list_gen import octa_face_COM_leg_list_gen
from .octa_face_leg_reduce import octa_face_leg_reduce

def octa_face_leg_reduce_coord_gen(radius: float, sigma: float):
    """Generates a list of reduced center of mass (COM) and leg coordinates of an octahedron face
    based on the given radius and reduction factor sigma.

    Args:
        radius (float): The radius of the octahedron.
        sigma (float): The reduction factor for the leg length.

    Returns:
        List[List[float]]: A list of reduced center of mass (COM) and leg coordinates for each
            octahedron face. Each element in the list is a sublist containing four floating point
            values: [COM, leg1_red, leg2_red, leg3_red]. The COM is the center of mass coordinate
            of the octahedron face, and leg1_red, leg2_red, leg3_red are the reduced leg coordinates
            after applying the reduction factor.

    Example:
        radius = 5.0
        sigma = 0.5
        COM_leg_red_list = octa_face_leg_reduce_coord_gen(radius, sigma)
        print(COM_leg_red_list)

    Note:
        The function uses other functions from the 'gen_platonic' and 'octa_face_leg_reduce' modules
        to generate the list of center of mass (COM) and leg coordinates, and then apply the reduction
        factor to the leg coordinates. The resulting reduced COM and leg coordinates are returned as a
        list of lists, where each sublist contains the COM and reduced leg coordinates for a specific
        octahedron face.
    """
    COM_leg_list = octa_face_COM_leg_list_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 3:
            temp_list.append(octa_face_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


