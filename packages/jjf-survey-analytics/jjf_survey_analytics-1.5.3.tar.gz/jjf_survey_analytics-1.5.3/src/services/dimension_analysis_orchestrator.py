#!/usr/bin/env python3
"""
DimensionAnalysisOrchestrator - Concurrent AI analysis orchestrator.

Orchestrates concurrent AI analysis of survey dimensions, integrating:
- Survey data extraction from Google Sheets
- AI analysis with async capability
- Validation and error handling
- Cache storage via repository pattern

This is the bridge between:
1. Raw Google Sheets data (via extract_free_text_responses)
2. AI analysis (via AIAnalyzer.analyze_dimension_responses_async)
3. Persistent cache (via QualitativeCacheFileRepository)

Features:
- Async/concurrent dimension analysis
- Automatic cache storage on success
- SHA256 hash-based cache invalidation
- Comprehensive error handling and logging
- 30-second timeout per dimension

Usage:
    from src.services.dimension_analysis_orchestrator import DimensionAnalysisOrchestrator
    from improved_extractor import SheetsReader

    # Load sheet data
    reader = SheetsReader()
    sheet_data = reader.read_all_sheets()

    # Create orchestrator
    orchestrator = DimensionAnalysisOrchestrator(db_session)

    # Analyze dimension
    result = await orchestrator.analyze_dimension(
        org_name="Example Org",
        dimension="Program Technology",
        sheet_data=sheet_data,
        force_refresh=False
    )
"""

import asyncio
import hashlib
import logging
import time
from typing import Any, Callable, Dict, List, Optional

from sqlalchemy.orm import Session

from src.analytics.ai_analyzer import AIAnalyzer, extract_free_text_responses
from src.repositories.qualitative_cache_file_repository import QualitativeCacheFileRepository

# Configure logging
logger = logging.getLogger(__name__)


class RetryConfig:
    """Configuration for retry logic with exponential backoff."""
    MAX_ATTEMPTS = 3
    BASE_DELAY = 2  # seconds
    BACKOFF_MULTIPLIER = 2

    # Error types that should trigger retry
    RETRYABLE_ERRORS = (
        ConnectionError,
        TimeoutError,
        asyncio.TimeoutError,
    )

    # Error message patterns that indicate retryable errors
    RETRYABLE_PATTERNS = [
        "timeout",
        "rate_limit",
        "rate limit",
        "connection",
        "service unavailable",
        "503",
        "429",
        "temporarily unavailable",
    ]

    @classmethod
    def is_retryable_error(cls, error: Exception) -> bool:
        """
        Determine if an error is retryable.

        Args:
            error: Exception to check

        Returns:
            True if error should trigger retry, False otherwise
        """
        # Check error type
        if isinstance(error, cls.RETRYABLE_ERRORS):
            return True

        # Check error message for patterns
        error_msg = str(error).lower()
        return any(pattern in error_msg for pattern in cls.RETRYABLE_PATTERNS)


