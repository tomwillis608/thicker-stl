"""Test the use case mesh dimension calculations."""

import pytest

from thicker.domain.mesh import Mesh
from thicker.use_cases.thicken_mesh import calculate_mesh_height, calculate_mesh_radius


@pytest.fixture
def simple_vertical_mesh():
    """Creates a simple mesh with known min and max z-values
    for testing height calculation."""
    vertices = [
        (0, 0, -2),  # Bottom vertex
        (1, 1, 0),  # Mid vertex
        (-1, -1, 2),  # Top vertex
    ]
    faces = [(0, 1, 2)]  # Single face using all vertices
    return Mesh(vertices=vertices, faces=faces)


def test_calculate_height_simple_mesh(simple_vertical_mesh):
    """Test height calculation with a simple vertical mesh."""
    height = calculate_mesh_height(simple_vertical_mesh)

    assert height == 4, f"Expected height to be 4, but got {height}"


def test_calculate_radius():
    """
    Test the calculation of the radius for a cylindrical mesh.
    """
    # Create a simple cylindrical mesh with vertices representing a unit cylinder
    vertices = [
        (1, 0, 0),  # Vertex at radius 1 along x-axis
        (0, 1, 0),  # Vertex at radius 1 along y-axis
        (-1, 0, 0),  # Vertex at radius 1 along -x-axis
        (0, -1, 0),  # Vertex at radius 1 along -y-axis
        (0.707, 0.707, 0),  # Vertex at radius ~1 along diagonal
        (-0.707, -0.707, 0),  # Vertex at radius ~1 along opposite diagonal
    ]

    faces = []  # Faces are irrelevant for radius calculation
    mesh = Mesh(vertices=vertices, faces=faces)

    # Call the radius calculation function
    radius = calculate_mesh_radius(mesh)

    # Assert that the calculated radius matches the expected value
    expected_radius = 1.0
    assert (
        pytest.approx(radius, rel=1e-3) == expected_radius
    ), f"Expected radius {expected_radius}, got {radius}"
