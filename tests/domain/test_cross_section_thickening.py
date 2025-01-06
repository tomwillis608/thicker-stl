"""Test cross-section thickening."""

import math

from thicker.domain.cross_section_thickening import thicken_cross_section
from thicker.domain.mesh import Mesh
from thicker.domain.slice import Slice


def test_thicken_cross_section():
    """
    Test that a narrow cross-section is correctly thickened.
    """
    # Vertices for a cylinder with a narrow waist at z=0.5
    vertices = [
        (1.0, 0.0, 0.0),  # Base
        # Narrow section
        (0.5, 0.0, 0.5),
        (0.0, 0.5, 0.5),
        (-0.5, 0.0, 0.5),
        (0.0, -0.5, 0.5),
        (1.0, 0.0, 1.0),  # Top
    ]
    faces = []  # Faces are not relevant for this test

    mesh = Mesh(vertices=vertices, faces=faces)

    # Define the narrow section and the offset
    offset = 0.2
    narrow_slice = Slice(
        vertices=[vertices[1], vertices[2], vertices[3], vertices[4]], z_height=0.5
    )
    narrow_slices = [ narrow_slice, ]

    # Apply the thickening transformation
    thickened_mesh = thicken_cross_section(mesh, narrow_slices, offset)

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

    assert math.isclose(thickened_mesh.vertices[5][0], (1.0, 0.0, 1.0)[0], rel_tol=1e-5)
    assert math.isclose(thickened_mesh.vertices[5][1], (1.0, 0.0, 1.0)[1], rel_tol=1e-5)
    assert math.isclose(thickened_mesh.vertices[5][2], (1.0, 0.0, 1.0)[2], rel_tol=1e-5)


def test_thicken_offset_cross_section():
    """
    Test that a narrow cross-section is correctly thickened.
    """
    # Vertices for a cylinder with a narrow waist at z=0.5
    # that is offset in y from the z-axis
    vertices = [
        (1.0, 2.0, 0.0),  # Base
        # Narrow section
        (0.5, 2.0, 0.5),
        (0.0, 2.5, 0.5),
        (-0.5, 2.0, 0.5),
        (0.0, -2.5, 0.5),
        (1.0, 2.0, 1.0),  # Top
    ]
    faces = []  # Faces are not relevant for this test

    mesh = Mesh(vertices=vertices, faces=faces)

    # Define the narrow section and the offset
    offset = 0.2
    narrow_slice = Slice(
        vertices=[vertices[1], vertices[2], vertices[3], vertices[4]], z_height=0.5
    )
    narrow_slices = [ narrow_slice, ]

    # Apply the thickening transformation
    thickened_mesh = thicken_cross_section(mesh, narrow_slices, offset)

    # Assert that the narrow section was thickened
    assert math.isclose(
        thickened_mesh.vertices[1][0], (0.7, 2.2, 0.5)[0], rel_tol=1e-5
    ), f"Expected vertex to be thickened, got {thickened_mesh.vertices[1]}"
    assert math.isclose(
        thickened_mesh.vertices[1][1], (0.7, 2.2, 0.5)[1], rel_tol=1e-5
    ), f"Expected vertex to be thickened, got {thickened_mesh.vertices[1]}"
    assert math.isclose(
        thickened_mesh.vertices[1][2], (0.7, 2.2, 0.5)[2], rel_tol=1e-5
    ), f"Expected vertex to be thickened, got {thickened_mesh.vertices[1]}"


    # Assert that other sections remain unchanged
    assert math.isclose(thickened_mesh.vertices[0][0], vertices[0][0], rel_tol=1e-5)
    assert math.isclose(thickened_mesh.vertices[0][1], vertices[0][1], rel_tol=1e-5)
    assert math.isclose(thickened_mesh.vertices[0][2], vertices[0][2], rel_tol=1e-5)

    assert math.isclose(thickened_mesh.vertices[5][0], vertices[5][0], rel_tol=1e-5)
    assert math.isclose(thickened_mesh.vertices[5][1], vertices[5][1], rel_tol=1e-5)
    assert math.isclose(thickened_mesh.vertices[5][2], vertices[5][2], rel_tol=1e-5)
