"""
Blueprint registration module.

Central location for registering all Flask blueprints.
Provides clean dependency injection pattern for all blueprints.
"""

from flask import Flask

from src.services.container import Container


def register_blueprints(app: Flask, container: Container) -> None:
    """
    Register all Flask blueprints with the app.

    Registers both page blueprints and API blueprints.
    Stores container in app config for global access.

    Args:
        app: Flask application instance
        container: Dependency injection container

    Example:
        app = Flask(__name__)
        container = get_container()
        register_blueprints(app, container)
    """
    # Import page blueprints
    from src.blueprints.admin_blueprint import admin_blueprint
    from src.blueprints.api.admin_edit_api import admin_edit_api
    from src.blueprints.api.algorithm_config_api import algorithm_config_api
    from src.blueprints.api.cache_api import cache_api

    # Import API blueprints
    from src.blueprints.api.data_api import data_api
    from src.blueprints.api.debug_api import debug_api
    from src.blueprints.api.help_api import help_api
    from src.blueprints.api.report_api import report_api
    from src.blueprints.api.stats_api import stats_api
    from src.blueprints.api.whats_new_api import whats_new_api
    from src.blueprints.auth_blueprint import auth_blueprint
    from src.blueprints.data_blueprint import data_blueprint
    from src.blueprints.health_blueprint import health_blueprint
    from src.blueprints.home_blueprint import home_blueprint
    from src.blueprints.report_blueprint import report_blueprint
    from src.blueprints.summary_blueprint import summary_blueprint

    # Register page blueprints
    app.register_blueprint(home_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(data_blueprint)
    app.register_blueprint(summary_blueprint)
    app.register_blueprint(report_blueprint)
    app.register_blueprint(health_blueprint)

    # Register API blueprints
    app.register_blueprint(data_api)
    app.register_blueprint(debug_api)
    app.register_blueprint(report_api)
    app.register_blueprint(cache_api)
    app.register_blueprint(stats_api)
    app.register_blueprint(admin_edit_api)
    app.register_blueprint(algorithm_config_api)
    app.register_blueprint(help_api)
    app.register_blueprint(whats_new_api)

    # Store container in app config for global access
    app.config["CONTAINER"] = container

    print("✓ Registered 15 blueprints:")
    print("  - Page blueprints: home, auth, admin, data, summary, report, health")
    print(
        "  - API blueprints: data_api, report_api, cache_api, stats_api, admin_edit_api, algorithm_config_api, help_api, whats_new_api"
    )
