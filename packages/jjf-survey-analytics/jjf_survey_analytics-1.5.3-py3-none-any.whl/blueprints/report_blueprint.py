"""
Report Blueprint for JJF Survey Analytics.

Provides organization and aggregate report viewing routes.
"""

import os

from flask import Blueprint, jsonify, make_response, render_template, request

from src.blueprints.auth_blueprint import require_auth
from src.services.container import get_container

# Create blueprint
report_blueprint = Blueprint("report", __name__)


@report_blueprint.route("/org/<org_name>")
@require_auth
def organization_detail(org_name: str):
    """
    Display organization detail page with survey status and contacts.

    Shows organization overview, contact information, and survey completion status.

    Args:
        org_name: Name of the organization

    Returns:
        Rendered organization detail template
    """
    container = get_container()
    data_service = container.data_service
    analytics_service = container.analytics_service

    try:
        # Check if data is loaded
        if not data_service.has_data():
            return (
                render_template("error.html", error="Data not loaded. Please refresh data first."),
                503,
            )

        # Get organization detail from analytics service
        detail = analytics_service.get_organization_detail(org_name)

        if not detail:
            return render_template("error.html", error=f"Organization not found: {org_name}"), 404

        return render_template(
            "reports/organization_detail.html",
            org_name=org_name,
            intake_record=detail.get("intake_record"),
            completion_pct=detail.get("completion_pct"),
            completed_surveys=detail.get("completed_surveys"),
            total_surveys=detail.get("total_surveys"),
            contacts=detail.get("contacts"),
        )

    except Exception as e:
        print(f"Error loading organization detail for {org_name}: {e}")
        import traceback

        traceback.print_exc()
        return render_template("error.html", error=str(e)), 500


