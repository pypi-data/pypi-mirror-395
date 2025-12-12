#!/usr/bin/env python3
# src/geminiai_cli/restore.py

"""
restore.py - Safe restore that picks the oldest timestamped backup by default.

Naming convention expected for automatic discovery (produced by backup.py):
  YYYY-MM-DD_HHMMSS-<email>.gemini
Examples:
  2025-10-22_042211-bose13x@gmail.com.gemini
  2025-10-21_020211-kingchess@gmail.com.gemini

Behavior:
 - If --from-dir or --from-archive is passed, those are used.
 - If nothing is passed, script scans --search-dir (default /root) for
   directories matching the timestamp pattern and picks the oldest (earliest)
   timestamp to restore.
 - Safety: lockfile, temp copy, diff verification, .bak move of existing ~/.gemini,
   atomic replace, dry-run and --force supported.
"""
from __future__ import annotations
import argparse
import fcntl
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Optional, Tuple
from .config import DEFAULT_BACKUP_DIR, NEON_GREEN, NEON_RED, NEON_YELLOW, NEON_CYAN, RESET, DEFAULT_GEMINI_HOME, TIMESTAMPED_DIR_REGEX, OLD_CONFIGS_DIR, GEMINI_CLI_HOME
from .b2 import B2Manager
from .settings import get_setting
from .credentials import resolve_credentials
from .session import get_active_session
from .cooldown import record_switch
from .reset_helpers import add_24h_cooldown_for_email, sync_resets_with_cloud
from .recommend import get_recommendation, Recommendation
from .ui import cprint, NEON_YELLOW, NEON_RED, NEON_GREEN, NEON_CYAN

LOCKFILE = os.path.join(GEMINI_CLI_HOME, ".backup.lock")

def acquire_lock(path: str = LOCKFILE):
    # Ensure the directory for the lockfile exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd = open(path, "w+")
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("Another backup/restore is running. Exiting.")
        sys.exit(2)
    return fd

def run(cmd: str, check: bool = True, capture: bool = False):
    if capture:
        return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return subprocess.run(cmd, shell=True, check=check)

def shlex_quote(s: str) -> str:
    return shlex.quote(s)

def parse_timestamp_from_name(name: str) -> Optional[time.struct_time]:
    """
    Parse timestamp prefix like '2025-10-22_042211' into struct_time.
    Return None if it doesn't match.
    """
    m = TIMESTAMPED_DIR_REGEX.match(name)
    if not m:
        return None
    ts_str = m.group(1)  # 'YYYY-MM-DD_HHMMSS'
    try:
        return time.strptime(ts_str, "%Y-%m-%d_%H%M%S")
    except Exception:
        return None

def find_oldest_archive_backup(search_dir: str) -> Optional[str]:
    """
    Search search_dir for backup archives (*.gemini.tar.gz) matching the
    timestamp pattern and return the full path of the oldest backup (earliest
    timestamp). If none found, return None.
    """
    candidates: list[Tuple[time.struct_time, str]] = []
    try:
        for entry in os.listdir(search_dir):
            full_path = os.path.join(search_dir, entry)
            # We are now looking for archive files, not directories
            if not (os.path.isfile(full_path) and entry.endswith(".gemini.tar.gz")):
                continue

            # The name for parsing is the filename itself
            ts = parse_timestamp_from_name(entry)
            if ts:
                candidates.append((ts, full_path))
    except FileNotFoundError:
        return None

    if not candidates:
        return None

    # Sort by timestamp struct_time ascending (earliest first)
    candidates.sort(key=lambda x: time.mktime(x[0]))
    return candidates[0][1]


def find_latest_archive_backup_for_email(search_dir: str, email: str) -> Optional[str]:
    """
    Search search_dir for backup archives (*.gemini.tar.gz) matching the
    timestamp pattern AND the email. Returns the LATEST (newest) backup.
    """
    candidates: list[Tuple[time.struct_time, str]] = []
    try:
        for entry in os.listdir(search_dir):
            full_path = os.path.join(search_dir, entry)
            if not (os.path.isfile(full_path) and entry.endswith(".gemini.tar.gz")):
                continue

            # Robust matching: Parse filename to extract email
            # Format: YYYY-MM-DD_HHMMSS-<email>.gemini.tar.gz
            # Use regex from config if possible, or just look for the email suffix pattern.
            # Filename: {timestamp_str}-{email}.gemini.tar.gz
            # where timestamp_str is YYYY-MM-DD_HHMMSS (17 chars)

            # Extract suffix after first 18 chars (timestamp + hyphen)
            if len(entry) <= 18:
                continue

            suffix = entry[18:] # <email>.gemini.tar.gz
            if not suffix.endswith(".gemini.tar.gz"):
                continue

            email_in_file = suffix[:-14] # remove .gemini.tar.gz

            if email_in_file != email:
                continue

            ts = parse_timestamp_from_name(entry)
            if ts:
                candidates.append((ts, full_path))
    except FileNotFoundError:
        return None

    if not candidates:
        return None

    # Sort by timestamp struct_time DESCENDING (latest first)
    candidates.sort(key=lambda x: time.mktime(x[0]), reverse=True)
    return candidates[0][1]


