# Copyright (c) 2025 Itential, Inc
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from unittest.mock import AsyncMock
from unittest.mock import Mock

import httpx
import pytest

from ipsdk import exceptions
from ipsdk.connection import AsyncConnection
from ipsdk.gateway import AsyncAuthMixin
from ipsdk.gateway import AsyncGatewayType
from ipsdk.gateway import AuthMixin
from ipsdk.gateway import Gateway
from ipsdk.gateway import GatewayType
from ipsdk.gateway import _make_body
from ipsdk.gateway import _make_headers
from ipsdk.gateway import _make_path
from ipsdk.gateway import gateway_factory
from ipsdk.http import Response

# --------- Factory Tests ---------


def test_gateway_factory_default():
    """Test gateway_factory with default parameters."""
    conn = gateway_factory()
    assert isinstance(conn, Gateway)
    assert conn.user == "admin@itential"
    assert conn.password == "admin"


def test_gateway_factory_custom_params():
    """Test gateway_factory with custom parameters."""
    conn = gateway_factory(
        host="gateway.example.com",
        port=8443,
        user="custom_user",
        password="custom_pass",
        use_tls=False,
        verify=False,
        timeout=60,
    )
    assert isinstance(conn, Gateway)
    assert conn.user == "custom_user"
    assert conn.password == "custom_pass"


def test_gateway_factory_async():
    """Test gateway_factory with async=True."""

    conn = gateway_factory(want_async=True)
    assert isinstance(conn, AsyncConnection)
    assert hasattr(conn, "authenticate")


# --------- Utility Function Tests ---------


def test_make_path():
    """Test _make_path utility function."""
    assert _make_path() == "/login"


def test_make_body():
    """Test _make_body utility function."""
    result = _make_body("user1", "pass1")
    expected = {"username": "user1", "password": "pass1"}
    assert result == expected


def test_make_body_with_special_chars():
    """Test _make_body with special characters."""
    result = _make_body("user@domain.com", "p@ssw0rd!")
    expected = {"username": "user@domain.com", "password": "p@ssw0rd!"}
    assert result == expected


def test_make_headers():
    """Test _make_headers utility function."""
    headers = _make_headers()
    assert headers["Content-Type"] == "application/json"
    assert headers["Accept"] == "application/json"


# --------- Sync AuthMixin Tests ---------


def test_auth_mixin_authenticate_success():
    """Test AuthMixin.authenticate successful authentication."""
    mixin = AuthMixin()
    mixin.user = "admin"
    mixin.password = "adminpass"
    mixin.client = Mock()

    # Mock successful response
    mock_response = Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mixin.client.post.return_value = mock_response

    mixin.authenticate()

    mixin.client.post.assert_called_once_with(
        "/login",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        json={"username": "admin", "password": "adminpass"},
    )
    mock_response.raise_for_status.assert_called_once()


# --------- Async AuthMixin Tests ---------


@pytest.mark.asyncio
async def test_async_auth_mixin_authenticate_success():
    """Test AsyncAuthMixin.authenticate successful authentication."""
    mixin = AsyncAuthMixin()
    mixin.user = "admin"
    mixin.password = "adminpass"
    mixin.client = AsyncMock()

    # Mock successful response
    mock_response = Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.raise_for_status = Mock()
    mixin.client.post.return_value = mock_response

    await mixin.authenticate()

    mixin.client.post.assert_awaited_once_with(
        "/login",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        json={"username": "admin", "password": "adminpass"},
    )
    mock_response.raise_for_status.assert_called_once()


# --------- Integration Tests ---------


def test_gateway_integration_with_connection():
    """Test that Gateway integrates properly with Connection base class."""
    gateway = gateway_factory()

    # Verify it has the expected connection methods
    assert hasattr(gateway, "get")
    assert hasattr(gateway, "post")
    assert hasattr(gateway, "put")
    assert hasattr(gateway, "delete")
    assert hasattr(gateway, "patch")
    assert hasattr(gateway, "authenticate")

    # Verify user and password are set correctly
    assert gateway.user == "admin@itential"
    assert gateway.password == "admin"


def test_gateway_base_url_construction():
    """Test that Gateway constructs the correct base URL."""
    gateway = gateway_factory(host="gateway.example.com", port=8443, use_tls=True)

    # The base URL should include the API path for gateway
    expected_base_url = "https://gateway.example.com:8443/api/v2.0/"
    assert str(gateway.client.base_url) == expected_base_url


def test_gateway_authentication_not_called_initially():
    """Test that Gateway doesn't authenticate until first API call."""
    gateway = gateway_factory()

    # Authentication should not have been called yet
    assert not gateway.authenticated
    assert gateway.token is None


