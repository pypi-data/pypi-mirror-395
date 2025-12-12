"""
Report API Blueprint for JJF Survey Analytics.

Provides API endpoints for async report generation and progress tracking.
"""

import logging

from flask import Blueprint, jsonify, request

from src.blueprints.auth_blueprint import require_auth
from src.services.container import get_container

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
report_api = Blueprint("report_api", __name__, url_prefix="/api/report")


@report_api.route("/org/<org_name>/generate", methods=["POST"])
@require_auth
def api_generate_org_report(org_name: str):
    """
    Start async generation of organization report with AI/no-AI options.

    Request Body:
        {
            "enable_ai": true,  // Default: true
            "force_regenerate": false  // Default: false (use cache/JSON if available)
        }

    Returns:
        JSON response with task ID for progress tracking
    """
    container = get_container()
    report_service = container.report_service

    try:
        # Parse request data
        data = request.get_json() or {}
        enable_ai = data.get("enable_ai", True)  # Default to AI-enabled
        force_regenerate = data.get("force_regenerate", False)

        # Start async report generation
        result = report_service.generate_organization_report_async(
            org_name, enable_ai=enable_ai, force_regenerate=force_regenerate
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@report_api.route("/org/<org_name>/generate/ai", methods=["POST"])
@require_auth
def api_generate_org_report_ai(org_name: str):
    """
    Generate organization report with AI analysis (force AI enabled).

    Request Body:
        {
            "force_regenerate": false  // Optional
        }

    Returns:
        JSON response with task ID for progress tracking
    """
    container = get_container()
    report_service = container.report_service

    try:
        data = request.get_json() or {}
        force_regenerate = data.get("force_regenerate", False)

        # Force AI enabled
        result = report_service.generate_organization_report_async(
            org_name, enable_ai=True, force_regenerate=force_regenerate
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@report_api.route("/org/<org_name>/generate/basic", methods=["POST"])
@require_auth
def api_generate_org_report_basic(org_name: str):
    """
    Generate organization report without AI analysis (basic metrics only).

    Request Body:
        {
            "force_regenerate": false  // Optional
        }

    Returns:
        JSON response with task ID for progress tracking
    """
    container = get_container()
    report_service = container.report_service

    try:
        data = request.get_json() or {}
        force_regenerate = data.get("force_regenerate", False)

        # Force AI disabled
        result = report_service.generate_organization_report_async(
            org_name, enable_ai=False, force_regenerate=force_regenerate
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@report_api.route("/aggregate/generate", methods=["POST"])
@require_auth
def api_generate_aggregate_report():
    """
    Start async generation of aggregate report.

    Returns:
        JSON response with task ID for progress tracking
    """
    container = get_container()
    report_service = container.report_service

    try:
        # Start async aggregate report generation
        result = report_service.generate_aggregate_report_async()

        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@report_api.route("/progress/<task_id>")
@require_auth
def api_report_progress(task_id: str):
    """
    Get progress of async report generation.

    Args:
        task_id: UUID of the async task

    Returns:
        JSON response with task progress information
    """
    container = get_container()
    report_service = container.report_service

    try:
        progress = report_service.get_task_progress(task_id)

        if not progress:
            return jsonify({"success": False, "error": "Task not found or expired"}), 404

        return jsonify({"success": True, "progress": progress})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@report_api.route("/org/<org_name>/capture-snapshot", methods=["POST"])
@require_auth
def capture_print_snapshot(org_name: str):
    """
    Capture a complete snapshot of current survey data and admin edits for printing.

    This ensures that all edited values are preserved and used in the printed report.
    Snapshots are timestamped and stored for later PDF generation.

    Args:
        org_name: Name of the organization

    Returns:
        JSON response with snapshot ID and metadata
    """
    container = get_container()
    report_service = container.report_service

    try:
        # Capture snapshot
        snapshot_result = report_service.capture_print_snapshot(org_name)

        if snapshot_result["success"]:
            return jsonify(snapshot_result)
        else:
            return jsonify(snapshot_result), 500

    except Exception as e:
        print(f"[Print Snapshot] Error capturing snapshot for {org_name}: {e}")
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


# 3-Phase Report Generation Endpoints


@report_api.route("/org/<org_name>/check-cache", methods=["GET"])
@require_auth
def check_report_cache(org_name: str):
    """
    Check cache status for organization reports.

    Args:
        org_name: Name of the organization

    Returns:
        JSON response with cache status
    """
    container = get_container()
    report_service = container.report_service

    try:
        cache_status = report_service.check_cache_status(org_name)

        return jsonify({"success": True, "organization": org_name, **cache_status})
    except Exception as e:
        print(f"Error checking cache: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@report_api.route("/org/<org_name>/generate-ai-analysis", methods=["POST"])
@require_auth
def generate_ai_analysis_only(org_name: str):
    """
    Phase 1: Generate ONLY AI qualitative analysis (async, cacheable).

    This endpoint starts an asynchronous task to generate AI analysis for an organization.
    The analysis can take 30-120 seconds and progress can be tracked via the progress endpoint.

    Args:
        org_name: Name of the organization

    Returns:
        JSON response with task ID for progress tracking
    """
    container = get_container()
    report_service = container.report_service

    try:
        # Start async AI analysis task
        task_id = report_service.generate_ai_analysis_async(org_name)

        return jsonify(
            {
                "success": True,
                "task_id": task_id,
                "message": f"Started AI analysis for {org_name}",
                "poll_url": f"/api/report/progress/{task_id}",
            }
        )
    except Exception as e:
        print(f"Error starting AI analysis: {str(e)}")
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@report_api.route("/org/<org_name>/generate-scores", methods=["POST"])
@require_auth
def generate_scores_only(org_name: str):
    """
    Phase 2: Generate ONLY quantitative scores (synchronous, fast).

    This endpoint generates quantitative scores without AI analysis.
    It completes in 1-2 seconds and returns immediately.

    Args:
        org_name: Name of the organization

    Returns:
        JSON response with scores data
    """
    container = get_container()
    report_service = container.report_service

    try:
        # Generate scores synchronously (fast)
        scores_data = report_service.generate_scores_sync(org_name)

        # Save to cache
        filepath = report_service.save_scores(org_name, scores_data)

        return jsonify(
            {
                "success": True,
                "organization": org_name,
                "scores": scores_data,
                "cached_to": filepath,
            }
        )
    except Exception as e:
        print(f"Error generating scores: {str(e)}")
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@report_api.route("/org/<org_name>/merge-and-render", methods=["POST"])
@require_auth
def merge_and_render_report(org_name: str):
    """
    Phase 3: Merge cached JSON and generate HTML report.

    This endpoint merges previously generated AI analysis and scores to create
    the final HTML report. Both Phase 1 and Phase 2 must be completed first.

    Note: This endpoint still uses file-based cache for backward compatibility.
    For database cache, use the Full Report page instead.

    Args:
        org_name: Name of the organization

    Returns:
        JSON response with redirect URL to the generated report
    """
    container = get_container()
    report_service = container.report_service

    try:
        # Load cached data (from file cache for backward compatibility)
        ai_data = report_service.load_ai_analysis(org_name)
        scores_data = report_service.load_scores(org_name)

        if not ai_data:
            return (
                jsonify({"success": False, "error": "AI analysis not found. Run Phase 1 first."}),
                400,
            )

        if not scores_data:
            return jsonify({"success": False, "error": "Scores not found. Run Phase 2 first."}), 400

        # Merge and generate report
        report_url = report_service.merge_and_generate_html(org_name, ai_data, scores_data)

        return jsonify(
            {
                "success": True,
                "organization": org_name,
                "redirect_url": report_url,
                "message": "Report generated successfully",
            }
        )
    except Exception as e:
        print(f"Error merging and rendering: {str(e)}")
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


# Progressive Loading Endpoints


@report_api.route("/org/<org_name>/ai/summary", methods=["GET"])
@require_auth
def get_ai_summary(org_name: str):
    """
    Get or generate AI executive summary for organization.

    Progressive loading endpoint: Returns just the executive summary section.
    Uses database cache if available, generates if not.

    Args:
        org_name: Name of the organization

    Returns:
        JSON response with summary HTML content
    """
    from src.repositories.qualitative_cache_file_repository import get_qualitative_cache_file_repository

    container = get_container()
    report_service = container.report_service
    cache_repo = get_qualitative_cache_file_repository()

    try:
        # Check database cache first (main summary)
        main_summary = cache_repo.get_main_summary(org_name)

        if main_summary:
            # Database cache hit - return immediately
            print(f"[AI Summary API] Loaded main summary from DB cache for {org_name}")
            return jsonify(
                {
                    "success": True,
                    "cached": True,
                    "html": main_summary,
                    "content": main_summary,
                }
            )

        # Fallback: Check file cache for backward compatibility
        ai_data = report_service.load_ai_analysis(org_name)

        if ai_data and "overall_summary" in ai_data:
            # File cache hit - return immediately
            print(f"[AI Summary API] Loaded main summary from file cache for {org_name}")
            return jsonify(
                {
                    "success": True,
                    "cached": True,
                    "html": ai_data.get("overall_summary", ""),
                    "content": ai_data.get("overall_summary", ""),
                }
            )

        # Cache miss - generate just the summary
        summary = report_service.generate_ai_summary_only(org_name)

        return jsonify({"success": True, "cached": False, "html": summary, "content": summary})

    except Exception as e:
        print(f"Error getting AI summary for {org_name}: {str(e)}")
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@report_api.route("/org/<org_name>/ai/dimension/<dimension>", methods=["GET"])
@require_auth
def get_ai_dimension_insight(org_name: str, dimension: str):
    """
    Get or generate AI insight for specific dimension.

    Progressive loading endpoint: Returns just one dimension's AI analysis.
    Uses database cache if available, generates if not.

    Args:
        org_name: Name of the organization
        dimension: Dimension name (e.g., "Program Technology")

    Returns:
        JSON response with dimension insight HTML content, modifiers, and score calculations
    """
    from src.repositories.qualitative_cache_file_repository import get_qualitative_cache_file_repository

    container = get_container()
    report_service = container.report_service
    cache_repo = get_qualitative_cache_file_repository()

    try:
        # Check database cache first
        cached = cache_repo.get_cached_data(org_name, dimension)

        # Get the base quantitative report (without AI)
        report = report_service.get_organization_report(org_name, use_cache=True, skip_ai=True)

        # Extract base score from variance_analysis
        base_score = 0.0
        if report and "maturity" in report and "variance_analysis" in report["maturity"]:
            variance = report["maturity"]["variance_analysis"].get(dimension, {})
            base_score = variance.get("weighted_score", 0.0)

        # Calculate adjusted score by applying AI modifiers to base score
        total_modifier = 0.0
        modifiers = []

        if cached:
            # Database cache hit - extract data
            dim_data = cached.get("data", {})
            modifiers = dim_data.get("modifiers", [])

            # Sum up modifier values
            total_modifier = sum(m.get("value", 0) for m in modifiers)

            # Calculate adjusted score (with clamping to [0, 5])
            adjusted_score = max(0, min(5, base_score + total_modifier))

            # Calculate weighted impact for proper score aggregation
            # Uses same logic as report_generator.py _precalculate_modifier_summaries
            from src.analytics.maturity_rubric import MaturityRubric
            dimension_weight = MaturityRubric.DIMENSION_WEIGHTS.get(dimension, 0.0)
            score_delta = adjusted_score - base_score
            overall_impact = score_delta * dimension_weight  # Weighted by dimension weight (0.20 for all)

            impact_summary = {
                "base_score": round(base_score, 2),
                "adjusted_score": round(adjusted_score, 2),
                "dimension_weight": round(dimension_weight, 2),
                "score_delta": round(score_delta, 3),
                "overall_impact": round(overall_impact, 3),  # Weighted impact on overall score
            }

            print(
                f"[AI Dimension API] {org_name}/{dimension}: base={base_score:.2f} + modifier={total_modifier:.2f} = adjusted={adjusted_score:.2f} (weighted impact={overall_impact:+.3f})"
            )

            return jsonify(
                {
                    "success": True,
                    "cached": True,
                    "dimension": dimension,
                    "html": dim_data.get("summary", ""),
                    "content": dim_data.get("summary", ""),
                    "modifiers": modifiers,
                    "base_score": round(base_score, 2),
                    "adjusted_score": round(adjusted_score, 2),
                    "total_modifier": round(total_modifier, 2),
                    "impact_summary": impact_summary,  # Include weighted impact calculations
                }
            )

        # Cache miss - generate just this dimension
        insight = report_service.generate_ai_dimension_insight(org_name, dimension)

        # Extract modifiers from newly generated insight
        modifiers = insight.get("modifiers", [])
        total_modifier = sum(m.get("value", 0) for m in modifiers)

        # Calculate adjusted score
        adjusted_score = max(0, min(5, base_score + total_modifier))

        # Calculate weighted impact for proper score aggregation
        # Uses same logic as report_generator.py _precalculate_modifier_summaries
        from src.analytics.maturity_rubric import MaturityRubric
        dimension_weight = MaturityRubric.DIMENSION_WEIGHTS.get(dimension, 0.0)
        score_delta = adjusted_score - base_score
        overall_impact = score_delta * dimension_weight  # Weighted by dimension weight (0.20 for all)

        impact_summary = {
            "base_score": round(base_score, 2),
            "adjusted_score": round(adjusted_score, 2),
            "dimension_weight": round(dimension_weight, 2),
            "score_delta": round(score_delta, 3),
            "overall_impact": round(overall_impact, 3),  # Weighted impact on overall score
        }

        print(
            f"[AI Dimension API] {org_name}/{dimension} (fresh): base={base_score:.2f} + modifier={total_modifier:.2f} = adjusted={adjusted_score:.2f} (weighted impact={overall_impact:+.3f})"
        )

        return jsonify(
            {
                "success": True,
                "cached": False,
                "dimension": dimension,
                "html": insight.get("summary", ""),
                "content": insight.get("summary", ""),
                "modifiers": modifiers,
                "base_score": round(base_score, 2),
                "adjusted_score": round(adjusted_score, 2),
                "total_modifier": round(total_modifier, 2),
                "impact_summary": impact_summary,  # Include weighted impact calculations
            }
        )

    except Exception as e:
        print(f"Error getting AI insight for {org_name}/{dimension}: {str(e)}")
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@report_api.route("/org/<org_name>/ai/all", methods=["GET"])
@require_auth
def get_all_ai_sections(org_name: str):
    """
    Get all AI sections at once (batch endpoint for efficiency).

    Returns all AI content in one request if cached. If not cached,
    triggers async generation and returns task_id for polling.

    Args:
        org_name: Name of the organization

    Returns:
        JSON response with all AI content or task_id for polling
    """
    from src.repositories.qualitative_cache_file_repository import get_qualitative_cache_file_repository

    container = get_container()
    report_service = container.report_service

    try:
        # Check file cache first
        cache_repo = get_qualitative_cache_file_repository()

        # Get main summary
        main_summary = cache_repo.get_main_summary(org_name)

        # Get all dimension data
        dimensions_data = {}
        all_cached = True

        for dimension in cache_repo.VALID_DIMENSIONS:
            cached = cache_repo.get_cached_data(org_name, dimension)
            if cached:
                dim_data = cached.get("data", {})
                dimensions_data[dimension] = {
                    "summary": dim_data.get("summary", ""),
                    "modifiers": dim_data.get("modifiers", []),
                }
            else:
                all_cached = False
                break

        if all_cached and dimensions_data:
            # Database cache hit - return all content immediately
            print(f"[AI All API] Loaded all sections from DB cache for {org_name}")
            return jsonify(
                {
                    "success": True,
                    "cached": True,
                    "summary": main_summary or "",
                    "dimensions": dimensions_data,
                }
            )

        # Fallback: Check file cache for backward compatibility
        ai_data = report_service.load_ai_analysis(org_name)

        if ai_data:
            # File cache hit - return all content immediately
            print(f"[AI All API] Loaded all sections from file cache for {org_name}")
            return jsonify(
                {
                    "success": True,
                    "cached": True,
                    "summary": ai_data.get("overall_summary", ""),
                    "dimensions": {
                        dim: {
                            "summary": data.get("summary", ""),
                            "modifiers": data.get("modifiers", []),
                        }
                        for dim, data in ai_data.get("dimensions", {}).items()
                    },
                }
            )

        # Cache miss - start async generation
        task_id = report_service.generate_ai_analysis_async(org_name)

        return jsonify(
            {
                "success": True,
                "cached": False,
                "task_id": task_id,
                "poll_url": f"/api/report/progress/{task_id}",
                "message": "AI analysis generation started",
            }
        )

    except Exception as e:
        print(f"Error getting all AI sections for {org_name}: {str(e)}")
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


# Card-Based Editor Endpoints


@report_api.route("/org/<org_name>/build-review", methods=["POST"])
@require_auth
def build_review_session(org_name: str):
    """
    Initialize build-review session for card-based qualitative editor.

    This endpoint:
    1. Validates organization exists and has responses
    2. Checks cache status for all 5 technology dimensions
    3. Creates session for tracking progress
    4. Returns session ID and cache status for frontend

    Request Body:
        {
            "force_refresh": false  // Optional: bypass cache and regenerate all
        }

    Response:
        {
            "session_id": "uuid-string",
            "org_name": "Organization Name",
            "status": "started",
            "dimensions": {
                "Program Technology": {"status": "pending", "cached": true, "version": 1},
                "Business Systems": {"status": "pending", "cached": false},
                "Data Management": {"status": "pending", "cached": true, "has_user_edits": true},
                "Infrastructure": {"status": "pending", "cached": false},
                "Organizational Culture": {"status": "pending", "cached": true}
            },
            "stream_url": "/api/report/org/Organization%20Name/build-review/stream/<session_id>"
        }

    Error Responses:
        404: Organization not found
        400: Organization has no survey responses
        500: Server error
    """
    from urllib.parse import quote
    from src.services.build_review_session import get_session_manager
    from src.repositories.qualitative_cache_file_repository import get_qualitative_cache_file_repository

    container = get_container()
    analytics_service = container.analytics_service
    qualitative_cache = get_qualitative_cache_file_repository()
    session_manager = get_session_manager()

    try:
        # Parse request data (silent=True handles empty/malformed JSON gracefully)
        data = request.get_json(silent=True) or {}
        force_refresh = data.get("force_refresh", False)

        # Log request details for debugging
        print(f"[build_review_session] Received request for org: {org_name}")
        print(f"[build_review_session] Request method: {request.method}")
        print(f"[build_review_session] Content-Type: {request.content_type}")
        print(f"[build_review_session] Request data: {data}")
        print(f"[build_review_session] Force refresh: {force_refresh}")

        # 1. Validate organization exists
        org_data = analytics_service.get_organization_detail(org_name)
        if not org_data:
            return jsonify({
                "success": False,
                "error": f"Organization '{org_name}' not found",
                "message": "Please verify the organization name is correct"
            }), 404

        # 2. Validate organization has survey responses
        # Note: get_organization_detail returns None if org has no data
        # If we got here, org exists and has responses
        has_responses = True

        if not has_responses:
            return jsonify({
                "success": False,
                "error": f"Organization '{org_name}' has no survey responses",
                "message": "At least one survey response (CEO, Tech Lead, or Staff) is required"
            }), 400

        # 3. Check cache status for all 5 dimensions
        dimensions = [
            "Program Technology",
            "Business Systems",
            "Data Management",
            "Infrastructure",
            "Organizational Culture"
        ]

        cache_status = {}
        for dimension in dimensions:
            # Get cache metadata (lightweight - no data loading)
            metadata = qualitative_cache.get_cache_metadata(org_name, dimension)

            if metadata and not force_refresh:
                # Cache exists and not forcing refresh
                cache_status[dimension] = {
                    "status": "pending",
                    "cached": True,
                    "version": metadata.get("version", 1),
                    "has_user_edits": metadata.get("has_user_edits", False),
                    "cached_at": metadata.get("updated_at") or metadata.get("created_at")
                }
            else:
                # No cache or force refresh requested
                cache_status[dimension] = {
                    "status": "pending",
                    "cached": False
                }

        # 4. Create session
        session_id, session_data = session_manager.create_session(
            org_name=org_name,
            cache_status=cache_status,
            force_refresh=force_refresh
        )

        # 5. Build response
        # URL-encode org_name for stream URL
        encoded_org = quote(org_name)
        stream_url = f"/api/report/org/{encoded_org}/build-review/stream/{session_id}"

        response_data = {
            "success": True,
            "session_id": session_id,
            "org_name": org_name,
            "status": "started",
            "dimensions": cache_status,
            "stream_url": stream_url,
            "created_at": session_data["created_at"]
        }

        print(f"[BuildReview] Created session {session_id} for {org_name}")
        print(f"[BuildReview] Cache status: {sum(1 for d in cache_status.values() if d.get('cached'))}/5 cached")

        return jsonify(response_data)

    except Exception as e:
        print(f"[BuildReview] Error creating session for {org_name}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


# Qualitative Data Save/Load Endpoints


@report_api.route("/qualitative/save/<org_name>", methods=["POST"])
@require_auth
def save_qualitative_edits(org_name: str):
    """
    Save edited qualitative analysis data for organization.

    This endpoint accepts edited data for both the main summary and all dimension-specific
    analysis, saving changes to the qualitative cache repository.

    Request Body:
        {
            "main_summary": "Organization-level summary text...",  // Optional
            "dimensions": {  // Optional
                "Program Technology": {
                    "summary": "Dimension summary...",
                    "score_modifiers": [
                        {
                            "factor": "Factor name",
                            "value": 5,
                            "reasoning": "Updated reasoning...",
                            "respondent": "John Doe",
                            "role": "CEO"
                        }
                    ]
                },
                "Business Systems": { ... },
                ...
            }
        }

    Response:
        {
            "success": true,
            "message": "Saved edits for Organization Name",
            "saved": {
                "main_summary": true,
                "dimensions": ["Program Technology", "Business Systems"]
            },
            "version": 2
        }

    Error Responses:
        400: Invalid request data or structure
        404: Organization not found in cache
        500: Server error during save
    """
    from src.repositories.qualitative_cache_file_repository import get_qualitative_cache_file_repository

    cache_repository = get_qualitative_cache_file_repository()

    try:
        # Parse request data
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided in request body"
            }), 400

        saved_items = {
            "main_summary": False,
            "dimensions": []
        }

        # Save main summary, title, and/or subtitle if provided
        summary_fields = {}
        if "main_summary" in data and data["main_summary"]:
            summary_fields["summary_text"] = data["main_summary"]
        if "summary_title" in data and data["summary_title"]:
            summary_fields["summary_title"] = data["summary_title"]
        if "summary_subtitle" in data and data["summary_subtitle"]:
            summary_fields["summary_subtitle"] = data["summary_subtitle"]

        if summary_fields:
            try:
                cache_repository.save_main_summary(org_name, **summary_fields)
                saved_items["main_summary"] = True
                if "summary_text" in summary_fields:
                    print(f"[Qualitative Save] Saved main summary for {org_name}")
                if "summary_title" in summary_fields:
                    print(f"[Qualitative Save] Saved summary title: {summary_fields['summary_title']}")
                if "summary_subtitle" in summary_fields:
                    print(f"[Qualitative Save] Saved summary subtitle: {summary_fields['summary_subtitle']}")
            except ValueError as e:
                # No cache entries exist - this is OK if dimensions are being saved
                print(f"[Qualitative Save] Could not save summary fields: {e}")

        # Save dimension edits if provided
        if "dimensions" in data and isinstance(data["dimensions"], dict):
            for dimension, dimension_data in data["dimensions"].items():
                try:
                    # Get existing cache data to preserve fields not being edited
                    existing_data = cache_repository.get_cached_data(org_name, dimension)

                    if existing_data and "data" in existing_data:
                        # Start with existing data to preserve unchanged fields
                        cache_data = existing_data["data"].copy()
                        print(f"[Qualitative Save] Loaded existing data for {dimension}: summary={len(cache_data.get('summary', ''))}, themes={len(cache_data.get('themes', []))}, modifiers={len(cache_data.get('modifiers', []))}")

                        # Update only fields provided in request
                        if "summary" in dimension_data:
                            cache_data["summary"] = dimension_data["summary"]
                            print(f"[Qualitative Save] Updated summary: {len(dimension_data['summary'])} chars")
                        if "themes" in dimension_data:
                            cache_data["themes"] = dimension_data["themes"]
                            print(f"[Qualitative Save] Updated themes: {len(dimension_data['themes'])} items")

                        # Transform score_modifiers to modifiers format (always replace if provided)
                        if "score_modifiers" in dimension_data:
                            cache_data["modifiers"] = []
                            for modifier in dimension_data["score_modifiers"]:
                                cache_data["modifiers"].append({
                                    "respondent": modifier.get("respondent", ""),
                                    "role": modifier.get("role", ""),
                                    "factor": modifier.get("reasoning", modifier.get("factor", "")),
                                    "value": modifier.get("value", 0)
                                })
                            print(f"[Qualitative Save] Updated modifiers: {len(cache_data['modifiers'])} items")
                    else:
                        # No existing data - require complete data structure
                        print(f"[Qualitative Save] No existing cache for {dimension}, creating new entry")
                        cache_data = {
                            "summary": dimension_data.get("summary", ""),
                            "themes": dimension_data.get("themes", []),
                            "modifiers": []
                        }

                        # Transform score_modifiers for new entry
                        if "score_modifiers" in dimension_data:
                            for modifier in dimension_data["score_modifiers"]:
                                cache_data["modifiers"].append({
                                    "respondent": modifier.get("respondent", ""),
                                    "role": modifier.get("role", ""),
                                    "factor": modifier.get("reasoning", modifier.get("factor", "")),
                                    "value": modifier.get("value", 0)
                                })

                    # Validate final structure before saving
                    print(f"[Qualitative Save] Final structure: summary={len(cache_data.get('summary', ''))}, themes={len(cache_data.get('themes', []))}, modifiers={len(cache_data.get('modifiers', []))}")

                    # Save to cache (this will trigger validation)
                    cache_repository.update_dimension_data(org_name, dimension, cache_data)
                    saved_items["dimensions"].append(dimension)
                    print(f"[Qualitative Save] ✓ Saved dimension: {dimension} (version incremented)")

                except ValueError as e:
                    error_msg = str(e)
                    print(f"[Qualitative Save] ✗ ValueError saving {dimension}: {error_msg}")
                    print(f"[Qualitative Save] Request data keys: {list(dimension_data.keys())}")
                    # Continue with other dimensions
                except Exception as e:
                    print(f"[Qualitative Save] ✗ Unexpected error saving {dimension}: {type(e).__name__}: {e}")
                    import traceback
                    traceback.print_exc()
                    # Continue with other dimensions

        # Check if anything was saved
        if not saved_items["main_summary"] and not saved_items["dimensions"]:
            return jsonify({
                "success": False,
                "error": "No valid data was saved. Check that cache entries exist.",
                "saved": saved_items
            }), 400

        # Get version from one of the saved entries
        version = 1
        if saved_items["dimensions"]:
            entry = cache_repository.get_cached_data(org_name, saved_items["dimensions"][0])
            if entry:
                version = entry.get("version", 1)

        return jsonify({
            "success": True,
            "message": f"Saved edits for {org_name}",
            "saved": saved_items,
            "version": version
        })

    except Exception as e:
        print(f"[Qualitative Save] Error saving edits for {org_name}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@report_api.route("/qualitative/main-summary/<org_name>", methods=["GET"])
@require_auth
def get_main_summary(org_name: str):
    """
    Get organization-level main summary text.

    This endpoint returns the main summary for an organization if it exists
    in the qualitative cache.

    Response (Success):
        {
            "success": true,
            "summary": "Organization-level summary text...",
            "version": 1
        }

    Response (Not Found):
        {
            "success": true,
            "summary": null,
            "version": 0,
            "message": "No main summary found for organization"
        }

    Error Responses:
        500: Server error
    """
    from src.repositories.qualitative_cache_file_repository import get_qualitative_cache_file_repository

    cache_repository = get_qualitative_cache_file_repository()

    try:
        # Load organization cache using file repository
        cache = cache_repository._load_org_cache(org_name)

        if cache and 'main_summary' in cache:
            main_summary = cache['main_summary']
            # Return main summary, title, and subtitle
            return jsonify({
                "success": True,
                "summary": main_summary.get('text'),
                "title": main_summary.get('title'),
                "subtitle": main_summary.get('subtitle'),
                "version": cache.get('version', 1)
            })
        else:
            # No summary found - return gracefully
            return jsonify({
                "success": True,
                "summary": None,
                "title": None,
                "subtitle": None,
                "version": 0,
                "message": f"No main summary found for {org_name}"
            })

    except Exception as e:
        print(f"[Qualitative Get] Error getting main summary for {org_name}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@report_api.route('/dimension-cache/<org_name>/<dimension>', methods=['GET'])
@require_auth
def get_dimension_cache(org_name: str, dimension: str):
    """
    Get cached dimension data for manual refresh.

    This endpoint allows the frontend to refresh a single dimension card by
    fetching the latest cached data from the database without a full page reload.

    Args:
        org_name: Organization name
        dimension: Technology dimension name

    Returns:
        JSON with cached dimension data or error

    Response (Success):
        {
            "success": true,
            "data": {
                "summary": "Dimension summary text...",
                "themes": [...],
                "score_modifiers": [...]
            },
            "version": 2,
            "source": "user_edited",
            "cached": true
        }

    Response (Not Found):
        {
            "success": false,
            "error": "No cached data found for this dimension"
        }

    Error Responses:
        404: No cache entry found
        500: Server error
    """
    from src.repositories.qualitative_cache_file_repository import get_qualitative_cache_file_repository

    try:
        cache_repo = get_qualitative_cache_file_repository()
        cached_data = cache_repo.get_cached_data(org_name, dimension)

        if not cached_data:
            return jsonify({
                "success": False,
                "error": "No cached data found for this dimension"
            }), 404

        # Extract data with source priority (user_edited > ai_generated)
        dim_data = cached_data.get('data', {})

        # FIX (JJF-60): Check for admin modifiers and use those instead of cached modifiers
        # Admin edits in admin_edits.json are the source of truth for modifiers
        modifiers = dim_data.get('modifiers', [])
        source = cached_data.get('source', 'unknown')

        container = get_container()
        admin_edit_service = container.admin_edit_service
        admin_edits = admin_edit_service.get_org_edits(org_name)

        if admin_edits:
            # Check if this dimension has admin modifiers
            score_modifiers = admin_edits.get('score_modifiers', {})
            # Try both "Data Management" and "Data_Management" formats
            dimension_key = dimension.replace('_', ' ')
            if dimension_key in score_modifiers:
                modifiers = score_modifiers[dimension_key]
                source = 'admin'
                print(f"[API] Using admin modifiers for {dimension_key} (count={len(modifiers)})")

        return jsonify({
            "success": True,
            "data": {
                "summary": dim_data.get('summary', ''),
                "themes": dim_data.get('themes', []),
                "score_modifiers": modifiers
            },
            "version": cached_data.get('version', 1),
            "source": source,
            "cached": True
        })

    except Exception as e:
        logger.error(f"Error fetching cache for {org_name}/{dimension}: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@report_api.route("/org/<org_name>/cache-status", methods=["GET"])
@require_auth
def check_dimension_cache_status(org_name: str):
    """
    Check if all dimension data is cached for an organization.

    This lightweight endpoint checks cache metadata without loading full data.
    Used by organization detail page to determine navigation path.

    Response:
        {
            "success": true,
            "org_name": "Organization Name",
            "all_dimensions_cached": true,
            "cached_count": 5,
            "total_count": 5,
            "dimensions": {
                "Program Technology": {"cached": true, "version": 1},
                "Business Systems": {"cached": true, "version": 1},
                ...
            }
        }
    """
    from src.repositories.qualitative_cache_file_repository import get_qualitative_cache_file_repository

    try:
        cache_repo = get_qualitative_cache_file_repository()

        dimensions = [
            "Program Technology",
            "Business Systems",
            "Data Management",
            "Infrastructure",
            "Organizational Culture"
        ]

        dimension_status = {}
        cached_count = 0

        for dimension in dimensions:
            metadata = cache_repo.get_cache_metadata(org_name, dimension)
            if metadata:
                dimension_status[dimension] = {
                    "cached": True,
                    "version": metadata.get("version", 1)
                }
                cached_count += 1
            else:
                dimension_status[dimension] = {"cached": False}

        all_cached = cached_count == len(dimensions)

        return jsonify({
            "success": True,
            "org_name": org_name,
            "all_dimensions_cached": all_cached,
            "cached_count": cached_count,
            "total_count": len(dimensions),
            "dimensions": dimension_status
        })

    except Exception as e:
        print(f"[Cache Status] Error checking status for {org_name}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@report_api.route("/org/<org_name>/build-review/stream/<session_id>", methods=["GET"])
@require_auth
def stream_build_review_progress(org_name: str, session_id: str):
    """
    Stream dimension analysis progress via Server-Sent Events (SSE).

    This endpoint streams real-time progress updates as each dimension analysis
    completes. Enables progressive loading in the card-based editor frontend.

    SSE Event Types:
        - dimension_started: Analysis begins for a dimension
        - dimension_complete: Analysis finished with full data
        - dimension_error: Analysis failed with error details
        - session_complete: All dimensions analyzed
        - heartbeat: Keep-alive ping every 15 seconds

    Args:
        org_name: Organization name
        session_id: Session UUID from build-review initialization

    Returns:
        SSE stream (text/event-stream) with analysis progress events

    Example Events:
        event: dimension_started
        data: {"dimension": "Program Technology", "timestamp": "...", "cached": true}

        event: dimension_complete
        data: {"dimension": "Program Technology", "cached": true, "data": {...}, "version": 1}

        event: session_complete
        data: {"session_id": "uuid", "dimensions_completed": 5, "duration_seconds": 25.3}

    Error Responses:
        404: Session not found or expired (sent as SSE error event)
        500: Server error (sent as SSE error event)
    """
    from src.services.build_review_session import get_session_manager
    from src.repositories.qualitative_cache_file_repository import get_qualitative_cache_file_repository
    from src.services.sse_service import SSEService
    from src.extractors.sheets_reader import SheetsReader

    try:
        # Get service dependencies
        session_manager = get_session_manager()
        cache_repository = get_qualitative_cache_file_repository()

        # Validate session exists
        session = session_manager.get_session(session_id)
        if not session:
            # Return error as JSON (SSE not yet started)
            return jsonify({
                "success": False,
                "error": "Session not found or expired",
                "session_id": session_id
            }), 404

        # Validate session org_name matches
        if session.get("org_name") != org_name:
            return jsonify({
                "success": False,
                "error": f"Session org mismatch: session is for '{session.get('org_name')}', not '{org_name}'",
                "session_id": session_id
            }), 400

        # Get dimensions from session
        dimensions = list(session.get("dimensions", {}).keys())
        if not dimensions:
            # Default to all 5 dimensions if not specified
            dimensions = [
                "Program Technology",
                "Business Systems",
                "Data Management",
                "Infrastructure",
                "Organizational Culture"
            ]

        # Load Google Sheets data for AI analysis
        print(f"[SSE] Loading Google Sheets data for {org_name}...")
        sheet_data = SheetsReader.fetch_all_tabs(use_cache=True, verbose=True)
        print(f"[SSE] Sheet data loaded: {list(sheet_data.keys())}")

        # Create SSE service and stream
        sse_service = SSEService(session_manager, cache_repository)

        print(f"[SSE] Starting stream for session {session_id}, org={org_name}, dimensions={len(dimensions)}")

        # Return SSE stream
        return sse_service.stream_dimension_analysis(
            session_id=session_id,
            org_name=org_name,
            dimensions=dimensions,
            sheet_data=sheet_data,
            analysis_function=None  # Will use real orchestrator for AI analysis
        )

    except Exception as e:
        print(f"[SSE] Error starting stream for {org_name}/{session_id}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@report_api.route("/org/<org_name>/dimension-scores", methods=["GET"])
@require_auth
def get_dimension_scores(org_name: str):
    """
    Get base dimension scores for an organization (FAST - no AI).

    This endpoint is optimized for speed by:
    1. Reading directly from persistent quantitative cache (30-50ms)
    2. Using skip_ai=True to avoid 2+ minute AI analysis
    3. Only triggering regeneration if cache miss or stale data

    Returns:
        JSON with dimension names as keys and weighted_score as values
        Example: {"Program Technology": 4.34, "Business Systems": 4.08, ...}
    """
    container = get_container()
    report_service = container.report_service

    try:
        # OPTIMIZED: Get quantitative report only (skip AI) - uses persistent cache
        # This is FAST: 30-50ms (cache hit) vs 150-200ms (regeneration) vs 2+ min (with AI)
        report = report_service.get_organization_report(org_name, use_cache=True, skip_ai=True)

        if not report or "maturity" not in report or "variance_analysis" not in report["maturity"]:
            return jsonify({"success": False, "error": "Report not available"}), 404

        # Extract dimension scores from variance_analysis
        # FIX (JJF-60): Return adjusted_score (includes admin modifiers) instead of weighted_score (base score)
        dimension_scores = {}
        for dimension, analysis in report["maturity"]["variance_analysis"].items():
            # Prefer adjusted_score (with admin modifiers) over weighted_score (base)
            dimension_scores[dimension] = analysis.get("adjusted_score", analysis.get("weighted_score", 0.0))

        logger.info(f"[API] Returning dimension scores for {org_name}: {dimension_scores}")

        return jsonify({
            "success": True,
            "organization": org_name,
            "dimension_scores": dimension_scores
        })

    except Exception as e:
        logger.error(f"[API] Error getting dimension scores for {org_name}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@report_api.route("/org/<org_name>/json", methods=["GET"])
@require_auth
def get_report_debug_json(org_name: str):
    """
    Get raw report data as JSON for debugging purposes.

    Returns the exact same data structure that the HTML organization report
    template receives, formatted as pretty-printed JSON. Useful for debugging
    score calculations, modifier application, and cache behavior.

    Query Parameters:
        use_cache: Use cached data (default: true)
        skip_ai: Skip AI analysis for faster response (default: true)

    Response Structure:
        {
            "_debug_info": {
                "generated_at": "2025-12-03T10:30:00",
                "from_cache": true,
                "admin_edits_applied": true,
                "dimensions_with_modifiers": 4,
                "cache_metadata": {...}
            },
            "organization_name": "Hadar Institute",
            "overall_score": 2.17,
            "header": {...},
            "maturity": {
                "overall_score": 2.17,
                "variance_analysis": {
                    "Program Technology": {
                        "weighted_score": 3.16,
                        "adjusted_score": 2.96,
                        "total_modifier": -0.20,
                        "modifier_source": "admin",
                        "dimension_weight": 0.20,
                        ...
                    },
                    ...
                }
            },
            "nps": {...},
            "tech_insights": {...}
        }

    Returns:
        JSON response with complete report data and debug information
    """
    from datetime import datetime

    container = get_container()
    report_service = container.report_service

    try:
        # Parse query parameters (same as organization_report view)
        use_cache = request.args.get("use_cache", "true").lower() == "true"
        skip_ai = request.args.get("skip_ai", "true").lower() == "true"

        # Generate report using same flow as HTML view
        report = report_service.get_organization_report(org_name, use_cache=use_cache, skip_ai=skip_ai)

        if not report:
            return jsonify({
                "success": False,
                "error": f"No data found for organization: {org_name}"
            }), 404

        # Build debug information
        debug_info = {
            "generated_at": datetime.now().isoformat(),
            "from_cache": use_cache,
            "skip_ai": skip_ai,
            "admin_edits_applied": False,
            "dimensions_with_modifiers": 0,
            "cache_metadata": {}
        }

        # Count dimensions with modifiers and check admin edits
        if "maturity" in report and "variance_analysis" in report["maturity"]:
            variance_analysis = report["maturity"]["variance_analysis"]

            for dimension, analysis in variance_analysis.items():
                if "total_modifier" in analysis and analysis.get("total_modifier") != 0:
                    debug_info["dimensions_with_modifiers"] += 1

                    # Check if admin edits were applied
                    if analysis.get("modifier_source") == "admin":
                        debug_info["admin_edits_applied"] = True

        # Check for cache metadata
        if "metadata" in report:
            debug_info["cache_metadata"] = report.get("metadata", {})

        # Build response structure
        response_data = {
            "_debug_info": debug_info,
            "organization_name": org_name,
            "overall_score": report.get("maturity", {}).get("overall_score", 0.0),
            "header": report.get("header", {}),
            "maturity": report.get("maturity", {}),
            "nps": report.get("nps", {}),
            "tech_insights": report.get("tech_insights", {}),
        }

        # Include ai_insights if present (from qualitative cache)
        if "ai_insights" in report:
            response_data["ai_insights"] = report["ai_insights"]

        # Include summary if present
        if "summary" in report:
            response_data["summary"] = report["summary"]

        # Return pretty-printed JSON
        from flask import Response
        import json

        json_output = json.dumps(response_data, indent=2, default=str)

        return Response(
            json_output,
            mimetype="application/json",
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "Cache-Control": "no-store, no-cache, must-revalidate, private, max-age=0"
            }
        )

    except Exception as e:
        logger.error(f"[API] Error generating debug JSON for {org_name}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500
