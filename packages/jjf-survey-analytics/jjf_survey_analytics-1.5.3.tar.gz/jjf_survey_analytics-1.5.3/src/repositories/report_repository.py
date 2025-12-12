#!/usr/bin/env python3
"""
ReportRepository - Repository for report JSON file persistence.

Abstracts JSON file storage for organization and aggregate reports.
Provides thread-safe file I/O with metadata tracking.
"""

import copy
import json
import os
import threading
from datetime import datetime
from typing import Any, Dict, List, Optional


class ReportRepository:
    """
    Repository for report JSON file persistence.

    Manages JSON file storage for:
    - Organization reports: reports_json/organizations/{org_name}.json
    - Aggregate report: reports_json/aggregate/aggregate_report.json

    Provides thread-safe file operations with deep copy isolation.
    """

    # Directory structure
    REPORTS_BASE_DIR = "reports_json"
    ORG_REPORTS_DIR = os.path.join(REPORTS_BASE_DIR, "organizations")
    AGGREGATE_REPORTS_DIR = os.path.join(REPORTS_BASE_DIR, "aggregate")
    AGGREGATE_REPORT_FILENAME = "aggregate_report.json"

    def __init__(self):
        """Initialize report repository with thread lock."""
        self._lock = threading.RLock()
        self._metadata: Dict[str, Any] = {
            "created_at": datetime.now().isoformat(),
            "save_count": 0,
            "load_count": 0,
        }
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Ensure report directories exist."""
        os.makedirs(self.ORG_REPORTS_DIR, exist_ok=True)
        os.makedirs(self.AGGREGATE_REPORTS_DIR, exist_ok=True)

    def _get_org_report_path(self, org_name: str) -> str:
        """Get file path for organization report."""
        safe_name = org_name.replace("/", "_").replace("\\", "_")
        return os.path.join(self.ORG_REPORTS_DIR, f"{safe_name}.json")

    def _get_aggregate_report_path(self) -> str:
        """Get file path for aggregate report."""
        return os.path.join(self.AGGREGATE_REPORTS_DIR, self.AGGREGATE_REPORT_FILENAME)

    def save_org_report(self, org_name: str, report: Dict[str, Any]) -> bool:
        """
        Save organization report to JSON file.

        Args:
            org_name: Name of organization
            report: Report data to save

        Returns:
            True if save successful, False otherwise
        """
        with self._lock:
            try:
                file_path = self._get_org_report_path(org_name)
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)

                self._metadata["save_count"] += 1
                return True

            except (IOError, OSError, TypeError) as e:
                print(f"[ReportRepository] Error saving org report for {org_name}: {e}")
                return False

    def load_org_report(self, org_name: str) -> Optional[Dict[str, Any]]:
        """
        Load organization report from JSON file.

        Args:
            org_name: Name of organization

        Returns:
            Report data or None if not found
        """
        with self._lock:
            try:
                file_path = self._get_org_report_path(org_name)

                if not os.path.exists(file_path):
                    return None

                with open(file_path, "r", encoding="utf-8") as f:
                    report = json.load(f)

                self._metadata["load_count"] += 1
                return copy.deepcopy(report)

            except (IOError, json.JSONDecodeError) as e:
                print(f"[ReportRepository] Error loading org report for {org_name}: {e}")
                return None

    def exists_org_report(self, org_name: str) -> bool:
        """
        Check if organization report file exists.

        Args:
            org_name: Name of organization

        Returns:
            True if file exists, False otherwise
        """
        with self._lock:
            file_path = self._get_org_report_path(org_name)
            return os.path.exists(file_path)

    def delete_org_report(self, org_name: str) -> bool:
        """
        Delete organization report file.

        Args:
            org_name: Name of organization

        Returns:
            True if delete successful, False otherwise
        """
        with self._lock:
            try:
                file_path = self._get_org_report_path(org_name)

                if not os.path.exists(file_path):
                    return False

                os.remove(file_path)
                return True

            except (IOError, OSError) as e:
                print(f"[ReportRepository] Error deleting org report for {org_name}: {e}")
                return False

    def save_aggregate_report(self, report: Dict[str, Any]) -> bool:
        """
        Save aggregate report to JSON file.

        Args:
            report: Aggregate report data to save

        Returns:
            True if save successful, False otherwise
        """
        with self._lock:
            try:
                file_path = self._get_aggregate_report_path()
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)

                self._metadata["save_count"] += 1
                return True

            except (IOError, OSError, TypeError) as e:
                print(f"[ReportRepository] Error saving aggregate report: {e}")
                return False

    def load_aggregate_report(self) -> Optional[Dict[str, Any]]:
        """
        Load aggregate report from JSON file.

        Returns:
            Aggregate report data or None if not found
        """
        with self._lock:
            try:
                file_path = self._get_aggregate_report_path()

                if not os.path.exists(file_path):
                    return None

                with open(file_path, "r", encoding="utf-8") as f:
                    report = json.load(f)

                self._metadata["load_count"] += 1
                return copy.deepcopy(report)

            except (IOError, json.JSONDecodeError) as e:
                print(f"[ReportRepository] Error loading aggregate report: {e}")
                return None

    def exists_aggregate_report(self) -> bool:
        """
        Check if aggregate report file exists.

        Returns:
            True if file exists, False otherwise
        """
        with self._lock:
            file_path = self._get_aggregate_report_path()
            return os.path.exists(file_path)

    def delete_aggregate_report(self) -> bool:
        """
        Delete aggregate report file.

        Returns:
            True if delete successful, False otherwise
        """
        with self._lock:
            try:
                file_path = self._get_aggregate_report_path()

                if not os.path.exists(file_path):
                    return False

                os.remove(file_path)
                return True

            except (IOError, OSError) as e:
                print(f"[ReportRepository] Error deleting aggregate report: {e}")
                return False

    def get_all_org_report_names(self) -> List[str]:
        """
        Get list of all organization names with saved reports.

        Returns:
            List of organization names (sorted)
        """
        with self._lock:
            try:
                if not os.path.exists(self.ORG_REPORTS_DIR):
                    return []

                org_names = []
                for filename in os.listdir(self.ORG_REPORTS_DIR):
                    if filename.endswith(".json"):
                        # Remove .json extension
                        org_name = filename[:-5]
                        org_names.append(org_name)

                return sorted(org_names)

            except (IOError, OSError) as e:
                print(f"[ReportRepository] Error listing org reports: {e}")
                return []

    def clear_all_org_reports(self) -> int:
        """
        Delete all organization report files.

        Returns:
            Number of files deleted
        """
        with self._lock:
            try:
                if not os.path.exists(self.ORG_REPORTS_DIR):
                    return 0

                count = 0
                for filename in os.listdir(self.ORG_REPORTS_DIR):
                    if filename.endswith(".json"):
                        file_path = os.path.join(self.ORG_REPORTS_DIR, filename)
                        os.remove(file_path)
                        count += 1

                return count

            except (IOError, OSError) as e:
                print(f"[ReportRepository] Error clearing org reports: {e}")
                return 0

    def get_report_metadata(self, org_name: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for organization report file.

        Args:
            org_name: Name of organization

        Returns:
            Metadata dictionary or None if file not found
        """
        with self._lock:
            try:
                file_path = self._get_org_report_path(org_name)

                if not os.path.exists(file_path):
                    return None

                stat = os.stat(file_path)
                return {
                    "org_name": org_name,
                    "file_path": file_path,
                    "file_size_bytes": stat.st_size,
                    "file_size_kb": round(stat.st_size / 1024, 2),
                    "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                }

            except (IOError, OSError) as e:
                print(f"[ReportRepository] Error getting metadata for {org_name}: {e}")
                return None

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get repository metadata and statistics.

        Returns:
            Dictionary containing metadata
        """
        with self._lock:
            org_count = len(self.get_all_org_report_names())
            aggregate_exists = self.exists_aggregate_report()

            return {
                "created_at": self._metadata["created_at"],
                "save_count": self._metadata["save_count"],
                "load_count": self._metadata["load_count"],
                "org_reports_count": org_count,
                "aggregate_report_exists": aggregate_exists,
                "org_reports_dir": self.ORG_REPORTS_DIR,
                "aggregate_reports_dir": self.AGGREGATE_REPORTS_DIR,
            }


# Global singleton instance
_report_repository_instance: Optional[ReportRepository] = None
_instance_lock = threading.RLock()


def get_report_repository() -> ReportRepository:
    """
    Get singleton report repository instance.

    Returns:
        Singleton ReportRepository instance
    """
    global _report_repository_instance

    if _report_repository_instance is None:
        with _instance_lock:
            if _report_repository_instance is None:
                _report_repository_instance = ReportRepository()

    return _report_repository_instance
