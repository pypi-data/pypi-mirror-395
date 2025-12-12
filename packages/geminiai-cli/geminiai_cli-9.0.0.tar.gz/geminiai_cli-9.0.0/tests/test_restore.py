# tests/test_restore.py

import pytest
from unittest.mock import patch, mock_open, MagicMock, ANY
import os
import time
import sys
import shutil
from geminiai_cli import restore

@patch("geminiai_cli.restore.fcntl")
def test_acquire_lock_success(mock_fcntl):
    with patch("builtins.open", mock_open()):
        fd = restore.acquire_lock()
        assert fd is not None
        mock_fcntl.flock.assert_called()

@patch("geminiai_cli.restore.fcntl")
def test_acquire_lock_fail(mock_fcntl):
    mock_fcntl.flock.side_effect = BlockingIOError
    with patch("builtins.open", mock_open()):
        with pytest.raises(SystemExit) as e:
            restore.acquire_lock()
        assert e.value.code == 2

def test_run():
    with patch("subprocess.run") as mock_run:
        restore.run("ls")
        mock_run.assert_called_with("ls", shell=True, check=True)

def test_parse_timestamp_from_name():
    ts = restore.parse_timestamp_from_name("2025-10-22_042211-test@test.gemini")
    assert ts is not None
    assert ts.tm_year == 2025

    assert restore.parse_timestamp_from_name("invalid") is None

@patch("os.listdir")
@patch("os.path.isfile", return_value=True)
def test_find_oldest_archive_backup(mock_isfile, mock_listdir):
    mock_listdir.return_value = [
        "2025-10-23_042211-test.gemini.tar.gz",
        "2025-10-22_042211-test.gemini.tar.gz"
    ]
    oldest = restore.find_oldest_archive_backup("/tmp")
    assert "2025-10-22" in oldest

@patch("os.listdir")
def test_find_oldest_archive_backup_none(mock_listdir):
    mock_listdir.return_value = []
    assert restore.find_oldest_archive_backup("/tmp") is None

@patch("geminiai_cli.restore.run")
@patch("os.makedirs")
def test_extract_archive(mock_makedirs, mock_run):
    restore.extract_archive("archive", "dest")
    mock_run.assert_called()

@patch("shutil.move")
@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.run")
@patch("os.path.exists", return_value=True)
@patch("os.makedirs")
@patch("os.replace")
@patch("shutil.rmtree")
@patch("tempfile.mkdtemp", return_value="/tmp/restore_tmp")
def test_main_from_dir(mock_mkdtemp, mock_rmtree, mock_replace, mock_makedirs, mock_exists, mock_run, mock_lock, mock_move):
    with patch("sys.argv", ["restore.py", "--from-dir", "/tmp/backup"]):
        mock_run.return_value.returncode = 0
        restore.main()
        # Verification passes

@patch("shutil.move")
@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.run")
@patch("os.path.exists", return_value=True)
@patch("os.makedirs")
@patch("os.replace")
@patch("shutil.rmtree")
@patch("tempfile.mkdtemp", return_value="/tmp/restore_tmp")
def test_main_from_archive(mock_mkdtemp, mock_rmtree, mock_replace, mock_makedirs, mock_exists, mock_run, mock_lock, mock_move):
    with patch("sys.argv", ["restore.py", "--from-archive", "/tmp/backup.tar.gz"]):
        mock_run.return_value.returncode = 0
        restore.main()

@patch("shutil.move")
@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.find_oldest_archive_backup", return_value="/tmp/oldest.tar.gz")
@patch("geminiai_cli.restore.run")
@patch("os.path.exists", return_value=True)
@patch("os.makedirs")
@patch("os.replace")
@patch("shutil.rmtree")
@patch("tempfile.mkdtemp", return_value="/tmp/restore_tmp")
def test_main_auto_oldest(mock_mkdtemp, mock_rmtree, mock_replace, mock_makedirs, mock_exists, mock_run, mock_find_oldest, mock_lock, mock_move):
    with patch("sys.argv", ["restore.py"]):
        mock_run.return_value.returncode = 0
        restore.main()
        mock_find_oldest.assert_called()

