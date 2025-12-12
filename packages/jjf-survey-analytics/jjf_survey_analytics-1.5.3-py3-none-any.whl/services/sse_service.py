#!/usr/bin/env python3
"""
SSEService - Server-Sent Events streaming service for real-time progress updates.

Provides SSE event generation and streaming for dimension analysis progress.
Enables progressive loading of qualitative data in the card-based editor.

Features:
- Standard SSE event formatting (event + data + double newline)
- Concurrent dimension analysis orchestration
- Real-time progress updates during analysis
- Heartbeat events to prevent connection timeout
- Graceful error handling and client disconnect detection

Usage:
    from src.services.sse_service import SSEService

    # Create service
    service = SSEService(session_manager, cache_repo)

    # Stream analysis progress
    response = service.stream_dimension_analysis(
        session_id="uuid",
        org_name="Example Org",
        dimensions=["Program Technology", ...]
    )

Event Types:
    - dimension_started: Analysis begins for a dimension
    - dimension_progress: Progress update during analysis (optional)
    - dimension_complete: Analysis finished with full data
    - dimension_error: Analysis failed with error details
    - session_complete: All dimensions analyzed
    - heartbeat: Keep-alive ping every 15 seconds
"""

import asyncio
import json
import logging
import queue
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Any, Callable, Dict, Generator, List, Optional

from flask import Response

from src.services.build_review_session import BuildReviewSessionManager
from src.services.dimension_analysis_orchestrator import DimensionAnalysisOrchestrator
from src.repositories.qualitative_cache_file_repository import QualitativeCacheFileRepository

logger = logging.getLogger(__name__)


