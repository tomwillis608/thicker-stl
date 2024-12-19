"""Test the file processor."""

from typing import List, Tuple

import numpy as np
import pytest

from thicker.adapters.file_processor import (
    STLMeshReader,
    STLMeshWriter,
    _convert_to_float,
)


def test_stl_mesh_reader_reads_valid_file(tmp_path):
    """Test STLMeshReader correctly reads a valid STL file."""
    # Arrange: Create a temporary test STL file
    stl_filepath =  "tests/fixtures/test_cylinder.stl"

    reader = STLMeshReader()

    # Act: Read the file
    vertices, faces = reader.read(str(stl_filepath))

    # Assert: Verify expected output
    assert isinstance(vertices, list)
    assert all(isinstance(v, tuple) and len(v) == 3 for v in vertices)
    assert isinstance(faces, list)
    assert all(isinstance(f, tuple) and len(f) == 3 for f in faces)


def test_stl_mesh_writer_writes_valid_file(tmp_path):
    """Test STLMeshWriter writes a valid STL file."""
    # Arrange: Define vertices and faces for a simple mesh
    vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    faces = [(0, 1, 2)]

    writer = STLMeshWriter()
    stl_filepath = tmp_path / "output_mesh.stl"

    # Act: Write the file
    writer.write(str(stl_filepath), vertices, faces)

    # Assert: File exists and is valid
    assert stl_filepath.exists()

    # Verify file content by reloading
    from stl import mesh
    written_mesh = mesh.Mesh.from_file(str(stl_filepath))
    assert len(written_mesh.vectors) == len(faces)



def test_convert_to_float_with_python_floats():
    """Test conversion when input contains Python floats."""
    vertices = [(1.0, 2.0, 3.0), (4.0, 5.0, 6.0)]
    result = _convert_to_float(vertices)
    assert result == vertices, \
        "Expected input to remain unchanged when already Python floats."

def test_convert_to_float_with_numpy_floats():
    """Test conversion when input contains NumPy float types."""
    vertices = [(np.float32(1.0), np.float64(2.0), np.float32(3.0))]
    expected = [(1.0, 2.0, 3.0)]
    result = _convert_to_float(vertices)
    assert result == expected, \
        "Expected NumPy floats to be converted to Python floats."

def test_convert_to_float_with_mixed_types():
    """Test conversion when input contains a mix of integers,
       Python floats, and NumPy floats."""
    vertices = [(1, 2.0, np.float32(3.0))]
    expected = [(1.0, 2.0, 3.0)]
    result = _convert_to_float(vertices)
    assert result == expected, \
        "Expected all values to be converted to Python floats."

def test_convert_to_float_with_empty_input():
    """Test conversion when input list is empty."""
    vertices: List[Tuple] = []
    result = _convert_to_float(vertices)
    assert result == [], "Expected an empty list when input is empty."

def test_convert_to_float_with_invalid_input():
    """Test conversion when input contains non-numeric types."""
    vertices = [(1, "a", 3.0)]  # Contains a string
    with pytest.raises(ValueError):
        _convert_to_float(vertices)
