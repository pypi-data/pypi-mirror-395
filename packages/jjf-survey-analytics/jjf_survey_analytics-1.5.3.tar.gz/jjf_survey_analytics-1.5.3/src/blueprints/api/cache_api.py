"""
Cache API Blueprint for JJF Survey Analytics.

Provides API endpoints for cache management and status monitoring.
"""

from flask import Blueprint, jsonify, request

from src.blueprints.auth_blueprint import require_auth
from src.services.container import get_container

# Create blueprint
cache_api = Blueprint("cache_api", __name__, url_prefix="/api")


@cache_api.route("/cache/status")
@require_auth
def cache_status():
    """
    Get report cache status for monitoring.

    Returns detailed status of in-memory report cache including:
    - Organization reports count and details
    - Aggregate report status
    - Cache validity checks

    Returns:
        JSON response with cache status information
    """
    container = get_container()
    cache_service = container.cache_service

    try:
        cache_info = cache_service.get_cache_status()
        return jsonify(cache_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cache_api.route("/reports/json/status")
@require_auth
def json_reports_status():
    """
    Get status of JSON-stored reports on disk.

    Scans report directories and returns information about
    all saved JSON report files.

    Returns:
        JSON response with JSON report file status
    """
    container = get_container()
    cache_service = container.cache_service

    try:
        json_status = cache_service.get_json_reports_status()
        return jsonify(json_status)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@cache_api.route("/cache/clear", methods=["POST"])
@require_auth
def clear_cache():
    """
    Manually clear the in-memory report cache.

    Clears all cached organization and aggregate reports.

    Returns:
        JSON response with success status
    """
    container = get_container()
    cache_service = container.cache_service

    try:
        cache_service.clear_report_cache()
        print("[Cache] Manually cleared all cached reports")

        return jsonify({"success": True, "message": "Report cache cleared successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@cache_api.route("/cache/sheets/status", methods=["GET"])
@require_auth
def get_sheets_cache_status():
    """
    Get status of Google Sheets cache.

    Returns information about cached sheet data.

    Returns:
        JSON response with sheets cache status
    """
    container = get_container()
    cache_service = container.cache_service

    try:
        cache_status = cache_service.get_sheets_cache_status()
        return jsonify({"success": True, "cache_status": cache_status})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@cache_api.route("/cache/sheets/clear", methods=["POST"])
@require_auth
def clear_sheets_cache():
    """
    Clear Google Sheets cache.

    Can optionally clear cache for specific tab or all tabs.

    Request Body:
        {
            "tab_name": "TabName"  // Optional: clear specific tab
        }

    Returns:
        JSON response with success status
    """
    container = get_container()
    cache_service = container.cache_service

    try:
        data = request.get_json() or {}
        tab_name = data.get("tab_name")  # Optional: clear specific tab

        cache_service.clear_sheets_cache(tab_name=tab_name, verbose=True)

        message = f"Cleared cache for {tab_name}" if tab_name else "Cleared all sheets cache"
        return jsonify({"success": True, "message": message})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@cache_api.route("/cache/unified/status", methods=["GET"])
@require_auth
def get_unified_cache_status():
    """
    Get status of unified caches for all organizations.

    Returns list of organizations with cache status including version info.

    Returns:
        JSON response with org cache status
    """
    from pathlib import Path
    import os
    from datetime import datetime
    from src.utils.cache_version import get_cache_metadata, is_cache_valid

    try:
        # Get current cache version metadata
        current_version_metadata = get_cache_metadata()

        cache_base = Path("cache/organizations")
        organizations = []

        if not cache_base.exists():
            return jsonify({
                "success": True,
                "organizations": [],
                "current_version": current_version_metadata
            })

        for org_dir in cache_base.iterdir():
            if not org_dir.is_dir():
                continue

            cache_file = org_dir / "cache.json"
            if not cache_file.exists():
                continue

            try:
                import json
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)

                org_name = cache_data.get("org_name", org_dir.name.replace("_", " ").title())

                # Check what sections exist
                has_quantitative = "quantitative" in cache_data and cache_data["quantitative"]
                has_qualitative = "qualitative" in cache_data and cache_data["qualitative"]

                # Get file stats
                stat = cache_file.stat()
                file_size_kb = round(stat.st_size / 1024, 2)
                last_modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

                # Get cache version info
                cached_version = cache_data.get("cache_version", "unknown")
                version_valid = is_cache_valid(cached_version)

                organizations.append({
                    "org_name": org_name,
                    "has_quantitative": has_quantitative,
                    "has_qualitative": has_qualitative,
                    "file_size_kb": file_size_kb,
                    "last_modified": last_modified,
                    "cache_version": cached_version,
                    "version_valid": version_valid
                })
            except Exception as e:
                print(f"[UnifiedCache] Error reading cache for {org_dir.name}: {e}")
                continue

        # Sort by org name
        organizations.sort(key=lambda x: x["org_name"])

        return jsonify({
            "success": True,
            "organizations": organizations,
            "current_version": current_version_metadata
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@cache_api.route("/cache/unified/clear-quantitative", methods=["POST"])
@require_auth
def clear_unified_quantitative_cache():
    """
    Clear quantitative cache for specific organization.

    This forces regeneration of scores on next page load.
    Useful after fixing bugs in score calculation logic.

    Request Body:
        {
            "org_name": "Organization Name"
        }

    Returns:
        JSON response with success status
    """
    from src.repositories.unified_cache_repository import get_unified_cache_repository

    try:
        data = request.get_json() or {}
        org_name = data.get("org_name")

        if not org_name:
            return jsonify({"success": False, "error": "org_name is required"}), 400

        # Get unified cache repository
        unified_cache = get_unified_cache_repository()

        # Load full cache
        cache = unified_cache.get_complete_cache(org_name)
        if not cache:
            return jsonify({"success": False, "error": f"No cache found for {org_name}"}), 404

        # Delete quantitative section
        if "quantitative" in cache:
            del cache["quantitative"]
            print(f"[UnifiedCache] Cleared quantitative cache for {org_name}")

        # Save cache back
        unified_cache.save_complete_cache(org_name, cache)

        return jsonify({
            "success": True,
            "message": f"Quantitative cache cleared for {org_name}"
        })

    except Exception as e:
        print(f"[UnifiedCache] Error clearing quantitative cache: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@cache_api.route("/cache/unified/clear-qualitative", methods=["POST"])
@require_auth
def clear_unified_qualitative_cache():
    """
    Clear qualitative (AI insights) cache for specific organization.

    This forces regeneration of AI analysis on next page load.
    Useful for re-running AI with updated prompts.

    Request Body:
        {
            "org_name": "Organization Name"
        }

    Returns:
        JSON response with success status
    """
    from src.repositories.unified_cache_repository import get_unified_cache_repository

    try:
        data = request.get_json() or {}
        org_name = data.get("org_name")

        if not org_name:
            return jsonify({"success": False, "error": "org_name is required"}), 400

        # Get unified cache repository
        unified_cache = get_unified_cache_repository()

        # Load full cache
        cache = unified_cache.get_complete_cache(org_name)
        if not cache:
            return jsonify({"success": False, "error": f"No cache found for {org_name}"}), 404

        # Delete qualitative section
        if "qualitative" in cache:
            del cache["qualitative"]
            print(f"[UnifiedCache] Cleared qualitative cache for {org_name}")

        # Save cache back
        unified_cache.save_complete_cache(org_name, cache)

        return jsonify({
            "success": True,
            "message": f"Qualitative (AI) cache cleared for {org_name}"
        })

    except Exception as e:
        print(f"[UnifiedCache] Error clearing qualitative cache: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
