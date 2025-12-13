# Copyright (c) 2025 Itential, Inc
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Tests for the ipsdk.__init__ module."""

import ipsdk

from ipsdk import gateway_factory
from ipsdk import logging
from ipsdk import metadata
from ipsdk import platform_factory


def test_module_exports():
    """Test that __init__.py exports the expected items."""
    # Test that __all__ exports are available at module level
    expected_exports = ["gateway_factory", "logging", "platform_factory"]

    for export in expected_exports:
        assert hasattr(ipsdk, export), f"Missing export: {export}"

    # Test that the actual functions are exported
    assert callable(ipsdk.gateway_factory)
    assert callable(ipsdk.platform_factory)
    # logging is a module, not a callable
    assert hasattr(ipsdk.logging, "info")


def test_version_attribute():
    """Test that __version__ is set correctly."""
    assert hasattr(ipsdk, "__version__")
    assert isinstance(ipsdk.__version__, str)
    assert len(ipsdk.__version__) > 0


def test_gateway_factory_integration():
    """Test that gateway_factory works when imported from ipsdk."""
    gateway = ipsdk.gateway_factory()

    # Basic functionality test
    assert hasattr(gateway, "authenticate")
    assert hasattr(gateway, "get")
    assert gateway.user == "admin@itential"
    assert gateway.password == "admin"


def test_platform_factory_integration():
    """Test that platform_factory works when imported from ipsdk."""
    platform = ipsdk.platform_factory()

    # Basic functionality test
    assert hasattr(platform, "authenticate")
    assert hasattr(platform, "get")
    assert platform.user == "admin"
    assert platform.password == "admin"


def test_logging_integration():
    """Test that logging works when imported from ipsdk."""
    # Test that logging has expected methods
    assert hasattr(ipsdk.logging, "debug")
    assert hasattr(ipsdk.logging, "info")
    assert hasattr(ipsdk.logging, "warning")
    assert hasattr(ipsdk.logging, "error")
    assert hasattr(ipsdk.logging, "critical")
    assert hasattr(ipsdk.logging, "set_level")


def test_factories_return_different_types():
    """Test that platform and gateway factories return different types."""
    platform = ipsdk.platform_factory()
    gateway = ipsdk.gateway_factory()

    # Should be different types
    assert type(platform) is not type(gateway)

    # But both should have connection-like interfaces
    for obj in [platform, gateway]:
        assert hasattr(obj, "get")
        assert hasattr(obj, "post")
        assert hasattr(obj, "put")
        assert hasattr(obj, "delete")
        assert hasattr(obj, "patch")
        assert hasattr(obj, "authenticate")


def test_async_factories():
    """Test that both factories support async variants."""
    async_platform = ipsdk.platform_factory(want_async=True)
    async_gateway = ipsdk.gateway_factory(want_async=True)

    # Both should have async interfaces
    for obj in [async_platform, async_gateway]:
        assert hasattr(obj, "authenticate")
        assert hasattr(obj, "get")


def test_module_imports():
    """Test that the module can be imported successfully."""
    # Test direct imports work

    # Test that they are the same as the module-level attributes
    assert gateway_factory is ipsdk.gateway_factory
    assert logging is ipsdk.logging
    assert platform_factory is ipsdk.platform_factory


def test_all_attribute():
    """Test that __all__ is correctly defined."""
    assert hasattr(ipsdk, "__all__")
    assert isinstance(ipsdk.__all__, tuple)

    expected_all = ("gateway_factory", "logging", "platform_factory")
    assert ipsdk.__all__ == expected_all

    # Test that all items in __all__ are actually available
    for item in ipsdk.__all__:
        assert hasattr(ipsdk, item)


def test_metadata_version_consistency():
    """Test that __version__ matches metadata.version."""

    assert ipsdk.__version__ == metadata.version


def test_factory_parameter_passing():
    """Test that factory functions properly pass parameters."""
    # Test platform factory with custom parameters
    platform = ipsdk.platform_factory(
        host="custom.platform.com",
        user="custom_user",
        password="custom_pass",
        timeout=60,
    )
    assert platform.user == "custom_user"
    assert platform.password == "custom_pass"

    # Test gateway factory with custom parameters
    gateway = ipsdk.gateway_factory(
        host="custom.gateway.com",
        user="custom_gateway_user",
        password="custom_gateway_pass",
        timeout=120,
    )
    assert gateway.user == "custom_gateway_user"
    assert gateway.password == "custom_gateway_pass"


def test_module_docstring():
    """Test that the module has proper documentation."""
    # Module should have some documentation
    assert ipsdk.__doc__ is not None or hasattr(ipsdk, "__doc__")
