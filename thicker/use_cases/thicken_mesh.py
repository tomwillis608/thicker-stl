"""Shape thickening use case.
- It should take in a Mesh instance and an offset value as inputs.
- It should return a new, thickened Mesh instance.
"""

from thicker.domain.mesh import Mesh
from thicker.domain.transformations import thicken_mesh
from thicker.interfaces.mesh_reader import MeshReader
from thicker.interfaces.mesh_writer import MeshWriter


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


def process_thickening(
    reader: MeshReader,
    writer: MeshWriter,
    input_path: str,
    output_path: str,
    offset: float,
) -> None:
    """
    Use case: Read a mesh, apply thickening, and save it.
    As called by the CLI connector.
    """
    # Read the input mesh
    vertices, faces = reader.read(input_path)

    # Domain logic: Perform thickening
    mesh = Mesh(vertices=vertices, faces=faces)
    thickened_mesh = thicken_mesh(mesh, offset)

    # Write the thickened mesh
    writer.write(output_path, thickened_mesh.vertices, thickened_mesh.faces)