# --------- Additional Gateway Test Cases ---------


def test_gateway_factory_with_all_parameters():
    """Test gateway_factory with all possible parameters."""
    gateway = gateway_factory(
        host="test.example.com",
        port=9443,
        use_tls=True,
        verify=False,
        user="testuser@itential",
        password="testpass123",
        timeout=90,
        want_async=False,
    )

    assert gateway.user == "testuser@itential"
    assert gateway.password == "testpass123"
    # Verify base path is set correctly
    assert "/api/v2.0" in str(gateway.client.base_url)


def test_gateway_factory_async_with_all_parameters():
    """Test async gateway_factory with all parameters."""

    gateway = gateway_factory(
        host="async.example.com",
        port=8443,
        use_tls=False,
        verify=True,
        user="asyncuser@itential",
        password="asyncpass",
        timeout=45,
        want_async=True,
    )

    assert isinstance(gateway, AsyncConnection)
    assert gateway.user == "asyncuser@itential"
    assert gateway.password == "asyncpass"


def test_gateway_type_aliases():
    """Test that gateway type aliases are correctly defined."""

    # Verify type aliases exist and are not None
    assert GatewayType is not None
    assert AsyncGatewayType is not None


def test_make_body_empty_strings():
    """Test _make_body with empty strings."""
    result = _make_body("", "")
    expected = {"username": "", "password": ""}
    assert result == expected


def test_make_body_unicode_characters():
    """Test _make_body with unicode characters."""
    result = _make_body("user_测试", "pass_テスト")
    expected = {"username": "user_测试", "password": "pass_テスト"}
    assert result == expected


def test_make_body_long_strings():
    """Test _make_body with long strings."""
    long_user = "a" * 100
    long_pass = "b" * 100
    result = _make_body(long_user, long_pass)
    expected = {"username": long_user, "password": long_pass}
    assert result == expected


def test_make_headers_immutable():
    """Test that _make_headers returns a new dict each time."""
    headers1 = _make_headers()
    headers2 = _make_headers()

    # Should be equal content but different objects
    assert headers1 == headers2
    assert headers1 is not headers2

    # Modifying one shouldn't affect the other
    headers1["Custom"] = "value"
    assert "Custom" not in headers2


def test_auth_mixin_assertion_errors():
    """Test AuthMixin authentication with missing credentials."""
    mixin = AuthMixin()

    # Test with no user
    mixin.user = None
    mixin.password = "password"
    with pytest.raises(AssertionError):
        mixin.authenticate()

    # Test with no password
    mixin.user = "user"
    mixin.password = None
    with pytest.raises(AssertionError):
        mixin.authenticate()

    # Test with both None
    mixin.user = None
    mixin.password = None
    with pytest.raises(AssertionError):
        mixin.authenticate()


@pytest.mark.asyncio
async def test_async_auth_mixin_assertion_errors():
    """Test AsyncAuthMixin authentication with missing credentials."""
    mixin = AsyncAuthMixin()

    # Test with no user
    mixin.user = None
    mixin.password = "password"
    with pytest.raises(AssertionError):
        await mixin.authenticate()

    # Test with no password
    mixin.user = "user"
    mixin.password = None
    with pytest.raises(AssertionError):
        await mixin.authenticate()

    # Test with both None
    mixin.user = None
    mixin.password = None
    with pytest.raises(AssertionError):
        await mixin.authenticate()


def test_gateway_base_url_with_port_variations():
    """Test Gateway base URL construction with different port configurations."""
    # Test with default HTTP port (80)
    gateway_http = gateway_factory(host="gateway.example.com", port=80, use_tls=False)
    expected_http = "http://gateway.example.com/api/v2.0/"
    assert str(gateway_http.client.base_url) == expected_http

    # Test with default HTTPS port (443)
    gateway_https = gateway_factory(host="gateway.example.com", port=443, use_tls=True)
    expected_https = "https://gateway.example.com/api/v2.0/"
    assert str(gateway_https.client.base_url) == expected_https

    # Test with custom port
    gateway_custom = gateway_factory(
        host="gateway.example.com", port=8080, use_tls=False
    )
    expected_custom = "http://gateway.example.com:8080/api/v2.0/"
    assert str(gateway_custom.client.base_url) == expected_custom