@report_blueprint.route("/report/org/<org_name>")
@require_auth
def organization_report(org_name: str):
    """
    Generate AI-powered organization report with maturity assessment.

    Uses ReportGenerator to create comprehensive analysis including:
    - Quantitative maturity scores across technology dimensions
    - Qualitative AI analysis of free text responses
    - Score modifiers based on contextual insights

    Implements intelligent caching: Report cached based on response count.
    Cache invalidates automatically when new responses are added.

    Query Parameters:
        ai: Enable/disable AI analysis (default: true)
        force: Force regeneration of cached data (default: false)

    Args:
        org_name: Name of the organization

    Returns:
        Rendered organization report template
    """
    container = get_container()
    data_service = container.data_service
    report_service = container.report_service

    try:
        import time

        start_time = time.time()

        # Parse query parameters
        enable_ai = request.args.get("ai", "true").lower() == "true"
        force_regenerate = request.args.get("force", "false").lower() == "true"
        print(f"[TIMING] Query params parsed in {time.time() - start_time:.3f}s")

        # Check if data is loaded
        if not data_service.has_data():
            return (
                render_template("error.html", error="Data not loaded. Please refresh data first."),
                503,
            )
        print(f"[TIMING] Data check in {time.time() - start_time:.3f}s")

        # Generate report (with caching)
        # Note: Force regeneration handled by clearing cache if needed
        if force_regenerate:
            # Clear cache for this organization
            cache_key = f"org_report_{org_name}"
            if hasattr(report_service, "clear_cache"):
                report_service.clear_cache(cache_key)

        # Skip AI analysis on initial page load for instant rendering
        # Progressive loader will fetch AI insights via /api/report/org/<name>/ai/dimension/<dimension>
        gen_start = time.time()
        report = report_service.get_organization_report(org_name, skip_ai=True)
        print(f"[TIMING] Report generation took {time.time() - gen_start:.3f}s")

        if not report:
            return (
                render_template("error.html", error=f"No data found for organization: {org_name}"),
                404,
            )

        # Check database cache for qualitative data (instant load if available)
        from src.repositories.qualitative_cache_file_repository import get_qualitative_cache_file_repository
        cache_load_start = time.time()
        cache_repo = get_qualitative_cache_file_repository()
        qualitative_data = {}

        # Try to load main summary, title, and subtitle from qualitative cache
        # Use the file repository's _load_org_cache() method
        cache_entry = cache_repo._load_org_cache(org_name)

        if cache_entry:
            # Load main summary from cache structure
            main_summary_data = cache_entry.get('main_summary', {})
            if main_summary_data and main_summary_data.get('text'):
                main_summary = main_summary_data['text']
                import json
                try:
                    if isinstance(main_summary, str):
                        qualitative_data['main_summary'] = json.loads(main_summary)
                    else:
                        qualitative_data['main_summary'] = main_summary
                except (json.JSONDecodeError, TypeError):
                    # If not JSON, store as-is (backwards compatibility)
                    qualitative_data['main_summary'] = main_summary
                print(f"[TIMING] Loaded main summary from file cache")

            # Apply title and subtitle from qualitative cache to report.summary
            if main_summary_data.get('title'):
                if 'summary' not in report:
                    report['summary'] = {}
                report['summary']['title'] = main_summary_data['title']
                print(f"[TIMING] Applied summary title from qualitative cache: {main_summary_data['title']}")

            if main_summary_data.get('subtitle'):
                if 'summary' not in report:
                    report['summary'] = {}
                report['summary']['subtitle'] = main_summary_data['subtitle']
                print(f"[TIMING] Applied summary subtitle from qualitative cache: {main_summary_data['subtitle']}")

        # Try to load all dimension data
        dimensions = [
            'Program Technology',
            'Business Systems',
            'Data Management',
            'Infrastructure',
            'Organizational Culture'
        ]

        dimensions_loaded = 0
        for dimension in dimensions:
            cached = cache_repo.get_cached_data(org_name, dimension)
            if cached and 'data' in cached:
                qualitative_data[dimension] = cached['data']
                dimensions_loaded += 1

        print(f"[TIMING] Loaded {dimensions_loaded}/5 dimensions from DB cache in {time.time() - cache_load_start:.3f}s")

        # Only redirect if main_summary is missing (dimensions can be partial)
        # This allows viewing reports even when some dimensions have no survey data
        if not qualitative_data.get('main_summary'):
            print(f"[REPORT] Missing main_summary for {org_name}, redirecting to build-review")
            from flask import redirect
            return redirect(f'/report/org/{org_name}/build-review')

        # Log if dimensions are partial but allow viewing
        if dimensions_loaded < 5:
            print(f"[REPORT] {org_name} has {dimensions_loaded}/5 dimensions (partial data) - proceeding with report")

        # Transform qualitative_data into report.ai_insights structure for template compatibility
        if qualitative_data:
            # Build ai_insights structure from database cache
            ai_insights = {
                "dimensions": {},
                "summary": qualitative_data.get('main_summary'),
                "recommendations": [],
                "total_impact_summary": {
                    "total_modifiers": 0,
                    "total_modifier_value": 0.0,
                    "total_positive_impact": 0.0,
                    "total_negative_impact": 0.0,
                    "net_impact": 0.0,
                    "dimensions_affected": 0
                }
            }

            # Get dimension weights from MaturityRubric (single source of truth)
            from src.analytics.maturity_rubric import MaturityRubric
            dimension_weights = MaturityRubric.DIMENSION_WEIGHTS

            # Transform each dimension's data
            for dimension in dimensions:
                if dimension in qualitative_data:
                    dim_data = qualitative_data[dimension]

                    # Extract score_modifiers (database cache format)
                    modifiers = dim_data.get('modifiers', [])

                    # Calculate modifier statistics
                    if modifiers:
                        total_modifier = sum(m.get('value', 0) for m in modifiers)

                        # Get dimension weight from MaturityRubric
                        weight = dimension_weights.get(dimension, 0.20)

                        # FIX (JJF-44): Calculate WEIGHTED impact (modifier × weight)
                        positive_impact = sum(m.get('value', 0) * weight for m in modifiers if m.get('value', 0) > 0)
                        negative_impact = sum(m.get('value', 0) * weight for m in modifiers if m.get('value', 0) < 0)

                        # Get scores from variance_analysis if available
                        if 'maturity' in report and 'variance_analysis' in report['maturity']:
                            variance = report['maturity']['variance_analysis'].get(dimension, {})
                            base_score = variance.get('weighted_score', 0.0)
                            adjusted_score = variance.get('adjusted_score', base_score)
                        else:
                            base_score = 0.0
                            adjusted_score = 0.0

                        # Calculate impact on overall score
                        # FIX (JJF-HOTFIX): Use DIRECT formula: modifier × weight = impact
                        # Previously used score_delta × weight, which was 0 when skip_ai=True
                        score_delta = adjusted_score - base_score
                        overall_impact = total_modifier * weight

                        ai_insights['dimensions'][dimension] = {
                            'summary': dim_data.get('summary', ''),
                            'themes': dim_data.get('themes', []),
                            'modifiers': modifiers,
                            'score_modifiers': modifiers,  # FIX (JJF-44): Template expects 'score_modifiers'
                            'modifier_summary': {
                                'modifier_count': len(modifiers),
                                'total_modifier': total_modifier,
                                'positive_impact': positive_impact,
                                'negative_impact': negative_impact
                            },
                            'impact_summary': {
                                'base_score': base_score,
                                'adjusted_score': adjusted_score,
                                'dimension_weight': weight,
                                'score_delta': score_delta,
                                'overall_impact': overall_impact
                            }
                        }

                        # Update totals
                        ai_insights['total_impact_summary']['total_modifiers'] += len(modifiers)
                        ai_insights['total_impact_summary']['total_modifier_value'] += total_modifier
                        ai_insights['total_impact_summary']['total_positive_impact'] += positive_impact
                        ai_insights['total_impact_summary']['total_negative_impact'] += negative_impact
                        ai_insights['total_impact_summary']['dimensions_affected'] += 1

            # Calculate net impact
            ai_insights['total_impact_summary']['net_impact'] = (
                ai_insights['total_impact_summary']['total_positive_impact'] +
                ai_insights['total_impact_summary']['total_negative_impact']
            )

            # Add ai_insights to report
            report['ai_insights'] = ai_insights
            print(f"[TIMING] Transformed qualitative_data into ai_insights: {ai_insights['total_impact_summary']['dimensions_affected']} dimensions, {ai_insights['total_impact_summary']['total_modifiers']} total modifiers")

        # BUGFIX (JJF-47, JJF-62): Always recalculate overall score from variance_analysis
        # This ensures overall score matches dimension scores even when qualitative cache has partial data
        print(f"[REPORT] Recalculating overall score from variance_analysis for {org_name}...")
        variance_analysis = report.get('maturity', {}).get('variance_analysis', {})
        if variance_analysis:
            from src.analytics.maturity_rubric import MaturityRubric
            overall_score = MaturityRubric.calculate_overall_score_from_dimensions(variance_analysis)
            report['maturity']['overall_score'] = overall_score
            print(f"[REPORT] Recalculated overall maturity score: {overall_score:.2f}")
        else:
            print(f"[REPORT] WARNING: No variance_analysis found for {org_name}, cannot recalculate overall score")

        # Get REQUIRE_AUTH from environment
        require_auth_env = os.getenv("REQUIRE_AUTH", "false").lower() == "true"

        # Render template and add cache-control headers to prevent stale data
        response = make_response(render_template(
            "reports/organization_report.html",
            report=report,
            org_name=org_name,
            enable_ai=enable_ai,
            force_regenerate=force_regenerate,
            require_auth=require_auth_env,
            qualitative_data=qualitative_data,  # Pass cached data to template
        ))

        # CRITICAL: Prevent browser/CDN caching of dynamic reports
        # Reports must always reflect current data, not cached HTML
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, private, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'

        return response

    except Exception as e:
        print(f"Error generating report for {org_name}: {e}")
        import traceback

        traceback.print_exc()
        return render_template("error.html", error=str(e)), 500


