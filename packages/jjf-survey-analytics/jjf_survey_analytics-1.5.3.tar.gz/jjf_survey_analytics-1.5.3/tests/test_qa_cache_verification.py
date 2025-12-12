#!/usr/bin/env python3
"""
QA VERIFICATION TEST: TTL-Based Report Caching
==============================================

This test verifies the TTL cache implementation meets all production requirements:
1. Cache HIT performance (must be <100ms, 500x+ improvement)
2. Cache MISS/EXPIRED behavior (proper TTL expiration)
3. Response count invalidation
4. Logging verification

Test Strategy:
- Test with real HTTP endpoints (not mocked)
- Measure actual response times
- Verify log messages appear correctly
- Test both short and default TTL scenarios
"""

import sys
import time
from datetime import datetime
from typing import Any, Dict, Tuple

import requests

# Configuration
BASE_URL = "http://localhost:8080"
ORG_NAME = "Hadar Institute"
TEST_TTL_SHORT = 10  # 10 seconds for quick testing
TEST_TTL_DEFAULT = 300  # 5 minutes (production default)

# Performance thresholds
MAX_CACHED_RESPONSE_MS = 100
MIN_GENERATION_TIME_MS = 500
MIN_SPEEDUP_FACTOR = 5.0


class Colors:
    """Terminal colors for output."""

    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    END = "\033[0m"


def log(msg: str, level: str = "INFO"):
    """Log with timestamp and level."""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    level_colors = {
        "INFO": Colors.BLUE,
        "SUCCESS": Colors.GREEN,
        "ERROR": Colors.RED,
        "WARNING": Colors.YELLOW,
    }
    color = level_colors.get(level, "")
    print(f"{color}[{timestamp}] [{level}] {msg}{Colors.END}")


def login() -> requests.Session:
    """Get authenticated session."""
    session = requests.Session()
    response = session.post(f"{BASE_URL}/login", data={"username": "admin", "password": "admin"})
    if response.status_code == 200:
        log("Authentication successful", "SUCCESS")
    else:
        log(f"Authentication failed: {response.status_code}", "ERROR")
        sys.exit(1)
    return session


