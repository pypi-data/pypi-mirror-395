"""
Basic tests to verify the project setup.
"""

import pytest

from src.surveyor.config.container import DIContainer
from src.surveyor.config.settings import load_config
from src.surveyor.utils.data_type_detector import DataTypeDetector


def test_di_container():
    """Test that DI container works."""
    container = DIContainer()

    # Test registering and getting a simple class
    class TestService:
        def __init__(self):
            self.value = "test"

    container.register_singleton(TestService, TestService)
    service = container.get(TestService)

    assert service.value == "test"

    # Test singleton behavior
    service2 = container.get(TestService)
    assert service is service2


def test_config_loading():
    """Test that configuration loads without errors."""
    config = load_config()

    assert config is not None
    assert config.database is not None
    assert config.google_sheets is not None
    assert config.logging is not None
    assert len(config.sheet_urls) == 6  # Default URLs


def test_data_type_detector():
    """Test data type detection."""
    detector = DataTypeDetector()

    # Test numeric detection
    result = detector.detect_and_convert("123.45")
    assert result["numeric_value"] == 123.45
    assert result["text_value"] == "123.45"

    # Test boolean detection
    result = detector.detect_and_convert("true")
    assert result["boolean_value"] is True
    assert result["text_value"] == "true"

    # Test text fallback
    result = detector.detect_and_convert("some text")
    assert result["text_value"] == "some text"
    assert result["numeric_value"] is None
    assert result["boolean_value"] is None


def test_column_type_detection():
    """Test column type detection."""
    detector = DataTypeDetector()

    # Test numeric column
    numeric_values = ["1", "2.5", "3", "4.7"]
    assert detector.detect_column_type(numeric_values) == "numeric"

    # Test boolean column
    boolean_values = ["true", "false", "yes", "no"]
    assert detector.detect_column_type(boolean_values) == "boolean"

    # Test text column
    text_values = ["hello", "world", "test", "data"]
    assert detector.detect_column_type(text_values) == "text"


if __name__ == "__main__":
    pytest.main([__file__])
