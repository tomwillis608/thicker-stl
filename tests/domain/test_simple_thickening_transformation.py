"""Test a simple thickening transformation."""

import pytest

from thicker.domain.mesh import Mesh
from thicker.domain.transformations import calculate_spherical_normal, thicken_mesh


@pytest.mark.parametrize("offset", [0.1, 0, -0.2])
def test_thickening_transformation(offset):
    """Test that thickening transformation increases vertex distances from origin."""
    # Arrange: Define a simple mesh but do not include a vertex at the origin
    vertices = [(0, 0, 1), (1, 0, 0), (0, 1, 0)]
    faces = [(0, 1, 2)]
    original_mesh = Mesh(vertices=vertices, faces=faces)

    # Act: Apply the thickening transformation
    thickened_mesh = thicken_mesh(original_mesh, offset, calculate_spherical_normal)
    # Assert: Check that vertices are offset outward by the given amount
    for original_vertex, thickened_vertex in zip(
        original_mesh.vertices, thickened_mesh.vertices
    ):
        # Calculate distance between original and thickened vertex
        distance = (
            (original_vertex[0] - thickened_vertex[0]) ** 2
            + (original_vertex[1] - thickened_vertex[1]) ** 2
            + (original_vertex[2] - thickened_vertex[2]) ** 2
        ) ** 0.5
        assert pytest.approx(distance, 0.01) == abs(offset)

    # Assert: Faces remain unchanged
    assert thickened_mesh.faces == original_mesh.faces


def test_thickening_origin_vertex():
    """Test that the thickening transformation
    for a vector at the origin does not change that vertex."""
    # Arrange: Define a simple mesh with a vertex at the origin
    vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    faces = [(0, 1, 2)]
    original_mesh = Mesh(vertices=vertices, faces=faces)
    offset = 0.1  # Thickness amount

    # Act: Apply the thickening transformation
    thickened_mesh = thicken_mesh(original_mesh, offset, calculate_spherical_normal)
    # Assert: Check that vertices(0) is still at the origin
    for i in range(3):
        assert (
            pytest.approx(original_mesh.vertices[0][i], 0.01)
            == thickened_mesh.vertices[0][i]
        )


def test_thicken_mesh_functional_equivalence():
    """
    Verify thicken_mesh produces the same output after refactoring.
    """
    # Arrange: Define a small input mesh and expected output
    input_mesh = Mesh(
        vertices=[(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)],
        faces=[(0, 1, 2)],
    )
    offset = 1.0
    expected_vertices = [
        (2.0, 0.0, 0.0),  # Vertex thickened along normal
        (0.0, 2.0, 0.0),
        (0.0, 0.0, 2.0),
    ]

    # Act: Apply the thickening transformation
    thickened_mesh = thicken_mesh(input_mesh, offset, calculate_spherical_normal)

    # Assert: Verify the thickened vertices match expectations
    assert thickened_mesh.vertices == expected_vertices
    assert thickened_mesh.faces == input_mesh.faces, "Faces should remain unchanged"
