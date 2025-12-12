# tests/test_prune.py

import pytest
from unittest.mock import patch, MagicMock, ANY
import os
import time
from geminiai_cli.prune import do_prune, get_backup_list, parse_ts, prune_list

# Helper to create mock args
def mock_args(backup_dir="/tmp/backups", keep=2, cloud=False, cloud_only=False, dry_run=False,
              b2_id=None, b2_key=None, bucket=None):
    return MagicMock(backup_dir=backup_dir, keep=keep, cloud=cloud, cloud_only=cloud_only, dry_run=dry_run,
                     b2_id=b2_id, b2_key=b2_key, bucket=bucket)

def test_parse_ts():
    ts = parse_ts("2023-01-01_120000-backup.gemini.tar.gz")
    assert ts is not None
    assert ts.tm_year == 2023

    assert parse_ts("invalid") is None

def test_get_backup_list():
    files = [
        "2023-01-01_120000-backup.gemini.tar.gz",
        "2023-01-02_120000-backup.gemini.tar.gz",
        "other_file.txt"
    ]
    backups = get_backup_list(files)
    assert len(backups) == 2
    assert backups[0][1] == "2023-01-02_120000-backup.gemini.tar.gz" # Newest first

@patch("os.path.exists", return_value=True)
@patch("os.listdir")
@patch("os.remove")
@patch("geminiai_cli.prune.cprint")
def test_do_prune_local(mock_cprint, mock_remove, mock_listdir, mock_exists):
    mock_listdir.return_value = [
        "2023-01-01_120000-backup.gemini.tar.gz",
        "2023-01-02_120000-backup.gemini.tar.gz",
        "2023-01-03_120000-backup.gemini.tar.gz"
    ]

    args = mock_args(keep=1) # Keep only the newest (3rd one)
    do_prune(args)

    assert mock_remove.call_count == 2 # Should remove the oldest two

    # Check deletion order/targets (oldest are deleted)
    # The list passed to prune_list is sorted newest first: 03, 02, 01
    # Keep 1 -> Keep 03. Delete 02, 01.

    calls = [args[0][0] for args in mock_remove.call_args_list]
    assert any("2023-01-01" in c for c in calls)
    assert any("2023-01-02" in c for c in calls)

@patch("os.path.exists", return_value=True)
@patch("os.listdir")
@patch("geminiai_cli.prune.cprint")
def test_do_prune_local_dry_run(mock_cprint, mock_listdir, mock_exists):
    mock_listdir.return_value = [
        "2023-01-01_120000-backup.gemini.tar.gz",
        "2023-01-02_120000-backup.gemini.tar.gz"
    ]
    args = mock_args(keep=1, dry_run=True)

    with patch("builtins.print") as mock_print:
        do_prune(args)
        assert mock_print.call_count >= 1 # Should print dry-run message
        # No removal mock needed as it shouldn't be called

@patch("geminiai_cli.prune.B2Manager")
@patch("geminiai_cli.prune.get_setting")
@patch("geminiai_cli.prune.cprint")
def test_do_prune_cloud(mock_cprint, mock_get_setting, mock_b2_class):
    args = mock_args(cloud=True, b2_id="id", b2_key="key", bucket="bucket")

    mock_b2_instance = mock_b2_class.return_value
    mock_bucket = MagicMock()
    mock_b2_instance.bucket = mock_bucket

    # Mock list_backups generator
    file1 = MagicMock()
    file1.file_name = "2023-01-01_120000-backup.gemini.tar.gz"
    file1.id_ = "id1"

    file2 = MagicMock()
    file2.file_name = "2023-01-02_120000-backup.gemini.tar.gz"
    file2.id_ = "id2"

    mock_b2_instance.list_backups.return_value = [(file1, None), (file2, None)]

    # Keep 1 -> Delete file1 (oldest)
    args.keep = 1

    do_prune(args)

    mock_bucket.delete_file_version.assert_called_with("id1", "2023-01-01_120000-backup.gemini.tar.gz")

