#!/usr/bin/env python3
"""
Google Sheets Tab Names Configuration

Single source of truth for all Google Sheets tab names used throughout the application.
Using Enum ensures type safety and prevents typos like "Staff" vs "Staf".

CRITICAL: These names MUST match the actual tab names in Google Sheets.
DO NOT change these values unless the Google Sheets tabs are also renamed.
"""

from enum import Enum


class SheetTab(str, Enum):
    """
    Google Sheets tab names.

    Inherits from str to allow direct string comparison and usage in dict keys.

    Example:
        >>> tab_name = SheetTab.STAFF
        >>> data = sheets_data.get(tab_name)
        >>> assert tab_name == "Staff"  # Works because Enum inherits from str
    """

    # Core survey tabs
    SUMMARY = "Summary"
    INTAKE = "Intake"
    CEO = "CEO"
    TECH = "Tech"
    STAFF = "Staff"  # ⚠️ CRITICAL: Actual tab name is "Staff" (not "Staf")

    # Reference tabs
    QUESTIONS = "Questions"
    KEY = "Key"
    ORG_MASTER = "OrgMaster"


# Tab GID mapping (for CSV export URLs)
TAB_GIDS = {
    SheetTab.SUMMARY: "0",
    SheetTab.INTAKE: "1366958616",
    SheetTab.CEO: "1242252865",
    SheetTab.TECH: "1545410106",
    SheetTab.STAFF: "377168987",  # ⚠️ Staff survey (not "Staf")
    SheetTab.QUESTIONS: "513349220",
    SheetTab.KEY: "1000323612",
    SheetTab.ORG_MASTER: "601687640",
}


# Organization field mappings per tab
ORG_FIELD_MAP = {
    SheetTab.INTAKE: "Organization Name:",
    SheetTab.CEO: "CEO Organization",
    SheetTab.TECH: "Organization",
    SheetTab.STAFF: "Organization",
}


# Question ID prefixes per survey type
QUESTION_PREFIXES = {
    SheetTab.CEO: "C-",
    SheetTab.TECH: "TL-",
    SheetTab.STAFF: "S-",
}


def get_tab_gid(tab: SheetTab) -> str:
    """
    Get the GID for a given tab.

    Args:
        tab: SheetTab enum value

    Returns:
        GID string for the tab

    Example:
        >>> get_tab_gid(SheetTab.STAFF)
        '377168987'
    """
    return TAB_GIDS[tab]


def get_org_field(tab: SheetTab) -> str:
    """
    Get the organization field name for a given tab.

    Args:
        tab: SheetTab enum value

    Returns:
        Field name that contains organization name in that tab

    Example:
        >>> get_org_field(SheetTab.STAFF)
        'Organization'
    """
    return ORG_FIELD_MAP.get(tab, "Organization")


def get_question_prefix(tab: SheetTab) -> str:
    """
    Get the question ID prefix for a given survey tab.

    Args:
        tab: SheetTab enum value

    Returns:
        Question ID prefix (e.g., "C-" for CEO)

    Example:
        >>> get_question_prefix(SheetTab.STAFF)
        'S-'
    """
    return QUESTION_PREFIXES.get(tab, "")


def validate_tab_name(name: str) -> bool:
    """
    Validate that a tab name exists in our enum.

    Args:
        name: String tab name to validate

    Returns:
        True if valid, False otherwise

    Example:
        >>> validate_tab_name("Staff")
        True
        >>> validate_tab_name("Staf")
        False
    """
    try:
        SheetTab(name)
        return True
    except ValueError:
        return False


# Export all for easy importing
__all__ = [
    'SheetTab',
    'TAB_GIDS',
    'ORG_FIELD_MAP',
    'QUESTION_PREFIXES',
    'get_tab_gid',
    'get_org_field',
    'get_question_prefix',
    'validate_tab_name',
]
