"""Test STL round trip with transformation."""

from thicker.adapters.file_processor import STLMeshReader, STLMeshWriter
from thicker.domain.mesh import Mesh
from thicker.use_cases.thicken_mesh import thicken_a_mesh


def test_read_thicken_write(tmpdir):
    """Test end-to-end STL processing: read, thicken, and write."""
    # Arrange: Create a simple test STL file
    input_stl_path = "tests/fixtures/test_cylinder.stl"
    output_stl_path = tmpdir / "output.stl"

    # Act: Read, transform, and write the STL
    input_vertices, input_faces = STLMeshReader.read(file_path=input_stl_path)
    input_mesh = Mesh(input_vertices, input_faces)
    thickened_mesh = thicken_a_mesh(original_mesh=input_mesh, offset=0.5)
    STLMeshWriter.write(
        output_path=output_stl_path,
        vertices=thickened_mesh.vertices,
        faces=thickened_mesh.faces,
    )

    # Assert: Verify that the output STL is valid
    written_vertices, written_faces = STLMeshReader.read(output_stl_path)
    assert len(written_vertices) == len(thickened_mesh.vertices)
    assert len(written_faces) == len(thickened_mesh.faces)
