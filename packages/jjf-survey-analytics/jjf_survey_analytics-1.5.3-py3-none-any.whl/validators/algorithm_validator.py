"""
Algorithm Configuration Validator.

Validates algorithm configuration structure and values for the JJF Survey Analytics
maturity assessment framework.
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ValidationSeverity(Enum):
    """Validation error severity levels."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationError:
    """Represents a validation error with context."""

    field: str
    message: str
    severity: ValidationSeverity
    expected: Optional[Any] = None
    actual: Optional[Any] = None


@dataclass
class ValidationResult:
    """Result of configuration validation."""

    valid: bool = True
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)

    def add_error(self, field: str, message: str, expected: Any = None, actual: Any = None) -> None:
        """Add an error to the validation result."""
        self.errors.append(
            ValidationError(
                field=field,
                message=message,
                severity=ValidationSeverity.ERROR,
                expected=expected,
                actual=actual,
            )
        )
        self.valid = False

    def add_warning(
        self, field: str, message: str, expected: Any = None, actual: Any = None
    ) -> None:
        """Add a warning to the validation result."""
        self.warnings.append(
            ValidationError(
                field=field,
                message=message,
                severity=ValidationSeverity.WARNING,
                expected=expected,
                actual=actual,
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert validation result to dictionary."""
        return {
            "valid": self.valid,
            "errors": [
                {
                    "field": e.field,
                    "message": e.message,
                    "severity": e.severity.value,
                    "expected": e.expected,
                    "actual": e.actual,
                }
                for e in self.errors
            ],
            "warnings": [
                {
                    "field": w.field,
                    "message": w.message,
                    "severity": w.severity.value,
                    "expected": w.expected,
                    "actual": w.actual,
                }
                for w in self.warnings
            ],
        }

    def get_error_messages(self) -> List[str]:
        """Get list of error messages for backward compatibility."""
        return [e.message for e in self.errors]


class AlgorithmValidator:
    """
    Validates algorithm configuration for maturity assessment.

    Validates:
    - Top-level structure and version
    - Maturity assessment configuration
    - Variance thresholds
    - Maturity levels
    - Dimension weights
    - AI analysis configuration
    - Scoring configuration
    """

    HEX_COLOR_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")

    def __init__(self):
        """Initialize the validator."""

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        """
        Validate algorithm configuration.

        Args:
            config: Algorithm configuration dictionary

        Returns:
            ValidationResult with errors and warnings
        """
        result = ValidationResult()

        # Validate top-level structure
        self._validate_top_level(config, result)

        # Validate algorithm_config section
        if "algorithm_config" in config and isinstance(config["algorithm_config"], dict):
            alg_config = config["algorithm_config"]
            self._validate_maturity_assessment(alg_config, result)
            self._validate_ai_analysis(alg_config, result)
            self._validate_scoring(alg_config, result)

        return result

    def _validate_top_level(self, config: Dict[str, Any], result: ValidationResult) -> None:
        """Validate top-level configuration structure."""
        # Check required fields
        if "version" not in config:
            result.add_error("version", "Missing required field: version")
        elif not isinstance(config["version"], (int, float)) or config["version"] < 1:
            result.add_error(
                "version",
                "Version must be a positive number (1, 2, 3...)",
                "number >= 1",
                config["version"],
            )

        if "algorithm_config" not in config:
            result.add_error("algorithm_config", "Missing required field: algorithm_config")

    def _validate_maturity_assessment(
        self, alg_config: Dict[str, Any], result: ValidationResult
    ) -> None:
        """Validate maturity_assessment configuration."""
        if not isinstance(alg_config, dict):
            result.add_error("algorithm_config", "algorithm_config must be a dictionary")
            return

        if "maturity_assessment" not in alg_config:
            result.add_error("algorithm_config.maturity_assessment", "Missing maturity_assessment")
            return

        ma = alg_config["maturity_assessment"]

        # Validate variance thresholds
        self._validate_variance_thresholds(ma, result)

        # Validate maturity levels
        self._validate_maturity_levels(ma, result)

        # Validate dimension weights
        self._validate_dimension_weights(ma, result)

    def _validate_variance_thresholds(self, ma: Dict[str, Any], result: ValidationResult) -> None:
        """Validate variance thresholds configuration."""
        if "variance_thresholds" not in ma:
            result.add_error(
                "maturity_assessment.variance_thresholds", "Missing variance_thresholds"
            )
            return

        vt = ma["variance_thresholds"]
        required_levels = ["low", "medium", "high"]

        for level in required_levels:
            if level not in vt:
                result.add_error(
                    f"variance_thresholds.{level}", f"Missing variance threshold: {level}"
                )
                continue

            threshold = vt[level]

            # Validate max value (high threshold may not have max)
            if "max" in threshold:
                max_val = threshold["max"]
                if not isinstance(max_val, (int, float)) or max_val < 0:
                    result.add_error(
                        f"variance_thresholds.{level}.max",
                        f"Invalid max value for {level} (must be a positive number)",
                        "number >= 0",
                        max_val,
                    )
            elif level in ["low", "medium"]:
                result.add_error(
                    f"variance_thresholds.{level}.max",
                    f"Missing max value for {level} variance threshold",
                )

            # Validate color
            color = threshold.get("color", "")
            if not self.HEX_COLOR_PATTERN.match(color):
                result.add_error(
                    f"variance_thresholds.{level}.color",
                    f"Invalid color for {level} (must be hex format: #RRGGBB)",
                    "#RRGGBB",
                    color,
                )

            # Validate label
            if not threshold.get("label") or not isinstance(threshold["label"], str):
                result.add_error(
                    f"variance_thresholds.{level}.label",
                    f"Missing or invalid label for {level} variance threshold",
                )

        # Validate threshold ordering
        if all(level in vt for level in ["low", "medium"]):
            low_max = vt["low"].get("max")
            med_max = vt["medium"].get("max")

            if isinstance(low_max, (int, float)) and isinstance(med_max, (int, float)):
                if low_max >= med_max:
                    result.add_error(
                        "variance_thresholds",
                        f"Thresholds must be ordered: low.max ({low_max}) < medium.max ({med_max})",
                        "low.max < medium.max",
                        f"{low_max} >= {med_max}",
                    )

                # Check high.max if it exists
                if "high" in vt and "max" in vt["high"]:
                    high_max = vt["high"]["max"]
                    if isinstance(high_max, (int, float)) and med_max >= high_max:
                        result.add_error(
                            "variance_thresholds",
                            f"Thresholds must be ordered: medium.max ({med_max}) < high.max ({high_max})",
                            "medium.max < high.max",
                            f"{med_max} >= {high_max}",
                        )

    def _validate_maturity_levels(self, ma: Dict[str, Any], result: ValidationResult) -> None:
        """Validate maturity levels configuration."""
        if "maturity_levels" not in ma:
            result.add_error("maturity_assessment.maturity_levels", "Missing maturity_levels")
            return

        ml = ma["maturity_levels"]
        required_levels = ["1_building", "2_emerging", "3_thriving"]

        for level in required_levels:
            if level not in ml:
                result.add_error(f"maturity_levels.{level}", f"Missing maturity level: {level}")
                continue

            level_config = ml[level]

            # Validate score_range
            if "score_range" not in level_config:
                result.add_error(
                    f"maturity_levels.{level}.score_range", f"Missing score_range for {level}"
                )
            else:
                sr = level_config["score_range"]
                min_score = sr.get("min")
                max_score = sr.get("max")

                if not isinstance(min_score, (int, float)) or min_score < 0:
                    result.add_error(
                        f"maturity_levels.{level}.score_range.min",
                        f"Invalid min score for {level} (must be >= 0)",
                        ">= 0",
                        min_score,
                    )

                if not isinstance(max_score, (int, float)) or max_score > 100:
                    result.add_error(
                        f"maturity_levels.{level}.score_range.max",
                        f"Invalid max score for {level} (must be <= 100)",
                        "<= 100",
                        max_score,
                    )

                if isinstance(min_score, (int, float)) and isinstance(max_score, (int, float)):
                    if min_score >= max_score:
                        result.add_error(
                            f"maturity_levels.{level}.score_range",
                            f"Invalid score range: min ({min_score}) must be < max ({max_score})",
                            "min < max",
                            f"{min_score} >= {max_score}",
                        )

            # Validate percentage_range
            if "percentage_range" not in level_config:
                result.add_error(
                    f"maturity_levels.{level}.percentage_range",
                    f"Missing percentage_range for {level}",
                )
            else:
                pr = level_config["percentage_range"]
                min_pct = pr.get("min")
                max_pct = pr.get("max")

                if not isinstance(min_pct, (int, float)) or min_pct < 0 or min_pct > 100:
                    result.add_error(
                        f"maturity_levels.{level}.percentage_range.min",
                        f"Invalid min percentage for {level} (must be 0-100)",
                        "0-100",
                        min_pct,
                    )

                if not isinstance(max_pct, (int, float)) or max_pct < 0 or max_pct > 100:
                    result.add_error(
                        f"maturity_levels.{level}.percentage_range.max",
                        f"Invalid max percentage for {level} (must be 0-100)",
                        "0-100",
                        max_pct,
                    )

                if isinstance(min_pct, (int, float)) and isinstance(max_pct, (int, float)):
                    if min_pct >= max_pct:
                        result.add_error(
                            f"maturity_levels.{level}.percentage_range",
                            f"Invalid percentage range for {level}: min must be < max",
                            "min < max",
                            f"{min_pct} >= {max_pct}",
                        )

            # Validate color
            color = level_config.get("color", "")
            if not self.HEX_COLOR_PATTERN.match(color):
                result.add_error(
                    f"maturity_levels.{level}.color",
                    f"Invalid color for {level} (must be hex format: #RRGGBB)",
                    "#RRGGBB",
                    color,
                )

            # Validate name
            if not level_config.get("name") or not isinstance(level_config["name"], str):
                result.add_error(
                    f"maturity_levels.{level}.name", f"Missing or invalid name for {level}"
                )

    def _validate_dimension_weights(self, ma: Dict[str, Any], result: ValidationResult) -> None:
        """Validate dimension weights configuration."""
        if "dimension_weights" not in ma:
            result.add_error("maturity_assessment.dimension_weights", "Missing dimension_weights")
            return

        dw = ma["dimension_weights"]
        required_dimensions = [
            "program_technology",
            "business_systems",
            "data_analytics",
            "infrastructure",
            "organizational_culture",
        ]

        total_weight = 0.0
        for dim in required_dimensions:
            weight = dw.get(dim)

            if not isinstance(weight, (int, float)):
                result.add_error(
                    f"dimension_weights.{dim}",
                    f"Missing or invalid weight for dimension: {dim}",
                    "number",
                    type(weight).__name__,
                )
            elif weight < 0 or weight > 1:
                result.add_error(
                    f"dimension_weights.{dim}",
                    f"Weight for {dim} must be between 0 and 1 (got {weight})",
                    "0 <= weight <= 1",
                    weight,
                )
            else:
                total_weight += weight

        # Validate weights sum to 1.0 (with tolerance)
        if abs(total_weight - 1.0) > 0.01:
            result.add_error(
                "dimension_weights",
                f"Dimension weights must sum to 1.0 (currently {total_weight:.2f})",
                1.0,
                total_weight,
            )

    def _validate_ai_analysis(self, alg_config: Dict[str, Any], result: ValidationResult) -> None:
        """Validate AI analysis configuration."""
        if "ai_analysis" not in alg_config:
            # AI analysis is optional
            return

        ai = alg_config["ai_analysis"]

        # Validate model_config
        if "model_config" not in ai:
            result.add_error("ai_analysis.model_config", "Missing model_config")
        else:
            mc = ai["model_config"]

            if not mc.get("model_name") or not isinstance(mc["model_name"], str):
                result.add_error(
                    "ai_analysis.model_config.model_name",
                    "AI model_name must be specified as a string",
                )

            timeout = mc.get("timeout_seconds")
            if not isinstance(timeout, (int, float)) or timeout < 10:
                result.add_error(
                    "ai_analysis.model_config.timeout_seconds",
                    "AI timeout_seconds must be >= 10",
                    ">= 10",
                    timeout,
                )

            max_retries = mc.get("max_retries")
            if not isinstance(max_retries, int) or max_retries < 0:
                result.add_error(
                    "ai_analysis.model_config.max_retries",
                    "AI max_retries must be >= 0",
                    ">= 0",
                    max_retries,
                )

        # Validate token_limits
        if "token_limits" not in ai:
            result.add_error("ai_analysis.token_limits", "Missing token_limits")
        else:
            tl = ai["token_limits"]
            required_limits = ["dimension_analysis", "dimension_insights", "aggregate_summary"]

            for limit_type in required_limits:
                if limit_type not in tl:
                    result.add_error(
                        f"ai_analysis.token_limits.{limit_type}",
                        f"Missing token limit: {limit_type}",
                    )
                else:
                    limit = tl[limit_type]

                    max_tokens = limit.get("max_tokens")
                    if not isinstance(max_tokens, (int, float)) or max_tokens < 100:
                        result.add_error(
                            f"ai_analysis.token_limits.{limit_type}.max_tokens",
                            f"{limit_type}.max_tokens must be >= 100",
                            ">= 100",
                            max_tokens,
                        )

                    temperature = limit.get("temperature")
                    if not isinstance(temperature, (int, float)) or not (0 <= temperature <= 2):
                        result.add_error(
                            f"ai_analysis.token_limits.{limit_type}.temperature",
                            f"{limit_type}.temperature must be between 0 and 2",
                            "0-2",
                            temperature,
                        )

    def _validate_scoring(self, alg_config: Dict[str, Any], result: ValidationResult) -> None:
        """Validate scoring configuration."""
        if "scoring" not in alg_config:
            # Scoring is optional
            return

        sc = alg_config["scoring"]

        if "valid_score_range" in sc:
            vsr = sc["valid_score_range"]
            min_score = vsr.get("min")
            max_score = vsr.get("max")

            if not isinstance(min_score, (int, float)) or min_score < 1:
                result.add_error(
                    "scoring.valid_score_range.min",
                    "valid_score_range.min must be >= 1",
                    ">= 1",
                    min_score,
                )

            if not isinstance(max_score, (int, float)) or max_score > 10:
                result.add_error(
                    "scoring.valid_score_range.max",
                    "valid_score_range.max must be <= 10",
                    "<= 10",
                    max_score,
                )

            if isinstance(min_score, (int, float)) and isinstance(max_score, (int, float)):
                if min_score >= max_score:
                    result.add_error(
                        "scoring.valid_score_range",
                        "valid_score_range.min must be < max",
                        "min < max",
                        f"{min_score} >= {max_score}",
                    )


# Singleton instance
_validator_instance: Optional[AlgorithmValidator] = None


def get_algorithm_validator() -> AlgorithmValidator:
    """Get the singleton AlgorithmValidator instance."""
    global _validator_instance
    if _validator_instance is None:
        _validator_instance = AlgorithmValidator()
    return _validator_instance


def reset_algorithm_validator() -> None:
    """Reset the singleton validator instance (for testing)."""
    global _validator_instance
    _validator_instance = None
