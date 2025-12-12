#!/usr/bin/env python3
"""
Test script for algorithm configuration validation.
Tests both valid and invalid configurations to ensure validation works properly.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path to import app
sys.path.insert(0, str(Path(__file__).parent))

from app import validate_algorithm_config


def test_valid_config():
    """Test that a valid configuration passes validation."""
    with open("config/algorithm_config.json", "r") as f:
        valid_config = json.load(f)

    is_valid, errors = validate_algorithm_config(valid_config)

    print("Test 1: Valid Configuration")
    print(f"Result: {'PASS' if is_valid else 'FAIL'}")
    if not is_valid:
        print(f"Errors: {errors}")
    print()

    return is_valid


def test_missing_version():
    """Test that missing version is caught."""
    config = {"algorithm_config": {"maturity_assessment": {}}}

    is_valid, errors = validate_algorithm_config(config)

    print("Test 2: Missing Version")
    print(f"Result: {'PASS' if not is_valid else 'FAIL'}")
    print(f"Errors: {errors}")
    print()

    return not is_valid and any("version" in err.lower() for err in errors)


def test_invalid_version():
    """Test that invalid version is caught."""
    config = {"version": -1, "algorithm_config": {}}

    is_valid, errors = validate_algorithm_config(config)

    print("Test 3: Invalid Version (negative)")
    print(f"Result: {'PASS' if not is_valid else 'FAIL'}")
    print(f"Errors: {errors}")
    print()

    return not is_valid and any("version" in err.lower() for err in errors)


def test_invalid_variance_threshold_ordering():
    """Test that incorrect variance threshold ordering is caught."""
    config = {
        "version": 1,
        "algorithm_config": {
            "maturity_assessment": {
                "variance_thresholds": {
                    "low": {"max": 1.5, "color": "#10b981", "label": "Low"},
                    "medium": {
                        "max": 1.0,
                        "color": "#f59e0b",
                        "label": "Medium",
                    },  # Invalid: should be > low
                    "high": {"max": 2.0, "color": "#ef4444", "label": "High"},
                }
            }
        },
    }

    is_valid, errors = validate_algorithm_config(config)

    print("Test 4: Invalid Variance Threshold Ordering")
    print(f"Result: {'PASS' if not is_valid else 'FAIL'}")
    print(f"Errors: {errors}")
    print()

    return not is_valid and any("ordered" in err.lower() for err in errors)


def test_invalid_hex_color():
    """Test that invalid hex colors are caught."""
    config = {
        "version": 1,
        "algorithm_config": {
            "maturity_assessment": {
                "variance_thresholds": {
                    "low": {"max": 0.8, "color": "red", "label": "Low"},  # Invalid: not hex
                    "medium": {"max": 1.6, "color": "#f59e0b", "label": "Medium"},
                    "high": {"max": 2.4, "color": "#ef4444", "label": "High"},
                }
            }
        },
    }

    is_valid, errors = validate_algorithm_config(config)

    print("Test 5: Invalid Hex Color")
    print(f"Result: {'PASS' if not is_valid else 'FAIL'}")
    print(f"Errors: {errors}")
    print()

    return not is_valid and any("hex" in err.lower() or "color" in err.lower() for err in errors)


def test_invalid_dimension_weights():
    """Test that dimension weights not summing to 1.0 is caught."""
    config = {
        "version": 1,
        "algorithm_config": {
            "maturity_assessment": {
                "variance_thresholds": {
                    "low": {"max": 0.8, "color": "#10b981", "label": "Low"},
                    "medium": {"max": 1.6, "color": "#f59e0b", "label": "Medium"},
                    "high": {"min": 1.6, "color": "#ef4444", "label": "High"},
                },
                "maturity_levels": {
                    "1_building": {
                        "name": "Building",
                        "score_range": {"min": 0, "max": 35},
                        "percentage_range": {"min": 0, "max": 35},
                        "color": "#ef4444",
                    },
                    "2_emerging": {
                        "name": "Emerging",
                        "score_range": {"min": 35, "max": 70},
                        "percentage_range": {"min": 36, "max": 70},
                        "color": "#f59e0b",
                    },
                    "3_thriving": {
                        "name": "Thriving",
                        "score_range": {"min": 70, "max": 100},
                        "percentage_range": {"min": 71, "max": 100},
                        "color": "#10b981",
                    },
                },
                "dimension_weights": {
                    "program_technology": 0.30,
                    "business_systems": 0.30,
                    "data_analytics": 0.20,  # Total: 0.95 (should be 1.0)
                    "infrastructure": 0.10,
                    "organizational_culture": 0.05,
                },
            }
        },
    }

    is_valid, errors = validate_algorithm_config(config)

    print("Test 6: Invalid Dimension Weights (not summing to 1.0)")
    print(f"Result: {'PASS' if not is_valid else 'FAIL'}")
    print(f"Errors: {errors}")
    print()

    return not is_valid and any("sum to 1.0" in err for err in errors)


def test_missing_maturity_level():
    """Test that missing required maturity levels are caught."""
    config = {
        "version": 1,
        "algorithm_config": {
            "maturity_assessment": {
                "maturity_levels": {
                    "1_building": {
                        "name": "Building",
                        "score_range": {"min": 0, "max": 35},
                        "percentage_range": {"min": 0, "max": 35},
                        "color": "#ef4444",
                    }
                    # Missing 2_emerging and 3_thriving
                }
            }
        },
    }

    is_valid, errors = validate_algorithm_config(config)

    print("Test 7: Missing Required Maturity Levels")
    print(f"Result: {'PASS' if not is_valid else 'FAIL'}")
    print(f"Errors: {errors}")
    print()

    return not is_valid and any("maturity level" in err.lower() for err in errors)


def test_invalid_score_range():
    """Test that invalid score ranges are caught."""
    config = {
        "version": 1,
        "algorithm_config": {
            "maturity_assessment": {
                "maturity_levels": {
                    "1_building": {
                        "name": "Building",
                        "score_range": {"min": 50, "max": 35},  # Invalid: min > max
                        "percentage_range": {"min": 0, "max": 35},
                        "color": "#ef4444",
                    },
                    "2_emerging": {
                        "name": "Emerging",
                        "score_range": {"min": 35, "max": 70},
                        "percentage_range": {"min": 36, "max": 70},
                        "color": "#f59e0b",
                    },
                    "3_thriving": {
                        "name": "Thriving",
                        "score_range": {"min": 70, "max": 100},
                        "percentage_range": {"min": 71, "max": 100},
                        "color": "#10b981",
                    },
                }
            }
        },
    }

    is_valid, errors = validate_algorithm_config(config)

    print("Test 8: Invalid Score Range (min > max)")
    print(f"Result: {'PASS' if not is_valid else 'FAIL'}")
    print(f"Errors: {errors}")
    print()

    return not is_valid and any("min" in err and "max" in err for err in errors)


def test_invalid_ai_temperature():
    """Test that invalid AI temperature is caught."""
    config = {
        "version": 1,
        "algorithm_config": {
            "ai_analysis": {
                "model_config": {
                    "model_name": "claude-3-5-sonnet-20241022",
                    "timeout_seconds": 60,
                    "max_retries": 3,
                },
                "token_limits": {
                    "dimension_analysis": {
                        "max_tokens": 2000,
                        "temperature": 3.5,  # Invalid: must be 0-2
                    },
                    "dimension_insights": {"max_tokens": 500, "temperature": 0.7},
                    "aggregate_summary": {"max_tokens": 2000, "temperature": 0.7},
                },
            }
        },
    }

    is_valid, errors = validate_algorithm_config(config)

    print("Test 9: Invalid AI Temperature (out of range)")
    print(f"Result: {'PASS' if not is_valid else 'FAIL'}")
    print(f"Errors: {errors}")
    print()

    return not is_valid and any("temperature" in err.lower() for err in errors)


def run_all_tests():
    """Run all validation tests."""
    print("=" * 80)
    print("Algorithm Configuration Validation Tests")
    print("=" * 80)
    print()

    tests = [
        ("Valid Configuration", test_valid_config),
        ("Missing Version", test_missing_version),
        ("Invalid Version", test_invalid_version),
        ("Invalid Variance Threshold Ordering", test_invalid_variance_threshold_ordering),
        ("Invalid Hex Color", test_invalid_hex_color),
        ("Invalid Dimension Weights", test_invalid_dimension_weights),
        ("Missing Maturity Level", test_missing_maturity_level),
        ("Invalid Score Range", test_invalid_score_range),
        ("Invalid AI Temperature", test_invalid_ai_temperature),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"Test '{name}' raised exception: {e}")
            results.append((name, False))

    print("=" * 80)
    print("Test Results Summary")
    print("=" * 80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print()
    print(f"Total: {passed}/{total} tests passed ({100 * passed // total}%)")
    print()

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
