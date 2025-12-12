import math


def icos_vert_coord(radius: float):
    """Generate vertex coordinates for an icosahedron with the given radius.

    The function calculates the vertex coordinates for an icosahedron with the given radius,
    using mathematical formulas and scaling based on the radius.

    Args:
        radius (float): The radius of the icosahedron.

    Returns:
        list: A list of vertex coordinates for the icosahedron.
    """
    scaler = radius/(2*math.sin(2*math.pi/5))
    m = (1+5**0.5)/2
    v0 = [0, 1, m]
    v1 = [0, 1, -m]
    v2 = [0, -1, m]
    v3 = [0, -1, -m]
    v4 = [1, m, 0]
    v5 = [1, -m, 0]
    v6 = [-1, m, 0]
    v7 = [-1, -m, 0]
    v8 = [m, 0, 1]
    v9 = [m, 0, -1]
    v10 = [-m, 0, 1]
    v11 = [-m, 0, -1]
    VertCoord = [v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11]
    VertCoord_ = []
    for i in VertCoord:
        temp_list = []
        for j in i:
            temp = j*scaler
            temp_list.append(temp)
        VertCoord_.append(temp_list)
    return VertCoord_


