# tests/test_sync.py

import pytest
from unittest.mock import patch, MagicMock
import os
from geminiai_cli.sync import cloud_sync, local_sync, get_local_backups, get_cloud_backups

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
def test_get_local_backups_fail(mock_isdir):
    with pytest.raises(SystemExit):
        get_local_backups("/path")

def test_get_cloud_backups():
    mock_b2 = MagicMock()

    file1 = MagicMock()
    file1.file_name = "cloud.gemini.tar.gz"

    file2 = MagicMock()
    file2.file_name = "cloud.txt"

    mock_b2.list_backups.return_value = [(file1, None), (file2, None)]

    files = get_cloud_backups(mock_b2)
    assert "cloud.gemini.tar.gz" in files
    assert "cloud.txt" not in files

def test_get_cloud_backups_fail():
    mock_b2 = MagicMock()
    mock_b2.list_backups.side_effect = Exception("Fail")
    with pytest.raises(SystemExit):
        get_cloud_backups(mock_b2)

@patch("geminiai_cli.sync.B2Manager")
@patch("geminiai_cli.sync.resolve_credentials")
@patch("geminiai_cli.sync.get_local_backups")
@patch("geminiai_cli.sync.get_cloud_backups")
@patch("geminiai_cli.sync.cprint")
def test_cloud_sync_upload(mock_cprint, mock_get_cloud, mock_get_local, mock_creds, mock_b2_class):
    mock_creds.return_value = ("id", "key", "bucket")
    mock_get_local.return_value = {"local.gemini.tar.gz"}
    mock_get_cloud.return_value = set() # Empty cloud

    mock_b2 = mock_b2_class.return_value

    args = mock_args()
    cloud_sync(args)

    mock_b2.upload.assert_called()

@patch("geminiai_cli.sync.B2Manager")
@patch("geminiai_cli.sync.resolve_credentials")
@patch("geminiai_cli.sync.get_local_backups")
@patch("geminiai_cli.sync.get_cloud_backups")
@patch("geminiai_cli.sync.cprint")
def test_cloud_sync_no_upload(mock_cprint, mock_get_cloud, mock_get_local, mock_creds, mock_b2_class):
    mock_creds.return_value = ("id", "key", "bucket")
    mock_get_local.return_value = {"file.gemini.tar.gz"}
    mock_get_cloud.return_value = {"file.gemini.tar.gz"} # Already exists

    mock_b2 = mock_b2_class.return_value

    args = mock_args()
    cloud_sync(args)

    mock_b2.upload.assert_not_called()

@patch("geminiai_cli.sync.B2Manager")
@patch("geminiai_cli.sync.resolve_credentials")
@patch("geminiai_cli.sync.get_local_backups")
@patch("geminiai_cli.sync.get_cloud_backups")
@patch("geminiai_cli.sync.cprint")
def test_local_sync_download(mock_cprint, mock_get_cloud, mock_get_local, mock_creds, mock_b2_class):
    mock_creds.return_value = ("id", "key", "bucket")
    mock_get_local.return_value = set()
    mock_get_cloud.return_value = {"cloud.gemini.tar.gz"}

    mock_b2 = mock_b2_class.return_value

    args = mock_args()
    with patch("os.makedirs"): # mock makedirs for backup_dir
        local_sync(args)

    mock_b2.download.assert_called()

@patch("geminiai_cli.sync.B2Manager")
@patch("geminiai_cli.sync.resolve_credentials")
@patch("geminiai_cli.sync.get_local_backups")
@patch("geminiai_cli.sync.get_cloud_backups")
@patch("geminiai_cli.sync.cprint")
def test_local_sync_no_download(mock_cprint, mock_get_cloud, mock_get_local, mock_creds, mock_b2_class):
    mock_creds.return_value = ("id", "key", "bucket")
    mock_get_local.return_value = {"file.gemini.tar.gz"}
    mock_get_cloud.return_value = {"file.gemini.tar.gz"}

    mock_b2 = mock_b2_class.return_value

    args = mock_args()
    with patch("os.makedirs"):
        local_sync(args)

    mock_b2.download.assert_not_called()
