# tests/test_prune.py

import pytest
from unittest.mock import patch, MagicMock, call
import os
import time
from geminiai_cli.prune import do_prune, get_backup_list, get_backup_list_dirs, prune_list, parse_ts

def mock_args(backup_dir="/tmp/backups", keep=2, cloud=False, cloud_only=False, dry_run=False, b2_id=None, b2_key=None, bucket=None):
    return MagicMock(backup_dir=backup_dir, keep=keep, cloud=cloud, cloud_only=cloud_only, dry_run=dry_run, b2_id=b2_id, b2_key=b2_key, bucket=bucket)

def test_parse_ts():
    ts = parse_ts("2023-01-01_120000-backup.gemini.tar.gz")
    assert ts is not None
    assert ts.tm_year == 2023

    assert parse_ts("invalid") is None
    assert parse_ts("2023-01-01_120000-backup.gemini") is not None # Directory format

def test_get_backup_list():
    files = [
        "2023-01-01_100000-user@example.com.gemini.tar.gz",
        "2023-01-02_100000-user@example.com.gemini.tar.gz",
        "invalid.txt",
        "2023-01-03_100000-user@example.com.gemini" # Should be ignored by get_backup_list
    ]
    backups = get_backup_list(files)
    assert len(backups) == 2
    # Should be sorted newest first
    assert backups[0][1] == "2023-01-02_100000-user@example.com.gemini.tar.gz"
    assert backups[1][1] == "2023-01-01_100000-user@example.com.gemini.tar.gz"

def test_get_backup_list_dirs():
    files = [
        "2023-01-01_100000-user@example.com.gemini",
        "2023-01-02_100000-user@example.com.gemini",
        "invalid.txt",
        "2023-01-03_100000-user@example.com.gemini.tar.gz" # Should be ignored by get_backup_list_dirs
    ]
    dirs = get_backup_list_dirs(files)
    assert len(dirs) == 2
    # Should be sorted newest first
    assert dirs[0][1] == "2023-01-02_100000-user@example.com.gemini"
    assert dirs[1][1] == "2023-01-01_100000-user@example.com.gemini"

def test_prune_list_no_action():
    backups = [("ts1", "file1"), ("ts2", "file2")]
    callback = MagicMock()
    # Keep 5, have 2. No prune.
    prune_list(backups, 5, False, callback)
    callback.assert_not_called()

def test_prune_list_action():
    backups = [("ts3", "file3"), ("ts2", "file2"), ("ts1", "file1")]
    callback = MagicMock()
    # Keep 1, have 3. Delete 2 oldest (file2, file1).
    prune_list(backups, 1, False, callback)
    assert callback.call_count == 2
    callback.assert_has_calls([call("file2"), call("file1")])

def test_prune_list_dry_run():
    backups = [("ts3", "file3"), ("ts2", "file2"), ("ts1", "file1")]
    callback = MagicMock()
    prune_list(backups, 1, True, callback)
    callback.assert_not_called()

@patch("os.path.exists", return_value=True)
@patch("os.listdir")
@patch("os.remove")
@patch("shutil.rmtree") # For directory deletion
@patch("geminiai_cli.prune.cprint")
def test_do_prune_local(mock_cprint, mock_rmtree, mock_remove, mock_listdir, mock_exists):
    # Mock os.listdir to return different lists for archives and directories
    # os.listdir for archive_dir, then for dir_backup_path
    mock_listdir.side_effect = [
        # First call for archive_dir (local archives)
        [
            "2023-01-01_100000-u.gemini.tar.gz",
            "2023-01-02_100000-u.gemini.tar.gz",
            "2023-01-03_100000-u.gemini.tar.gz"
        ],
        # Second call for dir_backup_path (local directories)
        [
            "2023-01-01_110000-u.gemini",
            "2023-01-02_110000-u.gemini",
            "2023-01-03_110000-u.gemini"
        ]
    ]

    args = mock_args(keep=1) # Keep only the newest for both archives and directories

    with patch("os.path.abspath", side_effect=lambda x: x): # Mock abspath for test simplicity
        with patch("os.path.expanduser", side_effect=lambda x: x): # Mock expanduser
            do_prune(args)

    # Should delete 2 oldest archives
    assert mock_remove.call_count == 2
    calls = [args[0][0] for args in mock_remove.call_args_list]
    assert any("2023-01-01_100000-u.gemini.tar.gz" in c for c in calls)
    assert any("2023-01-02_100000-u.gemini.tar.gz" in c for c in calls)

    # Should delete 2 oldest directories
    assert mock_rmtree.call_count == 2
    calls = [args[0][0] for args in mock_rmtree.call_args_list]
    assert any("2023-01-01_110000-u.gemini" in c for c in calls)
    assert any("2023-01-02_110000-u.gemini" in c for c in calls)


@patch("os.path.exists", return_value=False)
@patch("geminiai_cli.prune.cprint")
def test_do_prune_local_no_dir(mock_cprint, mock_exists):
    args = mock_args(keep=1) # default local
    do_prune(args)
    # Just prints warning for both archive and directory paths not found
    assert any("Archive backup directory not found" in str(args) for args in mock_cprint.call_args_list)
    assert any("Directory backup path not found" in str(args) for args in mock_cprint.call_args_list)


