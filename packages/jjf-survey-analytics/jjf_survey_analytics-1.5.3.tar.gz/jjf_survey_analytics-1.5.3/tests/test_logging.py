"""
Test script to demonstrate enhanced error logging for AI analysis
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analytics.logging_config import get_logger, setup_logging


def test_logging_setup():
    """Test that logging is properly configured"""
    print("\n=== Testing Logging Setup ===")

    # Configure logging
    setup_logging(log_level="DEBUG", log_to_file=True)

    logger = get_logger(__name__)
    logger.info("Logging system initialized successfully")

    print("✓ Logging configured")
    print("✓ Log files will be created in: logs/")


def test_log_levels():
    """Test different log levels"""
    print("\n=== Testing Log Levels ===")

    logger = get_logger("test_module")

    logger.debug("This is a DEBUG message - detailed information")
    logger.info("This is an INFO message - general information")
    logger.warning("This is a WARNING message - something to watch")
    logger.error("This is an ERROR message - something went wrong")
    logger.critical("This is a CRITICAL message - system failure")

    print("✓ All log levels tested")


def test_json_parse_error():
    """Simulate a JSON parsing error like in AI analysis"""
    print("\n=== Simulating JSON Parse Error ===")

    logger = get_logger("src.analytics.ai_analyzer")

    dimension = "Program Technology"
    malformed_json = """{
  "modifiers": [
    {
      "respondent": "John Doe",
      "role": "Tech Lead"
      "value": -0.5,
    }
  ]
}"""

    try:
        json.loads(malformed_json)
    except json.JSONDecodeError as e:
        # This mimics the enhanced error logging in ai_analyzer.py
        logger.error(
            f"JSON parsing error in dimension analysis for {dimension}",
            extra={
                "dimension": dimension,
                "error_type": "JSONDecodeError",
                "error_message": str(e),
                "json_error_line": e.lineno,
                "json_error_column": e.colno,
                "json_error_position": e.pos,
                "response_preview": malformed_json[:500],
                "full_response_length": len(malformed_json),
                "response_count": 3,
            },
        )

        # Log full response to debug
        logger.debug(f"Full AI response content for {dimension}:\n{malformed_json}")

        print("✓ JSON parse error logged with full context")
        print(f"  - Error line: {e.lineno}")
        print(f"  - Error column: {e.colno}")
        print(f"  - Error position: {e.pos}")


def test_success_logging():
    """Test successful AI response parsing"""
    print("\n=== Testing Success Case ===")

    logger = get_logger("src.analytics.ai_analyzer")

    dimension = "Business Systems"
    valid_json = """{
  "modifiers": [
    {
      "respondent": "Jane Smith",
      "role": "CEO",
      "value": 0.7,
      "factor": "Strong digital systems integration",
      "reasoning": "Excellent cross-platform data flow",
      "original_text": "Our systems work seamlessly together"
    }
  ],
  "summary": "Organization shows strong business systems maturity."
}"""

    try:
        logger.debug(f"Raw AI response length for {dimension}: {len(valid_json)} chars")
        logger.debug(f"Extracted content for {dimension} (first 200 chars): {valid_json[:200]}")

        result = json.loads(valid_json)
        logger.info(f"Successfully parsed AI response for dimension: {dimension}")

        print("✓ Successful parsing logged")
        print(f"  - Response length: {len(valid_json)} chars")
        print(f"  - Modifiers found: {len(result['modifiers'])}")
    except json.JSONDecodeError as e:
        print(f"✗ Unexpected parse error: {e}")


def test_structured_context():
    """Test logging with structured context"""
    print("\n=== Testing Structured Context ===")

    logger = get_logger("test_context")

    # Example with extra context
    logger.error(
        "Failed to process survey response",
        extra={
            "organization": "Test Org",
            "survey_type": "CEO",
            "question_id": "C-PT-1",
            "response_length": 247,
            "error_code": "VALIDATION_FAILED",
        },
    )

    print("✓ Structured context logged")


def verify_log_files():
    """Verify that log files were created"""
    print("\n=== Verifying Log Files ===")

    log_dir = Path("logs")
    log_files = {
        "app.log": "Main application log",
        "error.log": "Error-only log",
        "debug.log": "Debug-level log",
    }

    for log_file, description in log_files.items():
        log_path = log_dir / log_file
        if log_path.exists():
            size = log_path.stat().st_size
            print(f"✓ {log_file} created ({size} bytes) - {description}")
        else:
            print(f"✗ {log_file} NOT FOUND")


def main():
    """Run all logging tests"""
    print("=" * 60)
    print("Enhanced Logging Test Suite")
    print("=" * 60)

    try:
        test_logging_setup()
        test_log_levels()
        test_json_parse_error()
        test_success_logging()
        test_structured_context()
        verify_log_files()

        print("\n" + "=" * 60)
        print("All Tests Completed Successfully!")
        print("=" * 60)
        print("\nCheck the following files for detailed logs:")
        print("  - logs/app.log    (INFO and above)")
        print("  - logs/error.log  (ERROR and above)")
        print("  - logs/debug.log  (DEBUG and above)")
        print("\nNote: Console output shows INFO and above only.")

    except Exception as e:
        print(f"\n✗ Test suite failed: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
