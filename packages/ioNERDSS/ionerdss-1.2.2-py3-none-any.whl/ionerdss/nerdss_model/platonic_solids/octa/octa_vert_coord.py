def octa_vert_coord(radius: float):
    """Calculates the vertex coordinates of an octagon centered at the origin.
    The vertex coordinates are scaled by the given radius.

    Args:
        radius (float): The radius of the octagon.

    Returns:
        list: A list of 6 vertex coordinates, each represented as a list of 3D coordinates [x, y, z].
        The coordinates are scaled by the given radius.

    Example:
        radius = 2.0
        result = octa_vert_coord(radius)
        print(result)
    """
    
    scaler = radius
    v0 = [1, 0, 0]
    v1 = [-1, 0, 0]
    v2 = [0, 1, 0]
    v3 = [0, -1, 0]
    v4 = [0, 0, 1]
    v5 = [0, 0, -1]
    VertCoord = [v0, v1, v2, v3, v4, v5]
    VertCoord_ = []
    for i in VertCoord:
        temp_list = []
        for j in i:
            temp = j*scaler
            temp_list.append(temp)
        VertCoord_.append(temp_list)
    return VertCoord_


