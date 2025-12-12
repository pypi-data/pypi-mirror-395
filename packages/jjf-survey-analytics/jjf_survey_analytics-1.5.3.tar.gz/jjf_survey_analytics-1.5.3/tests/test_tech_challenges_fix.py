#!/usr/bin/env python3
"""
Test script to verify Technology Challenges component fix.
Verifies that aggregated counts are properly calculated.
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.services.organization_report_builder import get_organization_report_builder


def test_tech_insights_aggregation():
    """Test that tech insights properly aggregate responses."""

    # Initialize report builder
    builder = get_organization_report_builder(enable_ai=False)

    # Test with Hadar Institute (should have multiple respondents)
    print("\n" + "=" * 80)
    print("Testing Technology Challenges Fix - Hadar Institute")
    print("=" * 80)

    report = builder.build_report("Hadar Institute")

    if not report:
        print("❌ ERROR: Could not build report for Hadar Institute")
        return False

    tech_insights = report.get("tech_insights", {})

    # Test Challenges
    print("\n📊 Technology Challenges:")
    challenges = tech_insights.get("challenges", {})

    print(f"   CEO Response: {challenges.get('ceo', 'None')}")
    print(f"   Tech Lead Response: {challenges.get('tech_lead', 'None')}")
    print(f"   Staff Responses: {len(challenges.get('staff', []))} responses")

    aggregated_challenges = challenges.get("aggregated_counts", {})
    total_respondents = challenges.get("total_respondents", 0)

    print(f"\n   ✓ Total Respondents: {total_respondents}")
    print("   ✓ Aggregated Challenge Counts:")

    if aggregated_challenges:
        # Sort by frequency
        sorted_challenges = sorted(aggregated_challenges.items(), key=lambda x: x[1], reverse=True)
        for challenge, count in sorted_challenges:
            color = "🟢" if count >= 3 else "🔵" if count == 2 else "⚪"
            print(f"      {color} {challenge}: {count}/{total_respondents}")
    else:
        print("      ⚠️  No aggregated challenges found")

    # Test Priorities
    print("\n💰 Investment Priorities:")
    priorities = tech_insights.get("priorities", {})

    print(f"   CEO Response: {priorities.get('ceo', 'None')}")
    print(f"   Tech Lead Response: {priorities.get('tech_lead', 'None')}")
    print(f"   Staff Responses: {len(priorities.get('staff', []))} responses")

    aggregated_priorities = priorities.get("aggregated_counts", {})
    priority_respondents = priorities.get("total_respondents", 0)

    print(f"\n   ✓ Total Respondents: {priority_respondents}")
    print("   ✓ Aggregated Priority Counts:")

    if aggregated_priorities:
        # Sort by frequency
        sorted_priorities = sorted(aggregated_priorities.items(), key=lambda x: x[1], reverse=True)
        for priority, count in sorted_priorities:
            color = "🟢" if count >= 3 else "🔵" if count == 2 else "⚪"
            print(f"      {color} {priority}: {count}/{priority_respondents}")
    else:
        print("      ⚠️  No aggregated priorities found")

    # Validation
    print("\n" + "=" * 80)
    print("Validation Results:")
    print("=" * 80)

    success = True

    if total_respondents == 0:
        print("❌ FAIL: No challenge respondents counted")
        success = False
    else:
        print(f"✅ PASS: Found {total_respondents} challenge respondents")

    if priority_respondents == 0:
        print("❌ FAIL: No priority respondents counted")
        success = False
    else:
        print(f"✅ PASS: Found {priority_respondents} priority respondents")

    if not aggregated_challenges:
        print("❌ FAIL: No aggregated challenge counts")
        success = False
    else:
        print(f"✅ PASS: Found {len(aggregated_challenges)} unique challenges")

    if not aggregated_priorities:
        print("❌ FAIL: No aggregated priority counts")
        success = False
    else:
        print(f"✅ PASS: Found {len(aggregated_priorities)} unique priorities")

    # Check for proper aggregation (should have counts > 1 for some items)
    has_consensus = any(count >= 2 for count in aggregated_challenges.values())
    if has_consensus:
        print("✅ PASS: Found consensus items (count >= 2)")
    else:
        print("⚠️  WARNING: No consensus items found (all counts = 1)")

    print("\n" + "=" * 80)

    return success


if __name__ == "__main__":
    success = test_tech_insights_aggregation()
    sys.exit(0 if success else 1)