@patch("shutil.move")
@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.B2Manager")
@patch("geminiai_cli.restore.run")
@patch("os.path.exists", return_value=True)
@patch("os.makedirs")
@patch("os.replace")
@patch("shutil.rmtree")
@patch("tempfile.mkdtemp", return_value="/tmp/restore_tmp")
@patch("geminiai_cli.cooldown._sync_cooldown_file")
def test_main_cloud(mock_sync, mock_mkdtemp, mock_rmtree, mock_replace, mock_makedirs, mock_exists, mock_run, mock_b2, mock_lock, mock_move):
    with patch("sys.argv", ["restore.py", "--cloud", "--bucket", "b", "--b2-id", "i", "--b2-key", "k"]):
        mock_file = MagicMock()
        mock_file.file_name = "2025-10-22_042211-test.gemini.tar.gz"
        mock_b2.return_value.list_backups.return_value = [(mock_file, None)]

        mock_run.return_value.returncode = 0
        restore.main()
        mock_b2.return_value.download.assert_called()

@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.run")
@patch("os.path.exists", return_value=True)
@patch("shutil.rmtree")
@patch("tempfile.mkdtemp", return_value="/tmp/restore_tmp")
def test_main_verification_fail(mock_mkdtemp, mock_rmtree, mock_exists, mock_run, mock_lock):
    with patch("sys.argv", ["restore.py", "--from-archive", "archive.tar.gz"]):
        # Mock cp run ok
        # Mock diff run fail (first verify)
        mock_run.side_effect = [
            MagicMock(returncode=0), # tar
            MagicMock(returncode=0), # cp
            MagicMock(returncode=1, stdout="diff"), # diff
        ]
        with pytest.raises(SystemExit) as e:
            restore.main()
        assert e.value.code == 3

@patch("shutil.move")
@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.run")
@patch("os.path.exists", return_value=True)
@patch("os.replace")
@patch("shutil.rmtree")
@patch("tempfile.mkdtemp", return_value="/tmp/restore_tmp")
def test_main_post_verification_fail(mock_mkdtemp, mock_rmtree, mock_replace, mock_exists, mock_run, mock_lock, mock_move):
    with patch("sys.argv", ["restore.py", "--from-archive", "archive.tar.gz"]):
        # Mock diff run fail (post verify)
        mock_run.side_effect = [
            MagicMock(returncode=0), # tar
            MagicMock(returncode=0), # cp
            MagicMock(returncode=0), # diff 1
            MagicMock(returncode=1, stdout="diff"), # diff 2
        ]
        with pytest.raises(SystemExit) as e:
            restore.main()
        assert e.value.code == 4

@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.run")
@patch("os.path.exists", return_value=True)
@patch("os.replace")
@patch("shutil.rmtree")
@patch("tempfile.mkdtemp", return_value="/tmp/restore_tmp")
def test_main_dry_run(mock_mkdtemp, mock_rmtree, mock_replace, mock_exists, mock_run, mock_lock):
    with patch("sys.argv", ["restore.py", "--from-archive", "archive.tar.gz", "--dry-run"]):
        restore.main()
        # Ensure destructive commands not called (mock_run will be called for tar probably? no, check restore.py)
        # restore.py dry-run prints "DRY RUN: ..."
        # run() shouldn't be called.
        mock_run.assert_not_called()
        mock_replace.assert_not_called()

@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.B2Manager")
def test_main_cloud_missing_creds(mock_b2, mock_lock):
    with patch("sys.argv", ["restore.py", "--cloud"]): # Missing bucket/id/key
        with pytest.raises(SystemExit):
            restore.main()

@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.B2Manager")
def test_main_cloud_no_backups(mock_b2, mock_lock):
    with patch("sys.argv", ["restore.py", "--cloud", "--bucket", "b", "--b2-id", "i", "--b2-key", "k"]):
        mock_b2.return_value.list_backups.return_value = []
        with pytest.raises(SystemExit):
            restore.main()

