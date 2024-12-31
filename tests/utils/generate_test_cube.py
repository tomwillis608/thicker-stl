"""Generate a cube STL file for testing."""

import numpy as np
from stl import mesh


def create_test_stl(filename: str, side_length: float = 1.0, resolution: int = 1):
    """
    Generate an STL file of a cube with adjustable resolution.

    Args:
        filename (str): The name of the STL file to create.
        side_length (float): The length of the cube's side.
        resolution (int): The number of subdivisions along each side of the cube.
            Higher values increase face count.
    """
    if resolution < 1:
        raise ValueError("Resolution must be 1 or higher.")

    half_side = side_length / 2
    _ = side_length / resolution

    # Create the grid of vertices
    vertices = []
    for z in np.linspace(-half_side, half_side, resolution + 1):
        for y in np.linspace(-half_side, half_side, resolution + 1):
            for x in np.linspace(-half_side, half_side, resolution + 1):
                vertices.append((x, y, z))

    vertices = np.array(vertices)
    vertices_per_layer = (resolution + 1) ** 2  # Total vertices per z-layer

    # Create the faces
    faces = []

    # Helper function to add two triangles per quad
    def add_quad(v0, v1, v2, v3):
        faces.append([v0, v1, v2])  # Triangle 1
        faces.append([v2, v3, v0])  # Triangle 2

    # Generate faces for each side of the cube
    for z in range(resolution):  # Bottom to top
        for y in range(resolution):  # Back to front
            for x in range(resolution):  # Left to right
                # Compute vertex indices
                v0 = x + y * (resolution + 1) + z * vertices_per_layer
                v1 = v0 + 1
                v2 = v0 + (resolution + 1)
                v3 = v2 + 1
                v4 = v0 + vertices_per_layer
                v5 = v1 + vertices_per_layer
                v6 = v2 + vertices_per_layer
                v7 = v3 + vertices_per_layer

                # Add faces for six sides
                # Bottom face
                add_quad(v0, v1, v3, v2)
                # Top face
                add_quad(v4, v5, v7, v6)
                # Front face
                add_quad(v2, v3, v7, v6)
                # Back face
                add_quad(v0, v1, v5, v4)
                # Left face
                add_quad(v0, v2, v6, v4)
                # Right face
                add_quad(v1, v3, v7, v5)

    # Create the STL mesh
    cube = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            cube.vectors[i][j] = vertices[face[j]]

    # Save the STL file
    cube.save(filename)
    return filename


# Create and save the test STL file
if __name__ == "__main__":  # pragma: no cover
    filename = "tests/fixtures/test_cube.stl"
    side_length: float = 1.0
    resolution: int = 3
    stl_file = create_test_stl(filename, side_length, resolution)
    print(f"Test STL file saved to: {stl_file}")
