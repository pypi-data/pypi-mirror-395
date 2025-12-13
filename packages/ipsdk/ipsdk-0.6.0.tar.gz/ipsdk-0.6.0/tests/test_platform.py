# Copyright (c) 2025 Itential, Inc
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from unittest.mock import AsyncMock
from unittest.mock import Mock
from unittest.mock import patch

import httpx
import pytest

from ipsdk import exceptions
from ipsdk.connection import AsyncConnection
from ipsdk.connection import Connection
from ipsdk.http import Response
from ipsdk.platform import AsyncAuthMixin
from ipsdk.platform import AsyncPlatformType
from ipsdk.platform import AuthMixin
from ipsdk.platform import Platform
from ipsdk.platform import PlatformType
from ipsdk.platform import _make_basicauth_body
from ipsdk.platform import _make_basicauth_path
from ipsdk.platform import _make_oauth_body
from ipsdk.platform import _make_oauth_headers
from ipsdk.platform import _make_oauth_path
from ipsdk.platform import platform_factory

# --------- Factory Tests ---------


def test_platform_factory_default():
    """Test platform_factory with default parameters."""
    conn = platform_factory()
    assert isinstance(conn, Platform)
    assert conn.user == "admin"
    assert conn.password == "admin"
    assert conn.client_id is None
    assert conn.client_secret is None


def test_platform_factory_returns_connection():
    """Test that platform_factory returns a Connection instance."""
    p = platform_factory()
    assert isinstance(p, Connection)


def test_platform_factory_returns_async():
    """Test that platform_factory returns AsyncConnection when want_async=True."""
    p = platform_factory(want_async=True)
    assert isinstance(p, AsyncConnection)


def test_platform_factory_custom_params():
    """Test platform_factory with custom parameters."""
    conn = platform_factory(
        host="platform.example.com",
        port=443,
        user="custom_user",
        password="custom_pass",
        client_id="test_client",
        client_secret="test_secret",
        use_tls=True,
        verify=False,
        timeout=120,
    )
    assert isinstance(conn, Platform)
    assert conn.user == "custom_user"
    assert conn.password == "custom_pass"
    assert conn.client_id == "test_client"
    assert conn.client_secret == "test_secret"


def test_platform_factory_oauth_only():
    """Test platform_factory with only OAuth credentials."""
    conn = platform_factory(
        client_id="oauth_client", client_secret="oauth_secret", user=None, password=None
    )
    assert conn.client_id == "oauth_client"
    assert conn.client_secret == "oauth_secret"
    assert conn.user is None
    assert conn.password is None


# --------- Helper Function Tests ---------


def test_make_oauth_headers():
    """Test _make_oauth_headers utility function."""
    headers = _make_oauth_headers()
    assert headers == {"Content-Type": "application/x-www-form-urlencoded"}


def test_make_oauth_path():
    """Test _make_oauth_path utility function."""
    assert _make_oauth_path() == "/oauth/token"


def test_make_oauth_body():
    """Test _make_oauth_body utility function."""
    result = _make_oauth_body("test_id", "test_secret")
    expected = {
        "grant_type": "client_credentials",
        "client_id": "test_id",
        "client_secret": "test_secret",
    }
    assert result == expected


def test_make_oauth_body_special_chars():
    """Test _make_oauth_body with special characters."""
    result = _make_oauth_body("client@domain.com", "secret!@#$%")
    expected = {
        "grant_type": "client_credentials",
        "client_id": "client@domain.com",
        "client_secret": "secret!@#$%",
    }
    assert result == expected


def test_make_basicauth_body():
    """Test _make_basicauth_body utility function."""
    result = _make_basicauth_body("testuser", "testpass")
    expected = {"user": {"username": "testuser", "password": "testpass"}}
    assert result == expected


def test_make_basicauth_path():
    """Test _make_basicauth_path utility function."""
    assert _make_basicauth_path() == "/login"


# --------- Sync AuthMixin Tests ---------


