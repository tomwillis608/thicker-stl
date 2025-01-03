"""nox file for the project - automate the development tasks."""

import os

import nox

# Global variables
DEV_REQUIREMENTS = "requirements-dev.txt"


# Define the Nox sessions
@nox.session
def generate_requirements(session):
    """
    This session generates the production and development requirements.txt
    files from the requirements.in files using pip-tools.
    """
    # Install uv in the virtual environment
    session.install("uv")

    # Generate the production requirements.txt
    session.run(
        "uv", "pip", "compile", "requirements.in", "--output-file", "requirements.txt"
    )

    # Generate the development requirements.txt, including production dependencies
    session.run(
        "uv", "pip", "compile", "requirements-dev.in", "--output-file", DEV_REQUIREMENTS
    )


@nox.session
def install_dependencies(session):
    """
    This session installs the production dependencies
    from the requirements-dev.txt.
    """
    # Install dependencies (using the generated requirements-dev.txt)
    session.install("-r", DEV_REQUIREMENTS)


@nox.session(python=["3.11"])
def coverage(session):
    """
    Run tests and measure code coverage.
    """

    # Install all dev dependencies, including testing tools and numpy
    session.install("-r", DEV_REQUIREMENTS)

    # Run pytest with coverage
    session.run(
        "pytest",
        "--cov=thicker",  # Measure coverage for this module/package
        "--cov-report=term-missing",  # Show missing lines in the terminal
        "--cov-report=html",  # Generate an HTML coverage report
    )
    session.log("HTML report generated in 'htmlcov/' directory")


@nox.session(python=["3.11"])
def coverage_ci(session):
    """
    Run tests and measure code coverage in XML for CI.
    """
    if os.getenv("CI") == "true":
        # Install all dev dependencies, including testing tools and numpy
        session.install("-r", DEV_REQUIREMENTS)

        # Run pytest with coverage
        session.run(
            "pytest",
            "--cov=thicker",  # Measure coverage for this module/package
            "--cov-report=term-missing",  # Show missing lines in the terminal
            "--cov-report=xml",  # Generate an HTML coverage report
            "--cov-fail-under=100",  # Set your coverage threshold
        )
        session.log("XML report generated in '.' directory")
    else:
        session.log("Skipping coverage_ci XML, since we are not running in CI.")


@nox.session
def lint(session):
    """Run Ruff to lint the codebase."""
    session.install("ruff")
    session.run("ruff", "format", ".")
