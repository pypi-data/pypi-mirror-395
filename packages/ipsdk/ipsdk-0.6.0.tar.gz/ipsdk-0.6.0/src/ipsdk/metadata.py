# Copyright (c) 2025 Itential, Inc
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Package metadata and version information for the Itential Python SDK.

This module provides access to package metadata including the package name,
version, and author information. The version is dynamically retrieved from
the installed package metadata using importlib.metadata.

Attributes
----------
name : str
    The package name ("ipsdk"). Used throughout the SDK for logging,
    User-Agent headers, and other identification purposes.

author : str
    The package author ("Itential"). Identifies the organization responsible
    for developing and maintaining the SDK.

version : str
    The current package version string. Retrieved dynamically from the
    installed package metadata using importlib.metadata.version(). The
    version follows PEP440 format and is generated from git tags using
    the uv-dynamic-versioning build plugin.

Version Format
--------------
The version string follows PEP440 format with variations based on the git state:

- Release tags: "1.0.0" (from git tag v1.0.0)
- Development builds: "1.0.0.dev5+g1234567" (5 commits after v1.0.0)
- Dirty working tree: "1.0.0+d20250101" (uncommitted changes)
- No tags: "0.0.0" (fallback when no version tags exist)

The version is automatically updated during the build process based on git
tags and does not require manual maintenance.

Usage
-----
The metadata attributes are primarily used internally by the SDK but can also
be accessed by applications for logging, diagnostics, or display purposes.

Examples
--------
Accessing version information::

    from ipsdk import metadata

    print(f"SDK Name: {metadata.name}")
    print(f"SDK Version: {metadata.version}")
    print(f"SDK Author: {metadata.author}")

Using version in logging::

    from ipsdk import metadata, logging

    logging.info(f"Starting application with {metadata.name} v{metadata.version}")

Including version in User-Agent headers::

    # The SDK automatically includes version in User-Agent headers
    # Format: "ipsdk/{version}"
    # Example: "ipsdk/1.0.0"
    # This is done automatically by ConnectionBase.__init__()

Checking for specific versions::

    from ipsdk import metadata
    from packaging import version

    current = version.parse(metadata.version)
    minimum = version.parse("1.0.0")

    if current >= minimum:
        print("SDK version is compatible")
    else:
        print(f"SDK version {current} is below minimum {minimum}")
"""

from importlib.metadata import version as _version

name: str = "ipsdk"
author: str = "Itential"
version: str = _version(name)
