#!/usr/bin/env python3
# src/geminiai_cli/cli.py


import argparse
import sys
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from .ui import banner, cprint, console
from .banner import print_logo
from .login import do_login
from .logout import do_logout
from .session import do_session
from .cooldown import do_cooldown_list, do_remove_account
from .settings_cli import do_config
from .doctor import do_doctor
from .prune import do_prune
from .update import do_update, do_check_update
from .recommend import do_recommend
from .stats import do_stats
from .reset_helpers import (
    do_next_reset,
    do_capture_reset,
    do_list_resets,
    remove_entry_by_id,
)
from .config import (
    NEON_YELLOW, 
    NEON_CYAN, 
    DEFAULT_BACKUP_DIR, 
    DEFAULT_GEMINI_HOME,
    OLD_CONFIGS_DIR,
    CHAT_HISTORY_BACKUP_PATH
)
from .backup import perform_backup
from .restore import perform_restore
from .integrity import perform_integrity_check
from .list_backups import perform_list_backups
from .check_b2 import perform_check_b2
from .sync import perform_sync
from .chat import backup_chat_history, restore_chat_history, cleanup_chat_history, resume_chat
from .project_config import load_project_config, normalize_config_keys

def print_rich_help():
    """Prints a beautiful Rich-formatted help screen for the MAIN command."""
 #    print_logo()
    
    console.print("[bold white]Usage:[/] [bold cyan]geminiai[/] [dim][OPTIONS][/] [bold magenta]COMMAND[/] [dim][ARGS]...[/]\n")

    # Commands Table
    cmd_table = Table(show_header=False, box=None, padding=(0, 2))
    cmd_table.add_column("Command", style="bold cyan", width=20)
    cmd_table.add_column("Description", style="white")

    commands = [
        ("backup", "Backup Gemini configuration and chats"),
        ("restore", "Restore Gemini configuration from a backup"),
        ("chat", "Manage chat history"),
        ("check-integrity", "Check integrity of current configuration"),
        ("list-backups", "List available backups"),
        ("prune", "Prune old backups (local or cloud)"),
        ("check-b2", "Verify Backblaze B2 credentials"),
        ("sync", "Sync backups with Cloud (push/pull)"),
        ("config", "Manage persistent configuration"),
        ("doctor", "Run system diagnostic check"),
        ("resets", "Manage Gemini free tier reset schedules"),
        ("cooldown", "Show account cooldown status"),
        ("recommend", "Get the next best account recommendation"),
        ("stats", "Show usage statistics (last 7 days)"),
    ]
    
    for cmd, desc in commands:
        cmd_table.add_row(cmd, desc)

    console.print(Panel(cmd_table, title="[bold magenta]Available Commands[/]", border_style="cyan"))

    # Options Table
    opt_table = Table(show_header=False, box=None, padding=(0, 2))
    opt_table.add_column("Option", style="bold yellow", width=20)
    opt_table.add_column("Description", style="white")

    options = [
        ("--login", "Login to Gemini CLI"),
        ("--logout", "Logout from Gemini CLI"),
        ("--session", "Show current active session"),
        ("--update", "Reinstall / update Gemini CLI"),
        ("--check-update", "Check for updates"),
        ("--help, -h", "Show this message and exit"),
    ]

    for opt, desc in options:
        opt_table.add_row(opt, desc)

    console.print(Panel(opt_table, title="[bold yellow]Options[/]", border_style="green"))
    sys.exit(0)

class RichHelpParser(argparse.ArgumentParser):
    """
    Custom parser that overrides print_help to display a Rich-based help screen
    for subcommands (and the main command if accessed via standard flow).
    """
    def error(self, message):
        console.print(f"[bold red]Error:[/ {message}")
        # Only print full help if really needed, or just hint
        console.print("[dim]Use --help for usage information.[/]")
        sys.exit(2)

    def print_help(self, file=None):
        """
        Dynamically generates Rich help for ANY parser (main or subcommand).
        """
        # If this is the main parser (checking by prog name usually, or description),
        # we might want to use the specialized print_rich_help() for the fancy banner.
        # However, implementing a generic one is better for subcommands.
        
        if self.description and "Gemini AI Automation Tool" in self.description:
             # This is likely the main parser
             print_rich_help()
             return

        # For Subcommands (e.g., 'geminiai backup')
        console.print(f"[bold cyan]Command:[/ ] [bold magenta]{self.prog}[/]\n")
        if self.description:
            console.print(f"[italic]{self.description}[/]\n")
        
        # Usage
        console.print(f"[bold white]Usage:[/ ] [dim]{self.format_usage().strip().replace('usage: ', '')}[/]\n")

        # Arguments
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Option", style="bold yellow", width=30)
        table.add_column("Description", style="white")

        for action in self._actions:
            # Skip help if we want, but usually good to show
            opts = ", ".join(action.option_strings)
            if not opts:
                opts = action.dest # Positional arg
            
            help_text = action.help or ""
            # Handle default values
            if action.default != argparse.SUPPRESS and action.default is not None:
                # help_text += f" [dim](default: {action.default})[/]" 
                pass # argparse puts default in help usually, check formatting

            table.add_row(opts, help_text)

        console.print(Panel(table, title="[bold green]Arguments & Options[/]", border_style="cyan"))

