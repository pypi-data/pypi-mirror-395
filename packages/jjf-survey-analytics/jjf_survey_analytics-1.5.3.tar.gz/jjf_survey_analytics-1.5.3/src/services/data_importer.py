#!/usr/bin/env python3
"""
Data Importer - Import survey data from Google Sheets into normalized database.

Handles reading raw data from Google Sheets and inserting it into the normalized
database schema with proper type detection and deduplication.

Extracted from SurveyNormalizer as part of God class decomposition.
"""

import hashlib
import logging
import threading
from datetime import datetime
from typing import Any, Dict, List, Optional

# Import DataTypeDetector from surveyor utils
from src.surveyor.utils.data_type_detector import DataTypeDetector

logger = logging.getLogger(__name__)


class DataImporter:
    """
    Import raw survey data from Google Sheets into normalized database.

    Responsibilities:
    - Import raw survey data from Google Sheets
    - Parse response data into normalized format
    - Insert data into database tables
    - Handle deduplication via response hashing
    - Track import progress
    - Thread-safe operations
    """

    def __init__(
        self, schema_manager, data_service  # SchemaManager instance  # DataService instance
    ):
        """
        Initialize data importer.

        Args:
            schema_manager: SchemaManager instance for database access
            data_service: DataService instance for Google Sheets data
        """
        self.schema_manager = schema_manager
        self.data_service = data_service
        self.type_detector = DataTypeDetector()
        self._lock = threading.Lock()

        logger.info("DataImporter initialized")

    def import_survey_data(self, survey_name: str, verbose: bool = True) -> Dict[str, int]:
        """
        Import all survey data from Google Sheets for a specific survey.

        Args:
            survey_name: Name of survey tab to import (e.g., 'CEO', 'Tech', 'Staff')
            verbose: Enable verbose logging

        Returns:
            Dictionary with import statistics:
            {
                "responses": number of responses imported,
                "answers": number of answers created,
                "respondents": number of respondents created,
                "duplicates_skipped": number of duplicate responses skipped
            }
        """
        with self._lock:
            if verbose:
                logger.info(f"Starting import for survey: {survey_name}")

            # Get raw data from DataService
            raw_responses = self.data_service.get_tab_data(survey_name)

            if not raw_responses:
                logger.warning(f"No data found for survey: {survey_name}")
                return {"responses": 0, "answers": 0, "respondents": 0, "duplicates_skipped": 0}

            # Create or get survey record
            survey_id = self._ensure_survey_exists(survey_name)

            # Extract question keys from first response
            question_keys = self._extract_question_keys(raw_responses[0])

            # Create question records
            questions_created = self._create_questions(survey_id, question_keys)
            if verbose:
                logger.info(f"Created {questions_created} questions for {survey_name}")

            # Import responses and answers
            stats = {"responses": 0, "answers": 0, "respondents": 0, "duplicates_skipped": 0}

            for response_data in raw_responses:
                result = self._import_single_response(
                    survey_id, response_data, question_keys, verbose=verbose
                )

                if result["imported"]:
                    stats["responses"] += 1
                    stats["answers"] += result["answers_created"]
                    if result["new_respondent"]:
                        stats["respondents"] += 1
                else:
                    stats["duplicates_skipped"] += 1

            if verbose:
                logger.info(
                    f"Import completed for {survey_name}: "
                    f"{stats['responses']} responses, "
                    f"{stats['answers']} answers, "
                    f"{stats['respondents']} new respondents, "
                    f"{stats['duplicates_skipped']} duplicates skipped"
                )

            return stats

    def _ensure_survey_exists(self, survey_name: str) -> int:
        """
        Ensure survey record exists in database.

        Args:
            survey_name: Name of survey

        Returns:
            Survey ID
        """
        with self.schema_manager._get_connection() as conn:
            cursor = conn.cursor()

            # Generate spreadsheet_id from survey name (simplified)
            spreadsheet_id = hashlib.sha256(survey_name.encode()).hexdigest()[:32]

            # Insert survey record (ignore if exists)
            cursor.execute(
                """
                INSERT OR IGNORE INTO surveys
                (survey_name, survey_type, spreadsheet_id, description)
                VALUES (?, ?, ?, ?)
            """,
                (
                    survey_name,
                    survey_name,  # survey_type same as name for simplicity
                    spreadsheet_id,
                    f"Survey data from {survey_name}",
                ),
            )

            # Get survey ID
            cursor.execute(
                """
                SELECT id FROM surveys WHERE spreadsheet_id = ?
            """,
                (spreadsheet_id,),
            )

            result = cursor.fetchone()
            survey_id = result["id"] if isinstance(result, dict) else result[0]

            conn.commit()

            return survey_id

    def _extract_question_keys(self, first_response: Dict[str, Any]) -> List[str]:
        """
        Extract question keys from first response.

        Filters out metadata fields like Date, Browser, Device.

        Args:
            first_response: First response dictionary

        Returns:
            List of question keys
        """
        metadata_fields = {
            "Date",
            "Browser",
            "Device",
            "IP Address",
            "User Agent",
            "Timestamp",
            "Submission Time",
            "Response ID",
            "Organization Name",
        }

        question_keys = [
            key
            for key in first_response.keys()
            if key not in metadata_fields and not key.startswith("_")
        ]

        return question_keys

    def _create_questions(self, survey_id: int, question_keys: List[str]) -> int:
        """
        Create question records for survey.

        Args:
            survey_id: Survey ID
            question_keys: List of question keys

        Returns:
            Number of questions created
        """
        questions_created = 0

        with self.schema_manager._get_connection() as conn:
            cursor = conn.cursor()

            for i, question_key in enumerate(question_keys):
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO survey_questions
                    (survey_id, question_key, question_text, question_order)
                    VALUES (?, ?, ?, ?)
                """,
                    (survey_id, question_key, question_key, i + 1),
                )

                if cursor.rowcount > 0:
                    questions_created += 1

            conn.commit()

        return questions_created

    def _import_single_response(
        self,
        survey_id: int,
        response_data: Dict[str, Any],
        question_keys: List[str],
        verbose: bool = False,
    ) -> Dict[str, Any]:
        """
        Import a single response with deduplication check.

        Args:
            survey_id: Survey ID
            response_data: Response data dictionary
            question_keys: List of question keys
            verbose: Enable verbose logging

        Returns:
            Dictionary with import result:
            {
                "imported": bool,
                "answers_created": int,
                "new_respondent": bool,
                "response_hash": str
            }
        """
        # Calculate response hash for deduplication
        response_hash = self.calculate_response_hash(response_data)

        # Check for duplicate
        if self.check_duplicate(response_hash):
            if verbose:
                logger.debug(f"Skipping duplicate response: {response_hash[:8]}...")
            return {
                "imported": False,
                "answers_created": 0,
                "new_respondent": False,
                "response_hash": response_hash,
            }

        # Get or create respondent
        respondent_id, is_new_respondent = self._get_or_create_respondent(response_data)

        # Parse response date
        response_date = self._parse_response_date(response_data.get("Date", ""))

        # Create response record
        response_id = self._create_response_record(
            survey_id, respondent_id, response_date, response_hash
        )

        # Create answer records
        answers_created = self._create_answer_records(
            response_id, survey_id, response_data, question_keys
        )

        return {
            "imported": True,
            "answers_created": answers_created,
            "new_respondent": is_new_respondent,
            "response_hash": response_hash,
        }

    def calculate_response_hash(self, response_data: Dict[str, Any]) -> str:
        """
        Calculate SHA256 hash for deduplication.

        Hash includes: organization + stakeholder_type + submission_time + answers

        Args:
            response_data: Response data dictionary

        Returns:
            SHA256 hash string (64 characters)
        """
        # Build hash input from key fields
        hash_parts = [
            response_data.get("Organization Name", ""),
            response_data.get("Date", ""),
            response_data.get("Browser", ""),
            response_data.get("Device", ""),
        ]

        # Add all answer values in sorted order for consistency
        answer_keys = sorted(
            [
                k
                for k in response_data.keys()
                if k not in {"Date", "Browser", "Device", "IP Address", "User Agent"}
                and not k.startswith("_")
            ]
        )

        for key in answer_keys:
            hash_parts.append(str(response_data.get(key, "")))

        # Combine and hash
        hash_input = "|".join(hash_parts)
        return hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    def check_duplicate(self, response_hash: str) -> bool:
        """
        Check if response with this hash already exists.

        Args:
            response_hash: Response hash to check

        Returns:
            True if duplicate exists, False otherwise
        """
        with self.schema_manager._get_connection() as conn:
            conn.cursor()

            # Check if any response has this hash
            # Note: response_hash stored in survey_responses table would require schema change
            # For now, we'll check by looking for exact match in source_row_id or skip
            # In production, add response_hash column to survey_responses table

            # Simplified check: assume no duplicates for now
            # TODO: Add response_hash column to schema for proper deduplication
            return False

    def _get_or_create_respondent(self, response_data: Dict[str, Any]) -> tuple[int, bool]:
        """
        Get existing respondent or create new one.

        Args:
            response_data: Response data dictionary

        Returns:
            Tuple of (respondent_id, is_new_respondent)
        """
        respondent_hash = self._create_respondent_hash(response_data)

        with self.schema_manager._get_connection() as conn:
            cursor = conn.cursor()

            # Try to get existing respondent
            cursor.execute(
                """
                SELECT id FROM respondents WHERE respondent_hash = ?
            """,
                (respondent_hash,),
            )

            result = cursor.fetchone()

            if result:
                # Existing respondent
                respondent_id = result["id"] if isinstance(result, dict) else result[0]

                # Update last response date and count
                response_date = self._parse_response_date(response_data.get("Date", ""))
                cursor.execute(
                    """
                    UPDATE respondents
                    SET last_response_date = ?,
                        total_responses = total_responses + 1
                    WHERE id = ?
                """,
                    (response_date, respondent_id),
                )

                conn.commit()
                return (respondent_id, False)
            else:
                # Create new respondent
                response_date = self._parse_response_date(response_data.get("Date", ""))

                cursor.execute(
                    """
                    INSERT INTO respondents
                    (respondent_hash, browser, device, first_response_date,
                     last_response_date, total_responses)
                    VALUES (?, ?, ?, ?, ?, 1)
                """,
                    (
                        respondent_hash,
                        response_data.get("Browser", ""),
                        response_data.get("Device", ""),
                        response_date,
                        response_date,
                    ),
                )

                respondent_id = cursor.lastrowid
                conn.commit()

                return (respondent_id, True)

    def _create_respondent_hash(self, response_data: Dict[str, Any]) -> str:
        """
        Create a hash to identify unique respondents.

        Uses browser, device, and date (not time) to identify respondents.

        Args:
            response_data: Response data dictionary

        Returns:
            Hash string (16 characters)
        """
        identifier_parts = [
            response_data.get("Browser", ""),
            response_data.get("Device", ""),
            response_data.get("Date", "")[:10] if response_data.get("Date") else "",
        ]

        identifier_string = "|".join(identifier_parts)
        return hashlib.sha256(identifier_string.encode()).hexdigest()[:16]

    def _parse_response_date(self, date_string: str) -> Optional[datetime]:
        """
        Parse various date formats from the survey data.

        Args:
            date_string: Date string to parse

        Returns:
            Datetime object or None if parsing fails
        """
        if not date_string:
            return None

        date_formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%m/%d/%Y %H:%M:%S",
            "%m/%d/%Y %H:%M",
            "%Y-%m-%d",
            "%m/%d/%Y",
        ]

        for fmt in date_formats:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue

        logger.warning(f"Could not parse date: {date_string}")
        return None

    def _create_response_record(
        self,
        survey_id: int,
        respondent_id: int,
        response_date: Optional[datetime],
        response_hash: str,
    ) -> int:
        """
        Create survey response record.

        Args:
            survey_id: Survey ID
            respondent_id: Respondent ID
            response_date: Response date (can be None)
            response_hash: Response hash for deduplication

        Returns:
            Response ID
        """
        with self.schema_manager._get_connection() as conn:
            cursor = conn.cursor()

            # Use current time if response_date is None
            effective_date = response_date or datetime.now()

            cursor.execute(
                """
                INSERT INTO survey_responses
                (survey_id, respondent_id, response_date, completion_status)
                VALUES (?, ?, ?, 'complete')
            """,
                (survey_id, respondent_id, effective_date),
            )

            response_id = cursor.lastrowid
            conn.commit()

            return response_id

    def _create_answer_records(
        self,
        response_id: int,
        survey_id: int,
        response_data: Dict[str, Any],
        question_keys: List[str],
    ) -> int:
        """
        Create answer records for a response.

        Args:
            response_id: Response ID
            survey_id: Survey ID
            response_data: Response data dictionary
            question_keys: List of question keys

        Returns:
            Number of answers created
        """
        answers_created = 0

        with self.schema_manager._get_connection() as conn:
            cursor = conn.cursor()

            for question_key in question_keys:
                # Get question ID
                cursor.execute(
                    """
                    SELECT id FROM survey_questions
                    WHERE survey_id = ? AND question_key = ?
                """,
                    (survey_id, question_key),
                )

                question_result = cursor.fetchone()
                if not question_result:
                    continue

                question_id = (
                    question_result["id"]
                    if isinstance(question_result, dict)
                    else question_result[0]
                )

                # Get answer value
                answer_value = response_data.get(question_key, "")

                # Use DataTypeDetector to parse answer
                typed_answer = self.type_detector.detect_and_convert(answer_value)

                # Insert answer
                cursor.execute(
                    """
                    INSERT INTO survey_answers
                    (response_id, question_id, answer_text, answer_numeric,
                     answer_boolean, answer_date, is_empty)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        response_id,
                        question_id,
                        typed_answer["text_value"],
                        typed_answer["numeric_value"],
                        typed_answer["boolean_value"],
                        typed_answer["date_value"],
                        not bool(answer_value),
                    ),
                )

                answers_created += 1

            conn.commit()

        return answers_created


def get_data_importer(schema_manager, data_service) -> DataImporter:
    """
    Factory function to get DataImporter instance.

    Args:
        schema_manager: SchemaManager instance
        data_service: DataService instance

    Returns:
        DataImporter instance
    """
    return DataImporter(schema_manager, data_service)
