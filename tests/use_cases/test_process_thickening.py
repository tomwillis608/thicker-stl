"""Test the process_thickening_ori use case method."""

import math
from unittest.mock import Mock

import pytest

from thicker.domain.mesh import Mesh
from thicker.use_cases.thicken_mesh import (
    calculate_mesh_radius,
    process_thickening,
    process_thickening_ori,
)


def test_process_thickening_ori():
    # Mock reader and writer
    mock_reader = Mock()
    mock_writer = Mock()

    # Mock input data
    mock_reader.read.return_value = (
        [(0.0, 0.0, 1.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)],
        [(0, 1, 2)],
    )
    mock_writer.write.return_value = None

    # Run the process
    process_thickening_ori(mock_reader, mock_writer, "input.stl", "output.stl", 0.1)

    # Assertions
    mock_reader.read.assert_called_once()
    mock_writer.write.assert_called_once()


def test_process_thickening():
    # Mock reader and writer
    mock_reader = Mock()
    mock_writer = Mock()

    # Mock input data
    mock_reader.read.return_value = (
        [(0.0, 0.0, 1.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)],
        [(0, 1, 2)],
    )
    mock_writer.write.return_value = None

    # Run the process
    process_thickening(mock_reader, mock_writer, "input.stl", "output.stl", 0.1)

    # Assertions
    mock_reader.read.assert_called_once()
    mock_writer.write.assert_called_once()


def test_calculate_mesh_radius_excludes_base():
    """
    Test that the mesh radius calculation ignores vertices in the bottom
    19% of the figure's height.
    """

    # Create a simple mesh with a base and figure
    vertices = [
        # Base vertices
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (-1.0, 0.0, 0.0),
        (0.0, -1.0, 0.0),
        # Figure vertices (above base)
        (0.5, 0.0, 1.0),
        (0.0, 0.5, 1.0),
        (-0.5, 0.0, 1.0),
        (0.0, -0.5, 1.0),
    ]
    faces = []  # Faces are irrelevant for this test
    mesh = Mesh(vertices=vertices, faces=faces)

    # Calculate radius
    radius = calculate_mesh_radius(mesh)

    # The radius should be calculated from vertices above 0.38 (19% of 2.0)
    # Expected max radius should be 0.5 (ignoring the lower vertices)
    expected_radius = 0.5
    assert math.isclose(
        radius, expected_radius, rel_tol=1e-09, abs_tol=1e-09
    ), f"Expected radius {expected_radius}, got {radius}"


def test_calculate_radius_no_vertices_above_base():
    """
    Test that calculate_mesh_radius raises a ValueError if no vertices are found
    above the base height.
    """
    # Create a mesh where all vertices are at or below the base height
    vertices = [
        (1, 0, 0),  # All vertices at z = 0
        (0, 1, 0),
        (-1, 0, 0),
        (0, -1, 0),
    ]
    faces = []  # Faces are irrelevant for this test
    mesh = Mesh(vertices=vertices, faces=faces)

    # Expect a ValueError to be raised
    with pytest.raises(ValueError, match="No vertices found above the base height."):
        calculate_mesh_radius(mesh)


def test_calculate_radius_one_vertex_above_base():
    """
    Test that the function calculates the radius correctly for a mesh with only
    one vertex above the base height.
    """
    vertices = [
        (1, 0, 0),  # Base vertex (ignored)
        (0, 1, 0),  # Base vertex (ignored)
        (0, 0, 5),  # One vertex above base height
    ]
    mesh = Mesh(vertices=vertices, faces=[])

    # Expected radius is the distance from the z-axis to (0, 0, 5)
    expected_radius = 0.0

    radius = calculate_mesh_radius(mesh)
    assert math.isclose(
        radius, expected_radius, rel_tol=1e-09, abs_tol=1e-09
    ), f"Expected radius {expected_radius}, got {radius}"


def test_calculate_radius_empty_mesh():
    """
    Test that an empty mesh raises a ValueError.
    """
    mesh = Mesh(vertices=[], faces=[])

    with pytest.raises(ValueError, match="Mesh contains no vertices."):
        calculate_mesh_radius(mesh)