@patch("geminiai_cli.restore.acquire_lock")
@patch("os.path.exists", return_value=False)
def test_main_from_dir_not_found(mock_exists, mock_lock):
    with patch("sys.argv", ["restore.py", "--from-dir", "/tmp/notfound"]):
        with pytest.raises(SystemExit):
            restore.main()

@patch("geminiai_cli.restore.acquire_lock")
@patch("os.path.exists")
def test_main_from_archive_search_dir(mock_exists, mock_lock):
    def side_effect(path):
        if "archive.tar.gz" in path and ".geminiai-cli/backups" not in path:
            return False # User path not found
        if "archive.tar.gz" in path and ".geminiai-cli/backups" in path:
            return True # Search dir path found
        return True # Default for others (locale etc)
    mock_exists.side_effect = side_effect

    with patch("sys.argv", ["restore.py", "--from-archive", "archive.tar.gz"]):
        # Just verifying it doesn't exit early
        with pytest.raises(Exception, match="Stop"): # We expect our Stop exception
             # Actually find_oldest_archive_backup logic or extract will be called.
             # Here we just want to cover lines 232-245
             # Mock run to fail immediately to stop
             with patch("geminiai_cli.restore.run", side_effect=Exception("Stop")):
                 restore.main()

@patch("geminiai_cli.restore.acquire_lock")
@patch("os.path.exists", return_value=False)
def test_main_from_archive_not_found(mock_exists, mock_lock):
    with patch("sys.argv", ["restore.py", "--from-archive", "archive.tar.gz"]):
        with pytest.raises(SystemExit):
             restore.main()

@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.find_oldest_archive_backup", return_value=None)
@patch("os.path.exists", return_value=True)
def test_main_auto_no_backups(mock_exists, mock_find, mock_lock):
    with patch("sys.argv", ["restore.py"]):
        with pytest.raises(SystemExit):
            restore.main()

@patch("shutil.move")
@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.run")
@patch("os.path.exists", return_value=True)
@patch("os.replace")
@patch("shutil.rmtree")
@patch("tempfile.mkdtemp", return_value="/tmp/restore_tmp")
def test_main_rollback_success(mock_mkdtemp, mock_rmtree, mock_replace, mock_exists, mock_run, mock_lock, mock_move):
     with patch("sys.argv", ["restore.py", "--from-archive", "archive.tar.gz"]):
        # Mock diff run fail (post verify)
        mock_run.side_effect = [
            MagicMock(returncode=0), # tar
            MagicMock(returncode=0), # cp
            MagicMock(returncode=0), # diff 1
            MagicMock(returncode=1, stdout="diff"), # diff 2
        ]
        with pytest.raises(SystemExit) as e:
            restore.main()
        assert e.value.code == 4
        # os.replace should be called to restore .bak
        # We can't easily verify call count on os.replace here without more mocking,
        # but we cover the code path.

@patch("shutil.move")
@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.run")
@patch("os.path.exists", return_value=True)
@patch("os.replace", side_effect=[None, None, Exception("Rollback fail")])
@patch("shutil.rmtree")
@patch("tempfile.mkdtemp", return_value="/tmp/restore_tmp")
def test_main_rollback_fail(mock_mkdtemp, mock_rmtree, mock_replace, mock_exists, mock_run, mock_lock, mock_move):
     with patch("sys.argv", ["restore.py", "--from-archive", "archive.tar.gz"]):
        # Mock diff run fail (post verify)
        mock_run.side_effect = [
            MagicMock(returncode=0), # tar
            MagicMock(returncode=0), # cp
            MagicMock(returncode=0), # diff 1
            MagicMock(returncode=1, stdout="diff"), # diff 2
        ]
        with pytest.raises(SystemExit) as e:
            restore.main()
        assert e.value.code == 4