def extract_archive(archive_path: str, extract_to: str):
    os.makedirs(extract_to, exist_ok=True)
    cmd = f"tar -C {shlex_quote(extract_to)} -xzf {shlex_quote(archive_path)}"
    run(cmd)

def perform_restore(args: argparse.Namespace):
    email_before = get_active_session()
    
    # Check for required args if not set (legacy check)
    if not hasattr(args, 'dest') or args.dest is None:
        args.dest = "~/.gemini"

    # Handle search_dir default if missing
    if not hasattr(args, 'search_dir') or args.search_dir is None:
        args.search_dir = DEFAULT_BACKUP_DIR

    dest = os.path.abspath(os.path.expanduser(args.dest))
    ts_now = time.strftime("%Y%m%d-%H%M%S")

    chosen_src: Optional[str] = None
    from_archive: Optional[str] = None
    temp_download_path: Optional[str] = None # Initialize for cloud downloads

    # --- NEW CODE BLOCK: CLOUD DISCOVERY ---
    if hasattr(args, 'cloud') and args.cloud:
        key_id, app_key, bucket_name = resolve_credentials(args)

        b2 = B2Manager(key_id, app_key, bucket_name)
        
        # 1. List backups
        print("Fetching file list from B2...")
        # b2sdk list_file_versions returns a generator of FileVersion objects
        all_files = []
        for file_version, _ in b2.list_backups():
            if file_version.file_name.endswith(".gemini.tar.gz"):
                ts = parse_timestamp_from_name(file_version.file_name)
                if ts:
                    all_files.append((ts, file_version.file_name))
        
        if not all_files:
            print("No valid backups found in B2 bucket.")
            sys.exit(1)

        target_file_name = None

        if hasattr(args, 'auto') and args.auto:
            rec = get_recommendation()
            if not rec:
                cprint(NEON_RED, "No 'Green' (Ready) accounts available for auto-switch.")
                sys.exit(1)

            target_email = rec.email
            cprint(NEON_CYAN, f"Auto-switch recommendation: {target_email}")

            # Filter files for this email
            candidates = []
            for ts, fname in all_files:
                if target_email in fname:
                    candidates.append((ts, fname))

            if not candidates:
                cprint(NEON_RED, f"No backups found in cloud for recommended account: {target_email}")
                sys.exit(1)

            # Select LATEST (newest) for auto-switch
            candidates.sort(key=lambda x: time.mktime(x[0]), reverse=True)
            target_file_name = candidates[0][1]
            cprint(NEON_GREEN, f"Selected latest cloud backup for {target_email}: {target_file_name}")

        elif hasattr(args, 'from_archive') and args.from_archive:
            # User requested a specific file
            wanted_name = os.path.basename(args.from_archive)
            # Check if it exists in the list we just fetched
            for _, fname in all_files:
                if fname == wanted_name:
                    target_file_name = fname
                    break
            
            if target_file_name:
                print(f"Selected specified cloud backup: {target_file_name}")
            else:
                print(f"Error: Specified archive '{wanted_name}' not found in B2 bucket.")
                sys.exit(1)
        else:
            # 2. Auto-select oldest (matches existing logic)
            # Sorting by timestamp (earliest first)
            all_files.sort(key=lambda x: time.mktime(x[0]))
            target_file_name = all_files[0][1]
            print(f"Auto-selected oldest cloud backup: {target_file_name}")

        # 3. Download to a temporary file
        temp_download_path = os.path.join(tempfile.gettempdir(), target_file_name)
        # Ensure the directory for the temporary download exists
        os.makedirs(os.path.dirname(temp_download_path), exist_ok=True)

        try:
            b2.download(target_file_name, temp_download_path)
        except Exception:
            sys.exit(1)
        
        from_archive = temp_download_path
    # ---------------------------------------

    elif hasattr(args, 'auto') and args.auto:
        rec = get_recommendation()
        if not rec:
            cprint(NEON_RED, "No 'Green' (Ready) accounts available for auto-switch.")
            sys.exit(1)

        target_email = rec.email
        cprint(NEON_CYAN, f"Auto-switch recommendation: {target_email}")

        sd = os.path.abspath(os.path.expanduser(args.search_dir))
        latest_archive = find_latest_archive_backup_for_email(sd, target_email)

        if not latest_archive:
            cprint(NEON_RED, f"No backups found locally for recommended account: {target_email}")
            sys.exit(1)

        from_archive = latest_archive
        cprint(NEON_GREEN, f"Selected latest local backup for {target_email}: {from_archive}")

    elif hasattr(args, 'from_dir') and args.from_dir:
        chosen_src = os.path.abspath(os.path.expanduser(args.from_dir))
        if not os.path.exists(chosen_src):
            print(f"Specified --from-dir not found: {chosen_src}")
            sys.exit(1)
    elif hasattr(args, 'from_archive') and args.from_archive:
        # First, try the path as provided by the user
        user_path = os.path.abspath(os.path.expanduser(args.from_archive))
        
        # If not found, try looking in the default search directory
        if not os.path.exists(user_path):
            search_dir = os.path.abspath(os.path.expanduser(args.search_dir))
            basename = os.path.basename(user_path)
            path_in_search_dir = os.path.join(search_dir, basename)
            
            if os.path.exists(path_in_search_dir):
                from_archive = path_in_search_dir
                print(f"Found archive in default backup directory: {from_archive}")
            else:
                print(f"Specified --from-archive not found at '{user_path}' or in search directory '{search_dir}'")
                sys.exit(1)
        else:
            from_archive = user_path
    else:
        # Auto-discover oldest timestamped *archive* in search_dir
        sd = os.path.abspath(os.path.expanduser(args.search_dir))
        print(f"Searching for oldest backup archive in: {sd}")
        oldest_archive = find_oldest_archive_backup(sd)
        if not oldest_archive:
            print(f"No timestamped backup archives (*.gemini.tar.gz) found in {sd}")
            sys.exit(1)
        
        from_archive = oldest_archive
        print(f"Auto-selected oldest backup archive: {from_archive}")

    lockfd = acquire_lock()
    try:
        work_tmp = tempfile.mkdtemp(prefix="gemini-restore-")
        try:
            if from_archive:
                print(f"Extracting archive {from_archive} -> {work_tmp}")
                if not getattr(args, 'dry_run', False):
                    extract_archive(from_archive, work_tmp)
                else:
                    print("DRY RUN: would extract archive.")
                src_for_copy = work_tmp
            else:
                # chosen_src is set (either provided or auto-selected)
                src_for_copy = os.path.abspath(chosen_src)
                print("Source to restore from:", src_for_copy)

            # Copy into temporary dest - to prepare verification
            tmp_dest = f"{dest}.tmp-{ts_now}"
            print(f"Copying {src_for_copy} -> {tmp_dest}")
            if not getattr(args, 'dry_run', False):
                if os.path.exists(tmp_dest):
                    shutil.rmtree(tmp_dest)
                cp_cmd = f"cp -a {shlex_quote(src_for_copy)} {shlex_quote(tmp_dest)}"
                run(cp_cmd)
            else:
                print("DRY RUN: would cp -a ...")

            # Verify copy with diff -r
            print("Verifying copy with diff -r")
            if not getattr(args, 'dry_run', False):
                diff_proc = run(f"diff -r {shlex_quote(tmp_dest)} {shlex_quote(src_for_copy)}", capture=True, check=False)
                if diff_proc.returncode != 0:
                    print("Verification FAILED (diff shows differences):")
                    if diff_proc.stdout:
                        print(diff_proc.stdout)
                    shutil.rmtree(tmp_dest, ignore_errors=True)
                    sys.exit(3)
                else:
                    print("Verification OK.")
            else:
                print("DRY RUN: would run diff -r ...")

            # Prepare swap: move existing dest to archive unless --force
            bakname = None
            if os.path.exists(dest) and not args.force:
                bak_filename = f".gemini.bak-{ts_now}"
                bakname = os.path.join(OLD_CONFIGS_DIR, bak_filename)
                
                if args.dry_run:
                    cprint(NEON_YELLOW, f"[DRY-RUN] Would move existing {dest} to {bakname}")
                else:
                    cprint(NEON_YELLOW, f"Backing up existing configuration to {bakname}...")
                    # If destination archive exists (highly unlikely with timestamp), remove it first or it will fail/nest
                    if os.path.exists(bakname):
                         shutil.rmtree(bakname)
                    shutil.move(dest, bakname)

            # Install new .gemini (atomic replace)
            print(f"Installing new .gemini from {tmp_dest} -> {dest}")
            if not getattr(args, 'dry_run', False):
                try:
                    os.replace(tmp_dest, dest)
                except OSError as e:
                     # Fallback for cross-device link if using tmp in different mount
                     if e.errno == 18: # EXDEV
                         shutil.move(tmp_dest, dest)
                     else:
                         raise e
            else:
                print("DRY RUN: would os.replace(tmp_dest, dest)")

            # Post-restore verification
            if not getattr(args, 'dry_run', False):
                print("Post-restore verification: diff -r between restored dest and source")
                diff2 = run(f"diff -r {shlex_quote(dest)} {shlex_quote(src_for_copy)}", capture=True, check=False)
                if diff2.returncode != 0:
                    print("Post-restore verification FAILED:")
                    if diff2.stdout:
                        print(diff2.stdout)
                    print("Attempting rollback (if possible).")
                    if not getattr(args, 'force', False) and bakname and os.path.exists(bakname):
                        try:
                            os.replace(bakname, dest)
                            print("Rollback to previous copy succeeded.")
                        except Exception as e:
                            print("Rollback failed:", e)
                    sys.exit(4)
                else:
                    print("Post-restore verification OK.")
            else:
                print("DRY RUN: would run post-restore diff")

            print("Restore complete.")
            if bakname and os.path.exists(bakname):
                print("Previous .gemini moved to:", bakname)

            # Check for account switch and record it
            if not getattr(args, 'dry_run', False):
                # --- Auto-Cooldown for Outgoing Account ---
                if email_before:
                    cprint(NEON_YELLOW, f"Auto-adding 24h cooldown for outgoing account: {email_before}")
                    add_24h_cooldown_for_email(email_before)
                    
                    # Sync with Cloud
                    try:
                        b2_for_sync = None
                        if getattr(args, 'cloud', False):
                            # Re-use the B2 instance from the restore process
                            # (It is defined in the 'if args.cloud:' block above)
                            b2_for_sync = locals().get('b2') 
                        
                        if not b2_for_sync:
                            # Try to resolve credentials independently
                            try:
                                kid, key, bkt = resolve_credentials(args)
                                if kid and key and bkt:
                                    b2_for_sync = B2Manager(kid, key, bkt)
                            except Exception:
                                # Credentials might not be configured, skip sync
                                pass
                        
                        if b2_for_sync:
                            sync_resets_with_cloud(b2_for_sync)
                    except Exception as e:
                        cprint(NEON_RED, f"[WARN] Could not sync resets to cloud: {e}")
                    
                    # Also update the cooldown dashboard (gemini-cooldown.json)
                    record_switch(email_before, args=args)
                # ------------------------------------------

                email_after = get_active_session()
                if email_before != email_after and email_after is not None:
                    print(f"Account switch detected: -> {email_after}")
                    print("Recording switch for 24h cooldown period...")
                    # Pass args to handle potential cloud upload
                    record_switch(email_after, args=args)

        finally:
            # cleanup temp extraction dir if still present
            if os.path.exists(work_tmp):
                try:
                    shutil.rmtree(work_tmp)
                except Exception:
                    pass
        # ADD THIS:
        if temp_download_path and os.path.exists(temp_download_path):
            try:
                os.remove(temp_download_path)
            except Exception:
                pass
    finally:
        try:
            fcntl.flock(lockfd, fcntl.LOCK_UN)
            lockfd.close()
        except Exception:
            pass

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--from-dir", help="Directory backup to restore from (legacy, archive is preferred)")
    p.add_argument("--from-archive", help="Tar.gz archive to restore from")
    p.add_argument("--search-dir", default=DEFAULT_BACKUP_DIR, help="Directory to search for timestamped backups when no source is specified (default: ~/.geminiai-cli/backups)")
    p.add_argument("--dest", default="~/.gemini", help="Destination (default ~/.gemini)")
    p.add_argument("--force", action="store_true", help="Allow destructive replace without keeping .bak")
    p.add_argument("--dry-run", action="store_true", help="Do a dry run without destructive actions")
    p.add_argument("--cloud", action="store_true", help="Restore from Cloud (B2)")
    p.add_argument("--bucket", help="B2 Bucket Name")
    p.add_argument("--b2-id", help="B2 Key ID (or set env GEMINI_B2_KEY_ID)")
    p.add_argument("--b2-key", help="B2 App Key (or set env GEMINI_B2_APP_KEY)")
    p.add_argument("--auto", action="store_true", help="Automatically restore the next best available account")
    args = p.parse_args()

    perform_restore(args)

if __name__ == "__main__":
    main()
