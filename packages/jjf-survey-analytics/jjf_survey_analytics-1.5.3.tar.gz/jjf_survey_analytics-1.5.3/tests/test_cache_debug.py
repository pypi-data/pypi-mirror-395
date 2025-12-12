#!/usr/bin/env python3
"""Debug cache TTL validation."""

import json
import time

import requests

BASE_URL = "http://localhost:8080"


def login():
    """Get authenticated session."""
    session = requests.Session()
    _ = session.post(f"{BASE_URL}/login", data={"username": "admin", "password": "admin"})
    return session


def get_cache_status(session):
    """Get cache status."""
    response = session.get(f"{BASE_URL}/api/cache/status")
    return response.json()


def main():
    session = login()
    print("✓ Logged in\n")

    # Get cache status before
    print("=" * 60)
    print("CACHE STATUS BEFORE")
    print("=" * 60)
    status = get_cache_status(session)
    print(json.dumps(status, indent=2))

    # Wait 35 seconds
    print("\n" + "=" * 60)
    print("Waiting 35 seconds...")
    print("=" * 60)
    for i in range(35, 0, -5):
        print(f"  {i} seconds remaining...")
        time.sleep(5)

    # Get cache status after
    print("\n" + "=" * 60)
    print("CACHE STATUS AFTER 35 SECONDS")
    print("=" * 60)
    status = get_cache_status(session)
    print(json.dumps(status, indent=2))

    # Check if Hadar Institute is still valid
    org_reports = status.get("organization_reports", {}).get("organizations", [])
    hadar = next((r for r in org_reports if r["name"] == "Hadar Institute"), None)

    if hadar:
        print("\n" + "=" * 60)
        print("HADAR INSTITUTE CACHE STATUS")
        print("=" * 60)
        print(f"Valid: {hadar.get('valid')}")
        print(f"Cached at: {hadar.get('cached_at')}")
        print(f"Response count: {hadar.get('response_count')}")
        print(f"Current count: {hadar.get('current_count')}")

        if hadar.get("valid"):
            print("\n❌ ERROR: Cache should be EXPIRED but is still VALID!")
        else:
            print("\n✓ SUCCESS: Cache correctly marked as EXPIRED")
    else:
        print("\n⚠️  WARNING: Hadar Institute not found in cache")


if __name__ == "__main__":
    main()
