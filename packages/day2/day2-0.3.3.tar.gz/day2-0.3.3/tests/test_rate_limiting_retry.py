"""Tests for automatic rate limiting retry functionality."""

import unittest
from unittest.mock import Mock, call, patch

import requests

from day2 import Session
from day2.client.base import BaseClient
from day2.client.config import Config
from day2.exceptions import RateLimitError, ServerError


class TestRateLimitRetry(unittest.TestCase):
    """Test automatic retry on rate limiting."""

    def setUp(self):
        """Set up test fixtures."""
        # Configure with specific retry settings for testing
        self.config = Config(
            base_url="https://api.example.com",
            max_retries=3,
            retry_backoff_factor=1.0,
            retry_min_delay=0.1,  # Short delays for testing
            retry_max_delay=1.0,
        )
        self.session = Session(
            api_key="test-key", api_secret_key="test-secret", config=self.config
        )
        self.client = BaseClient(self.session, "test-service")

    @patch("time.sleep")  # Mock sleep to speed up tests
    @patch("requests.request")
    def test_retry_on_rate_limit_success(self, mock_request, mock_sleep):
        """Test that SDK retries on rate limit and eventually succeeds."""
        # First two calls return 429, third succeeds
        mock_responses = []

        # First attempt: rate limited
        response1 = Mock(spec=requests.Response)
        response1.status_code = 429
        response1.json.return_value = {"Message": "Rate limited"}
        response1.text = '{"Message": "Rate limited"}'
        response1.headers = {"x-request-id": "req-1"}
        mock_responses.append(response1)

        # Second attempt: still rate limited
        response2 = Mock(spec=requests.Response)
        response2.status_code = 429
        response2.json.return_value = {"Message": "Rate limited"}
        response2.text = '{"Message": "Rate limited"}'
        response2.headers = {"x-request-id": "req-2"}
        mock_responses.append(response2)

        # Third attempt: success
        response3 = Mock(spec=requests.Response)
        response3.status_code = 200
        response3.json.return_value = {"data": "success"}
        response3.text = '{"data": "success"}'
        response3.headers = {"x-request-id": "req-3"}
        mock_responses.append(response3)

        mock_request.side_effect = mock_responses

        # Should succeed after retries
        result = self.client._make_request("GET", "test-endpoint")

        # Verify success
        self.assertEqual(result, {"data": "success"})

        # Verify it made 3 attempts
        self.assertEqual(mock_request.call_count, 3)

        # Verify sleep was called between retries (2 times)
        self.assertEqual(mock_sleep.call_count, 2)

    @patch("time.sleep")
    @patch("requests.request")
    def test_retry_on_rate_limit_all_fail(self, mock_request, mock_sleep):
        """Test that SDK raises RateLimitError after all retries fail."""
        # All attempts return 429
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 429
        mock_response.json.return_value = {"Message": "Persistent rate limit"}
        mock_response.text = '{"Message": "Persistent rate limit"}'
        mock_response.headers = {"x-request-id": "rate-limit-persistent"}

        mock_request.return_value = mock_response

        # Should raise RateLimitError after exhausting retries
        with self.assertRaises(RateLimitError) as context:
            self.client._make_request("GET", "test-endpoint")

        error = context.exception
        self.assertEqual(error.status_code, 429)
        self.assertIn("Persistent rate limit", str(error))

        # Verify it made max_retries attempts
        self.assertEqual(mock_request.call_count, 3)

        # Verify sleep was called between each retry
        self.assertEqual(mock_sleep.call_count, 2)

    @patch("time.sleep")
    @patch("requests.request")
    def test_retry_on_server_error(self, mock_request, mock_sleep):
        """Test that SDK also retries on server errors."""
        # First attempt: server error, second: success
        response1 = Mock(spec=requests.Response)
        response1.status_code = 500
        response1.json.return_value = {"Message": "Internal server error"}
        response1.text = '{"Message": "Internal server error"}'
        response1.headers = {"x-request-id": "req-500"}

        response2 = Mock(spec=requests.Response)
        response2.status_code = 200
        response2.json.return_value = {"data": "success"}
        response2.text = '{"data": "success"}'
        response2.headers = {"x-request-id": "req-200"}

        mock_request.side_effect = [response1, response2]

        # Should succeed after retry
        result = self.client._make_request("GET", "test-endpoint")

        self.assertEqual(result, {"data": "success"})
        self.assertEqual(mock_request.call_count, 2)
        self.assertEqual(mock_sleep.call_count, 1)

    @patch("time.sleep")
    @patch("requests.request")
    def test_no_retry_on_client_errors(self, mock_request, mock_sleep):
        """Test that SDK does not retry on other client errors (400, 401, etc)."""
        # Return a 400 Bad Request
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 400
        mock_response.json.return_value = {"Message": "Bad request"}
        mock_response.text = '{"Message": "Bad request"}'
        mock_response.headers = {"x-request-id": "req-400"}

        mock_request.return_value = mock_response

        # Should raise immediately without retrying
        from day2.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            self.client._make_request("GET", "test-endpoint")

        # Should only make one attempt (no retries)
        self.assertEqual(mock_request.call_count, 1)

        # Should not sleep since no retries
        self.assertEqual(mock_sleep.call_count, 0)

    @patch("time.sleep")
    @patch("requests.request")
    def test_no_retry_when_disabled(self, mock_request, mock_sleep):
        """Test that retries can be disabled via config."""
        # Create client with retries disabled
        config = Config(base_url="https://api.example.com", max_retries=0)
        session = Session(
            api_key="test-key", api_secret_key="test-secret", config=config
        )
        client = BaseClient(session, "test-service")

        # Return rate limit error
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 429
        mock_response.json.return_value = {"Message": "Rate limited"}
        mock_response.text = '{"Message": "Rate limited"}'
        mock_response.headers = {"x-request-id": "req-429"}

        mock_request.return_value = mock_response

        # Should raise immediately without retrying
        with self.assertRaises(RateLimitError):
            client._make_request("GET", "test-endpoint")

        # Should only make one attempt
        self.assertEqual(mock_request.call_count, 1)

        # Should not sleep
        self.assertEqual(mock_sleep.call_count, 0)

    @patch("time.sleep")
    @patch("requests.request")
    def test_mixed_errors_retry_pattern(self, mock_request, mock_sleep):
        """Test retry with mixed rate limit and server errors."""
        # Pattern: 429 -> 500 -> 429 -> 200
        responses = [
            self._create_response(429, "Rate limited"),
            self._create_response(500, "Server error"),
            self._create_response(429, "Rate limited again"),
            self._create_response(200, {"data": "finally success"}),
        ]

        mock_request.side_effect = responses

        # Create client with more retries
        config = Config(
            base_url="https://api.example.com",
            max_retries=4,
            retry_min_delay=0.1,
            retry_max_delay=1.0,
        )
        session = Session(
            api_key="test-key", api_secret_key="test-secret", config=config
        )
        client = BaseClient(session, "test-service")

        # Should eventually succeed
        result = client._make_request("GET", "test-endpoint")

        self.assertEqual(result, {"data": "finally success"})
        self.assertEqual(mock_request.call_count, 4)
        self.assertEqual(mock_sleep.call_count, 3)

    def _create_response(self, status_code, data):
        """Helper to create mock response."""
        response = Mock(spec=requests.Response)
        response.status_code = status_code

        if isinstance(data, str):
            response.json.return_value = {"Message": data}
            response.text = f'{{"Message": "{data}"}}'
        else:
            response.json.return_value = data
            response.text = str(data)

        response.headers = {"x-request-id": f"req-{status_code}"}
        return response