@patch("geminiai_cli.prune.cprint")
@patch("geminiai_cli.credentials.get_setting", return_value=None)
@patch.dict(os.environ, {}, clear=True)
def test_do_prune_cloud_no_creds(mock_cprint, mock_get_setting):
    args = mock_args(cloud_only=True) # Forces cloud check
    with pytest.raises(SystemExit) as e:
        do_prune(args)
    assert e.value.code == 1

@patch("geminiai_cli.prune.B2Manager")
@patch("geminiai_cli.prune.cprint")
def test_do_prune_cloud_error(mock_cprint, mock_b2_class):
    args = mock_args(cloud=True, b2_id="id", b2_key="key", bucket="bucket")
    mock_b2_class.side_effect = Exception("Auth fail")

    do_prune(args)

    # Check for error print. We need to iterate through calls
    found = False
    for call in mock_cprint.call_args_list:
        # call is a tuple of (args, kwargs)
        # cprint is called like cprint(COLOR, TEXT)
        if len(call[0]) > 1 and "Cloud prune failed" in call[0][1]:
            found = True
            break

    assert found

@patch("os.path.exists", return_value=True)
@patch("os.listdir")
@patch("os.remove")
@patch("geminiai_cli.prune.cprint")
def test_do_prune_local_fail(mock_cprint, mock_remove, mock_listdir, mock_exists):
    mock_listdir.return_value = [
        "2023-01-01_120000-backup.gemini.tar.gz",
        "2023-01-02_120000-backup.gemini.tar.gz"
    ]
    # Keep 1 -> delete 1
    args = mock_args(keep=1)
    mock_remove.side_effect = Exception("Perm denied")

    do_prune(args)

    assert any("Failed to remove" in str(args) for args in mock_cprint.call_args_list)

@patch("os.path.exists", return_value=False)
@patch("geminiai_cli.prune.cprint")
def test_do_prune_local_dir_not_found(mock_cprint, mock_exists):
    args = mock_args() # default local
    do_prune(args)
    assert any("Backup directory not found" in str(args) for args in mock_cprint.call_args_list)

@patch("geminiai_cli.prune.cprint")
@patch("geminiai_cli.credentials.get_setting", return_value=None)
@patch.dict(os.environ, {}, clear=True)
def test_do_prune_cloud_skip_no_creds(mock_cprint, mock_get_setting):
    # Cloud requested via --cloud (not cloud_only), so local runs too.
    # If creds missing, resolve_credentials exits.
    args = mock_args(cloud=True) # b2_id=None
    with pytest.raises(SystemExit) as e:
        do_prune(args)
    assert e.value.code == 1

@patch("geminiai_cli.prune.B2Manager")
@patch("geminiai_cli.prune.get_setting")
@patch("geminiai_cli.prune.cprint")
def test_do_prune_cloud_delete_fail(mock_cprint, mock_get_setting, mock_b2_class):
    args = mock_args(cloud=True, b2_id="id", b2_key="key", bucket="bucket")

    mock_b2_instance = mock_b2_class.return_value
    mock_bucket = MagicMock()
    mock_b2_instance.bucket = mock_bucket

    file1 = MagicMock()
    file1.file_name = "2023-01-01_120000-backup.gemini.tar.gz"
    file1.id_ = "id1"
    file2 = MagicMock()
    file2.file_name = "2023-01-02_120000-backup.gemini.tar.gz"
    file2.id_ = "id2"

    mock_b2_instance.list_backups.return_value = [(file1, None), (file2, None)]
    mock_bucket.delete_file_version.side_effect = Exception("B2 Delete Fail")

    args.keep = 1
    do_prune(args)

    assert any("Failed to delete cloud file" in str(args) for args in mock_cprint.call_args_list)

def test_prune_list_no_action():
    # Test len <= keep_count
    with patch("geminiai_cli.prune.cprint") as mock_cprint:
        backups = ["a", "b"]
        prune_list(backups, 5, False, None)
        assert any("No pruning needed" in str(args) for args in mock_cprint.call_args_list)
