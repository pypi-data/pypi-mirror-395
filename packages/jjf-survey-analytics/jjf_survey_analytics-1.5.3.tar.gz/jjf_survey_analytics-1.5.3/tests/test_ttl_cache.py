#!/usr/bin/env python3
"""
Test script for TTL-based report caching verification.

This script tests:
1. Cache MISS on first request (report generation)
2. Cache FRESH on subsequent requests within TTL
3. Cache EXPIRED after TTL expires
4. Performance improvements from caching

Usage:
    python test_ttl_cache.py
"""

import os
import sys
import time
from datetime import datetime

import requests

# Configuration
BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")
ORG_NAME = "Hadar Institute"
TEST_USERNAME = os.getenv("TEST_USERNAME", "admin")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "admin")
CACHE_TTL_SECONDS = int(os.getenv("REPORT_CACHE_TTL", "300"))

# ANSI colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def log_test(message: str, status: str = "INFO"):
    """Log test message with timestamp and color."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    color = {"INFO": BLUE, "SUCCESS": GREEN, "ERROR": RED, "WARN": YELLOW}.get(status, RESET)

    print(f"{color}[{timestamp}] [{status}] {message}{RESET}")


def get_auth_session() -> requests.Session:
    """Create authenticated session."""
    session = requests.Session()

    # Login
    login_url = f"{BASE_URL}/login"
    response = session.post(
        login_url,
        data={"username": TEST_USERNAME, "password": TEST_PASSWORD},
        allow_redirects=False,
    )

    if response.status_code not in [200, 302]:
        raise Exception(f"Login failed: {response.status_code}")

    log_test("Authentication successful", "SUCCESS")
    return session


def clear_cache(session: requests.Session) -> bool:
    """Clear the report cache via API."""
    url = f"{BASE_URL}/api/cache/clear"
    try:
        response = session.post(url)
        if response.status_code == 200:
            log_test("Cache cleared successfully", "SUCCESS")
            return True
        else:
            log_test(f"Cache clear failed: {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log_test(f"Cache clear error: {e}", "ERROR")
        return False


def get_cache_status(session: requests.Session) -> dict:
    """Get current cache status."""
    url = f"{BASE_URL}/api/cache/status"
    try:
        response = session.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            log_test(f"Cache status failed: {response.status_code}", "ERROR")
            return {}
    except Exception as e:
        log_test(f"Cache status error: {e}", "ERROR")
        return {}


def test_report_request(session: requests.Session, org_name: str, test_name: str) -> tuple:
    """
    Make a report request and measure performance.

    Returns:
        tuple: (success: bool, duration_ms: float, cached: bool)
    """
    url = f"{BASE_URL}/report/org/{requests.utils.quote(org_name)}"

    log_test(f"Making request: {test_name}", "INFO")
    start_time = time.time()

    try:
        response = session.get(url, allow_redirects=True)
        duration_ms = (time.time() - start_time) * 1000

        success = response.status_code == 200

        if success:
            log_test(f"Request succeeded in {duration_ms:.1f}ms", "SUCCESS")
        else:
            log_test(f"Request failed: {response.status_code}", "ERROR")

        return success, duration_ms, False  # We'll check cache status separately

    except Exception as e:
        log_test(f"Request error: {e}", "ERROR")
        return False, 0, False


def run_cache_tests():
    """Run comprehensive cache validation tests."""
    print("\n" + "=" * 80)
    print(f"{BLUE}TTL Cache Validation Test Suite{RESET}")
    print(f"Target Organization: {ORG_NAME}")
    print(f"Cache TTL: {CACHE_TTL_SECONDS} seconds")
    print("=" * 80 + "\n")

    try:
        # Setup
        session = get_auth_session()

        # Test 1: Clear cache and verify
        print(f"\n{YELLOW}TEST 1: Cache Clear and Initial State{RESET}")
        print("-" * 80)
        clear_cache(session)
        time.sleep(1)

        cache_status = get_cache_status(session)
        org_cached = ORG_NAME in cache_status.get("organization_reports", {}).get(
            "organizations", {}
        )

        if not org_cached:
            log_test(f"Cache confirmed empty for {ORG_NAME}", "SUCCESS")
        else:
            log_test(f"WARNING: Cache still contains {ORG_NAME}", "WARN")

        # Test 2: First request (Cache MISS - should generate report)
        print(f"\n{YELLOW}TEST 2: First Request (Expected: Cache MISS){RESET}")
        print("-" * 80)
        log_test("This should trigger AI analysis (60+ seconds)...", "INFO")

        success1, duration1, _ = test_report_request(session, ORG_NAME, "First Request")

        if not success1:
            log_test("First request failed - cannot continue tests", "ERROR")
            return False

        if duration1 > 5000:  # More than 5 seconds indicates generation
            log_test(f"Report generation detected ({duration1:.0f}ms)", "SUCCESS")
        else:
            log_test(f"WARNING: Request too fast ({duration1:.0f}ms) - may be cached", "WARN")

        # Verify cache was populated
        time.sleep(1)
        cache_status = get_cache_status(session)
        org_reports = cache_status.get("organization_reports", {}).get("organizations", [])
        org_cached_data = next((r for r in org_reports if r["name"] == ORG_NAME), None)

        if org_cached_data and org_cached_data.get("valid"):
            log_test(f"Cache populated and valid for {ORG_NAME}", "SUCCESS")
            cached_at = org_cached_data.get("cached_at")
            log_test(f"Cached at: {cached_at}", "INFO")
        else:
            log_test(f"Cache not properly populated for {ORG_NAME}", "ERROR")

        # Test 3: Second request (Cache FRESH - should be instant)
        print(f"\n{YELLOW}TEST 3: Second Request (Expected: Cache FRESH){RESET}")
        print("-" * 80)
        log_test("This should return instantly (<100ms)...", "INFO")
        time.sleep(2)  # Brief pause to ensure clear separation

        success2, duration2, _ = test_report_request(session, ORG_NAME, "Second Request (Cached)")

        if not success2:
            log_test("Second request failed", "ERROR")
            return False

        # Performance validation
        if duration2 < 1000:  # Less than 1 second indicates cache hit
            log_test(f"Cache HIT confirmed - instant response ({duration2:.0f}ms)", "SUCCESS")
            speedup = duration1 / duration2
            log_test(f"Performance improvement: {speedup:.1f}x faster", "SUCCESS")
        else:
            log_test(f"WARNING: Response slow ({duration2:.0f}ms) - cache may have missed", "WARN")

        # Verify cache is still valid
        cache_status = get_cache_status(session)
        org_reports = cache_status.get("organization_reports", {}).get("organizations", [])
        org_cached_data = next((r for r in org_reports if r["name"] == ORG_NAME), None)

        if org_cached_data and org_cached_data.get("valid"):
            log_test(f"Cache still valid for {ORG_NAME}", "SUCCESS")
        else:
            log_test(f"Cache invalidated unexpectedly for {ORG_NAME}", "ERROR")

        # Test 4: TTL Expiration (optional - only if TTL is short enough)
        if CACHE_TTL_SECONDS <= 60:  # Only test if TTL is 1 minute or less
            print(f"\n{YELLOW}TEST 4: TTL Expiration (Expected: Cache EXPIRED){RESET}")
            print("-" * 80)
            wait_time = CACHE_TTL_SECONDS + 5
            log_test(f"Waiting {wait_time} seconds for cache to expire...", "INFO")

            for remaining in range(wait_time, 0, -5):
                print(f"  {remaining} seconds remaining...", end="\r")
                time.sleep(5)
            print()

            success3, duration3, _ = test_report_request(
                session, ORG_NAME, "Third Request (Expired)"
            )

            if not success3:
                log_test("Third request failed", "ERROR")
                return False

            if duration3 > 5000:  # More than 5 seconds indicates regeneration
                log_test(
                    f"Cache expiration detected - report regenerated ({duration3:.0f}ms)", "SUCCESS"
                )
            else:
                log_test(
                    f"WARNING: Response too fast ({duration3:.0f}ms) - cache may not have expired",
                    "WARN",
                )
        else:
            print(f"\n{YELLOW}TEST 4: TTL Expiration (SKIPPED){RESET}")
            print("-" * 80)
            log_test(f"Skipping TTL expiration test (TTL={CACHE_TTL_SECONDS}s is too long)", "INFO")
            log_test("To test expiration, set REPORT_CACHE_TTL=30 and rerun", "INFO")

        # Final summary
        print(f"\n{GREEN}{'='*80}{RESET}")
        print(f"{GREEN}Test Suite Complete{RESET}")
        print(f"{GREEN}{'='*80}{RESET}\n")

        print("Results Summary:")
        print(f"  First Request (Cache MISS):  {duration1:>8.0f}ms")
        print(f"  Second Request (Cache FRESH): {duration2:>8.0f}ms")
        if CACHE_TTL_SECONDS <= 60:
            print(f"  Third Request (Cache EXPIRED): {duration3:>8.0f}ms")
        print(f"\n  Performance Improvement: {(duration1/duration2):.1f}x faster with cache")

        return True

    except Exception as e:
        log_test(f"Test suite error: {e}", "ERROR")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Main test execution."""
    print(f"\n{BLUE}JJF Survey Analytics - TTL Cache Validation{RESET}")
    print(f"Testing against: {BASE_URL}\n")

    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            log_test("Server is running", "SUCCESS")
        else:
            log_test("Server health check failed", "ERROR")
            sys.exit(1)
    except Exception as e:
        log_test(f"Cannot connect to server: {e}", "ERROR")
        log_test(f"Make sure the app is running on {BASE_URL}", "ERROR")
        sys.exit(1)

    # Run tests
    success = run_cache_tests()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
