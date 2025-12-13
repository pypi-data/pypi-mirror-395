# Copyright (c) 2025 Itential, Inc
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Itential Platform client implementation for the SDK.

This module provides client implementations for connecting to and interacting
with Itential Platform. It includes both synchronous and asynchronous clients
with support for OAuth (client credentials) and basic username/password
authentication.

Components
----------
The module exports the following components:

platform_factory:
    Factory function that creates and configures Platform or AsyncPlatform
    instances based on the want_async parameter. This is the primary
    entry point for creating Platform connections.

Platform:
    Synchronous client for Itential Platform. Dynamically created by
    combining AuthMixin with Connection base class. Supports all standard
    HTTP methods (GET, POST, PUT, PATCH, DELETE) with automatic authentication
    using either OAuth or basic auth.

AsyncPlatform:
    Asynchronous client for Itential Platform. Dynamically created by
    combining AsyncAuthMixin with AsyncConnection base class. Provides
    async/await support for non-blocking API requests with OAuth or basic auth.

AuthMixin:
    Synchronous authentication mixin that implements both OAuth client
    credentials and basic username/password authentication for Platform.
    Automatically selects the appropriate authentication method based on
    provided credentials.

AsyncAuthMixin:
    Asynchronous authentication mixin that implements both OAuth and basic
    authentication for Platform with async/await support.

Authentication
--------------
Itential Platform supports two authentication methods:

OAuth Client Credentials (Recommended):
    Uses client_id and client_secret to obtain an access token via the
    OAuth 2.0 client credentials flow. The token is included in subsequent
    requests as a Bearer token in the Authorization header.

    Flow:
    1. Client is created with client_id and client_secret
    2. On first API request, POST to /oauth/token with credentials
    3. Extract access_token from response
    4. Include token in Authorization header for all subsequent requests

Basic Authentication:
    Uses username and password credentials for authentication. Credentials
    are sent to the /login endpoint and a session is maintained for
    subsequent requests.

    Flow:
    1. Client is created with user and password
    2. On first API request, POST to /login with credentials
    3. Session is maintained via cookies for subsequent requests

The authentication method is automatically selected based on which credentials
are provided:
- If client_id and client_secret are provided, OAuth is used
- If user and password are provided, basic auth is used
- If neither pair is complete, IpsdkError is raised

Base URL
--------
The Platform client uses the host as the base URL without any additional
path prefix. All API paths should include the full resource path including
the API version.

For example::

    platform.get("/api/v2.0/workflows")  # Full path required

Supported HTTP Methods
----------------------
All Platform clients support the following HTTP methods:

- GET: Retrieve resources
- POST: Create resources or submit data
- PUT: Update/replace resources
- PATCH: Partially update resources
- DELETE: Delete resources

Error Handling
--------------
All Platform operations may raise the following exceptions:

- RequestError: Network/connection errors (timeouts, connection refused,
  DNS failures)
- HTTPStatusError: HTTP error responses (401 Unauthorized, 404 Not Found,
  500 Internal Server Error, etc.)
- IpsdkError: General SDK errors (invalid parameters, missing/incomplete
  credentials)

Examples
--------
OAuth authentication (recommended)::

    from ipsdk import platform_factory

    # Create Platform client with OAuth
    platform = platform_factory(
        host="platform.example.com",
        client_id="your-client-id",
        client_secret="your-client-secret"
    )

    # Get all workflows
    response = platform.get("/api/v2.0/workflows")
    workflows = response.json()

    # Create a new workflow
    response = platform.post(
        "/api/v2.0/workflows",
        json={"name": "my-workflow", "description": "Test workflow"}
    )
    workflow = response.json()

Basic authentication::

    from ipsdk import platform_factory

    # Create Platform client with basic auth
    platform = platform_factory(
        host="platform.example.com",
        user="admin",
        password="password"
    )

    # Make API requests
    response = platform.get("/api/v2.0/workflows")
    workflows = response.json()

