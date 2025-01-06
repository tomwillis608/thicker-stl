"""Thicken narrow cross-sections."""

import math
from typing import Tuple

from thicker.domain.mesh import Mesh
from thicker.domain.slice import Slice


def thicken_cross_section(
    mesh: Mesh, narrow_sections: list[Slice], offset: float
) -> Mesh:
    threshold = 1.0
    thickener = CrossSectionThickener(threshold, offset)
    thickened_mesh = thickener.thicken(mesh, narrow_sections)
    assert isinstance(thickened_mesh, Mesh), "Argument of wrong type!"
    return thickened_mesh


class CrossSectionThickener:
    def __init__(self, threshold: float, offset: float):
        self.threshold = threshold
        self.offset = offset

    def thicken_vertex(
        self,
        vertex: Tuple[float, float, float],
        centroid: Tuple[float, float],
    ) -> Tuple[float, float, float]:
        """
        Thicken a vertex away from the centroid.

        :param vertex: The original vertex in a narrow cross-section.
        :param centroid: The centroid in the narrow cross-section to move away from.

        :return: The thickened vertex, moved away from the centroid.

        Calculate the vector from the centroid to the vertex.
        Scale this vector outward by the offset.
            𝑣_thickened = 𝑣_original + (𝑣_original - centroid)
                / abs((𝑣_original - centroid) * offset
        Equivalent maths:
            𝑣_thickened = 𝑣_original + math.copysign(offset, (𝑣_original - centroid))
        """
        if math.isclose(vertex[0], centroid[0]):
            delta_x = 0.0
        else:
            delta_x = math.copysign(self.offset, vertex[0] - centroid[0])

        if math.isclose(vertex[1], centroid[1]):
            delta_y = 0.0
        else:
            delta_y = math.copysign(self.offset, vertex[1] - centroid[1])

        new_vertex = (
            vertex[0] + delta_x,
            vertex[1] + delta_y,
            vertex[2],  # No thickening in z-direction
        )
        return new_vertex

    def thicken(self, mesh: Mesh, narrow_sections: list[Slice]) -> Mesh:
        """
        Thicken the narrow cross-sections of the mesh.

        Args:
            mesh: The original mesh to be thickened.
            narrow_sections: A list of Slices where narrow cross-sections
                were detected.

        Returns:
            A new Mesh object with thickened cross-sections.
        """
        new_vertices = []
        slice_vertices = []
        for narrow_section in narrow_sections:
            for vertex in narrow_section.vertices:
                slice_vertices.append(vertex)

        for x, y, z in mesh.vertices:
            if (x, y, z) in slice_vertices:
                new_vertex = self.get_thickened_vertex(x, y, z, narrow_sections)
                new_vertices.append(new_vertex)
            else:
                new_vertices.append((x, y, z))
        return Mesh(vertices=new_vertices, faces=mesh.faces)

    def get_thickened_vertex(
        self, x: float, y: float, z: float, narrow_sections: list[Slice]
    ) -> Tuple[float, float, float]:
        """ Adjust vertices at detected narrow sections. """
        for narrow_slice in narrow_sections:
            if (x, y, z) in narrow_slice.vertices:
                # Thicken according to the slice centroid
                # Move x and y radially from the slice centroid
                slice_centroid = narrow_slice.centroid()
                new_vertex = self.thicken_vertex(
                    vertex=(x, y, z),
                    centroid=slice_centroid,
                )
                return new_vertex
