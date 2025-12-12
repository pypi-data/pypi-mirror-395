def cube_face_vert_coord(radius: float):
    """Generates vertex coordinates for a cube face.

    This function takes the radius of a cube face as input, and generates a list of vertex coordinates for the cube face
    of a platonic solid. The vertex coordinates are calculated by scaling the pre-defined vertex coordinates of a unit cube
    by the given radius value.

    Args:
        radius (float): The radius of the platonic solid.

    Returns:
        List: Contains vertex coordinates for the cube face. Each vertex coordinate is a list of three floats representing the
        x, y, and z coordinates of the vertex. The vertex coordinates are scaled by the radius value. 

    Raises:
        None.

    Example:
        >>> cube_face_vert_coord(1.0)
        [[0.5773502691896257, 0.5773502691896257, 0.5773502691896257],
         [-0.5773502691896257, 0.5773502691896257, 0.5773502691896257],
         [0.5773502691896257, -0.5773502691896257, 0.5773502691896257],
         [0.5773502691896257, 0.5773502691896257, -0.5773502691896257],
         [-0.5773502691896257, -0.5773502691896257, 0.5773502691896257],
         [0.5773502691896257, -0.5773502691896257, -0.5773502691896257],
         [-0.5773502691896257, 0.5773502691896257, -0.5773502691896257],
         [-0.5773502691896257, -0.5773502691896257, -0.5773502691896257]]
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