@report_blueprint.route("/report/org/<org_name>/build-review")
@require_auth
def organization_build_review(org_name: str):
    """
    Build & Review qualitative analysis editor with card-based UI.

    Interactive editor for reviewing and refining AI-generated qualitative
    analysis across all five technology dimensions. Uses real-time SSE
    streaming for progressive dimension loading.

    Features:
    - Card-based UI for each dimension (JJF-18)
    - Real-time SSE streaming for progressive analysis (JJF-19, JJF-21)
    - Concurrent AI analysis orchestration (JJF-20)
    - Edit and save qualitative analysis per dimension
    - Cache-aware loading (instant for cached, progressive for fresh)
    - Debug information panel with calculation verification (JJF-41)

    Args:
        org_name: Name of the organization

    Returns:
        Rendered build-review template with card-based editor and debug data

    Related:
        - POST /api/report/org/<org_name>/build-review/init - Initialize session (JJF-17)
        - GET /api/report/org/<org_name>/build-review/stream/<session_id> - SSE stream (JJF-19)
        - /static/js/build_review_controller.js - Frontend controller (JJF-21)
        - /static/js/dimension_card.js - Card component (JJF-18)
    """
    try:
        # Get services from container
        container = get_container()
        data_service = container.data_service
        report_service = container.report_service

        # Check if data is loaded
        if not data_service.has_data():
            return (
                render_template("error.html", error="Data not loaded. Please refresh data first."),
                503,
            )

        # Generate report for debug section (skip_ai=True for fast loading)
        # This provides score calculations, modifiers, and verification data
        report = report_service.get_organization_report(org_name, skip_ai=True)

        # Check if report was successfully generated
        if not report:
            return (
                render_template("error.html", error=f"Unable to generate report for organization: {org_name}"),
                404,
            )

        # ============================================================================
        # PERFORMANCE OPTIMIZATION: Single bulk query replaces 6 individual queries
        # Uses load_organization_qualitative_data() to fetch all cache data at once
        # Before: 6 queries (150-200ms), After: 1 query (30-50ms), 75-85% faster
        # ============================================================================
        from src.repositories.qualitative_cache_file_repository import get_qualitative_cache_file_repository

        cache_repo = get_qualitative_cache_file_repository()

        # Define dimensions to load (5 valid technology dimensions only)
        dimensions = [
            'Program Technology',
            'Business Systems',
            'Data Management',
            'Infrastructure',
            'Organizational Culture'
        ]

        # Bulk load all qualitative data in a single query
        qual_data = cache_repo.load_organization_qualitative_data(org_name, dimensions)

        # Extract data from bulk result
        qualitative_data = {}
        if qual_data['main_summary']:
            qualitative_data['main_summary'] = qual_data['main_summary']
            print(f"[BUILD_REVIEW] Loaded main summary from DB cache")

        # Apply title and subtitle from qualitative cache to report.summary
        if qual_data['summary_title']:
            if 'summary' not in report:
                report['summary'] = {}
            report['summary']['title'] = qual_data['summary_title']
            print(f"[BUILD_REVIEW] Applied summary title from qualitative cache: {qual_data['summary_title']}")

        if qual_data['summary_subtitle']:
            if 'summary' not in report:
                report['summary'] = {}
            report['summary']['subtitle'] = qual_data['summary_subtitle']
            print(f"[BUILD_REVIEW] Applied summary subtitle from qualitative cache: {qual_data['summary_subtitle']}")

        # Extract dimension-specific data
        qualitative_data.update(qual_data['dimensions'])
        dimensions_loaded = qual_data['dimensions_loaded']

        print(f"[BUILD_REVIEW] Loaded {dimensions_loaded}/{len(dimensions)} dimensions from DB cache")

        # Reconstruct ai_insights if cache exists
        if qualitative_data:
            # Build ai_insights structure from cached data
            ai_insights = {
                "dimensions": {},
                "summary": qualitative_data.get('main_summary'),
                "recommendations": [],
                "total_impact_summary": {
                    "total_modifiers": 0,
                    "total_modifier_value": 0.0,
                    "total_positive_impact": 0.0,
                    "total_negative_impact": 0.0,
                    "net_impact": 0.0,
                    "dimensions_affected": 0
                }
            }

            # Get dimension weights from MaturityRubric (single source of truth)
            from src.analytics.maturity_rubric import MaturityRubric
            dimension_weights = MaturityRubric.DIMENSION_WEIGHTS

            # Transform each dimension's cached data
            for dimension in dimensions:
                if dimension in qualitative_data:
                    dim_data = qualitative_data[dimension]

                    # FIX (JJF-60): Prefer admin modifiers from merged report over qualitative cache
                    # Check if report already has admin modifiers for this dimension
                    dimension_key = dimension.replace(' ', '_')
                    report_has_admin_modifiers = False
                    if 'ai_insights' in report and 'dimensions' in report['ai_insights']:
                        report_dim = report['ai_insights']['dimensions'].get(dimension_key, {})
                        if report_dim.get('modifier_source') == 'admin':
                            modifiers = report_dim.get('score_modifiers', [])
                            report_has_admin_modifiers = True
                            print(f"[BUILD_REVIEW] Using admin modifiers for {dimension} from merged report (count={len(modifiers)})")

                    # Fallback to qualitative cache if no admin modifiers in report
                    if not report_has_admin_modifiers:
                        modifiers = dim_data.get('modifiers', [])

                    if modifiers:
                        # Get dimension weight from MaturityRubric
                        weight = dimension_weights.get(dimension, 0.20)

                        total_modifier = sum(m.get('value', 0) for m in modifiers)
                        # FIX: Must multiply by weight for weighted impact (was showing -4.5 instead of -0.45)
                        positive_impact = sum(m.get('value', 0) * weight for m in modifiers if m.get('value', 0) > 0)
                        negative_impact = sum(m.get('value', 0) * weight for m in modifiers if m.get('value', 0) < 0)

                        # Get scores from variance_analysis if available
                        if 'maturity' in report and 'variance_analysis' in report['maturity']:
                            variance = report['maturity']['variance_analysis'].get(dimension, {})
                            base_score = variance.get('weighted_score', 0.0)
                            adjusted_score = variance.get('adjusted_score', base_score)
                        else:
                            base_score = 0.0
                            adjusted_score = 0.0

                        # Calculate impact on overall score
                        # FIX (JJF-HOTFIX): Use DIRECT formula: modifier × weight = impact
                        # Previously used score_delta × weight, which was 0 when skip_ai=True
                        score_delta = adjusted_score - base_score
                        overall_impact = total_modifier * weight

                        ai_insights['dimensions'][dimension] = {
                            'summary': dim_data.get('summary', ''),
                            'themes': dim_data.get('themes', []),
                            'modifiers': modifiers,
                            'score_modifiers': modifiers,  # FIX: Template expects 'score_modifiers'
                            'modifier_summary': {
                                'modifier_count': len(modifiers),
                                'total_modifier': total_modifier,
                                'positive_impact': positive_impact,
                                'negative_impact': negative_impact
                            },
                            'impact_summary': {
                                'base_score': base_score,
                                'adjusted_score': adjusted_score,
                                'dimension_weight': weight,
                                'score_delta': score_delta,
                                'overall_impact': overall_impact
                            }
                        }

                        # Update totals
                        ai_insights['total_impact_summary']['total_modifiers'] += len(modifiers)
                        ai_insights['total_impact_summary']['total_modifier_value'] += total_modifier
                        ai_insights['total_impact_summary']['total_positive_impact'] += positive_impact
                        ai_insights['total_impact_summary']['total_negative_impact'] += negative_impact
                        ai_insights['total_impact_summary']['dimensions_affected'] += 1

            # Calculate net impact
            ai_insights['total_impact_summary']['net_impact'] = (
                ai_insights['total_impact_summary']['total_positive_impact'] +
                ai_insights['total_impact_summary']['total_negative_impact']
            )

            # Replace report's ai_insights with populated version
            report['ai_insights'] = ai_insights
            print(f"[BUILD_REVIEW] Transformed qualitative_data into ai_insights: {ai_insights['total_impact_summary']['dimensions_affected']} dimensions, {ai_insights['total_impact_summary']['total_modifiers']} total modifiers")

            # CRITICAL: Recalculate dimension scores with modifiers now that ai_insights is populated
            # The initial report was generated with skip_ai=True, so modifiers were not applied
            # Now we need to manually apply modifiers from ai_insights to variance_analysis

            # The variance_analysis is inside report['maturity'], not at root level
            variance_analysis = report.get('maturity', {}).get('variance_analysis', {})

            if variance_analysis:
                print(f"[BUILD_REVIEW] Checking dimension scores (modifiers already applied by ReportGenerator)...")

                for dimension_name, analysis in variance_analysis.items():
                    # Skip recalculation if modifiers were already applied by ReportGenerator
                    # (e.g., admin modifiers take precedence and were already calculated)
                    if 'modifier_source' in analysis and analysis['modifier_source'] in ['admin', 'ai']:
                        source = analysis['modifier_source']
                        modifier = analysis.get('total_modifier', 0)
                        base = analysis.get('weighted_score', 0)
                        adjusted = analysis.get('adjusted_score', base)
                        print(f"[BUILD_REVIEW]   {dimension_name}: base={base:.2f} + modifier={modifier:.3f} = adjusted={adjusted:.2f} (source={source}, already calculated)")
                        continue

                    # Only recalculate if no modifiers were applied yet
                    if dimension_name in ai_insights['dimensions']:
                        base_score = analysis.get('weighted_score', 0)
                        modifiers = ai_insights['dimensions'][dimension_name].get('modifiers', [])

                        if modifiers:
                            # Calculate total modifier (sum of all modifier values)
                            total_modifier = sum(m.get('value', 0) for m in modifiers)

                            # Apply modifier with clamping to [0, 5] range
                            adjusted_score = max(0, min(5, base_score + total_modifier))

                            # Update analysis with modifier data
                            analysis['total_modifier'] = total_modifier
                            analysis['adjusted_score'] = adjusted_score
                            analysis['modifier_source'] = 'ai'

                            print(f"[BUILD_REVIEW]   {dimension_name}: base={base_score:.2f} + modifier={total_modifier:.3f} = adjusted={adjusted_score:.2f}")
                        else:
                            print(f"[BUILD_REVIEW]   {dimension_name}: No modifiers, keeping base={base_score:.2f}")

                # Recalculate overall maturity score using centralized method
                # BUGFIX JJF-44: Was missing division by total_weight (worked only because sum=1.0)
                print(f"[BUILD_REVIEW] Overall score calculation breakdown:")
                for dimension_name, analysis in variance_analysis.items():
                    adjusted_score = analysis.get('adjusted_score', analysis.get('weighted_score', 0))
                    weight = dimension_weights.get(dimension_name, 0)
                    contribution = adjusted_score * weight
                    print(f"[BUILD_REVIEW]   {dimension_name}: {adjusted_score:.2f} × {weight:.2f} = {contribution:.3f}")

                # Use centralized calculation method (single source of truth)
                overall_score = MaturityRubric.calculate_overall_score_from_dimensions(variance_analysis)
                report['maturity']['overall_score'] = overall_score
                print(f"[BUILD_REVIEW] Recalculated overall maturity score: {overall_score:.2f}")

            # Also set report_title and report_subtitle if cached
            if qual_data['summary_title']:
                report['report_title'] = qual_data['summary_title']
            if qual_data['summary_subtitle']:
                report['report_subtitle'] = qual_data['summary_subtitle']
        else:
            # BUGFIX: Even if no qualitative data, still recalculate overall score
            # This ensures score is always accurate even when qualitative cache is missing
            print(f"[BUILD_REVIEW] No qualitative data found, but still recalculating overall score from variance_analysis...")
            variance_analysis = report.get('maturity', {}).get('variance_analysis', {})
            if variance_analysis:
                from src.analytics.maturity_rubric import MaturityRubric
                overall_score = MaturityRubric.calculate_overall_score_from_dimensions(variance_analysis)
                report['maturity']['overall_score'] = overall_score
                print(f"[BUILD_REVIEW] Recalculated overall maturity score: {overall_score:.2f}")

        # Check if report was generated successfully
        if not report:
            return (
                render_template("error.html", error=f"No data found for organization: {org_name}"),
                404,
            )

        # Render card-based editor template with report data for debug section
        return render_template(
            "reports/build_review.html",
            org_name=org_name,
            report=report,
            dimensions=dimensions
        )

    except Exception as e:
        print(f"Error loading build-review page for {org_name}: {e}")
        import traceback

        traceback.print_exc()
        return render_template("error.html", error=str(e)), 500


