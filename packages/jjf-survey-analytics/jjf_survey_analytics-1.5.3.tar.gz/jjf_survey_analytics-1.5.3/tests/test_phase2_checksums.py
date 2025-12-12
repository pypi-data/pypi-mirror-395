"""
Tests for Phase 2: Calculation Checksums and Verification

This test suite validates that:
1. Checksums are generated for all dimension calculations
2. Correct calculations pass validation
3. Incorrect calculations fail validation
4. Clamping logic (0-5 range) is properly validated
5. Report-level verification works correctly
"""

import unittest

from src.services.report_generator import ReportGenerator


class TestPhase2Checksums(unittest.TestCase):
    """Test checksum generation and validation"""

    def setUp(self):
        """Set up test data"""
        # Minimal sheet data for testing
        self.test_sheet_data = {"Questions": [], "Intake": [], "CEO": [], "Tech": [], "Staff": []}

    def test_checksum_generation_correct_calculation(self):
        """Test that checksums are generated for correct calculations"""
        generator = ReportGenerator(self.test_sheet_data, enable_ai=False)

        # Create test analysis with correct calculation: 3.0 + 0.5 = 3.5
        analysis = {"weighted_score": 3.0, "total_modifier": 0.5, "adjusted_score": 3.5}

        checksum = generator._calculate_dimension_checksum(analysis)

        # Verify checksum structure
        self.assertIn("checksum", checksum)
        self.assertIn("calculation", checksum)
        self.assertIn("formula", checksum)
        self.assertIn("valid", checksum)
        self.assertIn("expected", checksum)
        self.assertIn("actual", checksum)
        self.assertIn("error", checksum)
        self.assertIn("components", checksum)

        # Verify validation passed
        self.assertTrue(checksum["valid"], "Correct calculation should pass validation")
        self.assertEqual(checksum["expected"], 3.5)
        self.assertEqual(checksum["actual"], 3.5)
        self.assertLess(
            checksum["error"], 0.001, "Error should be negligible for correct calculation"
        )

    def test_checksum_validation_incorrect_calculation(self):
        """Test that incorrect calculations fail validation"""
        generator = ReportGenerator(self.test_sheet_data, enable_ai=False)

        # Create test analysis with WRONG calculation: 3.0 + 0.5 = 4.0 (should be 3.5!)
        analysis = {
            "weighted_score": 3.0,
            "total_modifier": 0.5,
            "adjusted_score": 4.0,  # INCORRECT!
        }

        checksum = generator._calculate_dimension_checksum(analysis)

        # Verify validation failed
        self.assertFalse(checksum["valid"], "Incorrect calculation should fail validation")
        self.assertEqual(checksum["expected"], 3.5)
        self.assertEqual(checksum["actual"], 4.0)
        self.assertGreater(
            checksum["error"], 0.4, "Error should be significant for incorrect calculation"
        )

    def test_checksum_clamping_negative_to_zero(self):
        """Test that checksum validates clamping negative results to 0"""
        generator = ReportGenerator(self.test_sheet_data, enable_ai=False)

        # Test negative result clamped to 0: 1.0 + (-2.0) = -1.0 → 0.0
        analysis = {"weighted_score": 1.0, "total_modifier": -2.0, "adjusted_score": 0.0}

        checksum = generator._calculate_dimension_checksum(analysis)

        # Verify validation passed (clamping is correct)
        self.assertTrue(checksum["valid"], "Correct clamping to 0 should pass validation")
        self.assertEqual(checksum["expected"], 0.0)
        self.assertEqual(checksum["actual"], 0.0)

    def test_checksum_clamping_over_five_to_five(self):
        """Test that checksum validates clamping over 5 results to 5"""
        generator = ReportGenerator(self.test_sheet_data, enable_ai=False)

        # Test over 5 result clamped to 5: 4.5 + 1.0 = 5.5 → 5.0
        analysis = {"weighted_score": 4.5, "total_modifier": 1.0, "adjusted_score": 5.0}

        checksum = generator._calculate_dimension_checksum(analysis)

        # Verify validation passed (clamping is correct)
        self.assertTrue(checksum["valid"], "Correct clamping to 5 should pass validation")
        self.assertEqual(checksum["expected"], 5.0)
        self.assertEqual(checksum["actual"], 5.0)

    def test_checksum_clamping_incorrect_negative(self):
        """Test that incorrect clamping fails validation"""
        generator = ReportGenerator(self.test_sheet_data, enable_ai=False)

        # Test incorrect clamping: 1.0 + (-2.0) = -1.0 but incorrectly set to -1.0 instead of 0.0
        analysis = {
            "weighted_score": 1.0,
            "total_modifier": -2.0,
            "adjusted_score": -1.0,  # Should be clamped to 0.0!
        }

        checksum = generator._calculate_dimension_checksum(analysis)

        # Verify validation failed
        self.assertFalse(checksum["valid"], "Incorrect clamping should fail validation")
        self.assertEqual(checksum["expected"], 0.0)
        self.assertEqual(checksum["actual"], -1.0)

    def test_checksum_components_structure(self):
        """Test that checksum components contain all required fields"""
        generator = ReportGenerator(self.test_sheet_data, enable_ai=False)

        analysis = {"weighted_score": 2.75, "total_modifier": 0.25, "adjusted_score": 3.0}

        checksum = generator._calculate_dimension_checksum(analysis)

        # Verify components structure
        self.assertIn("base_score", checksum["components"])
        self.assertIn("total_modifier", checksum["components"])
        self.assertIn("adjusted_score", checksum["components"])

        # Verify components values (rounded to 2 decimals)
        self.assertEqual(checksum["components"]["base_score"], 2.75)
        self.assertEqual(checksum["components"]["total_modifier"], 0.25)
        self.assertEqual(checksum["components"]["adjusted_score"], 3.0)

    def test_checksum_formula_string(self):
        """Test that formula string is correctly formatted"""
        generator = ReportGenerator(self.test_sheet_data, enable_ai=False)

        analysis = {"weighted_score": 3.5, "total_modifier": -0.5, "adjusted_score": 3.0}

        checksum = generator._calculate_dimension_checksum(analysis)

        # Verify formula includes max/min clamping
        self.assertIn("max(0, min(5,", checksum["formula"])
        self.assertIn("3.50", checksum["formula"])
        self.assertIn("-0.50", checksum["formula"])

    def test_verify_report_calculations_no_variance_analysis(self):
        """Test verification handles missing variance analysis"""
        generator = ReportGenerator(self.test_sheet_data, enable_ai=False)

        # Report without maturity or variance_analysis
        report = {}

        results = generator.verify_report_calculations(report)

        # Should fail with error message
        self.assertFalse(results["valid"])
        self.assertIn("Missing maturity variance analysis", results["errors"])
        self.assertEqual(results["dimensions_checked"], 0)

    def test_verify_report_calculations_all_valid(self):
        """Test verification with all valid checksums"""
        generator = ReportGenerator(self.test_sheet_data, enable_ai=False)

        # Create report with valid checksums
        report = {
            "maturity": {
                "variance_analysis": {
                    "Infrastructure": {
                        "weighted_score": 2.5,
                        "total_modifier": 0.5,
                        "adjusted_score": 3.0,
                        "checksum": {
                            "valid": True,
                            "expected": 3.0,
                            "actual": 3.0,
                            "error": 0.0,
                            "formula": "max(0, min(5, 2.50 + 0.50))",
                        },
                    },
                    "Data Management": {
                        "weighted_score": 4.0,
                        "total_modifier": -0.5,
                        "adjusted_score": 3.5,
                        "checksum": {
                            "valid": True,
                            "expected": 3.5,
                            "actual": 3.5,
                            "error": 0.0,
                            "formula": "max(0, min(5, 4.00 + -0.50))",
                        },
                    },
                }
            }
        }

        results = generator.verify_report_calculations(report)

        # Should pass validation
        self.assertTrue(results["valid"])
        self.assertEqual(results["dimensions_checked"], 2)
        self.assertEqual(results["dimensions_valid"], 2)
        self.assertEqual(results["dimensions_invalid"], 0)
        self.assertEqual(len(results["errors"]), 0)

    def test_verify_report_calculations_with_invalid(self):
        """Test verification with some invalid checksums"""
        generator = ReportGenerator(self.test_sheet_data, enable_ai=False)

        # Create report with one invalid checksum
        report = {
            "maturity": {
                "variance_analysis": {
                    "Infrastructure": {
                        "weighted_score": 2.5,
                        "total_modifier": 0.5,
                        "adjusted_score": 3.0,
                        "checksum": {
                            "valid": True,
                            "expected": 3.0,
                            "actual": 3.0,
                            "error": 0.0,
                            "formula": "max(0, min(5, 2.50 + 0.50))",
                        },
                    },
                    "Data Management": {
                        "weighted_score": 4.0,
                        "total_modifier": -0.5,
                        "adjusted_score": 4.0,  # WRONG! Should be 3.5
                        "checksum": {
                            "valid": False,
                            "expected": 3.5,
                            "actual": 4.0,
                            "error": 0.5,
                            "formula": "max(0, min(5, 4.00 + -0.50))",
                        },
                    },
                }
            }
        }

        results = generator.verify_report_calculations(report)

        # Should fail validation
        self.assertFalse(results["valid"])
        self.assertEqual(results["dimensions_checked"], 2)
        self.assertEqual(results["dimensions_valid"], 1)
        self.assertEqual(results["dimensions_invalid"], 1)
        self.assertEqual(len(results["errors"]), 1)

        # Verify error details
        error = results["errors"][0]
        self.assertEqual(error["dimension"], "Data Management")
        self.assertEqual(error["expected"], 3.5)
        self.assertEqual(error["actual"], 4.0)
        self.assertEqual(error["error"], 0.5)

    def test_verify_report_calculations_missing_checksums(self):
        """Test verification handles dimensions without checksums"""
        generator = ReportGenerator(self.test_sheet_data, enable_ai=False)

        # Create report with missing checksums
        report = {
            "maturity": {
                "variance_analysis": {
                    "Infrastructure": {
                        "weighted_score": 2.5,
                        "total_modifier": 0.5,
                        "adjusted_score": 3.0,
                        # No checksum!
                    },
                    "Data Management": {
                        "weighted_score": 4.0,
                        "total_modifier": -0.5,
                        "adjusted_score": 3.5,
                        "checksum": {
                            "valid": True,
                            "expected": 3.5,
                            "actual": 3.5,
                            "error": 0.0,
                            "formula": "max(0, min(5, 4.00 + -0.50))",
                        },
                    },
                }
            }
        }

        results = generator.verify_report_calculations(report)

        # Should still pass but with warnings
        self.assertTrue(results["valid"])
        self.assertEqual(results["dimensions_checked"], 2)
        self.assertEqual(results["dimensions_valid"], 1)
        self.assertEqual(len(results["warnings"]), 1)
        self.assertIn("Infrastructure: No checksum available", results["warnings"][0])

    def test_checksum_hash_uniqueness(self):
        """Test that different calculations produce different checksums"""
        generator = ReportGenerator(self.test_sheet_data, enable_ai=False)

        analysis1 = {"weighted_score": 3.0, "total_modifier": 0.5, "adjusted_score": 3.5}

        analysis2 = {"weighted_score": 2.0, "total_modifier": 1.5, "adjusted_score": 3.5}

        checksum1 = generator._calculate_dimension_checksum(analysis1)
        checksum2 = generator._calculate_dimension_checksum(analysis2)

        # Different input components should produce different checksums
        self.assertNotEqual(checksum1["checksum"], checksum2["checksum"])

    def test_checksum_floating_point_tolerance(self):
        """Test that tiny floating point errors are tolerated"""
        generator = ReportGenerator(self.test_sheet_data, enable_ai=False)

        # Simulate tiny floating point error
        analysis = {
            "weighted_score": 3.0,
            "total_modifier": 0.5,
            "adjusted_score": 3.5000000001,  # Tiny floating point error
        }

        checksum = generator._calculate_dimension_checksum(analysis)

        # Should still pass validation (error tolerance is 0.001)
        self.assertTrue(checksum["valid"], "Tiny floating point errors should be tolerated")
        self.assertLess(checksum["error"], 0.001)

    def test_add_checksums_to_all_dimensions(self):
        """Test that checksums are added to ALL dimensions via centralized modifier calculation"""
        generator = ReportGenerator(self.test_sheet_data, enable_ai=False)

        # Create variance analysis with dimensions that need checksums
        variance_analysis = {
            "Infrastructure": {
                "weighted_score": 2.5,
                # No total_modifier - should default to 0
                # No adjusted_score - should be calculated
                # No checksum - should be added
            },
            "Program Technology": {
                "weighted_score": 3.5,
                # Will be calculated based on modifiers (if any)
            },
            "Data Management": {
                "weighted_score": 4.0,
                # No total_modifier, adjusted_score, or checksum
            },
        }

        # Call the centralized modifier calculation method
        generator._calculate_and_apply_all_modifiers(
            org_name="Test Org",
            variance_analysis=variance_analysis,
            admin_edits=None,
            ai_insights=None,
        )

        # Verify Infrastructure now has checksum
        self.assertIn("checksum", variance_analysis["Infrastructure"])
        self.assertIn("total_modifier", variance_analysis["Infrastructure"])
        self.assertIn("adjusted_score", variance_analysis["Infrastructure"])
        self.assertEqual(variance_analysis["Infrastructure"]["total_modifier"], 0)
        self.assertEqual(variance_analysis["Infrastructure"]["adjusted_score"], 2.5)
        self.assertTrue(variance_analysis["Infrastructure"]["checksum"]["valid"])

        # Verify Program Technology has checksum
        self.assertIn("checksum", variance_analysis["Program Technology"])
        self.assertEqual(variance_analysis["Program Technology"]["total_modifier"], 0)
        self.assertEqual(variance_analysis["Program Technology"]["adjusted_score"], 3.5)
        self.assertTrue(variance_analysis["Program Technology"]["checksum"]["valid"])

        # Verify Data Management now has checksum
        self.assertIn("checksum", variance_analysis["Data Management"])
        self.assertEqual(variance_analysis["Data Management"]["total_modifier"], 0)
        self.assertEqual(variance_analysis["Data Management"]["adjusted_score"], 4.0)
        self.assertTrue(variance_analysis["Data Management"]["checksum"]["valid"])

    def test_ai_modifiers_applied_to_adjusted_score(self):
        """
        CRITICAL TEST: Verify AI-generated modifiers are applied to adjusted_score.

        This test prevents regression of the bug where modifiers were calculated
        but not applied (lines 474-478 in report_generator.py).
        """
        # Load real sheet data for testing
        from src.extractors.sheets_reader import SheetsReader

        sheet_data = SheetsReader.fetch_all_tabs(verbose=False, use_cache=True)

        # Generate a test report with AI modifiers
        generator = ReportGenerator(sheet_data, enable_ai=True)
        report = generator.generate_organization_report("Hadar Institute")

        # Check at least one dimension has modifiers
        has_modifiers = False
        for dimension_name, dimension_data in report["ai_insights"]["dimensions"].items():
            if dimension_data.get("modifiers") and len(dimension_data["modifiers"]) > 0:
                has_modifiers = True

                # Get scores
                variance = report["maturity"]["variance_analysis"][dimension_name]
                base_score = variance.get("weighted_score", 0)
                total_modifier = variance.get("total_modifier", 0)
                adjusted_score = variance.get("adjusted_score", 0)

                # Calculate expected adjusted score
                expected_adjusted = max(0, min(5, base_score + total_modifier))

                # CRITICAL ASSERTION: Adjusted score must equal base + modifier
                self.assertAlmostEqual(
                    adjusted_score,
                    expected_adjusted,
                    places=2,
                    msg=f"{dimension_name}: Adjusted score {adjusted_score} != "
                    f"expected {expected_adjusted} (base {base_score} + modifier {total_modifier})",
                )

                # If modifiers exist and aren't zero, adjusted must differ from base
                if abs(total_modifier) > 0.01:
                    self.assertNotAlmostEqual(
                        adjusted_score,
                        base_score,
                        places=2,
                        msg=f"{dimension_name}: Adjusted score {adjusted_score} should differ "
                        f"from base score {base_score} when modifier {total_modifier} != 0",
                    )

        # Ensure we actually tested something
        self.assertTrue(has_modifiers, "Test requires at least one dimension with AI modifiers")


if __name__ == "__main__":
    unittest.main()
