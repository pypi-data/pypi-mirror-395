#!/usr/bin/env python3
"""
SheetRepository - Repository for Google Sheets data access.

Abstracts Google Sheets data persistence from business logic services.
Provides thread-safe caching and integration with SheetsReader.
"""

import copy
import threading
from datetime import datetime
from typing import Any, Dict, List, Optional

from src.extractors.sheets_reader import SheetsReader


class SheetRepository:
    """
    Repository for Google Sheets data access.

    Provides abstraction layer over SheetsReader with:
    - Thread-safe data access
    - In-memory caching with deep copy isolation
    - Tab-level data retrieval
    - Metadata tracking
    - Singleton pattern
    """

    def __init__(self):
        """Initialize sheet repository with empty cache and thread lock."""
        self._data: Dict[str, List[Dict[str, Any]]] = {}
        self._lock = threading.RLock()
        self._metadata: Dict[str, Any] = {
            "last_fetch": None,
            "total_rows": 0,
            "tab_count": 0,
            "fetch_count": 0,
        }

    def fetch_all_tabs(
        self, verbose: bool = True, use_cache: bool = True
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetch all tab data from Google Sheets.

        Args:
            verbose: Enable verbose logging
            use_cache: Use SheetsReader cache when available

        Returns:
            Dictionary mapping tab names to row data
        """
        with self._lock:
            # Fetch from Google Sheets via SheetsReader
            raw_data = SheetsReader.fetch_all_tabs(
                verbose=verbose, use_cache=use_cache, force_refresh=not use_cache
            )

            # Remove metadata from raw data
            self._data = {tab: rows for tab, rows in raw_data.items() if tab != "_metadata"}

            # Update metadata
            self._metadata["last_fetch"] = datetime.now().isoformat()
            self._metadata["tab_count"] = len(self._data)
            self._metadata["total_rows"] = sum(len(rows) for rows in self._data.values())
            self._metadata["fetch_count"] += 1

            return copy.deepcopy(self._data)

    def get_tab(self, tab_name: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get data for a specific tab.

        Args:
            tab_name: Name of tab to retrieve

        Returns:
            List of row dictionaries for the tab, or None if not found
        """
        with self._lock:
            if tab_name not in self._data:
                return None
            return copy.deepcopy(self._data[tab_name])

    def get_all_tabs(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all loaded tab data.

        Returns:
            Dictionary mapping tab names to row data
        """
        with self._lock:
            return copy.deepcopy(self._data)

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

    def clear_cache(self) -> None:
        """Clear in-memory cache."""
        with self._lock:
            self._data.clear()
            self._metadata["tab_count"] = 0
            self._metadata["total_rows"] = 0

    def refresh(self, verbose: bool = True) -> Dict[str, List[Dict[str, Any]]]:
        """
        Force refresh data from Google Sheets.

        Args:
            verbose: Enable verbose logging

        Returns:
            Refreshed data dictionary
        """
        return self.fetch_all_tabs(verbose=verbose, use_cache=False)

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get repository metadata and statistics.

        Returns:
            Dictionary containing metadata about loaded data
        """
        with self._lock:
            return {
                "last_fetch": self._metadata["last_fetch"],
                "tab_count": len(self._data),
                "total_rows": sum(len(rows) for rows in self._data.values()),
                "fetch_count": self._metadata["fetch_count"],
                "tab_names": list(self._data.keys()),
                "tab_row_counts": {tab: len(rows) for tab, rows in self._data.items()},
            }


# Global singleton instance
_sheet_repository_instance: Optional[SheetRepository] = None
_instance_lock = threading.RLock()


def get_sheet_repository() -> SheetRepository:
    """
    Get singleton sheet repository instance.

    Returns:
        Singleton SheetRepository instance
    """
    global _sheet_repository_instance

    if _sheet_repository_instance is None:
        with _instance_lock:
            if _sheet_repository_instance is None:
                _sheet_repository_instance = SheetRepository()

    return _sheet_repository_instance
