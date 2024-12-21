"""
Command-Line Interface (CLI) for the Thickening Tool.

This module provides a CLI to interact with the thickening use case. It parses
user input and delegates to the appropriate use case while maintaining adherence
to clean architecture.
"""

import argparse
import sys

from thicker.adapters.stl_mesh_reader import STLMeshReader
from thicker.adapters.stl_mesh_writer import STLMeshWriter
from thicker.interfaces.mesh_reader import MeshReader
from thicker.interfaces.mesh_writer import MeshWriter
from thicker.use_cases.thicken_mesh import process_thickening


def parse_arguments():
    """
    Parse command-line arguments for the thickening tool.

    Returns:
        Namespace: Parsed arguments including input file, output file, and offset.
    """
    parser = argparse.ArgumentParser(
        description="Thickens a 3D mesh by the specified offset."
    )
    parser.add_argument(
        "--input", type=str, required=True, help="Path to the input STL file."
    )
    parser.add_argument(
        "--output", type=str, required=True, help="Path to save the thickened STL file."
    )
    parser.add_argument(
        "--offset",
        type=float,
        required=True,
        help="Offset value for thickening the mesh (positive or negative).",
    )
    return parser.parse_args()


def main():
    """
    Entry point for the CLI. Parses arguments and delegates to the
    process_thickening use case.

    Raises:
        ValueError: If any argument validation fails.
    """
    args = parse_arguments()

    # Validate parsed arguments
    if args.offset == 0:
        raise ValueError("Offset value must be non-zero.")
    try:
        # Simulate file operations
        # if not os.path.exists(args.input):
        #     raise FileNotFoundError(f"Input file not found: {args.input}")

        reader: MeshReader = STLMeshReader()
        writer: MeshWriter = STLMeshWriter()
        # Call the thickening use case
        process_thickening(
            reader,
            writer,
            input_path=args.input,
            output_path=args.output,
            offset=args.offset,
        )
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
