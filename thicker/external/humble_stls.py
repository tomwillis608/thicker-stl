"""Humble object to read STL data from files."""

# connectors/humble_stl_reader.py
from typing import List, Tuple

from stl import mesh


class STLReader:
    """A humble object to handle STL file operations."""

    @staticmethod
    def load(
        file_path: str,
    ) -> Tuple[List[Tuple[float, float, float]], List[Tuple[int, int, int]]]:
        """
        Load an STL file and parse its vertices and faces.

        Args:
            file_path (str): Path to the STL file.

        Returns:
            Tuple[List[Tuple[float, float, float]],
                List[Tuple[int, int, int]]]: Parsed vertices and faces.
        """
        stl_mesh = mesh.Mesh.from_file(file_path)
        vertices = [(v[0], v[1], v[2]) for v in stl_mesh.vectors.reshape(-1, 3)]
        faces = [(i, i + 1, i + 2) for i in range(0, len(vertices), 3)]
        return vertices, faces
