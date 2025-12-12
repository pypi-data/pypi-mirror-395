#!/usr/bin/env python3
"""
Test script for JJF-11: AI grounding validation
Validates that _validate_grounding() correctly detects generic vs. grounded text
"""

import sys
sys.path.insert(0, '/Users/masa/Clients/JJF/jjf-survey-analytics')

from src.analytics.ai_analyzer import AIAnalyzer


def test_grounding_validation():
    """Test the _validate_grounding() method with various scenarios."""

    analyzer = AIAnalyzer()

    # Test Data: Sample source responses
    source_responses = [
        {
            "respondent": "John Doe",
            "role": "CEO",
            "text": "We use Salesforce for donor management and WordPress for our website. Integration between systems is challenging."
        },
        {
            "respondent": "Jane Smith",
            "role": "Tech Lead",
            "text": "Our cloud infrastructure uses AWS and we have good backup procedures in place. Staff training on new tools is a gap."
        }
    ]

    # Test Case 1: Generic text (should FAIL)
    generic_text = (
        "Your organization should consider improving its technology infrastructure. "
        "It's important to invest in better systems and may want to explore cloud solutions. "
        "Best practices suggest regular staff training."
    )

    print("\n" + "="*80)
    print("TEST CASE 1: Generic text (should FAIL)")
    print("="*80)
    print(f"Text: {generic_text}")
    result1 = analyzer._validate_grounding(generic_text, source_responses, "Test Dimension")
    print(f"Result: {'PASS' if result1 else 'FAIL'} (expected: FAIL)")
    assert not result1, "Generic text should fail grounding validation"
    print("✓ Test passed: Generic text correctly rejected")

    # Test Case 2: Grounded text referencing actual responses (should PASS)
    grounded_text = (
        "Your team mentioned using Salesforce for donor management and WordPress for your website. "
        "The Tech Lead noted that cloud infrastructure uses AWS with good backup procedures. "
        "Integration challenges between systems were highlighted as an area needing attention."
    )

    print("\n" + "="*80)
    print("TEST CASE 2: Grounded text with specific references (should PASS)")
    print("="*80)
    print(f"Text: {grounded_text}")
    result2 = analyzer._validate_grounding(grounded_text, source_responses, "Test Dimension")
    print(f"Result: {'PASS' if result2 else 'FAIL'} (expected: PASS)")
    assert result2, "Grounded text should pass validation"
    print("✓ Test passed: Grounded text correctly accepted")

    # Test Case 3: Mixed - some grounding but too much generic advice (should FAIL)
    mixed_text = (
        "Your organization uses Salesforce and WordPress. However, you should consider "
        "implementing better integration practices. It's important to have a comprehensive "
        "technology strategy and may want to explore additional training opportunities."
    )

    print("\n" + "="*80)
    print("TEST CASE 3: Mixed text with some grounding but excessive generic advice (should FAIL)")
    print("="*80)
    print(f"Text: {mixed_text}")
    result3 = analyzer._validate_grounding(mixed_text, source_responses, "Test Dimension")
    print(f"Result: {'PASS' if result3 else 'FAIL'} (expected: FAIL)")
    assert not result3, "Mixed text with excessive generic phrases should fail"
    print("✓ Test passed: Mixed text correctly rejected due to generic phrases")

    # Test Case 4: Well-grounded with specific indicators (should PASS)
    well_grounded_text = (
        "Staff expressed challenges with integration between Salesforce and WordPress. "
        "The responses indicate AWS cloud infrastructure is currently in place with backup "
        "procedures. Training on new tools was noted as a gap requiring attention."
    )

    print("\n" + "="*80)
    print("TEST CASE 4: Well-grounded with specific indicators (should PASS)")
    print("="*80)
    print(f"Text: {well_grounded_text}")
    result4 = analyzer._validate_grounding(well_grounded_text, source_responses, "Test Dimension")
    print(f"Result: {'PASS' if result4 else 'FAIL'} (expected: PASS)")
    assert result4, "Well-grounded text with indicators should pass"
    print("✓ Test passed: Well-grounded text correctly accepted")

    # Test Case 5: Low semantic overlap (should FAIL)
    low_overlap_text = (
        "The feedback highlighted various technology challenges and opportunities. "
        "Several staff members discussed different aspects of the digital landscape. "
        "Overall technology maturity appears to be evolving."
    )

    print("\n" + "="*80)
    print("TEST CASE 5: Low semantic overlap with source (should FAIL)")
    print("="*80)
    print(f"Text: {low_overlap_text}")
    result5 = analyzer._validate_grounding(low_overlap_text, source_responses, "Test Dimension")
    print(f"Result: {'PASS' if result5 else 'FAIL'} (expected: FAIL)")
    assert not result5, "Text with low semantic overlap should fail"
    print("✓ Test passed: Low overlap text correctly rejected")

    print("\n" + "="*80)
    print("ALL TESTS PASSED!")
    print("="*80)
    print("\nSummary:")
    print("- Generic advice phrases are correctly detected and rejected")
    print("- Grounded text with source terminology is correctly accepted")
    print("- Semantic overlap validation works as expected")
    print("- Specific indicator phrases are properly recognized")
    print("\n✓ JJF-11 grounding validation is working correctly")


if __name__ == "__main__":
    try:
        test_grounding_validation()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
