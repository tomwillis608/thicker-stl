"""Shape thickening use case.
- It should take in a Mesh instance and an offset value as inputs.
- It should return a new, thickened Mesh instance.
"""

from thicker.domain.mesh import Mesh
from thicker.domain.transformations import (
    HemisphericalCylinderTransformation,
    calculate_cylindrical_normal,
    calculate_spherical_normal,
    thicken_mesh,
)
from thicker.interfaces.mesh_reader import MeshReader
from thicker.interfaces.mesh_writer import MeshWriter
from thicker.use_cases.constants import BASE_HEIGHT_PERCENTAGE


def thicken_a_mesh(original_mesh: Mesh, offset: float) -> Mesh:
    """Shape Thickening use case.
    Apply thickening transformation to a mesh.
    Args:
        original_mesh (Mesh): The original mesh to be thickened.
        offset (float): The amount to thicken each vertex.

    Returns:
        Mesh: A new Mesh instance with thickened vertices.
    """
    new_mesh = thicken_mesh(original_mesh, offset, calculate_spherical_normal)
    return new_mesh


def process_thickening_ori(
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
    thickened_mesh = thicken_mesh(mesh, offset, calculate_cylindrical_normal)

    # Write the thickened mesh
    writer.write(output_path, thickened_mesh.vertices, thickened_mesh.faces)


def calculate_mesh_height(mesh: Mesh) -> float:
    """
    Calculate the height of a given mesh based on its vertices.

    Args:
        mesh: A Mesh object containing vertices and faces.

    Returns:
        float: The height of the mesh, defined as the difference between the
               maximum and minimum z-coordinate values.
    """
    if not mesh.vertices:
        raise ValueError("Mesh contains no vertices.")

    # Extract the z-coordinates from the vertices
    z_coordinates = [vertex[2] for vertex in mesh.vertices]

    return max(z_coordinates) - min(z_coordinates)


def calculate_mesh_radius(mesh: Mesh) -> float:
    """
    Calculate the radius of a given mesh based on vertices above the base height.

    Args:
        mesh: A Mesh object containing vertices and faces.

    Returns:
        float: The radius of the mesh, defined as the maximum distance from
               the z-axis (0, 0) to any vertex in the x-y plane, excluding the base.

    Raises:
        ValueError: If the mesh has no vertices above the base height.
    """
    if not mesh.vertices:
        raise ValueError("Mesh contains no vertices.")

    base_height = BASE_HEIGHT_PERCENTAGE * calculate_mesh_height(mesh)

    # Filter vertices above the base height
    vertices_above_base = [(x, y) for x, y, z in mesh.vertices if z > base_height]

    if not vertices_above_base:
        raise ValueError("No vertices found above the base height.")

    # Compute squared distances from the z-axis for each vertex
    squared_distances = [x**2 + y**2 for x, y in vertices_above_base]

    # Return the square root of the maximum squared distance as the radius
    return max(squared_distances) ** 0.5


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
    # Domain: create the mesh
    mesh = Mesh(vertices=vertices, faces=faces)
    # Use case: calculate mesh dimensions
    mesh_height = calculate_mesh_height(mesh)
    print(f"Mesh height: {mesh_height}")
    mesh_radius = calculate_mesh_radius(mesh)
    print(f"Mesh radius: {mesh_radius}")
    cylinder_height = mesh_height - mesh_radius
    print(f"Cylinder height: {cylinder_height}")
    # Domain: setup transformation
    transformation = HemisphericalCylinderTransformation(cylinder_height, mesh_radius)
    # Domain logic: Perform thickening

    thickened_mesh = transformation.transform(mesh, offset)

    # Write the thickened mesh
    writer.write(output_path, thickened_mesh.vertices, thickened_mesh.faces)
