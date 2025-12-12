def mid_pt(a: float, b: float):
    """Compute the mid-point between two coordinates in 3-dimensional space.

    Parameters:
        a (float): The first coordinate in the form of [x, y, z].
        b (float): The second coordinate in the form of [x, y, z].

    Returns:
        List[float]: The mid-point coordinates in the form of [x, y, z].


    Examples
        >>> a = [0.0, 0.0, 0.0]
        >>> b = [2.0, 4.0, 6.0]
        >>> mid_pt(a, b)
        [1.0, 2.0, 3.0]

    Notes
        This function calculates the mid-point between two coordinates in 3-dimensional space
        by taking the average of the corresponding x, y, and z coordinates of the two points.
        The result is rounded to 15 decimal places using the `round()` function with `n` set to 15,
        which is the value of `n` used in the function implementation.
    """
    
    # this is a seperate function for calculating mid point of two coords
    n = 15
    return [round((a[0]+b[0])/2, n), round((a[1]+b[1])/2, n), round((a[2]+b[2])/2, n)]


