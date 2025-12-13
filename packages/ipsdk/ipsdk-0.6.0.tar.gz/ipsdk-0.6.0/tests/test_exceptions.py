# Copyright (c) 2025 Itential, Inc
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Test suite for the refactored exception module.

This test suite validates the simplified exception hierarchy:
- IpsdkError: Base exception
- RequestError: Wraps httpx.RequestError
- HTTPStatusError: Wraps httpx.HTTPStatusError
- SerializationError: Data serialization/deserialization errors
"""

from unittest.mock import Mock

import httpx
import pytest

from ipsdk import exceptions


class TestIpsdkError:
    """Test cases for the base IpsdkError exception class."""

    def test_basic_initialization(self):
        """Test basic exception initialization with just a message."""
        exc = exceptions.IpsdkError("Test error message")
        assert str(exc) == "Test error message"
        assert exc.args[0] == "Test error message"

    def test_initialization_with_httpx_exception(self):
        """Test exception initialization with an httpx exception."""
        mock_request = Mock()
        mock_request.url = "https://example.com"
        mock_response = Mock()
        mock_response.status_code = 500

        httpx_exc = httpx.HTTPStatusError(
            "Server error", request=mock_request, response=mock_response
        )

        exc = exceptions.IpsdkError("Wrapped error", httpx_exc)
        assert str(exc) == "Wrapped error"
        assert exc.request == mock_request
        assert exc.response == mock_response

    def test_str_representation(self):
        """Test string representation of the exception."""
        exc = exceptions.IpsdkError("Simple error")
        assert str(exc) == "Simple error"

    def test_inheritance(self):
        """Test that IpsdkError inherits from Exception."""
        exc = exceptions.IpsdkError("Test")
        assert isinstance(exc, Exception)
        assert isinstance(exc, exceptions.IpsdkError)

    def test_request_property_without_exception(self):
        """Test request property when no httpx exception was provided."""
        exc = exceptions.IpsdkError("Test error")
        # Accessing request without an httpx exception will raise AttributeError
        with pytest.raises(AttributeError):
            _ = exc.request

    def test_response_property_without_exception(self):
        """Test response property when no httpx exception was provided."""
        exc = exceptions.IpsdkError("Test error")
        # Accessing response without an httpx exception will raise AttributeError
        with pytest.raises(AttributeError):
            _ = exc.response


class TestRequestError:
    """Test cases for RequestError exception."""

    def test_initialization_with_httpx_request_error(self):
        """Test RequestError wraps httpx.RequestError correctly."""
        mock_request = Mock()
        mock_request.url = "https://example.com"

        httpx_exc = httpx.RequestError("Connection failed", request=mock_request)
        exc = exceptions.RequestError(httpx_exc)

        assert isinstance(exc, exceptions.IpsdkError)
        assert isinstance(exc, exceptions.RequestError)
        assert str(exc) == "Connection failed"
        assert exc.request == mock_request

    def test_initialization_with_connect_error(self):
        """Test RequestError wraps httpx.ConnectError."""
        mock_request = Mock()
        mock_request.url = "https://example.com"

        httpx_exc = httpx.ConnectError("Connection refused", request=mock_request)
        exc = exceptions.RequestError(httpx_exc)

        assert isinstance(exc, exceptions.RequestError)
        assert "Connection refused" in str(exc)

    def test_initialization_with_timeout(self):
        """Test RequestError wraps httpx.TimeoutException."""
        mock_request = Mock()
        mock_request.url = "https://example.com"

        httpx_exc = httpx.TimeoutException("Request timeout", request=mock_request)
        exc = exceptions.RequestError(httpx_exc)

        assert isinstance(exc, exceptions.RequestError)
        assert "Request timeout" in str(exc)

    def test_inheritance_chain(self):
        """Test RequestError inheritance chain."""
        mock_request = Mock()
        httpx_exc = httpx.RequestError("Test", request=mock_request)
        exc = exceptions.RequestError(httpx_exc)

        assert isinstance(exc, Exception)
        assert isinstance(exc, exceptions.IpsdkError)
        assert isinstance(exc, exceptions.RequestError)


class TestHTTPStatusError:
    """Test cases for HTTPStatusError exception."""

    def test_initialization_with_httpx_status_error(self):
        """Test HTTPStatusError wraps httpx.HTTPStatusError correctly."""
        mock_request = Mock()
        mock_request.url = "https://example.com"
        mock_response = Mock()
        mock_response.status_code = 404

        httpx_exc = httpx.HTTPStatusError(
            "Not found", request=mock_request, response=mock_response
        )
        exc = exceptions.HTTPStatusError(httpx_exc)

        assert isinstance(exc, exceptions.IpsdkError)
        assert isinstance(exc, exceptions.HTTPStatusError)
        assert str(exc) == "Not found"
        assert exc.request == mock_request
        assert exc.response == mock_response

    def test_initialization_with_4xx_error(self):
        """Test HTTPStatusError with 4xx client error."""
        mock_request = Mock()
        mock_request.url = "https://example.com"
        mock_response = Mock()
        mock_response.status_code = 400

        httpx_exc = httpx.HTTPStatusError(
            "Bad request", request=mock_request, response=mock_response
        )
        exc = exceptions.HTTPStatusError(httpx_exc)

        assert isinstance(exc, exceptions.HTTPStatusError)
        assert "Bad request" in str(exc)
        assert exc.response.status_code == 400

    def test_initialization_with_5xx_error(self):
        """Test HTTPStatusError with 5xx server error."""
        mock_request = Mock()
        mock_request.url = "https://example.com"
        mock_response = Mock()
        mock_response.status_code = 500

        httpx_exc = httpx.HTTPStatusError(
            "Internal server error", request=mock_request, response=mock_response
        )
        exc = exceptions.HTTPStatusError(httpx_exc)

        assert isinstance(exc, exceptions.HTTPStatusError)
        assert "Internal server error" in str(exc)
        assert exc.response.status_code == 500

    def test_inheritance_chain(self):
        """Test HTTPStatusError inheritance chain."""
        mock_request = Mock()
        mock_response = Mock()
        mock_response.status_code = 403

        httpx_exc = httpx.HTTPStatusError(
            "Forbidden", request=mock_request, response=mock_response
        )
        exc = exceptions.HTTPStatusError(httpx_exc)

        assert isinstance(exc, Exception)
        assert isinstance(exc, exceptions.IpsdkError)
        assert isinstance(exc, exceptions.HTTPStatusError)


class TestSerializationError:
    """Test cases for SerializationError exception."""

    def test_basic_initialization(self):
        """Test basic SerializationError initialization."""
        exc = exceptions.SerializationError("Serialization failed")
        assert str(exc) == "Serialization failed"
        assert exc.args[0] == "Serialization failed"

    def test_json_parse_error_scenario(self):
        """Test SerializationError for JSON parsing errors."""
        exc = exceptions.SerializationError("Failed to parse JSON: invalid syntax")
        assert isinstance(exc, exceptions.IpsdkError)
        assert isinstance(exc, exceptions.SerializationError)
        assert "Failed to parse JSON" in str(exc)

    def test_json_dump_error_scenario(self):
        """Test SerializationError for JSON serialization errors."""
        exc = exceptions.SerializationError("Failed to serialize object to JSON")
        assert isinstance(exc, exceptions.SerializationError)
        assert "serialize" in str(exc)

    def test_inheritance_chain(self):
        """Test SerializationError inheritance chain."""
        exc = exceptions.SerializationError("Test error")

        assert isinstance(exc, Exception)
        assert isinstance(exc, exceptions.IpsdkError)
        assert isinstance(exc, exceptions.SerializationError)

    def test_can_be_caught_as_ipsdk_error(self):
        """Test that SerializationError can be caught as IpsdkError."""
        try:
            msg = "Test"
            raise exceptions.SerializationError(msg)
        except exceptions.IpsdkError as e:
            assert str(e) == "Test"


class TestInternalFunctions:
    """Test cases for internal helper functions."""

    def test_detect_mock_side_effect_with_mock(self):
        """Test _detect_mock_side_effect detects mocks with side effects."""
        mock_obj = Mock()
        mock_obj.side_effect = Exception("test")

        with pytest.raises(exceptions._MockDetectionError):
            exceptions._detect_mock_side_effect(mock_obj)

    def test_detect_mock_side_effect_with_mock_no_side_effect(self):
        """Test _detect_mock_side_effect ignores mocks without side effects."""
        mock_obj = Mock()
        mock_obj.side_effect = None

        # Should not raise an exception
        exceptions._detect_mock_side_effect(mock_obj)

    def test_detect_mock_side_effect_with_regular_string(self):
        """Test _detect_mock_side_effect with regular string."""
        regular_string = "This is just a regular string"

        # Should not raise an exception
        exceptions._detect_mock_side_effect(regular_string)

    def test_detect_mock_side_effect_with_mock_like_string(self):
        """Test _detect_mock_side_effect with string containing 'Mock'."""
        # String contains "Mock" but is not actually a Mock object
        mock_like_string = "This Mock string should not trigger"

        # Should not raise an exception
        exceptions._detect_mock_side_effect(mock_like_string)


class TestExceptionHierarchy:
    """Test cases for the overall exception hierarchy."""

    def test_all_exceptions_inherit_from_ipsdk_error(self):
        """Test that all custom exceptions inherit from IpsdkError."""
        mock_request = Mock()
        mock_response = Mock()
        mock_response.status_code = 500

        httpx_request_exc = httpx.RequestError("Test", request=mock_request)
        httpx_status_exc = httpx.HTTPStatusError(
            "Test", request=mock_request, response=mock_response
        )

        exception_instances = [
            exceptions.IpsdkError("Test"),
            exceptions.RequestError(httpx_request_exc),
            exceptions.HTTPStatusError(httpx_status_exc),
            exceptions.SerializationError("Test"),
        ]

        for exc_instance in exception_instances:
            assert isinstance(exc_instance, exceptions.IpsdkError)
            assert isinstance(exc_instance, Exception)

    def test_exception_hierarchy_allows_specific_catching(self):
        """Test that specific exception types can be caught individually."""
        mock_request = Mock()
        httpx_exc = httpx.RequestError("Connection error", request=mock_request)

        try:
            raise exceptions.RequestError(httpx_exc)
        except exceptions.RequestError as e:
            assert isinstance(e, exceptions.RequestError)
            assert isinstance(e, exceptions.IpsdkError)

    def test_exception_hierarchy_allows_general_catching(self):
        """Test that all exceptions can be caught with IpsdkError."""
        exceptions_to_test = []

        mock_request = Mock()
        mock_response = Mock()
        mock_response.status_code = 404

        httpx_request_exc = httpx.RequestError("Test", request=mock_request)
        httpx_status_exc = httpx.HTTPStatusError(
            "Test", request=mock_request, response=mock_response
        )

        exceptions_to_test.append(exceptions.RequestError(httpx_request_exc))
        exceptions_to_test.append(exceptions.HTTPStatusError(httpx_status_exc))
        exceptions_to_test.append(exceptions.SerializationError("Test"))

        for exc in exceptions_to_test:
            try:
                raise exc
            except exceptions.IpsdkError:
                pass  # Successfully caught as IpsdkError


class TestExceptionUsagePatterns:
    """Test common exception usage patterns."""

    def test_wrapping_httpx_exceptions(self):
        """Test that httpx exceptions are properly wrapped."""
        mock_request = Mock()
        mock_request.url = "https://api.example.com/test"

        # Wrap a request error
        httpx_exc = httpx.RequestError("Network failure", request=mock_request)
        sdk_exc = exceptions.RequestError(httpx_exc)

        assert "Network failure" in str(sdk_exc)
        assert sdk_exc.request == mock_request

    def test_raising_and_catching_serialization_errors(self):
        """Test raising and catching SerializationError."""
        try:
            msg = "Invalid JSON format"
            raise exceptions.SerializationError(msg)
        except exceptions.SerializationError as e:
            assert "Invalid JSON" in str(e)

    def test_exception_can_be_re_raised(self):
        """Test that exceptions can be caught and re-raised."""
        mock_request = Mock()
        httpx_exc = httpx.RequestError("Original error", request=mock_request)

        with pytest.raises(exceptions.RequestError):
            raise exceptions.RequestError(httpx_exc)


class TestExceptionEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_error_message(self):
        """Test exception with empty error message."""
        exc = exceptions.IpsdkError("")
        assert str(exc) == ""

    def test_very_long_error_message(self):
        """Test exception with very long error message."""
        long_message = "x" * 1000
        exc = exceptions.SerializationError(long_message)
        assert str(exc) == long_message
        assert len(str(exc)) == 1000

    def test_unicode_in_error_message(self):
        """Test exception with unicode characters in message."""
        unicode_message = "Error: 世界 🌍 café"
        exc = exceptions.IpsdkError(unicode_message)
        assert str(exc) == unicode_message

    def test_multiline_error_message(self):
        """Test exception with multiline error message."""
        multiline_message = "Error occurred:\nLine 1\nLine 2\nLine 3"
        exc = exceptions.SerializationError(multiline_message)
        assert str(exc) == multiline_message
        assert "\n" in str(exc)


class TestExceptionIntegration:
    """Integration tests for exception handling scenarios."""

    def test_httpx_request_error_to_sdk_request_error(self):
        """Test converting httpx.RequestError to RequestError."""
        mock_request = Mock()
        mock_request.url = "https://example.com/api"
        mock_request.method = "GET"

        # Simulate various httpx request errors
        error_types = [
            httpx.RequestError("Connection timeout", request=mock_request),
            httpx.ConnectError("Connection refused", request=mock_request),
            httpx.TimeoutException("Read timeout", request=mock_request),
        ]

        for httpx_err in error_types:
            sdk_err = exceptions.RequestError(httpx_err)
            assert isinstance(sdk_err, exceptions.RequestError)
            assert sdk_err.request == mock_request

    def test_httpx_status_error_to_sdk_status_error(self):
        """Test converting httpx.HTTPStatusError to HTTPStatusError."""
        mock_request = Mock()
        mock_request.url = "https://example.com/api"
        mock_response = Mock()

        # Test various HTTP status codes
        status_codes = [400, 401, 403, 404, 500, 502, 503]

        for status_code in status_codes:
            mock_response.status_code = status_code
            httpx_err = httpx.HTTPStatusError(
                f"HTTP {status_code}", request=mock_request, response=mock_response
            )

            sdk_err = exceptions.HTTPStatusError(httpx_err)
            assert isinstance(sdk_err, exceptions.HTTPStatusError)
            assert sdk_err.response.status_code == status_code

    def test_exception_message_preservation(self):
        """Test that exception messages are preserved through wrapping."""
        original_message = "Original error message with details"

        mock_request = Mock()
        httpx_exc = httpx.RequestError(original_message, request=mock_request)
        sdk_exc = exceptions.RequestError(httpx_exc)

        assert str(sdk_exc) == original_message


class TestBackwardCompatibility:
    """Tests to ensure the simplified structure maintains essential functionality."""

    def test_can_catch_all_sdk_errors_generically(self):
        """Test that all SDK errors can be caught with base exception."""
        mock_request = Mock()
        mock_response = Mock()
        mock_response.status_code = 500

        httpx_request_exc = httpx.RequestError("Test", request=mock_request)
        httpx_status_exc = httpx.HTTPStatusError(
            "Test", request=mock_request, response=mock_response
        )

        test_exceptions = [
            exceptions.IpsdkError("Generic error"),
            exceptions.RequestError(httpx_request_exc),
            exceptions.HTTPStatusError(httpx_status_exc),
            exceptions.SerializationError("JSON error"),
        ]

        caught_count = 0
        for exc in test_exceptions:
            try:
                raise exc
            except exceptions.IpsdkError:
                caught_count += 1

        assert caught_count == len(test_exceptions)

    def test_exception_properties_accessible(self):
        """Test that wrapped exceptions expose request/response properties."""
        mock_request = Mock()
        mock_request.url = "https://example.com"
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not found"

        httpx_exc = httpx.HTTPStatusError(
            "Not found", request=mock_request, response=mock_response
        )
        sdk_exc = exceptions.HTTPStatusError(httpx_exc)

        assert sdk_exc.request == mock_request
        assert sdk_exc.response == mock_response
        assert sdk_exc.response.status_code == 404
        assert sdk_exc.response.text == "Not found"
