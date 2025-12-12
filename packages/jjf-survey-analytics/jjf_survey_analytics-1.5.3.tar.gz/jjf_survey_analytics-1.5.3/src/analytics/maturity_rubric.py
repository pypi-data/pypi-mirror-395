"""
Technology Maturity Assessment Rubric
Implements Jim Joseph Foundation's technology readiness scoring framework
"""

import logging
from statistics import mean, stdev
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)


class MaturityRubric:
    """Technology maturity assessment rubric implementation."""

    # Dimension weights for overall score (equal weighting)
    DIMENSION_WEIGHTS = {
        "Program Technology": 0.20,
        "Business Systems": 0.20,
        "Data Management": 0.20,
        "Infrastructure": 0.20,
        "Organizational Culture": 0.20,
    }

    # Stakeholder weights by dimension
    STAKEHOLDER_WEIGHTS = {
        "Program Technology": {"CEO": 0.25, "Tech Lead": 0.20, "Staff": 0.55},
        "Business Systems": {"CEO": 0.35, "Tech Lead": 0.30, "Staff": 0.35},
        "Data Management": {"CEO": 0.30, "Tech Lead": 0.40, "Staff": 0.30},
        "Infrastructure": {"CEO": 0.20, "Tech Lead": 0.50, "Staff": 0.30},
        "Organizational Culture": {"CEO": 0.40, "Tech Lead": 0.20, "Staff": 0.40},
    }

    # Maturity levels
    MATURITY_LEVELS = [
        (1.0, 1.9, "Building (Early)", 0, 20, "Significant gaps, primarily manual processes"),
        (2.0, 2.4, "Building (Late)", 21, 35, "Limited capabilities, basic digital adoption"),
        (2.5, 3.4, "Emerging", 36, 70, "Functional systems with integration gaps"),
        (3.5, 4.4, "Thriving (Early)", 71, 88, "Strategic integration, good capabilities"),
        (4.5, 5.0, "Thriving (Advanced)", 89, 100, "Innovation leader, full integration"),
    ]

    # Variance thresholds
    VARIANCE_THRESHOLDS = {
        "low": (0, 0.8, "Green", "Strong alignment"),
        "medium": (0.8, 1.6, "Yellow", "Some disagreement on effectiveness"),
        "high": (1.6, float("inf"), "Red", "Significant perception gaps requiring intervention"),
    }

    @classmethod
    def calculate_overall_score_from_dimensions(
        cls, variance_analysis: Dict[str, Dict[str, Any]]
    ) -> float:
        """
        Calculate overall maturity score from dimension analysis.

        SINGLE SOURCE OF TRUTH for overall score calculation across the platform.
        All backend implementations must use this method to ensure consistency.

        Formula:
            overall_score = Σ(dimension_score × weight) / Σ(weight)

        The method uses adjusted_score (with AI/admin modifiers) if available,
        otherwise falls back to weighted_score (base dimension score).

        Args:
            variance_analysis: Dictionary mapping dimension names to analysis dictionaries.
                             Each analysis dict must contain either:
                             - 'adjusted_score': Dimension score with AI/admin modifiers applied
                             - 'weighted_score': Base dimension score without modifiers

        Returns:
            float: Overall maturity score on a 1.0 to 5.0 scale.
                  Returns 1.0 (minimum score) if no valid dimensions found.

        Example:
            >>> variance_analysis = {
            ...     "Program Technology": {"adjusted_score": 4.00},
            ...     "Business Systems": {"adjusted_score": 4.10},
            ...     "Data Management": {"adjusted_score": 2.50},
            ...     "Infrastructure": {"adjusted_score": 2.33},
            ...     "Organizational Culture": {"adjusted_score": 2.92}
            ... }
            >>> MaturityRubric.calculate_overall_score_from_dimensions(variance_analysis)
            3.17

        Notes:
            - Used in 6+ locations: initial calculation, AI modifiers, admin edits,
              cached report reload, validation, and report generation
            - Ensures consistent scoring across all report variations
            - Defaults to 1.0 (lowest maturity) if no valid dimensions present
        """
        total_weighted_score = 0.0
        total_weight = 0.0

        # Debug logging to diagnose scoring issues
        logger.info(f"[MaturityRubric] calculate_overall_score_from_dimensions called")
        logger.info(f"[MaturityRubric] variance_analysis keys: {list(variance_analysis.keys())}")
        logger.info(f"[MaturityRubric] DIMENSION_WEIGHTS keys: {list(cls.DIMENSION_WEIGHTS.keys())}")

        for dimension, analysis in variance_analysis.items():
            weight = cls.DIMENSION_WEIGHTS.get(dimension, 0)
            logger.info(f"[MaturityRubric] Dimension '{dimension}': weight={weight}")
            if weight > 0:
                # Use adjusted score (with modifiers) if available,
                # otherwise use weighted score (base calculation)
                score = analysis.get("adjusted_score", analysis.get("weighted_score", 0))
                logger.info(f"[MaturityRubric]   - adjusted_score: {analysis.get('adjusted_score')}")
                logger.info(f"[MaturityRubric]   - weighted_score: {analysis.get('weighted_score')}")
                logger.info(f"[MaturityRubric]   - final score used: {score}")
                total_weighted_score += score * weight
                total_weight += weight

        # Calculate weighted average, default to 1.0 if no valid dimensions
        logger.info(f"[MaturityRubric] total_weighted_score: {total_weighted_score}")
        logger.info(f"[MaturityRubric] total_weight: {total_weight}")
        if total_weight > 0:
            overall_score = total_weighted_score / total_weight
        else:
            logger.warning(f"[MaturityRubric] NO VALID DIMENSIONS FOUND - defaulting to 1.0")
            overall_score = 1.0  # Default to lowest score if no valid data

        logger.info(f"[MaturityRubric] calculated overall_score: {overall_score:.2f}")
        return overall_score

    def __init__(self):
        """Initialize rubric."""
        self.dimension_mapping = self._build_dimension_mapping()

    def _build_dimension_mapping(self) -> Dict[str, str]:
        """
        Map question IDs to dimensions.
        Question IDs follow pattern: {Role}-{DimensionCode}-{Number}
        e.g., C-PT-1 = CEO, Program Technology, Question 1
        """
        # Dimension code to full name mapping
        dimension_codes = {
            "PT": "Program Technology",
            "BS": "Business Systems",
            "D": "Data Management",
            "I": "Infrastructure",
            "OC": "Organizational Culture",
        }

        # This will be populated dynamically from questions
        # For now, we'll parse based on the pattern
        mapping = {}

        # Common question IDs (will be populated from actual survey data)
        # Pattern: {C|TL|S}-{PT|BS|D|I|OC}-{number}
        for role in ["C", "TL", "S"]:
            for code, dimension in dimension_codes.items():
                for num in range(1, 30):  # Support up to 30 questions per dimension
                    q_id = f"{role}-{code}-{num}"
                    mapping[q_id] = dimension

        return mapping

    def calculate_dimension_score(
        self, responses: Dict[str, float], role: str, dimension: str
    ) -> float:
        """
        Calculate average score for a dimension from role responses.

        Args:
            responses: Dict of question_id -> score
            role: 'CEO', 'Tech Lead', or 'Staff'
            dimension: One of the 5 dimensions

        Returns:
            Average score for the dimension (1-5 scale), or None if no valid responses
        """
        dimension_scores = []

        for question_id, score in responses.items():
            if self.dimension_mapping.get(question_id) == dimension:
                try:
                    numeric_score = float(score)
                    # Only include scores 1-5 (6 is N/A, 0 is missing/invalid)
                    if 1 <= numeric_score <= 5:
                        dimension_scores.append(numeric_score)
                except (ValueError, TypeError):
                    continue

        return mean(dimension_scores) if dimension_scores else None

    def calculate_weighted_dimension_score(
        self, ceo_score: float, tech_score: float, staff_score: float, dimension: str
    ) -> float:
        """
        Calculate weighted dimension score across stakeholders.
        When stakeholders are missing, weights are adjusted proportionally.

        Args:
            ceo_score: CEO dimension score (or None if missing)
            tech_score: Tech Lead dimension score (or None if missing)
            staff_score: Staff dimension score (or None if missing)
            dimension: Dimension name

        Returns:
            Weighted dimension score, or None if all stakeholders missing
        """
        weights = self.STAKEHOLDER_WEIGHTS.get(
            dimension, {"CEO": 0.33, "Tech Lead": 0.33, "Staff": 0.34}
        )

        # Build list of available scores with their weights
        available = []
        if ceo_score is not None:
            available.append((ceo_score, weights.get("CEO", 0)))
        if tech_score is not None:
            available.append((tech_score, weights.get("Tech Lead", 0)))
        if staff_score is not None:
            available.append((staff_score, weights.get("Staff", 0)))

        if not available:
            return None

        # Calculate total weight of available stakeholders
        total_weight = sum(weight for _, weight in available)

        # Normalize weights and calculate weighted average
        if total_weight > 0:
            weighted = sum(score * (weight / total_weight) for score, weight in available)
            return weighted

        return None

    def calculate_variance(self, scores: List[float]) -> Tuple[float, str, str, str]:
        """
        Calculate variance and interpretation.

        Args:
            scores: List of scores from different stakeholders

        Returns:
            Tuple of (std_dev, level, color, description)
        """
        if len(scores) < 2:
            return 0.0, "low", "Green", "Insufficient data"

        try:
            std_dev = stdev(scores)
        except Exception:
            return 0.0, "low", "Green", "Calculation error"

        for level, (min_val, max_val, color, desc) in self.VARIANCE_THRESHOLDS.items():
            if min_val <= std_dev < max_val:
                return std_dev, level, color, desc

        return std_dev, "high", "Red", "Significant gaps"

    def get_maturity_level(self, score: float) -> Tuple[str, int, int, str]:
        """
        Get maturity level classification.

        Args:
            score: Overall or dimension score (1-5 scale)

        Returns:
            Tuple of (level_name, min_pct, max_pct, description)
        """
        for min_score, max_score, level, min_pct, max_pct, desc in self.MATURITY_LEVELS:
            if min_score <= score <= max_score:
                return level, min_pct, max_pct, desc

        # Default to Building if out of range
        return "Building (Early)", 0, 20, "Significant gaps, primarily manual processes"

    def generate_recommendations(
        self,
        overall_score: float,
        dimension_scores: Dict[str, float],
        variance_analysis: Dict[str, Dict],
    ) -> List[str]:
        """
        Generate actionable recommendations based on scores.

        Args:
            overall_score: Overall maturity score
            dimension_scores: Scores by dimension
            variance_analysis: Variance data by dimension

        Returns:
            List of recommendation strings
        """
        recommendations = []
        maturity_level, _, _, _ = self.get_maturity_level(overall_score)

        # Recommendations by overall maturity level
        if "Building" in maturity_level:
            recommendations.append("Priority: Conduct comprehensive technology needs assessment")
            recommendations.append(
                "Action: Establish basic infrastructure foundation (reliable internet, cloud email)"
            )
            recommendations.append("Support: Engage in fundamental training program for staf")
            recommendations.append("Timeline: 12-18 month intensive capacity building recommended")

        elif maturity_level == "Emerging":
            recommendations.append("Priority: Develop system integration plan to reduce data silos")
            recommendations.append("Action: Implement data governance policies and procedures")
            recommendations.append(
                "Support: Advance staff training to intermediate technology skills"
            )
            recommendations.append("Timeline: 6-12 month targeted support program recommended")

        else:  # Thriving
            recommendations.append(
                "Opportunity: Participate in innovation lab and pilot advanced technologies"
            )
            recommendations.append(
                "Leadership: Consider peer mentorship role for other organizations"
            )
            recommendations.append("Growth: Explore AI/ML applications for mission enhancement")
            recommendations.append(
                "Recognition: Strong candidate for sector leadership opportunities"
            )

        # Dimension-specific recommendations (focus on lowest scoring)
        valid_dimension_scores = [(d, s) for d, s in dimension_scores.items() if s is not None]

        if valid_dimension_scores:
            lowest_dimension = min(valid_dimension_scores, key=lambda x: x[1])
            dimension_name, dimension_score = lowest_dimension

            if dimension_score < 2.5:
                if dimension_name == "Program Technology":
                    recommendations.append(
                        f"Critical Gap ({dimension_name}): Invest in program delivery technology to support mission"
                    )
                elif dimension_name == "Business Systems":
                    recommendations.append(
                        f"Critical Gap ({dimension_name}): Integrate core business systems (CRM, finance, HR)"
                    )
                elif dimension_name == "Data Management":
                    recommendations.append(
                        f"Critical Gap ({dimension_name}): Establish data collection and analysis capabilities"
                    )
                elif dimension_name == "Infrastructure":
                    recommendations.append(
                        f"Critical Gap ({dimension_name}): Upgrade network and cybersecurity infrastructure"
                    )
                elif dimension_name == "Organizational Culture":
                    recommendations.append(
                        f"Critical Gap ({dimension_name}): Build technology-positive culture through leadership engagement"
                    )

        # High variance recommendations
        high_variance_dims = [
            dim for dim, analysis in variance_analysis.items() if analysis.get("level") == "high"
        ]

        if high_variance_dims:
            dim_list = ", ".join(high_variance_dims)
            recommendations.append(
                f"Alignment Needed: Significant perception gaps in {dim_list} - recommend stakeholder alignment sessions"
            )

        return recommendations[:6]  # Return top 6 recommendations

    def calculate_overall_maturity(self, org_responses: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive maturity assessment.

        Args:
            org_responses: Dictionary with CEO, Tech, Staff responses

        Returns:
            Complete maturity assessment with scores, variance, recommendations
        """
        dimension_scores = {}
        variance_analysis = {}

        dimensions = list(self.DIMENSION_WEIGHTS.keys())

        for dimension in dimensions:
            # Calculate scores by role
            ceo_score = self.calculate_dimension_score(
                org_responses.get("CEO", {}), "CEO", dimension
            )
            tech_score = self.calculate_dimension_score(
                org_responses.get("Tech", {}), "Tech Lead", dimension
            )
            staff_score = self.calculate_dimension_score(
                org_responses.get("Staff", {}), "Staff", dimension
            )

            # Calculate weighted dimension score
            weighted_score = self.calculate_weighted_dimension_score(
                ceo_score, tech_score, staff_score, dimension
            )
            dimension_scores[dimension] = weighted_score

            # Calculate variance (only for stakeholders with valid scores)
            scores_list = [s for s in [ceo_score, tech_score, staff_score] if s is not None]
            std_dev, level, color, desc = self.calculate_variance(scores_list)

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

        # Calculate overall score using centralized method (single source of truth)
        overall_score = self.calculate_overall_score_from_dimensions(variance_analysis)

        # Get maturity level
        maturity_level, min_pct, max_pct, maturity_desc = self.get_maturity_level(overall_score)

        # Generate recommendations
        recommendations = self.generate_recommendations(
            overall_score, dimension_scores, variance_analysis
        )

        return {
            "overall_score": round(overall_score, 2),
            "maturity_level": maturity_level,
            "maturity_percentage": int((overall_score - 1) / 4 * 100),
            "maturity_description": maturity_desc,
            "dimension_scores": dimension_scores,
            "variance_analysis": variance_analysis,
            "recommendations": recommendations,
        }
