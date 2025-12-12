"""
Application initialization utilities.

Handles data loading, cache clearing, and startup tasks.
Extracted from app.py to keep application factory clean.
"""

import os
import threading
from typing import Any, Dict

from src.extractors.sheets_reader import SheetsReader
from src.utils.cache_version import get_cache_metadata


def load_sheet_data(
    verbose: bool = False, use_cache: bool = True, force_refresh: bool = False
) -> Dict[str, Any]:
    """
    Load data from Google Sheets into memory with caching support.

    Args:
        verbose: Enable verbose logging
        use_cache: Use cached data if available
        force_refresh: Force refresh even if cache is valid

    Returns:
        Dictionary mapping tab names to data
    """
    return SheetsReader.fetch_all_tabs(
        verbose=verbose, use_cache=use_cache, force_refresh=force_refresh
    )


def clear_report_cache(app, force: bool = False):
    """
    Clear all cached reports from disk and memory.

    This is called on application startup to ensure reports are regenerated
    when code version or admin edits change.

    Args:
        app: Flask application instance
        force: If True, clear cache regardless of CLEAR_CACHE_ON_STARTUP setting
    """
    clear_cache_on_startup = app.config.get("CLEAR_CACHE_ON_STARTUP", True)

    if not force and not clear_cache_on_startup:
        print("[Cache] Cache clearing disabled (CLEAR_CACHE_ON_STARTUP=false)")
        return

    try:
        # Get cache service from container
        container = app.config.get("CONTAINER")
        if container:
            cache_service = container.cache_service
            cache_service.clear_all()
            print("[Cache] Cleared all caches via CacheService")
        else:
            # Fallback: Clear directories directly
            reports_dir = app.config.get("REPORTS_DIR", "reports_json")
            org_reports_dir = os.path.join(reports_dir, "organizations")
            aggregate_reports_dir = os.path.join(reports_dir, "aggregate")

            cleared_count = 0
            for directory in [org_reports_dir, aggregate_reports_dir]:
                if os.path.exists(directory):
                    for filename in os.listdir(directory):
                        if filename.endswith(".json"):
                            filepath = os.path.join(directory, filename)
                            os.remove(filepath)
                            cleared_count += 1

            print(f"[Cache] Cleared {cleared_count} cached report files from disk")

        # Log cache version info
        cache_meta = get_cache_metadata()
        print(f"[Cache Version] Current version: {cache_meta['cache_version']}")
        print(f"[Cache Version] Git commit: {cache_meta['git_commit']}")
        print(f"[Cache Version] Admin edits hash: {cache_meta['admin_edits_hash']}")

    except Exception as e:
        print(f"[Cache] Error clearing cache: {e}")


def load_admin_edits(app):
    """
    Load admin edits from JSON file.

    Args:
        app: Flask application instance
    """
    try:
        container = app.config.get("CONTAINER")
        if container:
            admin_edit_service = container.admin_edit_service
            # Load admin edits from file
            admin_edit_service.load_edits()
            print("✓ Admin edits loaded via AdminEditService")
    except Exception as e:
        print(f"✗ Failed to load admin edits: {e}")


def _prepopulate_quantitative_cache(app):
    """
    Pre-populate quantitative cache for all organizations on startup.

    This ensures the Build & Review page loads instantly (30-50ms from cache)
    instead of regenerating reports on first access (150-200ms+ per org).

    Args:
        app: Flask application instance
    """
    try:
        container = app.config.get("CONTAINER")
        if not container:
            print("[Cache] Container not available, skipping cache pre-population")
            return

        data_service = container.data_service
        report_service = container.report_service

        # Get all organization names from Intake submissions
        intake_data = data_service.get_tab_data("Intake")
        if not intake_data:
            print("[Cache] No organizations found in Intake, skipping cache pre-population")
            return

        # Extract unique organization names from Intake (note: column name has colon)
        org_names = list(set([row.get("Organization Name:") for row in intake_data if row.get("Organization Name:")]))
        org_names.sort()  # Sort for consistent ordering
        print(f"[Cache] Pre-populating quantitative cache for {len(org_names)} organizations...")

        success_count = 0
        for org_name in org_names:
            try:
                # Generate and cache quantitative report (skip_ai=True for speed)
                # This will check for existing cache and only regenerate if needed
                report = report_service.get_organization_report(org_name, use_cache=True, skip_ai=True)
                if report:
                    success_count += 1
                    print(f"[Cache] ✓ Cached quantitative report for {org_name}")
            except Exception as e:
                print(f"[Cache] ✗ Failed to cache report for {org_name}: {e}")

        print(f"[Cache] Pre-populated {success_count}/{len(org_names)} quantitative reports")

    except Exception as e:
        print(f"[Cache] Error pre-populating quantitative cache: {e}")


def load_data_async(app):
    """
    Load data from Google Sheets in background thread.

    This function is called on application startup to pre-load data.

    Args:
        app: Flask application instance
    """
    print("Loading data from Google Sheets on startup...")
    try:
        # Clear report cache to ensure fresh regeneration
        print("Clearing report cache...")
        clear_report_cache(app)

        # Load sheet data
        with app.app_context():
            container = app.config.get("CONTAINER")
            if container:
                data_service = container.data_service
                # Actually load the data by calling refresh_data()
                data_service.refresh_data(verbose=True)
                print("✓ Data loaded successfully via DataService. Ready to serve requests.")
            else:
                # Fallback: Load data directly
                load_sheet_data(verbose=True)
                print("✓ Data loaded successfully. Ready to serve requests.")

        # Load admin edits
        print("Loading admin edits...")
        load_admin_edits(app)
        print("✓ Admin edits loaded successfully!")

        # Pre-populate quantitative cache for all organizations
        print("Pre-populating quantitative cache...")
        _prepopulate_quantitative_cache(app)
        print("✓ Quantitative cache pre-populated!")

    except Exception as e:
        print(f"✗ Failed to load data on startup: {e}")
        print("  Application will start but data will be empty until refresh.")


def initialize_data_loading(app):
    """
    Initialize data loading based on deployment environment.

    On Railway: Load data asynchronously in background thread
    Locally: Load data synchronously on startup

    Args:
        app: Flask application instance
    """
    if not app.config.get("LOAD_DATA_ON_STARTUP", True):
        print("[Startup] Data loading disabled by configuration")
        return

    if app.config.get("ASYNC_DATA_LOADING", False):
        print("[Startup] Railway environment detected - starting background data load...")
        threading.Thread(target=load_data_async, args=(app,), daemon=True).start()
    else:
        print("[Startup] Local environment - loading data synchronously...")
        load_data_async(app)
