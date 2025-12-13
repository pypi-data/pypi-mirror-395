#!/usr/bin/env python3
# src/geminiai_cli/cooldown.py

import os
import json
import datetime
from typing import Dict, Optional

from .ui import cprint, console, NEON_CYAN, NEON_GREEN, NEON_YELLOW, NEON_RED, RESET
from .b2 import B2Manager
from .credentials import resolve_credentials
from .reset_helpers import get_all_resets, remove_entry_by_id, sync_resets_with_cloud
from . import history

# ... existing code ...

def do_remove_account(email: str, args=None):
    """
    Removes an account from the dashboard.
    1. Removes from 'gemini-resets.json' (Log)
    2. Removes from 'gemini-cooldown.json' (State)
    3. Syncs both changes to cloud (if credentials available)
    """
    cprint(NEON_CYAN, f"Removing account '{email}' from dashboard...")
    
    # 1. Remove from Resets (Logbook)
    removed_resets = remove_entry_by_id(email)
    if removed_resets:
        cprint(NEON_GREEN, f"[OK] Removed reset history for {email}")
    else:
        cprint(NEON_YELLOW, f"[INFO] No reset history found for {email}")

    # 2. Remove from Cooldowns (State)
    path = os.path.expanduser(COOLDOWN_FILE)
    data = get_cooldown_data()
    
    if email in data:
        del data[email]
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
            cprint(NEON_GREEN, f"[OK] Removed cooldown state for {email}")
        except IOError as e:
            cprint(NEON_RED, f"[ERROR] Failed to update local file: {e}")
    else:
        cprint(NEON_YELLOW, f"[INFO] No active cooldown state found for {email}")

    # 3. Cloud Sync (Both files)
    # Only attempt if we have credentials in args (or environment)
    try:
        key_id, app_key, bucket_name = resolve_credentials(args)
        if key_id and app_key and bucket_name:
            cprint(NEON_CYAN, "Syncing removal to cloud...")
            
            # Sync Cooldowns
            _sync_cooldown_file(direction='upload', args=args)
            
            # Sync Resets
            try:
                b2 = B2Manager(key_id, app_key, bucket_name)
                sync_resets_with_cloud(b2)
            except Exception as e:
                 cprint(NEON_RED, f"[WARN] Failed to sync resets removal: {e}")
                 
            cprint(NEON_GREEN, "Cloud sync complete.")
    except Exception:
        # Creds not available, skip silent
        pass
from rich.table import Table
from rich.panel import Panel
from rich.align import Align


from .config import NEON_CYAN, NEON_YELLOW, NEON_GREEN, NEON_RED, RESET, COOLDOWN_FILE

# File to store cooldown data
CLOUD_COOLDOWN_FILENAME = "gemini-cooldown.json"
COOLDOWN_HOURS = 24


def _sync_cooldown_file(direction: str, args):
    """
    Private helper to sync the cooldown file with B2 cloud storage.

    Args:
        direction: 'upload' or 'download'.
        args: Command-line arguments containing B2 credentials.
    """
    try:
        key_id, app_key, bucket_name = resolve_credentials(args)
        if not all([key_id, app_key, bucket_name]):
            cprint(NEON_YELLOW, "Warning: Cloud credentials not fully configured. Skipping cloud sync.")
            return

        b2 = B2Manager(key_id, app_key, bucket_name)
        local_path = os.path.expanduser(COOLDOWN_FILE)

        if direction == "download":
            cprint(NEON_CYAN, f"Downloading latest cooldown file from B2 bucket '{bucket_name}'...")
            content = b2.download_to_string(CLOUD_COOLDOWN_FILENAME)
            
            if content is None:
                cprint(NEON_YELLOW, "No cooldown file found in the cloud. Using local version.")
            else:
                try:
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    with open(local_path, "w") as f:
                        f.write(content)
                    cprint(NEON_GREEN, "Cooldown file synced from cloud.")
                except IOError as e:
                    cprint(NEON_RED, f"Error writing local cooldown file: {e}")

        elif direction == "upload":
            if not os.path.exists(local_path):
                cprint(NEON_YELLOW, "Local cooldown file not found. Skipping upload.")
                return
            cprint(NEON_CYAN, f"Uploading cooldown file to B2 bucket '{bucket_name}'...")
            try:
                b2.upload(local_path, CLOUD_COOLDOWN_FILENAME)
                cprint(NEON_GREEN, "Cooldown file synced to cloud.")
            except Exception as e:
                cprint(NEON_RED, f"Error uploading cooldown file: {e}")

    except Exception as e:
        cprint(NEON_RED, f"An unexpected error occurred during cloud sync: {e}")


def get_cooldown_data() -> Dict[str, str]:
    """
    Reads the cooldown data from the JSON file.

    Returns:
        A dictionary mapping email addresses to their last switch timestamp (ISO 8601).
        Returns an empty dictionary if the file doesn't exist or is invalid.
    """
    path = os.path.expanduser(COOLDOWN_FILE)
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            return {}
    except (json.JSONDecodeError, IOError):
        return {}

