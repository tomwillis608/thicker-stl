"""Mesh transformations."""

from math import sqrt
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


def calculate_cylindrical_normal(
    vertex: Tuple[float, float, float],
) -> Tuple[float, float, float]:
    """
    Calculate the normal vector for a vertex in cylindrical coordinates.

    Args:
        vertex (Tuple[float, float, float]): The vertex coordinates (x, y, z).

    Returns:
        Tuple[float, float, float]: The normal vector (nx, ny, 0).
    """
    x, y, _ = vertex
    norm = np.linalg.norm([x, y])
    return (x / norm, y / norm, 0) if norm != 0 else (0, 0, 0)


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


class HemisphereToppedCylinderTransformation:
    """
    Transformation to apply a hemisphere-topped cylinder shape to a mesh.
    """

    def __init__(self, cylinder_height: float, radius: float):
        """
        Initialize the transformation.

        Args:
            cylinder_height (float): Height of the cylindrical region.
            radius (float): Radius of the cylinder and hemisphere.
        """
        self.cylinder_height = cylinder_height
        self.radius = radius

    def transform(self, mesh: Mesh) -> Mesh:
        """
        Transform the vertices of a mesh.

        Args:
            mesh (Mesh): The mesh to transform.

        Returns:
            Mesh: A new mesh with transformed vertices and unchanged faces.
        """
        transformed_vertices = [self._transform_vertex(v) for v in mesh.vertices]
        return Mesh(vertices=transformed_vertices, faces=mesh.faces)

    def _transform_vertex(self, vertex):
        """
        Transform a single vertex based on the hemisphere-topped cylinder logic.

        Args:
            vertex (Tuple[float, float, float]): The vertex to transform.

        Returns:
            Tuple[float, float, float]: Transformed vertex coordinates.
        """
        x, y, z = vertex
        radius = sqrt(x**2 + y**2)

        if z <= self.cylinder_height:
            # Cylindrical region: project x, y onto cylinder surface
            if radius == 0:
                return (0, 0, z)  # Handle center point case
            scale = self.radius / radius
            return (x * scale, y * scale, z)
        else:
            # Hemisphere region: normalize and scale to radius
            norm = sqrt(x**2 + y**2 + z**2)
            return (
                x / norm * self.radius,
                y / norm * self.radius,
                z / norm * self.radius,
            )
