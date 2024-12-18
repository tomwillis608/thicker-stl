"""Test the file processor."""

from unittest.mock import patch

from thicker.adapters.file_processor import read_stl_data, write_stl_data


def test_read_stl_data_with_valid_data():
    """Test the connector with valid data to ensure type assertions pass."""
    # Arrange: Mock the HumbleSTLIO.read method

    with patch(
        "thicker.adapters.file_processor.HumbleSTLIO.read",
        return_value=([(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)], [(0, 1, 2)]),
    ) as mock_load:
        file_path = "test.stl"

        # Act: Call the connector
        vertices, faces = read_stl_data(file_path)

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


def test_write_stl_data_with_valid_data():
    """Test the connector with valid data to ensure type assertions pass."""
    # Arrange: Mock the HumbleSTLIO.read method

    with patch("thicker.adapters.file_processor.HumbleSTLIO.write") as mock_write:
        file_path = "test.stl"
        vertices = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
        faces = [(0, 1, 2)]

        # Act: Call the connector
        write_stl_data(file_path, vertices, faces)

        # Verify the mocked method was called
        mock_write.assert_called_once_with(file_path, vertices, faces)
