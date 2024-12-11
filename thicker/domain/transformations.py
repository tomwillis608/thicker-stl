"""Mesh transformations."""

from thicker.domain.mesh import Mesh


def unity_transformation(mesh: Mesh) -> Mesh:
    """A transformation that returns the mesh unchanged."""
    return mesh
