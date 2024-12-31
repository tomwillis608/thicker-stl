"""Integration tests for domed cylinder transformation from fixtures."""

import math

from thicker.adapters.stl_mesh_reader import STLMeshReader
from thicker.adapters.stl_mesh_writer import STLMeshWriter
from thicker.domain.mesh import Mesh
from thicker.domain.transformations import HemisphericalCylinderTransformation
from thicker.interfaces.mesh_reader import MeshReader
from thicker.interfaces.mesh_writer import MeshWriter


def test_cylindrical_model_transformation_read_write(tmpdir):
    """
    Test end-to-end STL processing: read, transform, and write.
    Verify the HemisphericalCylinderTransformation on a cylindrical test model.
    """
    # Arrange: Create a simple test STL file
    input_stl_path = "tests/fixtures/test_cylinder.stl"
    input_stl_path = "tests/fixtures/test_cylinder_2.stl"
    output_stl_path = "output.stl"
    # output_stl_path = tmpdir / "output.stl"
    reader: MeshReader = STLMeshReader()
    writer: MeshWriter = STLMeshWriter()
    # Define transformation parameters
    cylinder_height = 5.0  # center dome at height of 5 of 10
    radius = 5.0
    offset = 1.0

    # Act: Read, transform, and write the STL
    vertices, faces = reader.read(input_stl_path)
    mesh = Mesh(vertices=vertices, faces=faces)
    # Apply the transformation
    transformation = HemisphericalCylinderTransformation(cylinder_height, radius)
    transformed_mesh = transformation.transform(mesh, offset)
    writer.write(output_stl_path, transformed_mesh.vertices, transformed_mesh.faces)

    # Assert: Verify that the output STL is valid
    written_vertices, written_faces = reader.read(output_stl_path)
    assert len(written_vertices) == len(transformed_mesh.vertices)
    assert len(written_faces) == len(transformed_mesh.faces)

    # Assertions
    for original_vertex, transformed_vertex in zip(
        mesh.vertices, transformed_mesh.vertices
    ):
        # Calculate the normal for the original vertex
        normal = transformation.calculate_normal(original_vertex)

        # Calculate the expected transformed vertex
        expected_vertex = (
            original_vertex[0] + offset * normal[0],
            original_vertex[1] + offset * normal[1],
            original_vertex[2] + offset * normal[2],
        )

        # Assert the transformed vertex matches the expected vertex
        assert math.isclose(transformed_vertex[0], expected_vertex[0], rel_tol=1e-5)
        assert math.isclose(transformed_vertex[1], expected_vertex[1], rel_tol=1e-5)
        assert math.isclose(transformed_vertex[2], expected_vertex[2], rel_tol=1e-5)


def test_cube_model_transformation_read_write(tmpdir):
    """
    Test end-to-end STL processing: read, transform, and write.
    Verify the HemisphericalCylinderTransformation on a cylindrical test model.
    """
    # Arrange: Create a simple test STL file
    input_stl_path = "tests/fixtures/test_cube.stl"
    output_stl_path = "output_cube.stl"
    # output_stl_path = tmpdir / "output.stl"
    reader: MeshReader = STLMeshReader()
    writer: MeshWriter = STLMeshWriter()
    # Define transformation parameters
    cylinder_height = 0.375
    radius = 0.5
    offset = 0.5

    # Act: Read, transform, and write the STL
    vertices, faces = reader.read(input_stl_path)
    mesh = Mesh(vertices=vertices, faces=faces)
    # Apply the transformation
    transformation = HemisphericalCylinderTransformation(cylinder_height, radius)
    transformed_mesh = transformation.transform(mesh, offset)
    writer.write(output_stl_path, transformed_mesh.vertices, transformed_mesh.faces)

    # Assert: Verify that the output STL is valid
    written_vertices, written_faces = reader.read(output_stl_path)
    assert len(written_vertices) == len(transformed_mesh.vertices)
    assert len(written_faces) == len(transformed_mesh.faces)

    # Assertions
    for original_vertex, transformed_vertex in zip(
        mesh.vertices, transformed_mesh.vertices
    ):
        # Calculate the normal for the original vertex
        normal = transformation.calculate_normal(original_vertex)

        # Calculate the expected transformed vertex
        expected_vertex = (
            original_vertex[0] + offset * normal[0],
            original_vertex[1] + offset * normal[1],
            original_vertex[2] + offset * normal[2],
        )

        # Assert the transformed vertex matches the expected vertex
        assert math.isclose(transformed_vertex[0], expected_vertex[0], rel_tol=1e-5)
        assert math.isclose(transformed_vertex[1], expected_vertex[1], rel_tol=1e-5)
        assert math.isclose(transformed_vertex[2], expected_vertex[2], rel_tol=1e-5)
