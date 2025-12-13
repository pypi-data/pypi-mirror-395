import pytest
from enterprise_docs import cli

def test_sync_single_template(mock_files_setup, mock_shutil, mock_path, capsys, mocker):
    """Test syncing a single template."""
    # Mock user providing a template name
    mocker.patch("sys.argv", ["enterprise-docs", "sync", "Template1.md"])

    # We need to mock print_logo to avoid noise
    mocker.patch("enterprise_docs.cli.print_logo")

    # Run main
    try:
        cli.main()
    except SystemExit:
        # argparse might exit if it doesn't recognize arguments
        pass

    # Check if copy_docs filtered correctly.
    # We verify mock_shutil.copy

    # If the feature is NOT implemented, this test might fail because:
    # 1. argparse exits with error (unrecognized argument 'Template1.md')
    # 2. or it ignores it and copies everything.

    # We expect copy to be called exactly once for Template1.md
    assert mock_shutil.copy.call_count == 1
    args, _ = mock_shutil.copy.call_args
    src_file = args[0]
    assert src_file.name == "Template1.md"

    captured = capsys.readouterr()
    assert "✅ Copied Template1.md to" in captured.out

def test_sync_single_template_not_found(mock_files_setup, mock_shutil, mock_path, capsys, mocker):
    """Test syncing a non-existent template."""
    mocker.patch("sys.argv", ["enterprise-docs", "sync", "NonExistent.md"])
    mocker.patch("enterprise_docs.cli.print_logo")

    try:
        cli.main()
    except SystemExit:
        pass

    # Should not copy anything
    assert mock_shutil.copy.call_count == 0

    captured = capsys.readouterr()
    # We expect an error message
    assert "❌ Template 'NonExistent.md' not found" in captured.out
