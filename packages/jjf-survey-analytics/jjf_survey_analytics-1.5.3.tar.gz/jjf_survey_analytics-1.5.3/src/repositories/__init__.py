"""
Repositories package for data persistence abstraction.

Provides repository pattern implementation for:
- SheetRepository: Google Sheets data access
- ReportRepository: JSON report file persistence
- AdminEditRepository: Admin edits JSON persistence

Usage:
    from src.repositories import get_sheet_repository, get_report_repository

    sheet_repo = get_sheet_repository()
    report_repo = get_report_repository()
"""

from src.repositories.admin_edit_repository import AdminEditRepository, get_admin_edit_repository
from src.repositories.report_repository import ReportRepository, get_report_repository
from src.repositories.sheet_repository import SheetRepository, get_sheet_repository

__all__ = [
    "SheetRepository",
    "get_sheet_repository",
    "ReportRepository",
    "get_report_repository",
    "AdminEditRepository",
    "get_admin_edit_repository",
]
