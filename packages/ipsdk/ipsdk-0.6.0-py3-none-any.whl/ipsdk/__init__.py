# Copyright (c) 2025 Itential, Inc
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

r"""Itential Python SDK for Itential Platform and Automation Gateway.

This package provides a comprehensive SDK for interacting with Itential's APIs,
including both Platform and Automation Gateway. It offers both synchronous and
asynchronous HTTP client implementations with automatic authentication, request/response
handling, and robust error management.

Main Components
---------------
The SDK exports two main factory functions for creating client connections:

platform_factory:
    Creates connections to Itential Platform with support for both OAuth
    (client credentials) and basic authentication. Provides full access to
    Platform APIs for workflow management, automation, and orchestration.

gateway_factory:
    Creates connections to Itential Automation Gateway with basic authentication.
    Provides access to Gateway APIs for network device automation and
    configuration management.

logging:
    Comprehensive logging system with custom levels (TRACE, FATAL), sensitive
    data filtering, and convenient configuration functions.

Features
--------
- Automatic authentication on first request
- Support for both synchronous and asynchronous operations
- Configurable TLS/SSL certificate verification
- Request timeout configuration
- JSON request/response handling with automatic Content-Type headers
- Comprehensive exception hierarchy for error handling
- Built-in logging with trace-level debugging support
- Sensitive data filtering for PII and credentials

Example
-------
Basic usage with Platform::

    from ipsdk import platform_factory

    # Connect to Platform with OAuth
    platform = platform_factory(
        host="platform.example.com",
        client_id="your-client-id",
        client_secret="your-client-secret"
    )

    # Make API calls
    response = platform.get("/api/v2.0/workflows")
    workflows = response.json()

Basic usage with Gateway::

    from ipsdk import gateway_factory

    # Connect to Gateway with basic auth
    gateway = gateway_factory(
        host="gateway.example.com",
        user="admin@itential",
        password="password"
    )

    # Make API calls
    response = gateway.get("/devices")
    devices = response.json()

Async usage::

    from ipsdk import platform_factory

    # Create async client
    platform = platform_factory(
        host="platform.example.com",
        client_id="your-client-id",
        client_secret="your-client-secret",
        want_async=True
    )

    # Use async/await
    async def get_workflows():
        response = await platform.get("/api/v2.0/workflows")
        return response.json()

Logging configuration::

    from ipsdk import logging

    # Set logging level
    logging.set_level(logging.DEBUG)

    # Enable sensitive data filtering
    logging.enable_sensitive_data_filtering()

    # Add custom pattern
    logging.add_sensitive_data_pattern("ssn", r"\d{3}-\d{2}-\d{4}")
"""

from . import logging
from . import metadata
from .gateway import gateway_factory
from .platform import platform_factory

__version__ = metadata.version

__all__ = ("gateway_factory", "logging", "platform_factory")


logging.initialize()
