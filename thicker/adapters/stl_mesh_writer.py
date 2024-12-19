"""Connector to read STL files."""

from typing import List, Tuple

import numpy as np
from stl import mesh


class STLMeshWriter:
    """A humble object to handle STL file operations."""

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
