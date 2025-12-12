#!/usr/bin/env python3
"""
AdminEditRepository - Repository for admin edits JSON file persistence.

Abstracts admin edits JSON file storage from business logic services.
Provides thread-safe file I/O with backup management.
"""

import copy
import glob
import json
import os
import threading
from datetime import datetime
from typing import Any, Dict, List, Optional


class AdminEditRepository:
    """
    Repository for admin edits JSON file persistence.

    Manages JSON file storage for admin edits with:
    - Thread-safe file operations
    - Automatic backup before saves
    - Backup rotation (keep last 10)
    - Deep copy isolation
    """

    DEFAULT_EDITS_FILE = "admin_edits.json"
    MAX_BACKUPS = 10

    def __init__(self, edits_file: str = DEFAULT_EDITS_FILE):
        """
        Initialize admin edit repository.

        Args:
            edits_file: Path to admin edits JSON file
        """
        self._edits_file = edits_file
        self._lock = threading.RLock()
        self._metadata: Dict[str, Any] = {
            "created_at": datetime.now().isoformat(),
            "save_count": 0,
            "load_count": 0,
        }

    def load_all_edits(self) -> Dict[str, Any]:
        """
        Load all admin edits from JSON file.

        Returns:
            Dictionary of all admin edits (empty dict if file not found)
        """
        with self._lock:
            try:
                if not os.path.exists(self._edits_file):
                    return {}

                with open(self._edits_file, "r", encoding="utf-8") as f:
                    edits = json.load(f)

                self._metadata["load_count"] += 1
                return copy.deepcopy(edits)

            except (json.JSONDecodeError, IOError) as e:
                print(f"[AdminEditRepository] Error loading edits: {e}")
                return {}

    def save_all_edits(self, edits: Dict[str, Any]) -> bool:
        """
        Save all admin edits to JSON file.

        Automatically creates backup before saving.

        Args:
            edits: Dictionary of all admin edits

        Returns:
            True if save successful, False otherwise
        """
        with self._lock:
            try:
                # Create backup before saving
                if os.path.exists(self._edits_file):
                    self.create_backup()

                # Ensure directory exists
                os.makedirs(os.path.dirname(self._edits_file) or ".", exist_ok=True)

                # Save edits
                with open(self._edits_file, "w", encoding="utf-8") as f:
                    json.dump(edits, f, indent=2, ensure_ascii=False)

                self._metadata["save_count"] += 1

                # Rotate backups
                self._rotate_backups()

                return True

            except (IOError, OSError, TypeError) as e:
                print(f"[AdminEditRepository] Error saving edits: {e}")
                return False

    def get_org_edits(self, org_name: str) -> Optional[Dict[str, Any]]:
        """
        Get admin edits for a specific organization.

        Args:
            org_name: Name of organization

        Returns:
            Dictionary containing edits for the organization, or None if not found
        """
        with self._lock:
            all_edits = self.load_all_edits()
            org_edits = all_edits.get(org_name)

            if org_edits is None:
                return None

            return copy.deepcopy(org_edits)

    def save_org_edits(self, org_name: str, edits: Dict[str, Any]) -> bool:
        """
        Save admin edits for a specific organization.

        Args:
            org_name: Name of organization
            edits: Dictionary of edits to save

        Returns:
            True if save successful, False otherwise
        """
        with self._lock:
            all_edits = self.load_all_edits()
            all_edits[org_name] = copy.deepcopy(edits)
            return self.save_all_edits(all_edits)

    def delete_org_edits(self, org_name: str) -> bool:
        """
        Delete all edits for a specific organization.

        Args:
            org_name: Name of organization

        Returns:
            True if delete successful, False otherwise
        """
        with self._lock:
            all_edits = self.load_all_edits()

            if org_name not in all_edits:
                return False

            del all_edits[org_name]
            return self.save_all_edits(all_edits)

    def get_edited_orgs(self) -> List[str]:
        """
        Get list of organizations with edits.

        Returns:
            Sorted list of organization names with edits
        """
        with self._lock:
            all_edits = self.load_all_edits()
            return sorted(list(all_edits.keys()))

    def has_edits(self, org_name: str) -> bool:
        """
        Check if organization has any edits.

        Args:
            org_name: Name of organization

        Returns:
            True if organization has edits, False otherwise
        """
        with self._lock:
            all_edits = self.load_all_edits()
            return org_name in all_edits

    def clear_all_edits(self) -> bool:
        """
        Clear all admin edits.

        Returns:
            True if save successful, False otherwise
        """
        with self._lock:
            return self.save_all_edits({})

    def create_backup(self) -> str:
        """
        Create backup of current admin edits file.

        Returns:
            Path to backup file, or empty string if backup failed
        """
        with self._lock:
            try:
                if not os.path.exists(self._edits_file):
                    return ""

                # Generate backup filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                base_name = os.path.splitext(self._edits_file)[0]
                backup_file = f"{base_name}_backup_{timestamp}.json"

                # Copy current file to backup
                with open(self._edits_file, "r", encoding="utf-8") as src:
                    content = src.read()

                with open(backup_file, "w", encoding="utf-8") as dst:
                    dst.write(content)

                return backup_file

            except (IOError, OSError) as e:
                print(f"[AdminEditRepository] Error creating backup: {e}")
                return ""

    def restore_from_backup(self, backup_filename: str) -> bool:
        """
        Restore admin edits from backup file.

        Args:
            backup_filename: Name of backup file to restore from

        Returns:
            True if restore successful, False otherwise
        """
        with self._lock:
            try:
                if not os.path.exists(backup_filename):
                    print(f"[AdminEditRepository] Backup file not found: {backup_filename}")
                    return False

                # Validate backup file is valid JSON
                with open(backup_filename, "r", encoding="utf-8") as f:
                    backup_data = json.load(f)

                # Save current file as backup before restore
                if os.path.exists(self._edits_file):
                    self.create_backup()

                # Restore from backup
                return self.save_all_edits(backup_data)

            except (IOError, json.JSONDecodeError) as e:
                print(f"[AdminEditRepository] Error restoring from backup: {e}")
                return False

    def _rotate_backups(self) -> None:
        """Rotate backups, keeping only the most recent MAX_BACKUPS files."""
        try:
            base_name = os.path.splitext(self._edits_file)[0]
            backup_pattern = f"{base_name}_backup_*.json"
            backup_files = sorted(glob.glob(backup_pattern), reverse=True)

            # Delete old backups beyond MAX_BACKUPS
            for old_backup in backup_files[self.MAX_BACKUPS :]:
                try:
                    os.remove(old_backup)
                except OSError:
                    pass

        except Exception as e:
            print(f"[AdminEditRepository] Error rotating backups: {e}")

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get repository metadata and statistics.

        Returns:
            Dictionary containing metadata
        """
        with self._lock:
            all_edits = self.load_all_edits()
            org_count = len(all_edits)

            # Get file metadata
            file_exists = os.path.exists(self._edits_file)
            file_size = 0
            modified_at = None

            if file_exists:
                stat = os.stat(self._edits_file)
                file_size = stat.st_size
                modified_at = datetime.fromtimestamp(stat.st_mtime).isoformat()

            # Count backups
            base_name = os.path.splitext(self._edits_file)[0]
            backup_pattern = f"{base_name}_backup_*.json"
            backup_count = len(glob.glob(backup_pattern))

            return {
                "edits_file": self._edits_file,
                "file_exists": file_exists,
                "file_size_bytes": file_size,
                "file_size_kb": round(file_size / 1024, 2) if file_size > 0 else 0,
                "modified_at": modified_at,
                "created_at": self._metadata["created_at"],
                "save_count": self._metadata["save_count"],
                "load_count": self._metadata["load_count"],
                "org_count": org_count,
                "backup_count": backup_count,
                "edited_orgs": sorted(list(all_edits.keys())),
            }


# Global singleton instance
_admin_edit_repository_instance: Optional[AdminEditRepository] = None
_instance_lock = threading.RLock()


def get_admin_edit_repository(
    edits_file: str = AdminEditRepository.DEFAULT_EDITS_FILE,
) -> AdminEditRepository:
    """
    Get singleton admin edit repository instance.

    Args:
        edits_file: Path to edits JSON file (only used on first call)

    Returns:
        Singleton AdminEditRepository instance
    """
    global _admin_edit_repository_instance

    if _admin_edit_repository_instance is None:
        with _instance_lock:
            if _admin_edit_repository_instance is None:
                _admin_edit_repository_instance = AdminEditRepository(edits_file)

    return _admin_edit_repository_instance
