def tetr_vert_coord(radius: float):
    """Generate the coordinates of the vertices of a regular tetrahedron given the radius.

    Args:
        radius (float): The radius of the circumsphere of the tetrahedron.

    Returns:
        list: A list of 4 3-dimensional coordinate vectors representing the vertices of the tetrahedron.

    Example:
        >>> tetr_vert_coord(1.0)
        [[0.612372, 0.0, -0.353553],
         [-0.612372, 0.0, -0.353553],
         [0.0, 0.707107, 0.353553],
         [0.0, -0.707107, 0.353553]]
    """
    scaler = radius/(3/8)**0.5/2
    v0 = [1, 0, -1/2**0.5]
    v1 = [-1, 0, -1/2**0.5]
    v2 = [0, 1, 1/2**0.5]
    v3 = [0, -1, 1/2**0.5]
    VertCoord = [v0, v1, v2, v3]
    VertCoord_ = []
    for i in VertCoord:
        temp_list = []
        for j in i:
            temp = j*scaler
            temp_list.append(temp)
        VertCoord_.append(temp_list)
    return VertCoord_


