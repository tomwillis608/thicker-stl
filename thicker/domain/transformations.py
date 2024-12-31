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

    def transform(self, mesh: Mesh, offset: float) -> Mesh:
        """
        Transform the vertices of a mesh.

        Args:
            mesh (Mesh): The mesh to transform.
            offset (float): distance to move each vertex in the
                transformation direction.

        Returns:
            Mesh: A new mesh with transformed vertices and unchanged faces.
        """
        transformed_vertices = [self._transform_vertex(v, offset)
                                for v in mesh.vertices]
        return Mesh(vertices=transformed_vertices, faces=mesh.faces)

    def _transform_vertex(self, vertex: Tuple[float, float, float], offset: float) -> \
            Tuple[float, float, float]:
        """
        Transform a single vertex based on the hemisphere-topped cylinder logic.

        Args:
            vertex (Tuple[float, float, float]): The vertex to transform.

        Returns:
            Tuple[float, float, float]: Transformed vertex coordinates.
        """
        # x, y, z = vertex
        normal = self.calculate_normal(vertex)
        transformed_vertex = (
            vertex[0] + offset * normal[0],
            vertex[1] + offset * normal[1],
            vertex[2] + offset * normal[2],
        )
        return transformed_vertex

    def calculate_normal(self, vertex: tuple) -> tuple:

        """
        Calculate the normal vector for a vertex in the context of a
        hemisphere-topped cylinder transformation.

        The normal direction depends on whether the vertex is in the
        cylindrical region or the hemispherical region.

        Args:
            vertex (tuple): A tuple (x, y, z) representing the vertex coordinates.

        Returns:
            tuple: The normalized vector (nx, ny, nz), indicating the normal direction.

        Cylindrical Region:
        -------------------
        For vertices within the cylinder (z <= cylinder_height):
        The normal vector is perpendicular to the z-axis and lies in the x-y plane.

        The formula for the normal vector is:
        \\[
        \\mathbf{n} = \frac{(x, y, 0)}{\\sqrt{x^2 + y^2}}
        \\]
        If \\(\\sqrt{x^2 + y^2} = 0\\), the normal is (0, 0, 0).

        Hemispherical Region:
        ----------------------
        For vertices in the hemispherical cap (z > cylinder_height):
        The normal vector points radially outward from the center of the hemisphere.

        Let the center of the hemisphere be:
        \\[
        \\mathbf{c} = (0, 0, \text{cylinder_height})
        \\]

        The vector from the center to the vertex is:
        \\[
        \\mathbf{v} = (x - c_x, y - c_y, z - c_z)
        \\]

        The normal vector is:
        \\[
        \\mathbf{n} = \frac{\\mathbf{v}}{\\|\\mathbf{v}\\|}
        \\]
        where \\(\\|\\mathbf{v}\\| = \\sqrt{(x - c_x)^2 + (y - c_y)^2 + (z - c_z)^2}\\).
        If \\(\\|\\mathbf{v}\\| = 0\\), the normal is (0, 0, 0).
        """
        x, y, z = vertex
        if z <= self.cylinder_height:  # Cylindrical region
            norm = np.linalg.norm([x, y, 0])
            return (x / norm, y / norm, 0) if norm != 0 else (0, 0, 0)
        else:  # Hemispherical region
            center = (0, 0, self.cylinder_height)
            vector = (x - center[0], y - center[1], z - center[2])
            norm = np.linalg.norm(vector)
            return (vector[0] / norm, vector[1] / norm, vector[2] / norm) \
                if norm != 0 else (0, 0, 0)
