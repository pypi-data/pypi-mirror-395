
import pytest
import sys
from unittest.mock import MagicMock, mock_open, patch
from geminiai_cli.project_config import load_project_config, normalize_config_keys

# Fixture to mock sys.version_info to force tomllib import logic
# However, we can't easily unimport modules.
# Instead, we will test the logic assuming tomllib is available since we are on 3.12.
# We will focus on testing the file loading logic.

@pytest.fixture
def mock_fs_config(mocker):
    return mocker.patch("os.path.exists")

def test_normalize_config_keys():
    config = {
        "backup-dir": "/tmp",
        "verbose-mode": True,
        "simple_key": 1
    }
    normalized = normalize_config_keys(config)
    assert normalized["backup_dir"] == "/tmp"
    assert normalized["verbose_mode"] is True
    assert normalized["simple_key"] == 1

def test_load_project_config_no_files(mock_fs_config):
    mock_fs_config.return_value = False
    assert load_project_config() == {}

def test_load_project_config_geminiai_toml_tool_section(mock_fs_config, mocker):
    mock_fs_config.side_effect = lambda p: p == "geminiai.toml"

    toml_content = b"""
    [tool.geminiai]
    backup-dir = "val1"
    """

    # We need to mock tomllib.load. Since python 3.12 has tomllib...
    # We can mock the open call and let real tomllib parse, or mock tomllib.

    with patch("builtins.open", mock_open(read_data=toml_content)):
         # We rely on real tomllib parsing the bytes provided in read_data
        config = load_project_config()

    assert config == {"backup-dir": "val1"}

def test_load_project_config_geminiai_toml_root(mock_fs_config, mocker):
    mock_fs_config.side_effect = lambda p: p == "geminiai.toml"

    toml_content = b"""
    backup-dir = "val2"
    """

    with patch("builtins.open", mock_open(read_data=toml_content)):
        config = load_project_config()

    assert config == {"backup-dir": "val2"}

def test_load_project_config_geminiai_toml_error(mock_fs_config, mocker):
    mock_fs_config.side_effect = lambda p: p == "geminiai.toml"

    # Invalid TOML
    toml_content = b"invalid toml ["

    with patch("builtins.open", mock_open(read_data=toml_content)):
        config = load_project_config()

    assert config == {}

def test_load_project_config_pyproject_toml(mock_fs_config, mocker):
    mock_fs_config.side_effect = lambda p: p == "pyproject.toml"

    toml_content = b"""
    [tool.geminiai]
    option = "val3"
    """

    with patch("builtins.open", mock_open(read_data=toml_content)):
        config = load_project_config()

    assert config == {"option": "val3"}

def test_load_project_config_pyproject_toml_no_section(mock_fs_config, mocker):
    mock_fs_config.side_effect = lambda p: p == "pyproject.toml"

    toml_content = b"""
    [tool.other]
    option = "val4"
    """

    with patch("builtins.open", mock_open(read_data=toml_content)):
        config = load_project_config()

    assert config == {}

def test_load_project_config_pyproject_toml_error(mock_fs_config, mocker):
    mock_fs_config.side_effect = lambda p: p == "pyproject.toml"

    with patch("builtins.open", mock_open(read_data=b"[")):
        config = load_project_config()

    assert config == {}

def test_load_project_config_geminiai_toml_open_fail(mock_fs_config, mocker):
    mock_fs_config.side_effect = lambda p: p == "geminiai.toml"

    with patch("builtins.open", side_effect=OSError("Read error")):
        config = load_project_config()

    assert config == {}

def test_tomllib_import_fallback(mocker):
    # This test is tricky because the module is already loaded.
    # We can try to reload the module with modified sys.modules or sys.version_info
    # BUT, mocking sys.version_info is risky.
    # We can mock the module attribute.

    # We will skip testing the import logic branches (lines 4-11) specifically
    # as we are running on 3.12 and coverage might miss the < 3.11 branch.
    # However, if we really want to cover the `if not tomllib: return {}` line...

    with patch("geminiai_cli.project_config.tomllib", None):
        assert load_project_config() == {}
