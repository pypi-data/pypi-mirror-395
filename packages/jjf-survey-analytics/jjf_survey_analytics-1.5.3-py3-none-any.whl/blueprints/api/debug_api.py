"""
Debug API for diagnosing cache issues.
TEMPORARY - For troubleshooting production cache structure.
"""

from flask import Blueprint, jsonify

from src.blueprints.auth_blueprint import require_auth
from src.repositories.unified_cache_repository import get_unified_cache_repository
from src.services.container import get_container

debug_api = Blueprint("debug_api", __name__, url_prefix="/api/debug")


@debug_api.route("/cache/<org_name>")
@require_auth
def inspect_cache(org_name: str):
    """
    Inspect unified cache structure for debugging.

    Returns complete cache structure to diagnose data loading issues.
    """
    try:
        unified_cache = get_unified_cache_repository()

        # Load full cache
        cache = unified_cache._load_cache(org_name)

        if not cache:
            return jsonify({
                "error": "Cache not found",
                "org_name": org_name
            }), 404

        # Get quantitative data (what report service sees)
        quant_data = unified_cache.get_quantitative_data(org_name)

        return jsonify({
            "success": True,
            "org_name": org_name,
            "cache_keys": list(cache.keys()) if cache else [],
            "quantitative_keys": list(quant_data.keys()) if quant_data else [],
            "has_header": "header" in quant_data if quant_data else False,
            "has_maturity": "maturity" in quant_data if quant_data else False,
            "overall_score": quant_data.get("maturity", {}).get("overall_score") if quant_data else None,
            "maturity_level": quant_data.get("maturity", {}).get("maturity_level") if quant_data else None,
            "cache_version": cache.get("version") if cache else None,
            "cache_updated_at": cache.get("updated_at") if cache else None,
            "full_quantitative_sample": {
                "header": quant_data.get("header") if quant_data else None,
                "maturity_keys": list(quant_data.get("maturity", {}).keys()) if quant_data else [],
                "variance_analysis_keys": list(quant_data.get("maturity", {}).get("variance_analysis", {}).keys()) if quant_data else []
            }
        })

    except Exception as e:
        import traceback
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


@debug_api.route("/dimension-scores/<org_name>")
@require_auth
def inspect_dimension_scores_api(org_name: str):
    """
    Test the dimension-scores API that JavaScript calls.

    This is the API that populates window.baseScores.
    If it returns empty, the score defaults to 1.0.
    """
    import requests
    from flask import request as flask_request

    try:
        # Make internal request to the API
        base_url = flask_request.url_root.rstrip('/')
        api_url = f"{base_url}/api/report/org/{org_name}/dimension-scores"

        response = requests.get(api_url, cookies=flask_request.cookies)

        return jsonify({
            "success": True,
            "api_url": api_url,
            "api_status": response.status_code,
            "api_response": response.json() if response.ok else response.text[:500]
        })

    except Exception as e:
        import traceback
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


@debug_api.route("/report/<org_name>")
@require_auth
def inspect_report(org_name: str):
    """
    Inspect what report_service returns vs what's in cache.

    Compares ReportService.get_organization_report() output
    with unified cache to diagnose data loading issues.
    """
    try:
        container = get_container()
        report_service = container.report_service

        # Get report from report_service (what the page uses)
        report = report_service.get_organization_report(org_name, skip_ai=True, use_cache=True)

        if not report:
            return jsonify({
                "error": "Report not found",
                "org_name": org_name
            }), 404

        # Get unified cache data directly (what SHOULD be loaded)
        unified_cache = get_unified_cache_repository()
        cached_data = unified_cache.get_quantitative_data(org_name)

        return jsonify({
            "success": True,
            "org_name": org_name,
            "report_service_returned": {
                "keys": list(report.keys()) if report else [],
                "has_header": "header" in report if report else False,
                "has_maturity": "maturity" in report if report else False,
                "overall_score": report.get("maturity", {}).get("overall_score") if report else None,
                "maturity_level": report.get("maturity", {}).get("maturity_level") if report else None,
                "header_value": report.get("header") if report else None
            },
            "unified_cache_has": {
                "keys": list(cached_data.keys()) if cached_data else [],
                "overall_score": cached_data.get("maturity", {}).get("overall_score") if cached_data else None,
                "maturity_level": cached_data.get("maturity", {}).get("maturity_level") if cached_data else None
            },
            "scores_match": (
                report.get("maturity", {}).get("overall_score") ==
                cached_data.get("maturity", {}).get("overall_score")
            ) if report and cached_data else False
        })

    except Exception as e:
        import traceback
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500
