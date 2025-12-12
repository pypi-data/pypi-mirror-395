#!/usr/bin/env python3
"""
ReportDataExtractor - Pure data extraction and transformation for reports.

Extracts data from DataService and transforms it into report-ready formats.
This class is stateless and focused solely on data transformation - no business
logic, scoring, or report assembly.
"""

import copy
import threading
from collections import defaultdict
from typing import Any, Dict, List, Optional


class ReportDataExtractor:
    """
    Extract and transform survey data for report generation.

    Responsibilities:
    - Extract organization data from DataService
    - Extract responses grouped by stakeholder type
    - Transform data into report-ready formats
    - Group responses by dimension and category
    - Calculate response counts and statistics
    - Extract qualitative/text responses
    - Thread-safe operations with deep copies

    This class is a pure utility - no scoring, no calculations, no report assembly.
    """

    # Stakeholder field mappings for organization name lookup
    _STAKEHOLDER_ORG_FIELDS = {
        "CEO": "CEO Organization",
        "Tech": "Organization",
        "Staff": "Organization",
    }

    # Question ID prefixes by stakeholder type
    _QUESTION_PREFIXES = {"CEO": "C-", "Tech": "TL-", "Staff": "S-"}

    def __init__(self, data_service):
        """
        Initialize report data extractor with data service dependency.

        Args:
            data_service: DataService instance for accessing survey data
        """
        self._data_service = data_service
        self._lock = threading.RLock()

        # Build questions lookup on initialization
        self._questions_lookup = self._build_questions_lookup()

    def _build_questions_lookup(self) -> Dict[str, Dict[str, Any]]:
        """
        Build lookup dictionary for questions and answer keys from data service.

        Returns:
            Dictionary mapping question IDs to question metadata
        """
        questions = {}
        questions_data = self._data_service.get_tab_data("Questions")

        for row in questions_data:
            question_id = row.get("Question ID", "")
            if question_id:
                questions[question_id] = {
                    "question": row.get("QUESTION", ""),
                    "category": row.get("Category", "General"),
                    "answer_keys": {
                        1: row.get("Answer 1", ""),
                        2: row.get("Answer 2", ""),
                        3: row.get("Answer 3", ""),
                        4: row.get("Answer 4", ""),
                        5: row.get("Answer 5", ""),
                        6: row.get("Answer 6", ""),
                        7: row.get("Answer 7", ""),
                    },
                }

        return questions

    def extract_org_data(self, org_name: str) -> Optional[Dict[str, Any]]:
        """
        Extract all data for a specific organization from all tabs.

        Args:
            org_name: Organization name to extract data for

        Returns:
            Dictionary containing:
                - intake_record: Intake data row
                - ceo_record: CEO survey row (or None)
                - tech_records: List of Tech Lead survey rows
                - staff_records: List of Staff survey rows
            Returns None if organization not found in Intake tab

        Thread Safety:
            Returns deep copy of data to prevent mutation
        """
        with self._lock:
            # Get intake record
            intake_data = self._data_service.get_tab_data("Intake")
            intake_record = None
            for row in intake_data:
                if row.get("Organization Name:") == org_name:
                    intake_record = row
                    break

            if not intake_record:
                return None

            # Get CEO record
            ceo_data = self._data_service.get_tab_data("CEO")
            ceo_record = None
            for row in ceo_data:
                if row.get("CEO Organization") == org_name:
                    ceo_record = row
                    break

            # Get Tech records
            tech_data = self._data_service.get_tab_data("Tech")
            tech_records = [row for row in tech_data if row.get("Organization") == org_name]

            # Get Staff records
            staff_data = self._data_service.get_tab_data("Staff")
            staff_records = [row for row in staff_data if row.get("Organization") == org_name]

            return copy.deepcopy(
                {
                    "intake_record": intake_record,
                    "ceo_record": ceo_record,
                    "tech_records": tech_records,
                    "staff_records": staff_records,
                }
            )

    def extract_responses_by_stakeholder(self, org_name: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract responses grouped by stakeholder type (CEO, Tech Lead, Staff).

        Args:
            org_name: Organization name

        Returns:
            Dictionary mapping stakeholder types to lists of response dictionaries:
            {
                'CEO': [response_dict, ...],
                'Tech': [response_dict, ...],
                'Staff': [response_dict, ...]
            }

            Each response dictionary contains:
                - question_id: Question ID (e.g., "C-PT-1")
                - question_text: Full question text
                - answer_value: Raw answer value
                - answer_text: Human-readable answer text
                - respondent: Name of respondent
                - role: Stakeholder type
                - category: Question category/dimension

        Thread Safety:
            Returns deep copy of data to prevent mutation
        """
        with self._lock:
            org_data = self.extract_org_data(org_name)
            if not org_data:
                return {}

            responses_by_stakeholder = {"CEO": [], "Tech": [], "Staff": []}

            # Extract CEO responses
            if org_data["ceo_record"]:
                ceo_responses = self._extract_stakeholder_responses(
                    org_data["ceo_record"], "CEO", org_data["ceo_record"].get("Name", "CEO")
                )
                responses_by_stakeholder["CEO"] = ceo_responses

            # Extract Tech responses
            for tech_record in org_data["tech_records"]:
                tech_responses = self._extract_stakeholder_responses(
                    tech_record, "Tech", tech_record.get("Name", "Tech Lead")
                )
                responses_by_stakeholder["Tech"].extend(tech_responses)

            # Extract Staff responses
            for staff_record in org_data["staff_records"]:
                staff_responses = self._extract_stakeholder_responses(
                    staff_record, "Staff", staff_record.get("Name", "Staff")
                )
                responses_by_stakeholder["Staff"].extend(staff_responses)

            return copy.deepcopy(responses_by_stakeholder)

    def _extract_stakeholder_responses(
        self, record: Dict[str, Any], stakeholder_type: str, respondent_name: str
    ) -> List[Dict[str, Any]]:
        """
        Extract responses from a single stakeholder record.

        Args:
            record: Data record to extract from
            stakeholder_type: Type of stakeholder (CEO, Tech, Staff)
            respondent_name: Name of respondent

        Returns:
            List of response dictionaries
        """
        responses = []
        question_prefix = self._QUESTION_PREFIXES.get(stakeholder_type, "")

        for key, value in record.items():
            if key.startswith(question_prefix) and value:
                question_info = self._questions_lookup.get(key, {})

                response = {
                    "question_id": key,
                    "question_text": question_info.get("question", key),
                    "answer_value": value,
                    "answer_text": self._get_answer_text(value, question_info),
                    "respondent": respondent_name,
                    "role": stakeholder_type,
                    "category": question_info.get("category", "General"),
                }
                responses.append(response)

        return responses

    def extract_dimension_data(
        self, responses: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group responses by dimension/category.

        Args:
            responses: List of response dictionaries (from extract_responses_by_stakeholder)

        Returns:
            Dictionary mapping dimension names to lists of responses:
            {
                'Program Technology': [response1, response2, ...],
                'Business Systems': [...],
                ...
            }

        Thread Safety:
            Returns deep copy of data to prevent mutation
        """
        with self._lock:
            dimension_data = defaultdict(list)

            for response in responses:
                category = response.get("category", "General")
                dimension_data[category].append(response)

            return copy.deepcopy(dict(dimension_data))

    def calculate_response_stats(self, org_name: str) -> Dict[str, Any]:
        """
        Calculate response statistics for an organization.

        Args:
            org_name: Organization name

        Returns:
            Dictionary containing:
                - total_surveys: Expected number of surveys (3)
                - completed_surveys: Number of completed surveys
                - pending_surveys: Number of pending surveys
                - completion_percentage: Completion percentage
                - ceo_complete: Boolean for CEO completion
                - tech_complete: Boolean for Tech completion
                - staff_complete: Boolean for Staff completion
                - ceo_count: Number of CEO responses
                - tech_count: Number of Tech responses
                - staff_count: Number of Staff responses
                - total_response_count: Total responses across all stakeholders

        Thread Safety:
            Returns deep copy of data to prevent mutation
        """
        with self._lock:
            org_data = self.extract_org_data(org_name)
            if not org_data:
                return {
                    "total_surveys": 3,
                    "completed_surveys": 0,
                    "pending_surveys": 3,
                    "completion_percentage": 0,
                    "ceo_complete": False,
                    "tech_complete": False,
                    "staff_complete": False,
                    "ceo_count": 0,
                    "tech_count": 0,
                    "staff_count": 0,
                    "total_response_count": 0,
                }

            # Check completion status
            ceo_complete = bool(org_data["ceo_record"] and org_data["ceo_record"].get("Date"))
            tech_complete = any(r.get("Date") for r in org_data["tech_records"])
            staff_complete = any(r.get("Date") for r in org_data["staff_records"])

            completed_surveys = sum([ceo_complete, tech_complete, staff_complete])
            total_surveys = 3
            completion_percentage = (
                round((completed_surveys / total_surveys) * 100) if total_surveys > 0 else 0
            )

            # Count responses by stakeholder type
            responses_by_stakeholder = self.extract_responses_by_stakeholder(org_name)
            ceo_count = len(responses_by_stakeholder.get("CEO", []))
            tech_count = len(responses_by_stakeholder.get("Tech", []))
            staff_count = len(responses_by_stakeholder.get("Staff", []))

            return copy.deepcopy(
                {
                    "total_surveys": total_surveys,
                    "completed_surveys": completed_surveys,
                    "pending_surveys": total_surveys - completed_surveys,
                    "completion_percentage": completion_percentage,
                    "ceo_complete": ceo_complete,
                    "tech_complete": tech_complete,
                    "staff_complete": staff_complete,
                    "ceo_count": ceo_count,
                    "tech_count": tech_count,
                    "staff_count": staff_count,
                    "total_response_count": ceo_count + tech_count + staff_count,
                }
            )

    def extract_qualitative_responses(self, org_name: str) -> Dict[str, List[str]]:
        """
        Extract qualitative/text responses for AI analysis.

        Filters out numeric responses and extracts only text-based answers.

        Args:
            org_name: Organization name

        Returns:
            Dictionary mapping stakeholder types to lists of text responses:
            {
                'CEO': [text1, text2, ...],
                'Tech': [...],
                'Staff': [...]
            }

        Thread Safety:
            Returns deep copy of data to prevent mutation
        """
        with self._lock:
            responses_by_stakeholder = self.extract_responses_by_stakeholder(org_name)
            qualitative_responses = {"CEO": [], "Tech": [], "Staff": []}

            for stakeholder_type, responses in responses_by_stakeholder.items():
                for response in responses:
                    # Filter out numeric responses
                    if not self._is_numeric_response(response["answer_value"]):
                        text = str(response["answer_value"]).strip()
                        if text and text != "0":
                            qualitative_responses[stakeholder_type].append(text)

            return copy.deepcopy(qualitative_responses)

    def extract_numeric_responses(self, org_name: str) -> Dict[str, Dict[str, float]]:
        """
        Extract numeric responses (ratings 0-5) for maturity scoring.

        Args:
            org_name: Organization name

        Returns:
            Dictionary mapping stakeholder types to question-value mappings:
            {
                'CEO': {'C-PT-1': 4.0, 'C-PT-2': 3.0, ...},
                'Tech': {'TL-BS-1': 5.0, ...},
                'Staff': {'S-DM-1': 2.0, ...}
            }

        Thread Safety:
            Returns deep copy of data to prevent mutation
        """
        with self._lock:
            org_data = self.extract_org_data(org_name)
            if not org_data:
                return {"CEO": {}, "Tech": {}, "Staff": {}}

            numeric_responses = {"CEO": {}, "Tech": {}, "Staff": {}}

            # Extract CEO numeric responses
            if org_data["ceo_record"]:
                numeric_responses["CEO"] = self._extract_numeric_from_record(org_data["ceo_record"])

            # Extract Tech numeric responses (use first record)
            if org_data["tech_records"]:
                numeric_responses["Tech"] = self._extract_numeric_from_record(
                    org_data["tech_records"][0]
                )

            # Extract Staff numeric responses (use first record)
            if org_data["staff_records"]:
                numeric_responses["Staff"] = self._extract_numeric_from_record(
                    org_data["staff_records"][0]
                )

            return copy.deepcopy(numeric_responses)

    def _extract_numeric_from_record(self, record: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract numeric responses from a single record.

        Args:
            record: Data record to extract from

        Returns:
            Dictionary mapping question IDs to numeric values
        """
        numeric_responses = {}

        for key, value in record.items():
            if key.startswith(("C-", "TL-", "S-")) and value:
                try:
                    num_value = float(str(value).strip())
                    # Only include valid ratings (0-5, excluding 6 which is N/A)
                    if 0 <= num_value <= 5:
                        numeric_responses[key] = num_value
                except (ValueError, TypeError):
                    # Skip non-numeric responses
                    continue

        return numeric_responses

    def _is_numeric_response(self, value: Any) -> bool:
        """
        Check if a response value is numeric.

        Args:
            value: Response value to check

        Returns:
            True if value is numeric, False otherwise
        """
        try:
            num_value = float(str(value).strip())
            return 0 <= num_value <= 7
        except (ValueError, TypeError):
            return False

    def _get_answer_text(self, value: Any, question_info: Dict[str, Any]) -> str:
        """
        Get human-readable answer text from answer keys.

        Args:
            value: Answer value
            question_info: Question metadata with answer_keys

        Returns:
            Human-readable answer text or original value as string
        """
        try:
            answer_keys = question_info.get("answer_keys", {})
            numeric_value = int(float(str(value)))
            return answer_keys.get(numeric_value, str(value))
        except (ValueError, TypeError):
            return str(value)


# Singleton instance management
_report_data_extractor_instance: Optional[ReportDataExtractor] = None
_instance_lock = threading.RLock()


def get_report_data_extractor(data_service=None) -> ReportDataExtractor:
    """
    Get singleton report data extractor instance.

    Args:
        data_service: Optional DataService instance (uses singleton if None)

    Returns:
        Singleton ReportDataExtractor instance
    """
    global _report_data_extractor_instance

    if _report_data_extractor_instance is None:
        with _instance_lock:
            if _report_data_extractor_instance is None:
                # Import singleton if not provided
                if data_service is None:
                    from src.services.data_service import get_data_service

                    data_service = get_data_service()

                _report_data_extractor_instance = ReportDataExtractor(data_service)

    return _report_data_extractor_instance
