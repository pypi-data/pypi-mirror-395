#!/usr/bin/env python3
"""Complete cache TTL test with status monitoring."""

import time
from datetime import datetime

import requests

BASE_URL = "http://localhost:8080"
ORG_NAME = "Hadar Institute"


def log(msg):
    """Log with timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")


def login():
    """Get authenticated session."""
    session = requests.Session()
    _ = session.post(f"{BASE_URL}/login", data={"username": "admin", "password": "admin"})
    return session


def clear_cache(session):
    """Clear the cache."""
    response = session.post(f"{BASE_URL}/api/cache/clear")
    log(f"Cache cleared: {response.status_code}")


def get_cache_status(session):
    """Get cache status."""
    response = session.get(f"{BASE_URL}/api/cache/status")
    return response.json()


def request_report(session, test_name):
    """Request a report and measure time."""
    url = f"{BASE_URL}/report/org/{requests.utils.quote(ORG_NAME)}"
    log(f"Requesting report: {test_name}")

    start = time.time()
    response = session.get(url)
    duration = (time.time() - start) * 1000

    log(f"Response: {response.status_code} in {duration:.0f}ms")
    return duration


def check_hadar_cache(session):
    """Check Hadar Institute cache status."""
    status = get_cache_status(session)
    org_reports = status.get("organization_reports", {}).get("organizations", [])
    hadar = next((r for r in org_reports if r["name"] == ORG_NAME), None)

    if hadar:
        log(f"  Cached: True, Valid: {hadar.get('valid')}, At: {hadar.get('cached_at')}")
        return hadar.get("valid")
    else:
        log("  Cached: False")
        return False


def main():
    print("\n" + "=" * 70)
    print("COMPLETE TTL CACHE TEST")
    print("=" * 70)

    session = login()
    log("Authenticated")

    # Step 1: Clear cache
    print("\n--- STEP 1: Clear Cache ---")
    clear_cache(session)
    time.sleep(1)
    check_hadar_cache(session)

    # Step 2: First request (should generate)
    print("\n--- STEP 2: First Request (Should Generate) ---")
    duration1 = request_report(session, "Initial generation")
    time.sleep(1)
    valid1 = check_hadar_cache(session)

    # Step 3: Second request (should be cached)
    print("\n--- STEP 3: Second Request (Should Be Cached) ---")
    duration2 = request_report(session, "Cached response")
    time.sleep(1)
    valid2 = check_hadar_cache(session)

    # Step 4: Wait for expiration
    print("\n--- STEP 4: Wait for TTL Expiration (30 seconds) ---")
    log("Waiting 35 seconds for cache to expire...")
    for i in range(35, 0, -5):
        print(f"  {i}s...", end="", flush=True)
        time.sleep(5)
    print()

    # Check cache status before request
    log("Checking cache status after TTL...")
    valid3_before = check_hadar_cache(session)

    # Step 5: Third request (should regenerate if expired)
    print("\n--- STEP 5: Third Request (Should Regenerate if Expired) ---")
    duration3 = request_report(session, "After TTL expiration")
    time.sleep(1)
    valid3_after = check_hadar_cache(session)

    # Summary
    print("\n" + "=" * 70)
    print("TEST RESULTS")
    print("=" * 70)
    print(f"Request 1 (Generate):        {duration1:>8.0f}ms")
    print(f"Request 2 (Cache Fresh):     {duration2:>8.0f}ms  ({duration1/duration2:.1f}x faster)")
    print(f"Request 3 (After TTL):       {duration3:>8.0f}ms")

    print("\nCache Status:")
    print(f"  After Request 1: Valid={valid1}")
    print(f"  After Request 2: Valid={valid2}")
    print(f"  Before Request 3: Valid={valid3_before}")
    print(f"  After Request 3: Valid={valid3_after}")

    print("\nValidation:")
    if duration2 < 1000:
        print(f"  ✓ Cache HIT working (Request 2: {duration2:.0f}ms)")
    else:
        print(f"  ❌ Cache HIT failed (Request 2: {duration2:.0f}ms)")

    if not valid3_before:
        print("  ✓ Cache EXPIRED correctly after 35 seconds")
    else:
        print(f"  ❌ Cache did NOT expire (still valid={valid3_before})")

    if duration3 > 1000:
        print(f"  ✓ Regeneration triggered (Request 3: {duration3:.0f}ms)")
    else:
        print(f"  ⚠️  Request 3 was fast ({duration3:.0f}ms) - may be cached")


if __name__ == "__main__":
    main()
