import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock

from geminiai_cli.chat import (
    backup_chat_history,
    restore_chat_history,
    cleanup_chat_history,
    resume_chat,
)

def test_backup_and_restore_chat_history():
    with tempfile.TemporaryDirectory() as tmpdir:
        home_dir = Path(tmpdir)
        gemini_home_dir = home_dir / ".gemini"
        gemini_tmp_dir = gemini_home_dir / "tmp"
        gemini_tmp_dir.mkdir(parents=True)
        backup_path = home_dir / "chat_backups"

        # Create a dummy chat history file
        (gemini_tmp_dir / "chat1.txt").write_text("This is a chat history.")

        # 1. Backup the chat history
        backup_chat_history(backup_path, gemini_home_dir)

        # Verify the backup
        backup_dir = backup_path / "tmp"
        assert (backup_dir / "chat1.txt").exists()
        assert (backup_dir / "chat1.txt").read_text() == "This is a chat history."

        # 2. Clear the original chat history
        shutil.rmtree(gemini_tmp_dir)
        gemini_tmp_dir.mkdir()
        assert not (gemini_tmp_dir / "chat1.txt").exists()

        # 3. Restore the chat history
        restore_chat_history(backup_path, gemini_home_dir)

        # Verify the restore
        assert (gemini_tmp_dir / "chat1.txt").exists()
        assert (gemini_tmp_dir / "chat1.txt").read_text() == "This is a chat history."

def test_cleanup_chat_history():
    with tempfile.TemporaryDirectory() as tmpdir:
        home_dir = Path(tmpdir)
        gemini_home_dir = home_dir / ".gemini"
        gemini_tmp_dir = gemini_home_dir / "tmp"
        gemini_tmp_dir.mkdir(parents=True)

        # Create a dummy chat history file and a bin directory to be preserved
        (gemini_tmp_dir / "chat1.txt").write_text("This is a chat history.")
        (gemini_tmp_dir / "bin").mkdir()
        (gemini_tmp_dir / "bin" / "some_executable").write_text("...")

        # Cleanup without force
        with patch('builtins.input', return_value='y'):
            cleanup_chat_history(dry_run=False, force=False, gemini_home_dir=gemini_home_dir)

        # Verify that chat1.txt is deleted and bin is preserved
        assert not (gemini_tmp_dir / "chat1.txt").exists()
        assert (gemini_tmp_dir / "bin").exists()

@patch("subprocess.run")
def test_resume_chat(mock_run):
    resume_chat()
    mock_run.assert_called_once_with(["gemini", "--model", "pro", "--resume"])
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from geminiai_cli.chat import backup_chat_history, restore_chat_history, cleanup_chat_history, resume_chat
from geminiai_cli.config import NEON_RED, NEON_GREEN, NEON_YELLOW, NEON_CYAN

def test_backup_chat_history_exception(fs, capsys):
    fs.create_dir("/home/user/.gemini/tmp")
    fs.create_file("/home/user/.gemini/tmp/chat.log")
    fs.create_dir("/backup")

    gemini_home_dir = Path("/home/user/.gemini")
    backup_path = Path("/backup")

    with patch("shutil.copy", side_effect=Exception("Copy failed")):
        backup_chat_history(backup_path, gemini_home_dir)

    captured = capsys.readouterr()
    assert "Failed to backup chat history: Copy failed" in captured.out

def test_restore_chat_history_exception(fs, capsys):
    fs.create_dir("/backup/tmp")
    fs.create_file("/backup/tmp/chat.log")
    fs.create_dir("/home/user/.gemini")

    gemini_home_dir = Path("/home/user/.gemini")
    backup_path = Path("/backup")

    with patch("shutil.copy", side_effect=Exception("Restore failed")):
        restore_chat_history(backup_path, gemini_home_dir)

    captured = capsys.readouterr()
    assert "Failed to restore chat history: Restore failed" in captured.out

def test_cleanup_chat_history_listdir_exception(fs, capsys):
    fs.create_dir("/home/user/.gemini/tmp")
    gemini_home_dir = Path("/home/user/.gemini")

    with patch("os.listdir", side_effect=Exception("Access denied")):
        cleanup_chat_history(dry_run=False, force=False, gemini_home_dir=gemini_home_dir)

    captured = capsys.readouterr()
    assert "[ERROR] Could not list directory" in captured.out
    assert "Access denied" in captured.out

def test_cleanup_chat_history_interactive_cancel(fs, capsys):
    fs.create_dir("/home/user/.gemini/tmp")
    fs.create_file("/home/user/.gemini/tmp/chat.log")
    gemini_home_dir = Path("/home/user/.gemini")

    with patch("builtins.input", return_value="n"):
        cleanup_chat_history(dry_run=False, force=False, gemini_home_dir=gemini_home_dir)

    captured = capsys.readouterr()
    assert "Cleanup cancelled." in captured.out

def test_cleanup_chat_history_delete_exception(fs, capsys):
    fs.create_dir("/home/user/.gemini/tmp")
    fs.create_file("/home/user/.gemini/tmp/chat.log")
    gemini_home_dir = Path("/home/user/.gemini")

    with patch("os.unlink", side_effect=Exception("Delete failed")):
        cleanup_chat_history(dry_run=False, force=True, gemini_home_dir=gemini_home_dir)

    captured = capsys.readouterr()
    assert "[ERROR] Failed to delete chat.log: Delete failed" in captured.out

def test_resume_chat_file_not_found(capsys):
    with patch("subprocess.run", side_effect=FileNotFoundError):
        resume_chat()

    captured = capsys.readouterr()
    assert "The 'gemini' command was not found" in captured.out

def test_resume_chat_exception(capsys):
    with patch("subprocess.run", side_effect=Exception("Unexpected error")):
        resume_chat()

    captured = capsys.readouterr()
    assert "Failed to resume chat: Unexpected error" in captured.out
