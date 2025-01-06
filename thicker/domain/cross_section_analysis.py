"""Cross-section analysis of meshes."""

from thicker.domain.mesh import Mesh
from thicker.domain.slice import Slice


def detect_narrow_cross_sections(mesh: Mesh, threshold: float = 0.5) -> list[Slice]:
    """
    Detect narrow cross-sections in a given mesh.

    Args:
        mesh: The Mesh object containing vertices and faces.
        threshold: The minimum allowable radius for a cross-section.

    Returns:
        A list of Slices where the cross-section radius is below the threshold.
    """
    narrow_sections = []
    z_values = [z for _, _, z in mesh.vertices]

    # Determine the height range of the mesh
    min_z = min(z_values)
    max_z = max(z_values)
    num_slices = 100  # Number of horizontal slices to analyze

    slice_height = (max_z - min_z) / num_slices

    for i in range(num_slices):
        slice_z_min = min_z + i * slice_height
        slice_z_max = slice_z_min + slice_height

        # Get vertices in this slice
        slice_vertices = [
            (x, y, z) for x, y, z in mesh.vertices if slice_z_min <= z < slice_z_max
        ]

        if not slice_vertices:
            continue  # Skip empty slices

        # Calculate the max distance from the z-axis
        max_radius = max((x ** 2 + y ** 2) ** 0.5 for x, y, _ in slice_vertices)

        # Check if the radius is below the threshold
        if max_radius < threshold:
            narrow_sections.append(Slice(slice_vertices, slice_z_min))

    return narrow_sections
