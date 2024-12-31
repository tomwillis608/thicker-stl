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


def test_calculate_radius_empty_mesh():
    """Test radius calculation with an empty mesh."""
    empty_mesh = Mesh(vertices=[], faces=[])
    with pytest.raises(ValueError):
        _ = calculate_mesh_radius(empty_mesh)



def test_calculate_radius_origin_mesh():
    """Test radius calculation with all vertices at origin."""
    origin_mesh = Mesh(
        vertices=[(0, 0, 0), (0, 0, 0), (0, 0, 0)],
        faces=[(0, 1, 2)]
    )
    radius = calculate_mesh_radius(origin_mesh)
    assert radius == 0, "Expected radius of origin-only mesh to be 0"


def test_calculate_radius_different_z_levels():
    """Test radius calculation with vertices at different z-levels."""
    varied_z_mesh = Mesh(
        vertices=[
            (1, 0, 0),    # radius 1 at z=0
            (0, 2, 1),    # radius 2 at z=1
            (0, 0, 2),    # radius 0 at z=2
            (-1.5, 0, -1) # radius 1.5 at z=-1
        ],
        faces=[(0, 1, 2), (0, 2, 3)]
    )
    radius = calculate_mesh_radius(varied_z_mesh)
    assert radius == 2, "Expected radius to be the maximum radial distance (2.0)"
