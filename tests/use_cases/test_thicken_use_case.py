"""Test the thickening use case."""

from unittest.mock import patch

from thicker.domain.mesh import Mesh
from thicker.use_cases.thicken_mesh import thicken_a_mesh


def test_thicken_mesh_use_case():
    """Simple test of thicken_a_mesh()."""
    # Mock data
    original_mesh = Mesh(vertices=[(1, 0, 0), (0, 1, 0), (0, 0, 1)], faces=[(0, 1, 2)])
    thickened_mesh = Mesh(
        vertices=[(1.1, 0, 0), (0, 1.1, 0), (0, 0, 1.1)], faces=[(0, 1, 2)]
    )
    offset = 0.1

    # Mock the domain function
    with patch(
        "thicker.use_cases.thicken_mesh.thicken_mesh", return_value=thickened_mesh
    ) as mock_thicken:
        # Call the use case
        result = thicken_a_mesh(original_mesh, offset)

        # Assert the result is as expected
        assert result.vertices == thickened_mesh.vertices
        assert result.faces == thickened_mesh.faces
        assert result == thickened_mesh

        # # Verify that the domain function was called with the correct arguments
        mock_thicken.assert_called_once_with(original_mesh, offset)
