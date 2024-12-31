"""Test hemisphere-cylinder transformation."""

import numpy as np
import pytest

from thicker.domain.mesh import Mesh
from thicker.domain.transformations import HemisphereToppedCylinderTransformation


@pytest.fixture
def transformation():
    return HemisphereToppedCylinderTransformation(cylinder_height=10, radius=5)

def test_cylindrical_normal(transformation):
    vertex = (3, 4, 5)  # On the cylinder side
    expected_normal = (3 / 5, 4 / 5, 0)  # Normalized radial vector
    normal = transformation.calculate_normal(vertex)
    assert np.allclose(normal, expected_normal), \
        f"Expected {expected_normal}, got {normal}"

def test_hemispherical_normal(transformation):
    vertex = (0, 0, 12)  # On the top of the hemisphere
    expected_normal = (0, 0, 1)  # Directly upward
    normal = transformation.calculate_normal(vertex)
    assert np.allclose(normal, expected_normal), \
        f"Expected {expected_normal}, got {normal}"


def test_hemispherical_normal_diagonal(transformation):
    vertex = (3, 4, 12)  # On the hemisphere's slope
    center = (0, 0, 10)  # Hemisphere center
    vector_to_vertex = (vertex[0]-center[0],
                        vertex[1]-center[1],
                        vertex[2]-center[2])
    norm = np.linalg.norm(vector_to_vertex)
    expected_normal = (3 / norm, 4 / norm, 2 / norm)  # Properly normalized
    normal = transformation.calculate_normal(vertex)
    assert np.allclose(normal, expected_normal), \
        f"Expected {expected_normal}, got {normal}"



@pytest.fixture
def simple_mesh():
    vertices = [
        (3, 4, 5),   # Cylindrical vertex
        (0, 0, 12),  # Top of hemisphere
        (3, 4, 12),  # Sloped hemisphere vertex
    ]
    faces = []  # Faces aren't relevant for this test
    return Mesh(vertices=vertices, faces=faces)

def test_transform_cylindrical_vertex(transformation):
    vertex = (3, 4, 5)  # Cylindrical vertex
    offset = 2
    transformed_mesh = transformation.transform(Mesh(vertices=[vertex],
                                                     faces=[]), offset)
    expected_vertex = (3 + 2 * 3 / 5, 4 + 2 * 4 / 5, 5)  # Offset along normal
    assert np.allclose(
        transformed_mesh.vertices[0], expected_vertex
    ), f"Expected {expected_vertex}, got {transformed_mesh.vertices[0]}"

def test_transform_cylindrical_vertex_negative_offset(transformation):
    vertex = (3, 4, 5)  # Cylindrical vertex
    offset = -2
    transformed_mesh = transformation.transform(Mesh(vertices=[vertex],
                                                     faces=[]), offset)
    expected_vertex = (3 - 2 * 3 / 5, 4 - 2 * 4 / 5, 5)  # Offset inward along normal
    assert np.allclose(
        transformed_mesh.vertices[0], expected_vertex
    ), f"Expected {expected_vertex}, got {transformed_mesh.vertices[0]}"

def test_transform_hemispherical_vertex_top(transformation):
    vertex = (0, 0, 12)  # Top of hemisphere
    offset = 2
    transformed_mesh = transformation.transform(Mesh(vertices=[vertex],
                                                     faces=[]), offset)
    expected_vertex = (0, 0, 12 + 2)  # Offset directly upward
    assert np.allclose(
        transformed_mesh.vertices[0], expected_vertex
    ), f"Expected {expected_vertex}, got {transformed_mesh.vertices[0]}"

def test_transform_hemispherical_vertex_slope(transformation):
    vertex = (3, 4, 12)  # Sloped hemisphere vertex
    offset = 2
    transformed_mesh = transformation.transform(Mesh(vertices=[vertex],
                                                     faces=[]), offset)
    normal = transformation.calculate_normal(vertex)
    expected_vertex = (
        vertex[0] + 2 * normal[0],
        vertex[1] + 2 * normal[1],
        vertex[2] + 2 * normal[2],
    )
    assert np.allclose(
        transformed_mesh.vertices[0], expected_vertex
    ), f"Expected {expected_vertex}, got {transformed_mesh.vertices[0]}"