@report_blueprint.route("/report/org/<org_name>/internal")
@require_auth
def organization_report_internal(org_name: str):
    """
    Internal-only organization report with Strategic Recommendations.

    This route displays the full organization report including Strategic
    Recommendations section that is hidden from the external report view.
    Requires authentication.

    Args:
        org_name: Name of the organization

    Returns:
        Rendered internal organization report template
    """
    container = get_container()
    data_service = container.data_service
    report_service = container.report_service

    try:
        # Check if data is loaded
        if not data_service.has_data():
            return (
                render_template("error.html", error="Data not loaded. Please refresh data first."),
                503,
            )

        # Generate report (with caching)
        # Skip AI for internal reports too - use progressive loading
        report = report_service.get_organization_report(org_name, skip_ai=True)

        if not report:
            return (
                render_template("error.html", error=f"No data found for organization: {org_name}"),
                404,
            )

        return render_template(
            "reports/organization_report_internal.html", report=report, org_name=org_name
        )

    except Exception as e:
        print(f"Error generating internal report for {org_name}: {e}")
        import traceback

        traceback.print_exc()
        return render_template("error.html", error=str(e)), 500


@report_blueprint.route("/report/org/<org_name>/regenerate-html")
@require_auth
def regenerate_org_html(org_name: str):
    """Regenerate HTML from cached report without re-running AI analysis."""
    container = get_container()
    report_service = container.report_service

    try:
        # Get report from cache (don't regenerate)
        report = report_service.get_organization_report(org_name, use_cache=True)

        if not report:
            return (
                jsonify(
                    {
                        "error": f"No cached report available for {org_name}",
                        "suggestion": "Generate a report first",
                    }
                ),
                404,
            )

        return render_template("reports/organization_report.html", report=report, org_name=org_name)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@report_blueprint.route("/report/org/<org_name>/pd")
