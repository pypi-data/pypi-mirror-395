def cube_vert_coord(radius: float):
    """Calculates the coordinates of the vertices of a cube based on the given radius.

    This function calculates the coordinates of the vertices of a cube based on the given radius, using a scaling factor
    calculated as radius divided by the square root of 3.

    Args:
        radius (float): The radius of the cube.

    Returns:
        list: A list containing eight sub-lists, each containing three floating-point values representing the x, y, and z
        coordinates of a vertex of the cube.

    Example:
        cube_vert_coord(1.0)
        # Calculates the coordinates of the vertices of a cube with a radius of 1.0.
        # Returns a list containing eight sub-lists, each containing three floating-point values representing the x, y, and z
        # coordinates of a vertex of the cube.
    """
        
    scaler = radius/3**0.5
    v0 = [1, 1, 1]
    v1 = [-1, 1, 1]
    v2 = [1, -1, 1]
    v3 = [1, 1, -1]
    v4 = [-1, -1, 1]
    v5 = [1, -1, -1]
    v6 = [-1, 1, -1]
    v7 = [-1, -1, -1]
    VertCoord = [v0, v1, v2, v3, v4, v5, v6, v7]
    VertCoord_ = []
    for i in VertCoord:
        temp_list = []
        for j in i:
            temp = j*scaler
            temp_list.append(temp)
        VertCoord_.append(temp_list)
    return VertCoord_


