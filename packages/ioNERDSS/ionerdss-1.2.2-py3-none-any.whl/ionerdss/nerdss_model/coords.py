class Coords:
    """
    Holds the x, y, z coordinates of a 3D point. Includes basic vector arithmetic
    and distance calculation.

    Attributes:
        x (float): The x-coordinate.
        y (float): The y-coordinate.
        z (float): The z-coordinate.
    """
    def __init__(self, x: float, y: float, z: float):
        """
        Initializes a Coords instance.

        Args:
            x (float): x-coordinate.
            y (float): y-coordinate.
            z (float): z-coordinate.
        """
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def distance(self, other) -> float:
        """
        Calculates the Euclidean distance between two points.

        Args:
            other (Coords): The other point to calculate the distance to.

        Returns:
            float: The Euclidean distance between the two points.
        """
        return ((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)**0.5

    def __sub__(self, other):
        """
        Implements subtraction for Coords objects.

        Args:
            other (Coords): The other coordinate to subtract.

        Returns:
            Coords: The resulting coordinate.
        """
        return Coords(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        """
        Implements addition for Coords objects.

        Args:
            other (Coords): The other coordinate to add.

        Returns:
            Coords: The resulting coordinate.
        """
        return Coords(self.x + other.x, self.y + other.y, self.z + other.z)
    