def main():
    print_logo()
    # Handle main help manually to use Rich if no args or explicit help on main
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help"]):
        print_rich_help()

    # Use RichHelpParser for the main parser
    parser = RichHelpParser(description="Gemini AI Automation Tool", add_help=False)
    
    # Load project config (pyproject.toml / geminiai.toml)
    project_defaults = load_project_config()
    if project_defaults:
        # Normalize keys (kebab-case -> snake_case)
        project_defaults = normalize_config_keys(project_defaults)
        parser.set_defaults(**project_defaults)

    subparsers = parser.add_subparsers(dest="command", help="Available commands", parser_class=RichHelpParser)

    # Keep existing top-level arguments
    parser.add_argument("--login", action="store_true", help="Login to Gemini CLI")
    parser.add_argument("--logout", action="store_true", help="Logout from Gemini CLI")
    parser.add_argument("--session", action="store_true", help="Show current active session")
    parser.add_argument("--update", action="store_true", help="Reinstall / update Gemini CLI")
    parser.add_argument("--check-update", action="store_true", help="Check for updates")

    # Backup command
    backup_parser = subparsers.add_parser("backup", help="Backup Gemini configuration and chats (local or Backblaze B2 cloud).")
    backup_parser.add_argument("--src", default="~/.gemini", help="Source gemini dir (default ~/.gemini)")
    backup_parser.add_argument("--archive-dir", default=DEFAULT_BACKUP_DIR, help="Directory to store tar.gz archives (default: ~/.geminiai-cli/backups)")
    backup_parser.add_argument("--dest-dir-parent", default=OLD_CONFIGS_DIR, help="Parent directory where timestamped directory backups are stored")
    backup_parser.add_argument("--dry-run", action="store_true", help="Do not perform destructive actions")
    backup_parser.add_argument("--cloud", action="store_true", help="Create local backup AND upload to Cloud (B2)")
    backup_parser.add_argument("--bucket", help="B2 Bucket Name")
    backup_parser.add_argument("--b2-id", help="B2 Key ID (or set env GEMINI_B2_KEY_ID)")
    backup_parser.add_argument("--b2-key", help="B2 App Key (or set env GEMINI_B2_APP_KEY)")

    # Restore command
    restore_parser = subparsers.add_parser("restore", help="Restore Gemini configuration from a backup (local or Backblaze B2 cloud).")
    restore_parser.add_argument("--from-dir", help="Directory backup to restore from (preferred)")
    restore_parser.add_argument("--from-archive", help="Tar.gz archive to restore from")
    restore_parser.add_argument("--search-dir", default=DEFAULT_BACKUP_DIR, help="Directory to search for backup archives (*.gemini.tar.gz) when no --from-dir (default: ~/.geminiai-cli/backups)")
    restore_parser.add_argument("--dest", default="~/.gemini", help="Destination (default ~/.gemini)")
    restore_parser.add_argument("--force", action="store_true", help="Allow destructive replace without keeping .bak")
    restore_parser.add_argument("--dry-run", action="store_true", help="Do a dry run without destructive actions")
    restore_parser.add_argument("--cloud", action="store_true", help="Restore from Cloud (B2)")
    restore_parser.add_argument("--bucket", help="B2 Bucket Name")
    restore_parser.add_argument("--b2-id", help="B2 Key ID")
    restore_parser.add_argument("--b2-key", help="B2 App Key")
    restore_parser.add_argument("--auto", action="store_true", help="Automatically restore the best available account")

    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Manage chat history.")
    chat_subparsers = chat_parser.add_subparsers(dest="chat_command", help="Chat commands")
    chat_backup_parser = chat_subparsers.add_parser("backup", help="Backup chat history.")
    chat_restore_parser = chat_subparsers.add_parser("restore", help="Restore chat history.")
    chat_cleanup_parser = chat_subparsers.add_parser("cleanup", help="Clear temporary chat history and logs.")
    chat_cleanup_parser.add_argument("--dry-run", action="store_true", help="Show what would be deleted without doing it")
    chat_cleanup_parser.add_argument("--force", action="store_true", help="Skip confirmation prompt")
    chat_resume_parser = chat_subparsers.add_parser("resume", help="Resume the last chat session.")

    # Integrity check command
    integrity_parser = subparsers.add_parser("check-integrity", help="Check integrity of current configuration against the latest backup.")
    integrity_parser.add_argument("--src", default="~/.gemini", help="Source directory for integrity check (default: ~/.gemini)")

    # List backups command
    list_backups_parser = subparsers.add_parser("list-backups", help="List available backups (local or Backblaze B2 cloud).")
    list_backups_parser.add_argument("--search-dir", default=DEFAULT_BACKUP_DIR, help="Directory to search for backup archives (default: ~/.geminiai-cli/backups)")
    list_backups_parser.add_argument("--cloud", action="store_true", help="List backups from Cloud (B2)")
    list_backups_parser.add_argument("--bucket", help="B2 Bucket Name")
    list_backups_parser.add_argument("--b2-id", help="B2 Key ID")
    list_backups_parser.add_argument("--b2-key", help="B2 App Key")

    # Check B2 command
    check_b2_parser = subparsers.add_parser("check-b2", help="Verify Backblaze B2 credentials.")
    check_b2_parser.add_argument("--b2-id", help="B2 Key ID (or set env GEMINI_B2_KEY_ID)")
    check_b2_parser.add_argument("--b2-key", help="B2 App Key (or set env GEMINI_B2_APP_KEY)")
    check_b2_parser.add_argument("--bucket", help="B2 Bucket Name (or set env GEMINI_B2_BUCKET)")

    # Sync command (Unified Push/Pull)
    sync_parser = subparsers.add_parser("sync", help="Sync backups with Cloud (B2).")
    sync_subparsers = sync_parser.add_subparsers(dest="sync_direction", help="Sync direction")
    
    # Sync Push (Local -> Cloud)
    push_parser = sync_subparsers.add_parser("push", help="Upload missing local backups to Cloud.")
    push_parser.add_argument("--backup-dir", default=DEFAULT_BACKUP_DIR, help="Local backup directory (default: ~/.geminiai-cli/backups)")
    push_parser.add_argument("--bucket", help="B2 Bucket Name")
    push_parser.add_argument("--b2-id", help="B2 Key ID")
    push_parser.add_argument("--b2-key", help="B2 App Key")

    # Sync Pull (Cloud -> Local)
    pull_parser = sync_subparsers.add_parser("pull", help="Download missing Cloud backups to local.")
    pull_parser.add_argument("--backup-dir", default=DEFAULT_BACKUP_DIR, help="Local backup directory (default: ~/.geminiai-cli/backups)")
    pull_parser.add_argument("--bucket", help="B2 Bucket Name")
    pull_parser.add_argument("--b2-id", help="B2 Key ID")
    pull_parser.add_argument("--b2-key", help="B2 App Key")

    # Config command
    config_parser = subparsers.add_parser("config", help="Manage persistent configuration.")
    config_parser.add_argument("config_action", choices=["set", "get", "list", "unset"], help="Action to perform")
    config_parser.add_argument("key", nargs="?", help="Setting key")
    config_parser.add_argument("value", nargs="?", help="Setting value")
    config_parser.add_argument("--force", action="store_true", help="Force save sensitive keys without confirmation (automation mode)")

    # Resets command (New subcommand for reset management)
    resets_parser = subparsers.add_parser("resets", help="Manage Gemini free tier reset schedules.")
    resets_parser.add_argument("--list", action="store_true", help="List saved schedules")
    resets_parser.add_argument("--next", nargs="?", const="*ALL*", help="Show next usage time. Optionally pass email or id.")
    resets_parser.add_argument("--add", nargs="?", const="", help="Add time manually. Example: --add '01:00 PM user@example.com'")
    resets_parser.add_argument("--remove", nargs=1, help="Remove saved entry by id or email.")

    # Doctor command
    subparsers.add_parser("doctor", help="Run system diagnostic check.")

    # Prune command
    prune_parser = subparsers.add_parser("prune", help="Prune old backups.")
    prune_parser.add_argument("--keep", type=int, default=5, help="Number of recent backups to keep (default: 5)")
    prune_parser.add_argument("--backup-dir", default=DEFAULT_BACKUP_DIR, help="Local backup directory (default: ~/.geminiai-cli/backups)")
    prune_parser.add_argument("--cloud", action="store_true", help="Prune both local AND cloud backups")
    prune_parser.add_argument("--cloud-only", action="store_true", help="Only prune cloud backups")
    prune_parser.add_argument("--dry-run", action="store_true", help="Show what would be deleted without doing it")
    prune_parser.add_argument("--bucket", help="B2 Bucket Name")
    prune_parser.add_argument("--b2-id", help="B2 Key ID")
    prune_parser.add_argument("--b2-key", help="B2 App Key")

    # Cooldown command
    cooldown_parser = subparsers.add_parser("cooldown", help="Show account cooldown status, with optional cloud sync.")
    cooldown_parser.add_argument("--cloud", action="store_true", help="Sync cooldown status from the cloud.")
    cooldown_parser.add_argument("--bucket", help="B2 Bucket Name")
    cooldown_parser.add_argument("--b2-id", help="B2 Key ID")
    cooldown_parser.add_argument("--b2-key", help="B2 App Key")
    cooldown_parser.add_argument("--remove", nargs=1, help="Remove an account from the dashboard (both cooldown and resets).")

    # Recommend command
    recommend_parser = subparsers.add_parser("recommend", aliases=["next"], help="Suggest the next best account (Green & Least Recently Used).")
    # No arguments needed for now, but could add specific filters later.

    # Stats command
    stats_parser = subparsers.add_parser("stats", aliases=["usage"], help="Show usage statistics (last 7 days).")

    args = parser.parse_args()

    if args.command == "backup":
        perform_backup(args)
    elif args.command == "restore":
        perform_restore(args)
    elif args.command == "chat":
        if args.chat_command == "backup":
            backup_chat_history(CHAT_HISTORY_BACKUP_PATH, DEFAULT_GEMINI_HOME)
        elif args.chat_command == "restore":
            restore_chat_history(CHAT_HISTORY_BACKUP_PATH, DEFAULT_GEMINI_HOME)
        elif args.chat_command == "cleanup":
            cleanup_chat_history(args.dry_run, args.force, DEFAULT_GEMINI_HOME)
        elif args.chat_command == "resume":
            resume_chat()
    elif args.command == "check-integrity":
        perform_integrity_check(args)
    elif args.command == "list-backups":
        perform_list_backups(args)
    elif args.command == "check-b2":
        perform_check_b2(args)
    elif args.command == "sync":
        if args.sync_direction:
            perform_sync(args.sync_direction, args)
        else:
            # No subcommand provided
            parser.parse_args(["sync", "--help"])
    elif args.command == "config":
        do_config(args)
    elif args.command == "doctor":
        do_doctor()
    elif args.command == "prune":
        do_prune(args)
    elif args.command == "cooldown":
        if args.remove:
            do_remove_account(args.remove[0], args)
        else:
            do_cooldown_list(args)
    elif args.command == "recommend" or args.command == "next":
        do_recommend(args)
    elif args.command == "stats" or args.command == "usage":
        do_stats(args)
    elif args.command == "resets":
        if args.list:
            do_list_resets()
        elif args.remove is not None:
            key = args.remove[0]
            ok = remove_entry_by_id(key)
            if ok:
                cprint(NEON_CYAN, f"[OK] Removed entries matching: {key}")
            else:
                cprint(NEON_YELLOW, f"[WARN] No entries matched: {key}")
        elif args.next is not None:
            ident = args.next
            if ident == "*ALL*":
                ident = None
            do_next_reset(ident)
        elif args.add is not None:
            do_capture_reset(args.add)
        else:
            resets_parser.print_help()
    elif args.login:
        do_login()
    elif args.logout:
        do_logout()
    elif args.session:
        do_session()
    elif args.update:
        do_update()
    elif args.check_update:
        do_check_update()
    else:
        print_rich_help()


if __name__ == "__main__":
    main()
