""" The Slice class  - a set of vertices in a height range. """

class Slice:
    def __init__(self, vertices, z_height):
        """
        Initialize a Slice object.

        Args:
            vertices (list of tuples): List of (x, y, z) vertices in the slice.
            z_height (float): The z-height at which this slice was taken.
        """
        self.vertices = vertices
        self.z_height = z_height
