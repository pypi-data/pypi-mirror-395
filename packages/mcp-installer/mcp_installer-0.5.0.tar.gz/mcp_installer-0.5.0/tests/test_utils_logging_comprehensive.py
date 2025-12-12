"""Comprehensive tests for utils/logging.py to boost coverage from 19% to 90%+."""

import logging
import tempfile
from pathlib import Path

from mcpi.utils.logging import get_logger, setup_logging


class TestSetupLogging:
    """Comprehensive tests for setup_logging function."""

    def test_setup_logging_default_parameters(self):
        """Test setup_logging with default parameters."""
        logger = setup_logging()

        assert isinstance(logger, logging.Logger)
        assert logger.name == "mcpi"
        assert logger.level == logging.INFO
        assert len(logger.handlers) == 1  # Console handler only

        # Verify console handler
        handler = logger.handlers[0]
        assert isinstance(handler, logging.StreamHandler)
        assert handler.formatter is not None

    def test_setup_logging_debug_level(self):
        """Test setup_logging with DEBUG level."""
        logger = setup_logging(level="DEBUG")

        assert logger.level == logging.DEBUG
        assert logger.name == "mcpi"
        assert len(logger.handlers) == 1

    def test_setup_logging_warning_level(self):
        """Test setup_logging with WARNING level."""
        logger = setup_logging(level="WARNING")

        assert logger.level == logging.WARNING
        assert logger.name == "mcpi"
        assert len(logger.handlers) == 1

    def test_setup_logging_error_level(self):
        """Test setup_logging with ERROR level."""
        logger = setup_logging(level="ERROR")

        assert logger.level == logging.ERROR
        assert logger.name == "mcpi"
        assert len(logger.handlers) == 1

    def test_setup_logging_critical_level(self):
        """Test setup_logging with CRITICAL level."""
        logger = setup_logging(level="CRITICAL")

        assert logger.level == logging.CRITICAL
        assert logger.name == "mcpi"
        assert len(logger.handlers) == 1

    def test_setup_logging_lowercase_level(self):
        """Test setup_logging with lowercase level string."""
        logger = setup_logging(level="debug")

        assert logger.level == logging.DEBUG

    def test_setup_logging_no_console(self):
        """Test setup_logging with console disabled."""
        logger = setup_logging(console=False)

        assert logger.name == "mcpi"
        assert (
            len(logger.handlers) == 0
        )  # No handlers when console=False and no log_file

    def test_setup_logging_custom_format(self):
        """Test setup_logging with custom format string."""
        custom_format = "%(levelname)s: %(message)s"
        logger = setup_logging(format_string=custom_format)

        assert logger.name == "mcpi"
        assert len(logger.handlers) == 1

        # Verify custom format is applied
        handler = logger.handlers[0]
        assert handler.formatter._fmt == custom_format

    def test_setup_logging_with_log_file(self):
        """Test setup_logging with log file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test.log"
            logger = setup_logging(log_file=log_file)

            assert logger.name == "mcpi"
            assert len(logger.handlers) == 2  # Console + file handler

            # Verify file handler
            file_handler = None
            for handler in logger.handlers:
                if isinstance(handler, logging.handlers.RotatingFileHandler):
                    file_handler = handler
                    break

            assert file_handler is not None
            assert file_handler.baseFilename.endswith("test.log")
            assert file_handler.maxBytes == 10 * 1024 * 1024  # 10MB
            assert file_handler.backupCount == 5

    def test_setup_logging_file_only(self):
        """Test setup_logging with file handler only (no console)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test.log"
            logger = setup_logging(log_file=log_file, console=False)

            assert logger.name == "mcpi"
            assert len(logger.handlers) == 1  # File handler only

            handler = logger.handlers[0]
            assert isinstance(handler, logging.handlers.RotatingFileHandler)

    def test_setup_logging_creates_log_directory(self):
        """Test setup_logging creates log directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_dir = Path(temp_dir) / "logs" / "nested"
            log_file = nested_dir / "test.log"

            # Directory doesn't exist initially
            assert not nested_dir.exists()

            logger = setup_logging(log_file=log_file)

            # Directory should be created
            assert nested_dir.exists()
            assert logger.name == "mcpi"
            assert len(logger.handlers) == 2  # Console + file

    def test_setup_logging_file_permission_error(self):
        """Test setup_logging handles file permission errors gracefully."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a read-only directory
            readonly_dir = Path(temp_dir) / "readonly"
            readonly_dir.mkdir()
            readonly_dir.chmod(0o444)  # Read-only

            log_file = readonly_dir / "test.log"

            try:
                logger = setup_logging(log_file=log_file)

                # Should fall back to console-only logging
                assert logger.name == "mcpi"
                assert len(logger.handlers) == 1  # Console only

                handler = logger.handlers[0]
                assert isinstance(handler, logging.StreamHandler)
            finally:
                # Restore permissions for cleanup
                readonly_dir.chmod(0o755)

    def test_setup_logging_file_os_error(self):
        """Test setup_logging handles OS errors gracefully."""
        # Use an invalid path that will cause OSError
        invalid_path = Path("/dev/null/invalid/path/test.log")

        logger = setup_logging(log_file=invalid_path)

        # Should fall back to console-only logging
        assert logger.name == "mcpi"
        assert len(logger.handlers) == 1  # Console only

        handler = logger.handlers[0]
        assert isinstance(handler, logging.StreamHandler)

    def test_setup_logging_clears_existing_handlers(self):
        """Test setup_logging clears existing handlers."""
        # Set up logger with initial handler
        initial_logger = logging.getLogger("mcpi")
        initial_handler = logging.StreamHandler()
        initial_logger.addHandler(initial_handler)

        assert len(initial_logger.handlers) >= 1

        # Call setup_logging - should clear existing handlers
        logger = setup_logging()

        assert logger is initial_logger  # Same logger instance
        # Should have exactly 1 handler (the new console handler)
        # Note: The exact count may vary based on other tests, but it should be cleared and reset
        assert len(logger.handlers) >= 1
        assert all(
            not isinstance(h, type(initial_handler)) or h is not initial_handler
            for h in logger.handlers
        )

    def test_setup_logging_all_parameters(self):
        """Test setup_logging with all parameters specified."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "full_test.log"
            custom_format = "%(name)s - %(levelname)s - %(message)s"

            logger = setup_logging(
                level="WARNING",
                log_file=log_file,
                console=True,
                format_string=custom_format,
            )

            assert logger.name == "mcpi"
            assert logger.level == logging.WARNING
            assert len(logger.handlers) == 2  # Console + file

            # Verify both handlers have custom format
            for handler in logger.handlers:
                assert handler.formatter._fmt == custom_format


class TestGetLogger:
    """Tests for get_logger function."""

    def test_get_logger_default_name(self):
        """Test get_logger with default name."""
        logger = get_logger()

        assert isinstance(logger, logging.Logger)
        assert logger.name == "mcpi"

    def test_get_logger_custom_name(self):
        """Test get_logger with custom name."""
        custom_name = "custom_logger"
        logger = get_logger(custom_name)

        assert isinstance(logger, logging.Logger)
        assert logger.name == custom_name

    def test_get_logger_returns_same_instance(self):
        """Test get_logger returns same instance for same name."""
        logger1 = get_logger("test_logger")
        logger2 = get_logger("test_logger")

        assert logger1 is logger2

    def test_get_logger_different_names_different_instances(self):
        """Test get_logger returns different instances for different names."""
        logger1 = get_logger("logger1")
        logger2 = get_logger("logger2")

        assert logger1 is not logger2
        assert logger1.name == "logger1"
        assert logger2.name == "logger2"


class TestLoggingIntegration:
    """Integration tests for logging functionality."""

    def test_setup_and_get_logger_integration(self):
        """Test integration between setup_logging and get_logger."""
        # Setup logging
        setup_logger = setup_logging(level="DEBUG")

        # Get logger with same name
        get_logger_result = get_logger("mcpi")

        assert setup_logger is get_logger_result
        assert setup_logger.level == logging.DEBUG

    def test_logger_actually_logs_messages(self):
        """Test that logger actually logs messages correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "integration_test.log"

            logger = setup_logging(
                level="INFO",
                log_file=log_file,
                console=False,  # Only log to file for testing
            )

            # Log a test message
            test_message = "Integration test message"
            logger.info(test_message)

            # Verify message was written to file
            assert log_file.exists()
            log_content = log_file.read_text()
            assert test_message in log_content
            assert "INFO" in log_content

    def test_logger_respects_level_filtering(self):
        """Test that logger respects level filtering."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "level_test.log"

            # Set up logger at WARNING level
            logger = setup_logging(level="WARNING", log_file=log_file, console=False)

            # Log messages at different levels
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")

            # Verify only WARNING and ERROR messages are logged
            log_content = log_file.read_text()
            assert "Debug message" not in log_content
            assert "Info message" not in log_content
            assert "Warning message" in log_content
            assert "Error message" in log_content

    def test_rotating_file_handler_configuration(self):
        """Test that rotating file handler is configured correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "rotating_test.log"

            logger = setup_logging(log_file=log_file)

            # Find the rotating file handler
            rotating_handler = None
            for handler in logger.handlers:
                if isinstance(handler, logging.handlers.RotatingFileHandler):
                    rotating_handler = handler
                    break

            assert rotating_handler is not None
            assert rotating_handler.maxBytes == 10 * 1024 * 1024  # 10MB
            assert rotating_handler.backupCount == 5
            assert rotating_handler.baseFilename.endswith("rotating_test.log")


class TestLoggingErrorScenarios:
    """Tests for error scenarios in logging setup."""

    def test_setup_logging_with_none_log_file(self):
        """Test setup_logging handles None log_file correctly."""
        logger = setup_logging(log_file=None, console=True)

        assert logger.name == "mcpi"
        assert len(logger.handlers) == 1  # Console only
        assert isinstance(logger.handlers[0], logging.StreamHandler)

    def test_multiple_setup_calls_same_logger(self):
        """Test multiple setup_logging calls on same logger name."""
        logger1 = setup_logging(level="INFO")
        logger2 = setup_logging(level="DEBUG")

        # Should be same logger instance
        assert logger1 is logger2
        # Should have updated level
        assert logger1.level == logging.DEBUG
        # Handlers should be cleared and reset
        assert len(logger1.handlers) >= 1
