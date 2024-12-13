"""Test vertex calculations."""

import pytest

from thicker.domain.transformations import calculate_vertex_normal


def test_calculate_vertex_normal_unit_vector():
    """A unit vector should return itself as the normal."""
    assert calculate_vertex_normal((1, 0, 0)) == (1, 0, 0)
    assert calculate_vertex_normal((0, 1, 0)) == (0, 1, 0)
    assert calculate_vertex_normal((0, 0, 1)) == (0, 0, 1)


def test_calculate_vertex_normal_arbitrary_vector():
    """A non-unit vector should return its normalized form."""
    result = calculate_vertex_normal((3, 0, 4))
    assert pytest.approx(result, rel=1e-2) == (0.6, 0, 0.8)


def test_calculate_vertex_normal_zero_vector():
    """A zero vector should return (0, 0, 0) as the normal."""
    assert calculate_vertex_normal((0, 0, 0)) == (0, 0, 0)
