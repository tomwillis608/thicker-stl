""" test the Slice class. """

from thicker.domain.slice import Slice


def test_slice_initialization():
    """
    Test that a Slice object initializes correctly with vertices and z_height.
    """
    vertices = [(0.5, 0.2, 0.5), (0.4, -0.1, 0.5), (0.6, 0.1, 0.5)]
    z_height = 0.5

    slice_obj = Slice(vertices=vertices, z_height=z_height)

    assert slice_obj.vertices == vertices
    assert slice_obj.z_height == z_height


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
