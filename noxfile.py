""" nox file for the project - automate the development tasks. """
import nox

# Define the Nox sessions
@nox.session
def generate_requirements(session):
    """
    This session generates the production and development requirements.txt
    files from the requirements.in files using pip-tools.
    """
    # Install pip-tools in the virtual environment
    session.install('pip-tools')

    # Generate the production requirements.txt
    session.run('pip-compile', 'requirements.in', '--output-file', 'requirements.txt')

    # Generate the development requirements.txt, including production dependencies
    session.run('pip-compile', 'requirements-dev.in', '--output-file', 'requirements-dev.txt')

@nox.session
def install_dependencies(session):
    """
    This session installs the production or development dependencies
    from the requirements.txt or requirements-dev.txt.
    """
    # Install dependencies (using the generated requirements-dev.txt or requirements.txt)
    session.install('-r', 'requirements-dev.txt')  # Use requirements.txt if only prod dependencies are needed

# @nox.session(python=["3.10", "3.11"])
@nox.session(python=["3.11"])
def coverage(session):
    """
    Run tests and measure code coverage.
    """
    # Install dependencies
    # session.install("pytest", "pytest-cov")
    # Install all dev dependencies, including testing tools and numpy
    session.install("-r", "requirements-dev.txt")

    # Run pytest with coverage
    session.run(
        "pytest",
        "--cov=tests.utils",        # Measure coverage for this module/package
        "--cov-report=term-missing",  # Show missing lines in the terminal
        "--cov-report=html",       # Generate an HTML coverage report
    )
    session.log("HTML report generated in 'htmlcov/' directory")
