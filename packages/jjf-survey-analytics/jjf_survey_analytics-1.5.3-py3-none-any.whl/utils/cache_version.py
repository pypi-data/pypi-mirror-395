"""
Cache version management for report cache invalidation.

This module provides utilities to track cache versions and determine
when cached reports should be invalidated due to:
- Code version changes (git commit)
- Admin edits modifications
- Scoring algorithm changes
"""

import hashlib
import json
import os
from typing import Optional

from .version import get_version_info


def get_file_hash(filepath: str) -> Optional[str]:
    """
    Calculate SHA256 hash of a file.

    Args:
        filepath: Path to file

    Returns:
        Hex digest of file hash, or None if file doesn't exist
    """
    if not os.path.exists(filepath):
        return None

    try:
        with open(filepath, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()[:8]
    except Exception as e:
        print(f"[Cache Version] Error hashing {filepath}: {e}")
        return None


def get_admin_edits_hash() -> str:
    """
    Get hash of admin_edits.json file.

    Returns:
        Hash of admin edits file, or 'none' if file doesn't exist
    """
    admin_edits_file = "admin_edits.json"
    file_hash = get_file_hash(admin_edits_file)
    return file_hash or "none"


def get_cache_version() -> str:
    """
    Generate current cache version identifier.

    The cache version is a composite of:
    - Application version (__version__ from version.py)
    - Git commit hash (code version)
    - Admin edits file hash (configuration changes)

    Returns:
        Cache version string in format: {app_version}_{commit}_{admin_hash}
    """
    version_info = get_version_info()
    app_version = version_info.get("version", "unknown")
    commit = version_info.get("git_commit", "unknown")
    admin_hash = get_admin_edits_hash()

    return f"{app_version}_{commit}_{admin_hash}"


def is_cache_valid(cached_version: Optional[str]) -> bool:
    """
    Check if a cached version is still valid.

    Args:
        cached_version: Version string from cached report

    Returns:
        True if cache is valid, False if it should be regenerated
    """
    if not cached_version:
        return False

    current_version = get_cache_version()
    is_valid = cached_version == current_version

    if not is_valid:
        print(
            f"[Cache Version] Cache invalid - cached: {cached_version}, current: {current_version}"
        )

    return is_valid


def get_cache_metadata() -> dict:
    """
    Get metadata about current cache version.

    Returns:
        Dictionary with cache version and component hashes
    """
    version_info = get_version_info()

    return {
        "cache_version": get_cache_version(),
        "git_commit": version_info.get("git_commit"),
        "git_branch": version_info.get("git_branch"),
        "admin_edits_hash": get_admin_edits_hash(),
        "app_version": version_info.get("version"),
    }


if __name__ == "__main__":
    # Test cache version generation
    print("Current Cache Version:")
    print(json.dumps(get_cache_metadata(), indent=2))
