""" Test the process_thickening use case method. """

from unittest.mock import Mock

from thicker.use_cases.thicken_mesh import process_thickening


def test_process_thickening():
    # Mock reader and writer
    mock_reader = Mock()
    mock_writer = Mock()

    # Mock input data
    mock_reader.read.return_value = (
        [(0.0, 0.0, 1.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)],
        [(0, 1, 2)]
    )
    mock_writer.write.return_value = None

    # Run the process
    process_thickening(mock_reader, mock_writer, "input.stl", "output.stl", 0.1)

    # Assertions
    mock_reader.read.assert_called_once()
    mock_writer.write.assert_called_once()
