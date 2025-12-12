"""
Authentication Blueprint for JJF Survey Analytics.

Demonstrates the service integration pattern using dependency injection container.
All future blueprints should follow this pattern.

Pattern:
    1. Import container via get_container()
    2. Access services through container properties
    3. Use services for business logic
    4. Keep routes thin - delegate to services

Example:
    from src.blueprints.auth_blueprint import auth_blueprint, require_auth

    app.register_blueprint(auth_blueprint)

    @app.route('/protected')
    @require_auth
    def protected_route():
        return "Authenticated content"
"""

import os
from functools import wraps

from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for

# Import container for service access
from src.services.container import get_container

# Create blueprint
auth_blueprint = Blueprint("auth", __name__)


def require_auth(f):
    """
    Authentication decorator.

    Protects routes by checking if user is authenticated.
    Redirects to login page if not authenticated.

    Usage:
        @app.route('/protected')
        @require_auth
        def protected_route():
            return "Authenticated content"

    Args:
        f: Function to wrap

    Returns:
        Wrapped function with authentication check
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import current_app

        # Check if authentication is required via config
        if current_app.config.get("REQUIRE_AUTH", True):
            if "authenticated" not in session:
                # Check if this is an API request (path starts with /api/)
                if request.path.startswith("/api/"):
                    # Return JSON for API requests
                    return jsonify({"error": "Authentication required"}), 401
                else:
                    # Redirect to login for browser requests
                    return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login.

    GET: Show login form
    POST: Process login credentials and authenticate user

    Demonstrates container usage pattern for accessing services.

    Returns:
        GET: Rendered login template
        POST: Redirect to index on success, login form with error on failure
    """
    # Get container (demonstrates pattern for other blueprints)
    container = get_container()

    # Check if already authenticated
    if "authenticated" in session:
        return redirect(url_for("home.index"))

    if request.method == "POST":
        password = request.form.get("password", "")

        # Get expected password from environment
        expected_password = os.environ.get("ADMIN_PASSWORD", "survey2025!")

        if password == expected_password:
            session["authenticated"] = True
            session.permanent = True

            # Example: Log authentication event using analytics service
            # This demonstrates how services are accessed in blueprints
            try:
                # Get analytics service from container
                container.analytics_service

                # Services could track login events, user activity, etc.
                # analytics_service.log_event('login', {'timestamp': datetime.now()})
                # For now, this is just a demonstration of the pattern

            except Exception as e:
                # Log error but don't fail authentication
                print(f"Warning: Failed to log authentication event: {e}")

            return redirect(url_for("home.index"))
        else:
            return render_template("login.html", error="Invalid password")

    return render_template("login.html")


@auth_blueprint.route("/logout", methods=["GET", "POST"])
def logout():
    """
    Handle user logout.

    Clears session and redirects to login page.
    Accepts both GET and POST for flexibility.

    Returns:
        Redirect to login page
    """
    # Get container
    get_container()

    # Example: Log logout event
    # analytics_service = container.analytics_service
    # analytics_service.log_event('logout', {'timestamp': datetime.now()})

    # Clear session
    session.pop("authenticated", None)

    return redirect(url_for("auth.login"))


@auth_blueprint.route("/auth/status")
@require_auth
def auth_status():
    """
    API endpoint to check authentication status.

    Demonstrates:
    - Protected route with @require_auth decorator
    - Container usage for accessing services
    - JSON API response pattern

    Returns:
        JSON response with authentication status and container information
    """
    container = get_container()

    return jsonify(
        {
            "authenticated": True,
            "container_status": container.get_status(),
            "message": "User is authenticated",
        }
    )


@auth_blueprint.route("/auth/services")
@require_auth
def auth_services():
    """
    API endpoint to demonstrate service access pattern.

    Shows how blueprints can access multiple services through container.
    This is a proof-of-concept endpoint to validate the integration pattern.

    Returns:
        JSON response with service information
    """
    container = get_container()

    # Demonstrate accessing multiple services
    try:
        # Get cache service
        cache_service = container.cache_service
        cache_stats = cache_service.get_stats()

        # Get data service
        data_service = container.data_service
        data_stats = data_service.get_stats()

        # Get algorithm config service
        config_service = container.algorithm_config_service
        config_metadata = config_service.get_metadata()

        return jsonify(
            {
                "success": True,
                "services": {
                    "cache": {"initialized": True, "stats": cache_stats},
                    "data": {"initialized": True, "stats": data_stats},
                    "algorithm_config": {"initialized": True, "metadata": config_metadata},
                },
                "container_status": container.get_status(),
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
