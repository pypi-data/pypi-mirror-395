# Copyright (c) 2025 Itential, Inc
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

r"""Comprehensive logging system for the Itential Python SDK.

This module provides a full-featured logging implementation with support for
custom log levels, function tracing, and sensitive data filtering.

Features:
    - Extended logging levels:
        - TRACE (5) - For detailed function invocation tracing
        - FATAL (90) - For fatal errors that exit the application
        - NONE (100) - To disable all logging output
    - Convenience functions for all log levels: debug(), info(), warning(),
      error(), critical(), fatal(), exception(), trace()
    - Configuration functions:
        - set_level() - Set logging level with optional httpx/httpcore control
        - initialize() - Reset and initialize logging handlers
        - get_logger() - Get the main application logger
    - Sensitive data filtering:
        - enable_sensitive_data_filtering() - Enable PII/credential redaction
        - disable_sensitive_data_filtering() - Disable filtering
        - configure_sensitive_data_patterns() - Add custom patterns
        - add_sensitive_data_pattern() - Add individual pattern
        - remove_sensitive_data_pattern() - Remove pattern
        - get_sensitive_data_patterns() - List configured patterns
    - httpx/httpcore logging control via propagate parameter
    - Automatic initialization with stderr handler

Logging Levels:
    NOTSET (0), TRACE (5), DEBUG (10), INFO (20), WARNING (30), ERROR (40),
    CRITICAL (50), FATAL (90), NONE (100)

Example:
    Basic usage with console logging::

        from ipsdk import logging

        # Set logging level
        logging.set_level(logging.INFO)

        # Log messages at different levels
        logging.info("Application started")
        logging.warning("Configuration file not found, using defaults")
        logging.error("An error occurred")

    Function tracing for debugging::

        from ipsdk import logging

        # Enable TRACE level for detailed function tracing
        logging.set_level(logging.TRACE)

        def process_data(data):
            logging.trace(process_data)  # Logs "invoking process_data"
            # ... function implementation
            return result

    Fatal errors that exit the application::

        from ipsdk import logging

        if critical_error:
            logging.fatal("Critical failure, cannot continue")
            # This will log at FATAL level, print to console, and exit with code 1

    Sensitive data filtering::

        from ipsdk import logging

        # Enable sensitive data filtering
        logging.enable_sensitive_data_filtering()

        # Add custom pattern for SSN
        logging.add_sensitive_data_pattern(
            "ssn",
            r"(?:SSN|social[_-]?security):\s*(\d{3}-\d{2}-\d{4})"
        )

        # Log messages will automatically redact sensitive data
        logging.info("User credentials: api_key=secret123456789012345")
        # Output: "User credentials: [REDACTED_API_KEY]"

    Controlling httpx/httpcore logging::

        from ipsdk import logging

        # Enable httpx logging along with application logging
        logging.set_level(logging.DEBUG, propagate=True)

    Disabling all logging::

        from ipsdk import logging

        # Set to NONE to disable all log output
        logging.set_level(logging.NONE)
"""

import logging
import sys
import traceback

from functools import partial
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

from . import heuristics
from . import metadata

logging_message_format = "%(asctime)s: [%(name)s] %(levelname)s: %(message)s"

logging.getLogger(metadata.name).setLevel(100)

# Add the FATAL logging level
logging.FATAL = 90  # type: ignore[misc]
logging.addLevelName(logging.FATAL, "FATAL")

logging.NONE = logging.FATAL + 10
logging.addLevelName(logging.NONE, "NONE")

logging.TRACE = 5
logging.addLevelName(logging.TRACE, "TRACE")

# Logging level constants that wrap stdlib logging module constants
NOTSET = logging.NOTSET
TRACE = logging.NOTSET
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
NONE = logging.NONE

# Global flag for sensitive data filtering
_sensitive_data_filtering_enabled = False


