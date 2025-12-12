# tests/test_cli.py

import pytest
from unittest.mock import patch, MagicMock
from geminiai_cli.cli import main, print_rich_help, RichHelpParser

@patch("geminiai_cli.cli.do_login")
def test_main_login(mock_do_login):
    with patch("sys.argv", ["geminiai", "--login"]):
        main()
        mock_do_login.assert_called_once()

@patch("geminiai_cli.cli.do_logout")
def test_main_logout(mock_do_logout):
    with patch("sys.argv", ["geminiai", "--logout"]):
        main()
        mock_do_logout.assert_called_once()

@patch("geminiai_cli.cli.do_update")
def test_main_update(mock_do_update):
    with patch("sys.argv", ["geminiai", "--update"]):
        main()
        mock_do_update.assert_called_once()

@patch("geminiai_cli.cli.do_check_update")
def test_main_check_update(mock_do_check_update):
    with patch("sys.argv", ["geminiai", "--check-update"]):
        main()
        mock_do_check_update.assert_called_once()

# We test print_rich_help body now instead of mocking it
def test_print_rich_help():
    with patch("sys.exit") as mock_exit:
        print_rich_help()
        mock_exit.assert_called_with(0)

@patch("geminiai_cli.cli.perform_backup")
def test_main_backup(mock_perform_backup):
    with patch("sys.argv", ["geminiai", "backup"]):
        main()
        mock_perform_backup.assert_called_once()

@patch("geminiai_cli.cli.perform_restore")
def test_main_restore(mock_perform_restore):
    with patch("sys.argv", ["geminiai", "restore"]):
        main()
        mock_perform_restore.assert_called_once()

@patch("geminiai_cli.cli.perform_integrity_check")
def test_main_integrity(mock_perform_integrity):
    with patch("sys.argv", ["geminiai", "check-integrity"]):
        main()
        mock_perform_integrity.assert_called_once()

@patch("geminiai_cli.cli.perform_list_backups")
def test_main_list_backups(mock_perform_list_backups):
    with patch("sys.argv", ["geminiai", "list-backups"]):
        main()
        mock_perform_list_backups.assert_called_once()

@patch("geminiai_cli.cli.perform_check_b2")
def test_main_check_b2(mock_perform_check_b2):
    with patch("sys.argv", ["geminiai", "check-b2"]):
        main()
        mock_perform_check_b2.assert_called_once()

@patch("geminiai_cli.cli.do_list_resets")
def test_main_list_resets(mock_list):
    with patch("sys.argv", ["geminiai", "resets", "--list"]):
        main()
        mock_list.assert_called_once()

@patch("geminiai_cli.cli.remove_entry_by_id")
def test_main_remove_resets(mock_remove):
    mock_remove.return_value = True
    with patch("sys.argv", ["geminiai", "resets", "--remove", "id"]):
        main()
        mock_remove.assert_called_once_with("id")

@patch("geminiai_cli.cli.remove_entry_by_id")
def test_main_remove_resets_fail(mock_remove):
    mock_remove.return_value = False
    with patch("sys.argv", ["geminiai", "resets", "--remove", "id"]):
        main()
        mock_remove.assert_called_once_with("id")

@patch("geminiai_cli.cli.do_next_reset")
def test_main_next_resets(mock_next):
    with patch("sys.argv", ["geminiai", "resets", "--next"]):
        main()
        mock_next.assert_called_once_with(None)

@patch("geminiai_cli.cli.do_next_reset")
def test_main_next_arg_resets(mock_next):
    with patch("sys.argv", ["geminiai", "resets", "--next", "id"]):
        main()
        mock_next.assert_called_once_with("id")

@patch("geminiai_cli.cli.do_capture_reset")
def test_main_add_resets(mock_add):
    with patch("sys.argv", ["geminiai", "resets", "--add", "time"]):
        main()
        mock_add.assert_called_once_with("time")

# New tests for additional coverage

