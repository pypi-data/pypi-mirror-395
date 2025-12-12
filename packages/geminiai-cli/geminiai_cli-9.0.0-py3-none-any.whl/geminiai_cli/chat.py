import os
import shutil
import subprocess

from .ui import cprint
from .config import NEON_GREEN, NEON_RED, NEON_YELLOW, NEON_CYAN, RESET

def backup_chat_history(backup_path: str, gemini_home_dir: str):
    """Backup the chat history from the current user's Gemini directory."""
    source_path = os.path.join(gemini_home_dir, "tmp")

    if not os.path.exists(source_path):
        cprint(NEON_RED, "Gemini chat history directory not found.")
        return

    backup_dir = os.path.join(backup_path, "tmp")
    os.makedirs(backup_dir, exist_ok=True)

    try:
        for item in os.listdir(source_path):
            item_path = os.path.join(source_path, item)
            dest_path = os.path.join(backup_dir, item)
            if os.path.islink(item_path) or os.path.isfile(item_path):
                shutil.copy(item_path, dest_path)
            elif os.path.isdir(item_path):
                shutil.copytree(item_path, dest_path, dirs_exist_ok=True)
        cprint(NEON_GREEN, f"Chat history successfully backed up to {backup_dir}")
    except Exception as e:
        cprint(NEON_RED, f"Failed to backup chat history: {e}")


def restore_chat_history(backup_path: str, gemini_home_dir: str):
    """Restore the chat history to the current user's Gemini directory."""
    destination_path = os.path.join(gemini_home_dir, "tmp")
    backup_dir = os.path.join(backup_path, "tmp")

    if not os.path.exists(backup_dir):
        cprint(NEON_RED, "Chat history backup directory not found.")
        return

    os.makedirs(destination_path, exist_ok=True)

    try:
        for item in os.listdir(backup_dir):
            item_path = os.path.join(backup_dir, item)
            dest_path = os.path.join(destination_path, item)
            if os.path.islink(item_path) or os.path.isfile(item_path):
                shutil.copy(item_path, dest_path)
            elif os.path.isdir(item_path):
                shutil.copytree(item_path, dest_path, dirs_exist_ok=True)
        cprint(NEON_GREEN, "Chat history successfully restored.")
    except Exception as e:
        cprint(NEON_RED, f"Failed to restore chat history: {e}")


def cleanup_chat_history(dry_run: bool, force: bool, gemini_home_dir: str):
    """Clear temporary chat history and logs."""
    target_dir = os.path.join(gemini_home_dir, "tmp")
    
    if not os.path.exists(target_dir):
        cprint(NEON_YELLOW, f"[INFO] Nothing to clean. Directory not found: {target_dir}")
        return

    # Get list of items to be removed (excluding 'bin')
    try:
        all_items = os.listdir(target_dir)
    except Exception as e:
        cprint(NEON_RED, f"[ERROR] Could not list directory {target_dir}: {e}")
        return

    items_to_remove = [item for item in all_items if item != "bin"]

    if not items_to_remove:
        cprint(NEON_GREEN, "[OK] Directory is already clean (only preserved items remain).")
        return

    cprint(NEON_CYAN, f"Found {len(items_to_remove)} items to clean in {target_dir}")
    
    if not force and not dry_run:
        choice = input(f"{NEON_YELLOW}Are you sure you want to proceed? (y/N): ").strip().lower()
        if choice != 'y':
            cprint(NEON_CYAN, "Cleanup cancelled.")
            return

    cprint(NEON_YELLOW, f"[INFO] Cleaning up...")
    
    cleaned_count = 0
    
    for item in items_to_remove:
        item_path = os.path.join(target_dir, item)
        
        if dry_run:
            cprint(NEON_YELLOW, f"[DRY-RUN] Would delete: {item}")
            cleaned_count += 1
            continue
        
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
                cleaned_count += 1
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                cleaned_count += 1
        except Exception as e:
            cprint(NEON_RED, f"[ERROR] Failed to delete {item}: {e}")

    if dry_run:
        cprint(NEON_GREEN, f"[OK] Cleanup dry run finished. Would remove {cleaned_count} items.")
    else:
        cprint(NEON_GREEN, f"[OK] Cleanup finished. Removed {cleaned_count} items.")


def resume_chat():
    """Resume the last chat session."""
    try:
        subprocess.run(["gemini", "--model", "pro", "--resume"])
    except FileNotFoundError:
        cprint(NEON_RED, "The 'gemini' command was not found. Make sure it is in your PATH.")
    except Exception as e:
        cprint(NEON_RED, f"Failed to resume chat: {e}")
