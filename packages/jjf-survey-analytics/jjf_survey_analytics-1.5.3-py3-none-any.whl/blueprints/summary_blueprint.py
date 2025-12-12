"""
Summary Blueprint for JJF Survey Analytics.

Provides summary views of survey responses by stakeholder type.
"""

from flask import Blueprint, render_template

from src.blueprints.auth_blueprint import require_auth
from src.services.container import get_container

# Create blueprint
summary_blueprint = Blueprint("summary", __name__)


@summary_blueprint.route("/summary/organizations")
@require_auth
def summary_organizations():
    """
    Summary view of all organizations from master list.

    Shows intake status and response completion for all organizations.

    Returns:
        Rendered summary template with organization data
    """
    container = get_container()
    data_service = container.data_service
    analytics_service = container.analytics_service

    # Check if data is loaded
    if not data_service.has_data():
        return render_template(
            "simple/summary.html",
            page_title="Organizations",
            summary_type="organizations",
            data=[],
            columns=[],
            error="Data not loaded. Please refresh data first.",
        )

    # Get organizations summary from analytics
    data = analytics_service.get_organizations_summary()

    columns = [
        {"key": "organization", "label": "Organization", "class": "font-semibold text-gray-900"},
        {"key": "email", "label": "Email", "class": "text-gray-600"},
        {"key": "submitted_date", "label": "Intake Date", "class": "text-gray-500"},
        {"key": "status", "label": "Status", "class": "text-center", "badge": True},
    ]

    return render_template(
        "simple/summary.html",
        page_title="Organizations - Intake Submissions",
        summary_type="organizations",
        data=data,
        columns=columns,
        error=None,
    )


@summary_blueprint.route("/summary/ceo")
@require_auth
def summary_ceo():
    """
    Summary view of CEO survey responses.

    Shows all submitted CEO surveys with key response data.

    Returns:
        Rendered summary template with CEO data
    """
    container = get_container()
    data_service = container.data_service
    analytics_service = container.analytics_service

    # Check if data is loaded
    if not data_service.has_data():
        return render_template(
            "simple/summary.html",
            page_title="CEO Surveys",
            summary_type="ceo",
            data=[],
            columns=[],
            error="Data not loaded. Please refresh data first.",
        )

    # Get CEO summary from analytics
    data = analytics_service.get_ceo_summary()

    columns = [
        {"key": "organization", "label": "Organization", "class": "font-semibold text-gray-900"},
        {"key": "name", "label": "CEO Name", "class": "text-gray-700"},
        {"key": "email", "label": "Email", "class": "text-gray-600"},
        {"key": "submitted_date", "label": "Submitted", "class": "text-gray-500"},
        {"key": "vision", "label": "Vision", "class": "text-gray-600 text-sm"},
    ]

    return render_template(
        "simple/summary.html",
        page_title="CEO Survey Responses",
        summary_type="ceo",
        data=data,
        columns=columns,
        error=None,
    )


@summary_blueprint.route("/summary/tech")
@require_auth
def summary_tech():
    """
    Summary view of Tech Lead survey responses.

    Shows all submitted Tech Lead surveys with key response data.

    Returns:
        Rendered summary template with Tech Lead data
    """
    container = get_container()
    data_service = container.data_service
    analytics_service = container.analytics_service

    # Check if data is loaded
    if not data_service.has_data():
        return render_template(
            "simple/summary.html",
            page_title="Tech Lead Surveys",
            summary_type="tech",
            data=[],
            columns=[],
            error="Data not loaded. Please refresh data first.",
        )

    # Get Tech summary from analytics
    data = analytics_service.get_tech_summary()

    columns = [
        {"key": "organization", "label": "Organization", "class": "font-semibold text-gray-900"},
        {"key": "name", "label": "Tech Lead Name", "class": "text-gray-700"},
        {"key": "email", "label": "Email", "class": "text-gray-600"},
        {"key": "submitted_date", "label": "Submitted", "class": "text-gray-500"},
        {"key": "infrastructure", "label": "Infrastructure", "class": "text-gray-600 text-sm"},
    ]

    return render_template(
        "simple/summary.html",
        page_title="Tech Lead Survey Responses",
        summary_type="tech",
        data=data,
        columns=columns,
        error=None,
    )


@summary_blueprint.route("/summary/staff")
@require_auth
def summary_staff():
    """
    Summary view of Staff survey responses.

    Shows all submitted Staff surveys with key response data.

    Returns:
        Rendered summary template with Staff data
    """
    container = get_container()
    data_service = container.data_service
    analytics_service = container.analytics_service

    # Check if data is loaded
    if not data_service.has_data():
        return render_template(
            "simple/summary.html",
            page_title="Staff Surveys",
            summary_type="staff",
            data=[],
            columns=[],
            error="Data not loaded. Please refresh data first.",
        )

    # Get Staff summary from analytics
    data = analytics_service.get_staff_summary()

    columns = [
        {"key": "organization", "label": "Organization", "class": "font-semibold text-gray-900"},
        {"key": "name", "label": "Staff Name", "class": "text-gray-700"},
        {"key": "email", "label": "Email", "class": "text-gray-600"},
        {"key": "submitted_date", "label": "Submitted", "class": "text-gray-500"},
        {"key": "usage", "label": "Usage", "class": "text-gray-600 text-sm"},
    ]

    return render_template(
        "simple/summary.html",
        page_title="Staff Survey Responses",
        summary_type="staff",
        data=data,
        columns=columns,
        error=None,
    )


@summary_blueprint.route("/summary/complete")
@require_auth
def summary_complete():
    """
    Summary view of fully complete organizations.

    Shows organizations that have submitted all required surveys
    (Intake, CEO, Tech, and 3+ Staff).

    Returns:
        Rendered summary template with complete organization data
    """
    container = get_container()
    data_service = container.data_service
    analytics_service = container.analytics_service

    # Check if data is loaded
    if not data_service.has_data():
        return render_template(
            "simple/summary.html",
            page_title="Complete Organizations",
            summary_type="complete",
            data=[],
            columns=[],
            error="Data not loaded. Please refresh data first.",
        )

    # Get complete organizations from analytics
    data = analytics_service.get_complete_organizations()

    columns = [
        {"key": "organization", "label": "Organization", "class": "font-semibold text-gray-900"},
        {"key": "email", "label": "Email", "class": "text-gray-600"},
        {"key": "intake_date", "label": "Intake", "class": "text-gray-500 text-sm"},
        {"key": "ceo_date", "label": "CEO", "class": "text-blue-600 text-sm"},
        {"key": "tech_date", "label": "Tech", "class": "text-purple-600 text-sm"},
        {"key": "staff_date", "label": "Staff", "class": "text-green-600 text-sm"},
    ]

    return render_template(
        "simple/summary.html",
        page_title="Fully Complete Organizations",
        summary_type="complete",
        data=data,
        columns=columns,
        error=None,
    )
