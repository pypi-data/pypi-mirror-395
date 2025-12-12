"""
Data Blueprint for JJF Survey Analytics.

Provides data viewing and navigation routes for survey data tabs.
"""

from flask import Blueprint, render_template

from src.blueprints.auth_blueprint import require_auth
from src.extractors.sheets_reader import SheetsReader
from src.services.container import get_container

# Create blueprint
data_blueprint = Blueprint("data", __name__)


@data_blueprint.route("/data")
@require_auth
def data_nav():
    """
    Data navigation page with links to all survey data tabs.

    Shows list of available tabs with row counts and last extract time.

    Returns:
        Rendered data navigation template
    """
    container = get_container()
    data_service = container.data_service

    # Check if data is loaded
    if not data_service.has_data():
        return render_template(
            "simple/data_nav.html", tabs=[], error="Data not loaded. Please refresh data first."
        )

    # Get metadata
    metadata = data_service.get_metadata()
    last_fetch = metadata.get("last_fetch", "")

    # Build tabs list with row counts
    tabs = []
    for tab_name in SheetsReader.TABS.keys():
        row_count = len(data_service.get_tab_data(tab_name))
        tabs.append({"name": tab_name, "row_count": row_count, "last_extract": last_fetch})

    return render_template("simple/data_nav.html", tabs=tabs, error=None)


@data_blueprint.route("/data/<tab_name>")
@require_auth
def view_tab(tab_name: str):
    """
    Display specific survey data tab in table format.

    Shows all rows and columns for the requested tab with row indices.

    Args:
        tab_name: Name of the tab to display

    Returns:
        Rendered tab view template with data
    """
    container = get_container()
    data_service = container.data_service

    # Check if data is loaded
    if not data_service.has_data():
        return render_template(
            "simple/tab_view.html",
            tab_name=tab_name,
            data=[],
            columns=[],
            error="Data not loaded. Please refresh data first.",
        )

    # Get tab data
    data = data_service.get_tab_data(tab_name)

    if not data:
        return render_template(
            "simple/tab_view.html",
            tab_name=tab_name,
            data=[],
            columns=[],
            error=f"No data found for tab '{tab_name}'",
        )

    # Add row index to each row
    indexed_data = []
    for i, row in enumerate(data, 1):
        row_copy = row.copy()
        row_copy["_row_index"] = i
        indexed_data.append(row_copy)

    # Collect all unique columns
    columns = ["_row_index"]
    for row in indexed_data:
        for key in row.keys():
            if key not in columns and key != "_row_index":
                columns.append(key)

    return render_template(
        "simple/tab_view.html", tab_name=tab_name, data=indexed_data, columns=columns, error=None
    )
