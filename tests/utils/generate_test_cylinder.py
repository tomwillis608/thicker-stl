""" Utility to create a test STL file. """

import numpy as np
from stl import mesh


def create_test_stl(output_path: str) -> str:
    """ Create a simple cylinder STL file (with a radius of 1 unit and height of 4 units). """

    # Parameters for the cylinder
    radius = 1.0
    height = 4.0
    segments = 32  # Number of segments (higher = smoother). Must be > 3.

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

    print("Degenerate triangles present:", check_degenerate_triangles(vertices, faces))
    print("Is closed (exact):", test_mesh.is_closed(exact=True))

    # Save the mesh to a file
    test_mesh.save(output_path)
    return output_path

def calculate_normal(v0, v1, v2):
    # Cross product of edges to get the normal vector
    edge1 = v1 - v0
    edge2 = v2 - v0
    normal = np.cross(edge1, edge2)
    norm = np.linalg.norm(normal)
    return normal / norm if norm != 0 else np.array([0, 0, 0])


def validate_mesh(mesh):
    print("Normals:", mesh.normals)
    print("Is closed (exact):", mesh.is_closed(exact=True))

def check_degenerate_triangles(vertices, faces):
    for i, face in enumerate(faces):
        v0, v1, v2 = np.array(vertices[face[0]]), np.array(vertices[face[1]]), np.array(vertices[face[2]])
        # Check for duplicate vertices
        if np.array_equal(v0, v1) or np.array_equal(v1, v2) or np.array_equal(v2, v0):
            print(f"Degenerate triangle (duplicate vertices) in face {i}: {face}")
            return True
        # Check if vertices are collinear
        if np.linalg.norm(np.cross(v1 - v0, v2 - v0)) == 0:
            print(f"Degenerate triangle (collinear vertices) in face {i}: {face}")
            return True
    return False

def generate_vertices(height, radius, segments):
    """ Generate vertices for a cylinder by connecting vertices to form triangles. """
    vertices = []
    for i in range(segments):
        angle = 2 * np.pi * i / segments
        x_coord: float = radius * np.cos(angle)
        y_coord: float = radius * np.sin(angle)
        vertices.append([x_coord, y_coord, float(0)])  # Bottom circle
        vertices.append([x_coord, y_coord, float(height)])  # Top circle
    # Add the center of the top and bottom circle to the vertex list
    vertices.append([float(0), float(0), float(0)])  # Bottom center
    vertices.append([float(0), float(0), float(height)])  # Top center
    vertices = np.array(vertices)
    return vertices


def generate_faces(segments, vertices):
    """ Generate faces for a cylinder. """
    faces = []
    bottom_center = len(vertices) - 2
    top_center = len(vertices) - 1

    for i in range(segments):
        bottom_left = 2 * i
        bottom_right = 2 * ((i + 1) % segments)
        top_left = bottom_left + 1
        top_right = bottom_right + 1

        # Side faces (2 triangles per segment)
        faces.append([bottom_left, bottom_right, top_left])
        faces.append([top_left, bottom_right, top_right]) # fix winding order TL to TL

        # Bottom face (triangles connecting bottom vertices to center)
        faces.append([bottom_center, bottom_right, bottom_left]) # fix winding order, normal [0 0 -1]


        # Top face (triangles connecting top vertices to center)
        faces.append([top_center, top_left, top_right]) # fix winding order, normal [0 0 -1]

    return faces


# Create and save the test STL file
if __name__ == "__main__": # pragma: no cover
    STL_FILE = create_test_stl("tests/fixtures/test_cylinder.stl")
    print(f"Test STL file saved to: {STL_FILE}")
