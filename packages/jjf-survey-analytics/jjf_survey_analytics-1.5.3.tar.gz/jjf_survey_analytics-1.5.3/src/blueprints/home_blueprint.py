"""
Home Blueprint for JJF Survey Analytics.

Provides the main dashboard/landing page with participation overview.
"""

from flask import Blueprint, render_template

from src.blueprints.auth_blueprint import require_auth
from src.services.container import get_container

# Create blueprint
home_blueprint = Blueprint("home", __name__)


@home_blueprint.route("/")
@require_auth
def index():
    """
    Home page with organization participation dashboard.

    Displays overview statistics and participation metrics using the legacy dashboard.
    Requires authentication.

    Returns:
        Rendered simple/home.html template with organization participation data
    """
    container = get_container()

    # Get basic stats using the DataService API
    try:
        metadata = container.data_service.get_metadata()
        data_ready = metadata.get("has_data", False)
        stats = {
            "has_data": data_ready,
            "tab_count": metadata.get("tab_count", 0),
            "total_rows": metadata.get("total_rows", 0),
        }
    except Exception as e:
        print(f"[HOME] Error getting metadata: {e}")
        data_ready = False
        stats = {"has_data": False}

    # Build dashboard data using analytics service
    dashboard_data = {}
    if data_ready:
        analytics_service = container.analytics_service
        dashboard_data = {
            "overview": analytics_service.get_participation_overview(),
            "organizations": analytics_service.get_organizations_status(),
            "activity": analytics_service.get_latest_activity(),
            "funnel": analytics_service.get_funnel_data(),
        }

    # Render the LEGACY template
    return render_template(
        "simple/home.html", db_ready=data_ready, stats=stats, dashboard=dashboard_data
    )
