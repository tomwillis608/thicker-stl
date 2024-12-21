# thicker-stl - a 3D Model Thickening Tool

Today's TTRPG mini figures are too dainty. Make those STL thicker.

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/tomwillis608/thicker-stl/main.svg)]
(<https://results.pre-commit.ci/latest/github/tomwillis608/thicker-stl/main>)

## Project Overview

This tool is designed to apply a thickening algorithm to 3D models stored in STL (Stereolithography) format. The primary
goal is to preserve the overall shape of the model while thickening thin parts (e.g., limbs, fingers) to improve
structural integrity, especially for tabletop miniatures.

The tool focuses on **simple geometric modification** of STL models, making it ideal for 3D models used in
tabletop games.

## Features

- **STL File Input/Output**: Load 3D models in STL format, apply thickening, and save the modified model back in
STL format.
- **Thickening Algorithm**: Increases the thickness of 3D models without altering their fundamental shape.
- **Command-Line Interface (CLI)**: Easy-to-use terminal-based interface for interacting with the tool.

## Installation

To get started, you need Python 3.10 or higher installed on your system.

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/thickening-tool.git
   cd thickening-tool
   ```

2. Set up a virtual environment (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install CLI Locally: Run the following command to install the package in editable mode (if you are using pip):

   ```bash
   pip install -e .
   ```

## Usage

Once the tool is installed, you can use the command-line interface to process STL files.

```bash
thicker-stl --input input.stl --output output.stl --offset 0.1
```

### Example

To thicken a cylinder model, run the following command:

```bash
python main.py --input cylinder.stl --output thickened_cylinder.stl
```

Where:

- `--input`: Path to the input STL file.
- `--output`: Path where the thickened STL file will be saved.

## Development

### Project Structure

```text
/docs
    /adrs        # Architectural Decision Records
/src
    /domain      # Business logic for thickening models
    /infrastructure  # File I/O and external integrations
/tests
    /unit_tests  # Unit tests for the thickening algorithm
    /data        # Test STL files and test data
    /utils       # Helper utilities for testing (e.g., generating test STL files)
main.py         # Entry point for the CLI tool
requirements.txt # List of dependencies
README.md       # Project documentation
```

### Running Tests

To run the tests:

```bash
pytest
```

### Code Quality and Linting

The project uses **ruff** for linting and code quality checks. To run linting, use:

```bash
ruff .
```

## Architectural Decisions

- **STL File Format**: We chose to use the STL file format for simplicity and wide support.
- Refer to the [ADR 001](docs/adrs/001-use-stl-files.md) for more details.

## Contributing

Contributions are welcome! If you have ideas for improving the tool or fixing issues, feel free to open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