@patch("geminiai_cli.prune.resolve_credentials")
@patch("geminiai_cli.prune.B2Manager")
@patch("geminiai_cli.prune.cprint")
def test_do_prune_cloud(mock_cprint, mock_b2_cls, mock_creds):
    mock_creds.return_value = ("id", "key", "bucket")

    mock_b2 = mock_b2_cls.return_value

    fv1 = MagicMock()
    fv1.file_name = "2023-01-01_100000-u.gemini.tar.gz"
    fv1.id_ = "id1"

    fv2 = MagicMock()
    fv2.file_name = "2023-01-02_100000-u.gemini.tar.gz"
    fv2.id_ = "id2"

    mock_b2.list_backups.return_value = [(fv1, None), (fv2, None)]

    args = mock_args(keep=1, cloud=True, backup_dir="/tmp/nonexistent") # Local part will be skipped
    
    with patch("os.path.exists", return_value=False): # Skip local checks
        do_prune(args)

    mock_b2.bucket.delete_file_version.assert_called_once_with("id1", "2023-01-01_100000-u.gemini.tar.gz")

@patch("geminiai_cli.prune.resolve_credentials")
@patch("geminiai_cli.prune.cprint")
def test_do_prune_cloud_no_creds(mock_cprint, mock_creds):
    mock_creds.return_value = (None, None, None)
    args = mock_args(cloud=True, cloud_only=False, backup_dir="/tmp/nonexistent") # Local will try to run
    
    with patch("os.path.exists", return_value=False): # Skip local checks
        # This should warn about skipping cloud, not exit, if cloud_only is False.
        do_prune(args)
    assert any("Skipping (credentials not set)." in str(args) for args in mock_cprint.call_args_list)

@patch("geminiai_cli.prune.resolve_credentials")
@patch("geminiai_cli.prune.cprint")
def test_do_prune_cloud_only_no_creds_error(mock_cprint, mock_creds):
    mock_creds.return_value = (None, None, None)
    args = mock_args(cloud_only=True)
    do_prune(args)
    # Error printed
    assert any("Cloud credentials missing." in str(args) for args in mock_cprint.call_args_list)


@patch("geminiai_cli.prune.resolve_credentials")
@patch("geminiai_cli.prune.B2Manager")
@patch("geminiai_cli.prune.cprint")
def test_do_prune_cloud_exception(mock_cprint, mock_b2_cls, mock_creds):
    mock_creds.return_value = ("id", "key", "bucket")
    mock_b2_cls.side_effect = Exception("B2 Fail")

    args = mock_args(cloud=True, backup_dir="/tmp/nonexistent")

    with patch("os.path.exists", return_value=False):
        do_prune(args)

    assert any("Cloud prune failed" in str(args) for args in mock_cprint.call_args_list)

@patch("os.path.exists", return_value=True)
@patch("os.listdir")
@patch("os.remove")
@patch("shutil.rmtree")
@patch("geminiai_cli.prune.cprint")
@patch("geminiai_cli.prune.OLD_CONFIGS_DIR", "/root/.geminiai-cli/old_configs")
def test_do_prune_local_remove_fail(mock_cprint, mock_rmtree, mock_remove, mock_listdir, mock_exists):
    mock_listdir.side_effect = [
        ["2023-01-01_100000-u.gemini.tar.gz"], # archive_dir
        ["2023-01-01_110000-u.gemini"] # dir_backup_path
    ]
    mock_remove.side_effect = Exception("Permission denied for file")
    mock_rmtree.side_effect = Exception("Permission denied for dir")
    args = mock_args(keep=0) # delete all

    with patch("os.path.abspath", side_effect=lambda x: x):
        with patch("os.path.expanduser", side_effect=lambda x: x):
            do_prune(args)

    # Assert error logged - relaxed check
    file_err_found = False
    dir_err_found = False
    for call_args in mock_cprint.call_args_list:
        arg_str = str(call_args)
        if "Failed to remove" in arg_str and "2023-01-01_100000-u.gemini.tar.gz" in arg_str:
            file_err_found = True
        if "Failed to remove directory" in arg_str and "2023-01-01_110000-u.gemini" in arg_str:
            dir_err_found = True
    
    assert file_err_found, f"File removal error not found in cprint calls: {mock_cprint.call_args_list}"
    assert dir_err_found, f"Directory removal error not found in cprint calls: {mock_cprint.call_args_list}"


@patch("geminiai_cli.prune.resolve_credentials")
@patch("geminiai_cli.prune.B2Manager")
@patch("geminiai_cli.prune.cprint")
def test_do_prune_cloud_delete_fail(mock_cprint, mock_b2_cls, mock_creds):
    mock_creds.return_value = ("id", "key", "bucket")
    mock_b2 = mock_b2_cls.return_value

    fv1 = MagicMock()
    fv1.file_name = "2023-01-01_100000-u.gemini.tar.gz"
    fv1.id_ = "id1"
    fv2 = MagicMock()
    fv2.file_name = "2023-01-02_100000-u.gemini.tar.gz"
    fv2.id_ = "id2"

    mock_b2.list_backups.return_value = [(fv1, None), (fv2, None)]
    mock_b2.bucket.delete_file_version.side_effect = Exception("API Fail")

    args = mock_args(keep=1, cloud=True, backup_dir="/tmp/nonexistent")

    with patch("os.path.exists", return_value=False):
        do_prune(args)

    mock_b2.bucket.delete_file_version.assert_called()
    assert any("Failed to delete cloud file 2023-01-01_100000-u.gemini.tar.gz" in str(args) for args in mock_cprint.call_args_list)
