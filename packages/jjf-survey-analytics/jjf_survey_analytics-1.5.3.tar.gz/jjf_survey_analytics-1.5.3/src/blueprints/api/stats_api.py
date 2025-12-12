"""
Stats API Blueprint for JJF Survey Analytics.

Provides API endpoints for statistics and response rate data.
"""

from flask import Blueprint, jsonify

from src.blueprints.auth_blueprint import require_auth
from src.services.container import get_container

# Create blueprint
stats_api = Blueprint("stats_api", __name__, url_prefix="/api")


@stats_api.route("/stats")
@require_auth
def api_stats():
    """
    Get basic statistics about loaded data.

    Returns:
        JSON response with data statistics
    """
    container = get_container()
    data_service = container.data_service

    try:
        stats = data_service.get_metadata()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@stats_api.route("/response-rates")
@require_auth
def api_response_rates():
    """
    Get response rates for all organizations.

    Returns:
        JSON response with response rate data
    """
    container = get_container()
    analytics_service = container.analytics_service

    try:
        response_rates = analytics_service.get_response_rates()
        return jsonify(response_rates)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
