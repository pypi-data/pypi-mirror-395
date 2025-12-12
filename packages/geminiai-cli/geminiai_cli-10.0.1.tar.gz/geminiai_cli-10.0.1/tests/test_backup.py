# tests/test_backup.py

import pytest
from unittest.mock import patch, mock_open, MagicMock
import os
import subprocess
import json
import shutil
from geminiai_cli import backup

@patch("geminiai_cli.backup.fcntl")
def test_acquire_lock_success(mock_fcntl):
    with patch("builtins.open", mock_open()):
        fd = backup.acquire_lock()
        assert fd is not None
        mock_fcntl.flock.assert_called()

@patch("geminiai_cli.backup.fcntl")
def test_acquire_lock_fail(mock_fcntl):
    mock_fcntl.flock.side_effect = BlockingIOError
    with patch("builtins.open", mock_open()):
        with pytest.raises(SystemExit) as e:
            backup.acquire_lock()
        assert e.value.code == 2

def test_run():
    with patch("subprocess.run") as mock_run:
        backup.run("ls")
        mock_run.assert_called_with("ls", shell=True, check=True)

def test_run_capture():
    with patch("subprocess.run") as mock_run:
        backup.run("ls", capture=True)
        mock_run.assert_called_with("ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def test_read_active_email_no_file():
    with patch("os.path.exists", return_value=False):
        assert backup.read_active_email("/tmp") is None

def test_read_active_email_valid():
    data = json.dumps({"active": "user@example.com"})
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=data)):
            assert backup.read_active_email("/tmp") == "user@example.com"

def test_read_active_email_invalid_json():
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data="{invalid")):
            assert backup.read_active_email("/tmp") is None

def test_read_active_email_no_active_field():
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data="{}")):
            assert backup.read_active_email("/tmp") is None

def test_ensure_dir():
    with patch("os.makedirs") as mock_makedirs:
        backup.ensure_dir("/tmp/dir")
        mock_makedirs.assert_called_with("/tmp/dir", exist_ok=True)

def test_make_timestamp():
    assert len(backup.make_timestamp()) > 0

def test_atomic_symlink():
    with patch("os.path.lexists", side_effect=[True, False]):
        with patch("os.unlink") as mock_unlink:
            with patch("os.symlink") as mock_symlink:
                with patch("os.replace") as mock_replace:
                    backup.atomic_symlink("target", "link")
                    mock_unlink.assert_called()
                    mock_symlink.assert_called_with("target", mock_replace.call_args[0][0])
                    mock_replace.assert_called()

def test_atomic_symlink_exceptions():
    with patch("os.path.lexists", return_value=True):
         with patch("os.unlink", side_effect=Exception):
            with patch("os.symlink"):
                with patch("os.replace"):
                     # Should not crash
                     backup.atomic_symlink("target", "link")

@patch("geminiai_cli.backup.acquire_lock")
@patch("geminiai_cli.backup.read_active_email", return_value="user@example.com")
@patch("geminiai_cli.backup.run")
@patch("os.path.exists", return_value=True)
@patch("os.makedirs")
@patch("os.replace")
@patch("shutil.rmtree")
def test_main_success(mock_rmtree, mock_replace, mock_makedirs, mock_exists, mock_run, mock_email, mock_lock):
    with patch("sys.argv", ["backup.py"]):
        # Mock diff to succeed
        mock_run.return_value.returncode = 0
        backup.main()
        assert mock_run.call_count >= 2 # tar, cp, diff

@patch("geminiai_cli.backup.acquire_lock")
@patch("geminiai_cli.backup.read_active_email", return_value="user@example.com")
@patch("geminiai_cli.backup.run")
@patch("os.path.exists", return_value=True)
@patch("os.makedirs")
@patch("shutil.rmtree")
def test_main_diff_fail(mock_rmtree, mock_makedirs, mock_exists, mock_run, mock_email, mock_lock):
    with patch("sys.argv", ["backup.py"]):
        # Mock diff to fail
        mock_run.return_value.returncode = 1
        with pytest.raises(SystemExit) as e:
            backup.main()
        assert e.value.code == 3

