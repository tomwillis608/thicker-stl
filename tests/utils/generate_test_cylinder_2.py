import numpy as np
from stl import mesh


def generate_vertices_with_rings(
    radius, height, radial_segments, height_segments, cap_resolution
):
    """Generate vertices for a cylindrical mesh with concentric ring caps."""
    vertices = []

    # Side vertices
    for i in range(radial_segments):
        theta = 2 * np.pi * i / radial_segments
        for j in range(height_segments + 1):
            z = height * j / height_segments
            x = radius * np.cos(theta)
            y = radius * np.sin(theta)
            vertices.append((x, y, z))

    # Bottom cap center vertex
    vertices.append((0, 0, 0))
    bottom_center_index = len(vertices) - 1

    # Bottom cap rings
    for r in range(cap_resolution):
        ring_radius = radius * (cap_resolution - r) / cap_resolution
        for i in range(radial_segments):
            theta = 2 * np.pi * i / radial_segments
            x = ring_radius * np.cos(theta)
            y = ring_radius * np.sin(theta)
            z = 0
            vertices.append((x, y, z))

    # Top cap center vertex
    vertices.append((0, 0, height))
    top_center_index = len(vertices) - 1

    # Top cap rings
    for r in range(cap_resolution):
        ring_radius = radius * (cap_resolution - r) / cap_resolution
        for i in range(radial_segments):
            theta = 2 * np.pi * i / radial_segments
            x = ring_radius * np.cos(theta)
            y = ring_radius * np.sin(theta)
            z = height
            vertices.append((x, y, z))

    return vertices, bottom_center_index, top_center_index


def generate_faces(
    radius,
    height,
    radial_segments,
    height_segments,
    cap_resolution,
    vertices,
    bottom_center_index,
    top_center_index,
):
    """Generate faces for a cylindrical mesh with concentric ring caps."""
    faces = []

    # Side faces
    for i in range(radial_segments):
        for j in range(height_segments):
            v0 = i * (height_segments + 1) + j
            v1 = ((i + 1) % radial_segments) * (height_segments + 1) + j
            v2 = v0 + 1
            v3 = v1 + 1

            faces.append((v0, v1, v2))
            faces.append((v2, v1, v3))

    # Bottom cap faces
    base_index = radial_segments * (height_segments + 1)
    for r in range(cap_resolution - 1):
        ring_start = base_index + r * radial_segments
        next_ring_start = base_index + (r + 1) * radial_segments
        for i in range(radial_segments):
            v0 = ring_start + i
            v1 = ring_start + (i + 1) % radial_segments
            v2 = next_ring_start + i
            v3 = next_ring_start + (i + 1) % radial_segments

            faces.append((v0, v1, v2))
            faces.append((v2, v1, v3))

    # Connect the innermost ring to the bottom center
    innermost_ring_start = base_index + (cap_resolution - 1) * radial_segments
    for i in range(radial_segments):
        v0 = innermost_ring_start + i
        v1 = innermost_ring_start + (i + 1) % radial_segments
        faces.append((v0, v1, bottom_center_index))

    # Top cap faces
    base_index = (
        radial_segments * (height_segments + 1) + radial_segments * cap_resolution
    )
    for r in range(cap_resolution - 1):
        ring_start = base_index + r * radial_segments
        next_ring_start = base_index + (r + 1) * radial_segments
        for i in range(radial_segments):
            v0 = ring_start + i
            v1 = ring_start + (i + 1) % radial_segments
            v2 = next_ring_start + i
            v3 = next_ring_start + (i + 1) % radial_segments

            faces.append((v0, v1, v2))
            faces.append((v2, v1, v3))

    # Connect the innermost ring to the top center
    innermost_ring_start = base_index + (cap_resolution - 1) * radial_segments
    for i in range(radial_segments):
        v0 = innermost_ring_start + i
        v1 = innermost_ring_start + (i + 1) % radial_segments
        faces.append((v0, v1, top_center_index))

    return faces


def save_to_stl(vertices, faces, filename):
    """Save vertices and faces to an STL file."""
    stl_mesh = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            stl_mesh.vectors[i][j] = vertices[face[j]]

    stl_mesh.save(filename)
    print(f"STL file saved as {filename}")


def create_test_stl(
    radius, height, radial_segments, height_segments, cap_resolution, filename
):
    """Create a test STL file for a capped cylinder with concentric rings."""
    vertices, bottom_center_index, top_center_index = generate_vertices_with_rings(
        radius, height, radial_segments, height_segments, cap_resolution
    )
    faces = generate_faces(
        radius,
        height,
        radial_segments,
        height_segments,
        cap_resolution,
        vertices,
        bottom_center_index,
        top_center_index,
    )
    save_to_stl(vertices, faces, filename)


# Parameters for the test STL
RADIUS = 5.0
HEIGHT = 10.0
RADIAL_SEGMENTS = 64
HEIGHT_SEGMENTS = 20
CAP_RESOLUTION = 10
FILENAME = "capped_cylinder_with_rings.stl"

if __name__ == "__main__":  # pragma: no cover
    # Generate and save the STL
    create_test_stl(
        RADIUS, HEIGHT, RADIAL_SEGMENTS, HEIGHT_SEGMENTS, CAP_RESOLUTION, FILENAME
    )
