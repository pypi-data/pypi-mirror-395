#!/usr/bin/env python3
# src/geminiai_cli/sync.py

"""
sync.py - Synchronize backups between local storage and Cloud (B2).

Features:
- cloud-sync: Upload local backups that are missing in the cloud.
- local-sync: Download cloud backups that are missing locally.
"""
import os
import sys
import argparse
from .ui import cprint, NEON_GREEN, NEON_CYAN, NEON_YELLOW, NEON_RED, NEON_MAGENTA
from .b2 import B2Manager
from .settings import get_setting
from .credentials import resolve_credentials

def get_local_backups(backup_dir):
    """Returns a set of local backup filenames (only .tar.gz)."""
    if not os.path.isdir(backup_dir):
        cprint(NEON_RED, f"[ERROR] Local backup directory not found: {backup_dir}")
        sys.exit(1)
    
    files = {
        f for f in os.listdir(backup_dir)
        if os.path.isfile(os.path.join(backup_dir, f)) and f.endswith(".gemini.tar.gz")
    }
    return files

def get_cloud_backups(b2):
    """Returns a set of cloud backup filenames."""
    cloud_files = set()
    try:
        for file_version, _ in b2.list_backups():
            if file_version.file_name.endswith(".gemini.tar.gz"):
                cloud_files.add(file_version.file_name)
    except Exception as e:
        cprint(NEON_RED, f"[ERROR] Failed to list cloud backups: {e}")
        sys.exit(1)
    return cloud_files

def cloud_sync(args):
    """Syncs local backups to the cloud (upload missing)."""
    key_id, app_key, bucket_name = resolve_credentials(args)
    backup_dir = os.path.abspath(os.path.expanduser(args.backup_dir))

    cprint(NEON_MAGENTA, f"Starting Cloud Sync (Local -> B2: {bucket_name})...")
    
    b2 = B2Manager(key_id, app_key, bucket_name)
    
    cprint(NEON_CYAN, "Analyzing differences...")
    local_files = get_local_backups(backup_dir)
    cloud_files = get_cloud_backups(b2)

    missing_in_cloud = local_files - cloud_files

    if not missing_in_cloud:
        cprint(NEON_GREEN, "Cloud is already up-to-date with local backups.")
        return

    cprint(NEON_YELLOW, f"Found {len(missing_in_cloud)} files missing in cloud. Uploading...")

    for filename in sorted(missing_in_cloud):
        local_path = os.path.join(backup_dir, filename)
        b2.upload(local_path, remote_name=filename)

    cprint(NEON_GREEN, "Cloud Sync Completed Successfully!")

def local_sync(args):
    """Syncs cloud backups to local storage (download missing)."""
    key_id, app_key, bucket_name = resolve_credentials(args)
    backup_dir = os.path.abspath(os.path.expanduser(args.backup_dir))

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    cprint(NEON_MAGENTA, f"Starting Local Sync (B2: {bucket_name} -> Local)...")
    
    b2 = B2Manager(key_id, app_key, bucket_name)
    
    cprint(NEON_CYAN, "Analyzing differences...")
    local_files = get_local_backups(backup_dir)
    cloud_files = get_cloud_backups(b2)

    missing_locally = cloud_files - local_files

    if not missing_locally:
        cprint(NEON_GREEN, "Local storage is already up-to-date with cloud backups.")
        return

    cprint(NEON_YELLOW, f"Found {len(missing_locally)} files missing locally. Downloading...")

    for filename in sorted(missing_locally):
        local_path = os.path.join(backup_dir, filename)
        b2.download(remote_name=filename, local_path=local_path)

    cprint(NEON_GREEN, "Local Sync Completed Successfully!")
