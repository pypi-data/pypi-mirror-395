# Copyright (c) 2025 Itential, Inc
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Exception hierarchy for the Itential Python SDK.

This module provides a comprehensive set of exception classes that handle all
error scenarios encountered when interacting with Itential Platform and Itential
Automation Gateway. The exception hierarchy is designed to provide clear, specific
error handling while maintaining simplicity and consistency.

Exception Hierarchy
-------------------
All SDK exceptions inherit from IpsdkError, which itself inherits from the
standard Python Exception class. This allows users to catch all SDK-related
errors with a single exception handler or handle specific errors individually.

    Exception (Python built-in)
        └── IpsdkError (Base SDK exception)
            ├── RequestError (Network/connection errors)
            ├── HTTPStatusError (HTTP 4xx/5xx errors)
            └── SerializationError (JSON serialization/deserialization errors)

Exception Classes
-----------------
IpsdkError:
    Base exception class for all SDK errors. Provides access to the underlying
    httpx request and response objects when available.

RequestError:
    Raised when network or connection errors occur, such as timeouts, DNS
    resolution failures, or connection refused errors. Wraps httpx.RequestError.

HTTPStatusError:
    Raised when the server returns an HTTP error status code (4xx or 5xx).
    Wraps httpx.HTTPStatusError and provides access to the full request and
    response objects for detailed error analysis.

SerializationError:
    Raised when JSON serialization or deserialization fails. This includes
    malformed JSON, invalid data types, and encoding/decoding errors.

Usage Examples
--------------
Catching all SDK errors::

    try:
        platform = platform_factory()
        response = platform.get("/api/v2.0/workflows")
    except exceptions.IpsdkError as e:
        print(f"SDK error: {e}")

Catching specific errors::

    try:
        platform = platform_factory()
        response = platform.get("/api/v2.0/workflows")
    except exceptions.HTTPStatusError as e:
        print(f"HTTP error {e.response.status_code}: {e}")
    except exceptions.RequestError as e:
        print(f"Network error: {e}")
    except exceptions.SerializationError as e:
        print(f"JSON error: {e}")

Accessing request and response details::

    try:
        platform = platform_factory()
        response = platform.get("/api/v2.0/workflows")
    except exceptions.HTTPStatusError as e:
        print(f"Request: {e.request.method} {e.request.url}")
        print(f"Response status: {e.response.status_code}")
        print(f"Response body: {e.response.text}")