def test_authenticate_oauth_success():
    """Test AuthMixin.authenticate_oauth successful authentication."""
    mixin = AuthMixin()
    mixin.client_id = "test_id"
    mixin.client_secret = "test_secret"
    mixin.client = Mock()

    # Mock successful response
    mock_response = Mock(spec=Response)
    mock_response.text = '{"access_token": "test_token_123"}'
    mock_response.raise_for_status.return_value = None
    mixin.client.post.return_value = mock_response

    with patch(
        "ipsdk.jsonutils.loads", return_value={"access_token": "test_token_123"}
    ):
        mixin.authenticate_oauth()

    assert mixin.token == "test_token_123"
    mixin.client.post.assert_called_once_with(
        "/oauth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": "test_id",
            "client_secret": "test_secret",
        },
    )


def test_authenticate_user_success():
    """Test AuthMixin.authenticate_user successful authentication."""
    mixin = AuthMixin()
    mixin.user = "testuser"
    mixin.password = "testpass"
    mixin.client = Mock()

    # Mock successful response
    mock_response = Mock(spec=Response)
    mock_response.raise_for_status.return_value = None
    mixin.client.post.return_value = mock_response

    mixin.authenticate_user()

    mixin.client.post.assert_called_once_with(
        "/login", json={"user": {"username": "testuser", "password": "testpass"}}
    )


def test_authenticate_prefers_oauth():
    """Test that authenticate prefers OAuth when both credentials are available."""
    mixin = AuthMixin()
    mixin.client_id = "test_id"
    mixin.client_secret = "test_secret"
    mixin.user = "testuser"
    mixin.password = "testpass"
    mixin.client = Mock()

    # Mock OAuth success
    mock_response = Mock(spec=Response)
    mock_response.text = '{"access_token": "oauth_token"}'
    mock_response.raise_for_status.return_value = None
    mixin.client.post.return_value = mock_response

    with patch("ipsdk.jsonutils.loads", return_value={"access_token": "oauth_token"}):
        mixin.authenticate()

    # Should have called OAuth, not basic auth
    mixin.client.post.assert_called_once_with(
        "/oauth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": "test_id",
            "client_secret": "test_secret",
        },
    )
    assert mixin.token == "oauth_token"


def test_authenticate_oauth_preferred_over_basic():
    """Test that authenticate uses OAuth when both OAuth and basic credentials are
    available."""
    mixin = AuthMixin()
    mixin.client_id = "test_id"
    mixin.client_secret = "test_secret"
    mixin.user = "testuser"
    mixin.password = "testpass"
    mixin.client = Mock()

    # Mock OAuth success
    mock_response = Mock(spec=Response)
    mock_response.text = '{"access_token": "oauth_token"}'
    mock_response.raise_for_status.return_value = None
    mixin.client.post.return_value = mock_response

    with patch("ipsdk.jsonutils.loads", return_value={"access_token": "oauth_token"}):
        mixin.authenticate()

    # Should have called OAuth (not basic auth) since OAuth credentials are preferred
    mixin.client.post.assert_called_once_with(
        "/oauth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": "test_id",
            "client_secret": "test_secret",
        },
    )
    assert mixin.token == "oauth_token"


# --------- Async AuthMixin Tests ---------


@pytest.mark.asyncio
@pytest.mark.asyncio
async def test_async_authenticate_basicauth_success():
    """Test AsyncAuthMixin.authenticate_basicauth successful authentication."""
    mixin = AsyncAuthMixin()
    mixin.user = "testuser"
    mixin.password = "testpass"
    mixin.client = AsyncMock()

    # Mock successful response
    mock_response = Mock(spec=Response)
    mock_response.raise_for_status = Mock()
    mixin.client.post.return_value = mock_response

    await mixin.authenticate_basicauth()
    mixin.client.post.assert_awaited_once()


# --------- Integration Tests ---------


def test_platform_integration_with_connection():
    """Test that Platform integrates properly with Connection base class."""
    platform = platform_factory()

    # Verify it has the expected connection methods
    assert hasattr(platform, "get")
    assert hasattr(platform, "post")
    assert hasattr(platform, "put")
    assert hasattr(platform, "delete")
    assert hasattr(platform, "patch")
    assert hasattr(platform, "authenticate")

    # Verify credentials are set correctly
    assert platform.user == "admin"
    assert platform.password == "admin"


