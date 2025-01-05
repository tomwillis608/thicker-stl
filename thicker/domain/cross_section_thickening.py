""" Thicken narrow cross-sections. """

import math

from thicker.domain.mesh import Mesh


def thicken_cross_section(mesh: Mesh, narrow_sections, offset: float) -> Mesh:
    threshold = 1.0
    thickener = CrossSectionThickener(threshold, offset)
    thickened_mesh = thickener.thicken(mesh, narrow_sections)
    assert isinstance(thickened_mesh, Mesh), "Argument of wrong type!"
    return thickened_mesh


class CrossSectionThickener:
    def __init__(self, threshold: float, offset: float):
        self.threshold = threshold
        self.offset = offset

    def thicken(self, mesh: Mesh, narrow_sections: list[float]) -> Mesh:
        """
        Thicken the narrow cross sections of the mesh.

        Args:
            mesh: The original mesh to be thickened.
            narrow_sections: A list of z-heights where narrow cross sections
                were detected.

        Returns:
            A new Mesh object with thickened cross sections.
        """
        new_vertices = []
        for x, y, z in mesh.vertices:
            # Adjust vertices at detected narrow sections
            if any(math.isclose(z, height, abs_tol=0.01) for height in narrow_sections):
                distance = (x ** 2 + y ** 2) ** 0.5
                factor = (distance + self.offset) / distance
                new_x = x * factor
                new_y = y * factor
                new_vertices.append((new_x, new_y, z))
            else:
                new_vertices.append((x, y, z))

        return Mesh(vertices=new_vertices, faces=mesh.faces)