@patch("geminiai_cli.backup.acquire_lock")
@patch("geminiai_cli.backup.read_active_email", return_value="user@example.com")
@patch("os.path.exists", return_value=False)
def test_main_src_not_exist(mock_exists, mock_email, mock_lock):
    with patch("sys.argv", ["backup.py"]):
        with pytest.raises(SystemExit) as e:
            backup.main()
        assert e.value.code == 1

@patch("geminiai_cli.backup.acquire_lock")
@patch("geminiai_cli.backup.read_active_email", return_value="user@example.com")
@patch("geminiai_cli.backup.run")
@patch("os.path.exists", return_value=True)
def test_main_dry_run(mock_exists, mock_run, mock_email, mock_lock):
    with patch("sys.argv", ["backup.py", "--dry-run"]):
        backup.main()
        mock_run.assert_not_called()

@patch("geminiai_cli.backup.acquire_lock")
@patch("geminiai_cli.backup.read_active_email", return_value="user@example.com")
@patch("geminiai_cli.backup.run")
@patch("os.path.exists", return_value=True)
@patch("os.makedirs")
@patch("os.replace")
@patch("geminiai_cli.backup.B2Manager")
@patch("shutil.rmtree")
def test_main_cloud(mock_rmtree, mock_b2, mock_replace, mock_makedirs, mock_exists, mock_run, mock_email, mock_lock):
    with patch("sys.argv", ["backup.py", "--cloud", "--bucket", "b", "--b2-id", "i", "--b2-key", "k"]):
        mock_run.return_value.returncode = 0
        backup.main()
        mock_b2.assert_called()
        mock_b2.return_value.upload.assert_called()

@patch("geminiai_cli.backup.acquire_lock")
@patch("geminiai_cli.backup.read_active_email", return_value="user@example.com")
@patch("geminiai_cli.backup.run")
@patch("os.path.exists", return_value=True)
@patch("geminiai_cli.backup.B2Manager")
@patch("shutil.rmtree")
@patch("os.makedirs")
@patch("os.replace")
@patch("geminiai_cli.credentials.get_setting", return_value=None)
@patch.dict(os.environ, {}, clear=True)
def test_main_cloud_missing_creds(mock_get_setting, mock_replace, mock_makedirs, mock_rmtree, mock_b2, mock_exists, mock_run, mock_email, mock_lock):
    with patch("sys.argv", ["backup.py", "--cloud"]): # Missing bucket/id/key
        mock_run.return_value.returncode = 0
        # resolve_credentials calls sys.exit(1) if no creds found
        with pytest.raises(SystemExit) as e:
            backup.main()
        assert e.value.code == 1
        mock_b2.assert_not_called()

# NEW TESTS

@patch("geminiai_cli.backup.acquire_lock")
@patch("geminiai_cli.backup.read_active_email", return_value=None)
@patch("geminiai_cli.backup.run")
@patch("os.path.exists", return_value=True)
@patch("os.makedirs")
@patch("os.replace")
@patch("shutil.rmtree")
def test_main_no_active_email(mock_rmtree, mock_replace, mock_makedirs, mock_exists, mock_run, mock_email, mock_lock):
    # Test lines 123-125: fallback name
    # Test line 191: skipping latest symlink
    with patch("sys.argv", ["backup.py"]):
        mock_run.return_value.returncode = 0
        backup.main()
        # Should not crash
        assert mock_run.call_count >= 2

@patch("geminiai_cli.backup.acquire_lock")
@patch("geminiai_cli.backup.read_active_email", return_value="user@example.com")
@patch("geminiai_cli.backup.run")
@patch("os.path.exists", return_value=True)
@patch("os.makedirs")
@patch("os.replace")
@patch("shutil.rmtree")
@patch("geminiai_cli.backup.TIMESTAMPED_DIR_REGEX")
def test_main_regex_fail(mock_regex, mock_rmtree, mock_replace, mock_makedirs, mock_exists, mock_run, mock_email, mock_lock):
    # Test lines 127-129
    mock_regex.match.return_value = False
    with patch("sys.argv", ["backup.py"]):
        with pytest.raises(SystemExit) as e:
            backup.main()
        assert e.value.code == 1

