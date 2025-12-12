#!/usr/bin/env python3
"""
Test script for concurrent AI dimension analysis.

This tests the performance improvement from serial to concurrent processing.
"""

import asyncio
import os
import time

from dotenv import load_dotenv

from src.analytics.ai_analyzer import AIAnalyzer

# Load environment
load_dotenv(".env.local")

# Sample test data (minimal for quick testing)
SAMPLE_RESPONSES = {
    "Program Technology": [
        {
            "respondent": "Test User",
            "role": "CEO",
            "text": "We use modern digital tools for program delivery and participant engagement.",
        }
    ],
    "Business Systems": [
        {
            "respondent": "Test User",
            "role": "Tech Lead",
            "text": "Our CRM and accounting systems are well integrated and cloud-based.",
        }
    ],
    "Data Management": [
        {
            "respondent": "Test User",
            "role": "Staf",
            "text": "We collect data systematically but analysis tools could be improved.",
        }
    ],
    "Infrastructure": [
        {
            "respondent": "Test User",
            "role": "CEO",
            "text": "Infrastructure is solid with cloud hosting and regular backups.",
        }
    ],
    "Organizational Culture": [
        {
            "respondent": "Test User",
            "role": "Tech Lead",
            "text": "Team is generally tech-savvy but training could be more consistent.",
        }
    ],
}


def test_serial_execution():
    """Test the original serial implementation."""
    print("\n" + "=" * 80)
    print("TESTING SERIAL EXECUTION (Original Implementation)")
    print("=" * 80)

    analyzer = AIAnalyzer()

    def progress_callback(progress, message):
        print(f"[{progress}%] {message}")

    start_time = time.time()

    result = analyzer.analyze_organization_qualitative(
        org_name="Test Organization",
        all_responses=SAMPLE_RESPONSES,
        progress_callback=progress_callback,
    )

    end_time = time.time()
    elapsed = end_time - start_time

    print(f"\n✓ Serial execution completed in {elapsed:.2f} seconds")
    print(f"✓ Analyzed {len(result['dimensions'])} dimensions")

    return elapsed, result


async def test_concurrent_execution():
    """Test the new concurrent async implementation."""
    print("\n" + "=" * 80)
    print("TESTING CONCURRENT EXECUTION (New Async Implementation)")
    print("=" * 80)

    analyzer = AIAnalyzer()

    def progress_callback(progress, message):
        print(f"[{progress}%] {message}")

    start_time = time.time()

    result = await analyzer.analyze_organization_qualitative_async(
        org_name="Test Organization",
        all_responses=SAMPLE_RESPONSES,
        progress_callback=progress_callback,
    )

    end_time = time.time()
    elapsed = end_time - start_time

    print(f"\n✓ Concurrent execution completed in {elapsed:.2f} seconds")
    print(f"✓ Analyzed {len(result['dimensions'])} dimensions")

    return elapsed, result


def compare_results(serial_result, concurrent_result):
    """Compare results from both implementations."""
    print("\n" + "=" * 80)
    print("COMPARING RESULTS")
    print("=" * 80)

    # Check if same dimensions were analyzed
    serial_dims = set(serial_result["dimensions"].keys())
    concurrent_dims = set(concurrent_result["dimensions"].keys())

    if serial_dims == concurrent_dims:
        print(f"✓ Both analyzed same dimensions: {sorted(serial_dims)}")
    else:
        print("✗ Dimension mismatch!")
        print(f"  Serial: {sorted(serial_dims)}")
        print(f"  Concurrent: {sorted(concurrent_dims)}")

    # Check if both have modifiers and summaries
    for dim in serial_dims:
        serial_data = serial_result["dimensions"][dim]
        concurrent_data = concurrent_result["dimensions"].get(dim, {})

        has_modifiers = "modifiers" in serial_data and "modifiers" in concurrent_data
        has_summary = "summary" in serial_data and "summary" in concurrent_data

        print(f"  {dim}:")
        print(f"    Modifiers: {'✓' if has_modifiers else '✗'}")
        print(f"    Summary: {'✓' if has_summary else '✗'}")


def main():
    """Run performance comparison tests."""
    print("\n" + "=" * 80)
    print("CONCURRENT AI ANALYSIS PERFORMANCE TEST")
    print("=" * 80)
    print(f"\nTesting with {len(SAMPLE_RESPONSES)} dimensions")
    print("Each dimension will make an OpenAI API call (~10-20 seconds each)")

    # Check for API key
    if not os.getenv("OPENROUTER_API_KEY"):
        print("\n✗ ERROR: OPENROUTER_API_KEY not found in environment")
        print("Please ensure .env.local is configured correctly")
        return

    try:
        # Test serial execution
        serial_time, serial_result = test_serial_execution()

        # Test concurrent execution
        concurrent_time, concurrent_result = asyncio.run(test_concurrent_execution())

        # Compare results
        compare_results(serial_result, concurrent_result)

        # Print performance summary
        print("\n" + "=" * 80)
        print("PERFORMANCE SUMMARY")
        print("=" * 80)
        print(f"Serial execution:     {serial_time:.2f} seconds")
        print(f"Concurrent execution: {concurrent_time:.2f} seconds")

        speedup = serial_time / concurrent_time if concurrent_time > 0 else 0
        time_saved = serial_time - concurrent_time

        print(f"\nSpeedup: {speedup:.2f}x faster")
        print(f"Time saved: {time_saved:.2f} seconds ({time_saved/serial_time*100:.1f}% reduction)")

        # Expected performance
        print("\n" + "-" * 80)
        print("EXPECTED PERFORMANCE:")
        print("-" * 80)
        print("Serial: ~60 seconds (5 dimensions × ~12 seconds each)")
        print("Concurrent: ~20 seconds (max of 5 parallel calls)")
        print("Expected speedup: ~3x faster")
        print("-" * 80)

        if speedup >= 2.5:
            print("\n✓ SUCCESS: Concurrent implementation is significantly faster!")
        elif speedup >= 1.5:
            print("\n⚠ PARTIAL SUCCESS: Some speedup achieved, but less than expected")
        else:
            print("\n✗ FAILURE: Concurrent implementation not providing expected speedup")

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
