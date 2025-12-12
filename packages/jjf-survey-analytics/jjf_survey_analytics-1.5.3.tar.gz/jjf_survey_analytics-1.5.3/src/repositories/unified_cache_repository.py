#!/usr/bin/env python3
"""
UnifiedCacheRepository - Single source of truth for organization data.

Consolidates 3 separate cache systems into one unified structure:
- Quantitative data (variance_analysis, scores)
- Qualitative data (AI insights, summaries)
- Admin overrides (custom titles, modifiers)

File Structure:
    cache/organizations/<org_name>/cache.json
    {
        "org_name": "Organization Name",
        "created_at": "2025-12-03T...",
        "updated_at": "2025-12-03T...",
        "version": 1,
        "cache_version": "1.5.0_4f4eb42_a1b2c3d4",

        "quantitative": {
            "maturity": {
                "variance_analysis": {...},
                "overall_score": 3.60,
                "maturity_level": "Thriving",
                ...
            },
            "nps": {...},
            "tech_insights": {...}
        },

        "qualitative": {
            "main_summary": {
                "text": "AI-generated summary",
                "title": "Optional custom title",
                "subtitle": "Optional subtitle"
            },
            "dimensions": {
                "Business Systems": {
                    "summary": "AI analysis",
                    "themes": [...],
                    "modifiers": [...]
                }
            }
        },

        "admin_overrides": {
            "summary_title": "Admin custom title",
            "summary_body": "Admin custom body",
            "dimension_insights": {
                "Dimension Name": "Custom text"
            },
            "score_modifiers": {
                "Dimension_Name": [
                    {"id": 0, "value": 0.5}
                ]
            }
        }
    }

Benefits:
    - Single source of truth (one file per organization)
    - Atomic updates (all data updated together)
    - Easier debugging (everything in one place)
    - Better performance (one file read instead of 3)
    - Simpler mental model for developers

Related:
    - 1M-555: Cache consolidation ticket
    - docs/SCORE_DATA_FLOW.md: Architecture analysis
"""

import json
import os
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from src.utils.cache_version import get_cache_version, is_cache_valid

# Thread-safe singleton
_unified_cache_instance: Optional["UnifiedCacheRepository"] = None
_instance_lock = threading.RLock()


