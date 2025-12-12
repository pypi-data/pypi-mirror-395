"""
JJF Survey Analytics Platform - Version Information
Auto-generated version tracking with build metadata
"""

import datetime
import os
import subprocess
from typing import Dict, Optional

__version__ = "1.5.3"
__build_date__ = "2025-12-03T13:06:32.027709"
__build_number__ = None
__git_commit__ = "94b6319"
__git_branch__ = "main"


def get_git_info() -> Dict[str, Optional[str]]:
    """Get current git information."""
    try:
        commit = (
            subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL
            )
            .decode("utf-8")
            .strip()
        )

        branch = (
            subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"], stderr=subprocess.DEVNULL
            )
            .decode("utf-8")
            .strip()
        )

        return {"commit": commit, "branch": branch}
    except Exception:
        return {"commit": None, "branch": None}


def get_version_info() -> Dict[str, any]:
    """Get complete version information."""
    git_info = get_git_info()

    return {
        "version": __version__,
        "build_date": __build_date__ or datetime.datetime.now().isoformat(),
        "build_number": __build_number__,
        "git_commit": __git_commit__ or git_info["commit"],
        "git_branch": __git_branch__ or git_info["branch"],
        "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
    }


def get_version_string() -> str:
    """Get formatted version string."""
    info = get_version_info()
    parts = [f"v{info['version']}"]

    if info["git_commit"]:
        parts.append(f"({info['git_commit']})")

    if info["build_number"]:
        parts.append(f"build.{info['build_number']}")

    return " ".join(parts)


def print_version_info():
    """Print detailed version information."""
    info = get_version_info()
    print("═" * 60)
    print("JJF Survey Analytics Platform")
    print("═" * 60)
    print(f"Version:        {info['version']}")
    print(f"Build Date:     {info['build_date']}")
    if info["build_number"]:
        print(f"Build Number:   {info['build_number']}")
    if info["git_commit"]:
        print(f"Git Commit:     {info['git_commit']}")
    if info["git_branch"]:
        print(f"Git Branch:     {info['git_branch']}")
    print(f"Python:         {info['python_version']}")
    print("═" * 60)


if __name__ == "__main__":
    print_version_info()
