# tests/test_utils.py

import pytest
from unittest.mock import patch, mock_open
import subprocess
from geminiai_cli.utils import run, read_file, run_capture
from geminiai_cli.reset_helpers import run_cmd_safe

@patch("subprocess.check_output")
def test_run_capture(mock_check_output):
    mock_check_output.return_value = b"hello"
    assert run_capture("echo hello") == "hello"

@patch("subprocess.check_output")
def test_run_capture_exception(mock_check_output):
    mock_check_output.side_effect = subprocess.CalledProcessError(1, "cmd")
    assert run_capture("echo hello") is None

@patch("subprocess.run")
def test_run_cmd_safe(mock_subprocess_run):
    mock_subprocess_run.return_value.returncode = 0
    mock_subprocess_run.return_value.stdout = "hello"
    mock_subprocess_run.return_value.stderr = ""
    rc, stdout, stderr = run_cmd_safe("echo hello", capture=True)
    assert rc == 0
    assert stdout == "hello"
    assert stderr == ""

@patch("subprocess.run")
def test_run_cmd_safe_exception(mock_subprocess_run):
    # Test CalledProcessError
    called_process_error = subprocess.CalledProcessError(1, "cmd")
    called_process_error.stdout = b"error_out"
    called_process_error.stderr = b"error_err"

    # Test TimeoutExpired
    timeout_expired = subprocess.TimeoutExpired("cmd", 10)
    timeout_expired.stdout = b"timeout_out"
    timeout_expired.stderr = b"timeout_err"

    mock_subprocess_run.side_effect = [
        called_process_error,
        timeout_expired
    ]
    
    rc, stdout, stderr = run_cmd_safe("echo hello", capture=True)
    assert rc == 1
    assert str(called_process_error) in stderr
                                                            
    rc, stdout, stderr = run_cmd_safe("echo hello", capture=True, timeout=1)
    assert rc == 124
    assert "timeout_out" in stdout or "timeout_err" in stderr

@patch("subprocess.run")
def test_run(mock_run):
    run("echo hello")
    mock_run.assert_called_with("echo hello", shell=True, check=True)

@patch("subprocess.run")
@patch("geminiai_cli.utils.sys.exit")
@patch("geminiai_cli.utils.cprint")
def test_run_exception(mock_cprint, mock_exit, mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, "cmd")
    run("echo hello")
    mock_exit.assert_called_with(1)
    mock_cprint.assert_called()

@patch("os.path.exists", return_value=False)
def test_read_file_not_exists(mock_exists):
    assert read_file("test.txt") == ""

@patch("os.path.exists", return_value=True)
@patch("builtins.open", new_callable=mock_open, read_data="hello")
def test_read_file_exists(mock_exists, mock_file):
    assert read_file("test.txt") == "hello"

@patch("os.path.exists", return_value=True)
@patch("builtins.open", side_effect=Exception)
def test_read_file_exception(mock_exists, mock_file):
    assert read_file("test.txt") == ""
