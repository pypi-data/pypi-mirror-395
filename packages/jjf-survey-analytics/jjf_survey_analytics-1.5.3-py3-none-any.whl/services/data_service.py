#!/usr/bin/env python3
"""
DataService - Thread-safe in-memory data storage service.

Replaces global SHEET_DATA dictionary with proper service abstraction.
Integrates with SheetRepository for Google Sheets data extraction.
"""

import copy
import threading
from datetime import datetime
from typing import Any, Dict, List, Optional


class DataService:
    """
    Thread-safe data service for Google Sheets data.

    Manages in-memory storage of tab data with proper synchronization
    and integration with SheetRepository for data extraction.
    """

    def __init__(self, sheet_repository=None):
        """
        Initialize data service with optional repository injection.

        Args:
            sheet_repository: Optional SheetRepository instance (uses singleton if None)
        """
        # Import here to avoid circular dependency
        from src.repositories import get_sheet_repository

        self._sheet_repository = sheet_repository or get_sheet_repository()
        self._data: Dict[str, List[Dict[str, Any]]] = {}
        self._lock = threading.Lock()
        self._metadata: Dict[str, Any] = {
            "loaded_at": None,
            "tab_count": 0,
            "total_rows": 0,
            "load_count": 0,
        }

    def load_data(
        self, verbose: bool = False, use_cache: bool = True, force_refresh: bool = False
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Load data from Google Sheets into memory.

        Args:
            verbose: Enable verbose logging
            use_cache: Use local file cache
            force_refresh: Force refresh even if cache is valid

        Returns:
            Dictionary mapping tab names to row data
        """
        with self._lock:
            # Use repository instead of direct SheetsReader
            effective_use_cache = use_cache and not force_refresh
            self._data = self._sheet_repository.fetch_all_tabs(
                verbose=verbose, use_cache=effective_use_cache
            )

            # Update metadata
            self._metadata["loaded_at"] = datetime.now().isoformat()
            self._metadata["tab_count"] = len(self._data)
            self._metadata["total_rows"] = sum(len(rows) for rows in self._data.values())
            self._metadata["load_count"] += 1

            return self._data.copy()

    def get_tab_data(self, tab_name: str) -> List[Dict[str, Any]]:
        """
        Get data for a specific tab.

        Args:
            tab_name: Name of tab to retrieve

        Returns:
            List of row dictionaries for the tab (empty list if not found)
        """
        with self._lock:
            return copy.deepcopy(self._data.get(tab_name, []))

    def get_all_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all loaded tab data.

        Returns:
            Dictionary mapping tab names to row data
        """
        with self._lock:
            return copy.deepcopy(self._data)

    def has_data(self) -> bool:
        """
        Check if any data is loaded.

        Returns:
            True if data loaded, False otherwise
        """
        with self._lock:
            return len(self._data) > 0

    def has_tab(self, tab_name: str) -> bool:
        """
        Check if specific tab data is loaded.

        Args:
            tab_name: Name of tab to check

        Returns:
            True if tab exists, False otherwise
        """
        with self._lock:
            return tab_name in self._data

    def get_tab_names(self) -> List[str]:
        """
        Get list of all loaded tab names.

        Returns:
            List of tab names
        """
        with self._lock:
            return list(self._data.keys())

    def get_row_count(self, tab_name: str) -> int:
        """
        Get number of rows in a specific tab.

        Args:
            tab_name: Name of tab

        Returns:
            Number of rows (0 if tab not found)
        """
        with self._lock:
            return len(self._data.get(tab_name, []))

    def get_total_row_count(self) -> int:
        """
        Get total number of rows across all tabs.

        Returns:
            Total row count
        """
        with self._lock:
            return sum(len(rows) for rows in self._data.values())

    def get_org_response_count(self, org_name: str) -> int:
        """
        Count responses for a specific organization across CEO, Tech, and Staff tabs.

        Args:
            org_name: Name of organization

        Returns:
            Total number of responses for the organization
        """
        with self._lock:
            # Define field name mapping per tab
            org_field_map = {
                "CEO": "CEO Organization",
                "Tech": "Organization",
                "Staff": "Organization",
            }

            count = 0

            # Count CEO responses
            for row in self._data.get("CEO", []):
                if row.get(org_field_map["CEO"]) == org_name:
                    count += 1

            # Count Tech responses
            for row in self._data.get("Tech", []):
                if row.get(org_field_map["Tech"]) == org_name:
                    count += 1

            # Count Staff responses
            for row in self._data.get("Staff", []):
                if row.get(org_field_map["Staff"]) == org_name:
                    count += 1

            return count

    def get_all_org_names(self) -> List[str]:
        """
        Get list of all unique organization names from CEO, Tech, and Staff tabs.

        Returns:
            Sorted list of unique organization names
        """
        with self._lock:
            # Define field name mapping per tab
            org_field_map = {
                "CEO": "CEO Organization",
                "Tech": "Organization",
                "Staff": "Organization",
            }

            orgs = set()

            # Collect from CEO tab
            for row in self._data.get("CEO", []):
                org_name = row.get(org_field_map["CEO"])
                if org_name:
                    orgs.add(org_name)

            # Collect from Tech tab
            for row in self._data.get("Tech", []):
                org_name = row.get(org_field_map["Tech"])
                if org_name:
                    orgs.add(org_name)

            # Collect from Staff tab
            for row in self._data.get("Staff", []):
                org_name = row.get(org_field_map["Staff"])
                if org_name:
                    orgs.add(org_name)

            return sorted(list(orgs))

    def clear_data(self) -> None:
        """Clear all loaded data."""
        with self._lock:
            self._data.clear()
            self._metadata["tab_count"] = 0
            self._metadata["total_rows"] = 0
            self._metadata["cleared_at"] = datetime.now().isoformat()

    def refresh_data(self, verbose: bool = False) -> Dict[str, List[Dict[str, Any]]]:
        """
        Force refresh data from Google Sheets.

        Args:
            verbose: Enable verbose logging

        Returns:
            Refreshed data dictionary
        """
        return self.load_data(verbose=verbose, use_cache=False, force_refresh=True)

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get data service metadata and statistics.

        Returns:
            Dictionary containing metadata about loaded data
        """
        with self._lock:
            return {
                "has_data": len(self._data) > 0,
                "tab_count": len(self._data),
                "total_rows": sum(len(rows) for rows in self._data.values()),
                "loaded_at": self._metadata["loaded_at"],
                "load_count": self._metadata["load_count"],
                "tab_names": list(self._data.keys()),
                "tab_row_counts": {tab: len(rows) for tab, rows in self._data.items()},
            }


# Global singleton instance
_data_service_instance: Optional[DataService] = None
_instance_lock = threading.Lock()


def get_data_service(sheet_repository=None) -> DataService:
    """
    Get singleton data service instance.

    Args:
        sheet_repository: Optional SheetRepository instance (only used on first call)

    Returns:
        Singleton DataService instance
    """
    global _data_service_instance

    if _data_service_instance is None:
        with _instance_lock:
            if _data_service_instance is None:
                _data_service_instance = DataService(sheet_repository)

    return _data_service_instance