class UnifiedCacheRepository:
    """
    Thread-safe unified cache repository for organization data.

    Provides atomic read/write operations for:
    - Quantitative scores (variance_analysis, maturity levels)
    - Qualitative AI insights (summaries, themes, modifiers)
    - Admin overrides (custom text, score modifiers)

    All data stored in single file per organization for consistency.
    """

    # Cache base directory
    CACHE_BASE_DIR = Path("cache/organizations")

    # Cache version for schema migrations
    CACHE_VERSION = 1

    def __init__(self, base_dir: Optional[Path] = None):
        """
        Initialize unified cache repository.

        Args:
            base_dir: Optional custom base directory (defaults to cache/organizations)
        """
        self._base_dir = base_dir or self.CACHE_BASE_DIR
        self._lock = threading.RLock()

        # Ensure base directory exists
        self._base_dir.mkdir(parents=True, exist_ok=True)

        print(f"[UnifiedCache] Initialized at {self._base_dir}")

    def _get_org_cache_path(self, org_name: str) -> Path:
        """
        Get path to organization's unified cache file.

        Args:
            org_name: Organization name

        Returns:
            Path to cache.json file
        """
        # Sanitize org name for filesystem
        safe_name = org_name.replace(" ", "_").replace("/", "_").lower()
        org_dir = self._base_dir / safe_name
        org_dir.mkdir(parents=True, exist_ok=True)
        return org_dir / "cache.json"

    def _load_cache(self, org_name: str) -> Optional[Dict[str, Any]]:
        """
        Load unified cache for organization.

        Args:
            org_name: Organization name

        Returns:
            Cache dictionary or None if not exists or invalid
        """
        with self._lock:
            cache_path = self._get_org_cache_path(org_name)

            if not cache_path.exists():
                return None

            try:
                with open(cache_path, 'r') as f:
                    cache = json.load(f)

                    # Validate cache version
                    cached_version = cache.get("cache_version")
                    if not is_cache_valid(cached_version):
                        print(f"[UnifiedCache] Version mismatch - invalidating cache for {org_name}")
                        print(f"[UnifiedCache]   Cached: {cached_version}, Current: {get_cache_version()}")
                        return None

                    print(f"[UnifiedCache] Loaded cache for {org_name} (version: {cached_version})")
                    return cache
            except (json.JSONDecodeError, IOError) as e:
                print(f"[UnifiedCache] Error loading cache for {org_name}: {e}")
                return None

    def _save_cache(self, org_name: str, cache: Dict[str, Any]) -> bool:
        """
        Save unified cache for organization.

        Args:
            org_name: Organization name
            cache: Cache dictionary to save

        Returns:
            True if saved successfully, False otherwise
        """
        with self._lock:
            cache_path = self._get_org_cache_path(org_name)

            # Update metadata
            cache["updated_at"] = datetime.utcnow().isoformat()
            if "created_at" not in cache:
                cache["created_at"] = cache["updated_at"]
            if "version" not in cache:
                cache["version"] = self.CACHE_VERSION

            # Always update cache version on save
            cache["cache_version"] = get_cache_version()

            try:
                # Write atomically (write to temp, then rename)
                temp_path = cache_path.with_suffix('.tmp')
                with open(temp_path, 'w') as f:
                    json.dump(cache, f, indent=2)
                temp_path.replace(cache_path)

                print(f"[UnifiedCache] Saved cache for {org_name} (version: {cache['cache_version']})")
                return True
            except IOError as e:
                print(f"[UnifiedCache] Error saving cache for {org_name}: {e}")
                return False

    def _ensure_cache_structure(self, cache: Dict[str, Any], org_name: str) -> Dict[str, Any]:
        """
        Ensure cache has correct structure with all required sections.

        Args:
            cache: Existing cache or empty dict
            org_name: Organization name

        Returns:
            Cache with complete structure
        """
        if not cache:
            cache = {
                "org_name": org_name,
                "created_at": datetime.utcnow().isoformat(),
                "version": self.CACHE_VERSION
            }

        # Ensure all top-level sections exist
        if "quantitative" not in cache:
            cache["quantitative"] = {}
        if "qualitative" not in cache:
            cache["qualitative"] = {
                "main_summary": {},
                "dimensions": {}
            }
        if "admin_overrides" not in cache:
            cache["admin_overrides"] = {}

        return cache

    # ===== QUANTITATIVE DATA METHODS =====

    def get_quantitative_data(self, org_name: str) -> Optional[Dict[str, Any]]:
        """
        Get quantitative data (scores, variance_analysis) for organization.

        Args:
            org_name: Organization name

        Returns:
            Quantitative data dictionary or None if not cached
        """
        cache = self._load_cache(org_name)
        if not cache:
            return None

        return cache.get("quantitative")

    def save_quantitative_data(self, org_name: str, data: Dict[str, Any]) -> bool:
        """
        Save quantitative data for organization.

        Args:
            org_name: Organization name
            data: Quantitative data dictionary (maturity, nps, etc.)

        Returns:
            True if saved successfully
        """
        cache = self._load_cache(org_name) or {}
        cache = self._ensure_cache_structure(cache, org_name)

        cache["quantitative"] = data
        return self._save_cache(org_name, cache)

    def get_variance_analysis(self, org_name: str) -> Optional[Dict[str, Any]]:
        """
        Get variance_analysis (dimension scores) for organization.

        This is the most frequently accessed data, so we provide
        a convenience method for direct access.

        Args:
            org_name: Organization name

        Returns:
            variance_analysis dictionary or None
        """
        quant_data = self.get_quantitative_data(org_name)
        if not quant_data:
            return None

        maturity = quant_data.get("maturity", {})
        return maturity.get("variance_analysis")

    # ===== QUALITATIVE DATA METHODS =====

    def get_qualitative_data(self, org_name: str) -> Optional[Dict[str, Any]]:
        """
        Get qualitative data (AI insights, summaries) for organization.

        Args:
            org_name: Organization name

        Returns:
            Qualitative data dictionary or None if not cached
        """
        cache = self._load_cache(org_name)
        if not cache:
            return None

        return cache.get("qualitative")

    def save_qualitative_data(self, org_name: str, data: Dict[str, Any]) -> bool:
        """
        Save qualitative data for organization.

        Args:
            org_name: Organization name
            data: Qualitative data dictionary (main_summary, dimensions)

        Returns:
            True if saved successfully
        """
        cache = self._load_cache(org_name) or {}
        cache = self._ensure_cache_structure(cache, org_name)

        cache["qualitative"] = data
        return self._save_cache(org_name, cache)

    def get_main_summary(self, org_name: str) -> Optional[Dict[str, Any]]:
        """
        Get main summary (AI + custom title/subtitle) for organization.

        Args:
            org_name: Organization name

        Returns:
            Main summary dictionary or None
        """
        qual_data = self.get_qualitative_data(org_name)
        if not qual_data:
            return None

        return qual_data.get("main_summary")

    def get_dimension_data(self, org_name: str, dimension: str) -> Optional[Dict[str, Any]]:
        """
        Get AI data for specific dimension.

        Args:
            org_name: Organization name
            dimension: Dimension name

        Returns:
            Dimension data dictionary or None
        """
        qual_data = self.get_qualitative_data(org_name)
        if not qual_data:
            return None

        dimensions = qual_data.get("dimensions", {})
        return dimensions.get(dimension)

    # ===== ADMIN OVERRIDES METHODS =====

    def get_admin_overrides(self, org_name: str) -> Optional[Dict[str, Any]]:
        """
        Get admin overrides (custom text, score modifiers) for organization.

        Args:
            org_name: Organization name

        Returns:
            Admin overrides dictionary or None
        """
        cache = self._load_cache(org_name)
        if not cache:
            return None

        return cache.get("admin_overrides")

    def save_admin_overrides(self, org_name: str, overrides: Dict[str, Any]) -> bool:
        """
        Save admin overrides for organization.

        Args:
            org_name: Organization name
            overrides: Admin overrides dictionary

        Returns:
            True if saved successfully
        """
        cache = self._load_cache(org_name) or {}
        cache = self._ensure_cache_structure(cache, org_name)

        cache["admin_overrides"] = overrides
        return self._save_cache(org_name, cache)

    # ===== COMPLETE CACHE METHODS =====

    def get_complete_cache(self, org_name: str) -> Optional[Dict[str, Any]]:
        """
        Get complete unified cache for organization.

        Args:
            org_name: Organization name

        Returns:
            Complete cache dictionary or None
        """
        return self._load_cache(org_name)

    def save_complete_cache(self, org_name: str, cache: Dict[str, Any]) -> bool:
        """
        Save complete unified cache for organization.

        Use this for atomic updates of multiple sections.

        Args:
            org_name: Organization name
            cache: Complete cache dictionary

        Returns:
            True if saved successfully
        """
        cache = self._ensure_cache_structure(cache, org_name)
        return self._save_cache(org_name, cache)

    def invalidate_cache(self, org_name: str) -> bool:
        """
        Delete unified cache for organization.

        Args:
            org_name: Organization name

        Returns:
            True if deleted successfully
        """
        with self._lock:
            cache_path = self._get_org_cache_path(org_name)

            if cache_path.exists():
                try:
                    cache_path.unlink()
                    print(f"[UnifiedCache] Invalidated cache for {org_name}")
                    return True
                except OSError as e:
                    print(f"[UnifiedCache] Error invalidating cache for {org_name}: {e}")
                    return False

            return True

    def list_cached_organizations(self) -> list[str]:
        """
        List all organizations with cached data.

        Returns:
            List of organization names
        """
        with self._lock:
            orgs = []

            if not self._base_dir.exists():
                return orgs

            for org_dir in self._base_dir.iterdir():
                if org_dir.is_dir():
                    cache_file = org_dir / "cache.json"
                    if cache_file.exists():
                        try:
                            with open(cache_file) as f:
                                cache = json.load(f)
                                org_name = cache.get("org_name", org_dir.name.replace("_", " ").title())
                                orgs.append(org_name)
                        except (json.JSONDecodeError, IOError):
                            continue

            return sorted(orgs)


def get_unified_cache_repository(base_dir: Optional[Path] = None) -> UnifiedCacheRepository:
    """
    Get singleton unified cache repository instance.

    Args:
        base_dir: Optional custom base directory

    Returns:
        Singleton UnifiedCacheRepository instance
    """
    global _unified_cache_instance

    if _unified_cache_instance is None:
        with _instance_lock:
            if _unified_cache_instance is None:
                _unified_cache_instance = UnifiedCacheRepository(base_dir)

    return _unified_cache_instance
