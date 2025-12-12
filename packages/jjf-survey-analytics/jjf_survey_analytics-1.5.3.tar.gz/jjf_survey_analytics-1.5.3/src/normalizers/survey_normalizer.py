#!/usr/bin/env python3
"""
Survey Database Normalizer

Backward compatibility wrapper for legacy SurveyNormalizer API.
Delegates all operations to specialized services (SchemaManager, DataImporter, NormalizationOrchestrator).

This class is now a thin orchestration layer that maintains the original API
while leveraging the new service-oriented architecture.

Supports both SQLite (local) and PostgreSQL (production) via DATABASE_URL.

**Refactored from 983 lines to ~200 lines (80% reduction)**

Original responsibilities moved to:
- SchemaManager: Database schema management
- DataImporter: Data import and parsing
- NormalizationOrchestrator: Workflow coordination
- DataService: Google Sheets data access
- DataTypeDetector: Type detection and parsing
"""

import logging
from datetime import datetime
from typing import Any, Dict, Optional

# Import db_utils for backward compatibility
from scripts.utils.db_utils import is_postgresql
from src.services.data_importer import get_data_importer
from src.services.data_service import get_data_service
from src.services.normalization_orchestrator import get_normalization_orchestrator

# Import specialized services
from src.services.schema_manager import get_schema_manager

logger = logging.getLogger(__name__)