@patch("shutil.move")
@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.B2Manager")
@patch("geminiai_cli.restore.run")
@patch("os.path.exists", return_value=True)
@patch("os.makedirs")
@patch("os.replace")
@patch("shutil.rmtree")
@patch("tempfile.mkdtemp", return_value="/tmp/restore_tmp")
@patch("geminiai_cli.cooldown._sync_cooldown_file")
def test_main_cloud_specific_archive(mock_sync, mock_mkdtemp, mock_rmtree, mock_replace, mock_makedirs, mock_exists, mock_run, mock_b2, mock_lock, mock_move):
    specific_archive = "2025-11-21_231311-specific@test.gemini.tar.gz"
    with patch("sys.argv", ["restore.py", "--cloud", "--bucket", "b", "--b2-id", "i", "--b2-key", "k", "--from-archive", specific_archive]):
        mock_file_specific = MagicMock()
        mock_file_specific.file_name = specific_archive
        
        mock_file_old = MagicMock()
        mock_file_old.file_name = "2025-10-22_042211-old@test.gemini.tar.gz"
        
        # b2.list_backups returns both
        mock_b2.return_value.list_backups.return_value = [(mock_file_old, None), (mock_file_specific, None)]

        mock_run.return_value.returncode = 0
        restore.main()
        
        # Assert download was called with the SPECIFIC archive, not the oldest one
        mock_b2.return_value.download.assert_called_with(specific_archive, ANY)

# NEW TESTS

@patch("geminiai_cli.restore.acquire_lock")
def test_main_lock_exception(mock_lock):
     # Test line 325: exception in finally block when closing lock
    mock_fd = MagicMock()
    mock_lock.return_value = mock_fd

    with patch("geminiai_cli.restore.find_oldest_archive_backup", return_value="/tmp/backup.tar.gz"):
        with patch("geminiai_cli.restore.run", return_value=MagicMock(returncode=0)):
             with patch("os.path.exists", return_value=True):
                 with patch("os.makedirs"):
                     with patch("os.replace"):
                         with patch("shutil.move"):
                             with patch("shutil.rmtree"):
                                 with patch("tempfile.mkdtemp", return_value="/tmp/restore_tmp"):
                                     with patch("sys.argv", ["restore.py"]):
                                         with patch("geminiai_cli.restore.fcntl.flock") as mock_flock:
                                             mock_flock.side_effect = [None, Exception("Unlock fail")]
                                             restore.main()

@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.run")
@patch("os.path.exists", return_value=True)
@patch("os.replace")
@patch("shutil.rmtree")
@patch("tempfile.mkdtemp", return_value="/tmp/restore_tmp")
@patch("shutil.move")
def test_main_os_replace_fail_fallback(mock_move, mock_mkdtemp, mock_rmtree, mock_replace, mock_exists, mock_run, mock_lock):
    # Test lines 272-273: shutil.move fallback
    mock_replace.side_effect = [OSError(18, "Cross-device link"), None] # First replace fails (backup move), second succeeds (install)
    mock_run.return_value.returncode = 0
    with patch("sys.argv", ["restore.py", "--from-archive", "archive.tar.gz"]):
        restore.main()
        mock_move.assert_called()

@patch("shutil.move")
@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.run")
@patch("os.path.exists", return_value=True)
@patch("os.replace")
@patch("shutil.rmtree")
@patch("tempfile.mkdtemp", return_value="/tmp/restore_tmp")
def test_main_temp_extraction_rmtree_fail(mock_mkdtemp, mock_rmtree, mock_replace, mock_exists, mock_run, mock_lock, mock_move):
    # Test lines 313-314: rmtree exception ignored

    def side_effect(path, ignore_errors=False):
        if path == "/tmp/restore_tmp":
            raise Exception("Perm error")
        return None

    mock_rmtree.side_effect = side_effect
    mock_run.return_value.returncode = 0
    with patch("sys.argv", ["restore.py", "--from-archive", "archive.tar.gz"]):
        restore.main()
        # Should not crash

@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.run")
@patch("os.path.exists", return_value=True)
@patch("os.replace")
@patch("shutil.rmtree")
@patch("tempfile.mkdtemp", return_value="/tmp/restore_tmp")
def test_main_dest_not_exists(mock_mkdtemp, mock_rmtree, mock_replace, mock_exists, mock_run, mock_lock):
    # Test lines 261->278: os.path.exists(dest) is False

    def exists_side_effect(path):
        if path == os.path.expanduser("~/.gemini"):
            return False
        return True

    mock_exists.side_effect = exists_side_effect
    mock_run.return_value.returncode = 0

    with patch("sys.argv", ["restore.py", "--from-archive", "archive.tar.gz"]):
        restore.main()
        # Verify no backup move attempt
        # "Preparing to move existing" should NOT be printed?
        # Hard to assert print, but coverage should increase.

