# tests/test_settings.py

import pytest
from unittest.mock import patch, mock_open
import json
import os
from geminiai_cli.settings import load_settings, save_settings, set_setting, get_setting, remove_setting, list_settings

CONFIG_CONTENT = '{"key1": "value1", "key2": "value2"}'

@patch("os.path.exists")
def test_load_settings_exists(mock_exists):
    mock_exists.return_value = True
    with patch("builtins.open", mock_open(read_data=CONFIG_CONTENT)):
        settings = load_settings()
        assert settings["key1"] == "value1"

@patch("os.path.exists")
def test_load_settings_not_exists(mock_exists):
    mock_exists.return_value = False
    assert load_settings() == {}

@patch("os.path.exists")
def test_load_settings_malformed(mock_exists):
    mock_exists.return_value = True
    with patch("builtins.open", mock_open(read_data='{invalid}')):
        # json.load usually raises JSONDecodeError, which load_settings catches
        with patch("json.load", side_effect=json.JSONDecodeError("msg", "doc", 0)):
             assert load_settings() == {}

@patch("geminiai_cli.settings.save_settings")
@patch("geminiai_cli.settings.load_settings")
def test_set_setting(mock_load, mock_save):
    mock_load.return_value = {}
    set_setting("new_key", "new_val")
    mock_save.assert_called_with({"new_key": "new_val"})

@patch("geminiai_cli.settings.load_settings")
def test_get_setting(mock_load):
    mock_load.return_value = {"key": "val"}
    assert get_setting("key") == "val"
    assert get_setting("missing", "default") == "default"

@patch("geminiai_cli.settings.save_settings")
@patch("geminiai_cli.settings.load_settings")
def test_remove_setting(mock_load, mock_save):
    mock_load.return_value = {"key": "val"}
    assert remove_setting("key") is True
    mock_save.assert_called_with({})

@patch("geminiai_cli.settings.save_settings")
@patch("geminiai_cli.settings.load_settings")
def test_remove_setting_not_found(mock_load, mock_save):
    mock_load.return_value = {}
    assert remove_setting("key") is False
    mock_save.assert_not_called()

@patch("geminiai_cli.settings.load_settings")
def test_list_settings(mock_load):
    mock_load.return_value = {"a": 1}
    assert list_settings() == {"a": 1}

@patch("os.makedirs")
def test_save_settings(mock_makedirs):
    with patch("builtins.open", mock_open()) as mock_file:
        save_settings({"a": 1})
        mock_file().write.assert_called()
