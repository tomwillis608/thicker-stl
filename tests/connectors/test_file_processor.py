"""Test the file processor."""

from unittest.mock import patch

from thicker.connectors.file_processor import process_stl_data


def test_process_stl_data_with_valid_data():
    """Test the connector with valid data to ensure type assertions pass."""
    # Arrange: Mock the STLReader.load method

    with patch(
        "thicker.connectors.file_processor.STLReader.load",
        return_value=([(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)], [(0, 1, 2)]),
    ) as mock_load:
        file_path = "test.stl"

        # Act: Call the connector
        vertices, faces = process_stl_data(file_path)

        # Assert: Verify the data types are correct
        assert isinstance(vertices, list)
        assert all(
            isinstance(v, tuple)
            and len(v) == 3
            and all(isinstance(coord, float) for coord in v)
            for v in vertices
        )
        assert isinstance(faces, list)
        assert all(
            isinstance(f, tuple)
            and len(f) == 3
            and all(isinstance(idx, int) for idx in f)
            for f in faces
        )

        # Verify the mocked method was called
        mock_load.assert_called_once_with(file_path)