Asynchronous usage::

    from ipsdk import platform_factory

    # Create async Platform client
    platform = platform_factory(
        host="platform.example.com",
        client_id="your-client-id",
        client_secret="your-client-secret",
        want_async=True
    )

    # Use async/await for requests
    async def get_workflows():
        response = await platform.get("/api/v2.0/workflows")
        return response.json()

    async def create_workflow(name):
        response = await platform.post(
            "/api/v2.0/workflows",
            json={"name": name}
        )
        return response.json()

Custom configuration::

    from ipsdk import platform_factory

    # Create Platform with custom settings
    platform = platform_factory(
        host="platform.example.com",
        port=8443,
        use_tls=True,
        verify=True,
        client_id="your-client-id",
        client_secret="your-client-secret",
        timeout=60
    )

Error handling::

    from ipsdk import platform_factory
    from ipsdk.exceptions import HTTPStatusError, RequestError, IpsdkError

    try:
        platform = platform_factory(
            host="platform.example.com",
            client_id="your-client-id",
            client_secret="your-client-secret"
        )
        response = platform.get("/api/v2.0/workflows")
        workflows = response.json()
    except HTTPStatusError as e:
        print(f"HTTP error {e.response.status_code}: {e}")
    except RequestError as e:
        print(f"Network error: {e}")
    except IpsdkError as e:
        print(f"SDK error: {e}")

Working with responses::

    from ipsdk import platform_factory

    platform = platform_factory(host="platform.example.com")

    # Get workflows with query parameters
    response = platform.get(
        "/api/v2.0/workflows",
        params={"limit": 10, "offset": 0}
    )

    # Check response status
    if response.is_success():
        workflows = response.json()
        print(f"Found {len(workflows)} workflows")
    else:
        print(f"Request failed with status {response.status_code}")
