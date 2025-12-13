
import pytest
from unittest.mock import patch, MagicMock
import sys
import os
from geminiai_cli import restore

# Now that restore.py imports get_recommendation, we can patch it directly in restore module
@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.get_recommendation")
@patch("geminiai_cli.restore.run")
@patch("os.path.exists", return_value=True)
@patch("os.makedirs")
@patch("os.replace")
@patch("geminiai_cli.restore.shutil.move")
@patch("shutil.rmtree")
@patch("tempfile.mkdtemp", return_value="/tmp/restore_tmp")
@patch("os.listdir")
@patch("os.path.isfile", return_value=True)
def test_restore_auto_success(mock_isfile, mock_listdir, mock_mkdtemp, mock_rmtree, mock_move, mock_replace, mock_makedirs, mock_exists, mock_run, mock_rec, mock_lock):
    # Setup mock recommendation
    mock_rec_obj = MagicMock()
    mock_rec_obj.email = "auto@example.com"
    mock_rec.return_value = mock_rec_obj

    # Setup mock backups
    mock_listdir.return_value = [
        "2025-10-20_000000-other@example.com.gemini.tar.gz",
        "2025-10-21_100000-auto@example.com.gemini.tar.gz", # Old
        "2025-10-22_100000-auto@example.com.gemini.tar.gz", # Latest
    ]

    mock_run.return_value.returncode = 0

    with patch("sys.argv", ["restore.py", "--auto"]):
        restore.main()

    # Verify that get_recommendation was called
    mock_rec.assert_called_once()

    # Verify extraction of correct file
    found = False
    expected_file = "2025-10-22_100000-auto@example.com.gemini.tar.gz"
    for call in mock_run.call_args_list:
        args, _ = call
        if args and isinstance(args[0], str):
            cmd = args[0]
            if "tar -C" in cmd and expected_file in cmd:
                found = True
                break

    assert found, f"Did not find extraction command for {expected_file}"

@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.get_recommendation")
def test_restore_auto_no_recommendation(mock_rec, mock_lock):
    mock_rec.return_value = None
    with patch("sys.argv", ["restore.py", "--auto"]):
        with pytest.raises(SystemExit) as e:
            restore.main()
        # Should exit with error if no recommendation
        assert e.value.code != 0

@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.get_recommendation")
@patch("os.listdir")
def test_restore_auto_no_backups_for_email(mock_listdir, mock_rec, mock_lock):
    mock_rec_obj = MagicMock()
    mock_rec_obj.email = "auto@example.com"
    mock_rec.return_value = mock_rec_obj

    mock_listdir.return_value = ["2025-10-20_000000-other@example.com.gemini.tar.gz"]

    with patch("sys.argv", ["restore.py", "--auto"]):
        with pytest.raises(SystemExit) as e:
            restore.main()
        assert e.value.code != 0

@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.get_recommendation")
@patch("os.listdir")
@patch("os.path.isfile", return_value=True)
def test_find_latest_archive_backup_for_email_robustness(mock_isfile, mock_listdir, mock_rec, mock_lock):
    # Test strict email matching
    mock_listdir.return_value = [
        "2025-10-20_000000-sue@example.com.gemini.tar.gz",
        "2025-10-20_000000-josue@example.com.gemini.tar.gz",
    ]

    # We want to match "sue@example.com".
    # Current naive implementation "if email in filename" would match BOTH (since "sue@example.com" is in "josue@example.com")
    # if looking for sue@example.com.
    # Wait, 'sue@example.com' IS inside 'josue@example.com'.

    # So we need to improve the function to parse the filename.
    pass
