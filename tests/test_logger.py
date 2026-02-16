"""
Tests for the logger utility module.
"""
import logging
import pytest
from src.utils.logger import get_logger


class TestLogger:
    """Test suite for the get_logger function."""

    def test_logger_creates_instance(self):
        """Test that get_logger creates a logger instance."""
        logger = get_logger("test_module")
        assert logger is not None
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_module"

    def test_logger_logs_messages(self, caplog):
        """Test that logger can log messages at various levels."""
        logger = get_logger("test_log_messages", "DEBUG")

        with caplog.at_level(logging.DEBUG):
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")

        # Verify all messages were logged
        assert "Debug message" in caplog.text
        assert "Info message" in caplog.text
        assert "Warning message" in caplog.text
        assert "Error message" in caplog.text
