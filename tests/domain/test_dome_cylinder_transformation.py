""" Test hemisphere-cylinder transformation."""


def test_hemisphere_topped_cylinder_transformation():
    """
    Test the hemisphere-topped cylinder transformation on a unit cube.
    """
    # Arrange
    from math import sqrt

    class HemisphereCylinderTransformer:
        def __init__(self, cylinder_height, radius):
            self.cylinder_height = cylinder_height
            self.radius = radius

        def transform(self, vertex):
            x, y, z = vertex
            radius = sqrt(x ** 2 + y ** 2)

            if z <= self.cylinder_height:
                # Cylinder region: project x, y onto cylinder surface
                if radius == 0:
                    return (0, 0, z)  # Handle center point case
                scale = self.radius / radius
                return (x * scale, y * scale, z)
            else:
                # Hemisphere region: normalize and scale to radius
                norm = sqrt(x ** 2 + y ** 2 + z ** 2)
                return (x / norm * self.radius,
                        y / norm * self.radius,
                        z / norm * self.radius)

    transformer = HemisphereCylinderTransformer(cylinder_height=0.5, radius=1.0)

    # Define the vertices of a unit cube
    unit_cube_vertices = [
        (-1, -1, -1), (-1, -1, 1), (-1, 1, -1), (-1, 1, 1),
        (1, -1, -1), (1, -1, 1), (1, 1, -1), (1, 1, 1)
    ]

    # Expected transformed vertices
    expected_transformed_vertices = []
    for vertex in unit_cube_vertices:
        x, y, z = vertex
        if z <= 0.5:
            # Cylindrical region
            radius = sqrt(x ** 2 + y ** 2)
            scale = 1 / radius if radius != 0 else 1
            expected_transformed_vertices.append((x * scale, y * scale, z))
        else:
            # Hemispherical region
            norm = sqrt(x ** 2 + y ** 2 + z ** 2)
            expected_transformed_vertices.append((x / norm, y / norm, z / norm))

    # Act
    transformed_vertices = [transformer.transform(vertex)
                            for vertex in unit_cube_vertices]
    print(transformed_vertices)
    # Assert
    for transformed, expected in zip(transformed_vertices,
                                     expected_transformed_vertices):
        assert all(abs(t - e) < 1e-6 for t, e in zip(transformed, expected)), \
            f"Expected {expected}, got {transformed}"