@require_auth
def organization_report_pdf(org_name: str):
    """
    Generate PDF version of organization report.

    Attempts multiple PDF generation strategies:
    1. pdfkit (wkhtmltopdf)
    2. reportlab (basic PDF)
    3. weasyprint (CSS-aware)
    4. Fallback to HTML with print styles

    Args:
        org_name: Name of the organization

    Returns:
        PDF file download or HTML with print styles
    """
    container = get_container()
    data_service = container.data_service
    report_service = container.report_service

    try:
        # Check if data is loaded
        if not data_service.has_data():
            return jsonify({"error": "Data not loaded"}), 503

        # Get report (with caching)
        report = report_service.get_organization_report(org_name)

        if not report:
            return jsonify({"error": f"No data found for organization: {org_name}"}), 404

        # Render PDF template
        html_content = render_template(
            "reports/organization_report_pdf.html", org_name=org_name, report=report
        )

        # Try PDF generation using report service
        pdf_result = report_service.generate_pdf(html_content, org_name)

        if pdf_result["success"]:
            # Create response with PDF file
            filename = f"{org_name.replace(' ', '_')}_maturity_report.pd"
            response = make_response(pdf_result["pdf_data"])
            response.headers["Content-Type"] = "application/force-download"
            response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
            response.headers["Content-Description"] = "File Transfer"
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            response.headers["X-Content-Type-Options"] = "nosnif"
            response.headers["X-Download-Options"] = "noopen"
            response.headers["Content-Transfer-Encoding"] = "binary"
            response.headers["Content-Length"] = str(len(pdf_result["pdf_data"]))

            return response
        else:
            # Fallback to HTML with print styles
            return (
                render_template(
                    "reports/organization_report_pdf.html", org_name=org_name, report=report
                ),
                200,
                {"Content-Type": "text/html", "X-PDF-Fallback": "true"},
            )

    except Exception as e:
        print(f"Error generating PDF for {org_name}: {e}")
        import traceback

        traceback.print_exc()
        return jsonify({"error": "Failed to generate PDF report"}), 500


