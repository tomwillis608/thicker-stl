"""test the Slice class."""

import math

from thicker.domain.slice import Slice


def test_slice_initialization():
    """
    Test that a Slice object initializes correctly with vertices and z_height.
    """
    vertices = [(0.5, 0.2, 0.5), (0.4, -0.1, 0.5), (0.6, 0.1, 0.5)]
    z_height = 0.5

    slice_obj = Slice(vertices=vertices, z_height=z_height)

    assert slice_obj.vertices == vertices
    assert math.isclose(slice_obj.z_height, z_height)


def test_slice_centroid():
    """
    Test that the centroid of a Slice is calculated correctly.
    """
    vertices = [(0.0, 0.0, 0.5), (1.0, 0.0, 0.5), (0.0, 1.0, 0.5), (1.0, 1.0, 0.5)]
    z_height = 0.5
    slice_obj = Slice(vertices=vertices, z_height=z_height)

    expected_centroid = (0.5, 0.5)
    assert (
        slice_obj.centroid() == expected_centroid
    ), f"Expected centroid {expected_centroid}, got {slice_obj.centroid()}"


def test_slice_centroid_irregular():
    """
    Test that the centroid of a Slice is correctly calculated for irregular vertices.
    """
    vertices = [(2.0, 3.0, 0.5), (3.0, 4.0, 0.5), (4.0, 3.0, 0.5)]
    z_height = 0.5
    slice_obj = Slice(vertices=vertices, z_height=z_height)

    expected_centroid = (3.0, 3.3333333333333335)  # (sum of x) / 3, (sum of y) / 3
    assert (
        slice_obj.centroid() == expected_centroid
    ), f"Expected centroid {expected_centroid}, got {slice_obj.centroid()}"


def test_slice_empty_vertices():
    """
    Test that a Slice with no vertices returns a (0.0, 0.0) centroid.
    """
    vertices = []
    z_height = 0.5
    slice_obj = Slice(vertices=vertices, z_height=z_height)

    expected_centroid = (0.0, 0.0)
    assert (
        slice_obj.centroid() == expected_centroid
    ), f"Expected centroid {expected_centroid}, got {slice_obj.centroid()}"


def test_slice_single_vertex():
    """
    Test that the centroid is the single vertex itself when there is only one vertex.
    """
    vertices = [(1.0, 2.0, 0.5)]
    z_height = 0.5
    slice_obj = Slice(vertices=vertices, z_height=z_height)

    expected_centroid = (1.0, 2.0)
    assert (
        slice_obj.centroid() == expected_centroid
    ), f"Expected centroid {expected_centroid}, got {slice_obj.centroid()}"


def test_slice_collinear_vertices():
    """
    Test that the centroid is correctly calculated for collinear vertices.
    """
    vertices = [(1.0, 2.0, 0.5), (2.0, 4.0, 0.5), (3.0, 6.0, 0.5)]
    z_height = 0.5
    slice_obj = Slice(vertices=vertices, z_height=z_height)

    expected_centroid = (2.0, 4.0)  # The average of x and y coordinates
    assert (
        slice_obj.centroid() == expected_centroid
    ), f"Expected centroid {expected_centroid}, got {slice_obj.centroid()}"


def test_slice_repr_no_vertices():
    """
    Test the __repr__ method when the Slice has no vertices.
    """
    slice_obj = Slice(vertices=[], z_height=1.0)

    expected = "Slice(z_height=1.00, num_vertices=0, vertices=[])"
    assert repr(slice_obj) == expected, f"Unexpected repr: {repr(slice_obj)}"


def test_slice_repr_few_vertices():
    """
    Test the __repr__ method when the Slice has fewer than 3 vertices.
    """
    vertices = [(1.0, 2.0, 0.0), (0.5, 1.5, 0.5)]
    slice_obj = Slice(vertices=vertices, z_height=0.5)

    expected = (
        "Slice(z_height=0.50, num_vertices=2, "
        "vertices=[(1.0, 2.0, 0.0), (0.5, 1.5, 0.5)])"
    )
    assert repr(slice_obj) == expected, f"Unexpected repr: {repr(slice_obj)}"


def test_slice_repr_exactly_three_vertices():
    """
    Test the __repr__ method when the Slice has exactly 3 vertices.
    """
    vertices = [(1.0, 2.0, 0.0), (0.5, 1.5, 0.5), (0.7, 1.8, 1.0)]
    slice_obj = Slice(vertices=vertices, z_height=0.5)

    expected = (
        "Slice(z_height=0.50, num_vertices=3, "
        "vertices=[(1.0, 2.0, 0.0), (0.5, 1.5, 0.5), (0.7, 1.8, 1.0)])"
    )
    assert repr(slice_obj) == expected, f"Unexpected repr: {repr(slice_obj)}"


def test_slice_repr_more_than_three_vertices():
    """
    Test the __repr__ method when the Slice has more than 3 vertices.
    """
    vertices = [
        (1.0, 2.0, 0.0),
        (0.5, 1.5, 0.5),
        (0.7, 1.8, 1.0),
        (1.2, 2.3, 1.5),
        (0.9, 1.6, 2.0),
    ]
    slice_obj = Slice(vertices=vertices, z_height=1.0)

    expected = (
        "Slice(z_height=1.00, num_vertices=5, "
        "vertices=[(1.0, 2.0, 0.0), (0.5, 1.5, 0.5), (0.7, 1.8, 1.0)], ...)"
    )
    assert repr(slice_obj) == expected, f"Unexpected repr: {repr(slice_obj)}"


def test_slice_vertices_inequality():
    """Test slice inequality in vertices."""
    slice_left = Slice(
        vertices=[
            (0.4, 0.0, 0.5),
            (0.0, 0.4, 0.5),
            (-0.4, 0.0, 0.5),
            (0.0, -0.4, 0.5),
        ],
        z_height=0.5,
    )
    slice_right = Slice(
        vertices=[
            (0.4, 0.0, 0.5),
            (0.0, 0.4, 0.5),
        ],
        z_height=0.5,
    )
    assert slice_left != slice_right, f"Expect {slice_left} != {slice_right}"


def test_slice_z_height_inequality():
    """Test slice inequality in z_height."""
    slice_left = Slice(
        vertices=[
            (0.4, 0.0, 0.5),
            (0.0, 0.4, 0.5),
            (-0.4, 0.0, 0.5),
            (0.0, -0.4, 0.5),
        ],
        z_height=0.5,
    )
    slice_right = Slice(
        vertices=[
            (0.4, 0.0, 0.5),
            (0.0, 0.4, 0.5),
            (-0.4, 0.0, 0.5),
            (0.0, -0.4, 0.5),
        ],
        z_height=0.2,
    )
    assert slice_left != slice_right, f"Expect {slice_left} != {slice_right}"


def test_slice_vertices_equality():
    """Test slice equality method."""
    slice_left = Slice(
        vertices=[
            (0.4, 0.0, 0.5),
            (0.0, 0.4, 0.5),
            (-0.4, 0.0, 0.5),
            (0.0, -0.4, 0.5),
        ],
        z_height=0.5,
    )
    slice_right = Slice(
        vertices=[
            (0.4, 0.0, 0.5),
            (0.0, 0.4, 0.5),
            (-0.4, 0.0, 0.5),
            (0.0, -0.4, 0.5),
        ],
        z_height=0.5,
    )
    assert slice_left == slice_right, f"Expect {slice_left} == {slice_right}"
