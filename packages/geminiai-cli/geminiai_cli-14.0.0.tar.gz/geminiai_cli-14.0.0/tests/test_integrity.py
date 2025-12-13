# tests/test_integrity.py

import pytest
from unittest.mock import patch, MagicMock
import os
import time
import sys
import subprocess
from geminiai_cli import integrity

def test_run():
    with patch("subprocess.run") as mock_run:
        integrity.run("ls")
        mock_run.assert_called_with("ls", shell=True, check=True)

def test_run_capture():
    with patch("subprocess.run") as mock_run:
        integrity.run("ls", capture=True)
        mock_run.assert_called_with("ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def test_parse_timestamp_from_name():
    ts = integrity.parse_timestamp_from_name("2025-10-22_042211-test@test.gemini")
    assert ts is not None
    assert ts.tm_year == 2025

    assert integrity.parse_timestamp_from_name("invalid") is None

@patch("os.listdir")
@patch("os.path.isdir", return_value=True)
def test_find_latest_backup(mock_isdir, mock_listdir):
    mock_listdir.return_value = [
        "2025-10-23_042211-test.gemini",
        "2025-10-22_042211-test.gemini"
    ]
    latest = integrity.find_latest_backup("/tmp")
    assert "2025-10-23" in latest

@patch("os.listdir")
def test_find_latest_backup_none(mock_listdir):
    mock_listdir.return_value = []
    assert integrity.find_latest_backup("/tmp") is None

@patch("os.path.exists", return_value=False)
def test_main_src_not_exists(mock_exists):
    with patch("sys.argv", ["integrity.py"]):
        with pytest.raises(SystemExit) as e:
            integrity.main()
        assert e.value.code == 1

@patch("os.path.exists", return_value=True)
@patch("geminiai_cli.integrity.find_latest_backup", return_value=None)
def test_main_no_backup(mock_find, mock_exists):
    with patch("sys.argv", ["integrity.py"]):
        with pytest.raises(SystemExit) as e:
            integrity.main()
        assert e.value.code == 1

@patch("os.path.exists", return_value=True)
@patch("geminiai_cli.integrity.find_latest_backup", return_value="/tmp/backup")
@patch("geminiai_cli.integrity.run")
def test_main_diff_ok(mock_run, mock_find, mock_exists):
    with patch("sys.argv", ["integrity.py"]):
        mock_run.return_value.returncode = 0
        integrity.main()

@patch("os.path.exists", return_value=True)
@patch("geminiai_cli.integrity.find_latest_backup", return_value="/tmp/backup")
@patch("geminiai_cli.integrity.run")
def test_main_diff_fail(mock_run, mock_find, mock_exists):
    with patch("sys.argv", ["integrity.py"]):
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = "diff"
        mock_run.return_value.stderr = "err"
        integrity.main()

@patch("os.listdir")
@patch("os.path.isdir", return_value=False)
def test_find_latest_backup_not_dir(mock_isdir, mock_listdir):
    mock_listdir.return_value = ["2025-10-23_042211-test.gemini"]
    assert integrity.find_latest_backup("/tmp") is None

@patch("os.listdir")
@patch("os.path.isdir", return_value=True)
def test_find_latest_backup_bad_name(mock_isdir, mock_listdir):
    mock_listdir.return_value = ["invalid-name"]
    assert integrity.find_latest_backup("/tmp") is None

@patch("os.listdir", side_effect=FileNotFoundError)
def test_find_latest_backup_not_found(mock_listdir):
    assert integrity.find_latest_backup("/tmp") is None

@patch("os.path.exists", return_value=True)
@patch("geminiai_cli.integrity.find_latest_backup", return_value="/tmp/backup")
@patch("geminiai_cli.integrity.run")
@patch("builtins.print")
def test_main_diff_fail_stderr(mock_print, mock_run, mock_find, mock_exists):
    with patch("sys.argv", ["integrity.py"]):
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = "error"
        integrity.main()
        # Should print error
        assert any("error" in str(args) for args in mock_print.call_args_list)

@patch("time.strptime", side_effect=ValueError)
def test_parse_timestamp_exception(mock_strptime):
    # This string must match TIMESTAMPED_DIR_REGEX for us to reach strptime
    # Assuming regex is like YYYY-MM-DD_HHMMSS-...
    assert integrity.parse_timestamp_from_name("2025-10-22_042211-test") is None

@patch("os.path.exists", return_value=True)
@patch("geminiai_cli.integrity.find_latest_backup", return_value="/tmp/backup")
@patch("geminiai_cli.integrity.run")
@patch("builtins.print")
def test_main_diff_fail_no_stderr(mock_print, mock_run, mock_find, mock_exists):
    with patch("sys.argv", ["integrity.py"]):
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = "out"
        mock_run.return_value.stderr = ""
        integrity.main()
        # Should not print stderr (so we don't search for it)
        # We can assert it printed stdout
        assert any("out" in str(args) for args in mock_print.call_args_list)