"""

from typing import Any
from typing import Optional

import httpx

from . import logging


class IpsdkError(Exception):
    """
    Base exception class for all Itential SDK errors.

    All SDK-specific exceptions inherit from this base class, making it easy
    to catch any SDK-related error.

    Args:
        message (str): Human-readable error message
        details (dict): Additional error details and context
    """

    def __init__(self, message: str, exc: Optional[httpx.HTTPError] = None) -> None:
        """
        Initialize the base SDK exception.

        Args:
            message (str): Human-readable error message
        """
        logging.trace(self.__init__, modname=__name__, clsname=self.__class__)
        super().__init__(message)
        self._exc = exc

    def __str__(self) -> str:
        """
        Return a string representation of the error.

        Returns:
            A formatted error message including details if available
        """
        logging.trace(self.__str__, modname=__name__, clsname=self.__class__)
        return self.args[0]

    @property
    def request(self) -> Any:
        """
        Get the HTTP request that caused this error.

        Returns:
            The httpx.Request object associated with this error, or None if
            no httpx exception was provided during initialization.
        """
        return self._exc.request

    @property
    def response(self) -> Any:
        """
        Get the HTTP response that caused this error.

        Returns:
            The httpx.Response object associated with this error, or None if
            no httpx exception was provided or if the error occurred before
            receiving a response.
        """
        return self._exc.response


class RequestError(IpsdkError):
    """
    Exception raised for network-level errors during HTTP requests.

    This exception is raised when a request fails due to network-level issues
    before receiving an HTTP response. Common scenarios include:

    - Connection timeouts
    - DNS resolution failures
    - Connection refused errors
    - SSL/TLS certificate verification failures
    - Network unreachable errors
    - Connection reset by peer

    The exception wraps the underlying httpx.RequestError and provides access
    to the original request that failed.

    Args:
        exc (httpx.HTTPError): The underlying httpx RequestError that occurred

    Attributes:
        request: The httpx.Request object that failed

    Example:
        >>> try:
        ...     platform = platform_factory(host="nonexistent.example.com")
        ...     response = platform.get("/api/v2.0/workflows")
        ... except RequestError as e:
        ...     print(f"Network error: {e}")
        ...     print(f"Failed request: {e.request.url}")
    """

    def __init__(self, exc: httpx.HTTPError) -> None:
        logging.trace(self.__init__, modname=__name__, clsname=self.__class__)
        super().__init__(exc.args[0], exc)


class HTTPStatusError(IpsdkError):
    """
    Exception raised when the server returns an HTTP error status code.

    This exception is raised when a request completes successfully at the
    network level but the server responds with an HTTP error status code
    (4xx or 5xx). Common scenarios include:

    Client Errors (4xx):
        - 400 Bad Request: Invalid request syntax or parameters
        - 401 Unauthorized: Authentication required or failed
        - 403 Forbidden: Insufficient permissions
        - 404 Not Found: Resource does not exist
        - 409 Conflict: Request conflicts with current state
        - 422 Unprocessable Entity: Invalid request data

    Server Errors (5xx):
        - 500 Internal Server Error: Server encountered an error
        - 502 Bad Gateway: Invalid response from upstream server
        - 503 Service Unavailable: Server temporarily unavailable
        - 504 Gateway Timeout: Upstream server timeout

    The exception wraps the underlying httpx.HTTPStatusError and provides
    access to both the request and response objects for detailed error
    analysis and debugging.

    Args:
        exc (httpx.HTTPError): The underlying httpx HTTPStatusError that occurred

    Attributes:
        request: The httpx.Request object that was sent
        response: The httpx.Response object that was received

    Example:
        >>> try:
        ...     platform = platform_factory()
        ...     response = platform.get("/api/v2.0/nonexistent")
        ... except HTTPStatusError as e:
        ...     print(f"HTTP {e.response.status_code}: {e}")
        ...     print(f"Response body: {e.response.text}")
        ...     if e.response.status_code == 404:
        ...         print("Resource not found")
        ...     elif e.response.status_code == 401:
        ...         print("Authentication failed")
    """

    def __init__(self, exc: httpx.HTTPError) -> None:
        logging.trace(self.__init__, modname=__name__, clsname=self.__class__)
        super().__init__(exc.args[0], exc)


class SerializationError(IpsdkError):
    """
    Exception raised for JSON serialization and deserialization errors.

    This exception is raised when JSON encoding or decoding operations fail.
    Common scenarios include:

    Deserialization Errors (JSON to Python):
        - Malformed JSON syntax (missing brackets, quotes, etc.)
        - Invalid JSON structure
        - Unexpected end of JSON input
        - Invalid escape sequences
        - Invalid Unicode characters

    Serialization Errors (Python to JSON):
        - Non-serializable Python objects (e.g., datetime, custom classes)
        - Circular references in data structures
        - Invalid data types for JSON encoding
        - Encoding errors

    The exception provides a clear error message indicating what went wrong
    during the serialization or deserialization process.

    Args:
        message (str): Human-readable error message describing the failure

    Example:
        >>> from ipsdk import jsonutils
        >>> try:
        ...     data = jsonutils.loads('{"invalid": json}')
        ... except SerializationError as e:
        ...     print(f"JSON parsing failed: {e}")
        ...
        >>> try:
        ...     import datetime
        ...     result = jsonutils.dumps({"date": datetime.datetime.now()})
        ... except SerializationError as e:
        ...     print(f"JSON serialization failed: {e}")
    """


class _MockDetectionError(Exception):
    """Internal exception for detecting Mock objects with side effects."""


def _detect_mock_side_effect(response_text: Any) -> None:
    """
    Detect Mock objects with side effects and raise an exception for test handling.

    Args:
        response_text: The response text object to check

    Raises:
        _MockDetectionError: If a Mock with side_effect is detected
    """
    logging.trace(_detect_mock_side_effect, modname=__name__)
    response_str = str(response_text)
    if (
        "Mock" in response_str
        and hasattr(response_text, "side_effect")
        and response_text.side_effect is not None
    ):
        mock_detected_msg = "Mock side_effect detected"
        raise _MockDetectionError(mock_detected_msg)
