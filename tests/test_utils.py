import pytest
import os
import tempfile
import time
from unittest.mock import Mock, patch
from src.utils.logger import get_logger
from src.utils.http_client import SafeHTTPClient
from src.utils.cache import FileCache


def test_logger_creates_instance():
    """Test that get_logger returns a logger instance."""
    logger = get_logger("test")
    assert logger is not None
    assert logger.name == "test"


def test_logger_logs_messages(caplog):
    """Test that logger can log messages."""
    logger = get_logger("test")
    logger.info("Test message")
    assert "Test message" in caplog.text


def test_http_client_sets_user_agent():
    """Test that HTTP client sets proper user-agent."""
    client = SafeHTTPClient()
    assert "AI-Security-Intelligence" in client.headers["User-Agent"]


@patch('src.utils.http_client.requests.Session.get')
def test_http_client_fetch_with_timeout(mock_get):
    """Test that HTTP client respects timeout."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "test content"
    mock_get.return_value = mock_response

    client = SafeHTTPClient(timeout=10)
    response = client.fetch("https://example.com")

    mock_get.assert_called_once()
    assert mock_get.call_args[1]['timeout'] == 10
    assert response.text == "test content"


def test_cache_stores_and_retrieves():
    """Test that cache can store and retrieve values."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = FileCache(cache_dir=tmpdir, ttl_seconds=60)

        cache.set("test_key", {"data": "test value"})
        result = cache.get("test_key")

        assert result == {"data": "test value"}


def test_cache_returns_none_for_missing_key():
    """Test that cache returns None for missing keys."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = FileCache(cache_dir=tmpdir, ttl_seconds=60)

        result = cache.get("nonexistent")

        assert result is None


def test_cache_expires_old_entries():
    """Test that cache expires entries after TTL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = FileCache(cache_dir=tmpdir, ttl_seconds=1)

        cache.set("test_key", "test value")
        time.sleep(2)  # Wait for expiration
        result = cache.get("test_key")

        assert result is None
