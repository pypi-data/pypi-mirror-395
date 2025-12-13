import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_resources(mocker):
    return mocker.patch("enterprise_docs.cli.resources")

@pytest.fixture
def mock_path(mocker):
    return mocker.patch("enterprise_docs.cli.Path")

@pytest.fixture
def mock_shutil(mocker):
    return mocker.patch("enterprise_docs.cli.shutil")

@pytest.fixture
def mock_files_setup(mock_resources):
    """Setup mock files for resources.files().iterdir()"""
    mock_files = MagicMock()
    mock_resources.files.return_value = mock_files

    file1 = MagicMock()
    file1.name = "Template1.md"
    file1.suffix = ".md"

    file2 = MagicMock()
    file2.name = "Template2.md"
    file2.suffix = ".md"

    file3 = MagicMock()
    file3.name = "image.png"
    file3.suffix = ".png"

    mock_files.iterdir.return_value = [file1, file2, file3]
    return mock_files