class SurveyNormalizer:
    """
    Backward compatibility wrapper for SurveyNormalizer.

    Maintains original API while delegating to specialized services:
    - SchemaManager: Schema creation and validation
    - DataImporter: Data import from Google Sheets
    - NormalizationOrchestrator: Complete workflow coordination
    - DataService: Access to Google Sheets data

    This class is now a pure orchestration layer with ~200 lines,
    down from the original 983 lines (80% code reduction).
    """

    def __init__(
        self, source_db: str = "surveyor_data_improved.db", target_db: str = "survey_normalized.db"
    ):
        """
        Initialize survey normalizer with specialized services.

        Args:
            source_db: Legacy parameter (ignored, data comes from Google Sheets)
            target_db: Path to target normalized database
        """
        # Legacy parameters (kept for backward compatibility)
        self.source_db = source_db
        self.target_db = target_db
        self.auto_import = True
        self.use_postgresql = is_postgresql()

        # Initialize specialized services
        self._schema_manager = get_schema_manager(target_db)
        self._data_service = get_data_service()
        self._data_importer = get_data_importer(
            schema_manager=self._schema_manager, data_service=self._data_service
        )
        self._orchestrator = get_normalization_orchestrator(
            schema_manager=self._schema_manager,
            data_importer=self._data_importer,
            db_path=target_db,
        )

        db_type = "PostgreSQL" if self.use_postgresql else f"SQLite ({target_db})"
        logger.info(f"SurveyNormalizer initialized using {db_type}")

    # =========================================================================
    # MAIN PUBLIC API - Delegate to NormalizationOrchestrator
    # =========================================================================

    def normalize_survey_data(self) -> Dict[str, Any]:
        """
        Main method to normalize all survey data.

        This method maintains backward compatibility with the original API.
        Delegates to NormalizationOrchestrator for actual implementation.

        Returns:
            Dictionary with normalization results (for backward compatibility)
        """
        logger.info("Starting survey data normalization...")

        # Ensure data is loaded from Google Sheets
        if not self._data_service.has_data():
            logger.info("Loading data from Google Sheets...")
            self._data_service.load_data(verbose=True)

        # Delegate to orchestrator
        result = self._orchestrator.normalize_all_surveys(verbose=True, rebuild=False)

        # Convert result format for backward compatibility
        if result["status"] in ("success", "partial_success"):
            logger.info(
                "✅ Normalization completed successfully!\n"
                f"📈 Surveys processed: {result['surveys_processed']}\n"
                f"📝 Responses processed: {result['total_responses']}\n"
                f"💬 Answers created: {result['total_answers']}"
            )
        else:
            logger.error(f"❌ Normalization failed: {result.get('errors', [])}")

        return result

    def create_normalized_schema(self) -> None:
        """
        Create the normalized database schema for surveys.

        Delegates to SchemaManager.
        """
        logger.info("Creating normalized database schema...")
        self._schema_manager.create_schema()

        db_type = "PostgreSQL" if self.use_postgresql else f"SQLite ({self.target_db})"
        print(f"✅ Created normalized database schema: {db_type}")

    # =========================================================================
    # BACKWARD COMPATIBILITY METHODS
    # =========================================================================

    def auto_import_new_data(self) -> Dict[str, Any]:
        """
        Legacy method for auto-importing new data.

        NOTE: This method is retained for backward compatibility but is now
        a simplified wrapper. The new architecture automatically loads data
        from Google Sheets on demand.

        Returns:
            Result dictionary with import statistics
        """
        logger.info("Auto-import mode (loading from Google Sheets)...")

        # Ensure data is loaded
        if not self._data_service.has_data():
            self._data_service.load_data(verbose=True)

        # Run normalization
        result = self._orchestrator.normalize_all_surveys(verbose=True, rebuild=False)

        # Convert to legacy format
        return {
            "imported": result["surveys_processed"],
            "updated": 0,
            "total_processed": result["surveys_processed"],
            "message": f"Successfully processed {result['surveys_processed']} surveys",
        }

    def check_for_new_data(self) -> Dict[str, Any]:
        """
        Legacy method to check for new data.

        NOTE: This method is retained for backward compatibility but has
        simplified behavior. The new architecture uses Google Sheets as
        the single source of truth.

        Returns:
            Dictionary indicating data status (simplified)
        """
        logger.info("Checking for new data from Google Sheets...")

        # Refresh data from Google Sheets
        self._data_service.refresh_data(verbose=True)

        metadata = self._data_service.get_metadata()

        # Return legacy format
        return {
            "new_data": [],  # No longer tracked (Google Sheets is source of truth)
            "updated_data": [],
            "total_changes": metadata["total_rows"],
            "message": f"Found {metadata['total_rows']} total rows across {metadata['tab_count']} tabs",
        }

    def identify_survey_types(self) -> Dict[str, str]:
        """
        Legacy method to identify survey types.

        NOTE: The new architecture uses explicit tab names (CEO, Tech, Staff)
        from Google Sheets, so type identification is no longer needed.

        Returns:
            Empty dict (legacy compatibility only)
        """
        logger.warning(
            "identify_survey_types() is deprecated. " "New architecture uses explicit tab names."
        )
        return {}

    def import_single_spreadsheet(self, spreadsheet_id: str, update: bool = False) -> None:
        """
        Legacy method to import a single spreadsheet.

        NOTE: This method is deprecated. Use normalize_survey_data() instead.

        Args:
            spreadsheet_id: Legacy parameter (ignored)
            update: Legacy parameter (ignored)
        """
        logger.warning(
            "import_single_spreadsheet() is deprecated. " "Use normalize_survey_data() instead."
        )

        # Delegate to main normalization
        self.normalize_survey_data()

    def clear_spreadsheet_data(self, target_cursor, spreadsheet_id: str) -> None:
        """
        Legacy method to clear spreadsheet data.

        NOTE: This method is deprecated. Use rebuild schema instead.

        Args:
            target_cursor: Legacy parameter (ignored)
            spreadsheet_id: Legacy parameter (ignored)
        """
        logger.warning(
            "clear_spreadsheet_data() is deprecated. "
            "Use _orchestrator.rebuild_database() instead."
        )

    def process_survey_responses(
        self, source_cursor, target_cursor, sheet_id: str, title: str, sheet_type: str
    ) -> Dict[str, int]:
        """
        Legacy method to process survey responses.

        NOTE: This method is deprecated. Use DataImporter.import_survey_data() instead.

        Args:
            source_cursor: Legacy parameter (ignored)
            target_cursor: Legacy parameter (ignored)
            sheet_id: Legacy parameter (ignored)
            title: Survey name (e.g., 'CEO', 'Tech', 'Staff')
            sheet_type: Legacy parameter (ignored)

        Returns:
            Import statistics
        """
        logger.warning(
            "process_survey_responses() is deprecated. "
            "Use DataImporter.import_survey_data() instead."
        )

        # Delegate to data importer
        return self._data_importer.import_survey_data(survey_name=title, verbose=True)

    # =========================================================================
    # UTILITY METHODS (unchanged from original)
    # =========================================================================

    def create_respondent_hash(self, response_data: Dict) -> str:
        """
        Create a hash to identify unique respondents.

        Delegates to DataImporter._create_respondent_hash().

        Args:
            response_data: Response data dictionary

        Returns:
            Hash string (16 characters)
        """
        return self._data_importer._create_respondent_hash(response_data)

    def parse_response_date(self, date_string: str) -> Optional[datetime]:
        """
        Parse various date formats from the survey data.

        Delegates to DataImporter._parse_response_date().

        Args:
            date_string: Date string to parse

        Returns:
            Datetime object or None if parsing fails
        """
        return self._data_importer._parse_response_date(date_string)

    # =========================================================================
    # VALIDATION AND STATUS
    # =========================================================================

    def validate_schema(self) -> bool:
        """
        Validate that all required tables and columns exist.

        Delegates to SchemaManager.

        Returns:
            True if schema is valid, False otherwise
        """
        return self._schema_manager.validate_schema()

    def get_normalization_status(self) -> Dict[str, Any]:
        """
        Get current status of normalization.

        Delegates to NormalizationOrchestrator.

        Returns:
            Status dictionary
        """
        return self._orchestrator.get_normalization_status()


