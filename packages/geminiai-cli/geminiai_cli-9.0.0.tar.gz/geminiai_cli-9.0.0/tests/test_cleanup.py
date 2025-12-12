
import pytest
import os
from unittest.mock import MagicMock, patch
from pathlib import Path
from geminiai_cli.chat import cleanup_chat_history

@pytest.fixture
def mock_fs(mocker):
    return mocker.patch("os.path.exists"), mocker.patch("os.listdir"), mocker.patch("os.unlink"), mocker.patch("shutil.rmtree"), mocker.patch("os.path.isfile"), mocker.patch("os.path.isdir"), mocker.patch("os.path.islink")

@pytest.fixture
def mock_args():
    args = MagicMock()
    args.force = False
    args.dry_run = False
    return args

def test_do_cleanup_dir_not_exists(mock_args, capsys, mocker):
    mocker.patch("os.path.exists", return_value=False)

    cleanup_chat_history(mock_args.dry_run, mock_args.force, Path("/mock/home"))

    captured = capsys.readouterr()
    assert "Nothing to clean. Directory not found" in captured.out

def test_do_cleanup_list_error(mock_args, capsys, mocker):
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("os.listdir", side_effect=Exception("Permission denied"))

    cleanup_chat_history(mock_args.dry_run, mock_args.force, Path("/mock/home"))

    captured = capsys.readouterr()
    assert "Could not list directory" in captured.out

def test_do_cleanup_nothing_to_remove(mock_args, capsys, mocker):
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("os.listdir", return_value=["bin"]) # Only preserved item

    cleanup_chat_history(mock_args.dry_run, mock_args.force, Path("/mock/home"))

    captured = capsys.readouterr()
    assert "Directory is already clean" in captured.out

def test_do_cleanup_cancelled(mock_args, capsys, mocker):
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("os.listdir", return_value=["file1", "bin"])
    mocker.patch("builtins.input", return_value="n")

    cleanup_chat_history(mock_args.dry_run, mock_args.force, Path("/mock/home"))

    captured = capsys.readouterr()
    assert "Cleanup cancelled" in captured.out

def test_do_cleanup_force_success(mock_args, capsys, mocker):
    mock_args.force = True
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("os.listdir", return_value=["file1", "dir1", "bin"])

    # file1 is a file, dir1 is a directory
    def isfile_side_effect(path):
        return path.endswith("file1")

    def isdir_side_effect(path):
        return path.endswith("dir1")

    mocker.patch("os.path.isfile", side_effect=isfile_side_effect)
    mocker.patch("os.path.islink", return_value=False)
    mocker.patch("os.path.isdir", side_effect=isdir_side_effect)

    mock_unlink = mocker.patch("os.unlink")
    mock_rmtree = mocker.patch("shutil.rmtree")

    cleanup_chat_history(mock_args.dry_run, mock_args.force, Path("/mock/home"))

    assert mock_unlink.call_count == 1
    assert mock_rmtree.call_count == 1

    captured = capsys.readouterr()
    assert "Cleanup finished. Removed 2 items" in captured.out

def test_do_cleanup_dry_run(mock_args, capsys, mocker):
    mock_args.dry_run = True
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("os.listdir", return_value=["file1", "dir1", "bin"])

    mock_unlink = mocker.patch("os.unlink")
    mock_rmtree = mocker.patch("shutil.rmtree")

    cleanup_chat_history(mock_args.dry_run, mock_args.force, Path("/mock/home"))

    mock_unlink.assert_not_called()
    mock_rmtree.assert_not_called()

    captured = capsys.readouterr()
    assert "Would delete: file1" in captured.out
    assert "Would delete: dir1" in captured.out
    assert "Cleanup dry run finished. Would remove 2 items" in captured.out

def test_do_cleanup_interactive_yes(mock_args, capsys, mocker):
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("os.listdir", return_value=["file1"])
    mocker.patch("builtins.input", return_value="y")
    mocker.patch("os.path.isfile", return_value=True)
    mock_unlink = mocker.patch("os.unlink")

    cleanup_chat_history(mock_args.dry_run, mock_args.force, Path("/mock/home"))

    mock_unlink.assert_called_once()
    captured = capsys.readouterr()
    assert "Cleaning up..." in captured.out

def test_do_cleanup_delete_error(mock_args, capsys, mocker):
    mock_args.force = True
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("os.listdir", return_value=["file1"])
    mocker.patch("os.path.isfile", return_value=True)
    mocker.patch("os.unlink", side_effect=Exception("Disk error"))

    cleanup_chat_history(mock_args.dry_run, mock_args.force, Path("/mock/home"))

    captured = capsys.readouterr()
    assert "Failed to delete file1" in captured.out
