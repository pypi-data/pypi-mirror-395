#!/usr/bin/env python3
"""
Test retry logic for dimension analysis orchestrator.

Tests the exponential backoff retry mechanism for handling transient AI service failures.
"""

import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from src.services.dimension_analysis_orchestrator import (
    DimensionAnalysisOrchestrator,
    RetryConfig,
)


class TestRetryLogic(unittest.TestCase):
    """Test retry logic with exponential backoff."""

    def setUp(self):
        """Set up test fixtures."""
        self.orchestrator = DimensionAnalysisOrchestrator()
        self.sheet_data = {
            "CEO": [{"Organization": "Test Org", "C-PT-OE": "Test response"}],
            "Tech": [],
            "Staff": [],
        }

    def test_retry_config_retryable_errors(self):
        """Test RetryConfig correctly identifies retryable errors."""
        # Retryable errors
        self.assertTrue(RetryConfig.is_retryable_error(ConnectionError()))
        self.assertTrue(RetryConfig.is_retryable_error(TimeoutError()))
        self.assertTrue(RetryConfig.is_retryable_error(asyncio.TimeoutError()))

        # Error messages
        self.assertTrue(
            RetryConfig.is_retryable_error(Exception("Connection timeout"))
        )
        self.assertTrue(RetryConfig.is_retryable_error(Exception("Rate limit exceeded")))
        self.assertTrue(RetryConfig.is_retryable_error(Exception("503 Service unavailable")))

        # Non-retryable errors
        self.assertFalse(RetryConfig.is_retryable_error(ValueError("Invalid data")))
        self.assertFalse(RetryConfig.is_retryable_error(KeyError("Missing key")))

    @patch("src.services.dimension_analysis_orchestrator.extract_free_text_responses")
    async def test_success_on_first_attempt(self, mock_extract):
        """Test successful analysis on first attempt (no retry)."""
        # Mock responses
        mock_extract.return_value = {
            "Program Technology": [
                {
                    "respondent": "Test CEO",
                    "role": "CEO",
                    "question_id": "C-PT-OE",
                    "text": "Test response",
                }
            ]
        }

        # Mock AI analyzer
        mock_ai_result = {
            "summary": "Test summary",
            "modifiers": [],
        }
        self.orchestrator.ai_analyzer.analyze_dimension_responses_async = AsyncMock(
            return_value=mock_ai_result
        )

        # Execute analysis
        result = await self.orchestrator.analyze_dimension(
            org_name="Test Org",
            dimension="Program Technology",
            sheet_data=self.sheet_data,
        )

        # Verify success
        self.assertFalse(result.get("error", False))
        self.assertEqual(result["summary"], "Test summary")
        self.assertEqual(
            self.orchestrator.ai_analyzer.analyze_dimension_responses_async.call_count,
            1,
        )

    @patch("src.services.dimension_analysis_orchestrator.extract_free_text_responses")
    @patch("asyncio.sleep")  # Mock sleep to speed up tests
    async def test_success_after_retry(self, mock_sleep, mock_extract):
        """Test success after transient failures."""
        # Mock responses
        mock_extract.return_value = {
            "Program Technology": [
                {
                    "respondent": "Test CEO",
                    "role": "CEO",
                    "question_id": "C-PT-OE",
                    "text": "Test response",
                }
            ]
        }

        # Mock AI analyzer - fail twice, then succeed
        mock_ai_result = {
            "summary": "Test summary",
            "modifiers": [],
        }
        self.orchestrator.ai_analyzer.analyze_dimension_responses_async = AsyncMock(
            side_effect=[
                ConnectionError("Connection failed"),
                TimeoutError("Timeout"),
                mock_ai_result,  # Success on 3rd attempt
            ]
        )

        # Execute analysis
        result = await self.orchestrator.analyze_dimension(
            org_name="Test Org",
            dimension="Program Technology",
            sheet_data=self.sheet_data,
        )

        # Verify success after retries
        self.assertFalse(result.get("error", False))
        self.assertEqual(result["summary"], "Test summary")
        self.assertEqual(
            self.orchestrator.ai_analyzer.analyze_dimension_responses_async.call_count,
            3,
        )

        # Verify exponential backoff delays
        self.assertEqual(mock_sleep.call_count, 2)
        mock_sleep.assert_any_call(2)  # First retry: 2^0 * 2 = 2s
        mock_sleep.assert_any_call(4)  # Second retry: 2^1 * 2 = 4s

    @patch("src.services.dimension_analysis_orchestrator.extract_free_text_responses")
    @patch("asyncio.sleep")
    async def test_max_retries_exceeded(self, mock_sleep, mock_extract):
        """Test failure after max retries exceeded."""
        # Mock responses
        mock_extract.return_value = {
            "Program Technology": [
                {
                    "respondent": "Test CEO",
                    "role": "CEO",
                    "question_id": "C-PT-OE",
                    "text": "Test response",
                }
            ]
        }

        # Mock AI analyzer - always fail
        self.orchestrator.ai_analyzer.analyze_dimension_responses_async = AsyncMock(
            side_effect=ConnectionError("Connection failed")
        )

        # Execute analysis
        result = await self.orchestrator.analyze_dimension(
            org_name="Test Org",
            dimension="Program Technology",
            sheet_data=self.sheet_data,
        )

        # Verify failure
        self.assertTrue(result.get("error", False))
        self.assertEqual(result.get("retry_attempts"), RetryConfig.MAX_ATTEMPTS)
        self.assertIn("after 3 attempts", result["summary"])

        # Verify all retries attempted
        self.assertEqual(
            self.orchestrator.ai_analyzer.analyze_dimension_responses_async.call_count,
            RetryConfig.MAX_ATTEMPTS,
        )

        # Verify exponential backoff delays
        self.assertEqual(mock_sleep.call_count, RetryConfig.MAX_ATTEMPTS - 1)

    @patch("src.services.dimension_analysis_orchestrator.extract_free_text_responses")
    async def test_non_retryable_error(self, mock_extract):
        """Test immediate failure on non-retryable error."""
        # Mock responses
        mock_extract.return_value = {
            "Program Technology": [
                {
                    "respondent": "Test CEO",
                    "role": "CEO",
                    "question_id": "C-PT-OE",
                    "text": "Test response",
                }
            ]
        }

        # Mock AI analyzer - non-retryable error
        self.orchestrator.ai_analyzer.analyze_dimension_responses_async = AsyncMock(
            side_effect=ValueError("Invalid data format")
        )

        # Execute analysis
        result = await self.orchestrator.analyze_dimension(
            org_name="Test Org",
            dimension="Program Technology",
            sheet_data=self.sheet_data,
        )

        # Verify immediate failure (no retries)
        self.assertTrue(result.get("error", False))
        self.assertEqual(
            self.orchestrator.ai_analyzer.analyze_dimension_responses_async.call_count,
            1,  # Only 1 attempt, no retries
        )

    @patch("src.services.dimension_analysis_orchestrator.extract_free_text_responses")
    @patch("asyncio.sleep")
    async def test_retry_sse_events(self, mock_sleep, mock_extract):
        """Test SSE progress events during retry."""
        # Mock responses
        mock_extract.return_value = {
            "Program Technology": [
                {
                    "respondent": "Test CEO",
                    "role": "CEO",
                    "question_id": "C-PT-OE",
                    "text": "Test response",
                }
            ]
        }

        # Mock AI analyzer - fail once, then succeed
        mock_ai_result = {
            "summary": "Test summary",
            "modifiers": [],
        }
        self.orchestrator.ai_analyzer.analyze_dimension_responses_async = AsyncMock(
            side_effect=[
                TimeoutError("Timeout"),
                mock_ai_result,  # Success on 2nd attempt
            ]
        )

        # Track progress callbacks
        progress_events = []

        def progress_callback(dim, step, data):
            progress_events.append({"dimension": dim, "step": step, "data": data})

        # Execute analysis with callback
        result = await self.orchestrator.analyze_dimension(
            org_name="Test Org",
            dimension="Program Technology",
            sheet_data=self.sheet_data,
            progress_callback=progress_callback,
        )

        # Verify success
        self.assertFalse(result.get("error", False))

        # Verify retry event was sent
        retry_events = [e for e in progress_events if e["step"] == "dimension_retry"]
        self.assertEqual(len(retry_events), 1)
        self.assertEqual(retry_events[0]["data"]["attempt"], 2)
        self.assertEqual(retry_events[0]["data"]["max_attempts"], RetryConfig.MAX_ATTEMPTS)
        self.assertEqual(retry_events[0]["data"]["retry_after"], 2)

    def test_exponential_backoff_calculation(self):
        """Test exponential backoff delay calculation."""
        # Verify backoff delays match expected formula: BASE_DELAY * (MULTIPLIER ** attempt)
        expected_delays = {
            1: 2,  # 2 * 2^0 = 2s
            2: 4,  # 2 * 2^1 = 4s
            3: 8,  # 2 * 2^2 = 8s
        }

        for attempt in range(1, RetryConfig.MAX_ATTEMPTS + 1):
            delay = RetryConfig.BASE_DELAY * (
                RetryConfig.BACKOFF_MULTIPLIER ** (attempt - 1)
            )
            self.assertEqual(delay, expected_delays[attempt])


def async_test(coro):
    """Decorator to run async tests."""

    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro(*args, **kwargs))
        finally:
            loop.close()

    return wrapper


# Apply async_test decorator to all async test methods
for attr_name in dir(TestRetryLogic):
    if attr_name.startswith("test_") and asyncio.iscoroutinefunction(
        getattr(TestRetryLogic, attr_name)
    ):
        setattr(
            TestRetryLogic,
            attr_name,
            async_test(getattr(TestRetryLogic, attr_name)),
        )


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
