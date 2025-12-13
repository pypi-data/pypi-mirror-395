
import os
import argparse
import unittest.mock
import pytest
from geminiai_cli.backup import perform_backup
from geminiai_cli.restore import perform_restore, parse_timestamp_from_name

@pytest.fixture
def mock_subprocess(mocker):
    return mocker.patch("geminiai_cli.backup.subprocess.run")

@pytest.fixture
def mock_restore_subprocess(mocker):
    return mocker.patch("geminiai_cli.restore.subprocess.run")

def test_backup_encrypt_calls_gpg(mocker, mock_subprocess):
    # Mock filesystem and other dependencies
    mocker.patch("geminiai_cli.backup.os.path.exists", return_value=True)
    mocker.patch("geminiai_cli.backup.os.path.abspath", side_effect=lambda x: x)
    mocker.patch("geminiai_cli.backup.os.path.expanduser", side_effect=lambda x: x)
    mocker.patch("geminiai_cli.backup.ensure_dir")
    mocker.patch("geminiai_cli.backup.read_active_email", return_value="test@example.com")
    mocker.patch("geminiai_cli.backup.acquire_lock")
    mocker.patch("geminiai_cli.backup.fcntl.flock")
    mocker.patch("geminiai_cli.backup.shutil.rmtree")
    mocker.patch("geminiai_cli.backup.os.replace")
    mocker.patch("geminiai_cli.backup.atomic_symlink")
    mocker.patch("geminiai_cli.backup.os.remove") # Mock remove to prevent FileNotFoundError

    # Mock diff verification to pass
    mock_subprocess.return_value.returncode = 0

    # Args
    args = argparse.Namespace(
        src="/tmp/src",
        archive_dir="/tmp/archive",
        dest_dir_parent="/tmp/dest",
        dry_run=False,
        cloud=False,
        encrypt=True  # New flag
    )

    # Mock environment variable for password
    with unittest.mock.patch.dict(os.environ, {"GEMINI_BACKUP_PASSWORD": "password123"}):
        perform_backup(args)

    # Verify gpg command was called
    gpg_called = False
    for call in mock_subprocess.call_args_list:
        if len(call[0]) > 0:
             cmd = call[0][0]
             # check if cmd is list (for gpg) or string (for tar/diff)
             if isinstance(cmd, list) and cmd[0] == "gpg":
                gpg_called = True
                assert "--symmetric" in cmd
                assert ".tar.gz.gpg" in cmd[-2] # Output
                assert "--passphrase-fd" in cmd
                break

    assert gpg_called, "GPG command was not called during encrypted backup"

def test_restore_decrypt_calls_gpg(mocker, mock_restore_subprocess):
    # Mock filesystem
    mocker.patch("geminiai_cli.restore.os.path.exists", return_value=True)
    mocker.patch("geminiai_cli.restore.os.path.abspath", side_effect=lambda x: x)
    mocker.patch("geminiai_cli.restore.os.path.expanduser", side_effect=lambda x: x)
    mocker.patch("geminiai_cli.restore.os.makedirs")
    mocker.patch("geminiai_cli.restore.acquire_lock")
    mocker.patch("geminiai_cli.restore.fcntl.flock")
    mocker.patch("geminiai_cli.restore.shutil.rmtree")
    mocker.patch("geminiai_cli.restore.shutil.move")
    mocker.patch("geminiai_cli.restore.os.replace")
    mocker.patch("geminiai_cli.restore.os.remove")
    mocker.patch("geminiai_cli.restore.tempfile.mkdtemp", return_value="/tmp/work_tmp")
    mocker.patch("geminiai_cli.restore.get_active_session", return_value=None)

    # Mock file discovery
    # Ensure regex matches this
    mocker.patch("geminiai_cli.restore.os.listdir", return_value=["2025-01-01_120000-test@example.com.gemini.tar.gz.gpg"])
    mocker.patch("geminiai_cli.restore.os.path.isfile", return_value=True)

    # Mock diff verification
    mock_restore_subprocess.return_value.returncode = 0

    # Args
    args = argparse.Namespace(
        dest="/tmp/dest",
        search_dir="/tmp/archive",
        force=False,
        dry_run=False,
        cloud=False,
        auto=False
    )

    # Mock environment variable for password
    with unittest.mock.patch.dict(os.environ, {"GEMINI_BACKUP_PASSWORD": "password123"}):
        perform_restore(args)

    # Verify gpg command was called
    gpg_called = False
    for call in mock_restore_subprocess.call_args_list:
        if len(call[0]) > 0:
             cmd = call[0][0]
             if isinstance(cmd, list) and cmd[0] == "gpg":
                gpg_called = True
                assert "--decrypt" in cmd
                assert ".tar.gz.gpg" in cmd[-1] # Input
                assert "--passphrase-fd" in cmd
                break

    assert gpg_called, "GPG command was not called during encrypted restore"
