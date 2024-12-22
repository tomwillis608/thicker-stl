"""Mesh transformations."""

from typing import Callable, Tuple

import numpy as np

from thicker.domain.mesh import Mesh


def unity_transformation(mesh: Mesh) -> Mesh:
    """A transformation that returns the mesh unchanged."""
    return mesh


def calculate_spherical_normal(
    vertex: Tuple[float, float, float],
) -> Tuple[float, float, float]:
    """
    Calculate the normal vector for a given vertex in spherical coordinates.

    Args:
        vertex (Tuple[float, float, float]): The vertex coordinates (x, y, z).

    Returns:
        Tuple[float, float, float]: The normalized vector (nx, ny, nz).
    """
    x, y, z = vertex
    norm = np.linalg.norm([x, y, z])
    return (x / norm, y / norm, z / norm) if norm != 0 else (0, 0, 0)


def thicken_mesh(
    mesh: Mesh,
    offset: float,
    normal_calculator: Callable[
        [Tuple[float, float, float]], Tuple[float, float, float]
    ],
) -> Mesh:
    """
    Apply a simple spherical thickening transformation to a mesh.

    Args:
        mesh (Mesh): The original mesh to be thickened.
        offset (float): The amount to thicken each vertex.
        normal_calculator (Callable): A function to calculate the normal vector.

    Returns:
        Mesh: A new Mesh instance with thickened vertices.
    """
    # Apply the offset along the normal vector for each vertex
    new_vertices = []
    for vertex in mesh.vertices:
        normal = normal_calculator(vertex)
        thickened_vertex = (
            vertex[0] + normal[0] * offset,
            vertex[1] + normal[1] * offset,
            vertex[2] + normal[2] * offset,
        )
        new_vertices.append(thickened_vertex)

    # Return a new Mesh instance with updated vertices
    return Mesh(vertices=new_vertices, faces=mesh.faces)
