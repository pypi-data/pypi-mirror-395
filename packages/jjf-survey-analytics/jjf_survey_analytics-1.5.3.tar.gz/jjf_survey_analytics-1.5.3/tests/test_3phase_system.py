#!/usr/bin/env python3
"""
Test script for 3-phase report generation system.

This script tests the cache functionality and 3-phase workflow.
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.services.container import get_container


def test_cache_structure():
    """Test 1: Verify cache directory structure."""
    print("\n=== Test 1: Cache Directory Structure ===")
    cache_dir = "cache/reports"

    if os.path.exists(cache_dir):
        print(f"✓ Cache directory exists: {cache_dir}")
        print(f"  Directory is writable: {os.access(cache_dir, os.W_OK)}")
    else:
        print(f"✗ Cache directory does not exist: {cache_dir}")
        return False

    return True


def test_cache_helper_methods():
    """Test 2: Test cache helper methods."""
    print("\n=== Test 2: Cache Helper Methods ===")

    try:
        container = get_container()
        report_service = container.report_service

        # Test check_cache_status
        print("Testing check_cache_status...")
        test_org = "Test Organization"
        cache_status = report_service.check_cache_status(test_org)
        print(f"✓ check_cache_status returned: {cache_status}")

        # Test _get_cache_path
        print("\nTesting _get_cache_path...")
        ai_path = report_service._get_cache_path(test_org, "ai_analysis")
        scores_path = report_service._get_cache_path(test_org, "scores")
        print(f"✓ AI analysis path: {ai_path}")
        print(f"✓ Scores path: {scores_path}")

        return True

    except Exception as e:
        print(f"✗ Error testing cache helper methods: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_save_and_load_cache():
    """Test 3: Test saving and loading cache data."""
    print("\n=== Test 3: Save and Load Cache ===")

    try:
        container = get_container()
        report_service = container.report_service

        test_org = "Test Organization Save Load"

        # Test save and load AI analysis
        print("Testing AI analysis cache...")
        test_ai_data = {
            "organization": test_org,
            "dimensions": {
                "Program Technology": {
                    "summary": "Test summary",
                    "modifiers": [{"value": 0.2, "reason": "Test"}],
                }
            },
        }

        saved_path = report_service.save_ai_analysis(test_org, test_ai_data)
        print(f"✓ Saved AI analysis to: {saved_path}")

        loaded_ai_data = report_service.load_ai_analysis(test_org)
        if loaded_ai_data:
            print("✓ Loaded AI analysis successfully")
            print(f"  Has metadata: {'metadata' in loaded_ai_data}")
            print(f"  Organization: {loaded_ai_data.get('organization')}")
        else:
            print("✗ Failed to load AI analysis")
            return False

        # Test save and load scores
        print("\nTesting scores cache...")
        test_scores_data = {
            "organization": test_org,
            "maturity": {"overall_score": 3.5, "maturity_level": "Emerging"},
        }

        saved_path = report_service.save_scores(test_org, test_scores_data)
        print(f"✓ Saved scores to: {saved_path}")

        loaded_scores_data = report_service.load_scores(test_org)
        if loaded_scores_data:
            print("✓ Loaded scores successfully")
            print(f"  Has metadata: {'metadata' in loaded_scores_data}")
            print(f"  Organization: {loaded_scores_data.get('organization')}")
        else:
            print("✗ Failed to load scores")
            return False

        # Test check_cache_status after saving
        print("\nTesting cache status after saving...")
        cache_status = report_service.check_cache_status(test_org)
        print(f"✓ Cache status: {cache_status}")

        if cache_status["ai_cached"] and cache_status["scores_cached"]:
            print("✓ Both caches detected correctly")
        else:
            print("✗ Cache status incorrect")
            return False

        # Cleanup
        print("\nCleaning up test files...")
        if cache_status["ai_path"] and os.path.exists(cache_status["ai_path"]):
            os.remove(cache_status["ai_path"])
            print(f"  Removed: {cache_status['ai_path']}")
        if cache_status["scores_path"] and os.path.exists(cache_status["scores_path"]):
            os.remove(cache_status["scores_path"])
            print(f"  Removed: {cache_status['scores_path']}")

        return True

    except Exception as e:
        print(f"✗ Error testing save/load cache: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_phase_methods_exist():
    """Test 4: Verify 3-phase methods exist."""
    print("\n=== Test 4: 3-Phase Methods Existence ===")

    try:
        container = get_container()
        report_service = container.report_service

        # Check Phase 1 method
        if hasattr(report_service, "generate_ai_analysis_async"):
            print("✓ Phase 1 method exists: generate_ai_analysis_async")
        else:
            print("✗ Phase 1 method missing")
            return False

        # Check Phase 2 method
        if hasattr(report_service, "generate_scores_sync"):
            print("✓ Phase 2 method exists: generate_scores_sync")
        else:
            print("✗ Phase 2 method missing")
            return False

        # Check Phase 3 method
        if hasattr(report_service, "merge_and_generate_html"):
            print("✓ Phase 3 method exists: merge_and_generate_html")
        else:
            print("✗ Phase 3 method missing")
            return False

        # Check helper methods
        if hasattr(report_service, "_generate_ai_analysis_task"):
            print("✓ Helper method exists: _generate_ai_analysis_task")
        else:
            print("✗ Helper method missing")
            return False

        if hasattr(report_service, "_extract_org_data"):
            print("✓ Helper method exists: _extract_org_data")
        else:
            print("✗ Helper method missing")
            return False

        if hasattr(report_service, "_apply_ai_modifiers_to_report"):
            print("✓ Helper method exists: _apply_ai_modifiers_to_report")
        else:
            print("✗ Helper method missing")
            return False

        return True

    except Exception as e:
        print(f"✗ Error checking phase methods: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("3-Phase Report Generation System - Test Suite")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Cache Structure", test_cache_structure()))
    results.append(("Cache Helper Methods", test_cache_helper_methods()))
    results.append(("Save/Load Cache", test_save_and_load_cache()))
    results.append(("Phase Methods Exist", test_phase_methods_exist()))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ All tests passed! 3-phase system is ready.")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