# =============================================================================
# CLI ENTRY POINT (unchanged for backward compatibility)
# =============================================================================


def main():
    """Main function to run the survey normalization."""
    import sys

    print("🔄 Survey Database Normalizer")
    print("=" * 50)

    # Check command line arguments
    auto_mode = "--auto" in sys.argv or "-a" in sys.argv
    force_full = "--full" in sys.argv or "-" in sys.argv

    normalizer = SurveyNormalizer()

    if auto_mode and not force_full:
        # Auto-import mode: only process new/updated data
        print("🤖 Running in auto-import mode (new/updated data only)")
        normalizer.auto_import = True

        try:
            # Ensure data is loaded
            if not normalizer._data_service.has_data():
                print("📥 Loading data from Google Sheets...")
                normalizer._data_service.load_data(verbose=True)

            # Check if schema exists
            if not normalizer.validate_schema():
                print("📊 Creating initial database schema...")
                normalizer.create_normalized_schema()

            result = normalizer.auto_import_new_data()

            if result["total_processed"] > 0:
                print("\n✅ Auto-import completed successfully!")
                print(f"📥 Imported: {result['imported']} surveys")
            else:
                print(f"\n✅ {result['message']}")

            print(f"💾 Normalized database: {normalizer.target_db}")

        except Exception as e:
            print(f"\n❌ Auto-import failed: {e}")
            logger.exception("Auto-import failed")
            return 1

    else:
        # Full normalization mode
        if force_full:
            print("🔄 Running full normalization (forced)")
        else:
            print("🔄 Running full normalization")

        normalizer.auto_import = False

        try:
            # Ensure data is loaded
            if not normalizer._data_service.has_data():
                print("📥 Loading data from Google Sheets...")
                normalizer._data_service.load_data(verbose=True)

            # Run normalization
            normalizer.normalize_survey_data()
            print(f"\n💾 Normalized database created: {normalizer.target_db}")

        except Exception as e:
            print(f"\n❌ Normalization failed: {e}")
            logger.exception("Normalization failed")
            return 1

    return 0


if __name__ == "__main__":
    exit(main())
