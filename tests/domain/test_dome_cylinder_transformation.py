"""Test hemisphere-cylinder transformation."""

from math import sqrt

# def test_hemisphere_topped_cylinder_transformation():
from thicker.domain.mesh import Mesh
from thicker.domain.transformations import HemisphereToppedCylinderTransformation


def test_hemisphere_topped_cylinder_transformation():
    """
    Test the hemisphere-topped cylinder transformation on a simple mesh.
    """
    # Arrange
    transformer = HemisphereToppedCylinderTransformation(
        cylinder_height=0.5, radius=1.0
    )

    # Define a simple mesh with a unit cube's vertices
    unit_cube_vertices = [
        (-1, -1, -1),
        (-1, -1, 1),
        (-1, 1, -1),
        (-1, 1, 1),
        (1, -1, -1),
        (1, -1, 1),
        (1, 1, -1),
        (1, 1, 1),
    ]
    faces = [(0, 1, 2), (1, 2, 3)]  # Example faces (irrelevant for the test)
    mesh = Mesh(vertices=unit_cube_vertices, faces=faces)

    # Expected transformed vertices
    def expected_transformed(vertex):
        x, y, z = vertex
        radius = sqrt(x**2 + y**2)
        if z <= 0.5:
            # Cylindrical region
            if radius == 0:
                return (0, 0, z)
            scale = 1 / radius
            return (x * scale, y * scale, z)
        else:
            # Hemisphere region
            norm = sqrt(x**2 + y**2 + z**2)
            return (x / norm, y / norm, z / norm)

    expected_vertices = [expected_transformed(v) for v in unit_cube_vertices]

    # Act
    transformed_mesh = transformer.transform(mesh)

    # Assert
    for transformed, expected in zip(transformed_mesh.vertices, expected_vertices):
        assert all(
            abs(t - e) < 1e-6 for t, e in zip(transformed, expected)
        ), f"Expected {expected}, got {transformed}"