class SSEService:
    """
    Server-Sent Events service for streaming dimension analysis progress.

    Orchestrates concurrent dimension analysis and sends real-time progress
    updates via SSE protocol to the client.
    """

    # SSE configuration
    HEARTBEAT_INTERVAL = 15  # seconds
    DIMENSION_TIMEOUT = 30  # seconds per dimension
    MAX_CONCURRENT = 5  # Max concurrent dimension analyses

    def __init__(
        self,
        session_manager: BuildReviewSessionManager,
        cache_repository: QualitativeCacheFileRepository,
        orchestrator: Optional[DimensionAnalysisOrchestrator] = None
    ):
        """
        Initialize SSE service.

        Args:
            session_manager: Session manager for tracking progress
            cache_repository: Cache repository for checking/loading cached data
            orchestrator: Dimension analysis orchestrator (optional, creates new if not provided)
        """
        self.session_manager = session_manager
        self.cache_repository = cache_repository
        self.orchestrator = orchestrator or DimensionAnalysisOrchestrator(
            cache_repository=cache_repository
        )

    def stream_dimension_analysis(
        self,
        session_id: str,
        org_name: str,
        dimensions: List[str],
        sheet_data: Dict[str, List[Dict[str, Any]]],
        analysis_function: Optional[Callable] = None
    ) -> Response:
        """
        Stream dimension analysis progress via SSE.

        Creates SSE stream that sends events as each dimension analysis completes.
        Handles both cached and uncached dimensions, processing uncached ones
        concurrently.

        Args:
            session_id: Session UUID from build-review initialization
            org_name: Organization name
            dimensions: List of dimensions to analyze
            sheet_data: Complete sheet data from SheetsReader (dict with CEO/Tech/Staff tabs)
            analysis_function: Function to generate analysis (optional, for testing)

        Returns:
            Flask Response with SSE stream (Content-Type: text/event-stream)

        Event Flow:
            1. dimension_started (for each dimension)
            2. dimension_complete (when analysis finishes, with full data)
            3. dimension_error (if analysis fails)
            4. session_complete (when all dimensions done)
            5. heartbeat (every 15 seconds during processing)
        """
        def event_stream() -> Generator[str, None, None]:
            """
            Generate SSE events for dimension analysis progress.

            Yields formatted SSE messages as analysis progresses.
            """
            try:
                # Validate session exists
                session = self.session_manager.get_session(session_id)
                if not session:
                    error_event = self._format_event("error", {
                        "error": "Session not found or expired",
                        "session_id": session_id
                    })
                    yield error_event
                    return

                # Track analysis metrics
                start_time = time.time()
                completed_count = 0
                failed_count = 0
                total_dimensions = len(dimensions)

                # Process dimensions concurrently
                with ThreadPoolExecutor(max_workers=self.MAX_CONCURRENT) as executor:
                    # Submit all dimension analyses
                    future_to_dimension = {}

                    # Load dimension scores (base_score) once for all dimensions
                    # This is needed to add base_score to cached dimension data
                    dimension_scores = self._load_dimension_scores(org_name)

                    for dimension in dimensions:
                        # Check cache first
                        cached_data = self.cache_repository.get_cached_data(org_name, dimension)

                        if cached_data and not session.get("force_refresh", False):
                            # Cache hit - send dimension_started then immediate complete
                            started_event = self._format_event("dimension_started", {
                                "dimension": dimension,
                                "timestamp": datetime.utcnow().isoformat(),
                                "cached": True
                            })
                            yield started_event

                            # Update session status
                            self.session_manager.update_dimension_status(
                                session_id, dimension, "loading", cached=True
                            )

                            # Enhance cached data with base_score
                            enhanced_data = cached_data["data"].copy()
                            if dimension in dimension_scores:
                                enhanced_data["base_score"] = dimension_scores[dimension]
                                logger.info(f"[SSE] ✅ Added base_score={dimension_scores[dimension]:.2f} to cached data for '{dimension}'")
                            else:
                                logger.warning(f"[SSE] ❌ Dimension '{dimension}' not found in dimension_scores! Available: {list(dimension_scores.keys())}")
                                enhanced_data["base_score"] = 0.0

                            # Send completion immediately with enhanced cached data
                            complete_event = self._format_event("dimension_complete", {
                                "dimension": dimension,
                                "cached": True,
                                "data": enhanced_data,
                                "version": cached_data["version"],
                                "timestamp": datetime.utcnow().isoformat()
                            })
                            yield complete_event

                            # Update session status
                            self.session_manager.update_dimension_status(
                                session_id, dimension, "completed", cached=True
                            )

                            completed_count += 1

                        else:
                            # Cache miss - submit for async analysis
                            started_event = self._format_event("dimension_started", {
                                "dimension": dimension,
                                "timestamp": datetime.utcnow().isoformat(),
                                "cached": False
                            })
                            yield started_event

                            # Update session status
                            self.session_manager.update_dimension_status(
                                session_id, dimension, "loading", cached=False
                            )

                            # Create progress queue for this dimension
                            progress_q = queue.Queue()

                            # Submit analysis task (using real orchestrator)
                            future = executor.submit(
                                self._analyze_dimension,
                                org_name,
                                dimension,
                                session_id,
                                sheet_data,
                                analysis_function,
                                progress_q  # NEW: Pass progress queue
                            )
                            future_to_dimension[future] = (dimension, progress_q)

                    # Process async analyses as they complete
                    last_heartbeat = time.time()
                    pending_futures = set(future_to_dimension.keys())

                    while pending_futures:
                        # Check for progress events from all dimensions
                        for future, (dimension, progress_q) in list(future_to_dimension.items()):
                            # Drain progress queue and send events
                            while not progress_q.empty():
                                try:
                                    progress_data = progress_q.get_nowait()
                                    progress_event = self._format_event("dimension_progress", {
                                        "dimension": progress_data["dimension"],
                                        "step": progress_data["step"],
                                        "message": progress_data["data"].get("message", ""),
                                        "timestamp": progress_data["timestamp"]
                                    })
                                    yield progress_event
                                except queue.Empty:
                                    break

                        # Check for completed futures
                        done_futures = {f for f in pending_futures if f.done()}

                        for future in done_futures:
                            dimension, progress_q = future_to_dimension[future]

                            try:
                                # Get analysis result
                                result = future.result(timeout=0.1)

                                # Send completion event
                                complete_event = self._format_event("dimension_complete", {
                                    "dimension": dimension,
                                    "cached": False,
                                    "data": result["data"],
                                    "version": result.get("version", 1),
                                    "timestamp": datetime.utcnow().isoformat()
                                })
                                yield complete_event

                                # Update session status
                                self.session_manager.update_dimension_status(
                                    session_id, dimension, "completed", cached=False
                                )

                                completed_count += 1

                            except Exception as e:
                                # Send error event
                                error_event = self._format_event("dimension_error", {
                                    "dimension": dimension,
                                    "error": str(e),
                                    "timestamp": datetime.utcnow().isoformat()
                                })
                                yield error_event

                                # Update session status with error
                                self.session_manager.update_dimension_status(
                                    session_id, dimension, "error", error_message=str(e)
                                )

                                failed_count += 1

                                print(f"[SSE] Error analyzing {dimension}: {e}")
                                traceback.print_exc()

                            pending_futures.remove(future)

                        # Send heartbeat if needed
                        if time.time() - last_heartbeat > self.HEARTBEAT_INTERVAL:
                            heartbeat_event = self._format_event("heartbeat", {
                                "timestamp": datetime.utcnow().isoformat()
                            })
                            yield heartbeat_event
                            last_heartbeat = time.time()

                        # Small sleep to prevent busy waiting
                        if pending_futures:
                            time.sleep(0.1)

                # Generate organization summary if all dimensions succeeded
                if completed_count == total_dimensions and failed_count == 0:
                    try:
                        print(f"[SSE] Generating organization summary for {org_name}...")

                        # Send progress event
                        org_summary_start_event = self._format_event("organization_summary_started", {
                            "timestamp": datetime.utcnow().isoformat()
                        })
                        yield org_summary_start_event

                        # Collect all dimension results for summary generation
                        dimension_results = {}
                        for dimension in dimensions:
                            cached_data = self.cache_repository.get_cached_data(org_name, dimension)
                            if cached_data and "data" in cached_data:
                                # Extract the nested data dict which contains summary, themes, score_modifiers
                                dim_data = cached_data["data"]

                                # Validate structure before passing to AI analyzer
                                if isinstance(dim_data, dict):
                                    dimension_results[dimension] = {
                                        "summary": dim_data.get("summary", ""),
                                        "themes": dim_data.get("themes", []),
                                        "score_modifiers": dim_data.get("score_modifiers", [])
                                    }
                                    print(f"[SSE] Collected {dimension} data for org summary: "
                                          f"summary={len(str(dim_data.get('summary', '')))} chars, "
                                          f"themes={len(dim_data.get('themes', []))}, "
                                          f"modifiers={len(dim_data.get('score_modifiers', []))}")
                                else:
                                    print(f"[SSE] WARNING: Invalid data structure for {dimension}: {type(dim_data)}")
                            else:
                                print(f"[SSE] WARNING: No cached data found for {dimension}")

                        # FIX ISSUE 2: Check if Summary is already cached before regenerating
                        # Use get_main_summary() method which directly returns the cached summary text
                        cached_summary = self.cache_repository.get_main_summary(org_name)

                        org_summary = None

                        if cached_summary:
                            # Use cached Summary instead of regenerating
                            print(f"[SSE] Using cached organization summary for {org_name} ({len(cached_summary)} chars)")
                            org_summary = cached_summary
                        else:
                            # Generate organization summary using AI analyzer only if not cached
                            print(f"[SSE] No cached summary found, generating new organization summary for {org_name}...")
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)

                            try:
                                from src.analytics.ai_analyzer import AIAnalyzer
                                ai_analyzer = AIAnalyzer()

                                org_summary = loop.run_until_complete(
                                    ai_analyzer.generate_organization_summary_async(
                                        org_name=org_name,
                                        dimension_summaries=dimension_results
                                    )
                                )

                                # Save organization summary to database
                                self.cache_repository.save_main_summary(org_name, org_summary)

                                print(f"[SSE] Organization summary generated and saved for {org_name}: {len(org_summary)} chars")

                            finally:
                                loop.close()

                        # Send completion event with summary (whether cached or newly generated)
                        if org_summary:
                            org_summary_complete_event = self._format_event("organization_summary_complete", {
                                "summary": org_summary,
                                "timestamp": datetime.utcnow().isoformat(),
                                "cached": cached_summary is not None
                            })
                            yield org_summary_complete_event

                    except Exception as e:
                        print(f"[SSE] Error generating organization summary: {e}")
                        traceback.print_exc()

                        # Send error event but continue
                        org_summary_error_event = self._format_event("organization_summary_error", {
                            "error": str(e),
                            "timestamp": datetime.utcnow().isoformat()
                        })
                        yield org_summary_error_event

                # Send session completion event
                duration = time.time() - start_time
                complete_event = self._format_event("session_complete", {
                    "session_id": session_id,
                    "dimensions_completed": completed_count,
                    "dimensions_failed": failed_count,
                    "duration_seconds": round(duration, 2),
                    "timestamp": datetime.utcnow().isoformat()
                })
                yield complete_event

                print(f"[SSE] Session {session_id} completed: {completed_count} succeeded, {failed_count} failed ({total_dimensions} total) in {duration:.2f}s")

            except GeneratorExit:
                # Client disconnected
                print(f"[SSE] Client disconnected from session {session_id}")
            except Exception as e:
                # Unexpected error
                print(f"[SSE] Error in event stream: {e}")
                traceback.print_exc()

                error_event = self._format_event("error", {
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                })
                yield error_event

        # Return SSE Response
        return Response(
            event_stream(),
            mimetype="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",  # Disable nginx buffering
                "Connection": "keep-alive"
            }
        )

    def _analyze_dimension(
        self,
        org_name: str,
        dimension: str,
        session_id: str,
        sheet_data: Dict[str, List[Dict[str, Any]]],
        analysis_function: Optional[Callable] = None,
        progress_queue: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Analyze dimension using orchestrator with async AI analysis.

        Coordinates survey data extraction, AI analysis, and cache storage.
        Runs async orchestrator in thread pool executor context.

        THREAD SAFETY: Creates thread-local SQLAlchemy session to prevent
        "concurrent operations are not permitted" errors when multiple
        worker threads access database simultaneously.

        Args:
            org_name: Organization name
            dimension: Dimension to analyze
            session_id: Session ID for tracking
            sheet_data: Complete sheet data from SheetsReader
            analysis_function: Optional custom analysis function (for testing)
            progress_queue: Optional list to append progress events to

        Returns:
            Dictionary with analysis data:
            {
                "data": {
                    "summary": "...",
                    "themes": [...],
                    "score_modifiers": {...}
                },
                "version": 1,
                "progress_events": [...]  # If progress_queue provided
            }
        """
        # Use custom function if provided (for testing)
        if analysis_function:
            return analysis_function(org_name, dimension, session_id, sheet_data)

        # CREATE THREAD-LOCAL REPOSITORY INSTANCE
        # Each worker thread MUST have its own repository instance to prevent
        # concurrent file access issues. Singleton pattern would share the same
        # instance across all threads, causing file locking conflicts.
        from src.repositories.qualitative_cache_file_repository import get_qualitative_cache_file_repository
        thread_local_repo = get_qualitative_cache_file_repository()

        # Create thread-local orchestrator with dedicated repository
        thread_local_orchestrator = DimensionAnalysisOrchestrator(
            cache_repository=thread_local_repo
        )

        # Progress callback to capture events
        def on_progress(dim: str, step: str, data: Dict[str, Any]):
            if progress_queue is not None:
                try:
                    progress_queue.put({
                        "dimension": dim,
                        "step": step,
                        "data": data,
                        "timestamp": datetime.utcnow().isoformat()
                    }, block=False)
                except:
                    # Ignore if queue is full
                    pass

        # Run orchestrator async analysis in thread pool context
        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Run orchestrator analysis
            print(f"[SSE] Starting real AI analysis for {org_name}/{dimension}")

            result = loop.run_until_complete(
                thread_local_orchestrator.analyze_dimension(
                    org_name=org_name,
                    dimension=dimension,
                    sheet_data=sheet_data,
                    force_refresh=False,  # Use cache if available
                    progress_callback=on_progress  # NEW: Pass progress callback
                )
            )

            print(
                f"[SSE] Analysis complete for {org_name}/{dimension} "
                f"(cached={result.get('cached', False)}, "
                f"modifiers={len(result.get('score_modifiers', []))})"
            )

            # CRITICAL FIX: Add base_score to fresh analysis results (not just cached)
            # Load dimension scores to get base_score
            dimension_scores = self._load_dimension_scores(org_name)
            base_score = dimension_scores.get(dimension, 0.0)

            if dimension in dimension_scores:
                logger.info(f"[SSE] ✅ Adding base_score={base_score:.2f} to fresh analysis for '{dimension}'")
            else:
                logger.warning(f"[SSE] ❌ Dimension '{dimension}' not found in dimension_scores! Available: {list(dimension_scores.keys())}, using 0.0")

            # Format result for SSE response with base_score
            return {
                "data": {
                    "summary": result.get("summary", ""),
                    "themes": result.get("themes", []),
                    "score_modifiers": result.get("score_modifiers", []),
                    "base_score": base_score  # Add base_score here too!
                },
                "version": result.get("version", 1)
            }

        finally:
            # Clean up event loop
            loop.close()

    def _load_dimension_scores(self, org_name: str) -> Dict[str, float]:
        """
        Load dimension base scores (weighted_score) for an organization.

        This loads the quantitative scores from the report service to enhance
        dimension data with base_score field. Required for "Single Source of Truth"
        principle - dimension data should include both qualitative AND quantitative info.

        Args:
            org_name: Organization name

        Returns:
            Dictionary mapping dimension names to base scores (weighted_score)
            Returns empty dict if report cannot be generated.
        """
        try:
            from src.services.report_service import get_report_service

            report_service = get_report_service()
            report = report_service.get_organization_report(org_name, skip_ai=True, use_cache=True)

            if not report or 'maturity' not in report or 'variance_analysis' not in report['maturity']:
                logger.warning(f"[SSE] Cannot load dimension scores for {org_name}: report not available")
                return {}

            variance_analysis = report['maturity']['variance_analysis']
            dimension_scores = {}

            logger.info(f"[SSE] Loading dimension scores for {org_name}. Available dimensions: {list(variance_analysis.keys())}")

            for dimension, analysis in variance_analysis.items():
                # weighted_score is the base score before modifiers
                base_score = analysis.get('weighted_score', 0.0)
                dimension_scores[dimension] = base_score
                logger.info(f"[SSE] Loaded base_score for '{dimension}': {base_score:.2f}")

            logger.info(f"[SSE] Total dimension_scores loaded: {len(dimension_scores)}")
            return dimension_scores

        except Exception as e:
            logger.error(f"[SSE] Error loading dimension scores for {org_name}: {e}", exc_info=True)
            return {}

    def _format_event(self, event_type: str, data: Dict[str, Any]) -> str:
        """
        Format data as SSE event.

        SSE Format:
            event: <event_type>
            data: <json_data>
            <blank line>

        Args:
            event_type: Event type name
            data: Event data dictionary

        Returns:
            Formatted SSE message string
        """
        return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"