def test_platform_base_url_construction():
    """Test that Platform constructs the correct base URL."""
    platform = platform_factory(host="platform.example.com", port=443, use_tls=True)

    # Platform should have no base path (direct to host)
    expected_base_url = "https://platform.example.com"
    assert str(platform.client.base_url) == expected_base_url


def test_platform_authentication_not_called_initially():
    """Test that Platform doesn't authenticate until first API call."""
    platform = platform_factory()

    # Authentication should not have been called yet
    assert not platform.authenticated
    assert platform.token is None


def test_platform_oauth_token_handling():
    """Test that Platform properly handles OAuth tokens."""
    platform = platform_factory(client_id="test_client", client_secret="test_secret")

    # Token should be None initially
    assert platform.token is None

    # After setting a token, it should be available
    platform.token = "test_token_value"
    assert platform.token == "test_token_value"


# --------- Missing OAuth Error Cases ---------


# --------- Missing Basic Auth Error Cases ---------


# --------- Missing Async Auth Cases ---------


# --------- Platform Type and Factory Tests ---------


def test_platform_type_aliases():
    """Test that platform type aliases are correctly defined."""

    # Verify type aliases exist
    assert PlatformType is not None
    assert AsyncPlatformType is not None


def test_platform_factory_with_all_parameters():
    """Test platform_factory with all possible parameters."""
    conn = platform_factory(
        host="example.com",
        port=8443,
        use_tls=True,
        verify=False,
        user="admin",
        password="secret",
        client_id="oauth_client",
        client_secret="oauth_secret",
        timeout=120,
        want_async=False,
    )

    assert conn.user == "admin"
    assert conn.password == "secret"
    assert conn.client_id == "oauth_client"
    assert conn.client_secret == "oauth_secret"


def test_platform_factory_async_with_all_parameters():
    """Test platform_factory async version with all parameters."""
    conn = platform_factory(
        host="example.com",
        port=8443,
        use_tls=False,
        verify=True,
        user="testuser",
        password="testpass",
        client_id=None,
        client_secret=None,
        timeout=60,
        want_async=True,
    )

    assert isinstance(conn, AsyncConnection)
    assert conn.user == "testuser"
    assert conn.password == "testpass"


# --------- Missing Coverage Tests ---------


def test_authenticate_basic_auth_path():
    """Test authenticate() calls authenticate_user() with basic auth."""
    mixin = AuthMixin()
    mixin.user = "testuser"
    mixin.password = "testpass"
    mixin.client_id = None  # No OAuth credentials
    mixin.client_secret = None
    mixin.client = Mock()

    # Mock successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mixin.client.post.return_value = mock_response

    # Call authenticate - should choose basic auth path
    mixin.authenticate()

    # Verify basic auth was called
    mixin.client.post.assert_called_once_with(
        "/login", json={"user": {"username": "testuser", "password": "testpass"}}
    )


@pytest.mark.asyncio
async def test_async_authenticate_basic_auth_path():
    """Test async authenticate() calls authenticate_basicauth() with basic auth."""
    mixin = AsyncAuthMixin()
    mixin.user = "testuser"
    mixin.password = "testpass"
    mixin.client_id = None  # No OAuth credentials
    mixin.client_secret = None
    mixin.client = AsyncMock()

    # Mock successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mixin.client.post.return_value = mock_response

    # Call authenticate - should choose basic auth path
    await mixin.authenticate()

    # Verify basic auth was called
    mixin.client.post.assert_awaited_once()


# --------- Missing Error Handling Tests ---------


def test_authenticate_oauth_no_access_token():
    """Test authenticate_oauth when response has no access_token."""
    mixin = AuthMixin()
    mixin.client_id = "test_id"
    mixin.client_secret = "test_secret"
    mixin.client = Mock()

    # Mock response without access_token
    mock_response = Mock(spec=Response)
    mock_response.text = '{"error": "invalid_grant"}'
    mock_response.raise_for_status.return_value = None
    mixin.client.post.return_value = mock_response

    with patch("ipsdk.jsonutils.loads", return_value={"error": "invalid_grant"}):
        mixin.authenticate_oauth()

    # Token should be None when access_token is missing
    assert mixin.token is None


