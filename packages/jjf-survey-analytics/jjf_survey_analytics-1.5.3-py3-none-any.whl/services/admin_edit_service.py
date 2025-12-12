#!/usr/bin/env python3
"""
AdminEditService - Thread-safe admin edits management service.

Replaces global ADMIN_EDITS dictionary with proper service abstraction.
Handles persistence via AdminEditRepository and provides admin edit operations.
"""

import copy
import threading
from datetime import datetime
from typing import Any, Dict, List, Optional


class AdminEditService:
    """
    Thread-safe service for managing admin edits to organization reports.

    Admin edits allow manual customization of:
    - Summary title and body text
    - Score modifiers per dimension
    - Dimension-specific insights

    All edits are persisted via AdminEditRepository and affect report generation.
    """

    DEFAULT_EDITS_FILE = "admin_edits.json"

    def __init__(self, admin_edit_repository=None, edits_file: str = DEFAULT_EDITS_FILE):
        """
        Initialize admin edit service with optional repository injection.

        Args:
            admin_edit_repository: Optional AdminEditRepository instance (uses singleton if None)
            edits_file: Path to JSON file for persistence (only used if repository is None)
        """
        # Import here to avoid circular dependency
        from src.repositories import get_admin_edit_repository

        self._admin_edit_repository = admin_edit_repository or get_admin_edit_repository(edits_file)
        self._edits: Dict[str, Any] = {}
        self._lock = threading.Lock()
        self._metadata: Dict[str, Any] = {
            "loaded_at": None,
            "saved_at": None,
            "org_count": 0,
            "save_count": 0,
        }

    def load_edits(self) -> Dict[str, Any]:
        """
        Load admin edits from repository.

        Returns:
            Dictionary of all admin edits
        """
        with self._lock:
            # Load from repository
            self._edits = self._admin_edit_repository.load_all_edits()

            # Update metadata
            self._metadata["loaded_at"] = datetime.now().isoformat()
            self._metadata["org_count"] = len(self._edits)

            if self._edits:
                print(f"[Admin Edits] Loaded {len(self._edits)} edit records")
            else:
                print("[Admin Edits] No existing edits found, starting fresh")

            return copy.deepcopy(self._edits)

    def save_edits(self) -> bool:
        """
        Save admin edits to repository.

        Returns:
            True if save successful, False otherwise
        """
        with self._lock:
            # Save to repository
            success = self._admin_edit_repository.save_all_edits(self._edits)

            if success:
                self._metadata["saved_at"] = datetime.now().isoformat()
                self._metadata["save_count"] += 1
                print(f"[Admin Edits] Saved {len(self._edits)} edit records")
            else:
                print("[Admin Edits] Error saving edits")

            return success

    def get_org_edits(self, org_name: str) -> Dict[str, Any]:
        """
        Get admin edits for a specific organization.

        Args:
            org_name: Name of organization

        Returns:
            Dictionary containing edits for the organization with default structure
        """
        with self._lock:
            return copy.deepcopy(
                self._edits.get(
                    org_name,
                    {
                        "summary_title": None,
                        "summary_body": None,
                        "score_modifiers": {},
                        "dimension_insights": {},
                    },
                )
            )

    def save_org_edits(self, org_name: str, edits: Dict[str, Any]) -> bool:
        """
        Save admin edits for a specific organization.

        Args:
            org_name: Name of organization
            edits: Dictionary of edits to save/update

        Returns:
            True if save successful, False otherwise
        """
        with self._lock:
            # Initialize org edits if not exists
            if org_name not in self._edits:
                self._edits[org_name] = {
                    "summary_title": None,
                    "summary_body": None,
                    "score_modifiers": {},
                    "dimension_insights": {},
                }

            # Update the edits
            self._edits[org_name].update(edits)
            self._metadata["org_count"] = len(self._edits)

        # Save to file (releases lock before I/O)
        return self.save_edits()

    def update_summary(
        self, org_name: str, title: Optional[str] = None, body: Optional[str] = None
    ) -> bool:
        """
        Update summary title and/or body for an organization.

        Args:
            org_name: Name of organization
            title: New summary title (None to keep existing)
            body: New summary body (None to keep existing)

        Returns:
            True if save successful, False otherwise
        """
        edits = {}
        if title is not None:
            edits["summary_title"] = title
        if body is not None:
            edits["summary_body"] = body

        return self.save_org_edits(org_name, edits)

    def update_score_modifiers(
        self, org_name: str, dimension: str, modifiers: List[Dict[str, Any]]
    ) -> bool:
        """
        Update score modifiers for a specific dimension.

        Args:
            org_name: Name of organization
            dimension: Dimension name (e.g., 'Program Technology')
            modifiers: List of modifier objects with 'id' and 'value' keys
                      Example: [{"id": 0, "value": -1}, {"id": 1, "value": 0.5}]

        Returns:
            True if save successful, False otherwise
        """
        # Get current edits
        current_edits = self.get_org_edits(org_name)

        # Ensure score_modifiers dict exists
        if "score_modifiers" not in current_edits:
            current_edits["score_modifiers"] = {}

        # Update modifiers for this dimension
        current_edits["score_modifiers"][dimension] = modifiers

        # Save updated edits
        return self.save_org_edits(org_name, current_edits)

    def update_dimension_insight(self, org_name: str, dimension: str, insight: str) -> bool:
        """
        Update qualitative insight for a specific dimension.

        Args:
            org_name: Name of organization
            dimension: Dimension name
            insight: Qualitative insight text

        Returns:
            True if save successful, False otherwise
        """
        # Get current edits
        current_edits = self.get_org_edits(org_name)

        # Ensure dimension_insights dict exists
        if "dimension_insights" not in current_edits:
            current_edits["dimension_insights"] = {}

        # Update insight for this dimension
        current_edits["dimension_insights"][dimension] = insight

        # Save updated edits
        return self.save_org_edits(org_name, current_edits)

    def delete_org_edits(self, org_name: str) -> bool:
        """
        Delete all edits for a specific organization.

        Args:
            org_name: Name of organization

        Returns:
            True if delete successful, False otherwise
        """
        with self._lock:
            if org_name in self._edits:
                del self._edits[org_name]
                self._metadata["org_count"] = len(self._edits)

        return self.save_edits()

    def get_all_edits(self) -> Dict[str, Any]:
        """
        Get all admin edits for all organizations.

        Returns:
            Dictionary mapping org names to their edits
        """
        with self._lock:
            return copy.deepcopy(self._edits)

    def has_edits(self, org_name: str) -> bool:
        """
        Check if organization has any edits.

        Args:
            org_name: Name of organization

        Returns:
            True if organization has edits, False otherwise
        """
        with self._lock:
            return org_name in self._edits

    def get_edited_orgs(self) -> list[str]:
        """
        Get list of organizations with edits.

        Returns:
            Sorted list of organization names with edits
        """
        with self._lock:
            return sorted(list(self._edits.keys()))

    def clear_all_edits(self) -> bool:
        """
        Clear all admin edits.

        Returns:
            True if save successful, False otherwise
        """
        with self._lock:
            self._edits.clear()
            self._metadata["org_count"] = 0

        return self.save_edits()

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get service metadata and statistics.

        Returns:
            Dictionary containing metadata
        """
        with self._lock:
            # Get repository metadata
            repo_metadata = self._admin_edit_repository.get_metadata()

            return {
                "edits_file": repo_metadata.get("edits_file", "unknown"),
                "org_count": len(self._edits),
                "loaded_at": self._metadata["loaded_at"],
                "saved_at": self._metadata["saved_at"],
                "save_count": self._metadata["save_count"],
                "edited_orgs": sorted(list(self._edits.keys())),
                "repository_metadata": repo_metadata,
            }


# Global singleton instance
_admin_edit_service_instance: Optional[AdminEditService] = None
_instance_lock = threading.Lock()


def get_admin_edit_service(
    admin_edit_repository=None, edits_file: str = AdminEditService.DEFAULT_EDITS_FILE
) -> AdminEditService:
    """
    Get singleton admin edit service instance.

    Args:
        admin_edit_repository: Optional AdminEditRepository instance (only used on first call)
        edits_file: Path to edits JSON file (only used on first call if repository is None)

    Returns:
        Singleton AdminEditService instance
    """
    global _admin_edit_service_instance

    if _admin_edit_service_instance is None:
        with _instance_lock:
            if _admin_edit_service_instance is None:
                _admin_edit_service_instance = AdminEditService(admin_edit_repository, edits_file)

    return _admin_edit_service_instance
