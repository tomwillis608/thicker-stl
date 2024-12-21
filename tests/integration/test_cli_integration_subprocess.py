"""Integration test for CLI using a subprocess."""

import os
import subprocess


def test_cli_integration_valid_arguments(tmp_path):
    """Test the CLI with valid arguments by running it in a subprocess."""
    # Arrange
    input_file = "tests/fixtures/test_cylinder.stl"
    output_file = tmp_path / "test_output.stl"
    offset = "0.1"

    # Act
    result = subprocess.run(
        [
            "python",
            "-m",
            "thicker.cli.cli",  # CLI entry point
            "--input",
            input_file,
            "--output",
            str(output_file),
            "--offset",
            offset,
        ],
        capture_output=True,
        text=True,
    )

    # Assert
    assert (
        result.returncode == 0
    ), f"CLI failed with stdout: {result.stdout}, stderr: {result.stderr}"
    assert os.path.exists(output_file), "Output file was not created."
    # Additional validation for the generated file can be added here


def test_cli_integration_file_not_found():
    """Test the CLI with a non-existent input file."""
    # Arrange
    input_file = "non_existent_file.stl"
    output_file = "dummy_output.stl"
    offset = "0.1"

    # Act
    result = subprocess.run(
        [
            "python",
            "-m",
            "thicker.cli.cli",  # CLI entry point
            "--input",
            input_file,
            "--output",
            output_file,
            "--offset",
            offset,
        ],
        capture_output=True,
        text=True,
    )

    # Assert
    assert result.returncode == 2, "CLI should fail for non-existent input file."
    assert (
        f"[Errno 2] No such file or directory: '{input_file}'" in result.stderr
    ), "Expected file not found error message."
