import pytest
from pathlib import Path
from enterprise_docs import cli
from unittest.mock import MagicMock

def test_sync_custom_source(mock_shutil, mock_path, capsys, mocker):
    """Test syncing from a custom source directory."""
    # Mock user providing a custom source
    custom_source = "/path/to/custom_templates"
    mocker.patch("sys.argv", ["enterprise-docs", "sync", "--source", custom_source])
    mocker.patch("enterprise_docs.cli.print_logo")

    # Mock Path to handle custom source iteration
    # We need mock_path to return a mock object for custom_source that has iterdir()

    # We need to distinguish between dest path and source path
    # cli.copy_docs will do:
    # dest = Path(destination)
    # ...
    # if source:
    #    src = Path(source)
    # else:
    #    src = resources.files(...)

    # So we need Path(custom_source) to return a mock that has iterdir

    # Let's verify that copy_docs is called with the source argument first
    # This is an integration test of main -> copy_docs mostly, but also copy_docs logic.

    # But wait, if I mock Path, I need to control what Path(x) returns based on x.
    # mocker.patch("enterprise_docs.cli.Path") is already done by mock_path fixture.

    mock_dest_obj = MagicMock()
    mock_source_obj = MagicMock()

    def path_side_effect(arg):
        if arg == "./docs": # default dest
            return mock_dest_obj
        if arg == custom_source:
            return mock_source_obj
        return MagicMock()

    mock_path.side_effect = path_side_effect

    # Setup source files
    file1 = MagicMock()
    file1.name = "CustomTemplate.md"
    file1.suffix = ".md"

    mock_source_obj.iterdir.return_value = [file1]

    # Run main
    try:
        cli.main()
    except SystemExit:
        pass

    # Verify copy was called with file1
    # Check if we copied from custom source
    # mock_shutil.copy(f, dest / f.name)
    assert mock_shutil.copy.call_count == 1
    args, _ = mock_shutil.copy.call_args
    assert args[0] == file1

    captured = capsys.readouterr()
    assert "✅ Copied CustomTemplate.md" in captured.out or "✅ Copied documentation templates" in captured.out

def test_sync_custom_source_not_found(mock_path, capsys, mocker):
    """Test syncing from a non-existent custom source."""
    custom_source = "/bad/path"
    mocker.patch("sys.argv", ["enterprise-docs", "sync", "--source", custom_source])
    mocker.patch("enterprise_docs.cli.print_logo")

    # Mock Path(custom_source).exists() to return False?
    # Or iterdir raising FileNotFoundError?

    mock_source_obj = MagicMock()
    mock_source_obj.exists.return_value = False
    mock_source_obj.iterdir.side_effect = FileNotFoundError

    mock_path.return_value = mock_source_obj # Simplification

    # But wait, Path(destination) is also called.
    # If we want to test that it fails gracefully:

    try:
        cli.main()
    except SystemExit:
        pass

    # Ideally it should print an error
    captured = capsys.readouterr()
    # If not implemented, it acts as unrecognized argument or ignores it.

    # If implemented, it should probably verify source exists.
