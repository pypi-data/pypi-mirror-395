def octa_face_vert_coord(radius: float):
    """Generates the coordinates of the vertices of an octahedron based on the given radius.

    Args:
        radius (float): The radius of the octahedron.

    Returns:
        List[List[float]]: A list of vertex coordinates of the octahedron. Each element in the list
            is a sublist containing three floating point values representing the (x, y, z) coordinates
            of a vertex.

    Example:
        radius = 5.0
        vert_coord = octa_face_vert_coord(radius)
        print(vert_coord)

    Note:
        The function generates the vertex coordinates of an octahedron centered at the origin (0, 0, 0)
        with six vertices located at (+-radius, 0, 0), (0, +-radius, 0), and (0, 0, +-radius). The
        resulting vertex coordinates are returned as a list of lists, where each sublist contains the
        (x, y, z) coordinates of a specific vertex.
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


