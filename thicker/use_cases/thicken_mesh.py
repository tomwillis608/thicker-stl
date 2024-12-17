"""Shape thickening use case.
- It should take in a Mesh instance and an offset value as inputs.
- It should return a new, thickened Mesh instance.
"""

from thicker.domain.mesh import Mesh
from thicker.domain.transformations import thicken_mesh


def thicken_a_mesh(original_mesh: Mesh, offset: float) -> Mesh:
    """Shape Thickening use case.
    Apply thickening transformation to a mesh.
    Args:
        original_mesh (Mesh): The original mesh to be thickened.
        offset (float): The amount to thicken each vertex.

    Returns:
        Mesh: A new Mesh instance with thickened vertices.
    """
    new_mesh = thicken_mesh(original_mesh, offset)
    return new_mesh
