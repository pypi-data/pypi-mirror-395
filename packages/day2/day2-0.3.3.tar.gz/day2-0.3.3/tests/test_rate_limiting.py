"""Tests for rate limiting functionality and error handling."""

import time
import unittest
from unittest.mock import Mock, patch

import requests

from day2 import Session
from day2.client.base import BaseClient
from day2.client.config import Config
from day2.exceptions import RateLimitError


class TestRateLimiting(unittest.TestCase):
    """Test rate limiting error handling and retry logic."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = Config(base_url="https://api.example.com")
        self.session = Session(
            api_key="test-key", api_secret_key="test-secret", config=self.config
        )
        self.client = BaseClient(self.session, "test-service")

    @patch("requests.request")
    def test_rate_limit_error_handling(self, mock_request):
        """Test that 429 responses raise RateLimitError."""
        # Mock a 429 response
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 429
        mock_response.json.return_value = {"Message": "Too many requests"}
        mock_response.text = '{"Message": "Too many requests"}'
        mock_response.headers = {"x-request-id": "test-request-id-429"}
        mock_request.return_value = mock_response

        # Test that RateLimitError is raised
        with self.assertRaises(RateLimitError) as context:
            self.client._make_request("GET", "test-endpoint")

        # Verify exception details
        error = context.exception
        self.assertEqual(error.status_code, 429)
        self.assertEqual(error.request_id, "test-request-id-429")
        self.assertIn("Too many requests", str(error))

    @patch("requests.request")
    def test_rate_limit_error_without_request_id(self, mock_request):
        """Test rate limit error handling without request ID."""
        # Mock a 429 response without request ID
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 429
        mock_response.json.return_value = {"Message": "Rate limit exceeded"}
        mock_response.text = '{"Message": "Rate limit exceeded"}'
        mock_response.headers = {}  # No request ID
        mock_request.return_value = mock_response

        with self.assertRaises(RateLimitError) as context:
            self.client._make_request("GET", "test-endpoint")

        error = context.exception
        self.assertEqual(error.status_code, 429)
        self.assertIsNone(error.request_id)
        self.assertIn("Rate limit exceeded", str(error))

    @patch("requests.request")
    def test_rate_limit_error_with_empty_response(self, mock_request):
        """Test rate limit error with non-JSON response."""
        # Mock a 429 response with non-JSON content
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 429
        mock_response.json.side_effect = ValueError("No JSON")
        mock_response.text = "Rate limit exceeded"
        mock_response.headers = {"x-request-id": "test-request-id-text"}
        mock_request.return_value = mock_response

        with self.assertRaises(RateLimitError) as context:
            self.client._make_request("GET", "test-endpoint")

        error = context.exception
        self.assertEqual(error.status_code, 429)
        self.assertEqual(error.request_id, "test-request-id-text")

    def test_rate_limit_error_inheritance(self):
        """Test that RateLimitError is properly inherited from ClientError."""
        from day2.exceptions import ClientError, Day2Error

        error = RateLimitError("Test message", 429, "test-id")

        # Test inheritance
        self.assertIsInstance(error, ClientError)
        self.assertIsInstance(error, Day2Error)
        self.assertIsInstance(error, Exception)

        # Test attributes
        self.assertEqual(error.status_code, 429)
        self.assertEqual(error.request_id, "test-id")

    @patch("time.sleep")
    def test_rate_limit_retry_with_backoff(self, mock_sleep):
        """Test retry logic with exponential backoff for rate limiting."""

        def retry_with_backoff(func, max_retries=3, base_delay=1):
            """Simple retry logic with exponential backoff."""
            for attempt in range(max_retries):
                try:
                    return func()
                except RateLimitError:
                    if attempt == max_retries - 1:
                        raise  # Re-raise on final attempt

                    delay = base_delay * (2**attempt)
                    time.sleep(delay)

        # Mock function that fails twice then succeeds
        call_count = 0

        def mock_api_call():
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                raise RateLimitError("Rate limited", 429, f"req-{call_count}")
            return {"data": "success"}

        # Test successful retry
        result = retry_with_backoff(mock_api_call)
        self.assertEqual(result, {"data": "success"})
        self.assertEqual(call_count, 3)

        # Verify sleep was called with exponential backoff
        expected_sleeps = [1, 2]  # base_delay * (2 ** attempt) for attempts 0, 1
        actual_sleeps = [call.args[0] for call in mock_sleep.call_args_list]
        self.assertEqual(actual_sleeps, expected_sleeps)

    @patch("time.sleep")
    def test_rate_limit_retry_max_attempts(self, mock_sleep):
        """Test that retry logic respects max attempts."""

        def retry_with_backoff(func, max_retries=2, base_delay=1):
            """Retry logic that should fail after max_retries."""
            for attempt in range(max_retries):
                try:
                    return func()
                except RateLimitError:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(base_delay * (2**attempt))

        # Mock function that always fails
        def always_fails():
            raise RateLimitError("Always rate limited", 429, "always-fails")

        # Should raise after max attempts
        with self.assertRaises(RateLimitError):
            retry_with_backoff(always_fails, max_retries=2)

        # Should have slept only once (for the first retry)
        self.assertEqual(len(mock_sleep.call_args_list), 1)
        self.assertEqual(mock_sleep.call_args_list[0].args[0], 1)  # base_delay * 2^0

    @patch("requests.request")
    def test_session_tenant_list_rate_limiting(self, mock_request):
        """Test rate limiting with actual session tenant operations."""
        # Mock a 429 response for tenant list
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 429
        mock_response.json.return_value = {
            "Message": "API rate limit exceeded. Please reduce request frequency."
        }
        mock_response.text = (
            '{"Message": "API rate limit exceeded. Please reduce request frequency."}'
        )
        mock_response.headers = {"x-request-id": "tenant-rate-limit-123"}
        mock_request.return_value = mock_response

        # Test rate limiting on actual session operation
        with self.assertRaises(RateLimitError) as context:
            self.session.tenant.list_tenants()

        error = context.exception
        self.assertEqual(error.status_code, 429)
        self.assertEqual(error.request_id, "tenant-rate-limit-123")
        self.assertIn("API rate limit exceeded", str(error))

    @patch("requests.request")
    def test_session_assessment_list_rate_limiting(self, mock_request):
        """Test rate limiting with assessment operations."""
        # Mock a 429 response for assessment list
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 429
        mock_response.json.return_value = {
            "Message": "Rate limit exceeded: 2 RPS limit"
        }
        mock_response.text = '{"Message": "Rate limit exceeded: 2 RPS limit"}'
        mock_response.headers = {"x-request-id": "assessment-rate-limit-456"}
        mock_request.return_value = mock_response

        with self.assertRaises(RateLimitError) as context:
            self.session.assessment.list_assessments(
                tenant_id="test-tenant", status="PENDING"
            )

        error = context.exception
        self.assertEqual(error.status_code, 429)
        self.assertEqual(error.request_id, "assessment-rate-limit-456")
        self.assertIn("2 RPS limit", str(error))

    def test_rate_limit_error_message_formatting(self):
        """Test that RateLimitError formats messages correctly."""
        # Test with all parameters
        error = RateLimitError("Custom rate limit message", 429, "req-123")
        expected = "Custom rate limit message (Status: 429, RequestId: req-123)"
        self.assertEqual(str(error), expected)

        # Test without request ID
        error = RateLimitError("No request ID", 429, None)
        expected = "No request ID (Status: 429, RequestId: None)"
        self.assertEqual(str(error), expected)

        # Test with default status code
        error = RateLimitError("Default status", request_id="req-456")
        expected = "Default status (Status: 429, RequestId: req-456)"
        self.assertEqual(str(error), expected)


class TestRateLimitIntegration(unittest.TestCase):
    """Integration tests for rate limiting with real-world scenarios."""

    def setUp(self):
        """Set up integration test fixtures."""
        self.session = Session(
            api_key="test-integration-key", api_secret_key="test-integration-secret"
        )

    def test_rate_limit_monitor_simulation(self):
        """Test a rate limit monitoring simulation."""

        class RateLimitMonitor:
            """Simple rate limit monitor for testing."""

            def __init__(self):
                self.requests_made = 0
                self.rate_limited_count = 0

            def make_request(self, func, *args, **kwargs):
                """Simulate making a request with monitoring."""
                self.requests_made += 1
                try:
                    return func(*args, **kwargs)
                except RateLimitError:
                    self.rate_limited_count += 1
                    raise

        monitor = RateLimitMonitor()

        # Simulate a function that gets rate limited
        def simulate_api_call():
            if monitor.requests_made > 2:  # Rate limit after 2 requests
                raise RateLimitError(
                    "Simulated rate limit", 429, f"req-{monitor.requests_made}"
                )
            return {"success": True}

        # Make successful requests
        result1 = monitor.make_request(simulate_api_call)
        result2 = monitor.make_request(simulate_api_call)

        self.assertEqual(result1, {"success": True})
        self.assertEqual(result2, {"success": True})
        self.assertEqual(monitor.requests_made, 2)
        self.assertEqual(monitor.rate_limited_count, 0)

        # This should get rate limited
        with self.assertRaises(RateLimitError):
            monitor.make_request(simulate_api_call)

        self.assertEqual(monitor.requests_made, 3)
        self.assertEqual(monitor.rate_limited_count, 1)

    @patch("time.sleep")
    def test_rate_limit_handler_with_jitter(self, mock_sleep):
        """Test rate limiting with jitter in retry delays."""
        import random

        # Mock random to make test predictable
        with patch("random.random", return_value=0.5):

            def calculate_delay_with_jitter(attempt, base_delay=1, max_delay=60):
                """Calculate delay with jitter."""
                delay = min(base_delay * (2**attempt), max_delay)
                jitter = delay * 0.1 * random.random()  # Will be 0.5 from mock
                return delay + jitter

            # Test delay calculation
            delay_0 = calculate_delay_with_jitter(0)  # 1 + (1 * 0.1 * 0.5) = 1.05
            delay_1 = calculate_delay_with_jitter(1)  # 2 + (2 * 0.1 * 0.5) = 2.1
            delay_2 = calculate_delay_with_jitter(2)  # 4 + (4 * 0.1 * 0.5) = 4.2

            self.assertAlmostEqual(delay_0, 1.05, places=2)
            self.assertAlmostEqual(delay_1, 2.1, places=2)
            self.assertAlmostEqual(delay_2, 4.2, places=2)


if __name__ == "__main__":
    unittest.main()