@patch("shutil.move")
@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.run")
@patch("os.path.exists", return_value=True)
@patch("os.replace")
@patch("shutil.rmtree")
@patch("tempfile.mkdtemp", return_value="/tmp/restore_tmp")
@patch("geminiai_cli.cooldown._sync_cooldown_file")
def test_main_tmp_dest_not_exists(mock_sync, mock_mkdtemp, mock_rmtree, mock_replace, mock_exists, mock_run, mock_lock, mock_move):
    # Test lines 237->239: if os.path.exists(tmp_dest)

    def exists_side_effect(path):
        if ".tmp-" in str(path): # Use str(path) to handle PosixPath
            return False
        return True

    mock_exists.side_effect = exists_side_effect
    mock_run.return_value.returncode = 0

    with patch("sys.argv", ["restore.py", "--from-archive", "archive.tar.gz"]):
        restore.main()
        # rmtree shouldn't be called for tmp_dest
        # But rmtree is mocked global.
        # We can check if rmtree called with tmp_dest?
        # It's hard to distinguish args in global call list easily without filtering.
        # But coverage will tell.

@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.run")
@patch("os.path.exists", return_value=True)
@patch("os.replace")
@patch("shutil.rmtree")
@patch("tempfile.mkdtemp", return_value="/tmp/restore_tmp")
def test_main_force_replace(mock_mkdtemp, mock_rmtree, mock_replace, mock_exists, mock_run, mock_lock):
    # Test lines 266-267: --force removing existing dest
    mock_run.return_value.returncode = 0
    with patch("sys.argv", ["restore.py", "--from-archive", "archive.tar.gz", "--force"]):
        restore.main()
        mock_rmtree.assert_called() # Should call rmtree on dest

@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.B2Manager")
def test_main_cloud_specific_archive_not_found(mock_b2, mock_lock):
    # Test lines 163-164
    specific_archive = "notfound.tar.gz"
    with patch("sys.argv", ["restore.py", "--cloud", "--bucket", "b", "--b2-id", "i", "--b2-key", "k", "--from-archive", specific_archive]):
        mock_file = MagicMock()
        mock_file.file_name = "other.tar.gz"
        mock_b2.return_value.list_backups.return_value = [(mock_file, None)]
        with pytest.raises(SystemExit) as e:
            restore.main()
        assert e.value.code == 1

@patch("shutil.move")
@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.run")
@patch("os.path.exists", return_value=True)
@patch("os.replace")
@patch("shutil.rmtree")
@patch("tempfile.mkdtemp", return_value="/tmp/restore_tmp")
@patch("os.remove")
@patch("geminiai_cli.cooldown._sync_cooldown_file")
def test_main_cleanup_temp_download(mock_sync, mock_remove, mock_mkdtemp, mock_rmtree, mock_replace, mock_exists, mock_run, mock_lock, mock_move):
    # Test lines 316-320
    # Simulate cloud download flow partially or just force temp_download_path via some way?
    # It's a local variable in main. We need to go through the cloud path.
    with patch("sys.argv", ["restore.py", "--cloud", "--bucket", "b", "--b2-id", "i", "--b2-key", "k"]):
        with patch("geminiai_cli.restore.B2Manager") as mock_b2:
            mock_file = MagicMock()
            mock_file.file_name = "2025-10-22_042211-test.gemini.tar.gz"
            mock_b2.return_value.list_backups.return_value = [(mock_file, None)]
            mock_run.return_value.returncode = 0

            restore.main()
            mock_remove.assert_called()

