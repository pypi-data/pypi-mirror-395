# tests/test_logout.py

import pytest
from unittest.mock import patch, MagicMock
from geminiai_cli.logout import do_logout

@patch("geminiai_cli.logout.run")
@patch("geminiai_cli.logout.os.path.exists")
@patch("geminiai_cli.logout.cprint")
@patch("subprocess.run")
def test_do_logout_exists(mock_sub_run, mock_cprint, mock_exists, mock_run):
    mock_exists.return_value = True
    do_logout()

    mock_run.assert_called()
    assert any("Directory removed" in str(c) for c in mock_cprint.call_args_list)

@patch("geminiai_cli.logout.run")
@patch("geminiai_cli.logout.os.path.exists")
@patch("geminiai_cli.logout.cprint")
@patch("subprocess.run")
def test_do_logout_not_exists(mock_sub_run, mock_cprint, mock_exists, mock_run):
    mock_exists.return_value = False
    do_logout()

    # run called only for confirmation ls
    assert mock_run.call_count == 1
    assert any("Already logged out" in str(c) for c in mock_cprint.call_args_list)
