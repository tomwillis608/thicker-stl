""" Interface for concrete MeshReaders. """
from typing import List, Protocol, Tuple


class MeshReader(Protocol):
    """Protocol for reading mesh data."""
    def read(self, filepath: str) -> Tuple[List[Tuple[float, float, float]],
            List[Tuple[int, int, int]]]:
        """Reads a mesh file and returns vertices and faces."""
        ...
