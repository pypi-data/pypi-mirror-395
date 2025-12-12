"""
Algorithm Config API Blueprint for JJF Survey Analytics.

Provides API endpoints for managing algorithm configuration.
"""

from flask import Blueprint, jsonify, request

from src.blueprints.auth_blueprint import require_auth
from src.services.container import get_container

# Create blueprint
algorithm_config_api = Blueprint("algorithm_config_api", __name__, url_prefix="/api")


@algorithm_config_api.route("/algorithm-config", methods=["GET"])
@require_auth
def get_algorithm_config():
    """
    Get the current algorithm configuration.

    Returns:
        JSON response with algorithm configuration and metadata
    """
    container = get_container()
    algorithm_config_service = container.algorithm_config_service

    try:
        config = algorithm_config_service.get_config()

        # Service returns config directly, not a response wrapper
        return jsonify(
            {"success": True, "config": config, "version": config.get("version", "unknown")}
        )

    except Exception as e:
        print(f"Error loading algorithm config: {e}")
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@algorithm_config_api.route("/algorithm-config", methods=["POST"])
@require_auth
def update_algorithm_config():
    """
    Update the algorithm configuration.

    Request Body:
        {
            "config": {...},  // Complete new configuration
            "change_note": "Description of changes"  // Optional
        }

    Returns:
        JSON response with success status and backup information
    """
    container = get_container()
    algorithm_config_service = container.algorithm_config_service

    try:
        data = request.get_json()

        if not data or "config" not in data:
            return jsonify({"success": False, "error": "Missing config in request body"}), 400

        new_config = data["config"]
        change_note = data.get("change_note", "Configuration updated via admin panel")

        # Update configuration (includes validation and backup)
        # Service returns tuple: (success: bool, validation_result: Optional[Dict])
        success, validation_result = algorithm_config_service.update_config(
            new_config, validate=True
        )

        if success:
            # Create backup after successful update
            backup_filename = algorithm_config_service.create_backup()
            return jsonify(
                {
                    "success": True,
                    "message": "Configuration updated successfully",
                    "backup_created": backup_filename,
                    "change_note": change_note,
                }
            )
        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Configuration validation failed",
                        "validation_result": validation_result,
                    }
                ),
                400,
            )

    except Exception as e:
        print(f"Error updating algorithm config: {e}")
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@algorithm_config_api.route("/algorithm-config/history", methods=["GET"])
@require_auth
def get_algorithm_config_history():
    """
    Get the change history for algorithm configuration.

    Returns:
        JSON response with change log and available backups
    """
    container = get_container()
    algorithm_config_service = container.algorithm_config_service

    try:
        history = algorithm_config_service.get_history()
        backups = algorithm_config_service.list_backups()

        return jsonify({"success": True, "history": history, "backups": backups})

    except Exception as e:
        print(f"Error getting algorithm config history: {e}")
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@algorithm_config_api.route("/algorithm-config/backup/<filename>", methods=["GET"])
@require_auth
def download_algorithm_config_backup(filename: str):
    """
    Download a specific backup file.

    Args:
        filename: Name of the backup file

    Returns:
        JSON file download or error response
    """
    container = get_container()
    algorithm_config_service = container.algorithm_config_service

    try:
        # Service returns config directly or raises ValueError if not found
        backup_config = algorithm_config_service.get_backup(filename)

        return jsonify({"success": True, "config": backup_config, "filename": filename})

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        print(f"Error downloading algorithm config backup: {e}")
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500
