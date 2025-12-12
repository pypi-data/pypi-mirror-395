"""
What's New API Blueprint
Provides endpoints for displaying application changelog and updates
"""

import json
import os
from pathlib import Path
from flask import Blueprint, jsonify
from src.blueprints.auth_blueprint import require_auth

whats_new_api = Blueprint("whats_new_api", __name__)


def get_changelog_path():
    """Get path to changelog JSON file."""
    return Path(__file__).parent.parent.parent / "services" / "whats_new_changelog.json"


@whats_new_api.route("/api/whats-new/current", methods=["GET"])
@require_auth
def get_current_changelog():
    """
    Get current changelog data.

    Returns:
        JSON: Current version changelog with highlights, changes, and action items
    """
    try:
        changelog_path = get_changelog_path()

        if not changelog_path.exists():
            return jsonify({
                "error": "Changelog not found",
                "version": None
            }), 404

        with open(changelog_path, 'r', encoding='utf-8') as f:
            changelog_data = json.load(f)

        return jsonify(changelog_data)

    except json.JSONDecodeError as e:
        return jsonify({
            "error": f"Invalid changelog format: {str(e)}",
            "version": None
        }), 500

    except Exception as e:
        return jsonify({
            "error": f"Failed to load changelog: {str(e)}",
            "version": None
        }), 500


@whats_new_api.route("/api/whats-new/history", methods=["GET"])
@require_auth
def get_changelog_history():
    """
    Get changelog history (future feature).

    Currently returns only the current changelog.
    In the future, this could return a list of all historical changelogs.

    Returns:
        JSON: List of changelog entries
    """
    try:
        changelog_path = get_changelog_path()

        if not changelog_path.exists():
            return jsonify({
                "error": "Changelog not found",
                "changelogs": []
            }), 404

        with open(changelog_path, 'r', encoding='utf-8') as f:
            current_changelog = json.load(f)

        # For now, return current changelog as single-item list
        # Future: Load multiple changelog versions from a history file
        return jsonify({
            "changelogs": [current_changelog]
        })

    except Exception as e:
        return jsonify({
            "error": f"Failed to load changelog history: {str(e)}",
            "changelogs": []
        }), 500
