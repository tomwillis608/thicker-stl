"""Humble object to read and write STL data from files."""

# connectors/humble_stl_reader.py
from typing import List, Tuple

import numpy as np
from stl import mesh


class Humble_STL_IO:
    """A humble object to handle STL file operations."""

    @staticmethod
    def read(
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

    @staticmethod
    def write(
        output_path: str,
        vertices: List[Tuple[float, float, float]],
        faces: List[Tuple[int, int, int]],
    ):
        """
        Save an STL file from vertices and faces.

        Args:
            output_path (str): Path to the STL file to create.
            vertices (List[Tuple[float, float, float]]): The vertices in the shape.
            faces (List[Tuple[int, int, int]]): The paces made of vertices in the shape.

        Returns:
            None
        """

        # Convert regular lists to np.arrays
        vertices = np.array(vertices)
        faces = np.array(faces)

        # Create the mesh object
        new_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, face in enumerate(faces):
            for j in range(3):
                new_mesh.vectors[i][j] = vertices[face[j], :]

        # Save the mesh to a file
        new_mesh.save(output_path)
