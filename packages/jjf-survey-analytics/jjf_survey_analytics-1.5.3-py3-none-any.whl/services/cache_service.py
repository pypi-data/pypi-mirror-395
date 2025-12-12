#!/usr/bin/env python3
"""
CacheService - Thread-safe in-memory cache for reports and data.

Replaces global REPORT_CACHE dictionary with proper service abstraction.
Prepared for integration with ReportRepository for persistence (Phase 5).
"""

import copy
import threading
from datetime import datetime
from typing import Any, Dict, Optional


class CacheService:
    """
    Thread-safe cache service for report data.

    Manages in-memory caching of organization and aggregate reports
    with proper synchronization and metadata tracking.

    Note: ReportRepository integration will be completed in Phase 5
    when ReportService is refactored.
    """

    def __init__(self, report_repository=None):
        """
        Initialize cache service with optional repository injection.

        Args:
            report_repository: Optional ReportRepository instance (prepared for Phase 5)
        """
        # Import here to avoid circular dependency
        from src.repositories import get_report_repository

        # Store repository for future Phase 5 integration
        self._report_repository = report_repository or get_report_repository()

        self._cache: Dict[str, Any] = {"org_reports": {}, "aggregate_report": None}
        self._lock = threading.Lock()
        self._metadata: Dict[str, Any] = {
            "created_at": datetime.now().isoformat(),
            "cache_hits": 0,
            "cache_misses": 0,
            "org_reports_count": 0,
            "aggregate_reports_count": 0,
        }

    def get_org_report(self, org_name: str) -> Optional[Dict[str, Any]]:
        """
        Get cached organization report.

        Args:
            org_name: Name of organization

        Returns:
            Cached report data or None if not cached
        """
        with self._lock:
            if org_name in self._cache["org_reports"]:
                self._metadata["cache_hits"] += 1
                return copy.deepcopy(self._cache["org_reports"][org_name])
            else:
                self._metadata["cache_misses"] += 1
                return None

    def set_org_report(
        self, org_name: str, report: Dict[str, Any], response_count: int = 0
    ) -> None:
        """
        Cache organization report.

        Args:
            org_name: Name of organization
            report: Report data to cache
            response_count: Number of responses included in report
        """
        with self._lock:
            self._cache["org_reports"][org_name] = {
                "report": report,
                "response_count": response_count,
                "cached_at": datetime.now().isoformat(),
            }
            self._metadata["org_reports_count"] = len(self._cache["org_reports"])

    def has_org_report(self, org_name: str) -> bool:
        """
        Check if organization report is cached.

        Args:
            org_name: Name of organization

        Returns:
            True if cached, False otherwise
        """
        with self._lock:
            return org_name in self._cache["org_reports"]

    def get_aggregate_report(self) -> Optional[Dict[str, Any]]:
        """
        Get cached aggregate report.

        Returns:
            Cached aggregate report or None if not cached
        """
        with self._lock:
            if self._cache["aggregate_report"]:
                self._metadata["cache_hits"] += 1
                return copy.deepcopy(self._cache["aggregate_report"])
            else:
                self._metadata["cache_misses"] += 1
                return None

    def set_aggregate_report(self, report: Dict[str, Any], total_responses: int = 0) -> None:
        """
        Cache aggregate report.

        Args:
            report: Aggregate report data to cache
            total_responses: Total number of responses across all organizations
        """
        with self._lock:
            self._cache["aggregate_report"] = {
                "report": report,
                "total_responses": total_responses,
                "cached_at": datetime.now().isoformat(),
            }
            self._metadata["aggregate_reports_count"] = 1

    def has_aggregate_report(self) -> bool:
        """
        Check if aggregate report is cached.

        Returns:
            True if cached, False otherwise
        """
        with self._lock:
            return self._cache["aggregate_report"] is not None

    def clear_org_report(self, org_name: str) -> bool:
        """
        Clear specific organization report from cache.

        Args:
            org_name: Name of organization

        Returns:
            True if report was cached and cleared, False if not found
        """
        with self._lock:
            if org_name in self._cache["org_reports"]:
                del self._cache["org_reports"][org_name]
                self._metadata["org_reports_count"] = len(self._cache["org_reports"])
                return True
            return False

    def clear_aggregate_report(self) -> bool:
        """
        Clear aggregate report from cache.

        Returns:
            True if report was cached and cleared, False if not found
        """
        with self._lock:
            if self._cache["aggregate_report"] is not None:
                self._cache["aggregate_report"] = None
                self._metadata["aggregate_reports_count"] = 0
                return True
            return False

    def clear_all(self) -> None:
        """Clear all cached reports."""
        with self._lock:
            self._cache["org_reports"].clear()
            self._cache["aggregate_report"] = None
            self._metadata["org_reports_count"] = 0
            self._metadata["aggregate_reports_count"] = 0
            self._metadata["cleared_at"] = datetime.now().isoformat()

    def get_status(self) -> Dict[str, Any]:
        """
        Get cache status and statistics.

        Returns:
            Dictionary containing cache statistics and metadata
        """
        with self._lock:
            return {
                "org_reports_count": len(self._cache["org_reports"]),
                "aggregate_report_cached": self._cache["aggregate_report"] is not None,
                "cache_hits": self._metadata["cache_hits"],
                "cache_misses": self._metadata["cache_misses"],
                "hit_rate": (
                    self._metadata["cache_hits"]
                    / (self._metadata["cache_hits"] + self._metadata["cache_misses"])
                    if (self._metadata["cache_hits"] + self._metadata["cache_misses"]) > 0
                    else 0.0
                ),
                "created_at": self._metadata["created_at"],
                "org_reports": list(self._cache["org_reports"].keys()),
            }

    def get_org_report_metadata(self, org_name: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for cached organization report.

        Args:
            org_name: Name of organization

        Returns:
            Metadata dictionary or None if not cached
        """
        with self._lock:
            if org_name in self._cache["org_reports"]:
                cache_entry = self._cache["org_reports"][org_name]
                return {
                    "org_name": org_name,
                    "response_count": cache_entry.get("response_count", 0),
                    "cached_at": cache_entry.get("cached_at"),
                    "has_report": cache_entry.get("report") is not None,
                }
            return None

    def get_cache_status(self) -> Dict[str, Any]:
        """
        Get comprehensive cache status for monitoring.

        Returns detailed information about cached reports including
        organization reports and aggregate report status.

        Returns:
            Dictionary with cache status information:
            - organization_reports: dict with count and list of organizations
            - aggregate_report: dict with cached status and details
        """
        with self._lock:
            org_cache_keys = list(self._cache["org_reports"].keys())
            aggregate_cached = self._cache["aggregate_report"] is not None

            cache_info = {
                "organization_reports": {"count": len(org_cache_keys), "organizations": []},
                "aggregate_report": {"cached": aggregate_cached},
            }

            # Add details for each cached org report
            for org_name in org_cache_keys:
                cache_data = self._cache["org_reports"][org_name]
                cache_info["organization_reports"]["organizations"].append(
                    {
                        "name": org_name,
                        "response_count": cache_data.get("response_count", 0),
                        "cached_at": cache_data.get("cached_at"),
                    }
                )

            # Add details for aggregate report if cached
            if aggregate_cached:
                agg_data = self._cache["aggregate_report"]
                cache_info["aggregate_report"].update(
                    {
                        "total_responses": agg_data.get("total_responses", 0),
                        "cached_at": agg_data.get("cached_at"),
                    }
                )

            return cache_info

    def get_sheets_cache_status(self) -> Dict[str, Any]:
        """
        Get status of sheets cache from SheetsReader.

        Returns cache status for all tabs including file information,
        validity, row counts, and timestamps.

        Returns:
            Dictionary with sheets cache status information from SheetsReader
        """
        from src.extractors.sheets_reader import SheetsReader

        return SheetsReader.get_cache_status()

    def get_json_reports_status(self) -> Dict[str, Any]:
        """
        Get status of JSON-stored reports on disk.

        Scans report directories and returns information about
        all saved JSON report files.

        Returns:
            Dictionary with JSON report file status including:
            - org_reports: list of organization report files
            - aggregate_reports: list of aggregate report files
        """
        import json
        import os

        org_reports = []
        aggregate_reports = []

        # Get report directories from repository
        org_reports_dir = self._report_repository.ORG_REPORTS_DIR
        aggregate_reports_dir = self._report_repository.AGGREGATE_REPORTS_DIR

        # Scan organization reports
        if os.path.exists(org_reports_dir):
            for filename in os.listdir(org_reports_dir):
                if filename.endswith(".json"):
                    filepath = os.path.join(org_reports_dir, filename)
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            report_data = json.load(f)

                        org_name = report_data.get("organization", "Unknown")
                        with_ai = report_data.get("with_ai_analysis", True)
                        response_count = report_data.get("response_count", 0)

                        org_reports.append(
                            {
                                "organization": org_name,
                                "filename": filename,
                                "with_ai": with_ai,
                                "generated_at": report_data.get("generated_at"),
                                "response_count": response_count,
                                "file_size": os.path.getsize(filepath),
                            }
                        )
                    except Exception as e:
                        print(f"[JSON Status] Error reading {filename}: {e}")

        # Scan aggregate reports
        if os.path.exists(aggregate_reports_dir):
            for filename in os.listdir(aggregate_reports_dir):
                if filename.endswith(".json"):
                    filepath = os.path.join(aggregate_reports_dir, filename)
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            report_data = json.load(f)

                        with_ai = report_data.get("with_ai_analysis", True)
                        total_responses = report_data.get("total_responses", 0)

                        aggregate_reports.append(
                            {
                                "filename": filename,
                                "with_ai": with_ai,
                                "generated_at": report_data.get("generated_at"),
                                "total_responses": total_responses,
                                "file_size": os.path.getsize(filepath),
                            }
                        )
                    except Exception as e:
                        print(f"[JSON Status] Error reading {filename}: {e}")

        return {
            "org_reports": org_reports,
            "aggregate_reports": aggregate_reports,
            "org_reports_count": len(org_reports),
            "aggregate_reports_count": len(aggregate_reports),
        }

    def clear_report_cache(self, force: bool = False) -> None:
        """
        Clear all cached reports from memory and disk.

        Clears in-memory cache and optionally removes JSON report files.
        This is typically called on application startup or when cache
        needs to be invalidated.

        Args:
            force: If True, clear cache regardless of configuration
        """
        import os

        # Clear in-memory cache
        self.clear_all()
        print("[Cache] Cleared in-memory report cache")

        # Clear JSON cache files
        cleared_count = 0
        org_reports_dir = self._report_repository.ORG_REPORTS_DIR
        aggregate_reports_dir = self._report_repository.AGGREGATE_REPORTS_DIR

        for directory in [org_reports_dir, aggregate_reports_dir]:
            if os.path.exists(directory):
                for filename in os.listdir(directory):
                    if filename.endswith(".json"):
                        file_path = os.path.join(directory, filename)
                        try:
                            os.remove(file_path)
                            cleared_count += 1
                        except Exception as e:
                            print(f"[Cache] Error removing {file_path}: {e}")

        if cleared_count > 0:
            print(f"[Cache] Cleared {cleared_count} JSON report files")

    def clear_sheets_cache(self, tab_name: str = None, verbose: bool = False) -> None:
        """
        Clear Google Sheets cache.

        Delegates to SheetsReader to clear file-based cache.

        Args:
            tab_name: Optional specific tab to clear. If None, clears all tabs.
            verbose: If True, print verbose output
        """
        from src.extractors.sheets_reader import SheetsReader

        SheetsReader.clear_cache(tab_name=tab_name, verbose=verbose)


# Global singleton instance
_cache_service_instance: Optional[CacheService] = None
_instance_lock = threading.Lock()


def get_cache_service(report_repository=None) -> CacheService:
    """
    Get singleton cache service instance.

    Args:
        report_repository: Optional ReportRepository instance (only used on first call)

    Returns:
        Singleton CacheService instance
    """
    global _cache_service_instance

    if _cache_service_instance is None:
        with _instance_lock:
            if _cache_service_instance is None:
                _cache_service_instance = CacheService(report_repository)

    return _cache_service_instance
