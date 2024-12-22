"""Test new cylindrical thickening transformation."""

import math

from thicker.domain.mesh import Mesh
from thicker.domain.transformations import calculate_cylindrical_normal, thicken_mesh


def test_cylindrical_thickening_vertical():
    """
    Test cylindrical thickening transformation with a vertical cylinder.
    """
    # Arrange
    input_mesh = Mesh(
        vertices=[
            # on base plane
            (1.0, 0.0, 0.0),  # Point on the x-axis
            (0.0, 1.0, 0.0),  # Point on the y-axis
            (-1.0, 0.0, 0.0),  # Point on the negative x-axis
            (0.0, -1.0, 0.0),  # Point on the negative y-axis
            # on z=2 plane
            (1.0, 0.0, 2.0),  # Point on the x-axis
            (0.0, 1.0, 2.0),  # Point on the y-axis
            (-1.0, 0.0, 2.0),  # Point on the negative x-axis
            (0.0, -1.0, 2.0),  # Point on the negative y-axis
        ],
        faces=[],
    )
    offset = 0.1

    # Expected new vertices
    expected_vertices = [
        (1.1, 0.0, 0.0),  # Expanded outward from x-axis
        (0.0, 1.1, 0.0),  # Expanded outward from y-axis
        (-1.1, 0.0, 0.0),  # Expanded outward from negative x-axis
        (0.0, -1.1, 0.0),  # Expanded outward from negative y-axis
        (1.1, 0.0, 2.0),  # Expanded outward from x-axis
        (0.0, 1.1, 2.0),  # Expanded outward from y-axis
        (-1.1, 0.0, 2.0),  # Expanded outward from negative x-axis
        (0.0, -1.1, 2.0),  # Expanded outward from negative y-axis
    ]

    # Act
    transformed_mesh = thicken_mesh(input_mesh, offset, calculate_cylindrical_normal)

    # Assert
    for actual, expected in zip(transformed_mesh.vertices, expected_vertices):
        assert math.isclose(
            actual[0], expected[0], rel_tol=1e-9
        ), f"X mismatch: {actual[0]} != {expected[0]}"
        assert math.isclose(
            actual[1], expected[1], rel_tol=1e-9
        ), f"X mismatch: {actual[1]} != {expected[1]}"
        assert math.isclose(
            actual[2], expected[2], rel_tol=1e-9
        ), f"X mismatch: {actual[2]} != {expected[2]}"