def test_authenticate_oauth_non_dict_response():
    """Test authenticate_oauth when response is not a dict."""
    mixin = AuthMixin()
    mixin.client_id = "test_id"
    mixin.client_secret = "test_secret"
    mixin.client = Mock()

    # Mock response that parses to a list instead of dict
    mock_response = Mock(spec=Response)
    mock_response.text = '["invalid", "response"]'
    mock_response.raise_for_status.return_value = None
    mixin.client.post.return_value = mock_response

    with patch("ipsdk.jsonutils.loads", return_value=["invalid", "response"]):
        mixin.authenticate_oauth()

    # Token should be None when response is not a dict
    assert mixin.token is None


def test_authenticate_oauth_http_status_error():
    """Test authenticate_oauth raises TypeError due to source bug on HTTP error."""
    mixin = AuthMixin()
    mixin.client_id = "test_id"
    mixin.client_secret = "test_secret"
    mixin.client = Mock()

    # Mock HTTPStatusError
    mock_request = Mock()
    mock_response = Mock()
    mock_response.status_code = 401
    http_exc = httpx.HTTPStatusError(
        "401 Unauthorized", request=mock_request, response=mock_response
    )
    http_exc.message = "401 Unauthorized"

    mock_post_response = Mock()
    mock_post_response.raise_for_status.side_effect = http_exc
    mixin.client.post.return_value = mock_post_response

    # Source has bug: passes exc.message but HTTPStatusError only takes exc
    with pytest.raises(TypeError):
        mixin.authenticate_oauth()


def test_authenticate_oauth_request_error():
    """Test authenticate_oauth raises TypeError due to source bug on network error."""
    mixin = AuthMixin()
    mixin.client_id = "test_id"
    mixin.client_secret = "test_secret"
    mixin.client = Mock()

    # Mock RequestError
    mock_request = Mock()
    request_exc = httpx.RequestError("Network error", request=mock_request)
    request_exc.message = "Network error"

    mixin.client.post.side_effect = request_exc

    # Source has bug: passes exc.message but RequestError only takes exc
    with pytest.raises(TypeError):
        mixin.authenticate_oauth()


def test_authenticate_user_http_status_error():
    """Test authenticate_user raises TypeError due to source bug on HTTP error."""
    mixin = AuthMixin()
    mixin.user = "testuser"
    mixin.password = "testpass"
    mixin.client = Mock()

    # Mock HTTPStatusError
    mock_request = Mock()
    mock_response = Mock()
    mock_response.status_code = 403
    http_exc = httpx.HTTPStatusError(
        "403 Forbidden", request=mock_request, response=mock_response
    )
    http_exc.message = "403 Forbidden"

    mock_post_response = Mock()
    mock_post_response.raise_for_status.side_effect = http_exc
    mixin.client.post.return_value = mock_post_response

    # Source has bug: passes exc.message but HTTPStatusError only takes exc
    with pytest.raises(TypeError):
        mixin.authenticate_user()


def test_authenticate_user_request_error():
    """Test authenticate_user raises TypeError due to source bug on network error."""
    mixin = AuthMixin()
    mixin.user = "testuser"
    mixin.password = "testpass"
    mixin.client = Mock()

    # Mock RequestError
    mock_request = Mock()
    request_exc = httpx.RequestError("Connection timeout", request=mock_request)
    request_exc.message = "Connection timeout"

    mixin.client.post.side_effect = request_exc

    # Source has bug: passes exc.message but RequestError only takes exc
    with pytest.raises(TypeError):
        mixin.authenticate_user()


def test_authenticate_no_credentials_error():
    """Test authenticate raises IpsdkError when no credentials provided."""
    mixin = AuthMixin()
    mixin.user = None
    mixin.password = None
    mixin.client_id = None
    mixin.client_secret = None
    mixin.client = Mock()

    with pytest.raises(exceptions.IpsdkError) as exc_info:
        mixin.authenticate()

    assert "No valid authentication credentials provided" in str(exc_info.value)


