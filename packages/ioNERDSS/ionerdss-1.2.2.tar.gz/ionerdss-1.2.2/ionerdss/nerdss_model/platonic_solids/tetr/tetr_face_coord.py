def tetr_face_coord(radius: float):
    """Generates vertex coordinates of a tetrahedron given the radius of its circumscribed sphere.

    Args:
        radius (float): The radius of the circumscribed sphere of the tetrahedron.

    Returns:
        list: A list of vertex coordinates for the tetrahedron. The list contains 4 sub-lists,
        each representing the coordinates of one vertex. Each sub-list contains 3 floats representing
        the x, y, and z coordinates of the vertex.

    Example:
        >>> tetr_face_coord(1.0)
        [[0.612372, 0.0, -0.353553], [-0.612372, 0.0, -0.353553],
        [0.0, 0.612372, 0.353553], [0.0, -0.612372, 0.353553]]
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


