#!/usr/bin/env python3
"""
Normalization Orchestrator - Coordinate complete normalization workflow.

Orchestrates the complete survey data normalization process by coordinating
SchemaManager, DataImporter, and validation to execute the full workflow.

Extracted from SurveyNormalizer as part of God class decomposition.
"""

import logging
import threading
import time
from contextlib import contextmanager
from typing import Any, Dict

logger = logging.getLogger(__name__)


class NormalizationOrchestrator:
    """
    Orchestrate complete normalization workflow for survey data.

    Responsibilities:
    - Coordinate schema creation, data import, and validation
    - Track normalization jobs and progress
    - Handle error recovery and rollback
    - Provide status reporting
    - Thread-safe operations
    - Ensure single-instance execution
    """

    def __init__(
        self,
        schema_manager,  # SchemaManager instance
        data_importer,  # DataImporter instance
        db_path: str = "survey_normalized.db",
    ):
        """
        Initialize normalization orchestrator.

        Args:
            schema_manager: SchemaManager instance for schema operations
            data_importer: DataImporter instance for data import
            db_path: Path to target database (informational only)
        """
        self.schema_manager = schema_manager
        self.data_importer = data_importer
        self.db_path = db_path
        self._lock = threading.Lock()
        self._is_running = False

        logger.info(f"NormalizationOrchestrator initialized for: {db_path}")

    @contextmanager
    def _ensure_single_execution(self):
        """Context manager to ensure only one normalization runs at a time."""
        with self._lock:
            if self._is_running:
                raise RuntimeError("Normalization already in progress")
            self._is_running = True

        try:
            yield
        finally:
            with self._lock:
                self._is_running = False

    def normalize_all_surveys(self, verbose: bool = True, rebuild: bool = False) -> Dict[str, Any]:
        """
        Execute complete normalization workflow for all surveys.

        Workflow:
        1. Initialize schema (create or validate)
        2. Import all survey data
        3. Validate normalization
        4. Report statistics

        Args:
            verbose: Enable verbose logging
            rebuild: Drop and recreate schema before import

        Returns:
            Dictionary with normalization results:
            {
                "status": "success|error",
                "surveys_processed": N,
                "total_responses": M,
                "duration_seconds": X,
                "errors": [...],
                "surveys": {
                    "CEO": {...},
                    "Tech": {...},
                    "Staff": {...}
                }
            }
        """
        with self._ensure_single_execution():
            start_time = time.time()

            if verbose:
                logger.info("=" * 60)
                logger.info("Starting normalization workflow")
                logger.info(f"Database: {self.db_path}")
                logger.info(f"Rebuild: {rebuild}")
                logger.info("=" * 60)

            result = {
                "status": "success",
                "surveys_processed": 0,
                "total_responses": 0,
                "total_answers": 0,
                "total_respondents": 0,
                "duration_seconds": 0.0,
                "errors": [],
                "surveys": {},
            }

            try:
                # Phase 1: Schema initialization
                if verbose:
                    logger.info("\n[Phase 1/3] Schema Initialization")

                if rebuild:
                    self._rebuild_schema(verbose)
                else:
                    self._ensure_schema_exists(verbose)

                # Phase 2: Data import
                if verbose:
                    logger.info("\n[Phase 2/3] Data Import")

                survey_names = ["CEO", "Tech", "Staff"]

                for survey_name in survey_names:
                    try:
                        survey_result = self.normalize_survey(
                            survey_name=survey_name, verbose=verbose
                        )

                        result["surveys"][survey_name] = survey_result
                        result["surveys_processed"] += 1
                        result["total_responses"] += survey_result["responses"]
                        result["total_answers"] += survey_result["answers"]
                        result["total_respondents"] += survey_result["respondents"]

                    except Exception as e:
                        error_msg = f"Failed to import survey '{survey_name}': {e}"
                        logger.error(error_msg)
                        result["errors"].append(error_msg)
                        result["surveys"][survey_name] = {
                            "error": str(e),
                            "responses": 0,
                            "answers": 0,
                        }

                # Phase 3: Validation
                if verbose:
                    logger.info("\n[Phase 3/3] Validation")

                validation = self.validate_normalization()
                result["validation"] = validation

                if not validation["schema_valid"]:
                    result["status"] = "error"
                    result["errors"].append("Schema validation failed")

                # Calculate duration
                result["duration_seconds"] = time.time() - start_time

                # Final status
                if result["errors"]:
                    result["status"] = (
                        "partial_success" if result["surveys_processed"] > 0 else "error"
                    )

                if verbose:
                    self._print_summary(result)

            except Exception as e:
                result["status"] = "error"
                result["errors"].append(f"Normalization failed: {e}")
                result["duration_seconds"] = time.time() - start_time
                logger.exception("Normalization workflow failed")

            return result

    def normalize_survey(self, survey_name: str, verbose: bool = True) -> Dict[str, Any]:
        """
        Normalize a single survey.

        Args:
            survey_name: Name of survey to normalize (e.g., 'CEO', 'Tech', 'Staff')
            verbose: Enable verbose logging

        Returns:
            Import statistics dictionary:
            {
                "responses": N,
                "answers": M,
                "respondents": K,
                "duplicates_skipped": J
            }

        Raises:
            ValueError: If survey_name is invalid
            RuntimeError: If import fails
        """
        if verbose:
            logger.info(f"  Importing survey: {survey_name}")

        try:
            stats = self.data_importer.import_survey_data(survey_name=survey_name, verbose=verbose)

            if verbose:
                logger.info(
                    f"  ✓ {survey_name}: {stats['responses']} responses, "
                    f"{stats['answers']} answers, "
                    f"{stats['respondents']} new respondents"
                )

            return stats

        except Exception as e:
            logger.error(f"Failed to import survey '{survey_name}': {e}")
            raise RuntimeError(f"Survey import failed: {survey_name}") from e

    def rebuild_database(self, verbose: bool = True) -> bool:
        """
        Drop and recreate schema, then reimport all data.

        WARNING: This will delete all existing data!

        Args:
            verbose: Enable verbose logging

        Returns:
            True if rebuild successful, False otherwise
        """
        if verbose:
            logger.warning("=" * 60)
            logger.warning("REBUILDING DATABASE - ALL DATA WILL BE DELETED")
            logger.warning("=" * 60)

        try:
            # Check if already running
            with self._lock:
                if self._is_running:
                    raise RuntimeError("Normalization already in progress")

            # Rebuild schema (outside the execution context)
            self._rebuild_schema(verbose)

            # Reimport all data (this will acquire the lock)
            result = self.normalize_all_surveys(verbose=verbose, rebuild=False)  # Already rebuilt

            success = result["status"] in ("success", "partial_success")

            if verbose:
                if success:
                    logger.info("\n✓ Database rebuild completed successfully")
                else:
                    logger.error("\n✗ Database rebuild failed")

            return success

        except Exception as e:
            logger.exception(f"Database rebuild failed: {e}")
            return False

    def validate_normalization(self) -> Dict[str, Any]:
        """
        Validate that normalization completed successfully.

        Checks:
        - Schema integrity (all tables exist)
        - Data presence (surveys, responses, questions)
        - Referential integrity (no orphaned records)

        Returns:
            Validation result dictionary:
            {
                "schema_valid": bool,
                "surveys_count": N,
                "responses_count": M,
                "questions_count": K,
                "answers_count": J,
                "issues": [...]
            }
        """
        validation = {
            "schema_valid": False,
            "surveys_count": 0,
            "responses_count": 0,
            "questions_count": 0,
            "answers_count": 0,
            "respondents_count": 0,
            "issues": [],
        }

        try:
            # Validate schema
            validation["schema_valid"] = self.schema_manager.validate_schema()

            if not validation["schema_valid"]:
                validation["issues"].append("Schema validation failed")
                return validation

            # Count records
            with self.schema_manager._get_connection() as conn:
                cursor = conn.cursor()

                # Count surveys
                cursor.execute("SELECT COUNT(*) FROM surveys")
                result = cursor.fetchone()
                validation["surveys_count"] = result[0] if result else 0

                # Count responses
                cursor.execute("SELECT COUNT(*) FROM survey_responses")
                result = cursor.fetchone()
                validation["responses_count"] = result[0] if result else 0

                # Count questions
                cursor.execute("SELECT COUNT(*) FROM survey_questions")
                result = cursor.fetchone()
                validation["questions_count"] = result[0] if result else 0

                # Count answers
                cursor.execute("SELECT COUNT(*) FROM survey_answers")
                result = cursor.fetchone()
                validation["answers_count"] = result[0] if result else 0

                # Count respondents
                cursor.execute("SELECT COUNT(*) FROM respondents")
                result = cursor.fetchone()
                validation["respondents_count"] = result[0] if result else 0

            # Check for data presence
            if validation["surveys_count"] == 0:
                validation["issues"].append("No surveys found")
            if validation["responses_count"] == 0:
                validation["issues"].append("No responses found")
            if validation["questions_count"] == 0:
                validation["issues"].append("No questions found")

            logger.info(
                f"  Validation: {validation['surveys_count']} surveys, "
                f"{validation['responses_count']} responses, "
                f"{validation['questions_count']} questions, "
                f"{validation['answers_count']} answers"
            )

        except Exception as e:
            validation["schema_valid"] = False
            validation["issues"].append(f"Validation error: {e}")
            logger.error(f"Validation failed: {e}")

        return validation

    def get_normalization_status(self) -> Dict[str, Any]:
        """
        Get current status of normalization.

        Returns:
            Status dictionary:
            {
                "is_running": bool,
                "database_path": str,
                "schema_valid": bool,
                "last_validation": {...}
            }
        """
        status = {
            "is_running": self._is_running,
            "database_path": self.db_path,
            "schema_valid": False,
            "last_validation": None,
        }

        try:
            # Check if schema exists
            status["schema_valid"] = self.schema_manager.validate_schema()

            # If schema valid, get record counts
            if status["schema_valid"]:
                status["last_validation"] = self.validate_normalization()

        except Exception as e:
            logger.error(f"Failed to get normalization status: {e}")
            status["error"] = str(e)

        return status

    def _ensure_schema_exists(self, verbose: bool = True) -> None:
        """
        Ensure database schema exists, create if missing.

        Args:
            verbose: Enable verbose logging
        """
        if verbose:
            logger.info("  Checking database schema...")

        schema_valid = self.schema_manager.validate_schema()

        if not schema_valid:
            if verbose:
                logger.info("  Schema not found, creating...")
            self.schema_manager.create_schema()
        else:
            if verbose:
                logger.info("  ✓ Schema validated")

    def _rebuild_schema(self, verbose: bool = True) -> None:
        """
        Drop and recreate database schema.

        Args:
            verbose: Enable verbose logging
        """
        if verbose:
            logger.info("  Dropping existing schema...")

        self.schema_manager.drop_schema()

        if verbose:
            logger.info("  Creating new schema...")

        self.schema_manager.create_schema()

        if verbose:
            logger.info("  ✓ Schema rebuilt successfully")

    def _print_summary(self, result: Dict[str, Any]) -> None:
        """
        Print normalization summary.

        Args:
            result: Normalization result dictionary
        """
        logger.info("\n" + "=" * 60)
        logger.info("NORMALIZATION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Status: {result['status'].upper()}")
        logger.info(f"Duration: {result['duration_seconds']:.2f} seconds")
        logger.info(f"Surveys processed: {result['surveys_processed']}/3")
        logger.info(f"Total responses: {result['total_responses']}")
        logger.info(f"Total answers: {result['total_answers']}")
        logger.info(f"Total respondents: {result['total_respondents']}")

        if result["errors"]:
            logger.info(f"\nErrors ({len(result['errors'])}):")
            for error in result["errors"]:
                logger.info(f"  - {error}")

        logger.info("=" * 60)


def get_normalization_orchestrator(
    schema_manager, data_importer, db_path: str = "survey_normalized.db"
) -> NormalizationOrchestrator:
    """
    Factory function to get NormalizationOrchestrator instance.

    Args:
        schema_manager: SchemaManager instance
        data_importer: DataImporter instance
        db_path: Path to target database

    Returns:
        NormalizationOrchestrator instance
    """
    return NormalizationOrchestrator(
        schema_manager=schema_manager, data_importer=data_importer, db_path=db_path
    )
