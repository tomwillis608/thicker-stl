""" Test cross-section analysis domain code."""

from thicker.domain.cross_section_analysis import detect_narrow_cross_sections
from thicker.domain.mesh import Mesh


def test_no_narrow_cross_sections_in_uniform_cylinder():
    """
    Test that no narrow cross-sections are detected in a simple uniform cylinder.
    """
    # Hardcoded vertex and face data for a simple unit cylinder
    vertices = [
        (1, 0, 0),  # Point on circumference, bottom
        (0, 1, 0),  # Point on circumference, bottom
        (-1, 0, 0),  # Point on circumference, bottom
        (0, -1, 0),  # Point on circumference, bottom
        (1, 0, 1),  # Point on circumference, top
        (0, 1, 1),  # Point on circumference, top
        (-1, 0, 1),  # Point on circumference, top
        (0, -1, 1),  # Point on circumference, top
    ]

    faces = [
        (0, 1, 4),
        (1, 5, 4),  # Side faces
        (1, 2, 5),
        (2, 6, 5),  # Side faces
        (2, 3, 6),
        (3, 7, 6),  # Side faces
        (3, 0, 7),
        (0, 4, 7),  # Side faces
        (0, 1, 2, 3),  # Bottom cap
        (4, 5, 6, 7),  # Top cap
    ]

    # Create the mesh
    mesh = Mesh(vertices=vertices, faces=faces)

    # Run the narrow cross-section detection
    narrow_sections = detect_narrow_cross_sections(mesh, threshold=0.5)

    # Assert that no narrow cross-sections were found
    assert (
        narrow_sections == []
    ), f"Expected no narrow cross-sections, but found {narrow_sections}"


def test_detect_narrow_waist():
    """
    Test to detect a narrow waist feature in a cylindrical mesh.
    The mesh has a wide base, a narrow middle section (waist),
    and a wide top.
    """
    # Create vertices for a mesh with a narrow waist
    vertices = [
        # Base section (radius 1.0)
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (-1.0, 0.0, 0.0),
        (0.0, -1.0, 0.0),
        # Narrow waist (radius 0.4)
        (0.4, 0.0, 0.5),
        (0.0, 0.4, 0.5),
        (-0.4, 0.0, 0.5),
        (0.0, -0.4, 0.5),
        # Top section (radius 1.0)
        (1.0, 0.0, 1.0),
        (0.0, 1.0, 1.0),
        (-1.0, 0.0, 1.0),
        (0.0, -1.0, 1.0),
    ]

    # Faces are not relevant for cross-section detection
    faces = []

    # Create the Mesh object
    mesh = Mesh(vertices=vertices, faces=faces)

    # Call the function with a threshold of 0.5
    narrow_sections = detect_narrow_cross_sections(mesh, threshold=0.5)

    # Validate that the narrow section is detected at the expected height
    assert narrow_sections == [
        0.5
    ], f"Expected narrow section at z=0.5, got {narrow_sections}"
