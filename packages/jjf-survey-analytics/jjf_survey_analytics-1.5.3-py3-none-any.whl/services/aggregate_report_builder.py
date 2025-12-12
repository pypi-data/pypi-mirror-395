#!/usr/bin/env python3
"""
AggregateReportBuilder - Builder for foundation-level aggregate reports.

Extracts aggregate report generation logic from ReportGenerator God class.
Handles cross-organization statistics, participation metrics, dimension aggregation,
and maturity distribution analysis.
"""

import copy
import threading
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional


class AggregateReportBuilder:
    """
    Builder for generating foundation-wide aggregate reports.

    Responsibilities:
    - Build complete aggregate reports with 7 sections
    - Calculate cross-organization statistics
    - Generate participation metrics
    - Aggregate dimension scores and trends
    - Calculate maturity distribution
    - Thread-safe operations
    """

    def __init__(self, data_service, organization_report_builder, report_repository):
        """
        Initialize aggregate report builder with dependency injection.

        Args:
            data_service: DataService instance for accessing survey data
            organization_report_builder: OrganizationReportBuilder for individual reports
            report_repository: ReportRepository instance for persistence
        """
        self._data_service = data_service
        self._org_report_builder = organization_report_builder
        self._report_repository = report_repository
        self._lock = threading.RLock()

    def build_aggregate_report(self) -> Dict[str, Any]:
        """
        Build complete foundation-wide aggregate report.

        Returns:
            Dictionary containing aggregate report with 7 sections:
            - header: Report metadata
            - overview: High-level participation metrics
            - breakdown: Survey completion by type
            - timeline: Recent activity timeline
            - table: Organization status table
            - insights: Cross-organization statistics
            - recommendations: Actionable recommendations

        Thread Safety:
            Uses RLock for concurrent access protection
        """
        with self._lock:
            # Get tab data
            intake_data = self._data_service.get_tab_data("Intake")
            ceo_data = self._data_service.get_tab_data("CEO")
            tech_data = self._data_service.get_tab_data("Tech")
            staff_data = self._data_service.get_tab_data("Staff")

            # Build report sections (matching existing format exactly)
            report = {
                "header": self._build_header(),
                "overview": self._build_overview(intake_data, ceo_data, tech_data, staff_data),
                "breakdown": self._build_breakdown(ceo_data, tech_data, staff_data),
                "timeline": self._build_timeline(intake_data, ceo_data, tech_data, staff_data),
                "table": self._build_table(intake_data, ceo_data, tech_data, staff_data),
                "insights": self._build_insights(ceo_data, tech_data, staff_data),
                "recommendations": self._build_recommendations(
                    intake_data, ceo_data, tech_data, staff_data
                ),
            }

            return copy.deepcopy(report)

    def _build_header(self) -> Dict[str, Any]:
        """Build aggregate report header section."""
        return {
            "title": "JJF Survey Analytics - Aggregate Report",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "report_type": "Aggregate",
        }

    def _build_overview(
        self,
        intake_data: List[Dict[str, Any]],
        ceo_data: List[Dict[str, Any]],
        tech_data: List[Dict[str, Any]],
        staff_data: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Build aggregate overview metrics.

        Calculates participation rates and completion percentages.
        FIXED: Counts organizations, not individual responses.

        Args:
            intake_data: Intake tab data
            ceo_data: CEO tab data
            tech_data: Tech tab data
            staff_data: Staff tab data

        Returns:
            Dictionary containing overview metrics
        """
        total_orgs = len(intake_data)

        # Count unique organizations per survey type (not responses!)
        orgs_with_ceo = {
            r.get("CEO Organization") or r.get("Organization")
            for r in ceo_data
            if r.get("Date") and (r.get("CEO Organization") or r.get("Organization"))
        }
        orgs_with_tech = {
            r.get("Organization") for r in tech_data if r.get("Date") and r.get("Organization")
        }
        orgs_with_staff = {
            r.get("Organization") for r in staff_data if r.get("Date") and r.get("Organization")
        }

        # Organizations with at least one survey
        responding_orgs = orgs_with_ceo | orgs_with_tech | orgs_with_staff
        responding_orgs_count = len(responding_orgs)

        # Count completed survey types (not individual responses)
        ceo_complete = len(orgs_with_ceo)
        tech_complete = len(orgs_with_tech)
        staff_complete = len(orgs_with_staff)
        surveys_completed = ceo_complete + tech_complete + staff_complete

        # Expected surveys based on responding organizations
        expected_surveys = responding_orgs_count * 3  # 3 survey types per org

        # Count fully complete organizations (all 3 surveys)
        fully_complete = len(orgs_with_ceo & orgs_with_tech & orgs_with_staff)

        return {
            "total_organizations": total_orgs,
            "responding_organizations": responding_orgs_count,
            "total_surveys_expected": expected_surveys,
            "surveys_completed": surveys_completed,
            "surveys_pending": expected_surveys - surveys_completed,
            "completion_percentage": (
                round((surveys_completed / expected_surveys) * 100) if expected_surveys > 0 else 0
            ),
            "fully_complete_orgs": fully_complete,
            "ceo_complete": ceo_complete,
            "tech_complete": tech_complete,
            "staff_complete": staff_complete,
            "ceo_percentage": (
                round((ceo_complete / responding_orgs_count) * 100)
                if responding_orgs_count > 0
                else 0
            ),
            "tech_percentage": (
                round((tech_complete / responding_orgs_count) * 100)
                if responding_orgs_count > 0
                else 0
            ),
            "staff_percentage": (
                round((staff_complete / responding_orgs_count) * 100)
                if responding_orgs_count > 0
                else 0
            ),
        }

    def _build_breakdown(
        self,
        ceo_data: List[Dict[str, Any]],
        tech_data: List[Dict[str, Any]],
        staff_data: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Build aggregate breakdown by survey type.

        Args:
            ceo_data: CEO tab data
            tech_data: Tech tab data
            staff_data: Staff tab data

        Returns:
            Dictionary containing breakdown by survey type
        """
        return {
            "by_survey_type": {
                "CEO": {
                    "completed": len([r for r in ceo_data if r.get("Date")]),
                    "pending": len([r for r in ceo_data if not r.get("Date")]),
                    "total_responses": sum(
                        len([k for k in r.keys() if k.startswith("C-")])
                        for r in ceo_data
                        if r.get("Date")
                    ),
                },
                "Tech Lead": {
                    "completed": len([r for r in tech_data if r.get("Date")]),
                    "pending": len([r for r in tech_data if not r.get("Date")]),
                    "total_responses": sum(
                        len([k for k in r.keys() if k.startswith("TL-")])
                        for r in tech_data
                        if r.get("Date")
                    ),
                },
                "Staff": {
                    "completed": len([r for r in staff_data if r.get("Date")]),
                    "pending": len([r for r in staff_data if not r.get("Date")]),
                    "total_responses": sum(
                        len([k for k in r.keys() if k.startswith("S-")])
                        for r in staff_data
                        if r.get("Date")
                    ),
                },
            }
        }

    def _build_timeline(
        self,
        intake_data: List[Dict[str, Any]],
        ceo_data: List[Dict[str, Any]],
        tech_data: List[Dict[str, Any]],
        staff_data: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Build aggregate activity timeline.

        Args:
            intake_data: Intake tab data
            ceo_data: CEO tab data
            tech_data: Tech tab data
            staff_data: Staff tab data

        Returns:
            List of timeline events (most recent 20)
        """
        timeline = []

        # Collect all events
        for intake in intake_data:
            if intake.get("Date"):
                timeline.append(
                    {
                        "date": intake.get("Date", "")[:10],
                        "event_type": "Intake",
                        "organization": intake.get("Organization Name:", "Unknown"),
                        "count": 1,
                    }
                )

        for ceo in ceo_data:
            if ceo.get("Date"):
                timeline.append(
                    {
                        "date": ceo.get("Date", "")[:10],
                        "event_type": "CEO Survey",
                        "organization": ceo.get("CEO Organization", "Unknown"),
                        "count": 1,
                    }
                )

        for tech in tech_data:
            if tech.get("Date"):
                timeline.append(
                    {
                        "date": tech.get("Date", "")[:10],
                        "event_type": "Tech Survey",
                        "organization": tech.get("Organization", "Unknown"),
                        "count": 1,
                    }
                )

        for staff in staff_data:
            if staff.get("Date"):
                timeline.append(
                    {
                        "date": staff.get("Date", "")[:10],
                        "event_type": "Staff Survey",
                        "organization": staff.get("Organization", "Unknown"),
                        "count": 1,
                    }
                )

        # Sort by date descending
        timeline.sort(key=lambda x: x["date"], reverse=True)

        # Limit to recent 20 events
        return timeline[:20]

    def _build_table(
        self,
        intake_data: List[Dict[str, Any]],
        ceo_data: List[Dict[str, Any]],
        tech_data: List[Dict[str, Any]],
        staff_data: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Build aggregate organization status table.

        Args:
            intake_data: Intake tab data
            ceo_data: CEO tab data
            tech_data: Tech tab data
            staff_data: Staff tab data

        Returns:
            List of organization status records
        """
        org_status = []

        for intake in intake_data:
            org_name = intake.get("Organization Name:", "")
            if not org_name:
                continue

            # Find matching records
            ceo_record = next((r for r in ceo_data if r.get("CEO Organization") == org_name), None)
            tech_records = [r for r in tech_data if r.get("Organization") == org_name]
            staff_records = [r for r in staff_data if r.get("Organization") == org_name]

            # Calculate status
            ceo_complete = bool(ceo_record and ceo_record.get("Date"))
            tech_complete = any(r.get("Date") for r in tech_records)
            staff_complete = any(r.get("Date") for r in staff_records)

            completed = sum([ceo_complete, tech_complete, staff_complete])
            completion_pct = round((completed / 3) * 100)

            org_status.append(
                {
                    "organization": org_name,
                    "intake_date": intake.get("Date", "")[:10] if intake.get("Date") else "N/A",
                    "ceo_status": "Complete" if ceo_complete else "Pending",
                    "tech_status": "Complete" if tech_complete else "Pending",
                    "staff_status": "Complete" if staff_complete else "Pending",
                    "completion_percentage": completion_pct,
                    "overall_status": (
                        "Complete"
                        if completed == 3
                        else ("In Progress" if completed > 0 else "Not Started")
                    ),
                }
            )

        # Sort by completion percentage descending
        org_status.sort(key=lambda x: x["completion_percentage"], reverse=True)

        return org_status

    def _build_insights(
        self,
        ceo_data: List[Dict[str, Any]],
        tech_data: List[Dict[str, Any]],
        staff_data: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Build aggregate insights and statistics.

        Args:
            ceo_data: CEO tab data
            tech_data: Tech tab data
            staff_data: Staff tab data

        Returns:
            Dictionary containing aggregate statistics
        """
        # Collect all numeric responses
        all_responses = []

        for ceo in ceo_data:
            if ceo.get("Date"):
                for key, value in ceo.items():
                    if key.startswith("C-") and value:
                        if str(value).strip().isdigit():
                            all_responses.append(int(value))

        for tech in tech_data:
            if tech.get("Date"):
                for key, value in tech.items():
                    if key.startswith("TL-") and value:
                        if str(value).strip().isdigit():
                            all_responses.append(int(value))

        for staff in staff_data:
            if staff.get("Date"):
                for key, value in staff.items():
                    if key.startswith("S-") and value:
                        if str(value).strip().isdigit():
                            all_responses.append(int(value))

        # Calculate statistics
        if all_responses:
            avg_score = round(sum(all_responses) / len(all_responses), 2)
            min_score = min(all_responses)
            max_score = max(all_responses)
        else:
            avg_score = min_score = max_score = 0

        return {
            "total_responses": len(all_responses),
            "average_score": avg_score,
            "min_score": min_score,
            "max_score": max_score,
            "high_scores": len([r for r in all_responses if r >= 6]),
            "low_scores": len([r for r in all_responses if r <= 2]),
        }

    def _build_recommendations(
        self,
        intake_data: List[Dict[str, Any]],
        ceo_data: List[Dict[str, Any]],
        tech_data: List[Dict[str, Any]],
        staff_data: List[Dict[str, Any]],
    ) -> List[str]:
        """
        Build aggregate recommendations.

        Args:
            intake_data: Intake tab data
            ceo_data: CEO tab data
            tech_data: Tech tab data
            staff_data: Staff tab data

        Returns:
            List of recommendation strings
        """
        recommendations = []

        total_orgs = len(intake_data)
        ceo_complete = len([r for r in ceo_data if r.get("Date")])
        tech_complete = len([r for r in tech_data if r.get("Date")])
        staff_complete = len([r for r in staff_data if r.get("Date")])

        # CEO completion rate
        if ceo_complete < total_orgs * 0.5:
            recommendations.append(
                f"Focus on CEO survey completion: Only {ceo_complete}/{total_orgs} "
                f"({round((ceo_complete/total_orgs)*100)}%) completed"
            )

        # Tech completion rate
        if tech_complete < total_orgs * 0.5:
            recommendations.append(
                f"Increase Tech Lead engagement: Only {tech_complete} surveys completed"
            )

        # Staff completion rate
        if staff_complete < total_orgs * 0.5:
            recommendations.append(
                f"Prioritize Staff survey collection: Only {staff_complete} responses received"
            )

        # Overall completion
        total_expected = total_orgs * 3
        total_complete = ceo_complete + tech_complete + staff_complete
        if total_complete < total_expected * 0.75:
            recommendations.append(
                f"Overall survey completion is {round((total_complete/total_expected)*100)}% "
                "- target 75%+ for robust analysis"
            )

        if not recommendations:
            recommendations.append(
                "Strong survey completion rates across all categories - "
                "continue current outreach efforts"
            )

        return recommendations

    def calculate_participation_stats(self) -> Dict[str, Any]:
        """
        Calculate detailed participation statistics.

        Returns:
            Dictionary containing participation metrics:
            - response_rates: By stakeholder type
            - completion_rates: By organization
            - time_to_complete: Average days from intake
        """
        with self._lock:
            intake_data = self._data_service.get_tab_data("Intake")
            ceo_data = self._data_service.get_tab_data("CEO")
            tech_data = self._data_service.get_tab_data("Tech")
            staff_data = self._data_service.get_tab_data("Staff")

            # Build response rates
            total_orgs = len(intake_data)
            response_rates = {
                "ceo": (
                    len([r for r in ceo_data if r.get("Date")]) / total_orgs
                    if total_orgs > 0
                    else 0
                ),
                "tech": (
                    len([r for r in tech_data if r.get("Date")]) / total_orgs
                    if total_orgs > 0
                    else 0
                ),
                "staf": (
                    len([r for r in staff_data if r.get("Date")]) / total_orgs
                    if total_orgs > 0
                    else 0
                ),
            }

            # Calculate completion rates per org
            completion_rates = []
            for intake in intake_data:
                org_name = intake.get("Organization Name:", "")
                if not org_name:
                    continue

                ceo_complete = any(
                    r.get("CEO Organization") == org_name and r.get("Date") for r in ceo_data
                )
                tech_complete = any(
                    r.get("Organization") == org_name and r.get("Date") for r in tech_data
                )
                staff_complete = any(
                    r.get("Organization") == org_name and r.get("Date") for r in staff_data
                )

                completed = sum([ceo_complete, tech_complete, staff_complete])
                completion_rates.append(completed / 3)

            avg_completion = (
                sum(completion_rates) / len(completion_rates) if completion_rates else 0
            )

            return {
                "response_rates": response_rates,
                "average_completion_rate": avg_completion,
                "fully_complete_count": sum(1 for rate in completion_rates if rate == 1.0),
                "partially_complete_count": sum(1 for rate in completion_rates if 0 < rate < 1.0),
                "not_started_count": sum(1 for rate in completion_rates if rate == 0),
            }

    def aggregate_dimension_scores(self) -> Dict[str, Any]:
        """
        Aggregate dimension scores across all organizations.

        Returns:
            Dictionary containing dimension aggregates:
            - mean_scores: Average score per dimension
            - median_scores: Median score per dimension
            - std_dev: Standard deviation per dimension
            - distribution: Score distribution histograms
        """
        with self._lock:
            # Get all organization names
            org_names = self._data_service.get_all_org_names()

            # Collect dimension scores from all organizations
            dimension_scores = defaultdict(list)

            for org_name in org_names:
                # Build org report to get maturity assessment
                org_report = self._org_report_builder.build_report(org_name)
                if not org_report or "maturity" not in org_report:
                    continue

                maturity = org_report["maturity"]
                variance_analysis = maturity.get("variance_analysis", {})

                for dimension, analysis in variance_analysis.items():
                    score = analysis.get("weighted_score", 0)
                    if score > 0:  # Only include valid scores
                        dimension_scores[dimension].append(score)

            # Calculate aggregates
            aggregates = {}
            for dimension, scores in dimension_scores.items():
                if not scores:
                    continue

                sorted_scores = sorted(scores)
                n = len(sorted_scores)

                # Calculate statistics
                mean = sum(scores) / n
                median = (
                    sorted_scores[n // 2]
                    if n % 2 == 1
                    else (sorted_scores[n // 2 - 1] + sorted_scores[n // 2]) / 2
                )

                # Standard deviation
                variance = sum((x - mean) ** 2 for x in scores) / n
                std_dev = variance**0.5

                aggregates[dimension] = {
                    "mean": round(mean, 2),
                    "median": round(median, 2),
                    "std_dev": round(std_dev, 2),
                    "min": min(scores),
                    "max": max(scores),
                    "count": n,
                }

            return aggregates

    def calculate_maturity_distribution(self) -> Dict[str, Any]:
        """
        Calculate distribution of maturity levels across organizations.

        Returns:
            Dictionary containing maturity distribution:
            - building_count: Number of Building organizations (0-35%)
            - emerging_count: Number of Emerging organizations (36-70%)
            - thriving_count: Number of Thriving organizations (71-100%)
            - percentages: Distribution percentages
        """
        with self._lock:
            org_names = self._data_service.get_all_org_names()

            # Count organizations by maturity level
            building_count = 0
            emerging_count = 0
            thriving_count = 0

            for org_name in org_names:
                org_report = self._org_report_builder.build_report(org_name)
                if not org_report or "maturity" not in org_report:
                    continue

                maturity_level = org_report["maturity"].get("maturity_level", "")

                if maturity_level == "Building":
                    building_count += 1
                elif maturity_level == "Emerging":
                    emerging_count += 1
                elif maturity_level == "Thriving":
                    thriving_count += 1

            total = building_count + emerging_count + thriving_count

            return {
                "building_count": building_count,
                "emerging_count": emerging_count,
                "thriving_count": thriving_count,
                "total": total,
                "building_percentage": round((building_count / total) * 100) if total > 0 else 0,
                "emerging_percentage": round((emerging_count / total) * 100) if total > 0 else 0,
                "thriving_percentage": round((thriving_count / total) * 100) if total > 0 else 0,
            }

    def generate_trend_analysis(self) -> Dict[str, Any]:
        """
        Generate trends and patterns across organizations.

        Returns:
            Dictionary containing trend analysis:
            - highest_scoring_dimension: Dimension with highest avg score
            - lowest_scoring_dimension: Dimension with lowest avg score
            - most_aligned: Dimension with lowest variance
            - least_aligned: Dimension with highest variance
        """
        with self._lock:
            dimension_aggregates = self.aggregate_dimension_scores()

            if not dimension_aggregates:
                return {
                    "highest_scoring_dimension": None,
                    "lowest_scoring_dimension": None,
                    "most_aligned": None,
                    "least_aligned": None,
                }

            # Find highest and lowest scoring
            sorted_by_mean = sorted(
                dimension_aggregates.items(), key=lambda x: x[1]["mean"], reverse=True
            )
            highest = sorted_by_mean[0] if sorted_by_mean else None
            lowest = sorted_by_mean[-1] if sorted_by_mean else None

            # Find most and least aligned (by std deviation)
            sorted_by_std = sorted(dimension_aggregates.items(), key=lambda x: x[1]["std_dev"])
            most_aligned = sorted_by_std[0] if sorted_by_std else None
            least_aligned = sorted_by_std[-1] if sorted_by_std else None

            return {
                "highest_scoring_dimension": (
                    {"name": highest[0], "mean_score": highest[1]["mean"]} if highest else None
                ),
                "lowest_scoring_dimension": (
                    {"name": lowest[0], "mean_score": lowest[1]["mean"]} if lowest else None
                ),
                "most_aligned": (
                    {"name": most_aligned[0], "std_dev": most_aligned[1]["std_dev"]}
                    if most_aligned
                    else None
                ),
                "least_aligned": (
                    {"name": least_aligned[0], "std_dev": least_aligned[1]["std_dev"]}
                    if least_aligned
                    else None
                ),
            }


# Global singleton instance
_aggregate_report_builder_instance: Optional[AggregateReportBuilder] = None
_instance_lock = threading.RLock()


def get_aggregate_report_builder(
    data_service=None, organization_report_builder=None, report_repository=None
) -> AggregateReportBuilder:
    """
    Get singleton aggregate report builder instance.

    Args:
        data_service: Optional DataService instance (uses singleton if None)
        organization_report_builder: Optional OrganizationReportBuilder instance
        report_repository: Optional ReportRepository instance

    Returns:
        Singleton AggregateReportBuilder instance
    """
    global _aggregate_report_builder_instance

    if _aggregate_report_builder_instance is None:
        with _instance_lock:
            if _aggregate_report_builder_instance is None:
                # Import singletons if not provided
                if data_service is None:
                    from src.services.data_service import get_data_service

                    data_service = get_data_service()

                if organization_report_builder is None:
                    from src.services.organization_report_builder import (
                        get_organization_report_builder,
                    )

                    organization_report_builder = get_organization_report_builder()

                if report_repository is None:
                    from src.repositories.report_repository import get_report_repository

                    report_repository = get_report_repository()

                _aggregate_report_builder_instance = AggregateReportBuilder(
                    data_service, organization_report_builder, report_repository
                )

    return _aggregate_report_builder_instance
