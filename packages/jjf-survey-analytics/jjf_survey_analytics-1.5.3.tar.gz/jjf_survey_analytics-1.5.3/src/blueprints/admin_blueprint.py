"""
Admin Blueprint for JJF Survey Analytics.

Provides administrative functions for data management and cache control.
"""

from flask import Blueprint, render_template

from src.blueprints.auth_blueprint import require_auth
from src.services.container import get_container

# Create blueprint
admin_blueprint = Blueprint("admin", __name__)


@admin_blueprint.route("/admin")
@require_auth
def admin():
    """
    Admin dashboard page with data management functions.

    Shows current data statistics and management controls.

    Returns:
        Rendered admin template with statistics
    """
    container = get_container()
    data_service = container.data_service

    # Get statistics from data service
    stats = data_service.get_metadata()

    return render_template("simple/admin.html", stats=stats)


@admin_blueprint.route("/admin/cache")
@require_auth
def cache_management():
    """
    Cache management page.

    Provides interface for managing report cache and Google Sheets cache.

    Returns:
        Rendered cache management template
    """
    # No service calls needed - template handles cache UI
    return render_template("simple/cache_management.html")
