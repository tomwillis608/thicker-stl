"""Connector to read STL files."""

from typing import List, Tuple

from thicker.external.humble_stls import STLReader


def process_stl_data(
    file_path: str,
) -> Tuple[List[Tuple[float, float, float]], List[Tuple[int, int, int]]]:
    """
    Process STL data by delegating to the humble object.

    Args:
        file_path (str): Path to the STL file.

    Returns:
        Tuple[List[Tuple[float, float, float]],
            List[Tuple[int, int, int]]]: Processed vertices and faces.
    """

    # Delegate to the humble object to load data
    vertices, faces = STLReader.load(file_path)

    # Type assertions to ensure the data is well-formed
    assert isinstance(vertices, list), "Vertices must be a list."
    assert all(
        isinstance(v, tuple)
        and len(v) == 3
        and all(isinstance(coord, (float, int)) for coord in v)
        for v in vertices
    ), "Each vertex must be a tuple of three float or int coordinates."

    assert isinstance(faces, list), "Faces must be a list."
    assert all(
        isinstance(f, tuple) and len(f) == 3 and all(isinstance(idx, int) for idx in f)
        for f in faces
    ), "Each face must be a tuple of three integers."

    return vertices, faces