@patch("geminiai_cli.cli.cloud_sync")
def test_main_cloud_sync(mock_cloud_sync):
    with patch("sys.argv", ["geminiai", "cloud-sync"]):
        main()
        mock_cloud_sync.assert_called_once()

@patch("geminiai_cli.cli.local_sync")
def test_main_local_sync(mock_local_sync):
    with patch("sys.argv", ["geminiai", "local-sync"]):
        main()
        mock_local_sync.assert_called_once()

@patch("geminiai_cli.cli.do_config")
def test_main_config(mock_do_config):
    with patch("sys.argv", ["geminiai", "config", "list"]):
        main()
        mock_do_config.assert_called_once()

@patch("geminiai_cli.cli.do_doctor")
def test_main_doctor(mock_do_doctor):
    with patch("sys.argv", ["geminiai", "doctor"]):
        main()
        mock_do_doctor.assert_called_once()

@patch("geminiai_cli.cli.do_prune")
def test_main_prune(mock_do_prune):
    with patch("sys.argv", ["geminiai", "prune"]):
        main()
        mock_do_prune.assert_called_once()

@patch("geminiai_cli.cli.do_session")
def test_main_session(mock_do_session):
    with patch("sys.argv", ["geminiai", "--session"]):
        main()
        mock_do_session.assert_called_once()

# Test RichHelpParser
def test_rich_help_parser_error():
    parser = RichHelpParser()
    with patch("sys.exit") as mock_exit:
        parser.error("Test error")
        mock_exit.assert_called_with(2)

def test_rich_help_parser_print_help_subcommand():
    parser = RichHelpParser(prog="geminiai backup", description="Backup command")
    # Just ensure it runs without error and prints something
    with patch("builtins.print"):
        parser.print_help()

def test_rich_help_parser_print_help_main():
    parser = RichHelpParser(prog="geminiai", description="Gemini AI Automation Tool")
    with patch("sys.exit") as mock_exit:
         parser.print_help()
         # print_rich_help calls exit(0)
         mock_exit.assert_called_with(0)

@patch("geminiai_cli.cli.print_rich_help")
def test_main_no_args(mock_help):
    with patch("sys.argv", ["geminiai"]):
        with patch("sys.exit"): # Help parser exits
             main()
        mock_help.assert_called()

@patch("geminiai_cli.cli.print_rich_help")
def test_main_help_arg(mock_help):
    with patch("sys.argv", ["geminiai", "--help"]):
        with patch("sys.exit"):
            main()
        mock_help.assert_called()

@patch("geminiai_cli.cli.RichHelpParser.print_help")
def test_main_resets_no_args(mock_print_help):
    with patch("sys.argv", ["geminiai", "resets"]):
        main()
        mock_print_help.assert_called()

# Test arg parsing branches for backup (cloud options)
@patch("geminiai_cli.cli.perform_backup")
def test_main_backup_cloud(mock_backup):
    with patch("sys.argv", ["geminiai", "backup", "--cloud", "--bucket", "b", "--b2-id", "i", "--b2-key", "k"]):
        main()
        mock_backup.assert_called()

@patch("geminiai_cli.cli.perform_backup")
def test_main_backup_empty_src(mock_backup):
    with patch("sys.argv", ["geminiai", "backup", "--src", ""]):
        main()
        mock_backup.assert_called()

@patch("geminiai_cli.cli.perform_backup")
def test_main_backup_dry_run(mock_backup):
    with patch("sys.argv", ["geminiai", "backup", "--dry-run"]):
        main()
        mock_backup.assert_called()

@patch("geminiai_cli.cli.perform_backup")
def test_main_backup_no_archive_dir(mock_backup):
    # Default is set, so we need to explicitly set it to empty string to trigger false branch if argparse allows it
    # Actually argparse default fills it.
    # If I pass --archive-dir="", args.archive_dir will be "".
    with patch("sys.argv", ["geminiai", "backup", "--archive-dir", ""]):
        main()
        mock_backup.assert_called()