def log(lvl: int, msg: str) -> None:
    """Send the log message with the specified level.

    This function will send the log message to the logger with the specified
    logging level. If sensitive data filtering is enabled, the message will
    be scanned and any sensitive information (such as API keys, passwords,
    tokens) will be redacted before logging.

    This function should not be directly invoked. Use one of the convenience
    functions (debug, info, warning, error, critical, fatal) to send a log
    message with a given level.

    Args:
        lvl (int): The logging level of the message.
        msg (str): The message to write to the logger.

    Returns:
        None

    Raises:
        None
    """
    # Apply sensitive data filtering if enabled
    if _sensitive_data_filtering_enabled:
        msg = heuristics.scan_and_redact(msg)

    logging.getLogger(metadata.name).log(lvl, msg)


# Convenience functions for different logging levels
debug = partial(log, logging.DEBUG)
info = partial(log, logging.INFO)
warning = partial(log, logging.WARNING)
error = partial(log, logging.ERROR)
critical = partial(log, logging.CRITICAL)


def trace(
    f: Callable,
    modname: Optional[str] = None,
    clsname: Optional[str] = None
) -> None:
    """Log a trace message for function invocation.

    This function logs a trace-level message indicating that a function
    is being invoked. Useful for detailed debugging and execution flow tracking.

    Args:
        f (Callable): The function being invoked

    Returns:
        None

    Raises:
        None
    """
    msg = ""

    if modname is not None:
        msg += f"{modname}."

    if clsname is not None:
        msg += f"{clsname.__name__}."

    msg += f.__name__

    log(logging.TRACE, msg)


def exception(exc: Exception) -> None:
    """Log an exception error with full traceback.

    This function logs an exception at ERROR level, including the full
    traceback information to help with debugging. The traceback shows
    the complete call stack from where the exception was raised.

    Args:
        exc (Exception): Exception to log as an error.

    Returns:
        None

    Raises:
        None
    """
    # Format the exception with full traceback
    tb_lines = traceback.format_exception(type(exc), exc, exc.__traceback__)
    tb_text = "".join(tb_lines)
    log(logging.ERROR, tb_text)


def fatal(msg: str) -> None:
    """Log a fatal error and exit the application.

    A fatal error will log the message using level 90 (FATAL) and print
    an error message to stdout. It will then exit the application with
    return code 1.

    Args:
        msg (str): The message to print.

    Returns:
        None

    Raises:
        SystemExit: Always raised with exit code 1 after logging the fatal error.
    """
    log(logging.FATAL, msg)
    print(f"ERROR: {msg}")
    sys.exit(1)


def _get_loggers() -> set[logging.Logger]:
    """Get all relevant loggers for the application.

    Retrieves loggers that belong to the Itential MCP application and its
    dependencies (ipsdk, FastMCP).

    Returns:
        set[logging.Logger]: Set of logger instances for the application and dependencies.
    """
    loggers = set()
    for name in logging.Logger.manager.loggerDict:
        if name.startswith((metadata.name, "httpx")):
            loggers.add(logging.getLogger(name))
    return loggers


def get_logger() -> logging.Logger:
    """Get the main application logger.

    Args:
        None

    Returns:
        logging.Logger: The logger instance for the ipsdk application.

    Raises:
        None
    """
    return logging.getLogger(metadata.name)


def set_level(lvl: int, *, propagate: bool = False) -> None:
    """Set logging level for all loggers in the current Python process.

    Args:
        lvl (int): Logging level (e.g., logging.INFO, logging.DEBUG). This
            is a required argument.
        propagate (bool): Setting this value to True will also turn on
            logging for httpx and httpcore. Defaults to False.

    Returns:
        None

    Raises:
        None
    """
    logger = get_logger()

    if lvl == "NONE":
        lvl = NONE

    logger.setLevel(lvl)
    logger.propagate = False

    logger.log(logging.INFO, f"{metadata.name} version {metadata.version}")
    logger.log(logging.INFO, f"Logging level set to {lvl}")

    if propagate is True:
        for logger in _get_loggers():
            logger.setLevel(lvl)


