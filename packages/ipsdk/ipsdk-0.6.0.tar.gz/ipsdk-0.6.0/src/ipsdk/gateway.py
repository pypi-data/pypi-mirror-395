# Copyright (c) 2025 Itential, Inc
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Itential Automation Gateway client implementation for the SDK.

This module provides client implementations for connecting to and interacting
with Itential Automation Gateway 4.x. It includes both synchronous and
asynchronous clients with basic username/password authentication.

Components
----------
The module exports the following components:

gateway_factory:
    Factory function that creates and configures Gateway or AsyncGateway
    instances based on the want_async parameter. This is the primary
    entry point for creating Gateway connections.

Gateway:
    Synchronous client for Itential Automation Gateway. Dynamically created
    by combining AuthMixin with Connection base class. Supports all standard
    HTTP methods (GET, POST, PUT, PATCH, DELETE) with automatic authentication.

AsyncGateway:
    Asynchronous client for Itential Automation Gateway. Dynamically created
    by combining AsyncAuthMixin with AsyncConnection base class. Provides
    async/await support for non-blocking API requests.

AuthMixin:
    Synchronous authentication mixin that implements basic username/password
    authentication for Gateway. Automatically authenticates on first request
    and handles authentication errors.

AsyncAuthMixin:
    Asynchronous authentication mixin that implements basic username/password
    authentication for Gateway with async/await support.

Authentication
--------------
Itential Automation Gateway uses basic authentication with username and password
credentials. The authentication flow works as follows:

1. Client is created with username and password via gateway_factory()
2. On first API request, authenticate() is called automatically
3. Credentials are sent to /login endpoint as JSON body
4. Authentication session is maintained for subsequent requests
5. Authentication errors are raised as HTTPStatusError or RequestError

Base URL
--------
The Gateway client automatically prepends "/api/v2.0" to all requests, so you
only need to provide the resource path when making API calls.

For example::

    gateway.get("/devices")  # Actual URL: https://host/api/v2.0/devices

Supported HTTP Methods
----------------------
All Gateway clients support the following HTTP methods:

- GET: Retrieve resources
- POST: Create resources or submit data
- PUT: Update/replace resources
- PATCH: Partially update resources
- DELETE: Delete resources

Error Handling
--------------
All Gateway operations may raise the following exceptions:

- RequestError: Network/connection errors (timeouts, connection refused,
  DNS failures)
- HTTPStatusError: HTTP error responses (401 Unauthorized, 404 Not Found,
  500 Internal Server Error, etc.)
- IpsdkError: General SDK errors (invalid parameters, missing credentials)

Examples
--------
Basic synchronous usage::

    from ipsdk import gateway_factory

    # Create Gateway client with default settings
    gateway = gateway_factory(
        host="gateway.example.com",
        user="admin@itential",
        password="password"
    )

    # Get all devices
    response = gateway.get("/devices")
    devices = response.json()

    # Get specific device
    response = gateway.get("/devices/device123")
    device = response.json()

    # Create a new resource
    response = gateway.post("/workflows", json={"name": "my-workflow"})
    workflow = response.json()

Asynchronous usage::

    from ipsdk import gateway_factory

    # Create async Gateway client
    gateway = gateway_factory(
        host="gateway.example.com",
        user="admin@itential",
        password="password",
        want_async=True
    )

    # Use async/await for requests
    async def get_devices():
        response = await gateway.get("/devices")
        return response.json()

Custom configuration::

    from ipsdk import gateway_factory

    # Create Gateway with custom settings
    gateway = gateway_factory(
        host="gateway.example.com",
        port=8443,
        use_tls=True,
        verify=True,
        user="admin@itential",
        password="password",
        timeout=60
    )

Error handling::

    from ipsdk import gateway_factory
    from ipsdk.exceptions import HTTPStatusError, RequestError

    gateway = gateway_factory(host="gateway.example.com")

    try:
        response = gateway.get("/devices")
        devices = response.json()
    except HTTPStatusError as e:
        print(f"HTTP error {e.response.status_code}: {e}")
    except RequestError as e:
        print(f"Network error: {e}")
