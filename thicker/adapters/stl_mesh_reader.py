"""Connector to read STL files."""

from typing import List, Tuple

from stl import mesh


def _convert_to_float(vertices: List[Tuple]) -> List[Tuple[float, float, float]]:
    """
    Ensure all vertex coordinates are Python float type.

    Args:
        vertices (List[Tuple]): List of vertices, possibly with NumPy float types.

    Returns:
        List[Tuple[float, float, float]]: List of vertices with native Python floats.
    """
    return [
        (float(vertex[0]), float(vertex[1]), float(vertex[2])) for vertex in vertices
    ]


class STLMeshReader:
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
        # Ensure vertices are Python floats
        vertices = _convert_to_float(vertices)
        faces = [(i, i + 1, i + 2) for i in range(0, len(vertices), 3)]

        # Type assertions to ensure the data is well-formed
        assert isinstance(vertices, list), "Vertices must be a list."
        assert all(
            isinstance(v, tuple)
            and len(v) == 3
            and all(isinstance(coord, (float, int)) for coord in v)
            for v in vertices
        ), "Each vertex must have three numeric coordinates."
        assert isinstance(faces, list), "Faces must be a list."
        assert all(
            isinstance(f, tuple)
            and len(f) == 3
            and all(isinstance(idx, int) for idx in f)
            for f in faces
        ), "Each face must be a tuple of three integers."

        return vertices, faces
