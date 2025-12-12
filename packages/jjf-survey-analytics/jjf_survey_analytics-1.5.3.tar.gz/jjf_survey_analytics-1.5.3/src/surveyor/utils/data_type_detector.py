"""
Data type detection and conversion utilities.
"""

import logging
import re
from datetime import datetime
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class DataTypeDetector:
    """Utility class for detecting and converting data types."""

    def __init__(self):
        # Regex patterns for different data types
        self.date_patterns = [
            r"\d{4}-\d{2}-\d{2}",  # YYYY-MM-DD
            r"\d{2}/\d{2}/\d{4}",  # MM/DD/YYYY
            r"\d{2}-\d{2}-\d{4}",  # MM-DD-YYYY
            r"\d{1,2}/\d{1,2}/\d{4}",  # M/D/YYYY
        ]

        self.number_pattern = r"^-?\d*\.?\d+$"
        self.boolean_patterns = {
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

    def detect_and_convert(self, value: Any) -> Dict[str, Any]:
        """
        Detect data type and convert value to appropriate typed fields.

        Returns a dictionary with typed values for database storage.
        """
        result = {
            "text_value": None,
            "numeric_value": None,
            "boolean_value": None,
            "date_value": None,
        }

        if value is None or value == "":
            return result

        # Convert to string for processing
        str_value = str(value).strip()
        result["text_value"] = str_value

        # Try to detect and convert to specific types

        # Boolean detection
        boolean_val = self._try_convert_boolean(str_value)
        if boolean_val is not None:
            result["boolean_value"] = boolean_val
            return result

        # Numeric detection
        numeric_val = self._try_convert_numeric(str_value)
        if numeric_val is not None:
            result["numeric_value"] = numeric_val
            return result

        # Date detection
        date_val = self._try_convert_date(str_value)
        if date_val is not None:
            result["date_value"] = date_val
            return result

        # Default to text
        return result

    def _try_convert_boolean(self, value: str) -> Optional[bool]:
        """Try to convert value to boolean."""
        try:
            lower_val = value.lower()
            return self.boolean_patterns.get(lower_val)
        except Exception:
            return None

    def _try_convert_numeric(self, value: str) -> Optional[float]:
        """Try to convert value to numeric."""
        try:
            # Remove common formatting
            cleaned = value.replace(",", "").replace("$", "").replace("%", "")

            if re.match(self.number_pattern, cleaned):
                return float(cleaned)
        except Exception:
            pass
        return None

    def _try_convert_date(self, value: str) -> Optional[datetime]:
        """Try to convert value to date."""
        for pattern in self.date_patterns:
            if re.match(pattern, value):
                try:
                    # Try different date formats
                    date_formats = [
                        "%Y-%m-%d",
                        "%m/%d/%Y",
                        "%m-%d-%Y",
                        "%m/%d/%y",
                        "%d/%m/%Y",
                        "%Y/%m/%d",
                    ]

                    for fmt in date_formats:
                        try:
                            return datetime.strptime(value, fmt)
                        except ValueError:
                            continue

                except Exception as e:
                    logger.debug(f"Failed to parse date {value}: {e}")
                    continue

        return None

    def detect_column_type(self, values: list) -> str:
        """
        Detect the most appropriate data type for a column based on its values.

        Returns: 'boolean', 'numeric', 'date', or 'text'
        """
        if not values:
            return "text"

        # Remove empty values for analysis
        non_empty_values = [v for v in values if v is not None and str(v).strip() != ""]

        if not non_empty_values:
            return "text"

        # Count successful conversions for each type
        boolean_count = 0
        numeric_count = 0
        date_count = 0

        for value in non_empty_values:
            str_val = str(value).strip()

            if self._try_convert_boolean(str_val) is not None:
                boolean_count += 1
            elif self._try_convert_numeric(str_val) is not None:
                numeric_count += 1
            elif self._try_convert_date(str_val) is not None:
                date_count += 1

        total_count = len(non_empty_values)

        # If 80% or more values can be converted to a specific type, use that type
        threshold = 0.8

        if boolean_count / total_count >= threshold:
            return "boolean"
        elif numeric_count / total_count >= threshold:
            return "numeric"
        elif date_count / total_count >= threshold:
            return "date"
        else:
            return "text"
