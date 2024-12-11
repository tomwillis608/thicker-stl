"""Define the Mesh class."""

from typing import List, Tuple


class Mesh:
    """Define the Polygonal Mesh Representation.

    Edges are not included at this time and
    could be dynamically calculated from faces."""

    def __init__(
        self,
        vertices: List[Tuple[float, float, float]],
        faces: List[Tuple[int, int, int]],
    ):
        self.vertices = vertices
        self.faces = faces
