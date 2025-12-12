#!/usr/bin/env python3
"""
Data Type Detection and Parsing Utilities.

Provides static methods for automatic type detection and parsing of survey answer data.
Extracted from SurveyNormalizer to provide reusable type detection logic.

Thread-safe by design (all static methods, no shared state).
"""

import re
from datetime import datetime
from typing import Any, Optional, Tuple


class DataTypeDetector:
    """
    Utility class for detecting and parsing survey answer data types.

    Handles automatic detection of:
    - Numeric values (integers, floats, percentages, ratings)
    - Boolean values (Yes/No, True/False, 1/0)
    - Date values (various formats)
    - Text values (fallback)

    All methods are static - no state, fully thread-safe.
    """

    @staticmethod
    def detect_type(value: Any) -> str:
        """
        Detect the data type of a value.

        Type detection priority:
        1. Boolean (Yes/No, True/False, 1/0)
        2. Numeric (integers, floats, percentages)
        3. Date (various date formats)
        4. Text (fallback)

        Args:
            value: Value to detect type for

        Returns:
            One of: 'boolean', 'numeric', 'date', 'text'
        """
        if value is None or value == "":
            return "text"

        # Try boolean first (most specific)
        if DataTypeDetector.parse_boolean(value) is not None:
            return "boolean"

        # Try numeric
        if DataTypeDetector.parse_numeric(value) is not None:
            return "numeric"

        # Try date
        if DataTypeDetector.parse_date(value) is not None:
            return "date"

        # Default to text
        return "text"

    @staticmethod
    def parse_numeric(value: Any) -> Optional[float]:
        """
        Parse numeric value from text or number.

        Handles:
        - Integers and floats
        - Percentages (strips %)
        - Ratings (1-5 scale)
        - Negative numbers
        - Numbers with commas (1,000)

        Args:
            value: Value to parse as numeric

        Returns:
            Float value or None if not numeric
        """
        if value is None or value == "":
            return None

        # If already a number, return it
        if isinstance(value, (int, float)):
            return float(value)

        # Convert to string and clean
        str_value = str(value).strip()

        if not str_value:
            return None

        try:
            # Remove common formatting
            cleaned = str_value.replace(",", "").replace("$", "").replace("%", "")

            # Check if it's a valid number pattern
            # Matches: -123, 123, 123.45, -123.45
            if re.match(r"^-?\d*\.?\d+$", cleaned):
                return float(cleaned)
        except (ValueError, AttributeError):
            pass

        return None

    @staticmethod
    def parse_boolean(value: Any) -> Optional[bool]:
        """
        Parse boolean value from text.

        Handles (case-insensitive):
        - Yes/No
        - True/False
        - Y/N
        - 1/0
        - On/Off

        Args:
            value: Value to parse as boolean

        Returns:
            True/False or None if not boolean
        """
        if value is None or value == "":
            return None

        # Boolean patterns (case-insensitive)
        boolean_patterns = {
            "true": True,
            "false": False,
            "yes": True,
            "no": False,
            "y": True,
            "n": False,
            "1": True,
            "0": False,
            "on": True,
            "off": False,
        }

        try:
            str_value = str(value).strip().lower()
            return boolean_patterns.get(str_value)
        except (AttributeError, ValueError):
            return None

    @staticmethod
    def parse_date(value: Any) -> Optional[str]:
        """
        Parse date from various formats.

        Handles:
        - ISO dates (YYYY-MM-DD)
        - US dates (MM/DD/YYYY)
        - Other common formats

        Args:
            value: Value to parse as date

        Returns:
            ISO format date string (YYYY-MM-DD) or None if not a date
        """
        if value is None or value == "":
            return None

        # If already a datetime object
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d")

        str_value = str(value).strip()

        if not str_value:
            return None

        # Date format patterns to try
        date_formats = [
            "%Y-%m-%d",  # ISO: 2025-11-12
            "%m/%d/%Y",  # US: 11/12/2025
            "%m-%d-%Y",  # US with dashes: 11-12-2025
            "%d/%m/%Y",  # European: 12/11/2025
            "%Y/%m/%d",  # ISO with slashes
            "%m/%d/%y",  # Short year: 11/12/25
        ]

        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(str_value, fmt)
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                continue

        return None

    @staticmethod
    def parse_value(
        value: Any, expected_type: Optional[str] = None
    ) -> Tuple[Any, str, Optional[float]]:
        """
        Parse value and return (parsed_value, type, numeric_value).

        This is the primary method for parsing survey answers. It detects the type
        and returns both the original value and a numeric representation if applicable.

        Args:
            value: Value to parse
            expected_type: Optional type hint ('numeric', 'boolean', 'date', 'text')

        Returns:
            Tuple of:
            - parsed_value: The parsed value (original or converted)
            - detected_type: Detected type string
            - numeric_value: Numeric representation (for booleans: 1.0/0.0, for numbers: the value)
        """
        if value is None or value == "":
            return (None, "text", None)

        # Detect type if not provided
        detected_type = expected_type if expected_type else DataTypeDetector.detect_type(value)

        # Parse based on detected type
        if detected_type == "boolean":
            bool_val = DataTypeDetector.parse_boolean(value)
            if bool_val is not None:
                # Return boolean with numeric representation
                numeric_val = 1.0 if bool_val else 0.0
                return (str(value), detected_type, numeric_val)

        elif detected_type == "numeric":
            numeric_val = DataTypeDetector.parse_numeric(value)
            if numeric_val is not None:
                return (str(value), detected_type, numeric_val)

        elif detected_type == "date":
            date_val = DataTypeDetector.parse_date(value)
            if date_val is not None:
                return (date_val, detected_type, None)

        # Default to text
        return (str(value), "text", None)
