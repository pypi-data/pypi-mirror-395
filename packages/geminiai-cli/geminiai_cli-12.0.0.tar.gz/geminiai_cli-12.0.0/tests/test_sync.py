# tests/test_sync.py

import pytest
from unittest.mock import patch, MagicMock
import os
from geminiai_cli.sync import perform_sync, get_local_backups, get_cloud_backups

def mock_args(backup_dir="/tmp/backups", b2_id=None, b2_key=None, bucket=None):
    return MagicMock(backup_dir=backup_dir, b2_id=b2_id, b2_key=b2_key, bucket=bucket)

@patch("os.path.isdir", return_value=True)
@patch("os.listdir")
@patch("os.path.isfile", return_value=True)
def test_get_local_backups(mock_isfile, mock_listdir, mock_isdir):
    mock_listdir.return_value = ["file1.gemini.tar.gz", "file2.txt"]
    files = get_local_backups("/path")
    assert "file1.gemini.tar.gz" in files
    assert "file2.txt" not in files

@patch("os.path.isdir", return_value=False)
def test_get_local_backups_no_dir(mock_isdir):
    # get_local_backups returns empty set if dir not found
    files = get_local_backups("/path")
    assert files == set()

def test_get_cloud_backups():
    mock_b2 = MagicMock()

    file1 = MagicMock()
    file1.name = "cloud.gemini.tar.gz" # Fixed attribute name from file_name to name based on implementation

    file2 = MagicMock()
    file2.name = "cloud.txt"

    mock_b2.list_files.return_value = [file1, file2] # list_files returns a list of file objects

    files = get_cloud_backups(mock_b2)
    assert "cloud.gemini.tar.gz" in files
    assert "cloud.txt" not in files

def test_get_cloud_backups_fail():
    mock_b2 = MagicMock()
    mock_b2.list_files.side_effect = Exception("Fail")
    with pytest.raises(SystemExit):
        get_cloud_backups(mock_b2)

@patch("geminiai_cli.sync.get_cloud_provider")
@patch("geminiai_cli.sync.resolve_credentials")
@patch("geminiai_cli.sync.get_local_backups")
@patch("geminiai_cli.sync.get_cloud_backups")
@patch("geminiai_cli.sync.cprint")
def test_perform_sync_push_upload(mock_cprint, mock_get_cloud, mock_get_local, mock_creds, mock_get_provider):
    mock_creds.return_value = ("id", "key", "bucket")
    mock_get_local.return_value = {"local.gemini.tar.gz"}
    mock_get_cloud.return_value = set() # Empty cloud

    mock_b2 = MagicMock()
    mock_get_provider.return_value = mock_b2

    args = mock_args()
    with patch("os.path.isdir", return_value=True):
         perform_sync("push", args)

    mock_b2.upload_file.assert_called()

@patch("geminiai_cli.sync.get_cloud_provider")
@patch("geminiai_cli.sync.resolve_credentials")
@patch("geminiai_cli.sync.get_local_backups")
@patch("geminiai_cli.sync.get_cloud_backups")
@patch("geminiai_cli.sync.cprint")
def test_perform_sync_push_no_upload(mock_cprint, mock_get_cloud, mock_get_local, mock_creds, mock_get_provider):
    mock_creds.return_value = ("id", "key", "bucket")
    mock_get_local.return_value = {"file.gemini.tar.gz"}
    mock_get_cloud.return_value = {"file.gemini.tar.gz"} # Already exists

    mock_b2 = MagicMock()
    mock_get_provider.return_value = mock_b2

    args = mock_args()
    with patch("os.path.isdir", return_value=True):
        perform_sync("push", args)

    mock_b2.upload_file.assert_not_called()

@patch("geminiai_cli.sync.get_cloud_provider")
@patch("geminiai_cli.sync.resolve_credentials")
@patch("geminiai_cli.sync.get_local_backups")
@patch("geminiai_cli.sync.get_cloud_backups")
@patch("geminiai_cli.sync.cprint")
def test_perform_sync_pull_download(mock_cprint, mock_get_cloud, mock_get_local, mock_creds, mock_get_provider):
    mock_creds.return_value = ("id", "key", "bucket")
    mock_get_local.return_value = set()
    mock_get_cloud.return_value = {"cloud.gemini.tar.gz"}

    mock_b2 = MagicMock()
    mock_get_provider.return_value = mock_b2

    args = mock_args()
    with patch("os.makedirs"): # mock makedirs for backup_dir
        with patch("os.path.isdir", return_value=True):
             perform_sync("pull", args)

    mock_b2.download_file.assert_called()

@patch("geminiai_cli.sync.get_cloud_provider")
@patch("geminiai_cli.sync.resolve_credentials")
@patch("geminiai_cli.sync.get_local_backups")
@patch("geminiai_cli.sync.get_cloud_backups")
@patch("geminiai_cli.sync.cprint")
def test_perform_sync_pull_no_download(mock_cprint, mock_get_cloud, mock_get_local, mock_creds, mock_get_provider):
    mock_creds.return_value = ("id", "key", "bucket")
    mock_get_local.return_value = {"file.gemini.tar.gz"}
    mock_get_cloud.return_value = {"file.gemini.tar.gz"}

    mock_b2 = MagicMock()
    mock_get_provider.return_value = mock_b2

    args = mock_args()
    with patch("os.makedirs"):
        with patch("os.path.isdir", return_value=True):
            perform_sync("pull", args)

    mock_b2.download_file.assert_not_called()

@patch("geminiai_cli.sync.get_cloud_provider")
@patch("geminiai_cli.sync.cprint")
def test_perform_sync_push_missing_dir(mock_cprint, mock_get_provider):
    mock_b2 = MagicMock()
    mock_get_provider.return_value = mock_b2
    args = mock_args()

    with patch("os.path.isdir", return_value=False):
        with pytest.raises(SystemExit):
            perform_sync("push", args)
