#!/usr/bin/env python3
"""
Google Sheets Direct Reader
Reads data directly from Google Sheets into memory without database.
"""

import csv
import io
import json
import os
import urllib.request
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


class SheetsReader:
    """Direct Google Sheets reader for in-memory storage with local JSON caching."""

    # Single spreadsheet ID for JJF Technology Assessment
    SPREADSHEET_ID = "15ZaH4wyt4Wz95kiW1kLe6h4bwuqsA-voBwSzGwni2ZU"

    # Cache configuration
    CACHE_DIR = "cache/sheets"
    CACHE_EXPIRY_HOURS = 1  # Cache expires after 1 hour

    # Tab configuration with GIDs
    TABS = {
        "Summary": "0",  # Summary/overview tab
        "Intake": "1366958616",  # Initial participation survey (28 responses)
        "CEO": "1242252865",  # CEO assessment + contacts (3 responses, C-* question IDs)
        "Tech": "1545410106",  # Tech Lead survey (2 responses, TL-* question IDs)
        "Staff": "377168987",  # Staff survey (4 responses, S-* question IDs)
        "Questions": "513349220",  # Question bank with IDs and answer options (67 questions)
        "Key": "1000323612",  # Organization reference lookup table (6 entries)
        "OrgMaster": "601687640",  # Master list of all organizations reached out to
    }

    @staticmethod
    def get_csv_export_url(gid: str) -> str:
        """Get CSV export URL for a specific tab."""
        return f"https://docs.google.com/spreadsheets/d/{SheetsReader.SPREADSHEET_ID}/export?format=csv&gid={gid}"

    @classmethod
    def _ensure_cache_dir(cls):
        """Ensure cache directory exists."""
        os.makedirs(cls.CACHE_DIR, exist_ok=True)

    @classmethod
    def _get_cache_file_path(cls, tab_name: str) -> str:
        """Get cache file path for a specific tab."""
        cls._ensure_cache_dir()
        return os.path.join(cls.CACHE_DIR, f"{tab_name}.json")

    @classmethod
    def _is_cache_valid(cls, cache_file_path: str) -> bool:
        """Check if cache file exists and is not expired."""
        if not os.path.exists(cache_file_path):
            return False

        # Check file age
        file_time = datetime.fromtimestamp(os.path.getmtime(cache_file_path))
        expiry_time = datetime.now() - timedelta(hours=cls.CACHE_EXPIRY_HOURS)

        return file_time > expiry_time

    @classmethod
    def _load_from_cache(
        cls, tab_name: str, verbose: bool = False
    ) -> Optional[List[Dict[str, Any]]]:
        """Load tab data from cache if valid."""
        cache_file_path = cls._get_cache_file_path(tab_name)

        if not cls._is_cache_valid(cache_file_path):
            return None

        try:
            with open(cache_file_path, "r", encoding="utf-8") as f:
                cache_data = json.load(f)

            if verbose:
                cache_time = datetime.fromtimestamp(os.path.getmtime(cache_file_path))
                print(
                    f"  ✓ Loaded {tab_name} from cache (cached: {cache_time.strftime('%Y-%m-%d %H:%M:%S')})"
                )

            return cache_data.get("data", [])

        except (json.JSONDecodeError, KeyError, IOError) as e:
            if verbose:
                print(f"  ⚠ Cache read error for {tab_name}: {e}")
            return None

    @classmethod
    def _save_to_cache(cls, tab_name: str, data: List[Dict[str, Any]], verbose: bool = False):
        """Save tab data to cache."""
        cache_file_path = cls._get_cache_file_path(tab_name)

        try:
            cache_data = {
                "tab_name": tab_name,
                "cached_at": datetime.now().isoformat(),
                "spreadsheet_id": cls.SPREADSHEET_ID,
                "row_count": len(data),
                "data": data,
            }

            with open(cache_file_path, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)

            if verbose:
                print(f"  ✓ Cached {tab_name} ({len(data)} rows)")

        except (IOError, TypeError) as e:
            if verbose:
                print(f"  ⚠ Cache write error for {tab_name}: {e}")

    @classmethod
    def clear_cache(cls, tab_name: Optional[str] = None, verbose: bool = False):
        """Clear cache for specific tab or all tabs."""
        if tab_name:
            # Clear specific tab
            cache_file_path = cls._get_cache_file_path(tab_name)
            if os.path.exists(cache_file_path):
                os.remove(cache_file_path)
                if verbose:
                    print(f"✓ Cleared cache for {tab_name}")
        else:
            # Clear all cache files
            if os.path.exists(cls.CACHE_DIR):
                for filename in os.listdir(cls.CACHE_DIR):
                    if filename.endswith(".json"):
                        os.remove(os.path.join(cls.CACHE_DIR, filename))
                if verbose:
                    print("✓ Cleared all cache files")

    @classmethod
    def get_cache_status(cls) -> Dict[str, Any]:
        """Get cache status for all tabs."""
        status = {
            "cache_dir": cls.CACHE_DIR,
            "cache_expiry_hours": cls.CACHE_EXPIRY_HOURS,
            "tabs": {},
        }

        for tab_name in cls.TABS.keys():
            cache_file_path = cls._get_cache_file_path(tab_name)

            if os.path.exists(cache_file_path):
                file_time = datetime.fromtimestamp(os.path.getmtime(cache_file_path))
                is_valid = cls._is_cache_valid(cache_file_path)

                try:
                    with open(cache_file_path, "r", encoding="utf-8") as f:
                        cache_data = json.load(f)
                    row_count = cache_data.get("row_count", 0)
                except Exception:
                    row_count = 0

                status["tabs"][tab_name] = {
                    "cached": True,
                    "cached_at": file_time.isoformat(),
                    "is_valid": is_valid,
                    "row_count": row_count,
                    "file_size_kb": round(os.path.getsize(cache_file_path) / 1024, 2),
                }
            else:
                status["tabs"][tab_name] = {
                    "cached": False,
                    "cached_at": None,
                    "is_valid": False,
                    "row_count": 0,
                    "file_size_kb": 0,
                }

        return status

    @classmethod
    def download_tab_data(
        cls, tab_name: str, gid: str, verbose: bool = False, use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """Download data from a specific tab with caching support."""
        # Try to load from cache first
        if use_cache:
            cached_data = cls._load_from_cache(tab_name, verbose)
            if cached_data is not None:
                return cached_data

        # Cache miss or disabled - download from Google Sheets
        try:
            csv_url = cls.get_csv_export_url(gid)
            if verbose:
                print(f"  Downloading {tab_name} from GID {gid}...")

            # Create request with headers
            req = urllib.request.Request(csv_url)
            req.add_header("User-Agent", "Mozilla/5.0")

            with urllib.request.urlopen(req, timeout=30) as response:
                csv_data = response.read().decode("utf-8")

            # Parse CSV
            if csv_data.strip() and not csv_data.startswith("<!DOCTYPE"):
                csv_reader = csv.DictReader(io.StringIO(csv_data))
                data = list(csv_reader)
                if verbose:
                    print(f"  ✓ Downloaded {len(data)} rows from {tab_name}")

                # Save to cache
                if use_cache:
                    cls._save_to_cache(tab_name, data, verbose)

                return data
            else:
                if verbose:
                    print(f"  ✗ Invalid data received for {tab_name}")
                return []

        except Exception as e:
            if verbose:
                print(f"  ✗ Error downloading {tab_name}: {e}")

            # If download fails, try to use expired cache as fallback
            if use_cache:
                cache_file_path = cls._get_cache_file_path(tab_name)
                if os.path.exists(cache_file_path):
                    try:
                        with open(cache_file_path, "r", encoding="utf-8") as f:
                            cache_data = json.load(f)
                        fallback_data = cache_data.get("data", [])
                        if verbose:
                            print(
                                f"  ⚠ Using expired cache for {tab_name} ({len(fallback_data)} rows)"
                            )
                        return fallback_data
                    except Exception:
                        pass

            return []

    @classmethod
    def fetch_all_tabs(
        cls, verbose: bool = False, use_cache: bool = True, force_refresh: bool = False
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetch data from all tabs and return as dictionary with caching support.

        Args:
            verbose: Print detailed progress information
            use_cache: Whether to use cached data when available
            force_refresh: Force refresh from Google Sheets, ignoring cache

        Returns:
            {
                'Summary': [rows...],
                'Intake': [rows...],
                'CEO': [rows...],
                ...
                '_metadata': {
                    'last_fetch': timestamp,
                    'total_rows': count,
                    'tabs_count': count,
                    'cache_status': {...}
                }
            }
        """
        # Override cache usage if force refresh is requested
        effective_use_cache = use_cache and not force_refresh

        if verbose:
            print(f"\n{'='*60}")
            print("Google Sheets Direct Reader")
            print(f"{'='*60}")
            print(f"Spreadsheet ID: {cls.SPREADSHEET_ID}")
            print(f"Tabs: {', '.join(cls.TABS.keys())}")
            print(f"Cache: {'Enabled' if effective_use_cache else 'Disabled'}")
            if force_refresh:
                print("Mode: Force refresh (ignoring cache)")
            print(f"{'='*60}\n")

        sheet_data = {}
        total_rows = 0
        successful_tabs = 0
        cache_hits = 0
        cache_misses = 0

        for tab_name, gid in cls.TABS.items():
            if verbose:
                print(f"[{tab_name}]")

            # Check if we're using cache for this tab
            if effective_use_cache and cls._load_from_cache(tab_name, False) is not None:
                cache_hits += 1
            else:
                cache_misses += 1

            data = cls.download_tab_data(tab_name, gid, verbose, effective_use_cache)
            sheet_data[tab_name] = data

            if data:
                total_rows += len(data)
                successful_tabs += 1

        # Get cache status
        cache_status = cls.get_cache_status()

        # Add metadata
        sheet_data["_metadata"] = {
            "last_fetch": datetime.now().isoformat(),
            "total_rows": total_rows,
            "tabs_count": successful_tabs,
            "spreadsheet_id": cls.SPREADSHEET_ID,
            "cache_enabled": effective_use_cache,
            "cache_hits": cache_hits,
            "cache_misses": cache_misses,
            "cache_status": cache_status,
        }

        if verbose:
            print(f"\n{'='*60}")
            print("Fetch Complete")
            print(f"{'='*60}")
            print(f"✓ Successfully fetched {successful_tabs}/{len(cls.TABS)} tabs")
            print(f"✓ Total rows: {total_rows}")
            if effective_use_cache:
                print(f"✓ Cache hits: {cache_hits}, Cache misses: {cache_misses}")
            print(f"{'='*60}\n")

        return sheet_data


def main():
    """Main function to test reader."""
    data = SheetsReader.fetch_all_tabs(verbose=True)

    print("\nData Summary:")
    for tab_name in SheetsReader.TABS.keys():
        row_count = len(data.get(tab_name, []))
        print(f"  - {tab_name}: {row_count} rows")

    print("\nMetadata:")
    metadata = data.get("_metadata", {})
    for key, value in metadata.items():
        print(f"  - {key}: {value}")


if __name__ == "__main__":
    main()
