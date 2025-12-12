"""
Admin Edit API Blueprint for JJF Survey Analytics.

Provides API endpoints for saving and retrieving admin edits to organization reports.
"""

import io
import json
from datetime import datetime

from flask import Blueprint, jsonify, request, send_file

from src.blueprints.auth_blueprint import require_auth
from src.services.container import get_container

# Create blueprint
admin_edit_api = Blueprint("admin_edit_api", __name__, url_prefix="/api/admin")


@admin_edit_api.route("/edits/<org_name>", methods=["GET"])
@require_auth
def get_admin_edits(org_name: str):
    """
    Get admin edits for an organization.

    Args:
        org_name: Name of the organization

    Returns:
        JSON response with admin edits
    """
    container = get_container()
    admin_edit_service = container.admin_edit_service

    try:
        edits = admin_edit_service.get_org_edits(org_name)
        return jsonify({"success": True, "edits": edits})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@admin_edit_api.route("/edits/<org_name>/summary", methods=["POST"])
@require_auth
def save_summary_edits(org_name: str):
    """
    Save summary title and body edits for an organization.

    Request Body:
        {
            "title": "Custom summary title",
            "body": "Custom summary body text"
        }

    Args:
        org_name: Name of the organization

    Returns:
        JSON response with success status
    """
    container = get_container()
    admin_edit_service = container.admin_edit_service
    cache_service = container.cache_service

    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        edits = {}
        if "title" in data:
            edits["summary_title"] = data["title"]
        if "body" in data:
            edits["summary_body"] = data["body"]

        success = admin_edit_service.save_org_edits(org_name, edits)

        if success:
            # Clear in-memory report cache
            cache_service.clear_org_report(org_name)
            print(f"[Cache] Cleared cached report for {org_name} due to summary edit")

            # Clear persistent quantitative cache
            from src.repositories.qualitative_cache_file_repository import get_qualitative_cache_file_repository
            cache_repo = get_qualitative_cache_file_repository()
            cache_repo.invalidate_quantitative_report(org_name)

            return jsonify({"success": True, "message": "Summary edits saved successfully"})
        else:
            return jsonify({"success": False, "error": "Failed to save edits"}), 500

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@admin_edit_api.route("/edits/<org_name>/modifiers", methods=["POST"])
@require_auth
def save_modifier_edits(org_name: str):
    """
    Save score modifier edits for an organization.

    Returns updated calculation breakdown data for immediate UI update (JJF-46).

    Request Body:
        {
            "dimension": "Program Technology",
            "modifiers": [
                {"label": "+5%", "value": 0.05, "description": "Strong vision"},
                {"label": "-3%", "value": -0.03, "description": "Limited budget"}
            ]
        }

    Args:
        org_name: Name of the organization

    Returns:
        JSON response with success status and calculation breakdown data
    """
    container = get_container()
    admin_edit_service = container.admin_edit_service
    cache_service = container.cache_service
    report_service = container.report_service

    try:
        data = request.get_json()
        if not data or "dimension" not in data or "modifiers" not in data:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": 'Invalid data format. Expected: {"dimension": "...", "modifiers": [...]}',
                    }
                ),
                400,
            )

        dimension = data["dimension"]
        modifiers = data["modifiers"]

        # Save modifier edits
        success = admin_edit_service.update_score_modifiers(org_name, dimension, modifiers)

        if success:
            # Clear in-memory report cache
            cache_service.clear_org_report(org_name)
            print(f"[Cache] Cleared cached report for {org_name} due to modifier edit")

            # Clear persistent quantitative cache
            from src.repositories.qualitative_cache_file_repository import get_qualitative_cache_file_repository
            cache_repo = get_qualitative_cache_file_repository()
            cache_repo.invalidate_quantitative_report(org_name)

            # JJF-46: Get updated calculation breakdown data
            # Use skip_ai=True for fast response (~50-100ms)
            report = report_service.get_organization_report(org_name, skip_ai=True)

            if report and "ai_insights" in report:
                ai_insights = report["ai_insights"]

                # Extract dimension-specific calculation data
                dimension_key = dimension.replace(" ", "_")
                dimension_data = ai_insights.get("dimensions", {}).get(dimension_key, {})

                breakdown_data = {
                    "modifier_summary": dimension_data.get("modifier_summary", {}),
                    "impact_summary": dimension_data.get("impact_summary", {}),
                    "modifiers": dimension_data.get("modifiers", [])
                }

                # Extract total impact summary (for aggregate section)
                total_impact_summary = ai_insights.get("total_impact_summary", {})

                return jsonify({
                    "success": True,
                    "message": f"Score modifiers saved for {dimension}",
                    "dimension": dimension,
                    "breakdown": breakdown_data,
                    "total_impact_summary": total_impact_summary
                })
            else:
                # Fallback if report generation fails
                return jsonify({
                    "success": True,
                    "message": f"Score modifiers saved for {dimension}"
                })

        else:
            return jsonify({"success": False, "error": "Failed to save modifier edits"}), 500

    except Exception as e:
        print(f"[Admin Edit API] Error saving modifiers: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@admin_edit_api.route("/edits/<org_name>/dimension-insight", methods=["POST"])
@require_auth
def save_dimension_insight_edit(org_name: str):
    """
    Save dimension insight edit for an organization.

    Request Body:
        {
            "dimension": "Program Technology",
            "insight": "Custom insight text for this dimension"
        }

    Args:
        org_name: Name of the organization

    Returns:
        JSON response with success status
    """
    container = get_container()
    admin_edit_service = container.admin_edit_service
    cache_service = container.cache_service

    try:
        data = request.get_json()
        if not data or "dimension" not in data or "insight" not in data:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": 'Invalid data format. Expected: {"dimension": "...", "insight": "..."}',
                    }
                ),
                400,
            )

        dimension = data["dimension"]
        insight = data["insight"]

        # Save dimension insight
        success = admin_edit_service.update_dimension_insight(org_name, dimension, insight)

        if success:
            # Clear in-memory report cache
            cache_service.clear_org_report(org_name)
            print(f"[Cache] Cleared cached report for {org_name} due to dimension insight edit")

            # Clear persistent quantitative cache
            from src.repositories.qualitative_cache_file_repository import get_qualitative_cache_file_repository
            cache_repo = get_qualitative_cache_file_repository()
            cache_repo.invalidate_quantitative_report(org_name)

            return jsonify({"success": True, "message": f"Dimension insight saved for {dimension}"})
        else:
            return jsonify({"success": False, "error": "Failed to save dimension insight"}), 500

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@admin_edit_api.route("/edits/<org_name>/download", methods=["GET"])
@require_auth
def download_org_modifications(org_name: str):
    """
    Download all modifications for an organization as a JSON file.

    This creates a downloadable JSON file containing all user modifications
    (summary edits, score modifiers, dimension insights) for backup purposes.

    Args:
        org_name: Name of the organization

    Returns:
        JSON file download with modifications
    """
    container = get_container()
    admin_edit_service = container.admin_edit_service

    try:
        # Get all edits for this organization
        edits = admin_edit_service.get_org_edits(org_name)

        # Create metadata
        modifications = {
            "metadata": {
                "organization": org_name,
                "exported_at": datetime.now().isoformat(),
                "version": "1.0",
                "format": "jjf-survey-modifications",
            },
            "modifications": edits,
        }

        # Convert to JSON
        json_data = json.dumps(modifications, indent=2)

        # Create file-like object
        json_bytes = io.BytesIO(json_data.encode("utf-8"))

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_org_name = org_name.replace(" ", "_").replace("/", "_")
        filename = f"{safe_org_name}_modifications_{timestamp}.json"

        # Send file
        return send_file(
            json_bytes, mimetype="application/json", as_attachment=True, download_name=filename
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@admin_edit_api.route("/edits/<org_name>/upload", methods=["POST"])
@require_auth
def upload_org_modifications(org_name: str):
    """
    Upload and restore modifications for an organization from a JSON file.

    This allows users to restore previously saved modifications if the server
    version becomes corrupted or lost.

    Request:
        File upload with 'file' field containing JSON modifications

    Args:
        org_name: Name of the organization

    Returns:
        JSON response with success status
    """
    container = get_container()
    admin_edit_service = container.admin_edit_service
    cache_service = container.cache_service

    try:
        # Check if file was uploaded
        if "file" not in request.files:
            return jsonify({"success": False, "error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"success": False, "error": "No file selected"}), 400

        # Read and parse JSON
        try:
            json_data = json.load(file)
        except json.JSONDecodeError as e:
            return jsonify({"success": False, "error": f"Invalid JSON file: {str(e)}"}), 400

        # Validate structure
        if "metadata" not in json_data or "modifications" not in json_data:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Invalid file format. Expected metadata and modifications fields.",
                    }
                ),
                400,
            )

        # Validate organization matches
        if json_data["metadata"].get("organization") != org_name:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"File is for organization '{json_data['metadata'].get('organization')}' but you're uploading to '{org_name}'",
                    }
                ),
                400,
            )

        # Validate format version
        if json_data["metadata"].get("format") != "jjf-survey-modifications":
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Invalid file format. Expected jjf-survey-modifications format.",
                    }
                ),
                400,
            )

        # Extract modifications
        modifications = json_data["modifications"]

        # Validate modifications structure
        required_fields = ["summary_title", "summary_body", "score_modifiers", "dimension_insights"]
        for field in required_fields:
            if field not in modifications:
                return jsonify({"success": False, "error": f"Missing required field: {field}"}), 400

        # Save modifications
        success = admin_edit_service.save_org_edits(org_name, modifications)

        if success:
            # Clear in-memory report cache
            cache_service.clear_org_report(org_name)
            print(f"[Admin Edits] Restored modifications for {org_name} from uploaded file")
            print(f"[Cache] Cleared cached report for {org_name} due to modification restore")

            # Clear persistent quantitative cache
            from src.repositories.qualitative_cache_file_repository import get_qualitative_cache_file_repository
            cache_repo = get_qualitative_cache_file_repository()
            cache_repo.invalidate_quantitative_report(org_name)

            return jsonify(
                {
                    "success": True,
                    "message": "Modifications restored successfully",
                    "restored_from": json_data["metadata"].get("exported_at"),
                    "summary": {
                        "has_summary_title": modifications.get("summary_title") is not None,
                        "has_summary_body": modifications.get("summary_body") is not None,
                        "modifier_dimensions": list(
                            modifications.get("score_modifiers", {}).keys()
                        ),
                        "insight_dimensions": list(
                            modifications.get("dimension_insights", {}).keys()
                        ),
                    },
                }
            )
        else:
            return jsonify({"success": False, "error": "Failed to save modifications"}), 500

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@admin_edit_api.route("/edits/download-all", methods=["GET"])
@require_auth
def download_all_modifications():
    """
    Download all modifications for all organizations as a single JSON file.

    This creates a complete backup of all user modifications across all organizations.

    Returns:
        JSON file download with all modifications
    """
    container = get_container()
    admin_edit_service = container.admin_edit_service

    try:
        # Get all edits
        all_edits = admin_edit_service.get_all_edits()

        # Create metadata
        modifications = {
            "metadata": {
                "exported_at": datetime.now().isoformat(),
                "version": "1.0",
                "format": "jjf-survey-modifications-bulk",
                "organization_count": len(all_edits),
            },
            "organizations": all_edits,
        }

        # Convert to JSON
        json_data = json.dumps(modifications, indent=2)

        # Create file-like object
        json_bytes = io.BytesIO(json_data.encode("utf-8"))

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"all_modifications_{timestamp}.json"

        # Send file
        return send_file(
            json_bytes, mimetype="application/json", as_attachment=True, download_name=filename
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
