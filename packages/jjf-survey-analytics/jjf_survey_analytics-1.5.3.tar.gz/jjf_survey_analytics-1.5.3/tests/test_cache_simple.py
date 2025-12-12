#!/usr/bin/env python3
"""Simple cache test with live log monitoring."""

import time

import requests

BASE_URL = "http://localhost:8080"
ORG_NAME = "Hadar Institute"


def login():
    """Get authenticated session."""
    session = requests.Session()
    _ = session.post(f"{BASE_URL}/login", data={"username": "admin", "password": "admin"})
    return session


def clear_cache(session):
    """Clear the cache."""
    response = session.post(f"{BASE_URL}/api/cache/clear")
    print(f"✓ Cache cleared: {response.status_code}")
    time.sleep(2)


def request_report(session, test_name):
    """Request a report and measure time."""
    url = f"{BASE_URL}/report/org/{requests.utils.quote(ORG_NAME)}"
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")

    start = time.time()
    response = session.get(url)
    duration = (time.time() - start) * 1000

    print(f"Status: {response.status_code}")
    print(f"Duration: {duration:.0f}ms")

    return duration


def main():
    print("TTL Cache Test - Simple Version")
    print("=" * 60)

    session = login()
    print("✓ Logged in")

    # Test 1: Clear cache and first request
    clear_cache(session)
    duration1 = request_report(session, "First Request (Cache MISS)")
    time.sleep(2)

    # Test 2: Second request (should be cached)
    duration2 = request_report(session, "Second Request (Cache FRESH)")
    time.sleep(2)

    # Test 3: Wait for TTL expiration
    print(f"\n{'='*60}")
    print("Waiting 35 seconds for cache to expire...")
    print(f"{'='*60}")
    time.sleep(35)

    duration3 = request_report(session, "Third Request (Cache EXPIRED)")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Request 1 (MISS):    {duration1:>8.0f}ms")
    print(f"Request 2 (FRESH):   {duration2:>8.0f}ms")
    print(f"Request 3 (EXPIRED): {duration3:>8.0f}ms")
    print(f"\nSpeedup: {duration1/duration2:.1f}x faster with cache")

    if duration3 < 1000:
        print("\n⚠️  WARNING: Request 3 was too fast - cache may not have expired!")
    else:
        print("\n✓ Cache expiration working correctly")


if __name__ == "__main__":
    main()