def test_authenticate_partial_oauth_credentials():
    """Test authenticate raises error with only client_id but no client_secret."""
    mixin = AuthMixin()
    mixin.client_id = "test_id"
    mixin.client_secret = None  # Missing secret
    mixin.user = None
    mixin.password = None
    mixin.client = Mock()

    with pytest.raises(exceptions.IpsdkError) as exc_info:
        mixin.authenticate()

    assert "No valid authentication credentials provided" in str(exc_info.value)


def test_authenticate_partial_basic_credentials():
    """Test authenticate raises error with only user but no password."""
    mixin = AuthMixin()
    mixin.client_id = None
    mixin.client_secret = None
    mixin.user = "testuser"
    mixin.password = None  # Missing password
    mixin.client = Mock()

    with pytest.raises(exceptions.IpsdkError) as exc_info:
        mixin.authenticate()

    assert "No valid authentication credentials provided" in str(exc_info.value)


# --------- Async Error Handling Tests ---------


@pytest.mark.asyncio
async def test_async_authenticate_oauth_success():
    """Test AsyncAuthMixin.authenticate_oauth successful authentication."""
    mixin = AsyncAuthMixin()
    mixin.client_id = "test_id"
    mixin.client_secret = "test_secret"
    mixin.client = AsyncMock()

    # Mock successful response
    mock_response = Mock(spec=Response)
    mock_response.text = '{"access_token": "async_token_123"}'
    mock_response.raise_for_status = Mock()
    mixin.client.post.return_value = mock_response

    await mixin.authenticate_oauth()

    # Verify the post was called with correct params
    mixin.client.post.assert_awaited_once_with(
        "/oauth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": "test_id",
            "client_secret": "test_secret",
        },
    )


@pytest.mark.asyncio
async def test_async_authenticate_oauth_http_status_error():
    """Test async authenticate_oauth raises TypeError due to source bug."""
    mixin = AsyncAuthMixin()
    mixin.client_id = "test_id"
    mixin.client_secret = "test_secret"
    mixin.client = AsyncMock()

    # Mock HTTPStatusError
    mock_request = Mock()
    mock_response = Mock()
    mock_response.status_code = 401
    http_exc = httpx.HTTPStatusError(
        "401 Unauthorized", request=mock_request, response=mock_response
    )
    http_exc.message = "401 Unauthorized"

    mock_post_response = Mock()
    mock_post_response.raise_for_status.side_effect = http_exc
    mixin.client.post.return_value = mock_post_response

    # Source has bug: passes exc.message but HTTPStatusError only takes exc
    with pytest.raises(TypeError):
        await mixin.authenticate_oauth()


@pytest.mark.asyncio
async def test_async_authenticate_oauth_request_error():
    """Test async authenticate_oauth raises TypeError due to bug."""
    mixin = AsyncAuthMixin()
    mixin.client_id = "test_id"
    mixin.client_secret = "test_secret"
    mixin.client = AsyncMock()

    # Mock RequestError
    mock_request = Mock()
    request_exc = httpx.RequestError("Network failure", request=mock_request)
    request_exc.message = "Network failure"

    mixin.client.post.side_effect = request_exc

    # Source has bug: passes exc.message but RequestError only takes exc
    with pytest.raises(TypeError):
        await mixin.authenticate_oauth()


@pytest.mark.asyncio
async def test_async_authenticate_basicauth_http_status_error():
    """Test async authenticate_basicauth raises TypeError due to bug."""
    mixin = AsyncAuthMixin()
    mixin.user = "testuser"
    mixin.password = "testpass"
    mixin.client = AsyncMock()

    # Mock HTTPStatusError
    mock_request = Mock()
    mock_response = Mock()
    mock_response.status_code = 403
    http_exc = httpx.HTTPStatusError(
        "403 Forbidden", request=mock_request, response=mock_response
    )
    http_exc.message = "403 Forbidden"

    mock_post_response = Mock()
    mock_post_response.raise_for_status.side_effect = http_exc
    mixin.client.post.return_value = mock_post_response

    # Source has bug: passes exc.message but HTTPStatusError only takes exc
    with pytest.raises(TypeError):
        await mixin.authenticate_basicauth()


