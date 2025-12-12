"""
Repository for spreadsheet-related operations.
"""

import logging
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from ..models.models import DataExtractionJob, Sheet, SheetCell, SheetColumn, SheetRow, Spreadsheet
from .base_repository import BaseRepository

logger = logging.getLogger(__name__)


class SpreadsheetRepository(BaseRepository[Spreadsheet]):
    """Repository for Spreadsheet operations."""

    def __init__(self, session: Session):
        super().__init__(session, Spreadsheet)

    def get_by_spreadsheet_id(self, spreadsheet_id: str) -> Optional[Spreadsheet]:
        """Get spreadsheet by Google Sheets ID."""
        try:
            return (
                self.session.query(Spreadsheet)
                .filter(Spreadsheet.spreadsheet_id == spreadsheet_id)
                .first()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting spreadsheet by ID {spreadsheet_id}: {e}")
            raise

    def get_with_sheets(self, id: int) -> Optional[Spreadsheet]:
        """Get spreadsheet with all its sheets loaded."""
        try:
            return (
                self.session.query(Spreadsheet)
                .options(joinedload(Spreadsheet.sheets))
                .filter(Spreadsheet.id == id)
                .first()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting spreadsheet with sheets for ID {id}: {e}")
            raise


class SheetRepository(BaseRepository[Sheet]):
    """Repository for Sheet operations."""

    def __init__(self, session: Session):
        super().__init__(session, Sheet)

    def get_by_spreadsheet_and_name(self, spreadsheet_id: int, sheet_name: str) -> Optional[Sheet]:
        """Get sheet by spreadsheet ID and name."""
        try:
            return (
                self.session.query(Sheet)
                .filter(Sheet.spreadsheet_id == spreadsheet_id, Sheet.name == sheet_name)
                .first()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting sheet {sheet_name} for spreadsheet {spreadsheet_id}: {e}")
            raise

    def get_with_structure(self, id: int) -> Optional[Sheet]:
        """Get sheet with columns and rows loaded."""
        try:
            return (
                self.session.query(Sheet)
                .options(joinedload(Sheet.columns), joinedload(Sheet.rows))
                .filter(Sheet.id == id)
                .first()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting sheet structure for ID {id}: {e}")
            raise


class SheetColumnRepository(BaseRepository[SheetColumn]):
    """Repository for SheetColumn operations."""

    def __init__(self, session: Session):
        super().__init__(session, SheetColumn)

    def get_by_sheet_and_name(self, sheet_id: int, column_name: str) -> Optional[SheetColumn]:
        """Get column by sheet ID and name."""
        try:
            return (
                self.session.query(SheetColumn)
                .filter(SheetColumn.sheet_id == sheet_id, SheetColumn.name == column_name)
                .first()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting column {column_name} for sheet {sheet_id}: {e}")
            raise

    def get_by_sheet_ordered(self, sheet_id: int) -> List[SheetColumn]:
        """Get all columns for a sheet ordered by column index."""
        try:
            return (
                self.session.query(SheetColumn)
                .filter(SheetColumn.sheet_id == sheet_id)
                .order_by(SheetColumn.column_index)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting ordered columns for sheet {sheet_id}: {e}")
            raise


class SheetRowRepository(BaseRepository[SheetRow]):
    """Repository for SheetRow operations."""

    def __init__(self, session: Session):
        super().__init__(session, SheetRow)

    def get_by_sheet_ordered(self, sheet_id: int) -> List[SheetRow]:
        """Get all rows for a sheet ordered by row index."""
        try:
            return (
                self.session.query(SheetRow)
                .filter(SheetRow.sheet_id == sheet_id)
                .order_by(SheetRow.row_index)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting ordered rows for sheet {sheet_id}: {e}")
            raise


class SheetCellRepository(BaseRepository[SheetCell]):
    """Repository for SheetCell operations."""

    def __init__(self, session: Session):
        super().__init__(session, SheetCell)

    def get_by_row_and_column(self, row_id: int, column_id: int) -> Optional[SheetCell]:
        """Get cell by row and column IDs."""
        try:
            return (
                self.session.query(SheetCell)
                .filter(SheetCell.row_id == row_id, SheetCell.column_id == column_id)
                .first()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting cell for row {row_id}, column {column_id}: {e}")
            raise

    def bulk_create(self, cells: List[SheetCell]) -> List[SheetCell]:
        """Bulk create cells for better performance."""
        try:
            self.session.add_all(cells)
            self.session.commit()
            return cells
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error bulk creating cells: {e}")
            raise


class DataExtractionJobRepository(BaseRepository[DataExtractionJob]):
    """Repository for DataExtractionJob operations."""

    def __init__(self, session: Session):
        super().__init__(session, DataExtractionJob)

    def get_latest_jobs(self, limit: int = 10) -> List[DataExtractionJob]:
        """Get latest extraction jobs."""
        try:
            return (
                self.session.query(DataExtractionJob)
                .order_by(DataExtractionJob.created_at.desc())
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting latest jobs: {e}")
            raise