def enable_sensitive_data_filtering() -> None:
    """Enable sensitive data filtering in log messages.

    When enabled, log messages will be scanned for potentially sensitive
    information (such as passwords, tokens, API keys) and redacted before
    being written to the log output.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    global _sensitive_data_filtering_enabled  # noqa: PLW0603
    _sensitive_data_filtering_enabled = True


def disable_sensitive_data_filtering() -> None:
    """Disable sensitive data filtering in log messages.

    When disabled, log messages will be written as-is without scanning
    for sensitive information. Use with caution in production environments
    as this may expose sensitive data in log files.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    global _sensitive_data_filtering_enabled  # noqa: PLW0603
    _sensitive_data_filtering_enabled = False


def is_sensitive_data_filtering_enabled() -> bool:
    """Check if sensitive data filtering is currently enabled.

    Returns the current state of sensitive data filtering to determine
    if log messages are being scanned and redacted.

    Args:
        None

    Returns:
        bool: True if filtering is enabled, False otherwise

    Raises:
        None
    """
    return _sensitive_data_filtering_enabled


def configure_sensitive_data_patterns(
    custom_patterns: Optional[Dict[str, str]] = None,
) -> None:
    """Configure custom patterns for sensitive data detection.

    Allows configuration of custom regular expression patterns to identify
    and redact sensitive information in log messages. Each pattern should
    match sensitive data that needs to be protected.

    Args:
        custom_patterns (Optional[Dict[str, str]]): Dictionary of custom regex
            patterns to add to the sensitive data scanner. Keys are pattern
            names (for identification) and values are regex patterns to match
            sensitive data. If None, no patterns are added

    Returns:
        None

    Raises:
        re.error: If any of the custom patterns are invalid regex expressions
    """
    heuristics.configure_scanner(custom_patterns)


def get_sensitive_data_patterns() -> List[str]:
    """Get a list of all sensitive data patterns currently configured.

    Returns the names of all patterns currently registered with the sensitive
    data scanner for identifying and redacting sensitive information.

    Args:
        None

    Returns:
        List[str]: List of pattern names that are being scanned for

    Raises:
        None
    """
    return heuristics.get_scanner().list_patterns()


def add_sensitive_data_pattern(name: str, pattern: str) -> None:
    """Add a new sensitive data pattern to scan for.

    Registers a new regular expression pattern with the sensitive data scanner.
    The pattern will be used to identify and redact matching sensitive information
    in log messages when filtering is enabled.

    Args:
        name (str): Unique name for the pattern, used for identification and
            later removal if needed
        pattern (str): Regular expression pattern to match sensitive data

    Returns:
        None

    Raises:
        re.error: If the regex pattern is invalid or malformed
    """
    heuristics.get_scanner().add_pattern(name, pattern)


def remove_sensitive_data_pattern(name: str) -> bool:
    """Remove a sensitive data pattern from scanning.

    Unregisters a previously added sensitive data pattern from the scanner.
    After removal, the pattern will no longer be used to identify and
    redact sensitive information in log messages.

    Args:
        name (str): Name of the pattern to remove (as provided when the
            pattern was added)

    Returns:
        bool: True if the pattern was found and removed, False if the
            pattern name didn't exist in the scanner

    Raises:
        None
    """
    return heuristics.get_scanner().remove_pattern(name)


def initialize() -> None:
    """Initialize logging configuration for the application.

    Resets all managed loggers by removing their existing handlers and
    replacing them with a standard StreamHandler that writes to stderr.
    This ensures consistent logging configuration across all related loggers.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    for logger in _get_loggers():
        handlers = logger.handlers[:]

        for handler in handlers:
            logger.removeHandler(handler)
            handler.close()

        stream_handler = logging.StreamHandler(sys.stderr)
        stream_handler.setFormatter(logging.Formatter(logging_message_format))

        logger.addHandler(stream_handler)
        logger.setLevel(NONE)
        logger.propagate = False
