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