class TestRetryIntegration(unittest.TestCase):
    """Integration tests for retry logic with session operations."""

    @patch("time.sleep")
    @patch("requests.request")
    def test_session_tenant_list_with_retry(self, mock_request, mock_sleep):
        """Test that session operations retry on rate limits."""
        # First attempt rate limited, second succeeds
        responses = [
            self._create_response(429, "Rate limited"),
            self._create_response(
                200,
                {
                    "Tenants": [
                        {"Id": "tenant-1", "Name": "Tenant One"},
                        {"Id": "tenant-2", "Name": "Tenant Two"},
                    ]
                },
            ),
        ]

        mock_request.side_effect = responses

        session = Session(api_key="test-key", api_secret_key="test-secret")

        # Should succeed after retry
        tenants = session.tenant.list_tenants()

        self.assertEqual(len(tenants.tenants), 2)
        self.assertEqual(mock_request.call_count, 2)

    def _create_response(self, status_code, data):
        """Helper to create mock response."""
        response = Mock(spec=requests.Response)
        response.status_code = status_code

        if isinstance(data, str):
            response.json.return_value = {"Message": data}
            response.text = f'{{"Message": "{data}"}}'
        else:
            response.json.return_value = data
            response.text = str(data).replace("'", '"')

        response.headers = {"x-request-id": f"req-{status_code}"}
        return response


if __name__ == "__main__":
    unittest.main()
