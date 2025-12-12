"""
Health Check Blueprint for JJF Survey Analytics.

Provides health check endpoints for monitoring and deployment verification.
Used by Railway and other deployment platforms to verify application status.
"""

import os

from flask import Blueprint, jsonify

from src.services.container import get_container
from src.utils.cache_version import get_cache_metadata
from src.utils.version import get_version_info, get_version_string

# Create blueprint
health_blueprint = Blueprint("health", __name__)


@health_blueprint.route("/health")
def health_check():
    """
    Health check endpoint for deployment monitoring.

    Returns application status, version, and component health information.
    Used by Railway health checks and monitoring systems.

    Returns:
        JSON response with:
        - status: 'healthy' if application is running
        - version: Application version string
        - components: Status of key application components
        - environment: Deployment environment information

    Example Response:
        {
            "status": "healthy",
            "version": "1.2.0",
            "components": {
                "data_service": true,
                "cache_service": true,
                "analytics_service": false
            },
            "environment": {
                "railway": true,
                "flask_env": "production"
            }
        }
    """
    try:
        # Get container to check service initialization
        container = get_container()

        # Get component status
        container_status = container.get_status()

        # Get version information
        version_info = get_version_info()

        # Get cache metadata
        try:
            cache_meta = get_cache_metadata()
            cache_status = {
                "version": cache_meta.get("cache_version"),
                "timestamp": cache_meta.get("timestamp"),
            }
        except Exception:
            cache_status = None

        # Build health response
        health_data = {
            "status": "healthy",
            "version": get_version_string(),
            "git_branch": version_info.get("git_branch"),
            "git_commit": version_info.get("git_commit"),
            "components": {
                "data_service": container_status.get("data_service", False),
                "cache_service": container_status.get("cache_service", False),
                "analytics_service": container_status.get("analytics_service", False),
                "admin_edit_service": container_status.get("admin_edit_service", False),
                "algorithm_config_service": container_status.get("algorithm_config_service", False),
            },
            "repositories": {
                "sheet_repository": container_status.get("sheet_repository", False),
                "report_repository": container_status.get("report_repository", False),
                "admin_edit_repository": container_status.get("admin_edit_repository", False),
            },
            "cache": cache_status,
            "environment": {
                "railway": bool(os.getenv("RAILWAY_ENVIRONMENT")),
                "flask_env": os.getenv("FLASK_ENV", "development"),
                "port": os.getenv("PORT", "8080"),
            },
        }

        return jsonify(health_data)

    except Exception as e:
        # Return unhealthy status if health check fails
        return (
            jsonify({"status": "unhealthy", "error": str(e), "version": get_version_string()}),
            503,
        )  # Service Unavailable


@health_blueprint.route("/health/ready")
def readiness_check():
    """
    Readiness check endpoint.

    Verifies that application is ready to serve requests.
    Checks that critical services are initialized.

    Returns:
        JSON response with:
        - ready: boolean indicating if app is ready
        - services_ready: dictionary of service initialization status

    Returns 503 if not ready, 200 if ready.
    """
    try:
        container = get_container()
        status = container.get_status()

        # Check critical services
        critical_services = [
            "data_service",
            "cache_service",
        ]

        all_ready = all(status.get(service, False) for service in critical_services)

        if all_ready:
            return jsonify({"ready": True, "services_ready": status})
        else:
            return (
                jsonify(
                    {
                        "ready": False,
                        "services_ready": status,
                        "message": "Some critical services not initialized",
                    }
                ),
                503,
            )

    except Exception as e:
        return jsonify({"ready": False, "error": str(e)}), 503


@health_blueprint.route("/health/live")
def liveness_check():
    """
    Liveness check endpoint.

    Simple check that application process is alive.
    Should return 200 as long as Flask is responding.

    Returns:
        JSON response with alive status
    """
    return jsonify({"alive": True, "version": get_version_string()})
