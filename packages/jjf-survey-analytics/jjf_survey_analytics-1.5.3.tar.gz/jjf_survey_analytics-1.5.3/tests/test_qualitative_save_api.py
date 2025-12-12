#!/usr/bin/env python3
"""
Test suite for qualitative save/load API endpoints.

Tests:
1. POST /api/qualitative/save/<org_name> - Save edited data
2. GET /api/qualitative/main-summary/<org_name> - Load main summary
3. Integration with QualitativeCacheRepository

Usage:
    pytest tests/test_qualitative_save_api.py -v
    python tests/test_qualitative_save_api.py
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestQualitativeSaveAPI(unittest.TestCase):
    """Test qualitative save/load API endpoints."""

    @classmethod
    def setUpClass(cls):
        """Set up test database and app."""
        # Create temporary database
        cls.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        cls.temp_db.close()
        cls.database_url = f"sqlite:///{cls.temp_db.name}"

        # Set environment variable for database
        os.environ["DATABASE_URL"] = cls.database_url

        # Import after setting env var
        from src.surveyor.models.base import BaseModel, create_database_engine, create_session_factory
        from src.surveyor.models.qualitative_cache import QualitativeCache

        # Create engine and session
        cls.engine = create_database_engine(cls.database_url, echo=False)
        SessionFactory = create_session_factory(cls.engine)
        cls.session = SessionFactory()

        # Create all tables
        BaseModel.metadata.create_all(cls.engine)

        # Add test data
        test_data = {
            "summary": "Test organization summary",
            "themes": ["Theme 1", "Theme 2", "Theme 3"],
            "modifiers": [
                {
                    "respondent": "CEO",
                    "role": "CEO",
                    "factor": "Strong leadership",
                    "value": 5
                }
            ]
        }

        # Create cache entries for test organization
        for dimension in ["Program Technology", "Business Systems", "Data Management"]:
            entry = QualitativeCache(
                org_name="Test Organization",
                dimension=dimension,
                ai_generated_json=json.dumps(test_data),
                response_count_hash="test_hash_123"
            )
            cls.session.add(entry)

        cls.session.commit()

    @classmethod
    def tearDownClass(cls):
        """Clean up test database."""
        cls.session.close()
        cls.engine.dispose()
        os.unlink(cls.temp_db.name)

    def test_01_save_main_summary_only(self):
        """Test saving only main summary."""
        from src.services.qualitative_cache_repository import get_qualitative_cache_repository

        repo = get_qualitative_cache_repository()

        # Save main summary
        summary_text = "This is the main organization summary."
        entry = repo.save_main_summary("Test Organization", summary_text)

        # Verify saved
        self.assertIsNotNone(entry)
        self.assertEqual(entry.main_summary, summary_text)

    def test_02_get_main_summary(self):
        """Test getting main summary."""
        from src.services.qualitative_cache_repository import get_qualitative_cache_repository

        repo = get_qualitative_cache_repository()

        # Save first
        summary_text = "Retrievable summary text."
        repo.save_main_summary("Test Organization", summary_text)

        # Get summary
        retrieved = repo.get_main_summary("Test Organization")
        self.assertEqual(retrieved, summary_text)

    def test_03_get_main_summary_not_found(self):
        """Test getting main summary when none exists."""
        from src.services.qualitative_cache_repository import get_qualitative_cache_repository

        repo = get_qualitative_cache_repository()

        # Get summary for non-existent org
        retrieved = repo.get_main_summary("Nonexistent Org")
        self.assertIsNone(retrieved)

    def test_04_update_dimension_data(self):
        """Test updating dimension data."""
        from src.services.qualitative_cache_repository import get_qualitative_cache_repository

        repo = get_qualitative_cache_repository()

        # Update data
        updated_data = {
            "summary": "Updated dimension summary",
            "themes": ["New theme 1", "New theme 2", "New theme 3"],
            "modifiers": [
                {
                    "respondent": "Tech Lead",
                    "role": "Tech Lead",
                    "factor": "Budget constraints",
                    "value": -3
                }
            ]
        }

        entry = repo.update_dimension_data("Test Organization", "Program Technology", updated_data)

        # Verify updated
        self.assertIsNotNone(entry)
        self.assertTrue(entry.has_user_edits())
        self.assertEqual(entry.version, 2)  # Version incremented

        # Verify data
        cached = repo.get_cached_data("Test Organization", "Program Technology")
        self.assertEqual(cached["source"], "user_edited")
        self.assertEqual(cached["data"]["summary"], "Updated dimension summary")

    def test_05_save_multiple_dimensions(self):
        """Test saving edits for multiple dimensions."""
        from src.services.qualitative_cache_repository import get_qualitative_cache_repository

        repo = get_qualitative_cache_repository()

        dimensions = ["Program Technology", "Business Systems", "Data Management"]

        for dimension in dimensions:
            updated_data = {
                "summary": f"Updated {dimension} summary",
                "themes": ["Theme A", "Theme B", "Theme C"],
                "modifiers": []
            }
            repo.update_dimension_data("Test Organization", dimension, updated_data)

        # Verify all saved
        for dimension in dimensions:
            cached = repo.get_cached_data("Test Organization", dimension)
            self.assertEqual(cached["source"], "user_edited")
            self.assertIn(dimension, cached["data"]["summary"])

    def test_06_save_with_score_modifiers_format(self):
        """Test saving with frontend score_modifiers format."""
        from src.services.qualitative_cache_repository import get_qualitative_cache_repository

        repo = get_qualitative_cache_repository()

        # Frontend format (score_modifiers with reasoning field)
        frontend_modifiers = [
            {
                "factor": "Leadership commitment",
                "value": 5,
                "reasoning": "CEO shows strong tech vision",
                "respondent": "Sarah Johnson",
                "role": "CEO"
            }
        ]

        # Transform to cache format
        cache_data = {
            "summary": "Test summary",
            "themes": ["Theme 1", "Theme 2", "Theme 3"],
            "modifiers": [
                {
                    "respondent": m["respondent"],
                    "role": m["role"],
                    "factor": m.get("reasoning", m.get("factor", "")),
                    "value": m["value"]
                }
                for m in frontend_modifiers
            ]
        }

        repo.update_dimension_data("Test Organization", "Program Technology", cache_data)

        # Verify saved with correct format
        cached = repo.get_cached_data("Test Organization", "Program Technology")
        self.assertEqual(len(cached["data"]["modifiers"]), 1)
        self.assertEqual(cached["data"]["modifiers"][0]["factor"], "CEO shows strong tech vision")

    def test_07_error_no_cache_entry(self):
        """Test error when trying to save without existing cache."""
        from src.services.qualitative_cache_repository import get_qualitative_cache_repository

        repo = get_qualitative_cache_repository()

        # Try to save main summary for non-existent org
        with self.assertRaises(ValueError):
            repo.save_main_summary("Nonexistent Org", "Summary text")

        # Try to update dimension for non-existent org
        with self.assertRaises(ValueError):
            repo.update_dimension_data("Nonexistent Org", "Program Technology", {
                "summary": "Test",
                "themes": ["A", "B", "C"],
                "modifiers": []
            })


def run_tests():
    """Run test suite."""
    print("=" * 70)
    print("Testing Qualitative Save/Load API")
    print("=" * 70)

    # Run tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestQualitativeSaveAPI)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
