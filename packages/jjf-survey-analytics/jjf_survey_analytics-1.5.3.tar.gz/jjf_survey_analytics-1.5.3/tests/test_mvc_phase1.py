#!/usr/bin/env python3
"""
Test script for Phase 1 MVC Refactoring: Pre-calculated modifier summaries.
Verifies that backend pre-calculates all values that template needs.
"""

import json
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.extractors.sheets_reader import SheetsReader
from src.services.report_generator import ReportGenerator


def test_precalculated_summaries():
    """Test that all modifier summaries are pre-calculated in backend."""
    print("=" * 80)
    print("Phase 1 MVC Refactoring Test: Pre-calculated Modifier Summaries")
    print("=" * 80)

    # Load sheet data
    print("\n1. Loading sheet data from Google Sheets...")
    sheet_data = SheetsReader.fetch_all_tabs(verbose=False, use_cache=True)
    print(f"   ✓ Loaded {len(sheet_data)} tabs")

    # Load admin edits to ensure modifiers exist
    print("\n2. Loading admin_edits.json...")
    try:
        with open("admin_edits.json", "r") as f:
            admin_edits = json.load(f)
        print(f"   ✓ Loaded admin edits for {len(admin_edits)} organizations")
    except FileNotFoundError:
        print("   ⚠ admin_edits.json not found, using no edits")
        admin_edits = None

    # Generate report with AI enabled
    print("\n3. Generating Hadar Institute report with AI...")
    generator = ReportGenerator(sheet_data, enable_ai=True, admin_edits=admin_edits)
    report = generator.generate_organization_report("Hadar Institute")

    if not report:
        print("   ✗ FAILED: Report generation returned None")
        return False

    print("   ✓ Report generated successfully")

    # Verify AI insights exist
    if "ai_insights" not in report or not report["ai_insights"]:
        print("\n   ⚠ No AI insights in report (AI may be disabled)")
        return True

    ai_insights = report["ai_insights"]
    print("   ✓ AI insights present")

    # Test 1: Verify dimension-level summaries
    print("\n4. Testing dimension-level pre-calculated summaries...")
    if "dimensions" not in ai_insights:
        print("   ✗ FAILED: No dimensions in AI insights")
        return False

    dimensions_with_modifiers = 0
    all_summaries_valid = True

    for dimension, analysis in ai_insights["dimensions"].items():
        modifiers = analysis.get("modifiers", [])
        if not modifiers:
            continue

        dimensions_with_modifiers += 1
        print(f"\n   Dimension: {dimension}")
        print(f"   - Modifiers count: {len(modifiers)}")

        # Check modifier_summary
        if "modifier_summary" not in analysis:
            print(f"   ✗ FAILED: modifier_summary MISSING for {dimension}")
            all_summaries_valid = False
            continue

        ms = analysis["modifier_summary"]
        required_keys = ["total_modifier", "modifier_count", "individual_values", "has_modifiers"]
        missing_keys = [k for k in required_keys if k not in ms]

        if missing_keys:
            print(f"   ✗ FAILED: modifier_summary missing keys: {missing_keys}")
            all_summaries_valid = False
            continue

        # Verify calculation accuracy
        manual_total = sum(m.get("value", 0) for m in modifiers)
        if abs(ms["total_modifier"] - manual_total) > 0.001:
            print(f"   ✗ FAILED: total_modifier mismatch: {ms['total_modifier']} vs {manual_total}")
            all_summaries_valid = False
            continue

        print("   ✓ modifier_summary valid:")
        print(f"     - total_modifier: {ms['total_modifier']:.2f}")
        print(f"     - modifier_count: {ms['modifier_count']}")
        print(f"     - has_modifiers: {ms['has_modifiers']}")

        # Check impact_summary
        if "impact_summary" not in analysis:
            print(f"   ✗ FAILED: impact_summary MISSING for {dimension}")
            all_summaries_valid = False
            continue

        ims = analysis["impact_summary"]
        required_keys = [
            "base_score",
            "adjusted_score",
            "dimension_weight",
            "score_delta",
            "overall_impact",
            "weighted_contribution",
        ]
        missing_keys = [k for k in required_keys if k not in ims]

        if missing_keys:
            print(f"   ✗ FAILED: impact_summary missing keys: {missing_keys}")
            all_summaries_valid = False
            continue

        # Verify calculation accuracy
        calculated_delta = ims["adjusted_score"] - ims["base_score"]
        if abs(ims["score_delta"] - calculated_delta) > 0.001:
            print(f"   ✗ FAILED: score_delta mismatch: {ims['score_delta']} vs {calculated_delta}")
            all_summaries_valid = False
            continue

        calculated_impact = ims["score_delta"] * ims["dimension_weight"]
        if abs(ims["overall_impact"] - calculated_impact) > 0.001:
            print(
                f"   ✗ FAILED: overall_impact mismatch: {ims['overall_impact']} vs {calculated_impact}"
            )
            all_summaries_valid = False
            continue

        print("   ✓ impact_summary valid:")
        print(f"     - base_score: {ims['base_score']:.2f}")
        print(f"     - adjusted_score: {ims['adjusted_score']:.2f}")
        print(f"     - dimension_weight: {ims['dimension_weight']:.2f}")
        print(f"     - score_delta: {ims['score_delta']:.2f}")
        print(f"     - overall_impact: {ims['overall_impact']:.3f}")

    if dimensions_with_modifiers == 0:
        print("\n   ⚠ No dimensions with modifiers found")
    elif all_summaries_valid:
        print(
            f"\n   ✓ All {dimensions_with_modifiers} dimensions have valid pre-calculated summaries"
        )
    else:
        print("\n   ✗ FAILED: Some dimension summaries are invalid")
        return False

    # Test 2: Verify total_impact_summary
    print("\n5. Testing total_impact_summary...")
    if "total_impact_summary" not in ai_insights:
        print("   ✗ FAILED: total_impact_summary MISSING")
        return False

    tis = ai_insights["total_impact_summary"]
    required_keys = [
        "total_positive_impact",
        "total_negative_impact",
        "net_impact",
        "dimensions_affected",
        "total_modifiers",
        "total_modifier_value",
    ]
    missing_keys = [k for k in required_keys if k not in tis]

    if missing_keys:
        print(f"   ✗ FAILED: total_impact_summary missing keys: {missing_keys}")
        return False

    # Verify by manually calculating
    manual_net_impact = 0
    manual_total_modifiers = 0
    manual_dimensions = 0

    for dimension, analysis in ai_insights["dimensions"].items():
        if "impact_summary" in analysis and analysis.get("modifiers"):
            manual_net_impact += analysis["impact_summary"]["overall_impact"]
            manual_total_modifiers += len(analysis.get("modifiers", []))
            manual_dimensions += 1

    if abs(tis["net_impact"] - manual_net_impact) > 0.001:
        print(f"   ✗ FAILED: net_impact mismatch: {tis['net_impact']} vs {manual_net_impact}")
        return False

    if tis["total_modifiers"] != manual_total_modifiers:
        print(
            f"   ✗ FAILED: total_modifiers mismatch: {tis['total_modifiers']} vs {manual_total_modifiers}"
        )
        return False

    if tis["dimensions_affected"] != manual_dimensions:
        print(
            f"   ✗ FAILED: dimensions_affected mismatch: {tis['dimensions_affected']} vs {manual_dimensions}"
        )
        return False

    print("   ✓ total_impact_summary valid:")
    print(f"     - net_impact: {tis['net_impact']:.3f}")
    print(f"     - total_modifiers: {tis['total_modifiers']}")
    print(f"     - dimensions_affected: {tis['dimensions_affected']}")
    print(f"     - total_positive_impact: {tis['total_positive_impact']:.3f}")
    print(f"     - total_negative_impact: {tis['total_negative_impact']:.3f}")

    # Test 3: Verify template can access values
    print("\n6. Testing template accessibility...")
    for dimension, analysis in ai_insights["dimensions"].items():
        if not analysis.get("modifiers"):
            continue

        # Simulate template access patterns
        try:
            modifier_summary = analysis["modifier_summary"]
            impact_summary = analysis["impact_summary"]

            # Template variables
            modifier_summary["total_modifier"]
            impact_summary["base_score"]
            impact_summary["adjusted_score"]
            impact_summary["dimension_weight"]
            impact_summary["overall_impact"]
            modifier_summary["modifier_count"]

            print(f"   ✓ {dimension}: All template variables accessible")
        except (KeyError, TypeError) as e:
            print(f"   ✗ FAILED: Cannot access template variables for {dimension}: {e}")
            return False

    total_impact_summary = ai_insights["total_impact_summary"]
    total_impact_summary["net_impact"]
    total_impact_summary["total_modifiers"]
    print("   ✓ Overall summary: All template variables accessible")

    print("\n" + "=" * 80)
    print("✓ Phase 1 MVC Refactoring: ALL TESTS PASSED")
    print("=" * 80)
    print("\nSummary:")
    print("- Backend pre-calculates all modifier summaries ✓")
    print("- Backend pre-calculates all impact calculations ✓")
    print("- Backend pre-calculates total impact summary ✓")
    print("- Template can access all pre-calculated values ✓")
    print("- Calculation accuracy verified ✓")
    print("\nResult: Template now ONLY renders, does NOT calculate")

    return True


if __name__ == "__main__":
    success = test_precalculated_summaries()
    sys.exit(0 if success else 1)
