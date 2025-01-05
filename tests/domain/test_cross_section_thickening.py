""" Test cross-section thickening. """

import math

from thicker.domain.cross_section_thickening import thicken_cross_section
from thicker.domain.mesh import Mesh


def test_thicken_cross_section():
    """
    Test that a narrow cross-section is correctly thickened.
    """
    # Vertices for a cylinder with a narrow waist at z=0.5
    vertices = [
        (1.0, 0.0, 0.0),  # Base
        (0.5, 0.0, 0.5),  # Narrow section
        (1.0, 0.0, 1.0),  # Top
    ]
    faces = []  # Faces are not relevant for this test

    mesh = Mesh(vertices=vertices, faces=faces)

    # Define the narrow section and the offset
    narrow_sections = [0.5]
    offset = 0.2

    # Apply the thickening transformation
    thickened_mesh = thicken_cross_section(mesh, narrow_sections, offset)

    # Assert that the narrow section was thickened
    assert math.isclose(
        thickened_mesh.vertices[1][0], (0.7, 0.0, 0.5)[0], rel_tol=1e-5
    ), f"Expected vertex to be thickened, got {thickened_mesh.vertices[1]}"
    assert math.isclose(
        thickened_mesh.vertices[1][1], (0.7, 0.0, 0.5)[1], rel_tol=1e-5
    ), f"Expected vertex to be thickened, got {thickened_mesh.vertices[1]}"
    assert math.isclose(
        thickened_mesh.vertices[1][2], (0.7, 0.0, 0.5)[2], rel_tol=1e-5
    ), f"Expected vertex to be thickened, got {thickened_mesh.vertices[1]}"

    # Assert that other sections remain unchanged
    assert math.isclose(thickened_mesh.vertices[0][0], (1.0, 0.0, 0.0)[0], rel_tol=1e-5)
    assert math.isclose(thickened_mesh.vertices[0][1], (1.0, 0.0, 0.0)[1], rel_tol=1e-5)
    assert math.isclose(thickened_mesh.vertices[0][2], (1.0, 0.0, 0.0)[2], rel_tol=1e-5)

    assert math.isclose(thickened_mesh.vertices[2][0], (1.0, 0.0, 1.0)[0], rel_tol=1e-5)
    assert math.isclose(thickened_mesh.vertices[2][1], (1.0, 0.0, 1.0)[1], rel_tol=1e-5)
    assert math.isclose(thickened_mesh.vertices[2][2], (1.0, 0.0, 1.0)[2], rel_tol=1e-5)