def test_gateway_base_url_auto_port_selection():
    """Test Gateway base URL construction with auto port selection (port=0)."""
    # Test auto port selection with TLS
    gateway_tls = gateway_factory(
        host="secure.gateway.com",
        port=0,  # Auto-select
        use_tls=True,
    )
    # Should use port 443 for HTTPS
    expected_tls = "https://secure.gateway.com/api/v2.0/"
    assert str(gateway_tls.client.base_url) == expected_tls

    # Test auto port selection without TLS
    gateway_no_tls = gateway_factory(
        host="plain.gateway.com",
        port=0,  # Auto-select
        use_tls=False,
    )
    # Should use port 80 for HTTP
    expected_no_tls = "http://plain.gateway.com/api/v2.0/"
    assert str(gateway_no_tls.client.base_url) == expected_no_tls


def test_gateway_integration_inheritance():
    """Test that Gateway properly inherits from both AuthMixin and Connection."""
    gateway = gateway_factory()

    # Should have AuthMixin methods
    assert hasattr(gateway, "authenticate")

    # Should have Connection methods
    assert hasattr(gateway, "get")
    assert hasattr(gateway, "post")
    assert hasattr(gateway, "put")
    assert hasattr(gateway, "delete")
    assert hasattr(gateway, "patch")

    # Should have ConnectionBase attributes
    assert hasattr(gateway, "client")
    assert hasattr(gateway, "user")
    assert hasattr(gateway, "password")
    assert hasattr(gateway, "authenticated")


def test_gateway_vs_async_gateway_types():
    """Test that sync and async gateway factories return different types."""
    sync_gateway = gateway_factory(want_async=False)
    async_gateway = gateway_factory(want_async=True)

    # Should be different types
    assert type(sync_gateway) is not type(async_gateway)

    # But both should have authentication methods
    assert hasattr(sync_gateway, "authenticate")
    assert hasattr(async_gateway, "authenticate")

    # And both should be connection-like
    assert hasattr(sync_gateway, "get")
    assert hasattr(async_gateway, "get")


# --------- Error Handling Tests ---------


def test_auth_mixin_http_status_error():
    """Test AuthMixin.authenticate raises HTTPStatusError on HTTP error."""
    mixin = AuthMixin()
    mixin.user = "admin"
    mixin.password = "adminpass"
    mixin.client = Mock()

    # Mock HTTPStatusError
    mock_request = Mock()
    mock_response = Mock()
    mock_response.status_code = 401
    http_exc = httpx.HTTPStatusError(
        "401 Unauthorized", request=mock_request, response=mock_response
    )

    mock_post_response = Mock()
    mock_post_response.raise_for_status.side_effect = http_exc
    mixin.client.post.return_value = mock_post_response

    with pytest.raises(exceptions.HTTPStatusError):
        mixin.authenticate()


def test_auth_mixin_request_error():
    """Test AuthMixin.authenticate raises RequestError on network error."""
    mixin = AuthMixin()
    mixin.user = "admin"
    mixin.password = "adminpass"
    mixin.client = Mock()

    # Mock RequestError
    mock_request = Mock()
    request_exc = httpx.RequestError("Connection timeout", request=mock_request)

    mixin.client.post.side_effect = request_exc

    with pytest.raises(exceptions.RequestError):
        mixin.authenticate()


@pytest.mark.asyncio
async def test_async_auth_mixin_http_status_error():
    """Test AsyncAuthMixin.authenticate raises HTTPStatusError on HTTP error."""
    mixin = AsyncAuthMixin()
    mixin.user = "admin"
    mixin.password = "adminpass"
    mixin.client = AsyncMock()

    # Mock HTTPStatusError
    mock_request = Mock()
    mock_response = Mock()
    mock_response.status_code = 403
    http_exc = httpx.HTTPStatusError(
        "403 Forbidden", request=mock_request, response=mock_response
    )

    mock_post_response = Mock()
    mock_post_response.raise_for_status.side_effect = http_exc
    mixin.client.post.return_value = mock_post_response

    with pytest.raises(exceptions.HTTPStatusError):
        await mixin.authenticate()


@pytest.mark.asyncio
async def test_async_auth_mixin_request_error():
    """Test AsyncAuthMixin.authenticate raises RequestError on network error."""
    mixin = AsyncAuthMixin()
    mixin.user = "admin"
    mixin.password = "adminpass"
    mixin.client = AsyncMock()

    # Mock RequestError
    mock_request = Mock()
    request_exc = httpx.RequestError("Network failure", request=mock_request)

    mixin.client.post.side_effect = request_exc

    with pytest.raises(exceptions.RequestError):
        await mixin.authenticate()


# --------- Additional Coverage Tests ---------


def test_gateway_client_headers():
    """Test that Gateway client has correct User-Agent header."""
    gateway = gateway_factory()

    # Should have User-Agent header set
    assert "User-Agent" in gateway.client.headers
    assert "ipsdk/" in gateway.client.headers["User-Agent"]


