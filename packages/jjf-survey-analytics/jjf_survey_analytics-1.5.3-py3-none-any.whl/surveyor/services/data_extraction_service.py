"""
Data extraction and normalization service.

This service coordinates the extraction of data from Google Sheets
and normalizes it into the database.
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, List, Optional

from ..models.models import DataExtractionJob, Sheet, SheetCell, SheetColumn, SheetRow, Spreadsheet
from ..repositories.spreadsheet_repository import (
    DataExtractionJobRepository,
    SheetCellRepository,
    SheetColumnRepository,
    SheetRepository,
    SheetRowRepository,
    SpreadsheetRepository,
)
from ..utils.data_type_detector import DataTypeDetector
from .google_sheets_service import IGoogleSheetsService, SheetData

logger = logging.getLogger(__name__)


class IDataExtractionService(ABC):
    """Interface for data extraction service."""

    @abstractmethod
    def extract_and_normalize(
        self, urls: List[str], job_name: Optional[str] = None
    ) -> DataExtractionJob:
        """Extract data from URLs and normalize into database."""


class DataExtractionService(IDataExtractionService):
    """Service for extracting and normalizing Google Sheets data."""

    def __init__(
        self,
        sheets_service: IGoogleSheetsService,
        spreadsheet_repo: SpreadsheetRepository,
        sheet_repo: SheetRepository,
        column_repo: SheetColumnRepository,
        row_repo: SheetRowRepository,
        cell_repo: SheetCellRepository,
        job_repo: DataExtractionJobRepository,
    ):
        self.sheets_service = sheets_service
        self.spreadsheet_repo = spreadsheet_repo
        self.sheet_repo = sheet_repo
        self.column_repo = column_repo
        self.row_repo = row_repo
        self.cell_repo = cell_repo
        self.job_repo = job_repo
        self.data_type_detector = DataTypeDetector()

    def extract_and_normalize(
        self, urls: List[str], job_name: Optional[str] = None
    ) -> DataExtractionJob:
        """Extract data from URLs and normalize into database."""
        # Create extraction job
        job = DataExtractionJob(
            job_name=job_name or f"Extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            status="running",
            spreadsheet_urls=urls,
            started_at=datetime.utcnow(),
        )
        job = self.job_repo.create(job)

        try:
            total_sheets = 0
            processed_sheets = 0
            total_rows = 0
            processed_rows = 0

            for url in urls:
                logger.info(f"Processing spreadsheet: {url}")

                try:
                    # Extract spreadsheet ID
                    spreadsheet_id = self.sheets_service.extract_spreadsheet_id(url)

                    # Get or create spreadsheet record
                    spreadsheet = self.spreadsheet_repo.get_by_spreadsheet_id(spreadsheet_id)
                    if not spreadsheet:
                        spreadsheet = Spreadsheet(
                            spreadsheet_id=spreadsheet_id,
                            url=url,
                            title=f"Spreadsheet_{spreadsheet_id}",
                        )
                        spreadsheet = self.spreadsheet_repo.create(spreadsheet)

                    # Get sheet data
                    sheet_data_list = self.sheets_service.get_sheet_data(url)
                    total_sheets += len(sheet_data_list)

                    for sheet_data in sheet_data_list:
                        logger.info(f"Processing sheet: {sheet_data.sheet_name}")

                        # Process sheet
                        rows_processed = self._process_sheet(spreadsheet, sheet_data)
                        total_rows += len(sheet_data.values)
                        processed_rows += rows_processed
                        processed_sheets += 1

                        # Update job progress
                        job.processed_sheets = processed_sheets
                        job.processed_rows = processed_rows
                        job.total_sheets = total_sheets
                        job.total_rows = total_rows
                        self.job_repo.update(job)

                except Exception as e:
                    logger.error(f"Error processing spreadsheet {url}: {e}")
                    # Continue with other spreadsheets
                    continue

            # Mark job as completed
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            job.total_sheets = total_sheets
            job.total_rows = total_rows
            job.processed_sheets = processed_sheets
            job.processed_rows = processed_rows

        except Exception as e:
            logger.error(f"Error in extraction job: {e}")
            job.status = "failed"
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()

        return self.job_repo.update(job)

    def _process_sheet(self, spreadsheet: Spreadsheet, sheet_data: SheetData) -> int:
        """Process a single sheet and return number of rows processed."""
        # Get or create sheet record
        sheet = self.sheet_repo.get_by_spreadsheet_and_name(spreadsheet.id, sheet_data.sheet_name)

        if not sheet:
            sheet = Sheet(
                name=sheet_data.sheet_name,
                spreadsheet_id=spreadsheet.id,
                row_count=len(sheet_data.values),
                column_count=len(sheet_data.headers),
            )
            sheet = self.sheet_repo.create(sheet)
        else:
            # Update counts
            sheet.row_count = len(sheet_data.values)
            sheet.column_count = len(sheet_data.headers)
            sheet = self.sheet_repo.update(sheet)

        # Process columns
        columns = self._process_columns(sheet, sheet_data.headers)

        # Process rows and cells
        return self._process_rows_and_cells(sheet, columns, sheet_data.values)

    def _process_columns(self, sheet: Sheet, headers: List[str]) -> List[SheetColumn]:
        """Process column headers and return column objects."""
        columns = []

        for index, header in enumerate(headers):
            column = self.column_repo.get_by_sheet_and_name(sheet.id, header)

            if not column:
                column = SheetColumn(
                    sheet_id=sheet.id,
                    name=header,
                    column_index=index,
                    data_type="text",  # Will be updated based on data
                )
                column = self.column_repo.create(column)

            columns.append(column)

        return columns

    def _process_rows_and_cells(
        self, sheet: Sheet, columns: List[SheetColumn], rows_data: List[List[Any]]
    ) -> int:
        """Process rows and cells data."""
        processed_count = 0

        for row_index, row_data in enumerate(rows_data):
            # Create or get row
            row = SheetRow(sheet_id=sheet.id, row_index=row_index)
            row = self.row_repo.create(row)

            # Create cells for this row
            cells_to_create = []

            for col_index, cell_value in enumerate(row_data):
                if col_index < len(columns):
                    column = columns[col_index]

                    # Detect data type and convert value
                    typed_values = self.data_type_detector.detect_and_convert(cell_value)

                    cell = SheetCell(
                        sheet_id=sheet.id,
                        row_id=row.id,
                        column_id=column.id,
                        raw_value=str(cell_value) if cell_value is not None else None,
                        **typed_values,
                    )
                    cells_to_create.append(cell)

            # Bulk create cells for better performance
            if cells_to_create:
                self.cell_repo.bulk_create(cells_to_create)

            processed_count += 1

        return processed_count