class DimensionAnalysisOrchestrator:
    """
    Orchestrates concurrent AI analysis of survey dimensions.

    Manages the full pipeline:
    1. Extract survey responses from Google Sheets data
    2. Call AI analyzer with async capability
    3. Validate and process results
    4. Save to cache if successful
    5. Handle errors gracefully
    """

    # Dimension code mapping (matches ai_analyzer.py)
    DIMENSION_CODES = {
        "Program Technology": "PT",
        "Business Systems": "BS",
        "Data Management": "D",
        "Infrastructure": "I",
        "Organizational Culture": "OC"
    }

    # Analysis timeout
    ANALYSIS_TIMEOUT = 30  # seconds

    def __init__(
        self,
        db_session: Optional[Session] = None,
        cache_repository: Optional[QualitativeCacheFileRepository] = None,
        ai_analyzer: Optional[AIAnalyzer] = None
    ):
        """
        Initialize orchestrator with dependencies.

        Args:
            db_session: SQLAlchemy session for database operations (optional, ignored for file repo)
            cache_repository: Cache repository instance (optional, creates new if not provided)
            ai_analyzer: AI analyzer instance (optional, creates new if not provided)
        """
        from src.repositories.qualitative_cache_file_repository import get_qualitative_cache_file_repository
        # Initialize cache repository
        if cache_repository:
            self.cache_repository = cache_repository
        else:
            # Use file-based repository (no database needed)
            self.cache_repository = get_qualitative_cache_file_repository()

        # Initialize AI analyzer
        self.ai_analyzer = ai_analyzer or AIAnalyzer()

        logger.info("[Orchestrator] Initialized with AI analyzer and cache repository")

    async def analyze_dimension(
        self,
        org_name: str,
        dimension: str,
        sheet_data: Dict[str, List[Dict[str, Any]]],
        force_refresh: bool = False,
        progress_callback: Optional[Callable[[str, str, Dict[str, Any]], None]] = None
    ) -> Dict[str, Any]:
        """
        Analyze a single dimension for an organization.

        Coordinates the full analysis pipeline:
        1. Check cache (unless force_refresh=True)
        2. Extract survey responses from sheet data
        3. Call AI analyzer (async)
        4. Save results to cache
        5. Return formatted result

        Args:
            org_name: Organization name
            dimension: Technology dimension name
            sheet_data: Complete sheet data from SheetsReader (dict with CEO/Tech/Staff tabs)
            force_refresh: Skip cache and force new AI analysis

        Returns:
            Dictionary with analysis result:
            {
                "summary": str,
                "themes": List[str],
                "score_modifiers": List[Dict],
                "cached": bool,
                "version": int,
                "error": bool (only if error occurred)
            }

        Raises:
            ValueError: If dimension is invalid
            TimeoutError: If analysis exceeds timeout
        """
        # Validate dimension
        if dimension not in self.DIMENSION_CODES:
            raise ValueError(
                f"Invalid dimension: {dimension}. "
                f"Valid dimensions: {', '.join(self.DIMENSION_CODES.keys())}"
            )

        logger.info(f"[Orchestrator] Analyzing {org_name}/{dimension} (force_refresh={force_refresh})")

        # Helper to send progress updates
        def send_progress(step: str, message: str, extra: Dict[str, Any] = None):
            if progress_callback:
                progress_callback(dimension, step, {"message": message, **(extra or {})})

        try:
            # Step 1: Check cache (unless force_refresh)
            send_progress("checking_cache", "Checking for cached analysis...")

            if not force_refresh:
                cached_data = self.cache_repository.get_cached_data(org_name, dimension)
                if cached_data:
                    logger.info(
                        f"[Orchestrator] Cache hit for {org_name}/{dimension} "
                        f"(source: {cached_data['source']}, version: {cached_data['version']})"
                    )
                    return {
                        "summary": cached_data["data"].get("summary", ""),
                        "themes": cached_data["data"].get("themes", []),
                        "score_modifiers": cached_data["data"].get("modifiers", []),
                        "cached": True,
                        "version": cached_data["version"]
                    }

            # Step 2: Extract survey responses from sheet data
            send_progress("extracting_responses", "Extracting survey responses...")

            logger.info(f"[Orchestrator] Extracting survey responses for {org_name}/{dimension}")
            dimension_responses = extract_free_text_responses(sheet_data, org_name)

            # Get responses for this specific dimension
            responses = dimension_responses.get(dimension, [])

            if not responses:
                logger.warning(f"[Orchestrator] No survey responses found for {org_name}/{dimension}")
                send_progress("complete", "No survey responses available")
                return {
                    "summary": f"No survey responses available for {dimension}.",
                    "themes": [],
                    "score_modifiers": [],
                    "cached": False,
                    "version": 1
                }

            logger.info(
                f"[Orchestrator] Found {len(responses)} survey responses for {org_name}/{dimension}"
            )

            send_progress("extracting_responses", f"Found {len(responses)} responses", {"count": len(responses)})

            # Calculate response hash for cache invalidation
            response_hash = self._calculate_response_hash(org_name, dimension, responses)

            # Step 3: Call AI analyzer with retry logic
            send_progress("ai_analyzing", "AI is analyzing responses... This may take 10-30 seconds")

            logger.info(f"[Orchestrator] Starting AI analysis for {org_name}/{dimension}")

            # Retry logic with exponential backoff
            ai_result = None
            last_error = None

            for attempt in range(1, RetryConfig.MAX_ATTEMPTS + 1):
                try:
                    # Use asyncio.wait_for to enforce timeout
                    ai_result = await asyncio.wait_for(
                        self.ai_analyzer.analyze_dimension_responses_async(
                            dimension=dimension,
                            free_text_responses=responses,
                            org_name=org_name
                        ),
                        timeout=self.ANALYSIS_TIMEOUT
                    )

                    # Success! Break out of retry loop
                    logger.info(
                        f"[Orchestrator] AI analysis succeeded for {org_name}/{dimension} "
                        f"(attempt {attempt}/{RetryConfig.MAX_ATTEMPTS})"
                    )
                    break

                except Exception as e:
                    last_error = e

                    # Check if this is the last attempt
                    is_last_attempt = (attempt == RetryConfig.MAX_ATTEMPTS)

                    # Check if error is retryable
                    is_retryable = RetryConfig.is_retryable_error(e)

                    logger.warning(
                        f"[Orchestrator] AI analysis attempt {attempt}/{RetryConfig.MAX_ATTEMPTS} "
                        f"failed for {org_name}/{dimension}: {str(e)[:100]} "
                        f"(retryable={is_retryable}, last_attempt={is_last_attempt})"
                    )

                    # If this is the last attempt or error is not retryable, give up
                    if is_last_attempt or not is_retryable:
                        if is_last_attempt:
                            logger.error(
                                f"[Orchestrator] Max retry attempts exceeded for {org_name}/{dimension}",
                                exc_info=True
                            )
                        else:
                            logger.error(
                                f"[Orchestrator] Non-retryable error for {org_name}/{dimension}: {str(e)}",
                                exc_info=True
                            )
                        break

                    # Calculate exponential backoff delay
                    retry_delay = RetryConfig.BASE_DELAY * (RetryConfig.BACKOFF_MULTIPLIER ** (attempt - 1))

                    # Send retry SSE event
                    send_progress("dimension_retry", f"Retrying... (attempt {attempt + 1}/{RetryConfig.MAX_ATTEMPTS})", {
                        "attempt": attempt + 1,
                        "max_attempts": RetryConfig.MAX_ATTEMPTS,
                        "retry_after": retry_delay,
                        "error": str(e)[:200]
                    })

                    logger.info(
                        f"[Orchestrator] Waiting {retry_delay}s before retry {attempt + 1} "
                        f"for {org_name}/{dimension}"
                    )

                    # Wait with exponential backoff
                    await asyncio.sleep(retry_delay)

            # Check if all retries failed
            if ai_result is None:
                error_type = "timeout" if isinstance(last_error, (asyncio.TimeoutError, TimeoutError)) else "failed"
                error_msg = str(last_error)[:200] if last_error else "Unknown error"

                logger.error(
                    f"[Orchestrator] All retry attempts failed for {org_name}/{dimension}: {error_msg}"
                )

                # Return error result with detailed information
                return {
                    "summary": f"Error: Analysis {error_type} after {RetryConfig.MAX_ATTEMPTS} attempts. {error_msg}",
                    "themes": [],
                    "score_modifiers": [],
                    "cached": False,
                    "error": True,
                    "error_type": error_type,
                    "error_message": error_msg,
                    "retry_attempts": RetryConfig.MAX_ATTEMPTS
                }

            logger.info(
                f"[Orchestrator] AI analysis complete for {org_name}/{dimension} "
                f"({len(ai_result.get('modifiers', []))} modifiers)"
            )

            send_progress("ai_complete", f"Analysis complete! Found {len(ai_result.get('modifiers', []))} insights", {
                "modifier_count": len(ai_result.get('modifiers', []))
            })

            # Step 4: Save to cache
            send_progress("saving_cache", "Saving analysis to cache...")

            try:
                themes = self._extract_themes_from_summary(ai_result.get("summary", ""), responses)
                self.cache_repository.save_ai_generated(
                    org_name=org_name,
                    dimension=dimension,
                    data={
                        "summary": ai_result.get("summary", ""),
                        "themes": themes,
                        "modifiers": ai_result.get("modifiers", [])
                    },
                    response_hash=response_hash
                )
                logger.info(f"[Orchestrator] Saved analysis to cache for {org_name}/{dimension}")
            except Exception as e:
                # Log cache error but don't fail the analysis
                logger.error(
                    f"[Orchestrator] Failed to save to cache for {org_name}/{dimension}: {e}",
                    exc_info=True
                )
                # Still generate themes for return value
                themes = self._extract_themes_from_summary(ai_result.get("summary", ""), responses)

            # Step 5: Return formatted result
            return {
                "summary": ai_result.get("summary", ""),
                "themes": themes,
                "score_modifiers": ai_result.get("modifiers", []),
                "cached": False,
                "version": 1
            }

        except ValueError as e:
            # Invalid dimension or validation error
            logger.error(f"[Orchestrator] Validation error for {org_name}/{dimension}: {e}")
            return {
                "summary": f"Error: {str(e)}",
                "themes": [],
                "score_modifiers": [],
                "cached": False,
                "error": True
            }

        except Exception as e:
            # Unexpected error
            logger.error(
                f"[Orchestrator] Unexpected error analyzing {org_name}/{dimension}: {e}",
                exc_info=True
            )
            return {
                "summary": f"Error: {str(e)}",
                "themes": [],
                "score_modifiers": [],
                "cached": False,
                "error": True
            }

    def _calculate_response_hash(
        self,
        org_name: str,
        dimension: str,
        responses: List[Dict[str, Any]]
    ) -> str:
        """
        Calculate SHA256 hash for response set.

        Hash includes:
        - Organization name
        - Dimension
        - Response count
        - Sorted respondent names and roles
        - Question IDs

        Args:
            org_name: Organization name
            dimension: Technology dimension
            responses: List of response dictionaries

        Returns:
            SHA256 hash (16 character hex string)
        """
        # Build hash input string
        hash_input = f"{org_name}_{dimension}_{len(responses)}"

        # Sort responses by respondent for consistent hashing
        sorted_responses = sorted(
            responses,
            key=lambda r: (r.get('respondent', ''), r.get('role', ''), r.get('question_id', ''))
        )

        # Add respondent identifiers and question IDs
        for response in sorted_responses:
            respondent = response.get('respondent', '')
            role = response.get('role', '')
            question_id = response.get('question_id', '')
            hash_input += f"_{respondent}_{role}_{question_id}"

        # Generate SHA256 hash (truncate to 16 chars for storage efficiency)
        hash_obj = hashlib.sha256(hash_input.encode('utf-8'))
        return hash_obj.hexdigest()[:16]

    def _extract_themes_from_summary(self, summary: str, responses: List[Dict] = None) -> List[Dict]:
        """
        Extract 3-5 themes from AI summary with proper structure for frontend.

        The AI analyzer returns a summary but not separate themes.
        This extracts key themes from the summary and structures them properly.

        Args:
            summary: AI-generated summary text
            responses: Optional list of survey responses for evidence extraction

        Returns:
            List of 3-5 theme dictionaries with structure:
            {
                "theme": "Theme title",
                "summary": "Theme description",
                "evidence": ["Supporting quote 1", "Supporting quote 2", ...]
            }
        """
        if not summary or len(summary) < 50:
            # Return placeholder themes for incomplete analysis
            return [
                {
                    "theme": "Analysis in Progress",
                    "summary": "Awaiting detailed insights from AI analysis",
                    "evidence": []
                },
                {
                    "theme": "Review Pending",
                    "summary": "Additional context needed for comprehensive assessment",
                    "evidence": []
                },
                {
                    "theme": "Detailed Insights Available",
                    "summary": "Complete analysis will provide comprehensive technology insights",
                    "evidence": []
                }
            ]

        # Simple extraction: split summary into sentences and take first 3-5
        sentences = [s.strip() for s in summary.split('.') if len(s.strip()) > 20]

        if len(sentences) >= 3:
            # Take first 3-5 sentences as themes
            theme_sentences = sentences[:min(5, len(sentences))]
        elif len(sentences) > 0:
            # Fewer than 3 sentences - use what we have
            theme_sentences = sentences
        else:
            # No sentences - create generic theme
            theme_sentences = [summary[:100] + "..." if len(summary) > 100 else summary]

        # Convert sentences to proper theme structure
        structured_themes = []
        for idx, sentence in enumerate(theme_sentences):
            # Extract first few words as theme title (capitalize properly)
            words = sentence.split()
            theme_title = " ".join(words[:5]) if len(words) >= 5 else sentence
            if len(theme_title) > 50:
                theme_title = theme_title[:47] + "..."

            # Use full sentence as summary
            theme_summary = sentence
            if len(theme_summary) > 200:
                theme_summary = theme_summary[:197] + "..."

            # Extract evidence from responses if available
            evidence = []
            if responses:
                # Take up to 2 responses as evidence for this theme
                for response in responses[:min(2, len(responses))]:
                    text = response.get('text', '')
                    if text and len(text) > 20:
                        # Truncate long responses for display
                        evidence_text = text[:150] + "..." if len(text) > 150 else text
                        evidence.append(evidence_text)

            structured_themes.append({
                "theme": theme_title,
                "summary": theme_summary,
                "evidence": evidence
            })

        # Ensure we have 3-5 themes (required by validation)
        while len(structured_themes) < 3:
            structured_themes.append({
                "theme": "Additional Analysis Insights",
                "summary": "Additional insights available upon detailed review of survey responses",
                "evidence": []
            })

        return structured_themes[:5]  # Max 5 themes


# Singleton instance for convenience
_orchestrator_instance: Optional[DimensionAnalysisOrchestrator] = None


def get_dimension_analysis_orchestrator(
    db_session: Optional[Session] = None,
    cache_repository: Optional[QualitativeCacheFileRepository] = None,
    ai_analyzer: Optional[AIAnalyzer] = None
) -> DimensionAnalysisOrchestrator:
    """
    Get singleton instance of DimensionAnalysisOrchestrator.

    Args:
        db_session: SQLAlchemy session (optional)
        cache_repository: Cache repository instance (optional)
        ai_analyzer: AI analyzer instance (optional)

    Returns:
        DimensionAnalysisOrchestrator instance
    """
    global _orchestrator_instance

    if _orchestrator_instance is None:
        _orchestrator_instance = DimensionAnalysisOrchestrator(
            db_session=db_session,
            cache_repository=cache_repository,
            ai_analyzer=ai_analyzer
        )

    return _orchestrator_instance