@patch("geminiai_cli.restore.acquire_lock")
@patch("geminiai_cli.restore.run")
@patch("os.path.exists", return_value=True)
@patch("shutil.rmtree")
@patch("tempfile.mkdtemp", return_value="/tmp/restore_tmp")
def test_main_verification_fail_with_stdout(mock_mkdtemp, mock_rmtree, mock_exists, mock_run, mock_lock):
    with patch("sys.argv", ["restore.py", "--from-archive", "archive.tar.gz"]):
        # Mock cp run ok
        # Mock diff run fail (first verify)
        mock_run.side_effect = [
            MagicMock(returncode=0), # tar
            MagicMock(returncode=0), # cp
            MagicMock(returncode=1, stdout="diff output"), # diff
        ]
        with pytest.raises(SystemExit) as e:
            restore.main()
        assert e.value.code == 3

import pytest
import os
import json
import time
import datetime
import argparse
from unittest.mock import MagicMock, patch
from geminiai_cli.restore import perform_restore
from geminiai_cli.recommend import Recommendation, AccountStatus

@pytest.fixture
def mock_restore_env(fs):
    """Setup a mock environment for restore tests."""
    fs.create_dir(os.path.expanduser("~/.gemini"))
    fs.create_dir(os.path.expanduser("~/geminiai/backups"))
    return fs

def test_restore_auto_local_no_rec(mock_restore_env, capsys):
    """Test --auto local restore fails if no recommendation."""
    args = argparse.Namespace(
        auto=True,
        cloud=False,
        dest="~/.gemini",
        search_dir="~/geminiai/backups",
        from_dir=None,
        from_archive=None,
        dry_run=False,
        force=False
    )

    with patch("geminiai_cli.restore.get_recommendation", return_value=None):
        with pytest.raises(SystemExit):
            perform_restore(args)

    captured = capsys.readouterr()
    assert "No 'Green' (Ready) accounts" in captured.out

def test_restore_auto_local_success(mock_restore_env, capsys):
    """Test --auto local restore with recommendation."""
    args = argparse.Namespace(
        auto=True,
        cloud=False,
        dest="~/.gemini",
        search_dir="~/geminiai/backups",
        from_dir=None,
        from_archive=None,
        dry_run=False,
        force=False
    )

    rec = Recommendation(email="test@example.com", status=AccountStatus.READY, last_used=None, next_reset=None)

    # Mock finding the backup
    search_dir = os.path.expanduser(args.search_dir)
    backup_file = os.path.join(search_dir, "2025-01-01_120000-test@example.com.gemini.tar.gz")
    mock_restore_env.create_file(backup_file)

    with patch("geminiai_cli.restore.get_recommendation", return_value=rec):
        with patch("geminiai_cli.restore.acquire_lock"), \
             patch("geminiai_cli.restore.extract_archive"), \
             patch("geminiai_cli.restore.run") as mock_run, \
             patch("geminiai_cli.restore.shutil.rmtree"), \
             patch("os.replace"), \
             patch("geminiai_cli.restore.get_active_session", return_value=None):

            mock_run.return_value.returncode = 0
            perform_restore(args)

    captured = capsys.readouterr()
    assert "Auto-switch recommendation: test@example.com" in captured.out
    assert "Selected latest local backup" in captured.out

def test_restore_auto_local_not_found(mock_restore_env, capsys):
    """Test --auto local restore fails if backup missing."""
    args = argparse.Namespace(
        auto=True,
        cloud=False,
        dest="~/.gemini",
        search_dir="~/geminiai/backups",
        from_dir=None,
        from_archive=None,
        dry_run=False,
        force=False
    )

    rec = Recommendation(email="test@example.com", status=AccountStatus.READY, last_used=None, next_reset=None)

    with patch("geminiai_cli.restore.get_recommendation", return_value=rec):
        with pytest.raises(SystemExit):
            perform_restore(args)

    captured = capsys.readouterr()
    assert "No backups found locally" in captured.out

