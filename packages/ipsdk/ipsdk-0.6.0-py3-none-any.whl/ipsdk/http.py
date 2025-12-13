# Copyright (c) 2025 Itential, Inc
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""HTTP utilities and enumerations for the Itential Python SDK.

This module provides HTTP-related enumerations with compatibility across
Python versions. HTTPStatus and HTTPMethod are re-exported or defined
to ensure consistent behavior across all supported Python versions.
"""

from http import HTTPStatus
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import httpx

from . import logging

# Import HTTPMethod from standard library (Python 3.11+) or define fallback
try:
    from http import HTTPMethod
except ImportError:
    # Python < 3.11: Define HTTPMethod enum for backward compatibility
    from enum import Enum

    class HTTPMethod(Enum):
        """Enumeration of HTTP methods.

        Includes all standard HTTP methods defined in RFC specifications.
        This is a compatibility implementation for Python < 3.11.
        Python 3.11+ uses http.HTTPMethod from the standard library.

        Attributes:
            GET: GET method - Retrieve a resource
            POST: POST method - Create a resource or submit data
            PUT: PUT method - Update/replace a resource
            DELETE: DELETE method - Delete a resource
            PATCH: PATCH method - Partially update a resource
            HEAD: HEAD method - Retrieve headers only
            OPTIONS: OPTIONS method - Get communication options
            TRACE: TRACE method - Echo the received request
            CONNECT: CONNECT method - Establish a tunnel to the server
        """

        GET = "GET"
        POST = "POST"
        PUT = "PUT"
        DELETE = "DELETE"
        PATCH = "PATCH"
        HEAD = "HEAD"
        OPTIONS = "OPTIONS"
        TRACE = "TRACE"
        CONNECT = "CONNECT"


class Request:
    """
    Wrapper class for HTTP requests that provides a clean interface for request data

    The Request class encapsulates all the information needed to make an HTTP request,
    including the method, path, parameters, headers, and body data. This provides a
    consistent interface for working with requests across the SDK.

    Args:
        method (str): The HTTP method (GET, POST, PUT, DELETE, PATCH)
        path (str): The URL path for the request
        params (Dict[str, Any], optional): Query parameters for the request
        headers (Dict[str, str], optional): HTTP headers for the request
        json (Union[str, bytes, dict, list], optional): JSON data for the request body

    Raises:
        ValueError: If required parameters are missing or invalid
    """

    def __init__(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Union[str, bytes, dict, list]] = None,
    ) -> None:
        logging.trace(self.__init__, modname=__name__, clsname=self.__class__)
        self.method = method
        self.path = path
        self.params = params or {}
        self.headers = headers or {}
        self.json = json

    @property
    def url(self) -> str:
        """
        Get the full URL for this request

        Returns:
            str: The complete URL including path and query parameters
        """
        return self.path

    def __repr__(self) -> str:
        """
        String representation of the request

        Returns:
            str: A string representation of the request
        """
        logging.trace(self.__repr__, modname=__name__, clsname=self.__class__)
        return f"Request(method='{self.method}', path='{self.path}')"


class Response:
    """
    Wrapper class for HTTP responses that provides enhanced functionality over
    httpx.Response

    The Response class wraps an httpx.Response object and provides additional
    convenience methods and properties for working with API responses. It maintains
    compatibility with the underlying httpx.Response while adding SDK-specific
    functionality.

    Args:
        httpx_response (httpx.Response): The underlying httpx response object

    Raises:
        ValueError: If the httpx_response is None or invalid
    """

    def __init__(self, httpx_response: httpx.Response) -> None:
        logging.trace(self.__init__, modname=__name__, clsname=self.__class__)
        if httpx_response is None:
            msg = "httpx_response cannot be None"
            raise ValueError(msg)

        self._response = httpx_response

    @property
    def status_code(self) -> int:
        """
        Get the HTTP status code

        Returns:
            int: The HTTP status code
        """
        return self._response.status_code

    @property
    def headers(self) -> httpx.Headers:
        """
        Get the response headers

        Returns:
            httpx.Headers: The response headers
        """
        return self._response.headers

    @property
    def content(self) -> bytes:
        """
        Get the raw response content as bytes

        Returns:
            bytes: The raw response content
        """
        return self._response.content

    @property
    def text(self) -> str:
        """
        Get the response content as text

        Returns:
            str: The response content decoded as text
        """
        return self._response.text

    @property
    def url(self) -> httpx.URL:
        """
        Get the request URL

        Returns:
            httpx.URL: The URL that was requested
        """
        return self._response.url

    @property
    def request(self) -> httpx.Request:
        """
        Get the original request object

        Returns:
            httpx.Request: The original request that generated this response
        """
        return self._response.request

    def json(self) -> Dict[str, Any]:
        """
        Parse the response content as JSON

        Returns:
            Dict[str, Any]: The parsed JSON response

        Raises:
            ValueError: If the response content is not valid JSON
        """
        logging.trace(self.json, modname=__name__, clsname=self.__class__)
        try:
            return self._response.json()
        except Exception as exc:
            msg = f"Failed to parse response as JSON: {exc!s}"
            raise ValueError(msg)

    def raise_for_status(self) -> None:
        """
        Raise an exception if the response status indicates an error

        Raises:
            httpx.HTTPStatusError: If the response status code indicates an error
        """
        logging.trace(self.raise_for_status, modname=__name__, clsname=self.__class__)
        self._response.raise_for_status()

    def is_success(self) -> bool:
        """
        Check if the response indicates success (2xx status code)

        Returns:
            bool: True if the status code is in the 2xx range, False otherwise
        """
        logging.trace(self.is_success, modname=__name__, clsname=self.__class__)
        return (
            HTTPStatus.OK.value <= self.status_code < HTTPStatus.MULTIPLE_CHOICES.value
        )

    def is_error(self) -> bool:
        """
        Check if the response indicates an error (4xx or 5xx status code)

        Returns:
            bool: True if the status code indicates an error, False otherwise
        """
        logging.trace(self.is_error, modname=__name__, clsname=self.__class__)
        return self.status_code >= HTTPStatus.BAD_REQUEST.value

    def __repr__(self) -> str:
        """
        String representation of the response

        Returns:
            str: A string representation of the response
        """
        logging.trace(self.__repr__, modname=__name__, clsname=self.__class__)
        return f"Response(status_code={self.status_code}, url='{self.url}')"
