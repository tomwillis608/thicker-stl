"""Test the Mesh class."""

from thicker.domain.mesh import Mesh


def test_create_mesh():
    """Test that a Mesh object is created with correct vertices and faces."""
    vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    faces = [(0, 1, 2)]

    mesh = Mesh(vertices=vertices, faces=faces)

    assert mesh.vertices == vertices
    assert mesh.faces == faces


def test_equality():
    """Test that meshes are equal."""
    vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    faces = [(0, 1, 2)]

    mesh1 = Mesh(vertices=vertices, faces=faces)
    mesh2 = Mesh(vertices=vertices, faces=faces)

    assert mesh1 == mesh2


def test_inequality():
    """Test that meshes are not equal."""
    vertices1 = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    faces1 = [(0, 1, 2)]
    vertices2 = [(0, 0, 1), (1, 0, 1), (0, 1, 1)]
    faces2 = [(1, 2, 0)]

    mesh1 = Mesh(vertices=vertices1, faces=faces1)
    mesh2 = Mesh(vertices=vertices2, faces=faces1)
    mesh3 = Mesh(vertices=vertices2, faces=faces2)

    assert mesh1 != mesh2
    assert mesh2 != mesh3


def test_bad_class():
    """Test meshes are equal to strings."""
    vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    faces = [(0, 1, 2)]

    mesh = Mesh(vertices=vertices, faces=faces)
    a_string = "moof"

    assert mesh != a_string