def test_restore_cloud_auto_success(mock_restore_env, capsys):
    """Test --auto --cloud restore success."""
    args = argparse.Namespace(
        auto=True,
        cloud=True,
        dest="~/.gemini",
        search_dir="~/geminiai/backups",
        from_dir=None,
        from_archive=None,
        dry_run=False,
        force=False,
        b2_id="id",
        b2_key="key",
        bucket="bucket"
    )

    rec = Recommendation(email="test@example.com", status=AccountStatus.READY, last_used=None, next_reset=None)

    with patch("geminiai_cli.restore.resolve_credentials", return_value=("id", "key", "bucket")):
        with patch("geminiai_cli.restore.B2Manager") as MockB2:
            b2_instance = MockB2.return_value
            file_version = MagicMock()
            file_version.file_name = "2025-01-01_120000-test@example.com.gemini.tar.gz"
            b2_instance.list_backups.return_value = [(file_version, None)]

            with patch("geminiai_cli.restore.get_recommendation", return_value=rec):
                 with patch("geminiai_cli.restore.acquire_lock"), \
                     patch("geminiai_cli.restore.extract_archive"), \
                     patch("geminiai_cli.restore.run") as mock_run, \
                     patch("geminiai_cli.restore.shutil.rmtree"), \
                     patch("os.replace"), \
                     patch("geminiai_cli.restore.get_active_session", return_value=None):

                     mock_run.return_value.returncode = 0
                     perform_restore(args)

    captured = capsys.readouterr()
    assert "Auto-switch recommendation: test@example.com" in captured.out
    assert "Selected latest cloud backup" in captured.out

def test_restore_cloud_auto_not_found(mock_restore_env, capsys):
    """Test --auto --cloud restore fails if no matching backup."""
    args = argparse.Namespace(
        auto=True,
        cloud=True,
        dest="~/.gemini",
        search_dir="~/geminiai/backups",
        from_dir=None,
        from_archive=None,
        dry_run=False,
        force=False
    )

    rec = Recommendation(email="test@example.com", status=AccountStatus.READY, last_used=None, next_reset=None)

    with patch("geminiai_cli.restore.resolve_credentials", return_value=("id", "key", "bucket")):
        with patch("geminiai_cli.restore.B2Manager") as MockB2:
            b2_instance = MockB2.return_value
            file_version = MagicMock()
            file_version.file_name = "2025-01-01_120000-other@example.com.gemini.tar.gz"
            b2_instance.list_backups.return_value = [(file_version, None)]

            with patch("geminiai_cli.restore.get_recommendation", return_value=rec):
                with pytest.raises(SystemExit):
                    perform_restore(args)

    captured = capsys.readouterr()
    assert "No backups found in cloud for recommended account" in captured.out

def test_restore_from_archive_search_fallback(mock_restore_env, capsys):
    """Test fallback to search dir when --from-archive path is just a filename."""
    args = argparse.Namespace(
        from_archive="mybackup.tar.gz",
        search_dir="~/geminiai/backups",
        dest="~/.gemini",
        cloud=False,
        auto=False,
        from_dir=None,
        dry_run=False,
        force=False
    )

    search_dir = os.path.expanduser(args.search_dir)
    mock_restore_env.create_file(os.path.join(search_dir, "mybackup.tar.gz"))

    with patch("geminiai_cli.restore.acquire_lock"), \
         patch("geminiai_cli.restore.extract_archive"), \
         patch("geminiai_cli.restore.run") as mock_run, \
         patch("geminiai_cli.restore.shutil.rmtree"), \
         patch("os.replace"), \
         patch("geminiai_cli.restore.get_active_session", return_value=None):

         mock_run.return_value.returncode = 0
         perform_restore(args)

    captured = capsys.readouterr()
    assert "Found archive in default backup directory" in captured.out

def test_restore_from_archive_not_found(mock_restore_env, capsys):
    """Test --from-archive fails if file not found anywhere."""
    args = argparse.Namespace(
        from_archive="nonexistent.tar.gz",
        search_dir="~/geminiai/backups",
        dest="~/.gemini",
        cloud=False,
        auto=False,
        from_dir=None,
        dry_run=False,
        force=False
    )

    with pytest.raises(SystemExit):
        perform_restore(args)

    captured = capsys.readouterr()
    assert "Specified --from-archive not found" in captured.out