def record_switch(email: str, args=None):
    """
    Records an account switch using a "merge-before-write" strategy for cloud sync.
    It downloads the latest state from the cloud, adds the new entry, and uploads.

    Args:
        email: The email address of the account that has become active.
        args: Optional command-line arguments for cloud credentials.
    """
    if not email:
        return
        
    # Record to history log
    history.record_event(email, "switch")

    # If cloud is configured, sync down the master file first to merge with it.
    if args:
        _sync_cooldown_file(direction='download', args=args)
        
    path = os.path.expanduser(COOLDOWN_FILE)
    # Now, get the most up-to-date data (either from cloud or local).
    data = get_cooldown_data()
    
    # Get current time in ISO 8601 format and update the record.
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    data[email] = now_iso
    
    try:
        # Write the newly merged data back to the local file.
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        cprint(NEON_RED, f"Error: Could not write to local cooldown file at {path}: {e}")
        return # Don't proceed to upload if local write failed

    # If cloud is configured, sync the merged file back up.
    if args:
        _sync_cooldown_file(direction='upload', args=args)

def do_cooldown_list(args=None):
    """
    Displays the Master Dashboard: merged view of Cooldowns (Switch events) and Scheduled Resets.
    """
    # 1. Sync if requested
    if args and getattr(args, 'cloud', False):
        _sync_cooldown_file(direction='download', args=args)
        # Also sync resets
        try:
            key_id, app_key, bucket_name = resolve_credentials(args)
            if key_id and app_key and bucket_name:
                b2 = B2Manager(key_id, app_key, bucket_name)
                sync_resets_with_cloud(b2)
        except Exception as e:
             cprint(NEON_RED, f"[WARN] Failed to sync resets: {e}")

    # 2. Load Data
    cooldown_map = get_cooldown_data() # {email: last_switch_iso}
    resets_list = get_all_resets()     # [{email:..., reset_ist:...}, ...]

    all_emails = set(cooldown_map.keys())
    for entry in resets_list:
        if entry.get("email"):
            all_emails.add(entry["email"].lower())

    if not all_emails:
        cprint(NEON_YELLOW, "No account data found (switches or resets).")
        return

    # 3. Build Table
    table = Table(show_header=True, header_style="bold white", border_style="blue", padding=(0, 1))
    table.add_column("Account", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Availability", style="white")
    table.add_column("Last Used", style="dim")
    table.add_column("Next Scheduled Reset", style="magenta")

    now = datetime.datetime.now(datetime.timezone.utc)
    
    # Helper for relative time
    def format_delta(delta):
        s = int(delta.total_seconds())
        if s < 0: return "passed"
        h, r = divmod(s, 3600)
        m, _ = divmod(r, 60)
        return f"In {h}h {m}m"

    def format_ago(delta):
        s = int(delta.total_seconds())
        if s < 60: return "Just now"
        if s < 3600: return f"{s//60}m ago"
        if s < 86400: return f"{s//3600}h ago"
        return f"{s//86400}d ago"

    sorted_emails = sorted(list(all_emails))

    for email in sorted_emails:
        # --- Analyze Cooldown (Last Switch) ---
        last_used_str = "-"
        availability_str = "Now"
        is_locked = False
        
        if email in cooldown_map:
            try:
                last_ts = datetime.datetime.fromisoformat(cooldown_map[email])
                if last_ts.tzinfo is None:
                    last_ts = last_ts.replace(tzinfo=datetime.timezone.utc)
                
                # Calculate ago
                ago_delta = now - last_ts
                last_used_str = format_ago(ago_delta)
                
                # Calculate Lockout
                unlock_time = last_ts + datetime.timedelta(hours=COOLDOWN_HOURS)
                remaining = unlock_time - now
                
                if remaining.total_seconds() > 0:
                    is_locked = True
                    availability_str = format_delta(remaining)
            except ValueError:
                last_used_str = "Invalid TS"

        # --- Analyze Resets (Next Scheduled) ---
        next_reset_str = "-"
        has_upcoming_reset = False
        
        # Filter resets for this email, find earliest future one
        my_resets = []
        for r in resets_list:
            if r.get("email", "").lower() == email:
                try:
                    # resets are stored as ISO strings (likely with timezone info)
                    # We need to compare safely.
                    r_ts = datetime.datetime.fromisoformat(r["reset_ist"])
                    if r_ts.tzinfo is None:
                         # If raw stored without TZ, assume local/UTC? 
                         # Existing logic uses IST timezone in reset_helpers, so it should have offsets.
                         # We'll blindly compare to 'now' if possible or just display.
                         pass
                    my_resets.append(r_ts)
                except Exception:
                    pass
        
        # Sort and find first future
        my_resets.sort()
        # We need to compare with 'now'. If resets are timezone aware (e.g. IST), 
        # and 'now' is UTC, python handles it if both have tzinfo.
        for r_ts in my_resets:
            if r_ts > now:
                # Found future reset
                diff = r_ts - now
                next_reset_str = format_delta(diff)
                has_upcoming_reset = True
                break

        # --- Determine Final Status ---
        if is_locked:
            status = "[bold red]🔴 COOLDOWN[/]"
            avail_style = "[red]" + availability_str + "[/]"
        elif has_upcoming_reset:
             # Not strictly locked by 24h rule, but has a scheduled event
            status = "[bold yellow]🟡 SCHEDULED[/]"
            avail_style = "[green]Now[/]"
        else:
            status = "[bold green]🟢 READY[/]"
            avail_style = "[bold green]Now[/]"

        table.add_row(email, status, avail_style, last_used_str, next_reset_str)

    console.print("\n[bold white]📊 Account Dashboard[/]")
    console.print(table)
    console.print()