def test_gateway_uses_https_by_default():
    """Test that Gateway uses HTTPS by default."""
    gateway = gateway_factory(host="example.com")

    assert str(gateway.client.base_url).startswith("https://")


def test_gateway_uses_http_when_tls_disabled():
    """Test that Gateway uses HTTP when use_tls=False."""
    gateway = gateway_factory(host="example.com", use_tls=False)

    assert str(gateway.client.base_url).startswith("http://")


def test_gateway_has_api_base_path():
    """Test that Gateway always includes /api/v2.0 in base URL."""
    gateway = gateway_factory(host="example.com")

    assert "/api/v2.0" in str(gateway.client.base_url)


def test_gateway_default_timeout():
    """Test that Gateway uses default timeout of 30 seconds."""
    gateway = gateway_factory()

    # The timeout should be set on the client
    assert gateway.client.timeout.read == 30


def test_gateway_custom_timeout():
    """Test that Gateway respects custom timeout value."""
    gateway = gateway_factory(timeout=60)

    assert gateway.client.timeout.read == 60


def test_gateway_verify_ssl_default():
    """Test that Gateway is created with verify=True by default."""
    gateway = gateway_factory(host="example.com")

    # Gateway should be created successfully with SSL verification
    assert gateway.client is not None


def test_auth_mixin_calls_correct_endpoint():
    """Test that AuthMixin authenticates to the correct endpoint."""
    mixin = AuthMixin()
    mixin.user = "admin"
    mixin.password = "adminpass"
    mixin.client = Mock()

    # Mock successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mixin.client.post.return_value = mock_response

    mixin.authenticate()

    # Verify endpoint is /login
    call_args = mixin.client.post.call_args
    assert call_args[0][0] == "/login" or call_args.args[0] == "/login"


def test_auth_mixin_sends_json_body():
    """Test that AuthMixin sends credentials as JSON body."""
    mixin = AuthMixin()
    mixin.user = "testuser"
    mixin.password = "testpass"
    mixin.client = Mock()

    # Mock successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mixin.client.post.return_value = mock_response

    mixin.authenticate()

    # Verify JSON body is sent
    call_args = mixin.client.post.call_args
    assert call_args.kwargs["json"] == {"username": "testuser", "password": "testpass"}


def test_auth_mixin_sends_correct_headers():
    """Test that AuthMixin sends correct Content-Type and Accept headers."""
    mixin = AuthMixin()
    mixin.user = "admin"
    mixin.password = "pass"
    mixin.client = Mock()

    # Mock successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mixin.client.post.return_value = mock_response

    mixin.authenticate()

    # Verify headers
    call_args = mixin.client.post.call_args
    headers = call_args.kwargs["headers"]
    assert headers["Content-Type"] == "application/json"
    assert headers["Accept"] == "application/json"


@pytest.mark.asyncio
async def test_async_auth_mixin_calls_correct_endpoint():
    """Test that AsyncAuthMixin authenticates to the correct endpoint."""
    mixin = AsyncAuthMixin()
    mixin.user = "admin"
    mixin.password = "adminpass"
    mixin.client = AsyncMock()

    # Mock successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status = Mock()
    mixin.client.post.return_value = mock_response

    await mixin.authenticate()

    # Verify endpoint is /login
    call_args = mixin.client.post.call_args
    assert call_args[0][0] == "/login" or call_args.args[0] == "/login"


@pytest.mark.asyncio
async def test_async_auth_mixin_sends_json_body():
    """Test that AsyncAuthMixin sends credentials as JSON body."""
    mixin = AsyncAuthMixin()
    mixin.user = "testuser"
    mixin.password = "testpass"
    mixin.client = AsyncMock()

    # Mock successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status = Mock()
    mixin.client.post.return_value = mock_response

    await mixin.authenticate()

    # Verify JSON body is sent
    call_args = mixin.client.post.call_args
    assert call_args.kwargs["json"] == {"username": "testuser", "password": "testpass"}


@pytest.mark.asyncio
async def test_async_auth_mixin_sends_correct_headers():
    """Test that AsyncAuthMixin sends correct Content-Type and Accept headers."""
    mixin = AsyncAuthMixin()
    mixin.user = "admin"
    mixin.password = "pass"
    mixin.client = AsyncMock()

    # Mock successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status = Mock()
    mixin.client.post.return_value = mock_response

    await mixin.authenticate()

    # Verify headers
    call_args = mixin.client.post.call_args
    headers = call_args.kwargs["headers"]
    assert headers["Content-Type"] == "application/json"
    assert headers["Accept"] == "application/json"
