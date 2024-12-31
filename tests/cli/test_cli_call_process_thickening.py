"""Test the CLI."""

import sys
from unittest.mock import MagicMock, patch

from thicker.cli.cli import main


def test_cli_calls_process_thickening(mocker):
    """Test that the CLI correctly calls the process_thickening_ori
    use case with arguments."""
    # Arrange: Mock the process_thickening_ori function
    mock_process_thickening = MagicMock()
    test_args = [
        "thicker",
        "--input",
        "input.stl",
        "--output",
        "output.stl",
        "--offset",
        "0.1",
    ]
    expected_input_file = "input.stl"
    expected_output_file = "output.stl"
    expected_offset = 0.1
    # Mock the dependencies passed to process_thickening_ori
    mock_reader = mocker.Mock(name="MockMeshReader")
    mock_writer = mocker.Mock(name="MockMeshWriter")
    _mock_reader_cls = mocker.patch(
        "thicker.cli.cli.STLMeshReader", return_value=mock_reader
    )
    _mock_writer_cls = mocker.patch(
        "thicker.cli.cli.STLMeshWriter", return_value=mock_writer
    )
    with patch("thicker.cli.cli.process_thickening", mock_process_thickening):
        with patch.object(sys, "argv", test_args):
            # Act: Call the CLI main function
            main()

    # Assert: Check that process_thickening_ori was called with the correct arguments
    mock_process_thickening.assert_called_once_with(
        mock_reader,
        mock_writer,
        input_path=expected_input_file,
        output_path=expected_output_file,
        offset=expected_offset,
    )
