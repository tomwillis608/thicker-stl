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

    def centroid(self):
        """
        Calculate the centroid of the slice in the x-y plane.

        Returns:
            tuple: The (x, y) coordinates of the centroid.
        """
        if not self.vertices:
            return (0.0, 0.0)

        x_coords = [v[0] for v in self.vertices]
        y_coords = [v[1] for v in self.vertices]

        centroid_x = sum(x_coords) / len(x_coords)
        centroid_y = sum(y_coords) / len(y_coords)

        return (centroid_x, centroid_y)
