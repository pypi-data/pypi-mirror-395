# tests/test_cli.py

import pytest
import shutil
import argparse
from pathlib import Path
from unittest.mock import MagicMock, call
from enterprise_docs import cli

# Fixtures are now in conftest.py

def test_list_docs(mock_resources, capsys):
    # Mock resources.files return value
    mock_files = MagicMock()
    mock_resources.files.return_value = mock_files

    # Create mock file objects
    file1 = MagicMock()
    file1.name = "template1.md"
    file1.suffix = ".md"

    file2 = MagicMock()
    file2.name = "other.txt"
    file2.suffix = ".txt"

    file3 = MagicMock()
    file3.name = "template2.md"
    file3.suffix = ".md"

    mock_files.iterdir.return_value = [file1, file2, file3]

    cli.list_docs()

    captured = capsys.readouterr()
    assert "template1.md" in captured.out
    assert "template2.md" in captured.out
    assert "other.txt" not in captured.out

def test_copy_docs(mock_resources, mock_shutil, mock_path, capsys):
    destination = "/tmp/docs"

    # Mock Path
    mock_dest_path = MagicMock()
    mock_path.return_value = mock_dest_path

    # Mock resources
    mock_files = MagicMock()
    mock_resources.files.return_value = mock_files

    file1 = MagicMock()
    file1.name = "template1.md"
    file1.suffix = ".md"

    file2 = MagicMock()
    file2.name = "other.txt"
    file2.suffix = ".txt"

    mock_files.iterdir.return_value = [file1, file2]

    cli.copy_docs(destination)

    # Verify mkdir was called
    mock_dest_path.mkdir.assert_called_once_with(parents=True, exist_ok=True)

    # Verify shutil.copy was called for the md file
    mock_shutil.copy.assert_called_once()
    assert mock_shutil.copy.call_args[0][0] == file1
    # The second arg is dest / f.name. Since we mocked Path, checking exact value is tricky without more complex mocks.
    # But checking called_once is good enough for now.

    captured = capsys.readouterr()
    assert "Copied documentation templates" in captured.out

def test_show_version(mocker, capsys):
    # Test version found
    mocker.patch("enterprise_docs.cli.version", return_value="1.0.0")
    cli.show_version()
    captured = capsys.readouterr()
    assert "enterprise-docs 1.0.0" in captured.out

    # Test PackageNotFoundError
    from importlib.metadata import PackageNotFoundError
    mocker.patch("enterprise_docs.cli.version", side_effect=PackageNotFoundError)
    cli.show_version()
    captured = capsys.readouterr()
    assert "enterprise-docs unknown" in captured.out

def test_main_list(mocker):
    mocker.patch("sys.argv", ["enterprise-docs", "list"])
    mock_list_docs = mocker.patch("enterprise_docs.cli.list_docs")
    mock_print_logo = mocker.patch("enterprise_docs.cli.print_logo")

    cli.main()

    mock_print_logo.assert_called_once()
    mock_list_docs.assert_called_once()

def test_main_sync(mocker):
    mocker.patch("sys.argv", ["enterprise-docs", "sync", "--to", "custom_dir"])
    mock_copy_docs = mocker.patch("enterprise_docs.cli.copy_docs")
    mock_print_logo = mocker.patch("enterprise_docs.cli.print_logo")

    cli.main()

    mock_print_logo.assert_called_once()
    # Note: copy_docs signature will change, so this test might need update later if I change the signature in source code.
    # But mock_copy_docs will just capture whatever arguments are passed.
    mock_copy_docs.assert_called_once()
    args, _ = mock_copy_docs.call_args
    assert args[0] == "custom_dir"

def test_main_version(mocker):
    mocker.patch("sys.argv", ["enterprise-docs", "version"])
    mock_show_version = mocker.patch("enterprise_docs.cli.show_version")
    mock_print_logo = mocker.patch("enterprise_docs.cli.print_logo")

    cli.main()

    mock_print_logo.assert_called_once()
    mock_show_version.assert_called_once()

def test_main_default_args(mocker):
    # Test sync without --to (should use default)
    mocker.patch("sys.argv", ["enterprise-docs", "sync"])
    mock_copy_docs = mocker.patch("enterprise_docs.cli.copy_docs")
    mock_print_logo = mocker.patch("enterprise_docs.cli.print_logo")

    cli.main()

    mock_copy_docs.assert_called_once()
    args, _ = mock_copy_docs.call_args
    assert args[0] == "./docs"
