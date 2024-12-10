""" Test cylinder generator. """

import os
from tests.utils.generate_test_cylinder import create_test_stl
from tempfile import TemporaryDirectory
import pytest

@pytest.fixture
def temporary_directory():
    """Provide a temporary directory for tests."""
    with TemporaryDirectory() as tmp_dir:
        yield tmp_dir

def test_create_cylinder_stl(temporary_directory):
    """Test the creation of a cylinder STL file."""
    output_path = os.path.join(temporary_directory, "test_cylinder.stl")
    create_test_stl(output_path)

    # Assert that the file was created
    assert os.path.exists(output_path), "STL file was not created"

    # Assert that the file is not empty
    assert os.path.getsize(output_path) > 0
