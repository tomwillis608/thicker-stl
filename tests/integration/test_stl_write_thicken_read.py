"""Test STL round trip with transformation."""

from thicker.adapters.file_processor import STLMeshReader, STLMeshWriter
from thicker.domain.mesh import Mesh
from thicker.interfaces.mesh_reader import MeshReader
from thicker.interfaces.mesh_writer import MeshWriter
from thicker.use_cases.thicken_mesh import thicken_a_mesh


def test_read_thicken_write(tmpdir):
    """Test end-to-end STL processing: read, thicken, and write."""
    # Arrange: Create a simple test STL file
    input_stl_path = "tests/fixtures/test_cylinder.stl"
    output_stl_path = tmpdir / "output.stl"
    reader: MeshReader = STLMeshReader()
    writer: MeshWriter = STLMeshWriter()
    offset = 0.5

    # Act: Read, transform, and write the STL
    vertices, faces = reader.read(input_stl_path)
    mesh = Mesh(vertices=vertices, faces=faces)
    thickened_mesh = thicken_a_mesh(mesh, offset)
    writer.write(output_stl_path, thickened_mesh.vertices, thickened_mesh.faces)

    # Assert: Verify that the output STL is valid
    written_vertices, written_faces = reader.read(output_stl_path)
    assert len(written_vertices) == len(thickened_mesh.vertices)
    assert len(written_faces) == len(thickened_mesh.faces)
