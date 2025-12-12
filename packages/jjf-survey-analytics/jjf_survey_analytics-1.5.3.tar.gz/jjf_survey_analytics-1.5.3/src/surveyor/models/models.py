"""
Data models for the surveyor application.

These models represent a normalized database schema for storing
data extracted from Google Sheets.
"""

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import BaseModel


class Spreadsheet(BaseModel):
    """Represents a Google Spreadsheet."""

    __tablename__ = "spreadsheets"

    spreadsheet_id = Column(String(255), unique=True, nullable=False, index=True)
    title = Column(String(500))
    url = Column(Text)
    last_synced = Column(DateTime)

    # Relationships
    sheets = relationship("Sheet", back_populates="spreadsheet", cascade="all, delete-orphan")


class Sheet(BaseModel):
    """Represents a sheet within a spreadsheet."""

    __tablename__ = "sheets"

    name = Column(String(255), nullable=False)
    spreadsheet_id = Column(Integer, ForeignKey("spreadsheets.id"), nullable=False)
    sheet_index = Column(Integer)
    row_count = Column(Integer, default=0)
    column_count = Column(Integer, default=0)

    # Relationships
    spreadsheet = relationship("Spreadsheet", back_populates="sheets")
    columns = relationship("SheetColumn", back_populates="sheet", cascade="all, delete-orphan")
    rows = relationship("SheetRow", back_populates="sheet", cascade="all, delete-orphan")


class SheetColumn(BaseModel):
    """Represents a column in a sheet."""

    __tablename__ = "sheet_columns"

    sheet_id = Column(Integer, ForeignKey("sheets.id"), nullable=False)
    name = Column(String(255), nullable=False)
    column_index = Column(Integer, nullable=False)
    data_type = Column(String(50))  # text, number, date, boolean, etc.

    # Relationships
    sheet = relationship("Sheet", back_populates="columns")
    cells = relationship("SheetCell", back_populates="column", cascade="all, delete-orphan")


class SheetRow(BaseModel):
    """Represents a row in a sheet."""

    __tablename__ = "sheet_rows"

    sheet_id = Column(Integer, ForeignKey("sheets.id"), nullable=False)
    row_index = Column(Integer, nullable=False)

    # Relationships
    sheet = relationship("Sheet", back_populates="rows")
    cells = relationship("SheetCell", back_populates="row", cascade="all, delete-orphan")


class SheetCell(BaseModel):
    """Represents a cell in a sheet."""

    __tablename__ = "sheet_cells"

    sheet_id = Column(Integer, ForeignKey("sheets.id"), nullable=False)
    row_id = Column(Integer, ForeignKey("sheet_rows.id"), nullable=False)
    column_id = Column(Integer, ForeignKey("sheet_columns.id"), nullable=False)

    # Store the raw value and typed values
    raw_value = Column(Text)
    text_value = Column(Text)
    numeric_value = Column(Float)
    boolean_value = Column(Boolean)
    date_value = Column(DateTime)

    # Relationships
    row = relationship("SheetRow", back_populates="cells")
    column = relationship("SheetColumn", back_populates="cells")


class DataExtractionJob(BaseModel):
    """Tracks data extraction jobs."""

    __tablename__ = "data_extraction_jobs"

    job_name = Column(String(255))
    status = Column(String(50))  # pending, running, completed, failed
    spreadsheet_urls = Column(JSON)  # List of URLs processed
    total_sheets = Column(Integer, default=0)
    processed_sheets = Column(Integer, default=0)
    total_rows = Column(Integer, default=0)
    processed_rows = Column(Integer, default=0)
    error_message = Column(Text)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)


class DataValidationError(BaseModel):
    """Stores data validation errors encountered during extraction."""

    __tablename__ = "data_validation_errors"

    job_id = Column(Integer, ForeignKey("data_extraction_jobs.id"))
    spreadsheet_id = Column(String(255))
    sheet_name = Column(String(255))
    row_index = Column(Integer)
    column_name = Column(String(255))
    error_type = Column(String(100))  # type_conversion, missing_required, invalid_format, etc.
    error_message = Column(Text)
    raw_value = Column(Text)

    # Relationship
    job = relationship("DataExtractionJob")
