import unittest
import numpy as np
from typing import List

def distance(a: List[float], b: List[float]) -> float:
    """Compute the Euclidean distance between two points in n-dimensional space.

    Args:
        a (List[float]): The coordinates of the first point.
        b (List[float]): The coordinates of the second point.

    Returns:
        float: The Euclidean distance between the two points.


    Examples:
        >>> a = [0, 0, 0]
        >>> b = [1, 1, 1]
        >>> distance(a, b)
        1.7320508075688772

    Notes
        This function computes the Euclidean distance between two points by taking
        the square root of the sum of squared differences of each coordinate. The 
        result is rounded to 15 decimal places using string formatting.
    """
    return float(f"{np.linalg.norm(np.array(a) - np.array(b)):.15f}")

class TestDistance(unittest.TestCase):
    def test_distance(self):
        a = [0, 0, 0]
        b = [1, 1, 1]
        self.assertAlmostEqual(distance(a, b), 1.7320508075688772)

        a = [3, 4, 0]
        b = [0, 0, 12]
        self.assertAlmostEqual(distance(a, b), 13.0)

        a = [0, 4]
        b = [3, 0]
        self.assertAlmostEqual(distance(a, b), 5.0)

if __name__ == '__main__':
    unittest.main()
