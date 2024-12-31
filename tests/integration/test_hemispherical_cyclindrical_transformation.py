"""Test the hemispherical-cylindrical transformation use case."""

import tempfile

from thicker.adapters.stl_mesh_reader import STLMeshReader
from thicker.adapters.stl_mesh_writer import STLMeshWriter
from thicker.domain.mesh import Mesh
from thicker.interfaces.mesh_reader import MeshReader
from thicker.interfaces.mesh_writer import MeshWriter
from thicker.use_cases.thicken_mesh import process_thickening


def test_transform_stl_with_new_transformation():
    # Arrange:
    # Define a robust input mesh: A unit cylinder with flat caps
    input_mesh = Mesh(
        vertices=[
            # Bottom circle
            (0, 0, 0),  # Center
            (1, 0, 0),
            (0.707, 0.707, 0),
            (0, 1, 0),
            (-0.707, 0.707, 0),
            (-1, 0, 0),
            (-0.707, -0.707, 0),
            (0, -1, 0),
            (0.707, -0.707, 0),
            # Top circle
            (0, 0, 1),  # Center
            (1, 0, 1),
            (0.707, 0.707, 1),
            (0, 1, 1),
            (-0.707, 0.707, 1),
            (-1, 0, 1),
            (-0.707, -0.707, 1),
            (0, -1, 1),
            (0.707, -0.707, 1),
        ],
        faces=[
            # Bottom cap
            (0, 1, 2),
            (0, 2, 3),
            (0, 3, 4),
            (0, 4, 5),
            (0, 5, 6),
            (0, 6, 7),
            (0, 7, 8),
            (0, 8, 1),
            # Top cap
            (9, 10, 11),
            (9, 11, 12),
            (9, 12, 13),
            (9, 13, 14),
            (9, 14, 15),
            (9, 15, 16),
            (9, 16, 17),
            (9, 17, 10),
            # Side faces
            (1, 10, 11),
            (1, 11, 2),
            (2, 11, 12),
            (2, 12, 3),
            (3, 12, 13),
            (3, 13, 4),
            (4, 13, 14),
            (4, 14, 5),
            (5, 14, 15),
            (5, 15, 6),
            (6, 15, 16),
            (6, 16, 7),
            (7, 16, 17),
            (7, 17, 8),
            (8, 17, 10),
            (8, 10, 1),
        ],
    )
    reader: MeshReader = STLMeshReader()
    writer: MeshWriter = STLMeshWriter()

    with (
        tempfile.NamedTemporaryFile(suffix=".stl") as input_file,
        tempfile.NamedTemporaryFile(suffix=".stl") as output_file,
    ):
        # Write the input mesh to a temporary file
        writer.write(input_file.name, input_mesh.vertices, input_mesh.faces)

        # Transformation parameters
        height = 1.0
        radius = 1.0
        offset = 0.2

        # Execute the transformation
        process_thickening(
            reader,
            writer,
            input_path=input_file.name,
            output_path=output_file.name,
            offset=offset,
        )

        # Read the output STL
        output_vertices, output_faces = reader.read(output_file.name)
        output_mesh = Mesh(output_vertices, output_faces)

        # Validate that the transformation applied correctly

        tolerance = 1e-6  # Define a tolerance for floating-point comparisons
        for vertex in output_mesh.vertices:
            x, y, z = vertex
            distance = (x**2 + y**2) ** 0.5
            # Debug outputs for investigation
            # print(f"Vertex: {vertex}, Distance from center: {distance}")
            if z <= height:
                assert distance <= radius + offset + tolerance, (
                    f"Vertex {vertex} exceeds the cylindrical boundary. "
                    f"Distance: {distance}, "
                    f"Expected <= {radius + offset + tolerance}"
                )
            else:
                f"Expected <= {radius + offset}"
                f"Expected <= {radius + offset}"
                assert distance <= radius + offset + offset + tolerance, (
                    f"Vertex {vertex} exceeds the hemispherical boundary. "
                    f"Distance: {distance}, "
                    f"Expected <= {radius + offset + offset + tolerance}"
                )

        # Ensure no faces were lost or incorrectly generated
        assert len(output_mesh.faces) == len(
            input_mesh.faces
        ), "Mismatch in the number of faces"