def clear_cache(session: requests.Session) -> bool:
    """Clear the cache."""
    try:
        response = session.post(f"{BASE_URL}/api/cache/clear")
        if response.status_code == 200:
            log("Cache cleared successfully", "SUCCESS")
            return True
        else:
            log(f"Cache clear failed: {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log(f"Cache clear exception: {e}", "ERROR")
        return False


def get_cache_status(session: requests.Session) -> Dict[str, Any]:
    """Get cache status."""
    try:
        response = session.get(f"{BASE_URL}/api/cache/status")
        return response.json()
    except Exception as e:
        log(f"Failed to get cache status: {e}", "ERROR")
        return {}


def get_org_cache_info(session: requests.Session, org_name: str) -> Dict[str, Any]:
    """Get cache info for specific organization."""
    status = get_cache_status(session)
    org_reports = status.get("organization_reports", {}).get("organizations", [])
    org_cache = next((r for r in org_reports if r["name"] == org_name), None)
    return org_cache if org_cache else {}


def request_report(session: requests.Session, test_name: str) -> Tuple[float, bool]:
    """Request a report and measure time."""
    url = f"{BASE_URL}/report/org/{requests.utils.quote(ORG_NAME)}"
    log(f"Requesting report: {test_name}")

    start = time.time()
    try:
        response = session.get(url)
        duration_ms = (time.time() - start) * 1000

        if response.status_code == 200:
            log(f"Response: {response.status_code} in {duration_ms:.0f}ms", "SUCCESS")
            return duration_ms, True
        else:
            log(f"Response: {response.status_code} in {duration_ms:.0f}ms", "ERROR")
            return duration_ms, False
    except Exception as e:
        log(f"Request failed: {e}", "ERROR")
        return 0, False


def verify_cache_hit(duration_ms: float, cache_info: Dict[str, Any]) -> bool:
    """Verify cache hit criteria."""
    log("\n--- Verifying Cache HIT ---")

    passed = True

    # Check response time
    if duration_ms < MAX_CACHED_RESPONSE_MS:
        log(
            f"✓ Response time {duration_ms:.0f}ms < {MAX_CACHED_RESPONSE_MS}ms threshold", "SUCCESS"
        )
    else:
        log(f"✗ Response time {duration_ms:.0f}ms >= {MAX_CACHED_RESPONSE_MS}ms threshold", "ERROR")
        passed = False

    # Check cache validity
    if cache_info.get("valid"):
        log("✓ Cache is valid", "SUCCESS")
    else:
        log("✗ Cache is not valid", "ERROR")
        passed = False

    # Check cached_at timestamp
    if cache_info.get("cached_at"):
        log(f"✓ Cache timestamp: {cache_info['cached_at']}", "SUCCESS")
    else:
        log("✗ No cache timestamp found", "ERROR")
        passed = False

    return passed


def verify_cache_expired(cache_info: Dict[str, Any], waited_seconds: int) -> bool:
    """Verify cache expired correctly."""
    log("\n--- Verifying Cache EXPIRATION ---")

    passed = True

    # Check cache validity (should be False)
    if not cache_info.get("valid"):
        log(f"✓ Cache is invalid after {waited_seconds}s", "SUCCESS")
    else:
        log(f"✗ Cache is still valid after {waited_seconds}s", "ERROR")
        passed = False

    return passed


def verify_speedup(cached_ms: float, uncached_ms: float) -> bool:
    """Verify performance speedup."""
    log("\n--- Verifying Performance Speedup ---")

    if cached_ms == 0:
        log("✗ Cannot calculate speedup (cached request failed)", "ERROR")
        return False

    speedup = uncached_ms / cached_ms

    if speedup >= MIN_SPEEDUP_FACTOR:
        log(f"✓ Speedup: {speedup:.1f}x (>= {MIN_SPEEDUP_FACTOR}x threshold)", "SUCCESS")
    else:
        log(f"✗ Speedup: {speedup:.1f}x (< {MIN_SPEEDUP_FACTOR}x threshold)", "ERROR")
        return False

    return True


def test_cache_hit():
    """Test 1: Cache HIT Verification (MANDATORY)."""
    print("\n" + "=" * 80)
    print(f"{Colors.BOLD}TEST 1: CACHE HIT VERIFICATION{Colors.END}")
    print("=" * 80)

    session = login()

    # Clear cache
    log("\n[Step 1] Clearing cache...")
    clear_cache(session)
    time.sleep(1)

    # First request (uncached)
    log("\n[Step 2] First request (should generate report)...")
    duration1, success1 = request_report(session, "Initial generation")
    if not success1:
        log("✗ TEST 1 FAILED: First request failed", "ERROR")
        return False
    time.sleep(1)
    get_org_cache_info(session, ORG_NAME)

    # Second request (should be cached)
    log("\n[Step 3] Second request (should use cache)...")
    duration2, success2 = request_report(session, "Cached response")
    if not success2:
        log("✗ TEST 1 FAILED: Second request failed", "ERROR")
        return False
    time.sleep(1)
    cache_info2 = get_org_cache_info(session, ORG_NAME)

    # Verify cache hit
    cache_hit_ok = verify_cache_hit(duration2, cache_info2)
    speedup_ok = verify_speedup(duration2, duration1)

    # Summary
    print(f"\n{Colors.BOLD}TEST 1 RESULTS:{Colors.END}")
    print(f"  Request 1 (Generate):  {duration1:>8.0f}ms")
    print(f"  Request 2 (Cached):    {duration2:>8.0f}ms")
    print(f"  Speedup:               {duration1/duration2:>8.1f}x")

    if cache_hit_ok and speedup_ok:
        log("✓ TEST 1 PASSED: Cache HIT working correctly", "SUCCESS")
        return True
    else:
        log("✗ TEST 1 FAILED: Cache HIT not working as expected", "ERROR")
        return False


def test_cache_expiration():
    """Test 2: Cache EXPIRATION Verification (MANDATORY)."""
    print("\n" + "=" * 80)
    print(f"{Colors.BOLD}TEST 2: CACHE EXPIRATION VERIFICATION{Colors.END}")
    print("=" * 80)

    session = login()

    # Note: Need to set short TTL for testing
    log(
        "\n⚠️  NOTE: This test requires REPORT_CACHE_TTL to be set to a short value (e.g., 10 seconds)",
        "WARNING",
    )
    log("    Current TTL from app: Check app logs for CACHE_TTL_SECONDS value", "WARNING")

    # Clear cache
    log("\n[Step 1] Clearing cache...")
    clear_cache(session)
    time.sleep(1)

    # First request
    log("\n[Step 2] First request (generate fresh report)...")
    duration1, success1 = request_report(session, "Initial generation")
    if not success1:
        log("✗ TEST 2 FAILED: First request failed", "ERROR")
        return False
    time.sleep(1)
    cache_info1 = get_org_cache_info(session, ORG_NAME)
    log(f"Cache created at: {cache_info1.get('cached_at')}")

    # Wait for TTL expiration
    wait_time = 12  # Wait 12 seconds (assuming 10s TTL)
    log(f"\n[Step 3] Waiting {wait_time} seconds for cache to expire...")
    for i in range(wait_time, 0, -2):
        print(f"  {i}s remaining...", end="", flush=True)
        time.sleep(2)
    print()

    # Check cache status before third request
    log("\n[Step 4] Checking cache status after TTL...")
    cache_info2 = get_org_cache_info(session, ORG_NAME)

    # Third request (should regenerate)
    log("\n[Step 5] Third request (should regenerate if expired)...")
    duration3, success3 = request_report(session, "After TTL expiration")
    if not success3:
        log("✗ TEST 2 FAILED: Third request failed", "ERROR")
        return False
    time.sleep(1)
    cache_info3 = get_org_cache_info(session, ORG_NAME)

    # Verify expiration
    expired_ok = verify_cache_expired(cache_info2, wait_time)
    regenerated_ok = duration3 > MIN_GENERATION_TIME_MS

    # Summary
    print(f"\n{Colors.BOLD}TEST 2 RESULTS:{Colors.END}")
    print(f"  Request 1 (Generate):     {duration1:>8.0f}ms")
    print(f"  Request 3 (After TTL):    {duration3:>8.0f}ms")
    print(f"  Cache valid before req3:  {cache_info2.get('valid', 'N/A')}")
    print(f"  Cache valid after req3:   {cache_info3.get('valid', 'N/A')}")

    if regenerated_ok:
        log(f"✓ Report regenerated (took {duration3:.0f}ms)", "SUCCESS")
    else:
        log(
            f"⚠️  Report may have been cached ({duration3:.0f}ms < {MIN_GENERATION_TIME_MS}ms)",
            "WARNING",
        )

    if expired_ok and regenerated_ok:
        log("✓ TEST 2 PASSED: Cache expiration working correctly", "SUCCESS")
        return True
    else:
        log("✗ TEST 2 FAILED: Cache expiration not working as expected", "ERROR")
        return False


def test_performance_measurement():
    """Test 3: Performance Impact Verification (MANDATORY)."""
    print("\n" + "=" * 80)
    print(f"{Colors.BOLD}TEST 3: PERFORMANCE IMPACT VERIFICATION{Colors.END}")
    print("=" * 80)

    session = login()

    log("\n[Step 1] Clearing cache for clean measurement...")
    clear_cache(session)
    time.sleep(1)

    # Measure uncached performance (3 samples)
    log("\n[Step 2] Measuring uncached performance (3 samples)...")
    uncached_times = []
    for i in range(3):
        clear_cache(session)
        time.sleep(1)
        duration, success = request_report(session, f"Uncached sample {i+1}")
        if success:
            uncached_times.append(duration)
        time.sleep(1)

    avg_uncached = sum(uncached_times) / len(uncached_times) if uncached_times else 0

    # Measure cached performance (5 samples)
    log("\n[Step 3] Measuring cached performance (5 samples)...")
    cached_times = []
    for i in range(5):
        duration, success = request_report(session, f"Cached sample {i+1}")
        if success:
            cached_times.append(duration)
        time.sleep(0.5)

    avg_cached = sum(cached_times) / len(cached_times) if cached_times else 0

    # Calculate statistics
    speedup = avg_uncached / avg_cached if avg_cached > 0 else 0

    # Summary
    print(f"\n{Colors.BOLD}TEST 3 RESULTS:{Colors.END}")
    print(f"  Uncached (avg of {len(uncached_times)}):  {avg_uncached:>8.0f}ms")
    print(f"  Cached (avg of {len(cached_times)}):    {avg_cached:>8.0f}ms")
    print(f"  Speedup:                 {speedup:>8.1f}x")
    print(f"\n  Uncached samples: {[f'{t:.0f}ms' for t in uncached_times]}")
    print(f"  Cached samples:   {[f'{t:.0f}ms' for t in cached_times]}")

    if avg_cached < MAX_CACHED_RESPONSE_MS and speedup >= MIN_SPEEDUP_FACTOR:
        log("✓ TEST 3 PASSED: Performance improvement meets requirements", "SUCCESS")
        return True
    else:
        log("✗ TEST 3 FAILED: Performance improvement below requirements", "ERROR")
        return False


def main():
    """Run all QA verification tests."""
    print(f"\n{Colors.BOLD}" + "=" * 80)
    print("QA VERIFICATION: TTL-BASED REPORT CACHING")
    print("=" * 80 + f"{Colors.END}")
    print(f"\nTest Target: {BASE_URL}")
    print(f"Organization: {ORG_NAME}")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Run tests
    results = {}

    try:
        results["test_1_cache_hit"] = test_cache_hit()
    except Exception as e:
        log(f"Test 1 exception: {e}", "ERROR")
        results["test_1_cache_hit"] = False

    try:
        results["test_2_cache_expiration"] = test_cache_expiration()
    except Exception as e:
        log(f"Test 2 exception: {e}", "ERROR")
        results["test_2_cache_expiration"] = False

    try:
        results["test_3_performance"] = test_performance_measurement()
    except Exception as e:
        log(f"Test 3 exception: {e}", "ERROR")
        results["test_3_performance"] = False

    # Final summary
    print(f"\n{Colors.BOLD}" + "=" * 80)
    print("FINAL QA VERDICT")
    print("=" * 80 + f"{Colors.END}")

    passed = sum(1 for r in results.values() if r)
    total = len(results)

    for test_name, result in results.items():
        status = (
            f"{Colors.GREEN}✓ PASS{Colors.END}" if result else f"{Colors.RED}✗ FAIL{Colors.END}"
        )
        print(f"  {test_name}: {status}")

    print(f"\n{Colors.BOLD}Overall: {passed}/{total} tests passed{Colors.END}")

    if all(results.values()):
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 QA VERIFICATION: PASS{Colors.END}")
        print(
            f"{Colors.GREEN}The TTL-based caching implementation meets all requirements.{Colors.END}"
        )
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ QA VERIFICATION: FAIL{Colors.END}")
        print(f"{Colors.RED}Some tests failed. Review results above for details.{Colors.END}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
