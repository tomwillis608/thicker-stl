"""Test the Mesh class."""

from thicker.domain.mesh import Mesh


def test_create_mesh():
    """Test that a Mesh object is created with correct vertices and faces."""
    vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    faces = [(0, 1, 2)]

    mesh = Mesh(vertices=vertices, faces=faces)

    assert mesh.vertices == vertices
    assert mesh.faces == faces


# def test_add_vertex():
#     """Test that a vertex can be added to the mesh."""
#     mesh = Mesh(vertices=[], faces=[])
#     mesh.add_vertex((0, 0, 0))
#
#     assert len(mesh.vertices) == 1
#     assert mesh.vertices[0] == (0, 0, 0)
#
#
# def test_add_face():
#     """Test that a face can be added to the mesh."""
#     vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
#     mesh = Mesh(vertices=vertices, faces=[])
#     mesh.add_face((0, 1, 2))
#
#     assert len(mesh.faces) == 1
#     assert mesh.faces[0] == (0, 1, 2)
