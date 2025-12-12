"""
Google Sheets service for fetching data from Google Spreadsheets.
"""

import logging
import os
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Optional

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

from ..config.settings import GoogleSheetsConfig

logger = logging.getLogger(__name__)


@dataclass
class SheetData:
    """Container for sheet data."""

    spreadsheet_id: str
    sheet_name: str
    values: List[List[Any]]
    headers: List[str]


class IGoogleSheetsService(ABC):
    """Interface for Google Sheets service."""

    @abstractmethod
    def get_sheet_data(self, url: str, sheet_name: Optional[str] = None) -> List[SheetData]:
        """Get data from a Google Sheet."""

    @abstractmethod
    def extract_spreadsheet_id(self, url: str) -> str:
        """Extract spreadsheet ID from Google Sheets URL."""


class GoogleSheetsService(IGoogleSheetsService):
    """Service for interacting with Google Sheets API."""

    def __init__(self, config: GoogleSheetsConfig):
        if not GOOGLE_AVAILABLE:
            raise ImportError(
                "Google API client libraries not available. "
                "Install with: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib"
            )

        self.config = config
        self._service = None
        self._credentials = None

    def _get_credentials(self) -> Credentials:
        """Get Google API credentials."""
        if self._credentials:
            return self._credentials

        creds = None
        token_file = "token.json"

        # Load existing token
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, self.config.scopes)

        # If there are no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not self.config.credentials_file:
                    raise ValueError(
                        "Google credentials file not configured. "
                        "Set GOOGLE_CREDENTIALS_FILE environment variable or provide credentials.json"
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.config.credentials_file, self.config.scopes
                )
                creds = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(token_file, "w") as token:
                token.write(creds.to_json())

        self._credentials = creds
        return creds

    def _get_service(self):
        """Get Google Sheets service."""
        if not self._service:
            creds = self._get_credentials()
            self._service = build("sheets", "v4", credentials=creds)
        return self._service

    def extract_spreadsheet_id(self, url: str) -> str:
        """Extract spreadsheet ID from Google Sheets URL."""
        # Pattern to match Google Sheets URLs
        pattern = r"/spreadsheets/d/([a-zA-Z0-9-_]+)"
        match = re.search(pattern, url)

        if not match:
            raise ValueError(f"Invalid Google Sheets URL: {url}")

        return match.group(1)

    def get_sheet_data(self, url: str, sheet_name: Optional[str] = None) -> List[SheetData]:
        """Get data from a Google Sheet."""
        try:
            spreadsheet_id = self.extract_spreadsheet_id(url)
            service = self._get_service()

            # Get spreadsheet metadata to find all sheets
            spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            sheets = spreadsheet.get("sheets", [])

            result = []

            # If specific sheet name provided, filter to that sheet
            if sheet_name:
                sheets = [s for s in sheets if s["properties"]["title"] == sheet_name]
                if not sheets:
                    raise ValueError(f"Sheet '{sheet_name}' not found in spreadsheet")

            for sheet in sheets:
                sheet_title = sheet["properties"]["title"]
                logger.info(f"Fetching data from sheet: {sheet_title}")

                # Get all data from the sheet
                range_name = f"'{sheet_title}'"
                result_data = (
                    service.spreadsheets()
                    .values()
                    .get(spreadsheetId=spreadsheet_id, range=range_name)
                    .execute()
                )

                values = result_data.get("values", [])

                if values:
                    # First row as headers
                    headers = values[0] if values else []
                    data_rows = values[1:] if len(values) > 1 else []

                    # Normalize row lengths to match headers
                    normalized_rows = []
                    for row in data_rows:
                        # Pad row to match header length
                        while len(row) < len(headers):
                            row.append("")
                        normalized_rows.append(row[: len(headers)])  # Trim if longer

                    result.append(
                        SheetData(
                            spreadsheet_id=spreadsheet_id,
                            sheet_name=sheet_title,
                            values=normalized_rows,
                            headers=headers,
                        )
                    )
                else:
                    logger.warning(f"No data found in sheet: {sheet_title}")

            return result

        except HttpError as error:
            logger.error(f"Google Sheets API error: {error}")
            raise
        except Exception as error:
            logger.error(f"Error fetching sheet data: {error}")
            raise


class MockGoogleSheetsService(IGoogleSheetsService):
    """Mock implementation for testing without Google API."""

    def extract_spreadsheet_id(self, url: str) -> str:
        """Extract spreadsheet ID from URL."""
        pattern = r"/spreadsheets/d/([a-zA-Z0-9-_]+)"
        match = re.search(pattern, url)
        if not match:
            raise ValueError(f"Invalid Google Sheets URL: {url}")
        return match.group(1)

    def get_sheet_data(self, url: str, sheet_name: Optional[str] = None) -> List[SheetData]:
        """Return mock data for testing."""
        spreadsheet_id = self.extract_spreadsheet_id(url)

        # Return sample data
        return [
            SheetData(
                spreadsheet_id=spreadsheet_id,
                sheet_name=sheet_name or "Sheet1",
                values=[
                    ["Sample Data 1", "Sample Data 2", "Sample Data 3"],
                    ["Row 2 Col 1", "Row 2 Col 2", "Row 2 Col 3"],
                ],
                headers=["Column 1", "Column 2", "Column 3"],
            )
        ]
