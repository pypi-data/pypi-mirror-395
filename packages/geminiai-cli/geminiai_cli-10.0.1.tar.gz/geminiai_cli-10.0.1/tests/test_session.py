# tests/test_session.py

import pytest
from unittest.mock import patch, mock_open
import os
import json
from geminiai_cli import session

# Helper for json.load
def mock_json_load(data):
    return patch("json.load", return_value=data)

@patch("os.path.exists")
def test_get_active_session_exists(mock_exists):
    mock_exists.return_value = True
    with patch("builtins.open", mock_open(read_data='{"active": "test@example.com"}')):
        assert session.get_active_session() == "test@example.com"

@patch("os.path.exists")
def test_get_active_session_not_exists(mock_exists):
    mock_exists.return_value = False
    assert session.get_active_session() is None

@patch("os.path.exists")
def test_get_active_session_malformed(mock_exists):
    mock_exists.return_value = True
    with patch("builtins.open", mock_open(read_data='{invalid_json}')):
        # json.load will raise JSONDecodeError
        with patch("json.load", side_effect=json.JSONDecodeError("msg", "doc", 0)):
             assert session.get_active_session() is None

@patch("geminiai_cli.session.get_active_session")
@patch("geminiai_cli.session.cprint")
def test_do_session_active(mock_cprint, mock_get_session):
    mock_get_session.return_value = "user@example.com"
    session.do_session()
    # Check that success message was printed
    # cprint arguments: color, text
    # call_args_list[1] should be the success message
    assert mock_cprint.call_count == 2
    assert "Active Session" in mock_cprint.call_args_list[1][0][1]

@patch("geminiai_cli.session.get_active_session")
@patch("geminiai_cli.session.cprint")
def test_do_session_inactive(mock_cprint, mock_get_session):
    mock_get_session.return_value = None
    session.do_session()
    assert mock_cprint.call_count == 3 # Heading, Error, Hint
    assert "No active session" in mock_cprint.call_args_list[1][0][1]

# Patch the symbol in CLI module where it is imported!
@patch("geminiai_cli.cli.do_session")
def test_main_session_arg(mock_do_session):
    from geminiai_cli.cli import main
    with patch("sys.argv", ["geminiai", "--session"]):
        main()
        mock_do_session.assert_called_once()
