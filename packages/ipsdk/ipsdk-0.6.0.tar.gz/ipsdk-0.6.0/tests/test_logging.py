# Copyright (c) 2025 Itential, Inc
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import logging
import sys

from unittest.mock import Mock
from unittest.mock import patch

from ipsdk import heuristics
from ipsdk import logging as ipsdk_logging
from ipsdk import metadata


class TestLoggingConstants:
    """Test logging constants and levels."""

    def test_logging_constants_exist(self):
        """Test that all logging constants are properly defined."""
        assert hasattr(ipsdk_logging, "NOTSET")
        assert hasattr(ipsdk_logging, "TRACE")
        assert hasattr(ipsdk_logging, "DEBUG")
        assert hasattr(ipsdk_logging, "INFO")
        assert hasattr(ipsdk_logging, "WARNING")
        assert hasattr(ipsdk_logging, "ERROR")
        assert hasattr(ipsdk_logging, "CRITICAL")
        assert hasattr(ipsdk_logging, "FATAL")
        assert hasattr(ipsdk_logging, "NONE")

    def test_logging_constants_values(self):
        """Test that logging constants have correct values."""
        assert ipsdk_logging.NOTSET == logging.NOTSET
        assert ipsdk_logging.TRACE == logging.NOTSET  # TRACE is aliased to NOTSET
        assert ipsdk_logging.DEBUG == logging.DEBUG
        assert ipsdk_logging.INFO == logging.INFO
        assert ipsdk_logging.WARNING == logging.WARNING
        assert ipsdk_logging.ERROR == logging.ERROR
        assert ipsdk_logging.CRITICAL == logging.CRITICAL
        assert ipsdk_logging.FATAL == 90
        assert ipsdk_logging.NONE == 100

    def test_fatal_level_registered(self):
        """Test that FATAL level is properly registered with logging module."""
        assert logging.getLevelName(90) == "FATAL"

    def test_none_level_registered(self):
        """Test that NONE level is properly registered with logging module."""
        assert logging.getLevelName(100) == "NONE"

    def test_trace_level_registered(self):
        """Test that TRACE level is properly registered with logging module."""
        assert logging.getLevelName(5) == "TRACE"


