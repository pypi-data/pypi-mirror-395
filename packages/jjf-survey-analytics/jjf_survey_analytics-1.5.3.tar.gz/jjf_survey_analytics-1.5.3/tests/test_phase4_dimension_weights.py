"""
Phase 4 MVC Refactoring Tests: Dimension Weights Consolidation
Tests that dimension weights are pre-calculated in backend from single source of truth
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest

from src.analytics.maturity_rubric import MaturityRubric


class TestPhase4DimensionWeights:
    """
    Phase 4: Test dimension weights consolidation

    Verify that:
    1. MaturityRubric.DIMENSION_WEIGHTS is the single source of truth
    2. Dimension weights are pre-calculated in variance_analysis
    3. Template receives pre-calculated dimension_weight values
    """

    def test_01_maturity_rubric_has_dimension_weights(self):
        """Test that MaturityRubric defines DIMENSION_WEIGHTS as class constant"""
        assert hasattr(
            MaturityRubric, "DIMENSION_WEIGHTS"
        ), "MaturityRubric must define DIMENSION_WEIGHTS constant"

        weights = MaturityRubric.DIMENSION_WEIGHTS
        assert isinstance(weights, dict), "DIMENSION_WEIGHTS must be a dictionary"
        assert len(weights) == 5, "Must have weights for all 5 dimensions"

        # Verify all dimensions present
        expected_dimensions = {
            "Program Technology",
            "Business Systems",
            "Data Management",
            "Infrastructure",
            "Organizational Culture",
        }
        assert (
            set(weights.keys()) == expected_dimensions
        ), "DIMENSION_WEIGHTS must contain all 5 dimensions"

        # Verify equal weighting (20% each)
        for dimension, weight in weights.items():
            assert weight == 0.20, f"{dimension} weight should be 0.20, got {weight}"

        # Verify sum is 1.0
        total_weight = sum(weights.values())
        assert (
            abs(total_weight - 1.0) < 0.001
        ), f"Dimension weights must sum to 1.0, got {total_weight}"

        print("✓ MaturityRubric.DIMENSION_WEIGHTS verified as single source of truth")

    def test_02_dimension_weights_in_variance_analysis(self, sample_report):
        """Test that variance_analysis includes pre-calculated dimension_weight"""
        variance_analysis = sample_report["maturity"]["variance_analysis"]

        for dimension, analysis in variance_analysis.items():
            assert (
                "dimension_weight" in analysis
            ), f"{dimension} must have pre-calculated dimension_weight"

            weight = analysis["dimension_weight"]
            assert isinstance(weight, float), f"{dimension} dimension_weight must be float"
            assert weight == 0.20, f"{dimension} dimension_weight should be 0.20, got {weight}"

        print(f"✓ All {len(variance_analysis)} dimensions have pre-calculated dimension_weight")

    def test_03_single_source_of_truth(self, sample_report):
        """Test that variance_analysis weights match MaturityRubric.DIMENSION_WEIGHTS"""
        rubric_weights = MaturityRubric.DIMENSION_WEIGHTS
        variance_analysis = sample_report["maturity"]["variance_analysis"]

        for dimension, analysis in variance_analysis.items():
            backend_weight = analysis["dimension_weight"]
            rubric_weight = rubric_weights[dimension]

            assert backend_weight == rubric_weight, (
                f"{dimension}: Backend weight ({backend_weight}) must match "
                f"MaturityRubric.DIMENSION_WEIGHTS ({rubric_weight})"
            )

        print(
            "✓ Backend dimension_weight matches MaturityRubric.DIMENSION_WEIGHTS (single source of truth)"
        )

    def test_04_no_template_calculations_needed(self, sample_report):
        """Test that template can use dimension_weight directly without calculation"""
        variance_analysis = sample_report["maturity"]["variance_analysis"]

        # Verify all required fields for template rendering exist
        for dimension, analysis in variance_analysis.items():
            # Template needs these pre-calculated values:
            assert "dimension_weight" in analysis, f"{dimension} missing dimension_weight"
            assert "adjusted_score" in analysis, f"{dimension} missing adjusted_score"
            assert "weighted_score" in analysis, f"{dimension} missing weighted_score"

            # Verify template can use dimension_weight directly
            weight = analysis["dimension_weight"]
            score = analysis.get("adjusted_score", analysis["weighted_score"])

            # Template should be able to calculate: score × weight
            weighted_contribution = score * weight
            assert isinstance(
                weighted_contribution, float
            ), "Template should be able to multiply score by pre-calculated weight"

        print("✓ Template can use pre-calculated dimension_weight without hardcoded dict")


# Fixtures


@pytest.fixture
def sample_report():
    """
    Generate a sample report with variance_analysis including dimension_weight.
    This simulates the output from ReportGenerator after Phase 4 implementation.
    """
    from src.services.report_generator import ReportGenerator

    # Initialize generator with empty sheet_data (not needed for this test)
    generator = ReportGenerator(sheet_data={})

    # Create mock maturity assessment
    maturity = {
        "variance_analysis": {
            "Program Technology": {
                "weighted_score": 3.16,
                "adjusted_score": 3.16,
                "total_modifier": 0.0,
            },
            "Business Systems": {
                "weighted_score": 3.17,
                "adjusted_score": 3.17,
                "total_modifier": 0.0,
            },
            "Data Management": {
                "weighted_score": 3.75,
                "adjusted_score": 3.75,
                "total_modifier": 0.0,
            },
            "Infrastructure": {
                "weighted_score": 1.75,
                "adjusted_score": 1.75,
                "total_modifier": 0.0,
            },
            "Organizational Culture": {
                "weighted_score": 2.22,
                "adjusted_score": 2.22,
                "total_modifier": 0.0,
            },
        }
    }

    # Create minimal report
    report = {"maturity": maturity}

    # Apply Phase 4: Add dimension weights to variance_analysis
    generator._add_checksums_to_dimensions(report)

    return report


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
