# ipsdk

[![PyPI version](https://badge.fury.io/py/ipsdk.svg)](https://badge.fury.io/py/ipsdk)
[![Python Versions](https://img.shields.io/pypi/pyversions/ipsdk.svg)](https://pypi.org/project/ipsdk/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Tests](https://github.com/itential/ipsdk/workflows/Run%20pre%20merge%20pipeline/badge.svg)](https://github.com/itential/ipsdk/actions)
[![Coverage](https://img.shields.io/badge/coverage-95%25-green)](https://github.com/itential/ipsdk)

The Itential Python SDK provides a robust client implementation in Python for writing
scripts and applications that can make API calls to Itential Platform or Itential
Automation Gateway 4.x.

**Status**: Beta - Active development with comprehensive test coverage (95%+)

## Features

- **Easy API Requests**: Automatic authentication on first API call with session management
- **Multiple Authentication Methods**:
  - OAuth (client credentials) for Itential Platform
  - Basic authentication (username/password) for both Platform and Gateway
- **Sync and Async Support**: Both synchronous and asynchronous HTTP clients via `want_async` parameter
- **Comprehensive Logging**: Custom logging system with multiple levels (including FATAL), file and console handlers, and httpx integration control
- **Flexible Configuration**: Customizable connection settings including TLS, certificate verification, timeouts, and proxy support
- **Type Safety**: Full type hints with mypy support for enhanced development experience
- **HTTP Methods**: Support for GET, POST, PUT, DELETE, and PATCH operations with automatic JSON handling
- **Request/Response Wrappers**: Enhanced request and response objects with additional utilities beyond raw httpx

## Getting started

## Requirements

- Python 3.10 or higher
- httpx >= 0.28.1

### Tested Python Versions

| Python Version | Status | Notes |
|----------------|--------|-------|
| 3.10           | ✅ Tested | Minimum recommended version |
| 3.11           | ✅ Tested | Full support |
| 3.12           | ✅ Tested | Full support |
| 3.13           | ✅ Tested | Latest stable release |
| 3.14           | 🔄 Beta | Development/preview testing |

The SDK is automatically tested against Python 3.10-3.13 in our CI pipeline to ensure compatibility across all supported versions.

## Installation

Install `ipsdk` using pip:

```bash
$ pip install ipsdk
```

Or using uv (recommended for development):

```bash
$ uv add ipsdk
```

The `ipsdk` package provides factory functions for connecting to either
Itential Platform or Itential Automation Gateway.

The `platform_factory(...)` function creates a connection to Itential Platform
The `gateway_factory(...)` function creates a connection to Itential Automation Gateway

### Basic Authentication

Use basic authentication with username and password:

```python
>>> import ipsdk
>>> platform = ipsdk.platform_factory(
...     host="platform.itential.dev",
...     user="admin@pronghorn",
...     password="your-password"
... )
>>> res = platform.get("/health/server")
>>> res
<Response [200 OK]>
>>> res.text
'{"version":"15.8.10-2023.2.44","release":"2023.2.9"...`
```

### OAuth Authentication

For Itential Platform, you can use OAuth with client credentials:

```python
>>> import ipsdk
>>> platform = ipsdk.platform_factory(
...     host="platform.itential.dev",
...     client_id="your-client-id",
...     client_secret="your-client-secret"
... )
>>> res = platform.get("/adapters")
```

### Gateway Connection

Connecting to Itential Automation Gateway uses the same pattern:

```python
>>> import ipsdk
>>> gateway = ipsdk.gateway_factory(
...     host="gateway.itential.dev",
...     user="admin@itential",
...     password="your-password"
... )
>>> res = gateway.get("/devices")
```

### Async Support

The SDK fully supports `asyncio` for asynchronous operations. Set `want_async=True`
when creating the connection:

```python
import asyncio
import ipsdk

async def main():
    p = ipsdk.platform_factory(
        host="platform.itential.dev",
        user="admin@pronghorn",
        want_async=True
    )

    res = await p.get("/adapters")

if __name__ == "__main__":
    asyncio.run(main())
```

## HTTP Methods

The connection object supports the following HTTP methods:

- `GET` - Sends a HTTP GET request to the server and returns the results
- `POST` - Sends a HTTP POST request to the server and returns the results
- `PUT` - Sends a HTTP PUT request to the server and returns the results
- `DELETE` - Sends a HTTP DELETE request to the server and returns the results
- `PATCH` - Sends a HTTP PATCH request to the server and returns the results

The following table shows the keyword arguments for each HTTP method:

 | Keyword  | `GET`         | `POST`   | `PUT`    | `DELETE`      | `PATCH`  |
 |----------|---------------|----------|----------|---------------|----------|
 | `path`   | Required      | Required | Required | Required      | Required |
 | `params` | Optional      | Optional | Optional | Optional      | Optional |
 | `json`   | Not Supported | Optional | Optional | Not Supported | Optional |

The `path` argument specifies the relative path of the URI.   This value is
prepended to the base URL.  The base URL for Itential Platform is `<host>` and
the base URL for Itential Automation Gateway is `<host>/api/v2.0`.

The `params` argument accepts a `dict` object that is transformed into the URL
query string.  For example, if `params={"foo": "bar"}` the resulting query
string would be `?foo=bar`

The `json` argument accepts the payload to send in the request as JSON. This
argument accepts either a `list` or `dict` object. When specified, the data
will automatically be converted to a JSON string and the `Content-Type` and
`Accept` headers will be set to `application/json`.

## Configuration

Both the `platform_factory` and `gateway_factory` functions support
configuration using keyword arguments. The table below shows the keyword
arguments for each function along with their default value.

 | Keyword         | `platform_factory` | `gateway_factory` |
 |-----------------|--------------------|-------------------|
 | `host`          | `localhost`        | `localhost`       |
 | `port`          | `0`                | `0`               |
 | `use_tls`       | `True`             | `True`            |
 | `verify`        | `True`             | `True`            |
 | `user`          | `admin`            | `admin@itential`  |
 | `password`      | `admin`            | `admin`           |
 | `client_id`     | `None`             | Not Supported     |
 | `client_secret` | `None`             | Not Supported     |
 | `timeout`       | `30`               | `30`              |
 | `want_async`    | `False`            | `False`           |

## Logging

The SDK includes a comprehensive logging system accessible via `ipsdk.logging`:

```python
import ipsdk

# Configure logging level
ipsdk.logging.set_level(ipsdk.logging.DEBUG)

# Enable file logging
ipsdk.logging.configure_file_logging(
    "/path/to/logfile.log",
    level=ipsdk.logging.INFO
)

# Use convenience functions
ipsdk.logging.info("Connected to platform")
ipsdk.logging.debug("Request details: %s", request_data)
ipsdk.logging.error("API call failed")
```

**Logging Features**:
- **Multiple Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL, and custom FATAL (90) level
- **Convenience Functions**: `debug()`, `info()`, `warning()`, `error()`, `critical()`, `fatal()`, `exception()`
- **File Logging**: Automatic directory creation and custom formatting support
- **Console Control**: Switch between stdout/stderr output
- **httpx Integration**: Optional control of httpx/httpcore logging via `propagate` parameter
- **Handler Management**: Add/remove file handlers and customize console output

For detailed logging documentation, see the logging module docstrings.

## Development

For development setup, testing, and contribution guidelines, see the [Development Guide](docs/development.md).


## License

This project is licensed under the GPLv3 open source license.  See
[license](LICENSE)
