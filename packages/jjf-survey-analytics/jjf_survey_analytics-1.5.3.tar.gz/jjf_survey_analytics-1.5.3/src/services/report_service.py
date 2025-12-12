#!/usr/bin/env python3
"""
ReportService - Async wrapper for ReportGenerator.

Provides async API interface for report generation while delegating
to the refactored ReportGenerator orchestration layer.
"""

import asyncio
import os
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Optional

from src.services.report_generator import ReportGenerator

if TYPE_CHECKING:
    from src.services.admin_edit_service import AdminEditService
    from src.services.cache_service import CacheService
    from src.services.data_service import DataService


class ReportService:
    """
    Async report generation service.

    Wraps ReportGenerator with async/background task support for API endpoints.
    Manages task tracking, progress monitoring, and print snapshots.
    """

    def __init__(
        self,
        report_generator: ReportGenerator,
        data_service: "DataService",
        admin_edit_service: "AdminEditService",
        cache_service: "CacheService" = None,
    ):
        """
        Initialize ReportService.

        Args:
            report_generator: ReportGenerator instance for actual report generation
            data_service: DataService for fetching fresh data
            admin_edit_service: AdminEditService for fetching fresh admin edits
            cache_service: Optional CacheService for report caching
        """
        self._report_generator = report_generator
        self._data_service = data_service
        self._admin_edit_service = admin_edit_service
        self._cache_service = cache_service
        self._executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="report_task")
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()

    def generate_organization_report_async(
        self, org_name: str, enable_ai: bool = False, force_regenerate: bool = False
    ) -> Dict[str, Any]:
        """
        Generate organization report asynchronously.

        Args:
            org_name: Organization name
            enable_ai: Enable AI-generated insights (not yet implemented)
            force_regenerate: Force regeneration bypassing cache

        Returns:
            Dictionary with task_id and initial status
        """
        task_id = str(uuid.uuid4())

        with self._lock:
            self._tasks[task_id] = {
                "task_id": task_id,
                "type": "organization_report",
                "org_name": org_name,
                "status": "pending",
                "progress": 0,
                "started_at": datetime.now().isoformat(),
                "completed_at": None,
                "result": None,
                "error": None,
            }

        # Submit task to executor
        _ = self._executor.submit(
            self._generate_org_report_task, task_id, org_name, enable_ai, force_regenerate
        )

        return {
            "success": True,
            "task_id": task_id,
            "status": "pending",
            "message": f"Organization report generation started for {org_name}",
        }

    def generate_aggregate_report_async(self) -> Dict[str, Any]:
        """
        Generate aggregate report asynchronously.

        Returns:
            Dictionary with task_id and initial status
        """
        task_id = str(uuid.uuid4())

        with self._lock:
            self._tasks[task_id] = {
                "task_id": task_id,
                "type": "aggregate_report",
                "status": "pending",
                "progress": 0,
                "started_at": datetime.now().isoformat(),
                "completed_at": None,
                "result": None,
                "error": None,
            }

        # Submit task to executor
        self._executor.submit(self._generate_aggregate_report_task, task_id)

        return {
            "success": True,
            "task_id": task_id,
            "status": "pending",
            "message": "Aggregate report generation started",
        }

    def get_task_progress(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get progress information for a background task.

        Args:
            task_id: Task identifier

        Returns:
            Task progress dictionary or None if task not found
        """
        with self._lock:
            return self._tasks.get(task_id)

    def get_organization_report(
        self, org_name: str, use_cache: bool = True, skip_ai: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Get organization report synchronously (for front-end views).

        Args:
            org_name: Organization name
            use_cache: Whether to use cached report
            skip_ai: If True, skip AI analysis for instant page load (AI loaded progressively via API)

        Returns:
            Organization report dictionary or None
        """
        try:
            # Check unified cache first (30-50ms vs 150-200ms regeneration)
            if use_cache and skip_ai:
                from src.repositories.unified_cache_repository import get_unified_cache_repository
                unified_cache = get_unified_cache_repository()

                # Load quantitative data from unified cache
                cached_quant_data = unified_cache.get_quantitative_data(org_name)
                if cached_quant_data:
                    # Wrap in report structure for compatibility
                    cached_report = {
                        'report': cached_quant_data,
                        'data_hash': cached_quant_data.get('metadata', {}).get('data_hash'),
                        'version': cached_quant_data.get('metadata', {}).get('version'),
                        'cached_at': cached_quant_data.get('metadata', {}).get('cached_at')
                    }
                else:
                    cached_report = None

                if cached_report:
                    # Verify data hash to detect stale cache
                    current_hash = self._calculate_data_hash(org_name)
                    cached_hash = cached_report.get('data_hash')

                    if cached_hash and cached_hash == current_hash:
                        print(f"[Cache] Using persistent cache for {org_name} (hash match)")
                        report = cached_report.get('report')

                        # CRITICAL FIX (JJF-60): Merge fresh admin edits into cached report
                        # Admin edits are stored separately and need to be merged with cached quantitative data
                        admin_edits = self._admin_edit_service.get_all_edits()
                        print(f"[DEBUG] admin_edits keys: {list(admin_edits.keys()) if admin_edits else None}")
                        print(f"[DEBUG] Looking for org_name: '{org_name}'")
                        print(f"[DEBUG] org_name in admin_edits: {org_name in admin_edits if admin_edits else False}")
                        if admin_edits and org_name in admin_edits:
                            print(f"[Cache] Merging fresh admin edits for {org_name}")
                            report = self._merge_admin_edits_into_report(report, admin_edits[org_name], org_name)
                        else:
                            print(f"[Cache] No admin edits found for {org_name} to merge")

                        # CRITICAL FIX (JJF-61): Merge AI modifiers from qualitative cache into loaded cache
                        # When loading from unified cache, AI modifiers aren't present in variance_analysis
                        # Must merge them from qualitative cache (same logic as generation path)
                        report = self._merge_ai_modifiers_into_report(report, org_name)

                        return report
                    else:
                        print(f"[Cache] Stale cache detected for {org_name}, regenerating")

            # Generate fresh report with current data
            print(f"[Cache] Generating fresh quantitative report for {org_name}")

            # Get fresh data for report generation
            sheet_data = self._data_service.get_all_data()
            admin_edits = self._admin_edit_service.get_all_edits()

            # Create fresh ReportGenerator with current data
            # Respect skip_ai parameter - don't initialize AI if we're skipping it
            fresh_generator = ReportGenerator(
                sheet_data=sheet_data,
                enable_ai=not skip_ai and bool(os.getenv("OPENROUTER_API_KEY")),
                admin_edits=admin_edits,
            )

            report = fresh_generator.generate_organization_report(org_name, skip_ai=skip_ai)

            # Save to unified cache if quantitative only (skip_ai=True)
            if report and skip_ai:
                from src.repositories.unified_cache_repository import get_unified_cache_repository
                unified_cache = get_unified_cache_repository()

                # Extract quantitative sections from report and add metadata
                # Report structure has header, maturity, nps, tech_insights at top level
                # Unified cache needs them under 'quantitative' key, but save_quantitative_data handles that
                data_hash = self._calculate_data_hash(org_name)
                quantitative_data = {
                    'header': report.get('header', {}),  # Include header for template compatibility
                    'maturity': report.get('maturity', {}),
                    'nps': report.get('nps', {}),
                    'tech_insights': report.get('tech_insights', {}),
                    'metadata': {
                        'cached_at': datetime.now().isoformat(),
                        'data_hash': data_hash,
                        'version': self._get_algorithm_version()
                    }
                }

                # CRITICAL FIX (JJF-60, JJF-61, JJF-62): Merge AI modifiers into BOTH cache AND returned report
                # JJF-60: Fixed cached loading path to include modifiers
                # JJF-61: Added cache-save path merging logic
                # JJF-62: Apply merged modifiers to returned report (not just cache)
                # Without this, fresh generation returns report WITHOUT modifiers, causing inconsistency
                report_dict = {
                    'maturity': quantitative_data.get('maturity', {}),
                    'header': quantitative_data.get('header', {}),
                    'nps': quantitative_data.get('nps', {}),
                    'tech_insights': quantitative_data.get('tech_insights', {})
                }
                report_dict = self._merge_ai_modifiers_into_report(report_dict, org_name)

                # Update BOTH cache data and returned report
                quantitative_data['maturity'] = report_dict.get('maturity', {})
                report = report_dict  # JJF-62 FIX: Apply merged modifiers to returned report

                # DEBUG: Log modifier state before save
                if 'maturity' in quantitative_data and 'variance_analysis' in quantitative_data['maturity']:
                    for dim_name, dim_data in quantitative_data['maturity']['variance_analysis'].items():
                        if 'total_modifier' in dim_data:
                            print(f"[Cache] Pre-save check: {dim_name} has total_modifier={dim_data.get('total_modifier')}, source={dim_data.get('modifier_source')}")

                success = unified_cache.save_quantitative_data(org_name, quantitative_data)
                if success:
                    print(f"[UnifiedCache] Saved quantitative report for {org_name}")
                else:
                    print(f"[UnifiedCache] WARNING: Failed to save quantitative report for {org_name}")

            return report
        except Exception as e:
            print(f"Error generating organization report for {org_name}: {e}")
            return None

    def get_aggregate_report(self, use_cache: bool = True) -> Optional[Dict[str, Any]]:
        """
        Get aggregate report synchronously (for front-end views).

        Args:
            use_cache: Whether to use cached report (currently unused, reserved for future caching)

        Returns:
            Aggregate report dictionary or None
        """
        try:
            # Get fresh data for report generation
            sheet_data = self._data_service.get_all_data()
            admin_edits = self._admin_edit_service.get_all_edits()

            # Create fresh ReportGenerator with current data
            fresh_generator = ReportGenerator(
                sheet_data=sheet_data,
                enable_ai=bool(os.getenv("OPENROUTER_API_KEY")),
                admin_edits=admin_edits,
            )

            # Use fresh ReportGenerator for synchronous operation
            return fresh_generator.generate_aggregate_report()
        except Exception as e:
            print(f"Error generating aggregate report: {e}")
            return None

    def capture_print_snapshot(self, org_name: str) -> Dict[str, Any]:
        """
        Capture a print-ready snapshot of organization report.

        Args:
            org_name: Organization name

        Returns:
            Dictionary with snapshot_id and metadata
        """
        try:
            # Get fresh data for report generation
            sheet_data = self._data_service.get_all_data()
            admin_edits = self._admin_edit_service.get_all_edits()

            # Create fresh ReportGenerator with current data
            fresh_generator = ReportGenerator(
                sheet_data=sheet_data,
                enable_ai=bool(os.getenv("OPENROUTER_API_KEY")),
                admin_edits=admin_edits,
            )

            # Generate report synchronously for snapshot
            report = fresh_generator.generate_organization_report(org_name)

            if not report:
                return {"success": False, "error": f"Failed to generate report for {org_name}"}

            # Create snapshot ID
            snapshot_id = f"{org_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # Store snapshot (in future, could save to disk/S3)
            with self._lock:
                if not hasattr(self, "_snapshots"):
                    self._snapshots = {}
                self._snapshots[snapshot_id] = {
                    "snapshot_id": snapshot_id,
                    "org_name": org_name,
                    "created_at": datetime.now().isoformat(),
                    "report": report,
                }

            return {
                "success": True,
                "snapshot_id": snapshot_id,
                "org_name": org_name,
                "created_at": datetime.now().isoformat(),
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_snapshot(self, snapshot_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a saved snapshot.

        Args:
            snapshot_id: Snapshot identifier

        Returns:
            Snapshot data or None if not found
        """
        with self._lock:
            if not hasattr(self, "_snapshots"):
                return None
            return self._snapshots.get(snapshot_id)

    def get_organization_report_from_snapshot(
        self, org_name: str, snapshot_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get organization report from a saved snapshot.

        Args:
            org_name: Organization name (for validation)
            snapshot_id: Snapshot identifier

        Returns:
            Report data from snapshot or None if not found
        """
        snapshot = self.get_snapshot(snapshot_id)
        if snapshot and snapshot.get("org_name") == org_name:
            return snapshot.get("report")
        return None

    def generate_pdf(self, html_content: str, org_name: str) -> Dict[str, Any]:
        """
        Generate PDF from HTML content.

        Attempts multiple strategies:
        1. pdfkit (wkhtmltopdf) if available
        2. Fallback to returning HTML with print styles

        Args:
            html_content: Rendered HTML content
            org_name: Organization name (for filename)

        Returns:
            Dictionary with:
              - success: bool
              - pdf_data: bytes (if successful)
              - error: str (if failed)
              - fallback_html: str (if pdfkit unavailable)
        """
        try:
            # Try importing pdfkit
            import pdfkit

            # PDF generation options
            options = {
                "page-size": "A4",
                "margin-top": "0.5in",
                "margin-right": "0.5in",
                "margin-bottom": "0.5in",
                "margin-left": "0.5in",
                "encoding": "UTF-8",
                "no-outline": None,
                "enable-local-file-access": None,
                "print-media-type": None,
                "quiet": "",
            }

            # Generate PDF from HTML string
            pdf_data = pdfkit.from_string(html_content, False, options=options)

            return {"success": True, "pdf_data": pdf_data}

        except ImportError:
            # pdfkit not installed, return HTML with print styles
            return {
                "success": False,
                "error": "pdfkit not installed",
                "fallback_html": html_content,
                "message": "PDF generation requires wkhtmltopdf. Returning HTML for browser printing.",
            }

        except Exception as e:
            # Other errors (wkhtmltopdf not found, etc.)
            return {
                "success": False,
                "error": str(e),
                "fallback_html": html_content,
                "message": f"PDF generation failed: {str(e)}. Use browser print instead.",
            }

    # Private task execution methods

    def _generate_org_report_task(
        self, task_id: str, org_name: str, enable_ai: bool, force_regenerate: bool
    ) -> None:
        """Execute organization report generation task."""
        try:
            # Update status to in_progress
            self._update_progress(task_id, 10, "Initializing report generation...")

            # Get fresh data and edits for this report
            sheet_data = self._data_service.get_all_data()
            admin_edits = self._admin_edit_service.get_all_edits()

            # Create generator with requested AI setting (per-request)
            generator = ReportGenerator(
                sheet_data=sheet_data,
                enable_ai=enable_ai,  # Use the requested setting
                admin_edits=admin_edits,
            )

            self._update_progress(task_id, 20, f"Generating report for {org_name}...")

            # Generate report with this generator
            # Note: force_regenerate parameter is currently unused (reserved for future caching)
            report = generator.generate_organization_report(org_name)

            # Update progress
            self._update_progress(task_id, 90, "Finalizing report...")

            # Store result
            with self._lock:
                if task_id in self._tasks:
                    self._tasks[task_id]["status"] = "complete"
                    self._tasks[task_id]["progress"] = 100
                    self._tasks[task_id]["completed_at"] = datetime.now().isoformat()
                    self._tasks[task_id]["result"] = report

        except Exception as e:
            # Store error
            with self._lock:
                if task_id in self._tasks:
                    self._tasks[task_id]["status"] = "error"
                    self._tasks[task_id]["error"] = str(e)
                    self._tasks[task_id]["completed_at"] = datetime.now().isoformat()

    def _update_progress(self, task_id: str, progress: int, message: str = None) -> None:
        """
        Update task progress.

        Args:
            task_id: Task identifier
            progress: Progress percentage (0-100)
            message: Optional progress message
        """
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id]["progress"] = progress
                if message:
                    self._tasks[task_id]["message"] = message

    def _generate_aggregate_report_task(self, task_id: str) -> None:
        """Execute aggregate report generation task."""
        try:
            # Update status to in_progress
            with self._lock:
                if task_id in self._tasks:
                    self._tasks[task_id]["status"] = "in_progress"
                    self._tasks[task_id]["progress"] = 10

            # Get fresh data for report generation
            sheet_data = self._data_service.get_all_data()
            admin_edits = self._admin_edit_service.get_all_edits()

            # Create fresh ReportGenerator with current data
            fresh_generator = ReportGenerator(
                sheet_data=sheet_data,
                enable_ai=bool(os.getenv("OPENROUTER_API_KEY")),
                admin_edits=admin_edits,
            )

            # Generate aggregate report using fresh ReportGenerator
            report = fresh_generator.generate_aggregate_report()

            # Update progress
            with self._lock:
                if task_id in self._tasks:
                    self._tasks[task_id]["progress"] = 90

            # Store result
            with self._lock:
                if task_id in self._tasks:
                    self._tasks[task_id]["status"] = "complete"
                    self._tasks[task_id]["progress"] = 100
                    self._tasks[task_id]["completed_at"] = datetime.now().isoformat()
                    self._tasks[task_id]["result"] = report

        except Exception as e:
            # Store error
            with self._lock:
                if task_id in self._tasks:
                    self._tasks[task_id]["status"] = "error"
                    self._tasks[task_id]["error"] = str(e)
                    self._tasks[task_id]["completed_at"] = datetime.now().isoformat()

    # 3-Phase Report Generation Methods

    def generate_ai_analysis_async(self, org_name: str) -> str:
        """
        Phase 1: Generate AI analysis asynchronously with granular progress.

        Args:
            org_name: Organization name

        Returns:
            Task ID for progress tracking
        """
        task_id = str(uuid.uuid4())

        # Initialize progress
        with self._lock:
            self._tasks[task_id] = {
                "task_id": task_id,
                "type": "ai_analysis",
                "org_name": org_name,
                "status": "in_progress",
                "progress": 0,
                "message": "Starting AI analysis...",
                "started_at": datetime.now().isoformat(),
                "completed_at": None,
                "result": None,
                "error": None,
                "phase": "ai_analysis",
            }

        # Submit to thread pool
        self._executor.submit(self._generate_ai_analysis_task, task_id, org_name)

        return task_id

    def generate_scores_sync(self, org_name: str) -> dict:
        """
        Phase 2: Generate quantitative scores synchronously (fast, no AI).

        Args:
            org_name: Organization name

        Returns:
            Dictionary containing scores data
        """

        # Get organization data
        sheet_data = self._data_service.get_all_data()
        admin_edits = self._admin_edit_service.get_all_edits()

        # Create generator WITHOUT AI
        generator = ReportGenerator(
            sheet_data=sheet_data, enable_ai=False, admin_edits=admin_edits  # NO AI for this phase
        )

        # Generate report (only quantitative parts will run)
        report_data = generator.generate_organization_report(org_name)

        if not report_data:
            raise ValueError(f"Could not generate scores for {org_name}")

        # Extract only the scores data (quantitative, non-AI data)
        # IMPORTANT: tech_insights is quantitative data (frequency counts from survey responses)
        # It belongs in scores cache, NOT AI cache, so it persists when AI cache is cleared
        scores_data = {
            "organization": org_name,
            "maturity": report_data.get("maturity", {}),
            "nps": report_data.get("nps", {}),
            "variance_analysis": report_data.get("variance_analysis", {}),
            "numeric_responses": report_data.get("numeric_responses", {}),
            "tech_insights": report_data.get("tech_insights", {}),  # Added: quantitative tech data
        }

        return scores_data

    def merge_and_generate_html(self, org_name: str, ai_data: dict, scores_data: dict) -> str:
        """
        Phase 3: Merge AI and scores, generate final HTML report.

        Args:
            org_name: Organization name
            ai_data: Cached AI analysis data
            scores_data: Cached scores data

        Returns:
            URL path to generated report
        """
        # Get organization data
        sheet_data = self._data_service.get_all_data()
        admin_edits = self._admin_edit_service.get_all_edits()

        # Create generator with AI enabled
        generator = ReportGenerator(sheet_data=sheet_data, enable_ai=True, admin_edits=admin_edits)

        # Generate base report
        report_data = generator.generate_organization_report(org_name)

        if not report_data:
            raise ValueError(f"Could not generate report for {org_name}")

        # Merge in the cached AI analysis
        if ai_data:
            report_data["ai_insights"] = ai_data

            # Apply AI modifiers to scores
            if ai_data.get("dimensions"):
                self._apply_ai_modifiers_to_report(report_data, ai_data)

        # Note: Currently no separate cache for merged reports
        # The report_data is returned and rendered directly by the view

        return f"/report/org/{org_name}"

    def _apply_ai_modifiers_to_report(self, report_data: dict, ai_data: dict) -> None:
        """Apply AI score modifiers to the base quantitative scores."""
        dimensions = report_data.get("maturity", {}).get("dimensions", {})
        ai_dimensions = ai_data.get("dimensions", {})

        for dim_name, dim_data in dimensions.items():
            if dim_name in ai_dimensions:
                ai_modifiers = ai_dimensions[dim_name].get("modifiers", [])

                # Calculate total modifier
                total_modifier = sum(m.get("value", 0) for m in ai_modifiers)

                # Apply to score
                original_score = dim_data.get("weighted_score", 0)
                adjusted_score = max(0, min(5, original_score + total_modifier))

                dim_data["ai_modifier"] = total_modifier
                dim_data["adjusted_score"] = adjusted_score

    def _generate_ai_analysis_task(self, task_id: str, org_name: str) -> None:
        """Background task for Phase 1: AI analysis only (now uses async concurrent processing)."""
        try:
            self._update_progress(task_id, 5, "Fetching organization data...")

            # Get organization data
            sheet_data = self._data_service.get_all_data()
            org_data = self._extract_org_data(org_name, sheet_data)

            if not org_data:
                self._update_progress(task_id, 0, f"Organization '{org_name}' not found")
                with self._lock:
                    if task_id in self._tasks:
                        self._tasks[task_id]["status"] = "error"
                        self._tasks[task_id]["error"] = f"Organization '{org_name}' not found"
                        self._tasks[task_id]["completed_at"] = datetime.now().isoformat()
                return

            self._update_progress(task_id, 10, "Extracting free text responses...")

            # Extract free text responses
            from src.analytics.ai_analyzer import extract_free_text_responses

            free_text_responses = extract_free_text_responses(sheet_data, org_name)

            # Create progress callback for granular tracking
            def ai_progress_callback(progress_pct, message):
                # Map AI progress (0-100%) to our range (10-95%)
                mapped_progress = 10 + int(progress_pct * 0.85)
                self._update_progress(task_id, mapped_progress, message)

            self._update_progress(task_id, 15, "Starting concurrent AI analysis (5 dimensions)...")

            # Create AI analyzer
            admin_edits = self._admin_edit_service.get_all_edits()
            generator = ReportGenerator(
                sheet_data=sheet_data, enable_ai=True, admin_edits=admin_edits
            )

            # Run ASYNC AI analysis with concurrent dimension processing
            if generator.ai_analyzer:
                # Run async analysis in the thread pool's event loop
                ai_insights = asyncio.run(
                    generator.ai_analyzer.analyze_organization_qualitative_async(
                        org_name, free_text_responses, progress_callback=ai_progress_callback
                    )
                )

                # Save to cache
                self.save_ai_analysis(org_name, ai_insights)

                self._update_progress(task_id, 100, "AI analysis complete!")
                with self._lock:
                    if task_id in self._tasks:
                        self._tasks[task_id]["status"] = "complete"
                        self._tasks[task_id]["result"] = ai_insights
                        self._tasks[task_id]["completed_at"] = datetime.now().isoformat()
            else:
                self._update_progress(task_id, 0, "AI analyzer not available")
                with self._lock:
                    if task_id in self._tasks:
                        self._tasks[task_id]["status"] = "error"
                        self._tasks[task_id]["error"] = "AI analyzer not available"
                        self._tasks[task_id]["completed_at"] = datetime.now().isoformat()

        except Exception as e:
            import traceback

            error_msg = f"Error during AI analysis: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            self._update_progress(task_id, 0, error_msg)
            with self._lock:
                if task_id in self._tasks:
                    self._tasks[task_id]["status"] = "error"
                    self._tasks[task_id]["error"] = error_msg
                    self._tasks[task_id]["completed_at"] = datetime.now().isoformat()

    def _extract_org_data(self, org_name: str, sheet_data: dict) -> Optional[dict]:
        """Extract organization data from sheets (helper method)."""
        org_data = {"ceo_record": None, "tech_records": [], "staff_records": []}

        # Get CEO record
        ceo_data = sheet_data.get("CEO", [])
        for record in ceo_data:
            if record.get("CEO Organization") == org_name:
                org_data["ceo_record"] = record
                break

        # Get Tech records
        tech_data = sheet_data.get("Tech", [])
        for record in tech_data:
            if record.get("Organization") == org_name:
                org_data["tech_records"].append(record)

        # Get Staff records
        staff_data = sheet_data.get("Staff", [])
        for record in staff_data:
            if record.get("Organization") == org_name:
                org_data["staff_records"].append(record)

        # Return None if no data found
        if not any([org_data["ceo_record"], org_data["tech_records"], org_data["staff_records"]]):
            return None

        return org_data

    # Cache Management Methods

    def _get_cache_path(self, org_name: str, cache_type: str) -> str:
        """Get cache file path for organization report data."""
        import os

        cache_dir = os.path.join("cache", "reports")
        os.makedirs(cache_dir, exist_ok=True)

        # Sanitize org name for filename
        safe_name = org_name.replace(" ", "_").replace("/", "_")
        filename = f"{safe_name}_{cache_type}.json"
        return os.path.join(cache_dir, filename)

    def save_ai_analysis(self, org_name: str, ai_data: dict) -> str:
        """Save AI analysis results to JSON cache."""
        import json
        from datetime import datetime

        filepath = self._get_cache_path(org_name, "ai_analysis")

        # Add metadata
        ai_data["metadata"] = {
            "organization": org_name,
            "generated_at": datetime.utcnow().isoformat(),
            "cache_type": "ai_analysis",
        }

        with open(filepath, "w") as f:
            json.dump(ai_data, f, indent=2)

        print(f"[Cache] Saved AI analysis to {filepath}")
        return filepath

    def load_ai_analysis(self, org_name: str) -> Optional[dict]:
        """Load cached AI analysis results."""
        import json
        import os

        filepath = self._get_cache_path(org_name, "ai_analysis")

        if not os.path.exists(filepath):
            return None

        with open(filepath, "r") as f:
            data = json.load(f)

        print(f"[Cache] Loaded AI analysis from {filepath}")
        return data

    def save_scores(self, org_name: str, scores_data: dict) -> str:
        """Save quantitative scores to JSON cache."""
        import json
        from datetime import datetime

        filepath = self._get_cache_path(org_name, "scores")

        # Add metadata
        scores_data["metadata"] = {
            "organization": org_name,
            "generated_at": datetime.utcnow().isoformat(),
            "cache_type": "scores",
        }

        with open(filepath, "w") as f:
            json.dump(scores_data, f, indent=2)

        print(f"[Cache] Saved scores to {filepath}")
        return filepath

    def load_scores(self, org_name: str) -> Optional[dict]:
        """Load cached quantitative scores."""
        import json
        import os

        filepath = self._get_cache_path(org_name, "scores")

        if not os.path.exists(filepath):
            return None

        with open(filepath, "r") as f:
            data = json.load(f)

        print(f"[Cache] Loaded scores from {filepath}")
        return data

    def check_cache_status(self, org_name: str) -> dict:
        """Check if cached data exists for organization."""
        import os

        ai_path = self._get_cache_path(org_name, "ai_analysis")
        scores_path = self._get_cache_path(org_name, "scores")

        return {
            "ai_cached": os.path.exists(ai_path),
            "scores_cached": os.path.exists(scores_path),
            "ai_path": ai_path if os.path.exists(ai_path) else None,
            "scores_path": scores_path if os.path.exists(scores_path) else None,
        }

    def shutdown(self) -> None:
        """Shutdown the executor and cleanup resources."""
        self._executor.shutdown(wait=True)

    # Cache Hash Calculation Methods

    def _merge_admin_edits_into_report(self, report: Dict[str, Any], org_admin_edits: Dict[str, Any], org_name: str) -> Dict[str, Any]:
        """
        Merge fresh admin edits into a cached report.

        This is critical for cache correctness: admin_edits.json is the source of truth
        for modifiers, but the quantitative cache only contains base calculations.
        We must merge them together before serving to the user.

        Args:
            report: Cached report dictionary
            org_admin_edits: Admin edits for this organization from admin_edits.json
            org_name: Organization name (for logging)

        Returns:
            Report with admin edits merged in
        """
        if not report or not org_admin_edits:
            return report

        # Get or create ai_insights section
        if 'ai_insights' not in report:
            report['ai_insights'] = {}

        ai_insights = report['ai_insights']

        # Get or create dimensions section
        if 'dimensions' not in ai_insights:
            ai_insights['dimensions'] = {}

        # Merge score modifiers into each dimension
        score_modifiers = org_admin_edits.get('score_modifiers', {})

        for dimension, modifiers in score_modifiers.items():
            dimension_key = dimension.replace(' ', '_')

            # Get or create dimension entry
            if dimension_key not in ai_insights['dimensions']:
                ai_insights['dimensions'][dimension_key] = {}

            dimension_data = ai_insights['dimensions'][dimension_key]

            # Inject modifiers
            dimension_data['score_modifiers'] = modifiers
            dimension_data['modifier_source'] = 'admin'

            # Recalculate impact using the modifiers
            base_score = dimension_data.get('base_score', 0.0)
            total_modifier = sum(m.get('value', 0) for m in modifiers)

            # Update modifier_summary
            dimension_data['modifier_summary'] = {
                'modifier_count': len(modifiers),
                'total_modifier': total_modifier,
                'source': 'admin'
            }

            # Update impact_summary
            dimension_weight = dimension_data.get('impact_summary', {}).get('dimension_weight', 0.2)
            overall_impact = total_modifier * dimension_weight

            dimension_data['impact_summary'] = dimension_data.get('impact_summary', {})
            dimension_data['impact_summary']['overall_impact'] = overall_impact
            dimension_data['impact_summary']['dimension_weight'] = dimension_weight

        # CRITICAL: Also update variance_analysis section (used by report template)
        if 'maturity' in report and 'variance_analysis' in report['maturity']:
            variance_analysis = report['maturity']['variance_analysis']

            for dimension, modifiers in score_modifiers.items():
                # Try both formats: "Data Management" and "Data_Management"
                dimension_with_space = dimension.replace('_', ' ')
                dimension_with_underscore = dimension.replace(' ', '_')

                # Find the dimension in variance_analysis
                analysis_key = None
                if dimension_with_space in variance_analysis:
                    analysis_key = dimension_with_space
                elif dimension_with_underscore in variance_analysis:
                    analysis_key = dimension_with_underscore
                elif dimension in variance_analysis:
                    analysis_key = dimension

                if analysis_key:
                    analysis = variance_analysis[analysis_key]
                    base_score = analysis.get('weighted_score', 0.0)
                    total_modifier = sum(m.get('value', 0) for m in modifiers)
                    adjusted_score = max(0, min(5, base_score + total_modifier))

                    # Update variance_analysis with admin modifier data
                    analysis['total_modifier'] = total_modifier
                    analysis['adjusted_score'] = adjusted_score
                    analysis['modifier_source'] = 'admin'
                    analysis['modifier_count'] = len(modifiers)

                    # CRITICAL FIX: Recalculate checksum after updating modifier values
                    # Without this, checksum reflects stale pre-modifier values
                    analysis['checksum'] = self._calculate_dimension_checksum(analysis)

                    print(f"[Cache] Updated variance_analysis for {analysis_key}: base={base_score:.2f} + modifier={total_modifier:.2f} = adjusted={adjusted_score:.2f}")

        print(f"[Cache] Merged {len(score_modifiers)} dimension modifiers for {org_name}")

        return report

    def _merge_ai_modifiers_into_report(self, report: Dict[str, Any], org_name: str) -> Dict[str, Any]:
        """
        Merge AI modifiers from qualitative cache into report's variance_analysis.

        This method loads AI modifiers from the OLD qualitative cache location and merges
        them into the variance_analysis section. This is necessary because the unified cache
        doesn't store AI modifiers directly - they're kept separately in qualitative cache.

        Args:
            report: Report dictionary (from unified cache or fresh generation)
            org_name: Organization name

        Returns:
            Report with AI modifiers merged into variance_analysis
        """
        if not report or 'maturity' not in report or 'variance_analysis' not in report['maturity']:
            print(f"[Cache] No variance_analysis found in report for {org_name}, skipping AI modifier merge")
            return report

        variance_analysis = report['maturity']['variance_analysis']
        print(f"[Cache] Checking OLD qualitative cache (legacy location) for AI modifiers to merge into variance_analysis...")

        # Import and load from OLD qualitative cache location
        from src.repositories.qualitative_cache_file_repository import QualitativeCacheFileRepository

        qualitative_data = None
        # Try actual cache location first (qualitative_cache/)
        try:
            actual_cache = QualitativeCacheFileRepository(cache_dir="qualitative_cache")
            qualitative_data = actual_cache.load_organization_qualitative_data(org_name)
            if qualitative_data and qualitative_data.get('dimensions'):
                print(f"[Cache] Found qualitative data in ACTUAL location (qualitative_cache/)")
        except Exception as e:
            print(f"[Cache] No data in actual location: {e}")

        # Fallback to config default location if actual location had no data
        if not qualitative_data or not qualitative_data.get('dimensions'):
            try:
                from config import Config
                config_cache_dir = Config().QUALITATIVE_CACHE_DIR
                default_cache = QualitativeCacheFileRepository(cache_dir=config_cache_dir)
                qualitative_data = default_cache.load_organization_qualitative_data(org_name)
                if qualitative_data and qualitative_data.get('dimensions'):
                    print(f"[Cache] Found qualitative data in CONFIG location ({config_cache_dir})")
            except Exception as e:
                print(f"[Cache] No data in config location: {e}")

        if qualitative_data and 'dimensions' in qualitative_data:
            modifiers_merged = 0
            for dimension_name, dimension_data in qualitative_data['dimensions'].items():
                # Get AI modifiers from qualitative cache
                # Note: load_organization_qualitative_data() returns FLATTENED structure
                # where modifiers are directly under dimension_data, not nested in ai_generated
                modifiers = dimension_data.get('modifiers', [])

                if modifiers:
                    # Find matching dimension in variance_analysis
                    # Try both formats: "Data Management" and "Data_Management"
                    dimension_with_space = dimension_name.replace('_', ' ')
                    dimension_with_underscore = dimension_name.replace(' ', '_')

                    analysis_key = None
                    if dimension_with_space in variance_analysis:
                        analysis_key = dimension_with_space
                    elif dimension_with_underscore in variance_analysis:
                        analysis_key = dimension_with_underscore
                    elif dimension_name in variance_analysis:
                        analysis_key = dimension_name

                    if analysis_key:
                        analysis = variance_analysis[analysis_key]
                        base_score = analysis.get('weighted_score', 0.0)
                        total_modifier = sum(m.get('value', 0) for m in modifiers)
                        adjusted_score = max(0, min(5, base_score + total_modifier))

                        # Merge modifier data into variance_analysis
                        analysis['total_modifier'] = total_modifier
                        analysis['adjusted_score'] = adjusted_score
                        analysis['modifier_source'] = 'ai'  # From AI analysis
                        analysis['modifier_count'] = len(modifiers)

                        # CRITICAL FIX: Recalculate checksum after updating modifier values
                        # Without this, checksum reflects stale pre-modifier values
                        analysis['checksum'] = self._calculate_dimension_checksum(analysis)
                        print(f"[Cache] Recalculated checksum for {analysis_key}: {analysis['checksum']['calculation']}")

                        modifiers_merged += 1
                        print(f"[Cache] Merged {len(modifiers)} AI modifiers into {analysis_key}: total_modifier={total_modifier:+.2f}")

            if modifiers_merged > 0:
                print(f"[Cache] Successfully merged AI modifiers into {modifiers_merged} dimensions")
        else:
            from config import Config
            config_cache_dir = Config().QUALITATIVE_CACHE_DIR
            print(f"[Cache] No qualitative data found for {org_name} (tried: qualitative_cache/ and {config_cache_dir})")

        return report

    def _calculate_dimension_checksum(self, dimension_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate verification checksum for dimension score calculation.

        Validates that adjusted_score = max(0, min(5, base_score + total_modifier))

        This is a copy of the logic from report_generator.py to ensure checksum
        consistency when modifiers are merged from cache.

        Args:
            dimension_analysis: Dimension variance analysis dictionary

        Returns:
            Dictionary containing checksum, validation status, and debugging info
        """
        import hashlib

        # Extract calculation components
        base_score = dimension_analysis.get("weighted_score", 0)
        total_modifier = dimension_analysis.get("total_modifier", 0)
        adjusted_score = dimension_analysis.get("adjusted_score", 0)

        # Calculate expected result
        expected_score = max(0, min(5, base_score + total_modifier))

        # Calculate error (should be ~0 for correct calculations)
        error = abs(adjusted_score - expected_score)
        is_valid = error < 0.001  # Allow tiny floating point errors

        # Create human-readable calculation string
        calculation_str = f"{base_score:.2f} + {total_modifier:.2f} = {adjusted_score:.2f}"
        formula_str = f"max(0, min(5, {base_score:.2f} + {total_modifier:.2f}))"

        # Generate checksum from calculation components
        checksum_input = f"{base_score}|{total_modifier}|{adjusted_score}"
        checksum = hashlib.md5(checksum_input.encode()).hexdigest()[:8]

        return {
            "checksum": checksum,
            "calculation": calculation_str,
            "formula": formula_str,
            "valid": is_valid,
            "expected": round(expected_score, 2),
            "actual": round(adjusted_score, 2),
            "error": round(error, 4),
            "components": {
                "base_score": round(base_score, 2),
                "total_modifier": round(total_modifier, 2),
                "adjusted_score": round(adjusted_score, 2),
            },
        }

    def _calculate_data_hash(self, org_name: str) -> str:
        """
        Calculate SHA256 hash of relevant source data for cache invalidation.

        Hash includes:
        - Organization survey responses
        - Admin edits for this organization
        - Algorithm configuration version

        Args:
            org_name: Organization name

        Returns:
            SHA256 hash string (64 characters hex)
        """
        import hashlib
        import json

        # Get organization data
        sheet_data = self._data_service.get_all_data()
        org_data = self._extract_org_data(org_name, sheet_data)

        # Get admin edits for this organization
        admin_edits = self._admin_edit_service.get_org_edits(org_name)

        # Get algorithm config version
        algorithm_version = self._get_algorithm_version()

        # Build data dictionary for hashing
        data_dict = {
            'org_name': org_name,
            'org_data': org_data,
            'admin_edits': admin_edits,
            'algorithm_version': algorithm_version
        }

        # Convert to deterministic JSON string
        data_str = json.dumps(data_dict, sort_keys=True, default=str)

        # Calculate SHA256 hash
        return hashlib.sha256(data_str.encode()).hexdigest()

    def _get_algorithm_version(self) -> str:
        """
        Get current algorithm configuration version.

        Returns:
            Version string from algorithm config
        """
        try:
            from src.services.algorithm_config_service import get_algorithm_config_service
            config_service = get_algorithm_config_service()
            metadata = config_service.get_metadata()
            # Return version from config or default
            config = config_service.get_config()
            return str(config.get('version', '1.0'))
        except Exception:
            return '1.0'

    # Progressive Loading Methods

    def generate_ai_summary_only(self, org_name: str) -> str:
        """
        Generate only the executive summary (overall_summary) for an organization.

        Progressive loading: Returns just the summary text, saves to cache.

        Args:
            org_name: Organization name

        Returns:
            Summary text string
        """
        from src.analytics.ai_analyzer import extract_free_text_responses

        # Get organization data
        sheet_data = self._data_service.get_all_data()

        # Extract free text responses
        free_text_responses = extract_free_text_responses(sheet_data, org_name)

        # Flatten all responses for summary
        all_texts = []
        for dimension, responses in free_text_responses.items():
            for r in responses:
                all_texts.append({"dimension": dimension, "organization": org_name, **r})

        if not all_texts:
            return "No free text feedback available for analysis."

        # Generate summary using AI analyzer
        admin_edits = self._admin_edit_service.get_all_edits()
        generator = ReportGenerator(sheet_data=sheet_data, enable_ai=True, admin_edits=admin_edits)

        if generator.ai_analyzer:
            summary = generator.ai_analyzer.summarize_all_feedback(all_texts)

            # Update cache with summary (partial update)
            ai_data = self.load_ai_analysis(org_name) or {}
            ai_data["overall_summary"] = summary
            self.save_ai_analysis(org_name, ai_data)

            return summary

        return "AI analyzer not available"

    def generate_ai_dimension_insight(self, org_name: str, dimension: str) -> Dict[str, Any]:
        """
        Generate AI insight for a single dimension only.

        Progressive loading: Returns just one dimension's analysis, saves to cache.

        Args:
            org_name: Organization name
            dimension: Dimension name (e.g., "Program Technology")

        Returns:
            Dict with 'summary' and 'modifiers' for the dimension
        """
        from src.analytics.ai_analyzer import extract_free_text_responses

        # Get organization data
        sheet_data = self._data_service.get_all_data()

        # Extract free text responses
        free_text_responses = extract_free_text_responses(sheet_data, org_name)

        # Get responses for this specific dimension
        dimension_responses = free_text_responses.get(dimension, [])

        if not dimension_responses:
            return {"summary": f"No free text responses for {dimension}", "modifiers": []}

        # Generate insight using AI analyzer
        admin_edits = self._admin_edit_service.get_all_edits()
        generator = ReportGenerator(sheet_data=sheet_data, enable_ai=True, admin_edits=admin_edits)

        if generator.ai_analyzer:
            # Analyze this dimension (JJF-11: Pass org_name for sanity checking)
            result = generator.ai_analyzer.analyze_dimension_responses(
                dimension, dimension_responses, org_name
            )

            # Update cache with this dimension (partial update)
            ai_data = self.load_ai_analysis(org_name) or {}
            if "dimensions" not in ai_data:
                ai_data["dimensions"] = {}
            ai_data["dimensions"][dimension] = result
            self.save_ai_analysis(org_name, ai_data)

            return result

        return {"summary": "AI analyzer not available", "modifiers": []}
