import math


def icos_face_vert_coord(radius: float):
    """Generates the vertex coordinates of an icosahedron face.

    Args:
        radius (float): Radius of the icosahedron.

    Returns:
        list: A list of vertex coordinates of the icosahedron face.

    Example:
        >>> icos_face_vert_coord(1.0)
        [[v0_x, v0_y, v0_z],
         [v1_x, v1_y, v1_z],
         ...
        ]
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