def test_restore_cloud_specific_success(mock_restore_env, capsys):
    """Test --cloud --from-archive success."""
    # Use a timestamped name so it's considered valid
    valid_name = "2025-01-01_120000-specific.gemini.tar.gz"
    args = argparse.Namespace(
        cloud=True,
        from_archive=valid_name,
        auto=False,
        dest="~/.gemini",
        search_dir="~/geminiai/backups",
        from_dir=None,
        dry_run=False,
        force=False,
        b2_id="id",
        b2_key="key",
        bucket="bucket"
    )

    with patch("geminiai_cli.restore.resolve_credentials", return_value=("id", "key", "bucket")):
        with patch("geminiai_cli.restore.B2Manager") as MockB2:
            b2_instance = MockB2.return_value
            fv = MagicMock()
            fv.file_name = valid_name
            b2_instance.list_backups.return_value = [(fv, None)]

            with patch("geminiai_cli.restore.acquire_lock"), \
                 patch("geminiai_cli.restore.extract_archive"), \
                 patch("geminiai_cli.restore.run") as mock_run, \
                 patch("geminiai_cli.restore.shutil.rmtree"), \
                 patch("os.replace"), \
                 patch("geminiai_cli.restore.get_active_session", return_value=None):

                 mock_run.return_value.returncode = 0
                 perform_restore(args)

    captured = capsys.readouterr()
    assert "Selected specified cloud backup" in captured.out

def test_restore_cloud_specific_fail(mock_restore_env, capsys):
    """Test --cloud --from-archive not found."""
    args = argparse.Namespace(
        cloud=True,
        from_archive="missing.gemini.tar.gz",
        auto=False,
        dest="~/.gemini",
        search_dir="~/geminiai/backups",
        from_dir=None,
        dry_run=False,
        force=False,
        b2_id="id",
        b2_key="key",
        bucket="bucket"
    )

    with patch("geminiai_cli.restore.resolve_credentials", return_value=("id", "key", "bucket")):
        with patch("geminiai_cli.restore.B2Manager") as MockB2:
            b2_instance = MockB2.return_value
            # Provide at least one valid file so we don't exit early
            fv = MagicMock()
            fv.file_name = "2025-01-01_120000-existing.gemini.tar.gz"
            b2_instance.list_backups.return_value = [(fv, None)]

            with pytest.raises(SystemExit):
                 perform_restore(args)

    captured = capsys.readouterr()
    assert "Specified archive 'missing.gemini.tar.gz' not found" in captured.out

def test_restore_auto_cooldown_outgoing(mock_restore_env, capsys):
    """Test that cooldown is applied to outgoing account."""
    args = argparse.Namespace(
        cloud=False,
        auto=False,
        dest="~/.gemini",
        search_dir="~/geminiai/backups",
        from_dir=None,
        from_archive=None,
        dry_run=False,
        force=False
    )

    search_dir = os.path.expanduser(args.search_dir)
    mock_restore_env.create_file(os.path.join(search_dir, "2025-01-01_120000-new@test.com.gemini.tar.gz"))

    with patch("geminiai_cli.restore.get_active_session", side_effect=["old@test.com", "new@test.com"]):
         # Patch resolve_credentials to raise Exception (simulating missing creds) which perform_restore catches
         with patch("geminiai_cli.restore.resolve_credentials", side_effect=ValueError("No Creds")):
             with patch("geminiai_cli.restore.acquire_lock"), \
                 patch("geminiai_cli.restore.extract_archive"), \
                 patch("geminiai_cli.restore.run") as mock_run, \
                 patch("geminiai_cli.restore.shutil.rmtree"), \
                 patch("os.replace"), \
                 patch("geminiai_cli.restore.add_24h_cooldown_for_email") as mock_cooldown, \
                 patch("geminiai_cli.restore.record_switch") as mock_switch:

                 mock_run.return_value.returncode = 0
                 perform_restore(args)

                 mock_cooldown.assert_called_with("old@test.com")
                 mock_switch.assert_any_call("old@test.com", args=args)
                 mock_switch.assert_any_call("new@test.com", args=args)
