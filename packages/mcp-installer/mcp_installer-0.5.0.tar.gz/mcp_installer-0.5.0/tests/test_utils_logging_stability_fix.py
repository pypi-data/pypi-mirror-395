"""Fixed tests for logging utility edge cases that were failing."""

import logging

from mcpi.utils.logging import get_logger, setup_logging


class TestLoggingStabilityFixes:
    """Fixed versions of failing logging tests."""

    def test_setup_logging_with_empty_format_string_fixed(self):
        """Test setup_logging handles empty format string correctly.

        Python's logging.Formatter automatically defaults empty string to '%(message)s'.
        This is standard behavior - we test the actual behavior, not incorrect expectations.
        """
        logger = setup_logging(format_string="")

        assert logger.name == "mcpi"
        assert len(logger.handlers) == 1
        # Python logging.Formatter defaults empty string to '%(message)s'
        # This is the correct behavior to test
        assert logger.handlers[0].formatter._fmt == "%(message)s"

    def test_get_logger_with_empty_name_fixed(self):
        """Test get_logger with empty name correctly.

        Empty name returns the root logger, which has name "root" in Python logging.
        """
        logger = get_logger("")

        assert isinstance(logger, logging.Logger)
        # Root logger has name "root", not empty string
        assert logger.name == "root"
        # Verify it's actually the root logger
        assert logger is logging.getLogger("")
