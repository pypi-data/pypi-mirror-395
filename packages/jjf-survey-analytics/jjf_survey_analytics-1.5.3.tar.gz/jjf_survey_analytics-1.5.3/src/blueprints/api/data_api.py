"""
Data API Blueprint for JJF Survey Analytics.

Provides API endpoints for data refresh and extraction operations.
"""

from flask import Blueprint, jsonify

from src.blueprints.auth_blueprint import require_auth
from src.services.container import get_container

# Create blueprint
data_api = Blueprint("data_api", __name__, url_prefix="/api")


@data_api.route("/refresh", methods=["GET", "POST"])
@require_auth
def api_refresh():
    """
    Refresh data from Google Sheets and clear report cache.

    Accepts both GET and POST requests for flexibility.

    Returns:
        JSON response with refresh status and statistics
    """
    container = get_container()
    data_service = container.data_service
    cache_service = container.cache_service

    try:
        # Refresh data from Google Sheets
        data_service.refresh_data(verbose=True)

        # Get updated statistics
        stats = data_service.get_metadata()

        # Clear all caches when data is refreshed
        cache_service.clear_all()
        print("[Cache] Cleared all caches after data refresh")

        return jsonify(
            {
                "success": True,
                "message": "Data refreshed successfully from Google Sheets",
                "stats": stats,
                "cache_cleared": True,
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@data_api.route("/extract", methods=["GET", "POST"])
@require_auth
def api_extract():
    """
    Alias for /api/refresh for backward compatibility.

    Returns:
        JSON response with refresh status and statistics
    """
    return api_refresh()


@data_api.route("/data/refresh", methods=["POST"])
@require_auth
def api_data_refresh():
    """
    Force refresh of data from Google Sheets.

    Bypasses cache and fetches fresh data.

    Returns:
        JSON response with refresh status
    """
    container = get_container()
    data_service = container.data_service
    cache_service = container.cache_service

    try:
        # Force refresh data (bypass cache)
        data_service.refresh_data(verbose=True)

        # Clear all caches
        cache_service.clear_all()

        return jsonify(
            {"success": True, "message": "Data force-refreshed successfully", "cache_cleared": True}
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