"""

from typing import Any
from typing import Optional

import httpx

from . import connection
from . import exceptions
from . import logging


def _make_path() -> str:
    """
    Utility function that returns the login url

    Returns:
        A string that provides the login url
    """
    logging.trace(_make_path, modname=__name__)
    return "/login"


def _make_body(user: str, password: str) -> dict[str, str]:
    """
    Utility function to make the authentication body used to authenticate to
    the server

    Args:
        user (str): The username to use when authenticating
        password (str): The password to use when authenticating

    Returns:
        A dict object that can be used to send in the body of the
            authentication request
    """
    logging.trace(_make_body, modname=__name__)
    return {"username": user, "password": password}


def _make_headers() -> dict[str, str]:
    """
    Utility function that returns a dict object of headers

    Returns:
        A dict object that can be passed to a request to set the headers
    """
    logging.trace(_make_headers, modname=__name__)
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


class AuthMixin:
    """
    Authorization mixin for authenticating to Itential Automation Gateway
    """

    # Attributes that should be provided by ConnectionBase
    user: Optional[str]
    password: Optional[str]
    client: httpx.Client

    def authenticate(self) -> None:
        """
        Provides the authentication function for authenticating to the server
        """
        logging.trace(self.authenticate, modname=__name__, clsname=self.__class__)
        assert self.user is not None
        assert self.password is not None

        data = _make_body(self.user, self.password)
        headers = _make_headers()
        path = _make_path()

        try:
            res = self.client.post(path, headers=headers, json=data)
            res.raise_for_status()

        except httpx.HTTPStatusError as exc:
            logging.exception(exc)
            raise exceptions.HTTPStatusError(exc)

        except httpx.RequestError as exc:
            logging.exception(exc)
            raise exceptions.RequestError(exc)


class AsyncAuthMixin:
    """
    Async authorization mixin for authenticating to Itential Automation Gateway
    """

    # Attributes that should be provided by ConnectionBase
    user: Optional[str]
    password: Optional[str]
    client: httpx.AsyncClient

    async def authenticate(self) -> None:
        """
        Provides the authentication function for authenticating to the server
        """
        logging.trace(self.authenticate, modname=__name__, clsname=self.__class__)
        assert self.user is not None
        assert self.password is not None

        data = _make_body(self.user, self.password)
        headers = _make_headers()
        path = _make_path()

        try:
            res = await self.client.post(path, headers=headers, json=data)
            res.raise_for_status()

        except httpx.HTTPStatusError as exc:
            logging.exception(exc)
            raise exceptions.HTTPStatusError(exc)

        except httpx.RequestError as exc:
            logging.exception(exc)
            raise exceptions.RequestError(exc)


Gateway = type("Gateway", (AuthMixin, connection.Connection), {})
AsyncGateway = type("AsyncGateway", (AsyncAuthMixin, connection.AsyncConnection), {})

# Type aliases for mypy
GatewayType = Gateway
AsyncGatewayType = AsyncGateway


def gateway_factory(
    host: str = "localhost",
    port: int = 0,
    use_tls: bool = True,
    verify: bool = True,
    user: str = "admin@itential",
    password: str = "admin",
    timeout: int = 30,
    want_async: bool = False,
) -> Any:
    """Create a new instance of a Gateway connection.

    This factory function initializes a Gateway connection using provided parameters or
    environment variable overrides. Uses basic username/password authentication.

    Args:
        host (str): The target host for the connection. The default value for host
            is `localhost`

        port (int): Port number to use when connecting to the server.  The default
            value for port is `0`.  When the port value is set to 0, it will be
            automatically determined based  on the value of `use_tls`

        use_tls (bool): Whether to use TLS for the connection.  When this value is
            set to True, TLS will be enabled on the connection and when this value
            is set to False, TLS will be disabled.  The default value is True

        verify (bool): Whether to verify SSL certificates.  When this value is set
            to True, certificates will be verified when connecting to the server and
            when this value is set to False, certificate verification will be
            disabled.  The default value is True.

        user (str): The username to use when authenticating to the server.  The
            default value is `admin@itential`

        password (str): The password to use when authenticating to the server.  The
            default value is `admin`

        timeout (int): Timeout for the connection, in seconds.

        want_async (bool): When set to True, the factory function will return
            an async connection object and when set to False the factory will
            return a connection object.

    Returns:
        An initialized connection instance
    """
    logging.trace(gateway_factory, modname=__name__)

    factory = AsyncGateway if want_async is True else Gateway
    return factory(
        host=host,
        port=port,
        use_tls=use_tls,
        verify=verify,
        user=user,
        password=password,
        timeout=timeout,
        base_path="/api/v2.0",
    )
