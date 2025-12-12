#!/usr/bin/env python3
"""
Test Progressive Loading Endpoints

Quick test script to verify progressive loading API endpoints work correctly.
Run this after starting the Flask app to test the new endpoints.
"""

import time
from typing import Any, Dict

import requests

BASE_URL = "http://localhost:5001"  # Adjust if different
ORG_NAME = "AEPi"  # Change to a valid org in your data


def test_dimension_endpoint(org_name: str, dimension: str) -> Dict[str, Any]:
    """Test single dimension endpoint."""
    url = f"{BASE_URL}/api/report/org/{org_name}/ai/dimension/{dimension}"

    print(f"\n{'='*60}")
    print(f"Testing: GET {url}")
    print(f"{'='*60}")

    start_time = time.time()

    try:
        response = requests.get(url)
        elapsed = time.time() - start_time

        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {elapsed:.2f}s")

        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Cached: {data.get('cached')}")
            print(f"Dimension: {data.get('dimension')}")
            print(f"Content Length: {len(data.get('content', ''))} chars")
            print(f"Content Preview: {data.get('content', '')[:200]}...")
            return data
        else:
            print(f"Error: {response.text}")
            return {}

    except Exception as e:
        print(f"Exception: {e}")
        return {}


def test_all_dimensions(org_name: str):
    """Test all 5 dimension endpoints."""
    dimensions = [
        "Program Technology",
        "Business Systems",
        "Data Management",
        "Infrastructure",
        "Organizational Culture",
    ]

    results = {}
    total_start = time.time()

    for dimension in dimensions:
        result = test_dimension_endpoint(org_name, dimension)
        results[dimension] = result

        # Small delay between requests to avoid rate limiting
        time.sleep(0.5)

    total_elapsed = time.time() - total_start

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total Time: {total_elapsed:.2f}s")
    print(f"Successful: {sum(1 for r in results.values() if r.get('success'))}/{len(dimensions)}")
    print(f"Cached: {sum(1 for r in results.values() if r.get('cached'))}/{len(dimensions)}")
    print(f"Generated: {sum(1 for r in results.values() if not r.get('cached'))}/{len(dimensions)}")


def test_summary_endpoint(org_name: str):
    """Test executive summary endpoint."""
    url = f"{BASE_URL}/api/report/org/{org_name}/ai/summary"

    print(f"\n{'='*60}")
    print(f"Testing: GET {url}")
    print(f"{'='*60}")

    start_time = time.time()

    try:
        response = requests.get(url)
        elapsed = time.time() - start_time

        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {elapsed:.2f}s")

        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Cached: {data.get('cached')}")
            print(f"Content Length: {len(data.get('content', ''))} chars")
            print(f"Content Preview: {data.get('content', '')[:200]}...")
        else:
            print(f"Error: {response.text}")

    except Exception as e:
        print(f"Exception: {e}")


def test_all_endpoint(org_name: str):
    """Test batch all-sections endpoint."""
    url = f"{BASE_URL}/api/report/org/{org_name}/ai/all"

    print(f"\n{'='*60}")
    print(f"Testing: GET {url}")
    print(f"{'='*60}")

    start_time = time.time()

    try:
        response = requests.get(url)
        elapsed = time.time() - start_time

        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {elapsed:.2f}s")

        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Cached: {data.get('cached')}")

            if data.get("cached"):
                print(f"Summary Length: {len(data.get('summary', ''))} chars")
                print(f"Dimensions: {len(data.get('dimensions', {}))} available")
                for dim_name, dim_data in data.get("dimensions", {}).items():
                    print(f"  - {dim_name}: {len(dim_data.get('summary', ''))} chars")
            else:
                print(f"Task ID: {data.get('task_id')}")
                print(f"Poll URL: {data.get('poll_url')}")
        else:
            print(f"Error: {response.text}")

    except Exception as e:
        print(f"Exception: {e}")


def main():
    """Run all tests."""
    print(
        """
    ╔═══════════════════════════════════════════════════════════╗
    ║         Progressive Loading Endpoint Test Suite          ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    )

    print(f"Base URL: {BASE_URL}")
    print(f"Test Organization: {ORG_NAME}")
    print(f"\nMake sure Flask app is running on {BASE_URL}")
    input("Press Enter to continue...")

    # Test 1: Batch endpoint
    print("\n\n[TEST 1] Batch All-Sections Endpoint")
    test_all_endpoint(ORG_NAME)

    # Test 2: Individual dimensions
    print("\n\n[TEST 2] Individual Dimension Endpoints")
    test_all_dimensions(ORG_NAME)

    # Test 3: Summary endpoint
    print("\n\n[TEST 3] Executive Summary Endpoint")
    test_summary_endpoint(ORG_NAME)

    print("\n\n" + "=" * 60)
    print("✅ Test suite complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
