"""
Integration test for AI hallucination prevention in realistic report scenarios.

This test simulates the actual 70 Faces Media report generation scenario
to verify that hallucinated respondent names are properly detected and removed.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analytics.ai_analyzer import AIAnalyzer

def test_realistic_dimension_insights_with_hallucinations():
    """Test dimension insights generation with hallucinated names (realistic scenario)"""

    analyzer = AIAnalyzer()

    print("\n" + "=" * 80)
    print("INTEGRATION TEST: Realistic Dimension Insights with Hallucinations")
    print("=" * 80)

    # Simulate actual respondents from 70 Faces Media survey
    actual_respondents = [
        "Rabbi Michael Knopf",  # CEO
        "Jonathan Webber",       # Tech Lead
        "Sarah Cohen",           # Staff 1
        "Rachel Goldman",        # Staff 2
        "David Levine"           # Staff 3
    ]

    # Test Case 1: AI generates text with hallucinated names (the actual bug)
    print("\n--- Test Case 1: Hallucinated Names in Dimension Insights ---")

    hallucinated_insight = """Based on survey responses, your organization demonstrates strong
    technology integration in program delivery. Sarah Williams noted the importance of mobile
    accessibility, while Jonathan Webber highlighted cloud security improvements. John Doe
    emphasized staff training needs. Rabbi Michael Knopf expressed confidence in the current
    infrastructure."""

    print(f"Original AI-generated text (with hallucinations):")
    print(f"  {hallucinated_insight}")
    print(f"\nActual respondents: {', '.join(actual_respondents)}")

    cleaned_text = analyzer._validate_narrative_text(
        hallucinated_insight,
        actual_respondents,
        "Program Technology dimension insight"
    )

    print(f"\nCleaned text:")
    print(f"  {cleaned_text}")

    # Verify hallucinated names are removed
    assert "Sarah Williams" not in cleaned_text, "Failed to remove hallucinated name 'Sarah Williams'"
    assert "John Doe" not in cleaned_text, "Failed to remove hallucinated name 'John Doe'"

    # Verify valid names are preserved
    assert "Jonathan Webber" in cleaned_text, "Incorrectly removed valid name 'Jonathan Webber'"
    assert "Rabbi Michael Knopf" in cleaned_text, "Incorrectly removed valid name 'Rabbi Michael Knopf'"

    # Verify replacements are present
    assert "[respondent]" in cleaned_text, "Missing [respondent] replacement"

    print("\n✅ Test Case 1 PASSED: Hallucinated names removed, valid names preserved")

    # Test Case 2: All names are valid (no false positives)
    print("\n--- Test Case 2: All Valid Names (No False Positives) ---")

    valid_insight = """Based on survey responses, Rabbi Michael Knopf highlighted strategic
    technology planning, Jonathan Webber noted infrastructure improvements, and Sarah Cohen
    emphasized user training needs. Rachel Goldman and David Levine agreed on the importance
    of data security."""

    print(f"Original AI-generated text (all valid):")
    print(f"  {valid_insight}")

    cleaned_text_2 = analyzer._validate_narrative_text(
        valid_insight,
        actual_respondents,
        "Data Management dimension insight"
    )

    print(f"\nCleaned text:")
    print(f"  {cleaned_text_2}")

    # Text should be unchanged
    assert cleaned_text_2 == valid_insight, "Incorrectly modified text with all valid names"

    # All names should be preserved
    for name in actual_respondents:
        assert name in cleaned_text_2, f"Incorrectly removed valid name '{name}'"

    print("\n✅ Test Case 2 PASSED: All valid names preserved, no false positives")

    # Test Case 3: Mix of titles and hallucinated names
    print("\n--- Test Case 3: Mix of Titles and Hallucinated Names ---")

    mixed_insight = """The Tech Lead highlighted cloud infrastructure, while Jane Smith
    discussed mobile accessibility. The Executive Director emphasized strategic planning.
    Mark Johnson noted security concerns, and Sarah Cohen provided valuable feedback on
    user experience."""

    print(f"Original AI-generated text (mixed):")
    print(f"  {mixed_insight}")

    cleaned_text_3 = analyzer._validate_narrative_text(
        mixed_insight,
        actual_respondents,
        "Infrastructure dimension insight"
    )

    print(f"\nCleaned text:")
    print(f"  {cleaned_text_3}")

    # Verify hallucinated names removed
    assert "Jane Smith" not in cleaned_text_3, "Failed to remove hallucinated name 'Jane Smith'"
    assert "Mark Johnson" not in cleaned_text_3, "Failed to remove hallucinated name 'Mark Johnson'"

    # Verify titles preserved
    assert "Tech Lead" in cleaned_text_3, "Incorrectly removed title 'Tech Lead'"
    assert "Executive Director" in cleaned_text_3, "Incorrectly removed title 'Executive Director'"

    # Verify valid names preserved
    assert "Sarah Cohen" in cleaned_text_3, "Incorrectly removed valid name 'Sarah Cohen'"

    print("\n✅ Test Case 3 PASSED: Titles preserved, hallucinated names removed, valid names kept")

    # Test Case 4: Edge case - names with common words
    print("\n--- Test Case 4: Edge Cases with Common Business Terms ---")

    edge_case_insight = """The organization uses Google Cloud and Apple Systems for
    collaboration. Social Media presence and Cloud Security were evaluated."""

    print(f"Original AI-generated text (edge cases):")
    print(f"  {edge_case_insight}")

    cleaned_text_4 = analyzer._validate_narrative_text(
        edge_case_insight,
        actual_respondents,
        "Organizational Culture dimension insight"
    )

    print(f"\nCleaned text:")
    print(f"  {cleaned_text_4}")

    # Text should be unchanged - these are business terms, not names
    assert cleaned_text_4 == edge_case_insight, "Incorrectly modified text with business terms"

    # Verify business terms preserved
    assert "Google Cloud" in cleaned_text_4, "Incorrectly removed 'Google Cloud'"
    assert "Apple Systems" in cleaned_text_4, "Incorrectly removed 'Apple Systems'"
    assert "Social Media" in cleaned_text_4, "Incorrectly removed 'Social Media'"
    assert "Cloud Security" in cleaned_text_4, "Incorrectly removed 'Cloud Security'"

    print("\n✅ Test Case 4 PASSED: Business terms correctly preserved")

    # Test Case 5: Heavy hallucination scenario
    print("\n--- Test Case 5: Heavy Hallucination (Multiple Fake Names) ---")

    heavy_hallucination = """Emily Johnson shared insights on cloud migration, while Michael
    Chen discussed API integrations. Jennifer Williams emphasized security protocols, and
    Robert Martinez highlighted data governance. Lisa Anderson noted training needs."""

    print(f"Original AI-generated text (heavy hallucination):")
    print(f"  {heavy_hallucination}")

    cleaned_text_5 = analyzer._validate_narrative_text(
        heavy_hallucination,
        actual_respondents,
        "Business Systems dimension insight"
    )

    print(f"\nCleaned text:")
    print(f"  {cleaned_text_5}")

    # All names should be removed (none are valid)
    hallucinated_names = ["Emily Johnson", "Michael Chen", "Jennifer Williams",
                          "Robert Martinez", "Lisa Anderson"]
    for name in hallucinated_names:
        assert name not in cleaned_text_5, f"Failed to remove hallucinated name '{name}'"

    # Should have multiple [respondent] replacements
    replacement_count = cleaned_text_5.count("[respondent]")
    assert replacement_count == len(hallucinated_names), \
        f"Expected {len(hallucinated_names)} replacements, got {replacement_count}"

    print(f"\n✅ Test Case 5 PASSED: All {len(hallucinated_names)} hallucinated names removed")

    print("\n" + "=" * 80)
    print("ALL INTEGRATION TESTS PASSED!")
    print("=" * 80)
    print("\nSummary:")
    print("  ✅ Hallucinated names correctly detected and removed")
    print("  ✅ Valid respondent names preserved")
    print("  ✅ Common titles and business terms preserved")
    print("  ✅ Edge cases handled correctly")
    print("  ✅ Heavy hallucination scenarios handled")
    print("\nThe AI hallucination fix is working correctly!")
    print("=" * 80)

if __name__ == "__main__":
    test_realistic_dimension_insights_with_hallucinations()