class TestLogFunction:
    """Test the main log function."""

    def test_log_function_calls_logger(self):
        """Test that log function properly calls the logger."""
        with patch("ipsdk.logging.logging.getLogger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            ipsdk_logging.log(logging.INFO, "test message")

            mock_get_logger.assert_called_once_with(metadata.name)
            mock_logger.log.assert_called_once_with(logging.INFO, "test message")

    def test_log_function_different_levels(self):
        """Test log function with different logging levels."""
        with patch("ipsdk.logging.logging.getLogger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            levels_and_messages = [
                (logging.DEBUG, "debug message"),
                (logging.INFO, "info message"),
                (logging.WARNING, "warning message"),
                (logging.ERROR, "error message"),
                (logging.CRITICAL, "critical message"),
                (ipsdk_logging.FATAL, "fatal message"),
                (ipsdk_logging.NONE, "none message"),
                (5, "trace message"),  # TRACE level
            ]

            for level, message in levels_and_messages:
                ipsdk_logging.log(level, message)
                mock_logger.log.assert_called_with(level, message)


class TestConvenienceFunctions:
    """Test the convenience logging functions (debug, info, warning, etc.)."""

    def test_debug_function(self):
        """Test debug convenience function."""
        with patch("ipsdk.logging.logging.getLogger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            ipsdk_logging.debug("debug message")
            mock_logger.log.assert_called_once_with(logging.DEBUG, "debug message")

    def test_info_function(self):
        """Test info convenience function."""
        with patch("ipsdk.logging.logging.getLogger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            ipsdk_logging.info("info message")
            mock_logger.log.assert_called_once_with(logging.INFO, "info message")

    def test_warning_function(self):
        """Test warning convenience function."""
        with patch("ipsdk.logging.logging.getLogger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            ipsdk_logging.warning("warning message")
            mock_logger.log.assert_called_once_with(logging.WARNING, "warning message")

    def test_error_function(self):
        """Test error convenience function."""
        with patch("ipsdk.logging.logging.getLogger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            ipsdk_logging.error("error message")
            mock_logger.log.assert_called_once_with(logging.ERROR, "error message")

    def test_critical_function(self):
        """Test critical convenience function."""
        with patch("ipsdk.logging.logging.getLogger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            ipsdk_logging.critical("critical message")
            mock_logger.log.assert_called_once_with(
                logging.CRITICAL, "critical message"
            )


class TestTraceFunction:
    """Test the trace logging function."""

    def test_trace_function_with_callable(self):
        """Test trace function logs function name."""
        with patch("ipsdk.logging.log") as mock_log:

            def test_func():
                pass

            ipsdk_logging.trace(test_func)
            mock_log.assert_called_once_with(logging.TRACE, "test_func")

    def test_trace_function_with_different_functions(self):
        """Test trace function with different function types."""
        with patch("ipsdk.logging.log") as mock_log:

            def regular_func():
                pass

            class TestClass:
                def method(self):
                    pass

                @staticmethod
                def static_method():
                    pass

            test_cases = [
                (regular_func, "regular_func"),
                (TestClass.method, "method"),
                (TestClass.static_method, "static_method"),
            ]

            for func, expected_msg in test_cases:
                mock_log.reset_mock()
                ipsdk_logging.trace(func)
                mock_log.assert_called_once_with(logging.TRACE, expected_msg)


class TestExceptionFunction:
    """Test the exception logging function."""

    def test_exception_function_with_exception(self):
        """Test exception function logs exception with full traceback."""
        with patch("ipsdk.logging.log") as mock_log:
            test_exception = ValueError("test error")
            ipsdk_logging.exception(test_exception)
            # Verify it was called once with ERROR level
            assert mock_log.call_count == 1
            call_args = mock_log.call_args
            assert call_args[0][0] == logging.ERROR
            # Verify the logged message contains the exception type and message
            logged_message = call_args[0][1]
            assert "ValueError: test error" in logged_message

    def test_exception_function_with_different_exceptions(self):
        """Test exception function with different exception types and tracebacks."""
        with patch("ipsdk.logging.logging.getLogger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            exceptions_to_test = [
                (ValueError("value error"), "ValueError: value error"),
                (TypeError("type error"), "TypeError: type error"),
                (RuntimeError("runtime error"), "RuntimeError: runtime error"),
                (KeyError("key error"), "KeyError: 'key error'"),
            ]

            for exc, expected_message_part in exceptions_to_test:
                mock_logger.log.reset_mock()
                ipsdk_logging.exception(exc)
                # Verify it was called with ERROR level
                assert mock_logger.log.call_count == 1
                call_args = mock_logger.log.call_args
                assert call_args[0][0] == logging.ERROR
                # Verify the logged message contains the exception type and message
                logged_message = call_args[0][1]
                assert expected_message_part in logged_message


class TestFatalFunction:
    """Test the fatal logging function."""

    def test_fatal_function_logs_and_exits(self):
        """Test that fatal function logs message and exits."""
        with patch("ipsdk.logging.log") as mock_log, patch(
            "builtins.print"
        ) as mock_print, patch("sys.exit") as mock_exit:
            ipsdk_logging.fatal("fatal error")

            mock_log.assert_called_once_with(ipsdk_logging.FATAL, "fatal error")
            mock_print.assert_called_once_with("ERROR: fatal error")
            mock_exit.assert_called_once_with(1)

    def test_fatal_function_different_messages(self):
        """Test fatal function with different messages."""
        messages = ["critical failure", "system error", "cannot continue"]

        for message in messages:
            with patch("ipsdk.logging.log") as mock_log, patch(
                "builtins.print"
            ) as mock_print, patch("sys.exit") as mock_exit:
                ipsdk_logging.fatal(message)

                mock_log.assert_called_once_with(ipsdk_logging.FATAL, message)
                mock_print.assert_called_once_with(f"ERROR: {message}")
                mock_exit.assert_called_once_with(1)


class TestGetLogger:
    """Test the get_logger function."""

    def test_get_logger_returns_correct_logger(self):
        """Test get_logger returns the correct logger instance."""
        with patch("ipsdk.logging.logging.getLogger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            result = ipsdk_logging.get_logger()

            mock_get_logger.assert_called_once_with(metadata.name)
            assert result == mock_logger

    def test_get_logger_actual_logger(self):
        """Test get_logger returns actual Logger instance."""
        logger = ipsdk_logging.get_logger()
        assert isinstance(logger, logging.Logger)
        assert logger.name == metadata.name


class TestGetLoggersFunction:
    """Test the _get_loggers function."""

    def test_get_loggers_returns_set(self):
        """Test _get_loggers returns a set of loggers."""
        loggers = ipsdk_logging._get_loggers()
        assert isinstance(loggers, set)

    def test_get_loggers_includes_ipsdk_logger(self):
        """Test _get_loggers includes ipsdk logger."""
        # Ensure logger exists
        _ = logging.getLogger(metadata.name)
        loggers = ipsdk_logging._get_loggers()
        logger_names = {logger.name for logger in loggers}
        assert metadata.name in logger_names

    def test_get_loggers_includes_httpx_loggers(self):
        """Test _get_loggers includes httpx loggers when they exist."""
        # Create a test httpx logger
        logging.getLogger("httpx.test")

        loggers = ipsdk_logging._get_loggers()
        logger_names = {logger.name for logger in loggers}

        assert "httpx.test" in logger_names


class TestSetLevel:
    """Test the set_level function."""

    def test_set_level_basic(self):
        """Test set_level with basic parameters."""
        with patch("ipsdk.logging.get_logger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            ipsdk_logging.set_level(logging.INFO)

            mock_logger.setLevel.assert_called_once_with(logging.INFO)
            assert mock_logger.propagate is False
            assert mock_logger.log.call_count == 2  # Two log calls made

    def test_set_level_with_propagate(self):
        """Test set_level with propagate parameter."""
        with patch("ipsdk.logging.get_logger") as mock_get_logger, patch(
            "ipsdk.logging._get_loggers"
        ) as mock_get_loggers:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            mock_other_logger = Mock()
            mock_get_loggers.return_value = [mock_logger, mock_other_logger]

            ipsdk_logging.set_level(logging.DEBUG, propagate=True)

            mock_logger.setLevel.assert_called_with(logging.DEBUG)
            mock_other_logger.setLevel.assert_called_once_with(logging.DEBUG)
            assert mock_logger.propagate is False

    def test_set_level_different_levels(self):
        """Test set_level with different logging levels."""
        levels = [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
            ipsdk_logging.FATAL,
            ipsdk_logging.NONE,
        ]

        for level in levels:
            with patch("ipsdk.logging.get_logger") as mock_get_logger:
                mock_logger = Mock()
                mock_get_logger.return_value = mock_logger

                ipsdk_logging.set_level(level)

                mock_logger.setLevel.assert_called_once_with(level)

    def test_set_level_with_none_string(self):
        """Test set_level with 'NONE' string converts to NONE constant."""
        with patch("ipsdk.logging.get_logger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            ipsdk_logging.set_level("NONE")

            mock_logger.setLevel.assert_called_once_with(ipsdk_logging.NONE)


class TestSensitiveDataFiltering:
    """Test sensitive data filtering functions."""

    def test_enable_sensitive_data_filtering(self):
        """Test enable_sensitive_data_filtering sets flag."""
        ipsdk_logging.enable_sensitive_data_filtering()
        assert ipsdk_logging.is_sensitive_data_filtering_enabled() is True

    def test_disable_sensitive_data_filtering(self):
        """Test disable_sensitive_data_filtering unsets flag."""
        ipsdk_logging.enable_sensitive_data_filtering()
        ipsdk_logging.disable_sensitive_data_filtering()
        assert ipsdk_logging.is_sensitive_data_filtering_enabled() is False

    def test_is_sensitive_data_filtering_enabled_initial_state(self):
        """Test initial state of sensitive data filtering."""
        # Reset to initial state
        ipsdk_logging.disable_sensitive_data_filtering()
        result = ipsdk_logging.is_sensitive_data_filtering_enabled()
        assert isinstance(result, bool)

    def test_configure_sensitive_data_patterns(self):
        """Test configure_sensitive_data_patterns calls heuristics."""
        with patch("ipsdk.heuristics.configure_scanner") as mock_configure:
            custom_patterns = {"test": r"test_pattern"}
            ipsdk_logging.configure_sensitive_data_patterns(custom_patterns)
            mock_configure.assert_called_once_with(custom_patterns)

    def test_configure_sensitive_data_patterns_with_none(self):
        """Test configure_sensitive_data_patterns with None."""
        with patch("ipsdk.heuristics.configure_scanner") as mock_configure:
            ipsdk_logging.configure_sensitive_data_patterns(None)
            mock_configure.assert_called_once_with(None)

    def test_get_sensitive_data_patterns(self):
        """Test get_sensitive_data_patterns returns list."""
        with patch("ipsdk.heuristics.get_scanner") as mock_get_scanner:
            mock_scanner = Mock()
            mock_scanner.list_patterns.return_value = ["api_key", "password"]
            mock_get_scanner.return_value = mock_scanner

            result = ipsdk_logging.get_sensitive_data_patterns()

            assert result == ["api_key", "password"]
            mock_scanner.list_patterns.assert_called_once()

    def test_add_sensitive_data_pattern(self):
        """Test add_sensitive_data_pattern adds pattern to scanner."""
        with patch("ipsdk.heuristics.get_scanner") as mock_get_scanner:
            mock_scanner = Mock()
            mock_get_scanner.return_value = mock_scanner

            ipsdk_logging.add_sensitive_data_pattern("test_pattern", r"\d{4}-\d{4}")

            mock_scanner.add_pattern.assert_called_once_with(
                "test_pattern", r"\d{4}-\d{4}"
            )

    def test_remove_sensitive_data_pattern(self):
        """Test remove_sensitive_data_pattern removes pattern from scanner."""
        with patch("ipsdk.heuristics.get_scanner") as mock_get_scanner:
            mock_scanner = Mock()
            mock_scanner.remove_pattern.return_value = True
            mock_get_scanner.return_value = mock_scanner

            result = ipsdk_logging.remove_sensitive_data_pattern("test_pattern")

            assert result is True
            mock_scanner.remove_pattern.assert_called_once_with("test_pattern")

    def test_remove_sensitive_data_pattern_not_found(self):
        """Test remove_sensitive_data_pattern returns False when pattern not found."""
        with patch("ipsdk.heuristics.get_scanner") as mock_get_scanner:
            mock_scanner = Mock()
            mock_scanner.remove_pattern.return_value = False
            mock_get_scanner.return_value = mock_scanner

            result = ipsdk_logging.remove_sensitive_data_pattern("nonexistent")

            assert result is False

    def test_log_function_with_filtering_enabled(self):
        """Test log function filters sensitive data when filtering is enabled."""
        # Reset and enable filtering
        ipsdk_logging.disable_sensitive_data_filtering()
        heuristics.Scanner.reset_singleton()
        ipsdk_logging.enable_sensitive_data_filtering()

        with patch("ipsdk.logging.logging.getLogger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            # Log message with sensitive data (api_key requires 16+ chars)
            ipsdk_logging.log(logging.INFO, "api_key=secret1234567890abcd")

            # Verify the logged message has been redacted
            mock_logger.log.assert_called_once()
            call_args = mock_logger.log.call_args[0]
            assert call_args[0] == logging.INFO
            # The message should be redacted
            assert "secret1234567890abcd" not in call_args[1]
            assert "[REDACTED_API_KEY]" in call_args[1]

        # Cleanup
        ipsdk_logging.disable_sensitive_data_filtering()

    def test_log_function_with_filtering_disabled(self):
        """Test log function does not filter when filtering is disabled."""
        # Ensure filtering is disabled
        ipsdk_logging.disable_sensitive_data_filtering()

        with patch("ipsdk.logging.logging.getLogger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            # Log message with sensitive data
            ipsdk_logging.log(logging.INFO, "api_key=secret1234567890abcd")

            # Verify the logged message has NOT been redacted
            mock_logger.log.assert_called_once()
            call_args = mock_logger.log.call_args[0]
            assert call_args[0] == logging.INFO
            # The message should NOT be redacted
            assert "secret1234567890abcd" in call_args[1]
            assert "[REDACTED_API_KEY]" not in call_args[1]

    def test_convenience_functions_with_filtering(self):
        """Test convenience functions use filtering when enabled."""
        # Reset and enable filtering
        ipsdk_logging.disable_sensitive_data_filtering()
        heuristics.Scanner.reset_singleton()
        ipsdk_logging.enable_sensitive_data_filtering()

        with patch("ipsdk.logging.logging.getLogger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            # Test multiple convenience functions with sensitive data
            test_cases = [
                (ipsdk_logging.debug, logging.DEBUG, "Debug: password=testpass"),
                (ipsdk_logging.info, logging.INFO, "Info: api_key=key1234567890abcdef"),
                (
                    ipsdk_logging.warning,
                    logging.WARNING,
                    "Warning: secret=sec1234567890abcdef",
                ),
            ]

            for func, level, message in test_cases:
                mock_logger.reset_mock()
                func(message)

                mock_logger.log.assert_called_once()
                call_args = mock_logger.log.call_args[0]
                assert call_args[0] == level
                # The message should be redacted
                assert (
                    "testpass" not in call_args[1]
                    or "[REDACTED_PASSWORD]" in call_args[1]
                )

        # Cleanup
        ipsdk_logging.disable_sensitive_data_filtering()

    def test_log_function_filters_multiple_patterns(self):
        """Test log function filters multiple sensitive patterns in one message."""
        # Reset and enable filtering
        ipsdk_logging.disable_sensitive_data_filtering()
        heuristics.Scanner.reset_singleton()
        ipsdk_logging.enable_sensitive_data_filtering()

        with patch("ipsdk.logging.logging.getLogger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            # Log message with multiple sensitive data types
            message = "Credentials: api_key=key1234567890abcdef password=testpass"
            ipsdk_logging.log(logging.INFO, message)

            # Verify both patterns are redacted
            mock_logger.log.assert_called_once()
            call_args = mock_logger.log.call_args[0]
            logged_message = call_args[1]

            assert "key1234567890abcdef" not in logged_message
            assert "testpass" not in logged_message
            assert "[REDACTED_" in logged_message

        # Cleanup
        ipsdk_logging.disable_sensitive_data_filtering()


class TestInitialize:
    """Test the initialize function."""

    def test_initialize_resets_handlers(self):
        """Test initialize removes existing handlers and adds stderr handler."""
        with patch("ipsdk.logging._get_loggers") as mock_get_loggers:
            # Create a mock logger with existing handlers
            mock_logger = Mock()
            mock_handler1 = Mock()
            mock_handler2 = Mock()
            mock_logger.handlers = [mock_handler1, mock_handler2]
            mock_get_loggers.return_value = [mock_logger]

            with patch("ipsdk.logging.logging.StreamHandler") as mock_stream_handler:
                mock_new_handler = Mock()
                mock_stream_handler.return_value = mock_new_handler

                ipsdk_logging.initialize()

                # Verify old handlers were removed and closed
                mock_logger.removeHandler.assert_any_call(mock_handler1)
                mock_logger.removeHandler.assert_any_call(mock_handler2)
                mock_handler1.close.assert_called_once()
                mock_handler2.close.assert_called_once()

                # Verify new handler was added
                mock_stream_handler.assert_called_once_with(sys.stderr)
                mock_logger.addHandler.assert_called_once_with(mock_new_handler)
                mock_logger.setLevel.assert_called_once_with(ipsdk_logging.NONE)
                assert mock_logger.propagate is False

    def test_initialize_sets_correct_level(self):
        """Test initialize sets logger level to NONE."""
        with patch("ipsdk.logging._get_loggers") as mock_get_loggers:
            mock_logger = Mock()
            mock_logger.handlers = []
            mock_get_loggers.return_value = [mock_logger]

            with patch("ipsdk.logging.logging.StreamHandler"):
                ipsdk_logging.initialize()
                mock_logger.setLevel.assert_called_once_with(ipsdk_logging.NONE)

    def test_initialize_formats_handler(self):
        """Test initialize applies correct formatter to handler."""
        with patch("ipsdk.logging._get_loggers") as mock_get_loggers:
            mock_logger = Mock()
            mock_logger.handlers = []
            mock_get_loggers.return_value = [mock_logger]

            with patch("ipsdk.logging.logging.StreamHandler") as mock_stream_handler:
                mock_handler = Mock()
                mock_stream_handler.return_value = mock_handler

                ipsdk_logging.initialize()

                # Check that setFormatter was called
                mock_handler.setFormatter.assert_called_once()
                # Get the formatter that was set
                formatter_call = mock_handler.setFormatter.call_args[0][0]
                assert isinstance(formatter_call, logging.Formatter)


class TestIntegration:
    """Integration tests using actual logging functionality."""

    def test_actual_logging_output(self, caplog):
        """Test actual logging output using caplog fixture."""
        # Set up actual logging
        logger = ipsdk_logging.get_logger()
        logger.setLevel(logging.DEBUG)
        logger.propagate = True  # Enable propagation so caplog can capture messages

        with caplog.at_level(logging.DEBUG, logger=metadata.name):
            # Test different log levels
            ipsdk_logging.debug("debug message")
            ipsdk_logging.info("info message")
            ipsdk_logging.warning("warning message")
            ipsdk_logging.error("error message")
            ipsdk_logging.critical("critical message")

        # Check that messages were logged
        messages = [record.getMessage() for record in caplog.records]
        assert any("debug message" in msg for msg in messages)
        assert any("info message" in msg for msg in messages)
        assert any("warning message" in msg for msg in messages)
        assert any("error message" in msg for msg in messages)
        assert any("critical message" in msg for msg in messages)

    def test_trace_function_integration(self, caplog):
        """Test trace function with actual logging."""
        logger = ipsdk_logging.get_logger()
        logger.setLevel(logging.TRACE)
        logger.propagate = True

        def test_function():
            """Test function for tracing."""

        with caplog.at_level(logging.TRACE, logger=metadata.name):
            ipsdk_logging.trace(test_function)

        messages = [record.getMessage() for record in caplog.records]
        assert any("test_function" in msg for msg in messages)


class TestFormatString:
    """Test the logging message format string."""

    def test_logging_message_format_exists(self):
        """Test that logging_message_format is properly defined."""
        assert hasattr(ipsdk_logging, "logging_message_format")
        assert isinstance(ipsdk_logging.logging_message_format, str)
        assert "%(asctime)s" in ipsdk_logging.logging_message_format
        assert "%(name)s" in ipsdk_logging.logging_message_format
        assert "%(levelname)s" in ipsdk_logging.logging_message_format
        assert "%(message)s" in ipsdk_logging.logging_message_format
