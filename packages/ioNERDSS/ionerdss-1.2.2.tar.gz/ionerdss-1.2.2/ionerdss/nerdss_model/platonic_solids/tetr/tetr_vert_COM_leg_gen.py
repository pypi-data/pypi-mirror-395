from .tetr_vert_coord import tetr_vert_coord
from .tetr_vert_COM_leg import tetr_vert_COM_leg

def tetr_vert_COM_leg_gen(radius: float):
    """Generates the center of mass (COM) and midpoints of three edges of a tetrahedron for all possible combinations
    of vertices.
    
    Args:
        radius (float): The radius of the tetrahedron's circumsphere.
        
    Returns:
        list: A list of four COM_leg lists for each vertex combination, where each COM_leg list contains four values,
        [COM, lega, legb, legc], rounded to 10 decimal places.
    """
    coord = tetr_vert_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(tetr_vert_COM_leg(
        coord[0], coord[1], coord[2], coord[3]))
    COM_leg_list.append(tetr_vert_COM_leg(
        coord[1], coord[2], coord[3], coord[0]))
    COM_leg_list.append(tetr_vert_COM_leg(
        coord[2], coord[3], coord[0], coord[1]))
    COM_leg_list.append(tetr_vert_COM_leg(
        coord[3], coord[0], coord[1], coord[2]))
    return COM_leg_list


