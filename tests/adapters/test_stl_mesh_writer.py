"""Test the file processor."""


from thicker.adapters.stl_mesh_writer import STLMeshWriter


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
