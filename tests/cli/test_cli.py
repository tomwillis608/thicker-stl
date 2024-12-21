"""Test the CLI."""

import sys

import pytest

from thicker.cli.cli import main, parse_arguments


def test_parse_arguments_valid():
    """
    Test that valid arguments are parsed correctly.
    """
    test_args = [
        "script_name",
        "--input",
        "input.stl",
        "--output",
        "output.stl",
        "--offset",
        "2.0",
    ]
    sys.argv = test_args
    args = parse_arguments()
    assert args.input == "input.stl"
    assert args.output == "output.stl"
    assert args.offset == pytest.approx(2.0, 0.0001)


def test_parse_arguments_missing_input():
    """
    Test that missing input file raises a SystemExit.
    """
    test_args = [
        "script_name",
        "--offset",
        "2.0",
        "--output",
        "output.stl",
    ]
    sys.argv = test_args
    with pytest.raises(SystemExit):
        parse_arguments()


def test_parse_arguments_negative_offset():
    """
    Test that a valid negative offset is parsed correctly.
    """
    test_args = [
        "script_name",
        "--input",
        "input.stl",
        "--output",
        "output.stl",
        "--offset",
        "-1.5",
    ]
    sys.argv = test_args
    args = parse_arguments()
    assert args.offset == -1.5


def test_main_zero_offset():
    """
    Test that passing an offset of zero raises ValueError in the main function.
    """
    test_args = [
        "script_name",
        "--input",
        "input.stl",
        "--output",
        "output.stl",
        "--offset",
        "0",
    ]
    sys.argv = test_args
    with pytest.raises(ValueError, match="Offset value must be non-zero."):
        main()


def test_main_valid_arguments(mocker):
    """
    Test that the main function calls the use case with valid arguments.
    """
    test_args = [
        "script_name",
        "--input",
        "input.stl",
        "--output",
        "output.stl",
        "--offset",
        "2.0",
    ]
    sys.argv = test_args

    # Mock the dependencies passed to process_thickening
    mock_reader = mocker.Mock(name="MockMeshReader")
    mock_writer = mocker.Mock(name="MockMeshWriter")
    _mock_reader_cls = mocker.patch(
        "thicker.cli.cli.STLMeshReader", return_value=mock_reader
    )
    _mock_writer_cls = mocker.patch(
        "thicker.cli.cli.STLMeshWriter", return_value=mock_writer
    )

    # Mock the process_thickening use case
    mock_process = mocker.patch("thicker.cli.cli.process_thickening")

    main()

    # Assert process_thickening was called with correct arguments
    mock_process.assert_called_once_with(
        mock_reader,
        mock_writer,
        input_path="input.stl",
        output_path="output.stl",
        offset=2.0,
    )


def test_main_missing_offset():
    """
    Test that missing the offset raises a SystemExit.
    """
    test_args = [
        "script_name",
        "--input",
        "input.stl",
        "--output",
        "output.stl",
    ]
    sys.argv = test_args
    with pytest.raises(SystemExit):
        main()


def test_main_input_file_not_found(mocker):
    """
    Test that providing a non-existent input file raises FileNotFoundError.
    """
    test_args = [
        "script_name",
        "--input",
        "non_existent_file.stl",
        "--output",
        "output.stl",
        "--offset",
        "2.0",
    ]
    sys.argv = test_args

    # Mock the dependencies passed to process_thickening
    mock_reader = mocker.Mock(name="MockMeshReader")
    mock_writer = mocker.Mock(name="MockMeshWriter")
    _mock_reader_cls = mocker.patch(
        "thicker.cli.cli.STLMeshReader", return_value=mock_reader
    )
    _mock_writer_cls = mocker.patch(
        "thicker.cli.cli.STLMeshWriter", return_value=mock_writer
    )

    # Mock the process_thickening function to raise FileNotFoundError
    mock_process = mocker.patch(
        "thicker.cli.cli.process_thickening",
        side_effect=FileNotFoundError,
    )

    # Run the CLI and ensure it raises the appropriate error
    with pytest.raises(SystemExit) as exec_info_:
        main()

    # Assert that the CLI exits with code 2
    assert exec_info_.value.code == 2

    # Verify process_thickening was called once
    mock_process.assert_called_once_with(
        mock_reader,
        mock_writer,
        input_path="non_existent_file.stl",
        output_path="output.stl",
        offset=2.0,
    )


def test_main_unexpected_exception(mocker):
    """
    Test that providing a non-existent input file raises FileNotFoundError.
    """
    test_args = [
        "script_name",
        "--input",
        "non_existent_file.stl",
        "--output",
        "output.stl",
        "--offset",
        "2.0",
    ]
    sys.argv = test_args

    # Mock the dependencies passed to process_thickening
    mock_reader = mocker.Mock(name="MockMeshReader")
    mock_writer = mocker.Mock(name="MockMeshWriter")
    _mock_reader_cls = mocker.patch(
        "thicker.cli.cli.STLMeshReader", return_value=mock_reader
    )
    _mock_writer_cls = mocker.patch(
        "thicker.cli.cli.STLMeshWriter", return_value=mock_writer
    )

    # Mock the process_thickening function to raise FileNotFoundError
    mock_process = mocker.patch(
        "thicker.cli.cli.process_thickening",
        side_effect=Exception,
    )

    # Run the CLI and ensure it raises the appropriate error
    with pytest.raises(SystemExit) as exec_info_:
        main()

    # Assert that the CLI exits with code 2
    assert exec_info_.value.code == 1

    # Verify process_thickening was called once
    mock_process.assert_called_once_with(
        mock_reader,
        mock_writer,
        input_path="non_existent_file.stl",
        output_path="output.stl",
        offset=2.0,
    )
