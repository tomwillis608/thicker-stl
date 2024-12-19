"""Interface for concrete MeshWriters."""

from typing import List, Protocol, Tuple


class MeshWriter(Protocol):
    """Protocol for writing mesh data."""

    def write(
        self,
        filepath: str,
        vertices: List[Tuple[float, float, float]],
        faces: List[Tuple[int, int, int]],
    ) -> None:
        """Writes vertices and faces to a file."""
        ...
