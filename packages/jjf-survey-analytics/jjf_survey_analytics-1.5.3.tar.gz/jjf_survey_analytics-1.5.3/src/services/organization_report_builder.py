#!/usr/bin/env python3
"""
OrganizationReportBuilder - Builder for organization-specific reports.

Extracts organization report generation logic from ReportGenerator God class.
Handles maturity scoring, variance analysis, response summarization, and admin edits.
"""

import copy
import threading
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from src.analytics.maturity_rubric import MaturityRubric


class OrganizationReportBuilder:
    """
    Builder for generating comprehensive organization reports.

    Responsibilities:
    - Build complete organization reports with all sections
    - Calculate maturity scores per dimension
    - Generate variance analysis
    - Create response summaries
    - Apply admin edits
    - Thread-safe operations
    """

    def __init__(
        self,
        data_service,
        cache_service,
        admin_edit_service,
        report_repository,
        questions_lookup: Optional[Dict[str, Dict[str, Any]]] = None,
        enable_ai: bool = True,
    ):
        """
        Initialize organization report builder with dependency injection.

        Args:
            data_service: DataService instance for accessing survey data
            cache_service: CacheService instance for caching reports
            admin_edit_service: AdminEditService instance for admin overrides
            report_repository: ReportRepository instance for persistence
            questions_lookup: Optional pre-built questions lookup (built from data if None)
            enable_ai: Enable AI-powered qualitative analysis
        """
        self._data_service = data_service
        self._cache_service = cache_service
        self._admin_edit_service = admin_edit_service
        self._report_repository = report_repository
        self._rubric = MaturityRubric()
        self._enable_ai = enable_ai
        self._lock = threading.RLock()

        # Build questions lookup from data service if not provided
        self._questions_lookup = questions_lookup or self._build_questions_lookup()

        # Initialize AI analyzer if enabled
        self._ai_analyzer = None
        if self._enable_ai:
            try:
                from src.analytics.ai_analyzer import AIAnalyzer

                self._ai_analyzer = AIAnalyzer()
                print("[OrganizationReportBuilder] AI analyzer initialized successfully")
            except Exception as e:
                print(f"[OrganizationReportBuilder] Warning: AI analyzer not available: {e}")
                self._enable_ai = False

    def _build_questions_lookup(self) -> Dict[str, Dict[str, Any]]:
        """Build lookup dictionary for questions and answer keys from data service."""
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

    def build_report(self, org_name: str) -> Optional[Dict[str, Any]]:
        """
        Build complete organization report with all sections.

        Args:
            org_name: Organization name

        Returns:
            Dictionary containing complete report data, or None if org not found

        Thread Safety:
            Uses RLock for concurrent access protection
        """
        with self._lock:
            # Get organization data
            org_data = self._get_org_data(org_name)
            if not org_data or not org_data.get("intake_record"):
                return None

            # Calculate maturity assessment
            maturity_assessment = self._calculate_maturity_assessment(org_name, org_data)

            # Calculate NPS metrics
            nps_metrics = self._calculate_nps_metrics(org_data["staff_records"])

            # Extract tech insights
            tech_insights = self._extract_tech_insights(org_data)

            # Generate AI insights if enabled
            ai_insights, dimension_insights = self._generate_ai_insights(
                org_name, maturity_assessment
            )

            # Build report sections
            report = {
                "header": self._build_header(org_name, org_data["intake_record"]),
                "maturity": maturity_assessment,
                "nps": nps_metrics,
                "tech_insights": tech_insights,
                "ai_insights": ai_insights,
                "dimension_insights": dimension_insights,
                "timeline": self._build_timeline(org_data),
                "contacts": self._build_contacts(org_data),
                "intake": self._build_intake_insights(org_data["intake_record"]),
                "responses": self._build_responses(org_data),
                "export": self._build_export_data(org_name),
            }

            # Apply admin edits
            report = self._apply_admin_edits(org_name, report)

            return copy.deepcopy(report)

    def _get_org_data(self, org_name: str) -> Optional[Dict[str, Any]]:
        """
        Extract all organization data from data service.

        Args:
            org_name: Organization name

        Returns:
            Dictionary containing all org records, or None if not found
        """
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

        return {
            "intake_record": intake_record,
            "ceo_record": ceo_record,
            "tech_records": tech_records,
            "staff_records": staff_records,
        }

    def _calculate_dimension_scores(self, org_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate maturity scores for each dimension.

        Args:
            org_data: Organization data dictionary

        Returns:
            Dictionary mapping dimension names to scores
        """
        # Extract numeric responses
        org_responses = {
            "CEO": (
                self._extract_numeric_responses(org_data["ceo_record"])
                if org_data["ceo_record"]
                else {}
            ),
            "Tech": (
                self._extract_numeric_responses(org_data["tech_records"][0])
                if org_data["tech_records"]
                else {}
            ),
            "Staff": (
                self._extract_numeric_responses(org_data["staff_records"][0])
                if org_data["staff_records"]
                else {}
            ),
        }

        # Calculate dimension scores using rubric
        dimension_scores = {}
        for dimension in self._rubric.DIMENSION_WEIGHTS.keys():
            ceo_score = self._rubric.calculate_dimension_score(
                org_responses.get("CEO", {}), "CEO", dimension
            )
            tech_score = self._rubric.calculate_dimension_score(
                org_responses.get("Tech", {}), "Tech Lead", dimension
            )
            staff_score = self._rubric.calculate_dimension_score(
                org_responses.get("Staff", {}), "Staff", dimension
            )

            weighted_score = self._rubric.calculate_weighted_dimension_score(
                ceo_score, tech_score, staff_score, dimension
            )
            dimension_scores[dimension] = weighted_score

        return dimension_scores

    def _generate_variance_analysis(self, org_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate stakeholder alignment analysis.

        Args:
            org_data: Organization data dictionary

        Returns:
            Dictionary containing variance analysis per dimension
        """
        # Extract numeric responses
        org_responses = {
            "CEO": (
                self._extract_numeric_responses(org_data["ceo_record"])
                if org_data["ceo_record"]
                else {}
            ),
            "Tech": (
                self._extract_numeric_responses(org_data["tech_records"][0])
                if org_data["tech_records"]
                else {}
            ),
            "Staff": (
                self._extract_numeric_responses(org_data["staff_records"][0])
                if org_data["staff_records"]
                else {}
            ),
        }

        variance_analysis = {}

        for dimension in self._rubric.DIMENSION_WEIGHTS.keys():
            # Calculate scores by role
            ceo_score = self._rubric.calculate_dimension_score(
                org_responses.get("CEO", {}), "CEO", dimension
            )
            tech_score = self._rubric.calculate_dimension_score(
                org_responses.get("Tech", {}), "Tech Lead", dimension
            )
            staff_score = self._rubric.calculate_dimension_score(
                org_responses.get("Staff", {}), "Staff", dimension
            )

            # Calculate weighted dimension score
            weighted_score = self._rubric.calculate_weighted_dimension_score(
                ceo_score, tech_score, staff_score, dimension
            )

            # Calculate variance (only for stakeholders with valid scores)
            scores_list = [s for s in [ceo_score, tech_score, staff_score] if s is not None]
            std_dev, level, color, desc = self._rubric.calculate_variance(scores_list)

            variance_analysis[dimension] = {
                "ceo_score": ceo_score if ceo_score is not None else 0.0,
                "tech_score": tech_score if tech_score is not None else 0.0,
                "staff_score": staff_score if staff_score is not None else 0.0,
                "weighted_score": weighted_score if weighted_score is not None else 0.0,
                "variance": std_dev,
                "level": level,
                "color": color,
                "description": desc,
            }

        return variance_analysis

    def _calculate_maturity_assessment(
        self, org_name: str, org_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive maturity assessment.

        Args:
            org_name: Organization name
            org_data: Organization data dictionary

        Returns:
            Complete maturity assessment dictionary
        """
        # Extract numeric responses
        org_responses = {
            "CEO": (
                self._extract_numeric_responses(org_data["ceo_record"])
                if org_data["ceo_record"]
                else {}
            ),
            "Tech": (
                self._extract_numeric_responses(org_data["tech_records"][0])
                if org_data["tech_records"]
                else {}
            ),
            "Staff": (
                self._extract_numeric_responses(org_data["staff_records"][0])
                if org_data["staff_records"]
                else {}
            ),
        }

        # Use rubric to calculate overall maturity
        maturity_assessment = self._rubric.calculate_overall_maturity(org_responses)

        # Consolidate maturity description if AI is available
        if (
            self._enable_ai
            and self._ai_analyzer
            and maturity_assessment.get("maturity_description")
        ):
            try:
                maturity_assessment["maturity_description"] = self._ai_analyzer.consolidate_text(
                    maturity_assessment["maturity_description"], max_chars=55
                )
            except Exception as e:
                print(
                    f"[OrganizationReportBuilder] Warning: Could not consolidate maturity description: {e}"
                )

        return maturity_assessment

    def _create_response_summary(self, org_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Summarize responses by stakeholder type.

        Args:
            org_data: Organization data dictionary

        Returns:
            Dictionary containing response summary metrics
        """
        total_surveys = 3  # CEO, Tech, Staff
        completed = 0

        if org_data["ceo_record"] and org_data["ceo_record"].get("Date"):
            completed += 1
        if any(r.get("Date") for r in org_data["tech_records"]):
            completed += 1
        if any(r.get("Date") for r in org_data["staff_records"]):
            completed += 1

        completion_pct = round((completed / total_surveys) * 100) if total_surveys > 0 else 0

        return {
            "total_surveys": total_surveys,
            "completed_surveys": completed,
            "pending_surveys": total_surveys - completed,
            "completion_percentage": completion_pct,
            "ceo_complete": bool(org_data["ceo_record"] and org_data["ceo_record"].get("Date")),
            "tech_complete": any(r.get("Date") for r in org_data["tech_records"]),
            "staff_complete": any(r.get("Date") for r in org_data["staff_records"]),
        }

    def _apply_admin_edits(self, org_name: str, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply admin overrides to report data.

        Args:
            org_name: Organization name
            report: Report data dictionary

        Returns:
            Report with admin edits applied
        """
        org_edits = self._admin_edit_service.get_org_edits(org_name)
        if not org_edits or not any(org_edits.values()):
            return report

        print(f"[OrganizationReportBuilder] Applying admin edits for {org_name}")

        # Apply summary edits
        if org_edits.get("summary_title"):
            if "summary" not in report:
                report["summary"] = {}
            report["summary"]["title"] = org_edits["summary_title"]

        if org_edits.get("summary_subtitle"):
            if "summary" not in report:
                report["summary"] = {}
            report["summary"]["subtitle"] = org_edits["summary_subtitle"]

        if org_edits.get("summary_body"):
            if "summary" not in report:
                report["summary"] = {}
            report["summary"]["body"] = org_edits["summary_body"]

        # Apply dimension insight edits
        dimension_insight_edits = org_edits.get("dimension_insights", {})
        if (
            dimension_insight_edits
            and "dimension_insights" in report
            and report["dimension_insights"]
        ):
            for dimension, custom_insight in dimension_insight_edits.items():
                if dimension in report["dimension_insights"]:
                    report["dimension_insights"][dimension] = custom_insight
                else:
                    report["dimension_insights"][dimension] = custom_insight

        # Apply score modifiers
        score_modifiers = org_edits.get("score_modifiers", {})
        if score_modifiers and "maturity" in report and "variance_analysis" in report["maturity"]:
            print(
                f"[DEBUG] Applying score modifiers for dimensions: {list(score_modifiers.keys())}"
            )
            for dimension, modifiers in score_modifiers.items():
                dimension_key = dimension.replace("_", " ")
                print(f"[DEBUG] Processing dimension '{dimension}' (normalized: '{dimension_key}')")
                print(f"[DEBUG] Modifiers to apply: {modifiers}")

                if dimension_key in report["maturity"]["variance_analysis"]:
                    analysis = report["maturity"]["variance_analysis"][dimension_key]
                    print("[DEBUG] Found dimension in variance_analysis")

                    # Apply modifier values to AI insights if they exist
                    if (
                        "ai_insights" in report
                        and report["ai_insights"]
                        and "dimensions" in report["ai_insights"]
                    ):
                        print("[DEBUG] AI insights available for report")
                        print(
                            f"[DEBUG] Available AI insight dimensions: {list(report['ai_insights']['dimensions'].keys())}"
                        )

                        if dimension_key in report["ai_insights"]["dimensions"]:
                            ai_modifiers = report["ai_insights"]["dimensions"][dimension_key].get(
                                "modifiers", []
                            )
                            print(
                                f"[DEBUG] Found {len(ai_modifiers)} AI modifiers for dimension '{dimension_key}'"
                            )

                            for modifier_edit in modifiers:
                                modifier_id = modifier_edit.get("id")
                                new_value = modifier_edit.get("value", 0)

                                if modifier_id is not None and modifier_id < len(ai_modifiers):
                                    old_value = ai_modifiers[modifier_id]["value"]
                                    ai_modifiers[modifier_id]["value"] = new_value
                                    print(
                                        f"[DEBUG] Updated modifier {modifier_id}: {old_value} → {new_value}"
                                    )
                                else:
                                    print(
                                        f"[DEBUG] Skipping modifier {modifier_id}: out of bounds or invalid"
                                    )

                            print(
                                f"[DEBUG] Updated AI insights for {dimension_key}: modifiers={ai_modifiers}"
                            )
                        else:
                            print(
                                f"[DEBUG] WARNING: Dimension '{dimension_key}' not found in AI insights dimensions"
                            )
                    else:
                        print("[DEBUG] WARNING: No AI insights available in report")

                    # Recalculate adjusted score
                    base_score = analysis.get("weighted_score", 0)
                    total_modifier = sum(mod.get("value", 0) for mod in modifiers)
                    adjusted_score = max(0, min(5, base_score + total_modifier))
                    analysis["adjusted_score"] = adjusted_score

            # Recalculate overall score
            self._recalculate_overall_score(report)

        return report

    def _recalculate_overall_score(self, report: Dict[str, Any]) -> None:
        """
        Recalculate overall maturity score based on adjusted dimension scores.

        Args:
            report: Report dictionary (modified in place)
        """
        if "maturity" not in report or "variance_analysis" not in report["maturity"]:
            return

        # Use centralized calculation method (single source of truth)
        from src.analytics.maturity_rubric import MaturityRubric

        variance_analysis = report["maturity"]["variance_analysis"]
        new_overall_score = MaturityRubric.calculate_overall_score_from_dimensions(variance_analysis)
        report["maturity"]["overall_score"] = new_overall_score

    # Helper methods for building report sections

    def _extract_numeric_responses(self, record: Optional[Dict[str, Any]]) -> Dict[str, float]:
        """Extract numeric responses (ignoring text/open-ended)."""
        if not record:
            return {}

        numeric_responses = {}

        for key, value in record.items():
            if key.startswith(("C-", "TL-", "S-")) and value:
                try:
                    num_value = float(str(value).strip())
                    if 0 <= num_value <= 5:
                        numeric_responses[key] = num_value
                except (ValueError, TypeError):
                    continue

        return numeric_responses

    def _calculate_nps_metrics(self, staff_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate Net Promoter Score from staff responses."""
        # NPS calculation logic (simplified placeholder)
        # Real implementation would extract NPS question and calculate score
        return {
            "score": 0,
            "promoters": 0,
            "passives": 0,
            "detractors": 0,
            "total_responses": len(staff_records),
        }

    def _extract_tech_insights(self, org_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract tech insights from all stakeholder groups (CEO, Tech Lead, Staff)."""
        tech_records = org_data.get("tech_records", [])
        ceo_record = org_data.get("ceo_record", {})
        staff_records = org_data.get("staff_records", [])

        # Tech Lead data
        tech_policies = None
        tech_challenges = None
        tech_priorities = None

        if tech_records:
            tech_policies_raw = tech_records[0].get("TL-I-6")
            if tech_policies_raw and str(tech_policies_raw).strip() != "0":
                tech_policies = tech_policies_raw

            tech_challenges = tech_records[0].get("TL-CTC")
            tech_priorities = tech_records[0].get("TL-TIP")  # Fixed typo: was "TLC-TIP"

        # CEO data
        ceo_challenges = ceo_record.get("C-TC") if ceo_record else None
        ceo_priorities = ceo_record.get("C-TIP") if ceo_record else None

        # Staff data (aggregate from all staff responses)
        staff_challenges = []
        staff_priorities = []
        for staff in staff_records:
            challenge = staff.get("S-CTC")
            if challenge and str(challenge).strip():
                staff_challenges.append(challenge)

            priority = staff.get("S-TIP")
            if priority and str(priority).strip():
                staff_priorities.append(priority)

        # Aggregate all responses for frequency counting
        # Combine CEO, Tech Lead, and all Staff responses into single lists
        all_challenges = []
        all_priorities = []
        total_respondents = 0

        # Add CEO responses
        if ceo_challenges and str(ceo_challenges).strip():
            all_challenges.extend(
                [c.strip() for c in str(ceo_challenges).split(" | ") if c.strip()]
            )
            total_respondents += 1

        # Add Tech Lead responses
        if tech_challenges and str(tech_challenges).strip():
            all_challenges.extend(
                [c.strip() for c in str(tech_challenges).split(" | ") if c.strip()]
            )
            total_respondents += 1

        # Add Staff responses
        for staff_challenge in staff_challenges:
            if staff_challenge and str(staff_challenge).strip():
                all_challenges.extend(
                    [c.strip() for c in str(staff_challenge).split(" | ") if c.strip()]
                )
                total_respondents += 1

        # Reset respondent count for priorities
        priority_respondents = 0

        # Add CEO priorities
        if ceo_priorities and str(ceo_priorities).strip():
            all_priorities.extend(
                [p.strip() for p in str(ceo_priorities).split(" | ") if p.strip()]
            )
            priority_respondents += 1

        # Add Tech Lead priorities
        if tech_priorities and str(tech_priorities).strip():
            all_priorities.extend(
                [p.strip() for p in str(tech_priorities).split(" | ") if p.strip()]
            )
            priority_respondents += 1

        # Add Staff priorities
        for staff_priority in staff_priorities:
            if staff_priority and str(staff_priority).strip():
                all_priorities.extend(
                    [p.strip() for p in str(staff_priority).split(" | ") if p.strip()]
                )
                priority_respondents += 1

        # Calculate frequency counts
        challenge_counts = {}
        for challenge in all_challenges:
            challenge_counts[challenge] = challenge_counts.get(challenge, 0) + 1

        priority_counts = {}
        for priority in all_priorities:
            priority_counts[priority] = priority_counts.get(priority, 0) + 1

        return {
            "policies": tech_policies,
            "challenges": {
                "ceo": ceo_challenges,
                "tech_lead": tech_challenges,
                "staf": staff_challenges,
                "aggregated_counts": challenge_counts,
                "total_respondents": total_respondents,
            },
            "priorities": {
                "ceo": ceo_priorities,
                "tech_lead": tech_priorities,
                "staf": staff_priorities,
                "aggregated_counts": priority_counts,
                "total_respondents": priority_respondents,
            },
        }

    def _generate_ai_insights(
        self, org_name: str, maturity_assessment: Dict[str, Any]
    ) -> tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
        """Generate AI-powered qualitative analysis."""
        ai_insights = None
        dimension_insights = None

        if not self._enable_ai or not self._ai_analyzer:
            return ai_insights, dimension_insights

        try:
            from src.analytics.ai_analyzer import extract_free_text_responses

            print(f"[OrganizationReportBuilder] Starting AI analysis for {org_name}")
            free_text_responses = extract_free_text_responses(
                self._data_service.get_all_data(), org_name
            )

            ai_insights = self._ai_analyzer.analyze_organization_qualitative(
                org_name, free_text_responses
            )

            # Consolidate AI dimension summaries
            if ai_insights and "dimensions" in ai_insights:
                for dimension, analysis in ai_insights["dimensions"].items():
                    if "summary" in analysis and analysis["summary"]:
                        analysis["summary"] = self._ai_analyzer.consolidate_text(
                            analysis["summary"], max_chars=120
                        )

            # Generate dimension insights
            dimension_insights = self._ai_analyzer.generate_dimension_insights(free_text_responses)

            # Generate aggregate summary
            if maturity_assessment:
                aggregate_summary = self._generate_aggregate_summary(
                    maturity_assessment, ai_insights, org_name, free_text_responses
                )
                maturity_assessment["aggregate_summary"] = aggregate_summary

        except Exception as e:
            print(f"[OrganizationReportBuilder] Warning: AI analysis failed for {org_name}: {e}")

        return ai_insights, dimension_insights

    def _generate_aggregate_summary(
        self,
        maturity_assessment: Dict[str, Any],
        ai_insights: Optional[Dict[str, Any]],
        org_name: str,
        free_text_responses: Dict[str, List[Dict[str, Any]]] = None,
    ) -> Optional[str]:
        """Generate aggregate summary combining quantitative and qualitative insights."""
        if not self._ai_analyzer:
            return None

        try:
            # Build summary context
            overall_score = maturity_assessment.get("overall_score", 0)
            maturity_level = maturity_assessment.get("maturity_level", "Unknown")

            summary_parts = [
                f"{org_name} demonstrates {maturity_level.lower()} technology maturity",
                f"with an overall score of {overall_score:.1f}/5.0.",
            ]

            # Add AI insights if available, but validate for hallucinated names
            if ai_insights and "summary" in ai_insights:
                ai_summary = ai_insights["summary"]

                # Extract valid respondent names from free text responses
                valid_respondents = []
                if free_text_responses:
                    for dimension_responses in free_text_responses.values():
                        for response in dimension_responses:
                            if isinstance(response, dict):
                                respondent = response.get("respondent")
                                if respondent and respondent not in valid_respondents:
                                    valid_respondents.append(str(respondent))

                # Validate narrative text for hallucinated names
                if valid_respondents:
                    validated_summary = self._ai_analyzer._validate_narrative_text(
                        ai_summary,
                        valid_respondents,
                        source_context=f"aggregate summary: {org_name}"
                    )
                    summary_parts.append(validated_summary)
                else:
                    # No respondents to validate against, use as-is
                    summary_parts.append(ai_summary)

            return " ".join(summary_parts)
        except Exception as e:
            print(f"[OrganizationReportBuilder] Error generating aggregate summary: {e}")
            return None

    def _build_header(self, org_name: str, intake_record: Dict[str, Any]) -> Dict[str, Any]:
        """Build organization report header section."""
        return {
            "organization_name": org_name,
            "intake_date": (
                intake_record.get("Date", "N/A")[:10] if intake_record.get("Date") else "N/A"
            ),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    def _build_timeline(self, org_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Build organization activity timeline."""
        timeline = []

        # Intake event
        if org_data["intake_record"].get("Date"):
            timeline.append(
                {
                    "date": org_data["intake_record"].get("Date", "")[:10],
                    "event_type": "Intake",
                    "description": "Organization intake completed",
                    "icon": "clipboard-check",
                    "color": "gray",
                }
            )

        # CEO survey event
        if org_data["ceo_record"] and org_data["ceo_record"].get("Date"):
            timeline.append(
                {
                    "date": org_data["ceo_record"].get("Date", "")[:10],
                    "event_type": "CEO Survey",
                    "description": f"{org_data['ceo_record'].get('Name', 'CEO')} completed survey",
                    "icon": "user-tie",
                    "color": "blue",
                }
            )

        # Tech Lead survey events
        for tech in org_data["tech_records"]:
            if tech.get("Date"):
                timeline.append(
                    {
                        "date": tech.get("Date", "")[:10],
                        "event_type": "Tech Lead Survey",
                        "description": f"{tech.get('Name', 'Tech Lead')} completed survey",
                        "icon": "laptop-code",
                        "color": "purple",
                    }
                )

        # Staff survey events
        for staff in org_data["staff_records"]:
            if staff.get("Date"):
                timeline.append(
                    {
                        "date": staff.get("Date", "")[:10],
                        "event_type": "Staff Survey",
                        "description": f"{staff.get('Name', 'Staff')} completed survey",
                        "icon": "users",
                        "color": "green",
                    }
                )

        # Sort by date descending
        timeline.sort(key=lambda x: x["date"], reverse=True)

        return timeline

    def _build_contacts(self, org_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Build organization contacts list."""
        contacts = []

        # CEO contact
        if org_data["ceo_record"]:
            contacts.append(
                {
                    "name": org_data["ceo_record"].get("Name", ""),
                    "email": org_data["ceo_record"].get("CEO Email", ""),
                    "role": org_data["ceo_record"].get("CEO Role", "CEO"),
                    "type": "CEO",
                    "survey_complete": bool(org_data["ceo_record"].get("Date")),
                    "submission_date": (
                        org_data["ceo_record"].get("Date", "")[:10]
                        if org_data["ceo_record"].get("Date")
                        else None
                    ),
                }
            )

        # Tech Lead contacts
        for tech in org_data["tech_records"]:
            contacts.append(
                {
                    "name": tech.get("Name", ""),
                    "email": tech.get("Login Email", ""),
                    "role": "Tech Lead",
                    "type": "Tech Lead",
                    "survey_complete": bool(tech.get("Date")),
                    "submission_date": tech.get("Date", "")[:10] if tech.get("Date") else None,
                }
            )

        # Staff contacts
        for staff in org_data["staff_records"]:
            contacts.append(
                {
                    "name": staff.get("Name", ""),
                    "email": staff.get("Login Email", ""),
                    "role": "Staff",
                    "type": "Staff",
                    "survey_complete": bool(staff.get("Date")),
                    "submission_date": staff.get("Date", "")[:10] if staff.get("Date") else None,
                }
            )

        return contacts

    def _build_intake_insights(self, intake_record: Dict[str, Any]) -> Dict[str, Any]:
        """Build intake information insights."""
        return {
            "ai_usage": intake_record.get(
                "Please select which of these best describes how AI is currently being used in your organization:",
                "Not specified",
            ),
            "ai_policy": intake_record.get("Do you have an AI policy in place?", "Not specified"),
            "comments": intake_record.get(
                "Do you have any suggestions or comments for us on the Technology Strategy?", ""
            ),
            "raw_data": intake_record,
        }

    def _build_responses(self, org_data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Build organization survey responses by category."""
        responses_by_category = defaultdict(list)

        # Process CEO responses
        if org_data["ceo_record"]:
            for key, value in org_data["ceo_record"].items():
                if key.startswith("C-") and value:
                    question_info = self._questions_lookup.get(key, {})
                    category = question_info.get("category", "General")

                    response = {
                        "question_id": key,
                        "question_text": question_info.get("question", key),
                        "answer_value": value,
                        "answer_text": self._get_answer_text(value, question_info),
                        "respondent": org_data["ceo_record"].get("Name", "CEO"),
                        "role": "CEO",
                    }
                    responses_by_category[category].append(response)

        # Process Tech responses
        for tech in org_data["tech_records"]:
            for key, value in tech.items():
                if key.startswith("TL-") and value:
                    question_info = self._questions_lookup.get(key, {})
                    category = question_info.get("category", "General")

                    response = {
                        "question_id": key,
                        "question_text": question_info.get("question", key),
                        "answer_value": value,
                        "answer_text": self._get_answer_text(value, question_info),
                        "respondent": tech.get("Name", "Tech Lead"),
                        "role": "Tech Lead",
                    }
                    responses_by_category[category].append(response)

        # Process Staff responses
        for staff in org_data["staff_records"]:
            for key, value in staff.items():
                if key.startswith("S-") and value:
                    question_info = self._questions_lookup.get(key, {})
                    category = question_info.get("category", "General")

                    response = {
                        "question_id": key,
                        "question_text": question_info.get("question", key),
                        "answer_value": value,
                        "answer_text": self._get_answer_text(value, question_info),
                        "respondent": staff.get("Name", "Staff"),
                        "role": "Staff",
                    }
                    responses_by_category[category].append(response)

        return dict(responses_by_category)

    def _build_export_data(self, org_name: str) -> Dict[str, Any]:
        """Build export metadata for organization."""
        return {
            "organization_name": org_name,
            "export_timestamp": datetime.now().isoformat(),
            "formats_available": ["PDF", "CSV", "JSON"],
        }

    def _get_answer_text(self, value: Any, question_info: Dict[str, Any]) -> str:
        """Get answer text from answer keys."""
        try:
            answer_keys = question_info.get("answer_keys", {})
            numeric_value = int(float(str(value)))
            return answer_keys.get(numeric_value, str(value))
        except (ValueError, TypeError):
            return str(value)

    def _calculate_overall_score_checksum(
        self, dimensions: List[Dict], overall_score: float
    ) -> Dict:
        """
        Calculate checksum for overall weighted score across all dimensions.

        Validates: overall_score = sum(dimension_score * weight) / sum(weights)

        Args:
            dimensions: List of dimension analysis dictionaries
            overall_score: Overall maturity score to validate

        Returns:
            Dict with checksum, validation result, and calculation details
        """
        import hashlib

        # Extract dimension scores and weights
        dimension_data = []
        total_weight = 0
        weighted_sum = 0

        for dim in dimensions:
            dimension_name = dim.get("dimension", "Unknown")
            # Use adjusted_score if present, otherwise use weighted_score
            score = dim.get("adjusted_score", dim.get("weighted_score", 0))
            weight = self._rubric.DIMENSION_WEIGHTS.get(dimension_name, 0.20)

            dimension_data.append(
                {
                    "name": dimension_name,
                    "score": score,
                    "weight": weight,
                    "contribution": score * weight,
                }
            )
            weighted_sum += score * weight
            total_weight += weight

        # Calculate expected overall score
        expected_overall = weighted_sum / total_weight if total_weight > 0 else 0

        # Generate calculation string for checksum
        calc_parts = [f"{d['score']:.2f}*{d['weight']:.2f}" for d in dimension_data]
        calculation = f"({' + '.join(calc_parts)}) / {total_weight:.2f} = {expected_overall:.2f}"

        # Generate checksum
        checksum_input = f"{calculation}|{overall_score:.2f}"
        checksum = hashlib.md5(checksum_input.encode()).hexdigest()[:8]

        # Validation
        error = abs(expected_overall - overall_score)
        is_valid = error < 0.01  # Allow 0.01 rounding error

        return {
            "checksum": checksum,
            "calculation": calculation,
            "formula": "weighted_average(dimension_scores, weights)",
            "valid": is_valid,
            "expected": round(expected_overall, 2),
            "actual": round(overall_score, 2),
            "error": round(error, 4),
            "components": dimension_data,
            "total_weight": round(total_weight, 2),
        }

    def _calculate_modifier_chain_checksum(self, modifiers: List[Dict]) -> Dict:
        """
        Calculate checksum for modifier chain validation.

        Validates: total_modifier = sum(individual_modifier_values)

        Args:
            modifiers: List of modifier dictionaries

        Returns:
            Dict with checksum, validation, and modifier breakdown
        """
        import hashlib

        modifier_breakdown = []
        total = 0

        for mod in modifiers:
            value = mod.get("value", 0)
            source = "admin" if mod.get("is_admin_edit") else "ai"
            modifier_breakdown.append(
                {
                    "respondent": mod.get("respondent", "Unknown"),
                    "role": mod.get("role", "Unknown"),
                    "value": value,
                    "source": source,
                    "factor": mod.get("factor", ""),
                }
            )
            total += value

        # Generate calculation string
        values_str = " + ".join([f"{m['value']}" for m in modifier_breakdown])
        calculation = f"{values_str} = {total:.2f}" if values_str else "0 = 0"

        # Generate checksum
        checksum_input = f"{calculation}|{len(modifiers)}"
        checksum = hashlib.md5(checksum_input.encode()).hexdigest()[:8]

        return {
            "checksum": checksum,
            "calculation": calculation,
            "formula": "sum(modifier_values)",
            "total_modifier": round(total, 2),
            "modifier_count": len(modifiers),
            "non_zero_count": sum(1 for m in modifier_breakdown if m["value"] != 0),
            "admin_count": sum(1 for m in modifier_breakdown if m["source"] == "admin"),
            "ai_count": sum(1 for m in modifier_breakdown if m["source"] == "ai"),
            "modifiers": modifier_breakdown,
        }


# Global singleton instance
_org_report_builder_instance: Optional[OrganizationReportBuilder] = None
_instance_lock = threading.RLock()


def get_organization_report_builder(
    data_service=None,
    cache_service=None,
    admin_edit_service=None,
    report_repository=None,
    questions_lookup: Optional[Dict[str, Dict[str, Any]]] = None,
    enable_ai: bool = True,
) -> OrganizationReportBuilder:
    """
    Get singleton organization report builder instance.

    Args:
        data_service: Optional DataService instance (uses singleton if None)
        cache_service: Optional CacheService instance (uses singleton if None)
        admin_edit_service: Optional AdminEditService instance (uses singleton if None)
        report_repository: Optional ReportRepository instance (uses singleton if None)
        questions_lookup: Optional pre-built questions lookup
        enable_ai: Enable AI-powered analysis

    Returns:
        Singleton OrganizationReportBuilder instance
    """
    global _org_report_builder_instance

    if _org_report_builder_instance is None:
        with _instance_lock:
            if _org_report_builder_instance is None:
                # Import singletons if not provided
                if data_service is None:
                    from src.services.data_service import get_data_service

                    data_service = get_data_service()

                if cache_service is None:
                    from src.services.cache_service import get_cache_service

                    cache_service = get_cache_service()

                if admin_edit_service is None:
                    from src.services.admin_edit_service import get_admin_edit_service

                    admin_edit_service = get_admin_edit_service()

                if report_repository is None:
                    from src.repositories.report_repository import get_report_repository

                    report_repository = get_report_repository()

                _org_report_builder_instance = OrganizationReportBuilder(
                    data_service,
                    cache_service,
                    admin_edit_service,
                    report_repository,
                    questions_lookup,
                    enable_ai,
                )

    return _org_report_builder_instance
