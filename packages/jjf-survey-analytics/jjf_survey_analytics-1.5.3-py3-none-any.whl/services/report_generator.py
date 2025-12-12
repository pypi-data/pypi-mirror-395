"""
Report Generator for JJF Survey Analytics
Generates per-organization and aggregate reports
"""

from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from src.analytics.ai_analyzer import AIAnalyzer, extract_free_text_responses
from src.analytics.maturity_rubric import MaturityRubric


class ReportGenerator:
    """Generates reports for survey analytics data."""

    def __init__(
        self,
        sheet_data: Dict[str, List[Dict[str, Any]]],
        enable_ai: bool = True,
        admin_edits: Dict[str, Any] = None,
        progress_callback=None,
    ):
        """
        Initialize report generator with sheet data and optional admin edits.

        Args:
            sheet_data: Dictionary containing all tab data from Google Sheets
            enable_ai: Whether to enable AI-powered qualitative analysis
            admin_edits: Dictionary containing admin edits for all organizations
            progress_callback: Optional callback function(progress_pct, message)
        """
        self.sheet_data = sheet_data
        self.questions_lookup = self._build_questions_lookup()
        self.rubric = MaturityRubric()
        self.enable_ai = enable_ai
        self.admin_edits = admin_edits or {}
        self.progress_callback = progress_callback

        # Initialize AI analyzer if enabled
        self.ai_analyzer = None
        if self.enable_ai:
            try:
                self.ai_analyzer = AIAnalyzer()
                print("[ReportGenerator] AI analyzer initialized successfully")
            except Exception as e:
                print(f"Warning: AI analyzer not available: {e}")
                self.enable_ai = False

        # Initialize OrganizationReportBuilder for checksum methods
        # Note: This is a minimal initialization just for verification methods
        # Full report building uses the refactored OrganizationReportBuilder separately
        from src.services.organization_report_builder import OrganizationReportBuilder

        self._org_report_builder = OrganizationReportBuilder(
            data_service=None,  # Not needed for checksum methods
            cache_service=None,  # Not needed for checksum methods
            admin_edit_service=None,  # Not needed for checksum methods
            report_repository=None,  # Not needed for checksum methods
            questions_lookup=self.questions_lookup,
            enable_ai=False,  # Not needed for checksum methods
        )

    def _build_questions_lookup(self) -> Dict[str, Dict[str, Any]]:
        """Build lookup dictionary for questions and answer keys."""
        questions = {}
        questions_data = self.sheet_data.get("Questions", [])

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

    def _extract_numeric_responses(self, record: Dict[str, Any]) -> Dict[str, float]:
        """Extract numeric responses (ignoring text/open-ended)."""
        numeric_responses = {}

        for key, value in record.items():
            if key.startswith(("C-", "TL-", "S-")) and value:
                try:
                    # Try to convert to float
                    num_value = float(str(value).strip())
                    # Only include if it's a valid rating (0-5, excluding 6 which is N/A)
                    if 0 <= num_value <= 5:
                        numeric_responses[key] = num_value
                except (ValueError, TypeError):
                    # Skip text responses
                    continue

        return numeric_responses

    def generate_organization_report(
        self, org_name: str, skip_ai: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Generate comprehensive report for a single organization.

        Args:
            org_name: Organization name
            skip_ai: If True, skip AI analysis (for instant page load with progressive loading)

        Returns:
            Dictionary containing report data with maturity assessment
        """
        # Find intake record
        intake_data = self.sheet_data.get("Intake", [])
        intake_record = None
        for row in intake_data:
            if row.get("Organization Name:") == org_name:
                intake_record = row
                break

        if not intake_record:
            return None

        # Get CEO data
        ceo_data = self.sheet_data.get("CEO", [])
        ceo_record = None
        for row in ceo_data:
            if row.get("CEO Organization") == org_name:
                ceo_record = row
                break

        # Get Tech data
        tech_data = self.sheet_data.get("Tech", [])
        tech_records = [row for row in tech_data if row.get("Organization") == org_name]

        # Get Staff data
        staff_data = self.sheet_data.get("Staff", [])
        staff_records = [row for row in staff_data if row.get("Organization") == org_name]

        # Calculate Net Promoter Score from staff
        nps_metrics = self._calculate_nps_metrics(staff_records)

        # Extract tech insights with aggregation from all stakeholders
        # This creates the aggregated_counts structure needed by the template
        tech_insights = self._extract_tech_insights_aggregated(
            ceo_record, tech_records, staff_records
        )

        # Calculate maturity assessment
        org_responses = {
            "CEO": self._extract_numeric_responses(ceo_record) if ceo_record else {},
            "Tech": self._extract_numeric_responses(tech_records[0]) if tech_records else {},
            "Staff": self._extract_numeric_responses(staff_records[0]) if staff_records else {},
        }

        maturity_assessment = self.rubric.calculate_overall_maturity(org_responses)

        # AI-powered qualitative analysis
        ai_insights = None
        dimension_insights = None
        if self.enable_ai and self.ai_analyzer and not skip_ai:
            try:
                print(f"[AI] Starting qualitative analysis for {org_name}")

                # Update progress before extracting responses
                if self.progress_callback:
                    self.progress_callback(30, "Extracting free text responses...")

                free_text_responses = extract_free_text_responses(self.sheet_data, org_name)
                print(
                    f"[AI] Extracted {sum(len(responses) for responses in free_text_responses.values())} free text responses"
                )

                ai_insights = self.ai_analyzer.analyze_organization_qualitative(
                    org_name, free_text_responses, progress_callback=self.progress_callback
                )
                print(f"[AI] Completed qualitative analysis for {org_name}")

                # Update progress for consolidation
                if self.progress_callback:
                    self.progress_callback(60, "Consolidating dimension summaries...")

                # Consolidate AI dimension summaries
                if ai_insights and "dimensions" in ai_insights:
                    for dimension, analysis in ai_insights["dimensions"].items():
                        if "summary" in analysis and analysis["summary"]:
                            # Target 120 characters for dimension summaries
                            analysis["summary"] = self.ai_analyzer.consolidate_text(
                                analysis["summary"], max_chars=120
                            )
                print(f"[AI] Consolidated dimension summaries for {org_name}")

                # Update progress for insights generation
                if self.progress_callback:
                    self.progress_callback(65, "Generating dimension insights...")

                # Generate grantee-friendly dimension insights
                print(f"[AI] Generating dimension insights for {org_name}")
                dimension_insights = self.ai_analyzer.generate_dimension_insights(
                    free_text_responses
                )
                print(f"[AI] Generated {len(dimension_insights)} dimension insights")

                # Phase 1 MVC Refactoring: Pre-calculate modifier summaries
                print(f"[MVC] Pre-calculating modifier summaries for {org_name}")
                self._precalculate_modifier_summaries(ai_insights, maturity_assessment)
                print("[MVC] Completed modifier summary pre-calculation")

            except Exception as e:
                print(f"Warning: AI analysis failed for {org_name}: {e}")
                import traceback

                traceback.print_exc()
                ai_insights = None
                dimension_insights = None

        # Ensure ai_insights structure exists for admin edits and debug section
        # Even when AI generation is skipped, we need the dimensions dict
        # so that admin edits can populate modifiers
        if ai_insights is None:
            ai_insights = {"dimensions": {}, "summary": None, "recommendations": []}

        # Consolidate maturity description if AI is available
        if self.enable_ai and self.ai_analyzer and maturity_assessment.get("maturity_description"):
            try:
                # Target 55 characters for overall description
                maturity_assessment["maturity_description"] = self.ai_analyzer.consolidate_text(
                    maturity_assessment["maturity_description"], max_chars=55
                )
            except Exception as e:
                print(f"Warning: Could not consolidate maturity description: {e}")

        # Generate aggregate summary if AI is available
        if self.enable_ai and self.ai_analyzer and maturity_assessment:
            try:
                aggregate_summary = self._generate_aggregate_summary(
                    maturity_assessment, ai_insights, org_name
                )
                maturity_assessment["aggregate_summary"] = aggregate_summary
            except Exception as e:
                print(f"Warning: Could not generate aggregate summary: {e}")
                maturity_assessment["aggregate_summary"] = None

        # Build report sections
        report = {
            "header": self._build_org_header(org_name, intake_record),
            "maturity": maturity_assessment,  # Quantitative maturity assessment
            "nps": nps_metrics,  # Net Promoter Score from staff
            "tech_insights": tech_insights,  # Tech insights with aggregated counts (quantitative)
            "ai_insights": ai_insights,  # NEW: Qualitative AI analysis with modifiers
            "dimension_insights": dimension_insights,  # NEW: Grantee-friendly dimension summaries
            "timeline": self._build_org_timeline(
                intake_record, ceo_record, tech_records, staff_records
            ),
            "contacts": self._build_org_contacts(ceo_record, tech_records, staff_records),
            "intake": self._build_org_intake_insights(intake_record),
            "responses": self._build_org_responses(ceo_record, tech_records, staff_records),
            "export": self._build_org_export_data(org_name),
        }

        # Calculate and apply ALL modifiers (admin + AI) in one centralized location
        # This is the single source of truth for modifier calculation
        if "maturity" in report and "variance_analysis" in report["maturity"]:
            org_edits = self.admin_edits.get(org_name) if self.admin_edits else None
            self._calculate_and_apply_all_modifiers(
                org_name=org_name,
                variance_analysis=report["maturity"]["variance_analysis"],
                admin_edits=org_edits,
                ai_insights=ai_insights,
            )

        # Apply non-score admin edits (summary, dimension insights)
        report = self._apply_admin_edits(org_name, report)

        # Add dimension weights to all dimensions
        self._add_checksums_to_dimensions(report)

        # Recalculate overall maturity score after modifiers applied
        self._recalculate_overall_score(report)

        # Phase 1 MVC: Recalculate modifier summaries (reads adjusted_score from variance_analysis)
        # This must run AFTER checksums so adjusted_score is correctly calculated
        if report.get("ai_insights") and report.get("maturity"):
            print(f"[MVC] Recalculating modifier summaries for {org_name}")
            self._precalculate_modifier_summaries(report["ai_insights"], report["maturity"])

        # Update progress for completion
        if self.progress_callback:
            self.progress_callback(75, "AI analysis complete")

        # Phase 2 MVC: Add verification results to report metadata
        report["verification"] = self.verify_report_calculations(report)

        # Log any validation errors
        if not report["verification"]["valid"]:
            print(f"[Report Generator] VALIDATION ERRORS in {org_name} report:")
            for error in report["verification"]["errors"]:
                print(f"  - {error}")
        else:
            print(
                f"[Phase 2] Report verification passed: {report['verification']['dimensions_valid']}/{report['verification']['dimensions_checked']} dimensions valid"
            )

        return report

    def _calculate_and_apply_all_modifiers(
        self,
        org_name: str,
        variance_analysis: Dict[str, Any],
        admin_edits: Optional[Dict[str, Any]],
        ai_insights: Optional[Dict[str, Any]],
    ) -> None:
        """
        Single source of truth for all modifier calculations.

        Centralized logic for:
        - Collecting admin edit modifiers (from Google Sheets manual adjustments)
        - Collecting AI-generated modifiers (from OpenRouter analysis)
        - Applying floating point tolerance throughout (0.001)
        - Calculating adjusted_score = max(0, min(5, weighted_score + total_modifier))
        - Generating checksums for verification

        Modifier Priority:
        - Admin edits take precedence over AI modifiers
        - If admin edit exists for a dimension, AI modifiers are ignored
        - If no admin edit, AI modifiers are applied
        - Default modifier is 0 if neither admin nor AI modifiers exist

        Floating Point Handling:
        - All comparisons use tolerance: abs(value) < 0.001
        - Modifier sums < 0.001 are treated as 0

        Score Clamping:
        - All adjusted scores clamped to [0, 5] range
        - Formula: adjusted_score = max(0, min(5, base_score + total_modifier))

        Args:
            org_name: Organization name (for logging)
            variance_analysis: Dict with weighted scores per dimension (modified in-place)
            admin_edits: Dict of manual admin adjustments (or None)
            ai_insights: Dict with AI-generated modifiers per dimension (or None)

        Side Effects:
            Modifies variance_analysis in-place, adding:
            - total_modifier: Sum of all modifiers applied
            - adjusted_score: Final score after applying modifiers
            - checksum: Verification data for calculation correctness

        Example:
            Given dimension "Technology Strategy" with weighted_score=3.5:
            - Admin edits: [{id: 0, value: 0.3}, {id: 1, value: -0.2}]
            - Result: total_modifier=0.1, adjusted_score=3.6
        """
        if not variance_analysis:
            return

        print(f"[Modifier Calculation] Processing modifiers for {org_name}")

        # Get admin score modifiers if they exist
        admin_score_modifiers = {}
        if admin_edits and "score_modifiers" in admin_edits:
            admin_score_modifiers = admin_edits["score_modifiers"]

        # Get AI dimension modifiers if they exist
        ai_dimension_modifiers = {}
        if ai_insights and "dimensions" in ai_insights:
            ai_dimension_modifiers = ai_insights["dimensions"]

        # Process each dimension in variance analysis
        for dimension_name, analysis in variance_analysis.items():
            base_score = analysis.get("weighted_score", 0)

            # Convert dimension name to admin edits format (spaces to underscores)
            admin_key = dimension_name.replace(" ", "_")

            # Collect admin modifiers for this dimension
            admin_modifiers = []
            if admin_key in admin_score_modifiers:
                admin_modifiers = admin_score_modifiers[admin_key]

            # Collect AI modifiers for this dimension
            ai_modifiers = []
            if dimension_name in ai_dimension_modifiers:
                ai_modifiers = ai_dimension_modifiers[dimension_name].get("modifiers", [])

            # Calculate total modifier with priority logic
            total_modifier = 0.0
            modifier_source = "none"

            if admin_modifiers:
                # Admin edits take precedence
                total_modifier = sum(mod.get("value", 0) for mod in admin_modifiers)
                modifier_source = "admin"
                print(
                    f"[Modifier Calculation] {dimension_name}: Using admin modifiers ({len(admin_modifiers)} modifiers, total={total_modifier:.3f})"
                )
            elif ai_modifiers:
                # Use AI modifiers if no admin edits
                total_modifier = sum(mod.get("value", 0) for mod in ai_modifiers)
                modifier_source = "ai"
                print(
                    f"[Modifier Calculation] {dimension_name}: Using AI modifiers ({len(ai_modifiers)} modifiers, total={total_modifier:.3f})"
                )

                # === DEBUG LOGGING (START) ===
                print(f"[DEBUG] {dimension_name}: total_modifier calculated = {total_modifier}")
                print(f"[DEBUG] {dimension_name}: Individual values = {[mod.get('value', 0) for mod in ai_modifiers]}")
                # === DEBUG LOGGING (END) ===
            else:
                print(f"[Modifier Calculation] {dimension_name}: No modifiers found (default=0)")

            # Apply floating point tolerance
            if abs(total_modifier) < 0.001:
                total_modifier = 0.0
                if modifier_source != "none":
                    print(
                        f"[Modifier Calculation] {dimension_name}: Modifier sum < tolerance, setting to 0"
                    )

            # FIX ISSUE 1: Calculate adjusted score with clamping [0, 5]
            # CRITICAL: This adjusted_score MUST be applied to dimension BEFORE adding to overall
            adjusted_score = max(0, min(5, base_score + total_modifier))

            # Store results in variance analysis
            # IMPORTANT: adjusted_score will be used by calculate_overall_score_from_dimensions()
            analysis["total_modifier"] = total_modifier
            analysis["adjusted_score"] = adjusted_score
            analysis["modifier_source"] = modifier_source

            # Generate checksum for verification
            analysis["checksum"] = self._calculate_dimension_checksum(analysis)

            # Enhanced logging to verify modifier application
            dimension_weight = MaturityRubric.DIMENSION_WEIGHTS.get(dimension_name, 0.20)
            base_contribution = base_score * dimension_weight
            adjusted_contribution = adjusted_score * dimension_weight
            print(
                f"[Modifier Calculation] {dimension_name}:\n"
                f"  - Base Score: {base_score:.2f}\n"
                f"  - Total Modifier: {total_modifier:+.2f}\n"
                f"  - Adjusted Score: {adjusted_score:.2f} (MODIFIED!)\n"
                f"  - Dimension Weight: {dimension_weight:.2f}\n"
                f"  - Base Contribution to Overall: {base_contribution:.4f}\n"
                f"  - Adjusted Contribution to Overall: {adjusted_contribution:.4f}\n"
                f"  - Impact: {adjusted_contribution - base_contribution:+.4f} pts\n"
                f"  - Source: {modifier_source}, Valid: {analysis['checksum']['valid']}"
            )

    def _apply_admin_edits(self, org_name: str, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply non-score admin edits to the generated report.

        This method ONLY handles:
        - Custom summary titles and bodies
        - Custom dimension insights

        Score modifier logic has been moved to _calculate_and_apply_all_modifiers()
        """
        if not self.admin_edits or org_name not in self.admin_edits:
            return report

        org_edits = self.admin_edits[org_name]
        print(f"[Admin Edits] Applying non-score edits for {org_name}")

        # Apply summary edits
        if org_edits.get("summary_title"):
            if "summary" not in report:
                report["summary"] = {}
            report["summary"]["title"] = org_edits["summary_title"]
            print(f"[Admin Edits] Applied custom summary title: {org_edits['summary_title']}")

        if org_edits.get("summary_body"):
            if "summary" not in report:
                report["summary"] = {}
            report["summary"]["body"] = org_edits["summary_body"]
            print("[Admin Edits] Applied custom summary body")

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
                    print(f"[Admin Edits] Applied custom dimension insight for {dimension}")
                else:
                    # Add new dimension insight if it doesn't exist
                    report["dimension_insights"][dimension] = custom_insight
                    print(f"[Admin Edits] Added new custom dimension insight for {dimension}")

        # Update AI insights modifier values if admin edits exist
        # This ensures the UI displays the correct modifier values
        if "score_modifiers" in org_edits and "ai_insights" in report and report["ai_insights"]:
            score_modifiers = org_edits["score_modifiers"]
            ai_dimensions = report["ai_insights"].get("dimensions", {})

            for dimension, modifiers in score_modifiers.items():
                dimension_key = dimension.replace("_", " ")

                if dimension_key in ai_dimensions:
                    ai_modifiers = ai_dimensions[dimension_key].get("modifiers", [])

                    # Update modifier values based on admin edits
                    for modifier_edit in modifiers:
                        modifier_id = modifier_edit.get("id")
                        new_value = modifier_edit.get("value", 0)

                        if modifier_id is not None and modifier_id < len(ai_modifiers):
                            ai_modifiers[modifier_id]["value"] = new_value
                            print(
                                f"[Admin Edits] Updated {dimension_key} modifier {modifier_id} to {new_value}"
                            )

        return report

    # Removed: _apply_ai_modifiers_to_variance_analysis()
    # Logic consolidated into _calculate_and_apply_all_modifiers()

    def _recalculate_overall_score(self, report: Dict[str, Any]) -> None:
        """
        Recalculate overall maturity score based on adjusted dimension scores.

        FIX ISSUE 1: This method uses adjusted_score (with modifiers) from variance_analysis,
        NOT base weighted_score. The overall score calculation applies dimension weights
        to MODIFIED dimension scores.
        """
        if "maturity" not in report or "variance_analysis" not in report["maturity"]:
            return

        # Use centralized calculation method (single source of truth)
        from src.analytics.maturity_rubric import MaturityRubric

        variance_analysis = report["maturity"]["variance_analysis"]

        # Enhanced logging to verify adjusted_score is being used
        print("[Overall Score Recalculation] Using adjusted scores:")
        for dimension, analysis in variance_analysis.items():
            base_score = analysis.get("weighted_score", 0)
            adjusted_score = analysis.get("adjusted_score", base_score)
            modifier = analysis.get("total_modifier", 0)
            print(f"  - {dimension}: base={base_score:.2f}, modifier={modifier:+.2f}, adjusted={adjusted_score:.2f}")

        new_overall_score = MaturityRubric.calculate_overall_score_from_dimensions(variance_analysis)
        report["maturity"]["overall_score"] = new_overall_score
        print(f"[Overall Score] Recalculated with MODIFIED dimension scores: {new_overall_score:.2f}")

    def _precalculate_modifier_summaries(
        self, ai_insights: Optional[Dict[str, Any]], maturity_assessment: Dict[str, Any]
    ) -> None:
        """
        Phase 1 MVC Refactoring: Pre-calculate all modifier summaries in backend.
        Template should ONLY render pre-calculated values.

        Calculates:
        - modifier_summary: Total modifier value, count, individual values, has_modifiers flag
        - impact_summary: Base score, adjusted score, dimension weight, score delta, overall impact
        - total_impact_summary: Aggregate impact across all dimensions
        """
        if not ai_insights or "dimensions" not in ai_insights:
            return

        variance_analysis = maturity_assessment.get("variance_analysis", {})
        if not variance_analysis:
            return

        # Phase 4: Use single source of truth for dimension weights
        from src.analytics.maturity_rubric import MaturityRubric

        dimension_weights = MaturityRubric.DIMENSION_WEIGHTS

        # Initialize total impact tracking
        total_impact_summary = {
            "total_positive_impact": 0.0,
            "total_negative_impact": 0.0,
            "net_impact": 0.0,
            "dimensions_affected": 0,
            "total_modifiers": 0,
            "total_modifier_value": 0.0,
        }

        # Pre-calculate for each dimension
        for dimension, insights in ai_insights["dimensions"].items():
            modifiers = insights.get("modifiers", [])

            # Calculate modifier summary
            total_modifier = sum(m.get("value", 0) for m in modifiers)
            individual_values = [m.get("value", 0) for m in modifiers]

            insights["modifier_summary"] = {
                "total_modifier": total_modifier,
                "modifier_count": len(modifiers),
                "individual_values": individual_values,
                "has_modifiers": len(modifiers) > 0,
            }

            # Calculate impact on overall score
            # Get dimension weight (always set this, even if not in variance_analysis)
            weight = dimension_weights.get(dimension, 0.20)

            # Get scores from variance_analysis if available, otherwise use defaults
            if dimension in variance_analysis:
                variance = variance_analysis[dimension]
                base_score = variance.get("weighted_score", 0.0)
                adjusted_score = variance.get("adjusted_score", base_score)
            else:
                # Dimension not in variance_analysis - use defaults
                base_score = 0.0
                adjusted_score = 0.0

            score_delta = adjusted_score - base_score
            overall_impact = score_delta * weight
            weighted_contribution = adjusted_score * weight

            # ALWAYS set impact_summary for all dimensions (fixes 0% weight bug)
            insights["impact_summary"] = {
                "base_score": base_score,
                "adjusted_score": adjusted_score,
                "dimension_weight": weight,  # Always 0.20 (20%) from DIMENSION_WEIGHTS
                "score_delta": score_delta,
                "overall_impact": overall_impact,
                "weighted_contribution": weighted_contribution,
            }

            # Accumulate for total impact summary (only if dimension in variance_analysis)
            if dimension in variance_analysis and len(modifiers) > 0:
                if overall_impact > 0:
                    total_impact_summary["total_positive_impact"] += overall_impact
                elif overall_impact < 0:
                    total_impact_summary["total_negative_impact"] += overall_impact

                total_impact_summary["net_impact"] += overall_impact
                total_impact_summary["dimensions_affected"] += 1
                total_impact_summary["total_modifiers"] += len(modifiers)
                total_impact_summary["total_modifier_value"] += total_modifier

        # Store total impact summary at top level
        ai_insights["total_impact_summary"] = total_impact_summary

        print(f"[MVC] Pre-calculated summaries for {len(ai_insights['dimensions'])} dimensions")
        print(
            f"[MVC] Total impact: {total_impact_summary['net_impact']:.3f} across {total_impact_summary['dimensions_affected']} dimensions"
        )

    def _add_checksums_to_dimensions(self, report: Dict[str, Any]) -> None:
        """
        Add dimension weights to all dimensions in variance analysis.

        NOTE: This method only adds dimension_weight now.
        Checksums and adjusted_score calculation are handled by _calculate_and_apply_all_modifiers().

        Args:
            report: Organization report dictionary
        """
        if "maturity" not in report or "variance_analysis" not in report["maturity"]:
            return

        # Phase 4: Use single source of truth for dimension weights
        from src.analytics.maturity_rubric import MaturityRubric

        dimension_weights = MaturityRubric.DIMENSION_WEIGHTS

        for dimension, analysis in report["maturity"]["variance_analysis"].items():
            # Phase 4: Add dimension weight to analysis (pre-calculated for template)
            analysis["dimension_weight"] = dimension_weights.get(dimension, 0.20)

    def _calculate_dimension_checksum(self, dimension_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate verification checksum for dimension score calculation.

        Validates that adjusted_score = max(0, min(5, base_score + total_modifier))

        Args:
            dimension_analysis: Dimension variance analysis dictionary

        Returns:
            Dictionary containing checksum, validation status, and debugging info
        """
        import hashlib

        # Extract calculation components
        base_score = dimension_analysis.get("weighted_score", 0)
        total_modifier = dimension_analysis.get("total_modifier", 0)
        adjusted_score = dimension_analysis.get("adjusted_score", 0)

        # Calculate expected result
        expected_score = max(0, min(5, base_score + total_modifier))

        # Calculate error (should be ~0 for correct calculations)
        error = abs(adjusted_score - expected_score)
        is_valid = error < 0.001  # Allow tiny floating point errors

        # Create human-readable calculation string
        calculation_str = f"{base_score:.2f} + {total_modifier:.2f} = {adjusted_score:.2f}"
        formula_str = f"max(0, min(5, {base_score:.2f} + {total_modifier:.2f}))"

        # Generate checksum from calculation components
        checksum_input = f"{base_score}|{total_modifier}|{adjusted_score}"
        checksum = hashlib.md5(checksum_input.encode()).hexdigest()[:8]

        return {
            "checksum": checksum,
            "calculation": calculation_str,
            "formula": formula_str,
            "valid": is_valid,
            "expected": round(expected_score, 2),
            "actual": round(adjusted_score, 2),
            "error": round(error, 4),
            "components": {
                "base_score": round(base_score, 2),
                "total_modifier": round(total_modifier, 2),
                "adjusted_score": round(adjusted_score, 2),
            },
        }

    def verify_report_calculations(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify all score calculations in report are mathematically correct.

        Args:
            report: Complete organization report dictionary

        Returns:
            Validation results with any errors found
        """
        results = {
            "valid": True,
            "dimensions_checked": 0,
            "dimensions_valid": 0,
            "dimensions_invalid": 0,
            "errors": [],
            "warnings": [],
        }

        if "maturity" not in report or "variance_analysis" not in report["maturity"]:
            results["valid"] = False
            results["errors"].append("Missing maturity variance analysis")
            return results

        # Phase 3: Add overall score checksum
        if "overall_score" in report["maturity"]:
            # Build dimensions list for checksum calculation
            dimensions_list = []
            for dim_name, analysis in report["maturity"]["variance_analysis"].items():
                dimensions_list.append(
                    {
                        "dimension": dim_name,
                        "adjusted_score": analysis.get(
                            "adjusted_score", analysis.get("weighted_score", 0)
                        ),
                        "weighted_score": analysis.get("weighted_score", 0),
                    }
                )

            # Calculate overall score checksum using organization_report_builder
            overall_checksum = self._org_report_builder._calculate_overall_score_checksum(
                dimensions=dimensions_list, overall_score=report["maturity"]["overall_score"]
            )
            results["overall_score_checksum"] = overall_checksum

            # Validate overall score
            if not overall_checksum["valid"]:
                results["valid"] = False
                results["errors"].append(
                    {
                        "type": "overall_score",
                        "expected": overall_checksum["expected"],
                        "actual": overall_checksum["actual"],
                        "error": overall_checksum["error"],
                        "formula": overall_checksum["formula"],
                    }
                )

        # Phase 3: Add modifier chain checksums for each dimension
        results["modifier_chain_checksums"] = {}

        # Check each dimension
        for dimension, analysis in report["maturity"]["variance_analysis"].items():
            results["dimensions_checked"] += 1

            if "checksum" not in analysis:
                results["warnings"].append(f"{dimension}: No checksum available")
                continue

            checksum = analysis["checksum"]

            if checksum["valid"]:
                results["dimensions_valid"] += 1
            else:
                results["dimensions_invalid"] += 1
                results["valid"] = False
                results["errors"].append(
                    {
                        "dimension": dimension,
                        "expected": checksum["expected"],
                        "actual": checksum["actual"],
                        "error": checksum["error"],
                        "formula": checksum["formula"],
                    }
                )

            # Phase 3: Calculate modifier chain checksum for this dimension
            # Get modifiers from ai_insights if available
            modifiers = []
            if (
                report.get("ai_insights")
                and report["ai_insights"].get("dimensions")
                and dimension in report["ai_insights"]["dimensions"]
            ):
                modifiers = report["ai_insights"]["dimensions"][dimension].get(
                    "modifiers", []
                )

            if modifiers:
                modifier_checksum = self._org_report_builder._calculate_modifier_chain_checksum(
                    modifiers
                )
                results["modifier_chain_checksums"][dimension] = modifier_checksum

        return results

    def generate_aggregate_report(self) -> Dict[str, Any]:
        """
        Generate aggregate report across all organizations.

        Returns:
            Dictionary containing aggregate report data with 7 sections
        """
        intake_data = self.sheet_data.get("Intake", [])
        ceo_data = self.sheet_data.get("CEO", [])
        tech_data = self.sheet_data.get("Tech", [])
        staff_data = self.sheet_data.get("Staff", [])

        report = {
            "header": self._build_aggregate_header(),
            "overview": self._build_aggregate_overview(
                intake_data, ceo_data, tech_data, staff_data
            ),
            "breakdown": self._build_aggregate_breakdown(ceo_data, tech_data, staff_data),
            "timeline": self._build_aggregate_timeline(
                intake_data, ceo_data, tech_data, staff_data
            ),
            "table": self._build_aggregate_table(intake_data, ceo_data, tech_data, staff_data),
            "insights": self._build_aggregate_insights(ceo_data, tech_data, staff_data),
            "recommendations": self._build_aggregate_recommendations(
                intake_data, ceo_data, tech_data, staff_data
            ),
        }

        return report

    # Organization Report Section Builders

    def _build_org_header(self, org_name: str, intake_record: Dict) -> Dict[str, Any]:
        """Build organization report header section."""
        return {
            "organization_name": org_name,
            "intake_date": (
                intake_record.get("Date", "N/A")[:10] if intake_record.get("Date") else "N/A"
            ),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    def _build_org_summary(
        self, ceo_record: Optional[Dict], tech_records: List[Dict], staff_records: List[Dict]
    ) -> Dict[str, Any]:
        """Build organization summary metrics."""
        total_surveys = 3  # CEO, Tech, Staff
        completed = 0

        if ceo_record and ceo_record.get("Date"):
            completed += 1
        if any(r.get("Date") for r in tech_records):
            completed += 1
        if any(r.get("Date") for r in staff_records):
            completed += 1

        completion_pct = round((completed / total_surveys) * 100) if total_surveys > 0 else 0

        return {
            "total_surveys": total_surveys,
            "completed_surveys": completed,
            "pending_surveys": total_surveys - completed,
            "completion_percentage": completion_pct,
            "ceo_complete": bool(ceo_record and ceo_record.get("Date")),
            "tech_complete": any(r.get("Date") for r in tech_records),
            "staff_complete": any(r.get("Date") for r in staff_records),
            "total_responses": (
                len([k for k in (ceo_record or {}).keys() if k.startswith("C-")])
                + sum(len([k for k in r.keys() if k.startswith("TL-")]) for r in tech_records)
                + sum(len([k for k in r.keys() if k.startswith("S-")]) for r in staff_records)
            ),
        }

    def _build_org_timeline(
        self,
        intake_record: Dict,
        ceo_record: Optional[Dict],
        tech_records: List[Dict],
        staff_records: List[Dict],
    ) -> List[Dict[str, Any]]:
        """Build organization activity timeline."""
        timeline = []

        # Intake event
        if intake_record.get("Date"):
            timeline.append(
                {
                    "date": intake_record.get("Date", "")[:10],
                    "event_type": "Intake",
                    "description": "Organization intake completed",
                    "icon": "clipboard-check",
                    "color": "gray",
                }
            )

        # CEO survey event
        if ceo_record and ceo_record.get("Date"):
            timeline.append(
                {
                    "date": ceo_record.get("Date", "")[:10],
                    "event_type": "CEO Survey",
                    "description": f"{ceo_record.get('Name', 'CEO')} completed survey",
                    "icon": "user-tie",
                    "color": "blue",
                }
            )

        # Tech Lead survey events
        for tech in tech_records:
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
        for staff in staff_records:
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

        # Sort by date
        timeline.sort(key=lambda x: x["date"], reverse=True)

        return timeline

    def _build_org_contacts(
        self, ceo_record: Optional[Dict], tech_records: List[Dict], staff_records: List[Dict]
    ) -> List[Dict[str, Any]]:
        """Build organization contacts list."""
        contacts = []

        # CEO contact
        if ceo_record:
            contacts.append(
                {
                    "name": ceo_record.get("Name", ""),
                    "email": ceo_record.get("CEO Email", ""),
                    "role": ceo_record.get("CEO Role", "CEO"),
                    "type": "CEO",
                    "survey_complete": bool(ceo_record.get("Date")),
                    "submission_date": (
                        ceo_record.get("Date", "")[:10] if ceo_record.get("Date") else None
                    ),
                }
            )

        # Tech Lead contacts
        for tech in tech_records:
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
        for staff in staff_records:
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

    def _build_org_intake_insights(self, intake_record: Dict) -> Dict[str, Any]:
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

    def _build_org_responses(
        self, ceo_record: Optional[Dict], tech_records: List[Dict], staff_records: List[Dict]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Build organization survey responses by category."""
        responses_by_category = defaultdict(list)

        # Process CEO responses
        if ceo_record:
            for key, value in ceo_record.items():
                if key.startswith("C-") and value:
                    question_info = self.questions_lookup.get(key, {})
                    category = question_info.get("category", "General")

                    response = {
                        "question_id": key,
                        "question_text": question_info.get("question", key),
                        "answer_value": value,
                        "answer_text": self._get_answer_text(value, question_info),
                        "respondent": ceo_record.get("Name", "CEO"),
                        "role": "CEO",
                    }
                    responses_by_category[category].append(response)

        # Process Tech responses
        for tech in tech_records:
            for key, value in tech.items():
                if key.startswith("TL-") and value:
                    question_info = self.questions_lookup.get(key, {})
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
        for staff in staff_records:
            for key, value in staff.items():
                if key.startswith("S-") and value:
                    question_info = self.questions_lookup.get(key, {})
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

    def _build_org_export_data(self, org_name: str) -> Dict[str, Any]:
        """Build export metadata for organization."""
        return {
            "organization_name": org_name,
            "export_timestamp": datetime.now().isoformat(),
            "formats_available": ["PDF", "CSV", "JSON"],
        }

    # Aggregate Report Section Builders

    def _build_aggregate_header(self) -> Dict[str, Any]:
        """Build aggregate report header."""
        return {
            "title": "JJF Survey Analytics - Aggregate Report",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "report_type": "Aggregate",
        }

    def _build_aggregate_overview(
        self,
        intake_data: List[Dict],
        ceo_data: List[Dict],
        tech_data: List[Dict],
        staff_data: List[Dict],
    ) -> Dict[str, Any]:
        """Build aggregate overview metrics."""
        total_orgs = len(intake_data)

        # Count unique organizations per survey type (FIXED: count orgs, not responses)
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
        ceo_complete = len(orgs_with_ceo)  # 3 orgs
        tech_complete = len(orgs_with_tech)  # 2 orgs
        staff_complete = len(orgs_with_staff)  # 2 orgs (not 4 responses!)
        surveys_completed = ceo_complete + tech_complete + staff_complete  # 7 total

        # Expected surveys based on responding organizations
        expected_surveys = responding_orgs_count * 3  # 3 orgs × 3 = 9

        # Count fully complete organizations
        fully_complete = len(orgs_with_ceo & orgs_with_tech & orgs_with_staff)

        return {
            "total_organizations": total_orgs,  # 28 (intake)
            "responding_organizations": responding_orgs_count,  # 3 (NEW)
            "total_surveys_expected": expected_surveys,  # 9 (not 84)
            "surveys_completed": surveys_completed,  # 7 (not 9)
            "surveys_pending": expected_surveys - surveys_completed,  # 2
            "completion_percentage": (
                round((surveys_completed / expected_surveys) * 100) if expected_surveys > 0 else 0
            ),  # 78% (not 11%)
            "fully_complete_orgs": fully_complete,  # 1 (Hadar)
            "ceo_complete": ceo_complete,  # 3 orgs
            "tech_complete": tech_complete,  # 2 orgs
            "staff_complete": staff_complete,  # 2 orgs
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

    def _build_aggregate_breakdown(
        self, ceo_data: List[Dict], tech_data: List[Dict], staff_data: List[Dict]
    ) -> Dict[str, Any]:
        """Build aggregate breakdown by survey type."""
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

    def _build_aggregate_timeline(
        self,
        intake_data: List[Dict],
        ceo_data: List[Dict],
        tech_data: List[Dict],
        staff_data: List[Dict],
    ) -> List[Dict[str, Any]]:
        """Build aggregate activity timeline."""
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

    def _build_aggregate_table(
        self,
        intake_data: List[Dict],
        ceo_data: List[Dict],
        tech_data: List[Dict],
        staff_data: List[Dict],
    ) -> List[Dict[str, Any]]:
        """Build aggregate organization status table."""
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

    def _build_aggregate_insights(
        self, ceo_data: List[Dict], tech_data: List[Dict], staff_data: List[Dict]
    ) -> Dict[str, Any]:
        """Build aggregate insights and statistics."""
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

    def _build_aggregate_recommendations(
        self,
        intake_data: List[Dict],
        ceo_data: List[Dict],
        tech_data: List[Dict],
        staff_data: List[Dict],
    ) -> List[str]:
        """Build aggregate recommendations."""
        recommendations = []

        total_orgs = len(intake_data)
        ceo_complete = len([r for r in ceo_data if r.get("Date")])
        tech_complete = len([r for r in tech_data if r.get("Date")])
        staff_complete = len([r for r in staff_data if r.get("Date")])

        # CEO completion rate
        if ceo_complete < total_orgs * 0.5:
            recommendations.append(
                f"Focus on CEO survey completion: Only {ceo_complete}/{total_orgs} ({round((ceo_complete/total_orgs)*100)}%) completed"
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
                f"Overall survey completion is {round((total_complete/total_expected)*100)}% - target 75%+ for robust analysis"
            )

        if not recommendations:
            recommendations.append(
                "Strong survey completion rates across all categories - continue current outreach efforts"
            )

        return recommendations

    # Utility Methods

    def _generate_aggregate_summary(
        self,
        maturity_assessment: Dict[str, Any],
        ai_insights: Optional[Dict[str, Any]],
        org_name: str = None,
    ) -> str:
        """
        Generate an executive summary that consolidates insights from all dimensions.

        Args:
            maturity_assessment: Maturity assessment with dimension scores
            ai_insights: AI insights with dimension summaries (optional)

        Returns:
            A comprehensive 5-7 sentence summary (~600 characters) highlighting:
            - Overall organizational maturity
            - 2-3 key strengths with specific scores
            - 2-3 critical gaps requiring attention
            - Strategic priorities and recommendations
            - Implementation timeline or next steps
        """
        overall_score = maturity_assessment.get("overall_score", 0)
        maturity_level = maturity_assessment.get("maturity_level", "Unknown")
        variance_analysis = maturity_assessment.get("variance_analysis", {})

        if not variance_analysis:
            return "No dimension data available for analysis."

        # Collect dimension scores
        dimension_scores = {
            dim: analysis["weighted_score"]
            for dim, analysis in variance_analysis.items()
            if "weighted_score" in analysis
        }

        if not dimension_scores:
            return "No dimension scores available for analysis."

        # Identify strengths (top 2 highest scoring dimensions)
        sorted_dimensions = sorted(dimension_scores.items(), key=lambda x: x[1], reverse=True)
        strengths = sorted_dimensions[:2]
        gaps = sorted_dimensions[-2:]

        # Build context for AI
        dimension_summaries = []
        for dim, score in sorted_dimensions:
            level = self._get_maturity_level_name(score)
            summary_line = f"{dim}: {level} ({score:.1f}/5.0)"

            # Add AI summary if available
            if ai_insights and "dimensions" in ai_insights:
                dim_insights = ai_insights["dimensions"].get(dim, {})
                if "summary" in dim_insights and dim_insights["summary"]:
                    summary_line += f" - {dim_insights['summary']}"

            dimension_summaries.append(summary_line)

        # Create prompt for aggregate summary with expanded requirements
        org_reference = org_name if org_name else "the organization"
        prompt = """Based on these technology maturity assessments for {org_reference}, create a comprehensive 5-7 sentence executive summary (~600 characters):

Overall Score: {overall_score:.1f}/5.0 ({maturity_level})

Dimension Assessments:
{chr(10).join(dimension_summaries)}

Requirements:
- Paragraph 1 (2 sentences): Overall assessment and maturity characterization
- Paragraph 2 (2-3 sentences): Key strengths with specific dimension scores and what's working well (mention: {strengths[0][0]} at {strengths[0][1]:.1f} and {strengths[1][0]} at {strengths[1][1]:.1f})
- Paragraph 3 (2 sentences): Critical gaps with specific dimension scores and business impact (mention: {gaps[0][0]} at {gaps[0][1]:.1f} and {gaps[1][0]} at {gaps[1][1]:.1f})
- Final sentence: Top strategic priority with actionable next step

Length: 500-600 characters (5-7 sentences)
Tone: Professional, executive-level, actionable
Format: Three paragraphs separated by line breaks

Executive Summary:"""

        # Use existing AI infrastructure to generate
        if self.ai_analyzer:
            try:
                # Generate summary with AI - increased max_tokens for longer output
                response = self.ai_analyzer.client.chat.completions.create(
                    model=self.ai_analyzer.model,
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are an expert technology consultant creating comprehensive executive summaries for nonprofit organizations. When referring to the organization, use '{org_reference}' instead of generic terms like 'the nonprofit' or 'nonprofit's'. Provide detailed, actionable insights in 5-7 sentences organized into three paragraphs.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.4,
                    max_tokens=400,  # Increased from 150 to accommodate longer summary
                )

                summary = response.choices[0].message.content.strip()

                # Remove quotes if LLM added them
                if summary.startswith('"') and summary.endswith('"'):
                    summary = summary[1:-1]
                if summary.startswith("'") and summary.endswith("'"):
                    summary = summary[1:-1]

                # Consolidate to target length if needed (increased from 200 to 600)
                if len(summary) > 650:
                    summary = self.ai_analyzer.consolidate_text(summary, max_chars=600)

                return summary
            except Exception as e:
                print(f"Error generating aggregate summary with AI: {e}")
                # Fall through to fallback

        # Fallback: construct basic summary without AI (expanded version)
        summary_parts = []

        # Overall assessment
        summary_parts.append(
            f"The organization demonstrates {maturity_level.lower()} technology maturity "
            f"with an overall score of {overall_score:.1f}/5.0"
        )

        # Strengths
        if strengths:
            summary_parts.append(
                f"Strong performance in {strengths[0][0]} ({strengths[0][1]:.1f}) "
                f"and {strengths[1][0]} ({strengths[1][1]:.1f}) provides a solid operational foundation, "
                "demonstrating effective practices in these critical areas"
            )

        # Gaps
        if gaps:
            summary_parts.append(
                f"However, critical gaps in {gaps[0][0]} ({gaps[0][1]:.1f}) "
                f"and {gaps[1][0]} ({gaps[1][1]:.1f}) present significant risks and require immediate attention "
                "to prevent operational challenges and ensure sustainable growth"
            )

        # Strategic recommendation with implementation guidance
        if overall_score < 2.5:
            summary_parts.append(
                "Top Priority: Establish foundational technology systems and build core technical capacity "
                "through systematic investment in infrastructure, training, and standardized processes"
            )
        elif overall_score < 3.5:
            summary_parts.append(
                "Top Priority: Focus on system integration and process optimization while addressing "
                "identified gaps through targeted improvements and cross-functional collaboration"
            )
        else:
            summary_parts.append(
                "Top Priority: Pursue strategic innovation and advanced capabilities by leveraging "
                "existing strengths while continuously monitoring and improving lower-performing areas"
            )

        return ". ".join(summary_parts) + "."

    def _extract_tech_insights_aggregated(
        self, ceo_record: Optional[Dict], tech_records: List[Dict], staff_records: List[Dict]
    ) -> Dict[str, Any]:
        """
        Extract tech insights from all stakeholders with aggregated frequency counts.

        Aggregates technology challenges and investment priorities from CEO, Tech Lead,
        and Staff surveys to show which issues are most commonly reported across the organization.

        Args:
            ceo_record: CEO survey response
            tech_records: List of Tech Lead survey responses
            staff_records: List of Staff survey responses

        Returns:
            Dictionary with:
                - policies: Tech policies from Tech Lead (TL-I-6)
                - challenges: Dict with aggregated_counts and total_respondents
                - priorities: Dict with aggregated_counts and total_respondents
        """
        # Tech Lead data
        tech_policies = None
        tech_challenges = None
        tech_priorities = None

        if tech_records:
            tech_policies_raw = tech_records[0].get("TL-I-6")
            if tech_policies_raw and str(tech_policies_raw).strip() != "0":
                tech_policies = tech_policies_raw

            tech_challenges = tech_records[0].get("TL-CTC")
            tech_priorities = tech_records[0].get("TL-TIP")  # Fixed: was "TLC-TIP"

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

    def _calculate_nps_metrics(self, staff_responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate Net Promoter Score metrics from staff S-I-6 responses.

        Returns:
            Dict with average score, NPS, count, and distribution
        """
        scores = []
        for response in staff_responses:
            score_value = response.get("S-I-6")
            if score_value and str(score_value).strip().isdigit():
                score = int(score_value)
                if 0 <= score <= 10:
                    scores.append(score)

        if not scores:
            return {
                "score": None,
                "nps": None,
                "count": 0,
                "distribution": {"detractors": 0, "passives": 0, "promoters": 0},
                "classification": None,
            }

        # Calculate distribution
        detractors = len([s for s in scores if s <= 6])
        passives = len([s for s in scores if 7 <= s <= 8])
        promoters = len([s for s in scores if s >= 9])
        total = len(scores)

        # Net Promoter Score formula: (% Promoters) - (% Detractors)
        nps = ((promoters / total) - (detractors / total)) * 100

        # Average score
        avg_score = sum(scores) / total

        # Classification based on average
        if avg_score >= 9:
            classification = "Promoter"
        elif avg_score >= 7:
            classification = "Passive"
        else:
            classification = "Detractor"

        return {
            "score": round(avg_score, 1),
            "nps": round(nps, 1),
            "count": total,
            "distribution": {
                "detractors": detractors,
                "passives": passives,
                "promoters": promoters,
            },
            "classification": classification,
            "scores": scores,  # Individual scores for debugging
        }

    def _get_maturity_level_name(self, score: float) -> str:
        """Get maturity level name for a given score."""
        if score < 2.0:
            return "Building (Early)"
        elif score < 2.5:
            return "Building (Late)"
        elif score < 3.5:
            return "Emerging"
        elif score < 4.5:
            return "Thriving (Early)"
        else:
            return "Thriving (Advanced)"

    def _get_answer_text(self, value: Any, question_info: Dict) -> str:
        """Get answer text from answer key lookup."""
        if not question_info or "answer_keys" not in question_info:
            return str(value)

        value_str = str(value).strip()
        if value_str.isdigit():
            answer_num = int(value_str)
            if 1 <= answer_num <= 7:
                answer_text = question_info["answer_keys"].get(answer_num, "")
                if answer_text:
                    return answer_text

        return str(value)

    def generate_feedback_summary(self) -> Optional[str]:
        """
        Generate AI-powered summary of all free text feedback for the home page.

        Returns:
            Summary string or None if AI not available
        """
        if not self.enable_ai or not self.ai_analyzer:
            return None

        try:
            # Collect all free text responses across all organizations
            all_responses = []

            # Get all organization names from Intake
            intake_data = self.sheet_data.get("Intake", [])
            org_names = [
                row.get("Organization Name:")
                for row in intake_data
                if row.get("Organization Name:")
            ]

            for org_name in org_names:
                free_text = extract_free_text_responses(self.sheet_data, org_name)

                for dimension, responses in free_text.items():
                    for response in responses:
                        all_responses.append(
                            {"organization": org_name, "dimension": dimension, **response}
                        )

            if not all_responses:
                return "No qualitative feedback available for analysis."

            # Generate AI summary
            summary = self.ai_analyzer.summarize_all_feedback(all_responses)
            return summary

        except Exception as e:
            print(f"Error generating feedback summary: {e}")
            return None
