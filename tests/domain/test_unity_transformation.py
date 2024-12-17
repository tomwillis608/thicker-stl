"""Test the unity transformation."""

from thicker.domain.mesh import Mesh
from thicker.domain.transformations import unity_transformation


def test_unity_transformation():
    """Test that the unity transformation does not modify the mesh."""
    # Arrange: Define a simple mesh
    vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
    faces = [(0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 2, 3)]
    original_mesh = Mesh(vertices=vertices, faces=faces)

    # Act: Apply the unity transformation
    transformed_mesh = unity_transformation(original_mesh)

    # Assert: Verify the vertices and faces remain unchanged
    assert transformed_mesh.vertices == original_mesh.vertices
    assert transformed_mesh.faces == original_mesh.faces