@patch("geminiai_cli.cli.perform_backup")
def test_main_backup_no_dest_parent(mock_backup):
    with patch("sys.argv", ["geminiai", "backup", "--dest-dir-parent", ""]):
        main()
        mock_backup.assert_called()

# Test arg parsing for restore (cloud options)
@patch("geminiai_cli.cli.perform_restore")
def test_main_restore_cloud(mock_restore):
    with patch("sys.argv", ["geminiai", "restore", "--cloud", "--bucket", "b", "--b2-id", "i", "--b2-key", "k", "--dest", "d", "--force", "--dry-run", "--from-dir", "d", "--from-archive", "a", "--search-dir", "s"]):
        main()
        mock_restore.assert_called()

@patch("geminiai_cli.cli.perform_restore")
def test_main_restore_empty_search_dir(mock_restore):
    with patch("sys.argv", ["geminiai", "restore", "--search-dir", ""]):
        main()
        mock_restore.assert_called()

# Test arg parsing for list-backups
@patch("geminiai_cli.cli.perform_list_backups")
def test_main_list_backups_args(mock_list):
     with patch("sys.argv", ["geminiai", "list-backups", "--cloud", "--bucket", "b", "--b2-id", "i", "--b2-key", "k", "--search-dir", "s"]):
        main()
        mock_list.assert_called()

@patch("geminiai_cli.cli.perform_list_backups")
def test_main_list_backups_empty_search_dir(mock_list):
     with patch("sys.argv", ["geminiai", "list-backups", "--search-dir", ""]):
        main()
        mock_list.assert_called()

# Test arg parsing for check-b2
@patch("geminiai_cli.cli.perform_check_b2")
def test_main_check_b2_args(mock_check):
     with patch("sys.argv", ["geminiai", "check-b2", "--bucket", "b", "--b2-id", "i", "--b2-key", "k"]):
        main()
        mock_check.assert_called()

# Test arg parsing for check-integrity
@patch("geminiai_cli.cli.perform_integrity_check")
def test_main_integrity_args(mock_integrity):
    with patch("sys.argv", ["geminiai", "check-integrity", "--src", "s"]):
        main()
        mock_integrity.assert_called()

def test_rich_help_parser_print_help_subcommand_with_default():
    parser = RichHelpParser(prog="geminiai backup", description="Backup command")
    parser.add_argument("--test", default="val", help="help")
    with patch("builtins.print"):
        parser.print_help()

@patch("geminiai_cli.cli.print_rich_help")
def test_main_else_branch(mock_help):
    # To hit the else branch, we need valid args that don't match any known command logic block?
    # But argparse handles command validation.
    # The 'else' block is `else: print_rich_help()`.
    # This happens if args.command is None (no subcommand) AND no top level args matched.
    # But main uses `subparsers.add_subparsers(dest="command"...)`.
    # If no subcommand provided, args.command is None.
    # If no flags provided, we hit `if len(sys.argv) == 1`.
    # If we provide an unknown flag, argparse errors.
    # If we provide a known flag that doesn't have a handler logic block?
    # All flags have handlers.
    # If we provide NO flags and NO command, but we bypass the manual check `if len(sys.argv) == 1`?
    # Wait, `if len(sys.argv) == 1` calls print_rich_help.
    # So we need `sys.argv` length > 1 but no command and no top level flag.
    # e.g. `geminiai --unknown` -> argparse error.

    # What if we just patch parse_args to return empty namespace with command=None?
    with patch("argparse.ArgumentParser.parse_args") as mock_parse:
        mock_parse.return_value = MagicMock(command=None, login=False, logout=False, session=False, update=False, check_update=False)
        # We need sys.argv > 1 to avoid first check
        with patch("sys.argv", ["geminiai", "--something-ignored"]):
            main()
            mock_help.assert_called()