"""

from typing import Any
from typing import Optional

import httpx

from . import connection
from . import exceptions
from . import jsonutils
from . import logging


def _make_oauth_headers() -> dict[str, str]:
    """
    Create HTTP headers for OAuth token request.

    Returns the headers dict required for OAuth client credentials
    token requests. The Content-Type is set to application/x-www-form-urlencoded
    as required by the OAuth 2.0 specification.

    Args:
        None

    Returns:
        dict[str, str]: Headers dict with Content-Type for OAuth requests

    Raises:
        None
    """
    logging.trace(_make_oauth_headers, modname=__name__)
    return {"Content-Type": "application/x-www-form-urlencoded"}


def _make_oauth_path() -> str:
    """
    Get the URL path for OAuth token endpoint.

    Returns the API path used to request OAuth access tokens using
    client credentials grant type.

    Args:
        None

    Returns:
        str: The OAuth token endpoint path

    Raises:
        None
    """
    logging.trace(_make_oauth_path, modname=__name__)
    return "/oauth/token"


def _make_oauth_body(client_id: str, client_secret: str) -> dict[str, str]:
    """
    Create request body for OAuth client credentials authentication.

    Constructs the form data required for OAuth 2.0 client credentials
    grant type. The body includes grant_type, client_id, and client_secret
    which are sent as form-encoded data to the token endpoint.

    Args:
        client_id (str): OAuth client identifier
        client_secret (str): OAuth client secret

    Returns:
        dict[str, str]: Form data dict for OAuth token request

    Raises:
        None
    """
    logging.trace(_make_oauth_body, modname=__name__)
    return {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }


def _make_basicauth_body(user: str, password: str) -> dict[str, dict[str, str]]:
    """
    Create request body for basic username/password authentication.

    Constructs the JSON request body required for basic authentication
    to Platform. The body contains a nested user object with username
    and password fields.

    Args:
        user (str): Username for authentication
        password (str): Password for authentication

    Returns:
        dict[str, dict[str, str]]: JSON body dict for basic auth request

    Raises:
        None
    """
    logging.trace(_make_basicauth_body, modname=__name__)
    return {
        "user": {
            "username": user,
            "password": password,
        }
    }


def _make_basicauth_path() -> str:
    """
    Get the URL path for basic authentication endpoint.

    Returns the API path used for username/password authentication
    to Platform.

    Args:
        None

    Returns:
        str: The basic authentication endpoint path

    Raises:
        None
    """
    logging.trace(_make_basicauth_path, modname=__name__)
    return "/login"


class AuthMixin:
    """
    Authorization mixin for authenticating to Itential Platform.
    """

    # Attributes that should be provided by ConnectionBase
    user: Optional[str]
    password: Optional[str]
    client_id: Optional[str]
    client_secret: Optional[str]
    client: httpx.Client
    token: Optional[str]

    def authenticate(self) -> None:
        """
        Provides the authentication function for authenticating to the server
        """
        logging.trace(self.authenticate, modname=__name__, clsname=self.__class__)
        if self.client_id is not None and self.client_secret is not None:
            self.authenticate_oauth()
        elif self.user is not None and self.password is not None:
            self.authenticate_user()
        else:
            msg = (
                "No valid authentication credentials provided. "
                "Required: (client_id + client_secret) or (user + password)"
            )
            raise exceptions.IpsdkError(msg)

        logging.info("client connection successfully authenticated")

    def authenticate_user(self) -> None:
        """
        Performs authentication for basic authorization
        """
        logging.trace(self.authenticate_user, modname=__name__, clsname=self.__class__)
        logging.info("Attempting to perform basic authentication")

        assert self.user is not None
        assert self.password is not None
        data = _make_basicauth_body(self.user, self.password)
        path = _make_basicauth_path()

        try:
            res = self.client.post(path, json=data)
            res.raise_for_status()

        except httpx.HTTPStatusError as exc:
            logging.exception(exc)
            raise exceptions.HTTPStatusError(exc.message, exc)

        except httpx.RequestError as exc:
            logging.exception(exc.message, exc)
            raise exceptions.RequestError(exc.message, exc)

    def authenticate_oauth(self) -> None:
        """
        Performs authentication for OAuth client credentials
        """
        logging.trace(self.authenticate_oauth, modname=__name__, clsname=self.__class__)
        logging.info("Attempting to perform oauth authentication")

        assert self.client_id is not None
        assert self.client_secret is not None
        data = _make_oauth_body(self.client_id, self.client_secret)
        headers = _make_oauth_headers()
        path = _make_oauth_path()

        try:
            res = self.client.post(path, headers=headers, data=data)
            res.raise_for_status()

            # Parse the response to extract the token
            response_data = jsonutils.loads(res.text)
            if isinstance(response_data, dict):
                access_token = response_data.get("access_token")
            else:
                access_token = None

            self.token = access_token

        except httpx.HTTPStatusError as exc:
            logging.exception(exc)
            raise exceptions.HTTPStatusError(exc.message, exc)

        except httpx.RequestError as exc:
            logging.exception(exc.message, exc)
            raise exceptions.RequestError(exc.message, exc)


class AsyncAuthMixin:
    """
    Platform is a HTTP connection to Itential Platform
    """

    # Attributes that should be provided by ConnectionBase
    user: Optional[str]
    password: Optional[str]
    client_id: Optional[str]
    client_secret: Optional[str]
    client: httpx.AsyncClient
    token: Optional[str]

    async def authenticate(self) -> None:
        """
        Provides the authentication function for authenticating to the server
        """
        logging.trace(self.authenticate, modname=__name__, clsname=self.__class__)
        if self.client_id is not None and self.client_secret is not None:
            await self.authenticate_oauth()

        elif self.user is not None and self.password is not None:
            await self.authenticate_basicauth()

        else:
            msg = (
                "No valid authentication credentials provided. "
                "Required: (client_id + client_secret) or (user + password)"
            )
            raise exceptions.IpsdkError(msg)

        logging.info("client connection successfully authenticated")

    async def authenticate_basicauth(self) -> None:
        """
        Performs authentication for basic authorization
        """
        logging.trace(
            self.authenticate_basicauth, modname=__name__, clsname=self.__class__
        )
        logging.info("Attempting to perform basic authentication")

        assert self.user is not None
        assert self.password is not None
        data = _make_basicauth_body(self.user, self.password)
        path = _make_basicauth_path()

        try:
            res = await self.client.post(path, json=data)
            res.raise_for_status()

        except httpx.HTTPStatusError as exc:
            logging.exception(exc)
            raise exceptions.HTTPStatusError(exc.message, exc)

        except httpx.RequestError as exc:
            logging.exception(exc.message, exc)
            raise exceptions.RequestError(exc.message, exc)

    async def authenticate_oauth(self) -> None:
        """
        Performs authentication for OAuth client credentials
        """
        logging.trace(self.authenticate_oauth, modname=__name__, clsname=self.__class__)
        logging.info("Attempting to perform oauth authentication")

        assert self.client_id is not None
        assert self.client_secret is not None
        data = _make_oauth_body(self.client_id, self.client_secret)
        headers = _make_oauth_headers()
        path = _make_oauth_path()

        try:
            res = await self.client.post(path, headers=headers, data=data)
            res.raise_for_status()

        except httpx.HTTPStatusError as exc:
            logging.exception(exc)
            raise exceptions.HTTPStatusError(exc.message, exc)

        except httpx.RequestError as exc:
            logging.exception(exc.message, exc)
            raise exceptions.RequestError(exc.message, exc)


# Define type aliases for the dynamically created classes
Platform = type("Platform", (AuthMixin, connection.Connection), {})
AsyncPlatform = type("AsyncPlatform", (AsyncAuthMixin, connection.AsyncConnection), {})

# Type aliases for mypy
PlatformType = Platform
AsyncPlatformType = AsyncPlatform


def platform_factory(
    host: str = "localhost",
    port: int = 0,
    use_tls: bool = True,
    verify: bool = True,
    user: str = "admin",
    password: str = "admin",
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    timeout: int = 30,
    want_async: bool = False,
) -> Any:
    """
    Create a new instance of a Platform connection.

    This factory function initializes a Platform connection using provided parameters or
    environment variable overrides. Supports both user/password and client credentials.

    Args:
        host (str): The target host for the connection.  The default value for
            host is `localhost`

        port (int): Port number to connect to.   The default value for port
            is `0`.   When the value is set to `0`, the port will be automatically
            determined based on the value of `use_tls`

        use_tls (bool): Whether to use TLS for the connection.  When this argument
            is set to `True`, TLS will be enabled and when this value is set
            to `False`, TLS will be disabled  The default value is `True`

        verify (bool): Whether to verify SSL certificates.  When this value
            is set to `True`, the connection will attempt to verify the
            certificates and when this value is set to `False` Certificate
            verification will be disabled.  The default value is `True`

        user (str): The username to use when authenticating to the server.  The
            default value is `admin`

        password (str): The password to use when authenticating to the server.  The
            default value is `admin`

        client_id (str): Optional client ID for token-based authentication.  When
            this value is set, the client will attempt to use OAuth to authenticate
            to the server instead of basic auth.   The default value is None

        client_secret (str): Optional client secret for token-based authentication.
            This value works in conjunction with `client_id` to authenticate to the
            server.  The default value is None

        timeout (int): Configures the timeout value for requests sent to the server.
            The default value for timeout is `30`.

        want_async (bool): When set to True, the factory function will return
            an async connection object and when set to False the factory will
            return a connection object.

    Returns:
        Platform: An initialized Platform connection instance.
    """
    logging.trace(platform_factory, modname=__name__)

    factory = AsyncPlatform if want_async is True else Platform
    return factory(
        host=host,
        port=port,
        use_tls=use_tls,
        verify=verify,
        user=user,
        password=password,
        client_id=client_id,
        client_secret=client_secret,
        timeout=timeout,
    )