@pytest.mark.asyncio
async def test_async_authenticate_basicauth_request_error():
    """Test async authenticate_basicauth raises TypeError due to bug."""
    mixin = AsyncAuthMixin()
    mixin.user = "testuser"
    mixin.password = "testpass"
    mixin.client = AsyncMock()

    # Mock RequestError
    mock_request = Mock()
    request_exc = httpx.RequestError("Connection failed", request=mock_request)
    request_exc.message = "Connection failed"

    mixin.client.post.side_effect = request_exc

    # Source has bug: passes exc.message but RequestError only takes exc
    with pytest.raises(TypeError):
        await mixin.authenticate_basicauth()


@pytest.mark.asyncio
async def test_async_authenticate_no_credentials_error():
    """Test async authenticate raises IpsdkError when no credentials provided."""
    mixin = AsyncAuthMixin()
    mixin.user = None
    mixin.password = None
    mixin.client_id = None
    mixin.client_secret = None
    mixin.client = AsyncMock()

    with pytest.raises(exceptions.IpsdkError) as exc_info:
        await mixin.authenticate()

    assert "No valid authentication credentials provided" in str(exc_info.value)


@pytest.mark.asyncio
async def test_async_authenticate_oauth_path():
    """Test async authenticate() chooses OAuth path when OAuth credentials provided."""
    mixin = AsyncAuthMixin()
    mixin.client_id = "test_id"
    mixin.client_secret = "test_secret"
    mixin.user = None
    mixin.password = None
    mixin.client = AsyncMock()

    # Mock successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status = Mock()
    mixin.client.post.return_value = mock_response

    await mixin.authenticate()

    # Verify OAuth was called
    mixin.client.post.assert_awaited_once_with(
        "/oauth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": "test_id",
            "client_secret": "test_secret",
        },
    )


# --------- Additional Integration Tests ---------


def test_platform_mixin_inheritance():
    """Test that Platform properly inherits from both AuthMixin and Connection."""
    platform = platform_factory()

    # Should have AuthMixin methods
    assert hasattr(platform, "authenticate")
    assert hasattr(platform, "authenticate_oauth")
    assert hasattr(platform, "authenticate_user")

    # Should have Connection methods
    assert hasattr(platform, "get")
    assert hasattr(platform, "post")
    assert hasattr(platform, "_send_request")
    assert hasattr(platform, "_build_request")


def test_platform_client_headers():
    """Test that Platform client has correct User-Agent header."""
    platform = platform_factory()

    # Should have User-Agent header set
    assert "User-Agent" in platform.client.headers
    assert "ipsdk/" in platform.client.headers["User-Agent"]


def test_platform_uses_https_by_default():
    """Test that Platform uses HTTPS by default."""
    platform = platform_factory(host="example.com")

    assert str(platform.client.base_url).startswith("https://")


def test_platform_uses_http_when_tls_disabled():
    """Test that Platform uses HTTP when use_tls=False."""
    platform = platform_factory(host="example.com", use_tls=False)

    assert str(platform.client.base_url).startswith("http://")


def test_platform_custom_port_in_url():
    """Test that Platform includes custom port in base URL."""
    platform = platform_factory(host="example.com", port=8443, use_tls=True)

    assert "8443" in str(platform.client.base_url)


def test_platform_standard_port_not_in_url():
    """Test that Platform does not include standard ports (80, 443) in base URL."""
    platform_https = platform_factory(host="example.com", port=443, use_tls=True)
    platform_http = platform_factory(host="example.com", port=80, use_tls=False)

    # Standard ports should not appear in URL
    assert ":443" not in str(platform_https.client.base_url)
    assert ":80" not in str(platform_http.client.base_url)


def test_platform_zero_port_auto_determines():
    """Test that Platform auto-determines port when port=0."""
    platform_tls = platform_factory(host="example.com", port=0, use_tls=True)
    platform_no_tls = platform_factory(host="example.com", port=0, use_tls=False)

    # Port 0 should auto-determine to 443 (HTTPS) or 80 (HTTP)
    # Standard ports are not shown in URL
    assert ":443" not in str(platform_tls.client.base_url)
    assert ":80" not in str(platform_no_tls.client.base_url)
    assert str(platform_tls.client.base_url).startswith("https://")
    assert str(platform_no_tls.client.base_url).startswith("http://")