@report_blueprint.route("/report/org/<org_name>/pdf/snapshot/<snapshot_id>")
@require_auth
def organization_report_pdf_from_snapshot(org_name: str, snapshot_id: str):
    """
    Generate PDF version of organization report from a captured snapshot.

    Args:
        org_name: Name of the organization
        snapshot_id: ID of the snapshot to use

    Returns:
        PDF file download or HTML with print styles
    """
    container = get_container()
    report_service = container.report_service

    try:
        # Generate report from snapshot
        report = report_service.get_organization_report_from_snapshot(org_name, snapshot_id)

        if not report:
            return (
                jsonify({"error": f"Failed to generate report from snapshot for: {org_name}"}),
                500,
            )

        # Render PDF template with snapshot-generated report
        html_content = render_template(
            "reports/organization_report_pdf.html", org_name=org_name, report=report
        )

        # Return HTML with print styles (browser PDF generation)
        print(
            f"[PDF Snapshot] Returning HTML with print styles for {org_name} from snapshot {snapshot_id}"
        )
        print("[PDF Snapshot] User can use browser's Print to PDF functionality")

        return (
            html_content,
            200,
            {
                "Content-Type": "text/html; charset=utf-8",
                "X-PDF-Fallback": "true",
                "X-Snapshot-ID": snapshot_id,
            },
        )

    except Exception as e:
        print(f"Error generating PDF from snapshot for {org_name}: {e}")
        import traceback

        traceback.print_exc()
        return jsonify({"error": "Failed to generate PDF from snapshot"}), 500


@report_blueprint.route("/report/aggregate")
@require_auth
def aggregate_report():
    """
    Generate aggregate report across all organizations.

    Provides comprehensive maturity assessment aggregated across
    all surveyed organizations with comparative analytics.

    Implements intelligent caching: Report cached based on total response count.
    Cache invalidates automatically when any new response is added.

    Returns:
        Rendered aggregate report template
    """
    container = get_container()
    data_service = container.data_service
    report_service = container.report_service

    try:
        # Check if data is loaded
        if not data_service.has_data():
            return (
                render_template("error.html", error="Data not loaded. Please refresh data first."),
                503,
            )

        # Generate aggregate report (with caching)
        report = report_service.get_aggregate_report()

        if not report:
            return render_template("error.html", error="Unable to generate aggregate report"), 500

        return render_template("reports/aggregate_report.html", report=report)

    except Exception as e:
        print(f"Error generating aggregate report: {e}")
        import traceback

        traceback.print_exc()
        return render_template("error.html", error=str(e)), 500
