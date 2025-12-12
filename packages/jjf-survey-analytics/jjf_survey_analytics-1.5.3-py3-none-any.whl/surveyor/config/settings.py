"""
Application settings and configuration.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class DatabaseConfig:
    """Database configuration settings."""

    url: str = "sqlite:///surveyor.db"
    echo: bool = False


@dataclass
class GoogleSheetsConfig:
    """Google Sheets API configuration."""

    credentials_file: Optional[str] = None
    scopes: List[str] = None

    def __post_init__(self):
        if self.scopes is None:
            self.scopes = [
                "https://www.googleapis.com/auth/spreadsheets.readonly",
                "https://www.googleapis.com/auth/drive.readonly",
            ]


@dataclass
class LoggingConfig:
    """Logging configuration."""

    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[str] = None


@dataclass
class AppConfig:
    """Main application configuration."""

    database: DatabaseConfig
    google_sheets: GoogleSheetsConfig
    logging: LoggingConfig

    # Google Sheets URLs to process
    sheet_urls: List[str] = None

    def __post_init__(self):
        if self.sheet_urls is None:
            self.sheet_urls = [
                "https://docs.google.com/spreadsheets/d/1fAAXXGOiDWc8lMVaRwqvuM2CDNAyNY_Px3usyisGhaw/edit?gid=365352546#gid=365352546",
                "https://docs.google.com/spreadsheets/d/1qEHKDVIO4YTR3TjMt336HdKLIBMV2cebAcvdbGOUdCU/edit?usp=sharing",
                "https://docs.google.com/spreadsheets/d/1-aw7gjjvRMQj89lstVBtKDZ67Cs-dO1SHNsp4scJ4II/edit?usp=sharing",
                "https://docs.google.com/spreadsheets/d/1f3NKqhNR-CJr_e6_eLSTLbSFuYY8Gm0dxpSL0mlybMA/edit?usp=sharing",
                "https://docs.google.com/spreadsheets/d/1mQxcZ9U1UsVmHstgWdbHuT7bqfVXV4ZNCr9pn0TlVWM/edit?usp=sharing",
                "https://docs.google.com/spreadsheets/d/1h9AooI-E70v36EOxuErh4uYBg2TLbsF7X5kXdkrUkoQ/edit?usp=sharing",
            ]


def load_config() -> AppConfig:
    """Load configuration from environment variables and defaults."""

    # Database configuration
    db_config = DatabaseConfig(
        url=os.getenv("DATABASE_URL", "sqlite:///surveyor.db"),
        echo=os.getenv("DATABASE_ECHO", "false").lower() == "true",
    )

    # Google Sheets configuration
    credentials_file = os.getenv("GOOGLE_CREDENTIALS_FILE")
    if credentials_file and not Path(credentials_file).exists():
        credentials_file = None

    sheets_config = GoogleSheetsConfig(credentials_file=credentials_file)

    # Logging configuration
    logging_config = LoggingConfig(level=os.getenv("LOG_LEVEL", "INFO"), file=os.getenv("LOG_FILE"))

    return AppConfig(database=db_config, google_sheets=sheets_config, logging=logging_config)
