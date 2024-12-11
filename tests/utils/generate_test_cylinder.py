""" Utility to create a test STL file. """

import numpy as np
from stl import mesh


def create_test_stl(output_path: str) -> str:
    """ Create a simple cylinder STL file (with a radius of 1 unit and height of 2 units). """

    # Parameters for the cylinder
    radius = 1.0
    height = 2.0
    segments = 30  # Number of segments (higher = smoother)

    # Generate the vertices for the cylinder
    vertices = generate_vertices(height, radius, segments)

    # Generate the faces of the cylinder (connecting vertices to form triangles)
    faces = generate_faces(segments, vertices)
    faces = np.array(faces)

    # Create the mesh object
    test_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            test_mesh.vectors[i][j] = vertices[face[j], :]

    # Save the mesh to a file
    test_mesh.save(output_path)
    return output_path


def generate_vertices(height, radius, segments):
    """ Generate vertices for a cylinder by connecting vertices to form triangles. """
    vertices = []
    for i in range(segments):
        angle = 2 * np.pi * i / segments
        x_coord: float = radius * np.cos(angle)
        y_coord: float = radius * np.sin(angle)
        vertices.append([x_coord, y_coord, 0])  # Bottom circle
        vertices.append([x_coord, y_coord, height])  # Top circle
    # Add the center of the top and bottom circle to the vertex list
    vertices.append([0, 0, 0])  # Bottom center
    vertices.append([0, 0, height])  # Top center
    vertices = np.array(vertices)
    return vertices


def generate_faces(segments, vertices):
    """ Generate faces for a cylinder. """
    faces = []
    for i in range(segments):
        bottom_left = 2 * i
        bottom_right = 2 * ((i + 1) % segments)
        top_left = bottom_left + 1
        top_right = bottom_right + 1

        # Side faces (4 per segment: 2 triangles)
        faces.append([bottom_left, bottom_right, top_left])
        faces.append([bottom_right, top_right, top_left])

        # Bottom face (center with bottom vertices)
        faces.append([bottom_left, bottom_right, len(vertices) - 2])

        # Top face (center with top vertices)
        faces.append([top_left, top_right, len(vertices) - 1])

    return faces


# Create and save the test STL file
if __name__ == "__main__": # pragma: no cover
    STL_FILE = create_test_stl("test_cylinder.stl")
    print(f"Test STL file saved to: {STL_FILE}")
