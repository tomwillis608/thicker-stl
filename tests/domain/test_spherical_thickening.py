"""Test the spherical thickening."""

import math

from thicker.domain.mesh import Mesh
from thicker.domain.transformations import calculate_spherical_normal, thicken_mesh


def test_thicken_mesh_spherical_transformation():
    """Test that spherical thickening correctly offsets vertices."""
    # Arrange
    vertices = [
        (1.0, 0.0, 0.0),  # Point on +x axis
        (0.0, 1.0, 0.0),  # Point on +y axis
        (0.0, 0.0, 1.0),  # Point on +z axis
        (-1.0, 0.0, 0.0),  # Point on -x axis
        (0.0, -1.0, 0.0),  # Point on -y axis
        (0.0, 0.0, -1.0),  # Point on -z axis
        (1.0, 1.0, 1.0),  # Point on the first octant
        (-1.0, -1.0, -1.0),  # Point on the opposite octant
    ]
    faces = [(0, 1, 2), (3, 4, 5)]  # Arbitrary faces
    mesh = Mesh(vertices=vertices, faces=faces)
    offset = 1.0

    # Act
    transformed_mesh = thicken_mesh(mesh, offset, calculate_spherical_normal)

    # Assert
    expected_vertices = [
        (2.0, 0.0, 0.0),  # Offset along +x axis
        (0.0, 2.0, 0.0),  # Offset along +y axis
        (0.0, 0.0, 2.0),  # Offset along +z axis
        (-2.0, 0.0, 0.0),  # Offset along -x axis
        (0.0, -2.0, 0.0),  # Offset along -y axis
        (0.0, 0.0, -2.0),  # Offset along -z axis
        (1.5774, 1.5774, 1.5774),  # Normalized diagonal offset in first octant
        (-1.5774, -1.5774, -1.5774),  # Normalized diagonal offset in opposite octant
    ]

    for actual, expected in zip(transformed_mesh.vertices, expected_vertices):
        assert math.isclose(
            actual[0], expected[0], rel_tol=1e-4
        ), f"X mismatch: {actual[0]} != {expected[0]}"
        assert math.isclose(
            actual[1], expected[1], rel_tol=1e-4
        ), f"Y mismatch: {actual[1]} != {expected[1]}"
        assert math.isclose(
            actual[2], expected[2], rel_tol=1e-4
        ), f"Z mismatch: {actual[2]} != {expected[2]}"
