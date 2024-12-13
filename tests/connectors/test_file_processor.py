"""Test the file processor."""

from thicker.connectors.file_processor import process_stl_data

# mocker.patch('thicker.domain.mesh.Mesh', return_value=mock_mesh_object)


def test_process_stl_data():
    """Test that process_stl_data correctly processes STL file input."""
    # Arrange
    sample_file_path = "test.stl"
    expected_vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    expected_faces = [(0, 1, 2)]

    # Act
    vertices, faces = process_stl_data(sample_file_path)

    # Assert
    assert vertices == expected_vertices, "Vertices do not match expected output."
    assert faces == expected_faces, "Faces do not match expected output."
