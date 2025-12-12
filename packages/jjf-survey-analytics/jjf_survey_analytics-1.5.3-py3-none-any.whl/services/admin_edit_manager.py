#!/usr/bin/env python3
"""
AdminEditManager - Manages admin edit application and score recalculation.

Extracts admin edit application logic from ReportGenerator/OrganizationReportBuilder.
Handles applying admin overrides to reports and recalculating affected scores.
"""

import copy
import threading
from typing import Any, Dict, Optional


class AdminEditManager:
    """
    Thread-safe manager for applying admin edits to organization reports.

    Responsibilities:
    - Apply summary title and body edits
    - Apply dimension insight text overrides
    - Apply score modifiers to dimension scores
    - Recalculate overall maturity score from adjusted dimensions
    - Preserve original values for audit trail
    - Thread-safe operations with RLock

    Admin Edit Structure:
    {
        "summary_title": str,
        "summary_body": str,
        "dimension_insights": {
            "Dimension Name": "Custom insight text"
        },
        "score_modifiers": {
            "Dimension Name": [
                {"id": 0, "value": 5},  # Add 5 points
                {"id": 1, "value": -3}  # Subtract 3 points
            ]
        }
    }
    """

    # Dimension weights for overall score calculation (from MaturityRubric)
    DIMENSION_WEIGHTS = {
        "Program Technology": 0.20,
        "Business Systems": 0.20,
        "Data Management": 0.20,
        "Infrastructure": 0.20,
        "Organizational Culture": 0.20,
    }

    def __init__(self, admin_edit_service):
        """
        Initialize admin edit manager with dependency injection.

        Args:
            admin_edit_service: AdminEditService instance for fetching edits
        """
        self._admin_edit_service = admin_edit_service
        self._lock = threading.RLock()

    def apply_edits_to_report(self, report: Dict[str, Any], org_name: str) -> Dict[str, Any]:
        """
        Apply all admin edits to a report and recalculate scores.

        Args:
            report: Report data dictionary
            org_name: Organization name

        Returns:
            Deep copy of report with all admin edits applied

        Thread Safety:
            Uses RLock for concurrent access protection
        """
        with self._lock:
            # Deep copy to avoid modifying original
            report_copy = copy.deepcopy(report)

            # Get admin edits for organization
            org_edits = self._admin_edit_service.get_org_edits(org_name)

            # Check if edits exist and contain any non-empty values
            if not org_edits or not self._has_any_edits(org_edits):
                return report_copy

            print(f"[AdminEditManager] Applying admin edits for {org_name}")

            # Apply summary edits
            report_copy = self.apply_summary_edits(report_copy, org_edits)

            # Apply dimension insight edits
            report_copy = self.apply_dimension_insight_edits(report_copy, org_edits)

            # Apply score modifiers and recalculate
            report_copy = self.apply_score_modifiers(report_copy, org_edits)

            # Recalculate overall score based on adjusted dimensions
            report_copy = self.recalculate_overall_score(report_copy)

            return report_copy

    def apply_summary_edits(self, report: Dict[str, Any], edits: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply summary title and body edits to report.

        Args:
            report: Report data dictionary
            edits: Admin edits dictionary

        Returns:
            Report with summary edits applied
        """
        # Ensure summary section exists
        if "summary" not in report:
            report["summary"] = {}

        # Apply summary title
        if edits.get("summary_title"):
            report["summary"]["title"] = edits["summary_title"]
            print("[AdminEditManager] Applied custom summary title")

        # Apply summary body
        if edits.get("summary_body"):
            report["summary"]["body"] = edits["summary_body"]
            print("[AdminEditManager] Applied custom summary body")

        return report

    def apply_dimension_insight_edits(
        self, report: Dict[str, Any], edits: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply dimension insight text overrides to report.

        Args:
            report: Report data dictionary
            edits: Admin edits dictionary

        Returns:
            Report with dimension insight edits applied
        """
        dimension_insight_edits = edits.get("dimension_insights", {})
        if not dimension_insight_edits:
            return report

        # Ensure dimension_insights section exists
        if "dimension_insights" not in report:
            report["dimension_insights"] = {}

        # Apply each dimension insight edit
        for dimension, custom_insight in dimension_insight_edits.items():
            if custom_insight:  # Only apply non-empty insights
                report["dimension_insights"][dimension] = custom_insight
                print(f"[AdminEditManager] Applied custom dimension insight for {dimension}")

        return report

    def apply_score_modifiers(
        self, report: Dict[str, Any], edits: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply score modifiers to dimension scores and update AI modifiers.

        This method:
        1. Updates AI modifier values in ai_insights section
        2. Calculates total modifier for each dimension
        3. Applies modifiers to base weighted scores
        4. Clamps adjusted scores to valid range (0-5)
        5. Stores adjusted scores in variance_analysis

        Args:
            report: Report data dictionary
            edits: Admin edits dictionary

        Returns:
            Report with score modifiers applied
        """
        score_modifiers = edits.get("score_modifiers", {})
        if not score_modifiers:
            return report

        # Ensure maturity section exists with variance_analysis
        if "maturity" not in report or "variance_analysis" not in report["maturity"]:
            return report

        # Process each dimension's score modifiers
        for dimension, modifiers in score_modifiers.items():
            # Convert dimension key back to original format (e.g., "Program_Technology" -> "Program Technology")
            dimension_key = dimension.replace("_", " ")

            if dimension_key not in report["maturity"]["variance_analysis"]:
                continue

            analysis = report["maturity"]["variance_analysis"][dimension_key]

            # Update AI modifier values if AI insights exist
            self._update_ai_modifiers(report, dimension_key, modifiers)

            # Calculate total modifier from admin edits
            total_modifier = sum(mod.get("value", 0) for mod in modifiers)

            # Get base score
            base_score = analysis.get("weighted_score", 0)

            # Apply modifier and clamp to valid range (0-5)
            adjusted_score = self._clamp_score(base_score + total_modifier)

            # Store adjusted score AND total_modifier in variance_analysis
            # This allows the debug display to show modifier values correctly
            analysis["adjusted_score"] = adjusted_score
            analysis["total_modifier"] = total_modifier

            print(
                f"[AdminEditManager] Applied score modifier to {dimension_key}: "
                f"{base_score:.2f} + {total_modifier} = {adjusted_score:.2f}"
            )

        return report

    def recalculate_overall_score(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recalculate overall maturity score based on adjusted dimension scores.

        Uses centralized calculation method to ensure consistency across the platform.

        Args:
            report: Report dictionary (modified in place)

        Returns:
            Report with recalculated overall score
        """
        if "maturity" not in report or "variance_analysis" not in report["maturity"]:
            return report

        # Use centralized calculation method (single source of truth)
        from src.analytics.maturity_rubric import MaturityRubric

        variance_analysis = report["maturity"]["variance_analysis"]
        new_overall_score = MaturityRubric.calculate_overall_score_from_dimensions(variance_analysis)
        report["maturity"]["overall_score"] = new_overall_score
        print(f"[AdminEditManager] Recalculated overall maturity score: {new_overall_score:.2f}")

        return report

    # Private Helper Methods

    def _has_any_edits(self, edits: Dict[str, Any]) -> bool:
        """Check if edits dictionary contains any non-empty values."""
        if edits.get("summary_title"):
            return True
        if edits.get("summary_body"):
            return True
        if edits.get("dimension_insights"):
            return True
        if edits.get("score_modifiers"):
            return True
        return False

    def _update_ai_modifiers(
        self, report: Dict[str, Any], dimension_key: str, modifiers: list[Dict[str, Any]]
    ) -> None:
        """
        Update AI modifier values in ai_insights section.

        Args:
            report: Report data dictionary
            dimension_key: Dimension name
            modifiers: List of modifier edits with id and value
        """
        # Check if AI insights exist
        if "ai_insights" not in report or not report["ai_insights"]:
            return

        if "dimensions" not in report["ai_insights"]:
            return

        if dimension_key not in report["ai_insights"]["dimensions"]:
            return

        # Get AI modifiers for this dimension
        ai_modifiers = report["ai_insights"]["dimensions"][dimension_key].get("modifiers", [])

        # Update each modifier value based on admin edits
        for modifier_edit in modifiers:
            modifier_id = modifier_edit.get("id")
            new_value = modifier_edit.get("value", 0)

            if modifier_id is not None and modifier_id < len(ai_modifiers):
                ai_modifiers[modifier_id]["value"] = new_value
                print(
                    f"[AdminEditManager] Updated {dimension_key} "
                    f"modifier {modifier_id} to {new_value}"
                )

    def _clamp_score(self, score: float) -> float:
        """
        Clamp score to valid range (0-5).

        Args:
            score: Score value to clamp

        Returns:
            Clamped score between 0 and 5
        """
        return max(0.0, min(5.0, score))


# Global singleton instance
_admin_edit_manager_instance: Optional[AdminEditManager] = None
_instance_lock = threading.RLock()


def get_admin_edit_manager(admin_edit_service=None) -> AdminEditManager:
    """
    Get singleton admin edit manager instance.

    Args:
        admin_edit_service: Optional AdminEditService instance (uses singleton if None)

    Returns:
        Singleton AdminEditManager instance
    """
    global _admin_edit_manager_instance

    if _admin_edit_manager_instance is None:
        with _instance_lock:
            if _admin_edit_manager_instance is None:
                # Import singleton if not provided
                if admin_edit_service is None:
                    from src.services.admin_edit_service import get_admin_edit_service

                    admin_edit_service = get_admin_edit_service()

                _admin_edit_manager_instance = AdminEditManager(admin_edit_service)

    return _admin_edit_manager_instance