@patch("geminiai_cli.backup.acquire_lock")
@patch("geminiai_cli.backup.read_active_email", return_value="user@example.com")
@patch("geminiai_cli.backup.run")
@patch("os.path.exists", return_value=True)
@patch("os.makedirs")
@patch("os.replace")
@patch("shutil.rmtree")
@patch("geminiai_cli.backup.atomic_symlink", side_effect=Exception("Symlink error"))
def test_main_symlink_fail(mock_symlink, mock_rmtree, mock_replace, mock_makedirs, mock_exists, mock_run, mock_email, mock_lock):
    # Test lines 188-189
    with patch("sys.argv", ["backup.py"]):
        mock_run.return_value.returncode = 0
        backup.main()
        # Should print exception but not crash
        mock_symlink.assert_called()

@patch("geminiai_cli.backup.acquire_lock")
@patch("geminiai_cli.backup.read_active_email", return_value="user@example.com")
@patch("geminiai_cli.backup.run")
@patch("os.path.exists")
@patch("os.makedirs")
@patch("os.replace")
@patch("shutil.rmtree")
def test_main_tmp_exists(mock_rmtree, mock_replace, mock_makedirs, mock_exists, mock_run, mock_email, mock_lock):
    # Test lines 151-152: if os.path.exists(tmp_dest): shutil.rmtree(tmp_dest)

    # Smart side effect to handle gettext calls too
    def exists_side_effect(path):
        if path == "/home/jules/.gemini": # src
            return True
        if ".tmp-" in str(path): # tmp_dest
            return True
        return True # Default True for others (like locales)

    mock_exists.side_effect = exists_side_effect
    mock_run.return_value.returncode = 0

    with patch("sys.argv", ["backup.py"]):
        backup.main()
        mock_rmtree.assert_called()

@patch("geminiai_cli.backup.acquire_lock")
@patch("geminiai_cli.backup.read_active_email", return_value="user@example.com")
@patch("geminiai_cli.backup.run")
@patch("os.path.exists")
@patch("os.makedirs")
@patch("os.replace")
@patch("shutil.rmtree")
def test_main_tmp_not_exists(mock_rmtree, mock_replace, mock_makedirs, mock_exists, mock_run, mock_email, mock_lock):
    # Test lines 151-152: if os.path.exists(tmp_dest): False branch

    def exists_side_effect(path):
        if path == "/home/jules/.gemini": # src
            return True
        if ".tmp-" in str(path): # tmp_dest
            return False
        return True # Default True

    mock_exists.side_effect = exists_side_effect
    mock_run.return_value.returncode = 0

    with patch("sys.argv", ["backup.py"]):
        backup.main()
        mock_rmtree.assert_not_called()

@patch("geminiai_cli.backup.acquire_lock")
def test_main_lock_exception(mock_lock):
    # Test line 216-217: exception in finally block when closing lock
    mock_fd = MagicMock()
    mock_lock.return_value = mock_fd

    # Actually, let's just test main running successfully, but flock raises Exception on close
    with patch("geminiai_cli.backup.read_active_email", return_value="user@example.com"):
        with patch("geminiai_cli.backup.run") as mock_run:
             mock_run.return_value.returncode = 0
             with patch("os.path.exists", return_value=True):
                 with patch("os.makedirs"):
                     with patch("os.replace"):
                         with patch("shutil.rmtree"):
                             with patch("sys.argv", ["backup.py"]):
                                 # Mock flock to raise exception when called with UNLOCK (which happens in finally)
                                 # acquire_lock calls flock with LOCK_EX.
                                 # finally calls flock with LOCK_UN.

                                 # mock_lock returns a file descriptor.
                                 # backup.py imports fcntl.
                                 with patch("geminiai_cli.backup.fcntl.flock") as mock_flock:
                                     # First call success, second call raise
                                     mock_flock.side_effect = [None, Exception("Unlock fail")]
                                     backup.main()
                                     # Should swallow exception

@patch("geminiai_cli.backup.acquire_lock")
@patch("geminiai_cli.backup.read_active_email", return_value="user@example.com")
@patch("geminiai_cli.backup.run")
@patch("os.path.exists", return_value=True)
@patch("os.makedirs")
@patch("shutil.rmtree")
def test_main_diff_fail_no_stdout(mock_rmtree, mock_makedirs, mock_exists, mock_run, mock_email, mock_lock):
    with patch("sys.argv", ["backup.py"]):
        # Mock diff to fail
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = "" # Coverage for "if diff_proc.stdout:"
        with pytest.raises(SystemExit) as e:
            backup.main()
        assert e.value.code == 3
