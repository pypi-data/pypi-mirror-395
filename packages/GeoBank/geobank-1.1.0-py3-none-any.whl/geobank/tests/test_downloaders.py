"""
Tests for the downloaders module.
"""

import socket
from unittest.mock import MagicMock, patch
from urllib.error import URLError

import pytest

from geobank.downloaders import download_with_retry


class TestDownloadWithRetry:
    """Tests for download_with_retry function."""

    @patch("geobank.downloaders.urllib.request.urlopen")
    def test_successful_download(self, mock_urlopen):
        """Test successful download on first attempt."""
        mock_response = MagicMock()
        mock_response.read.return_value = b"test content"
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        result = download_with_retry("http://example.com/test.txt")

        assert result == b"test content"
        assert mock_urlopen.call_count == 1

    @patch("geobank.downloaders.time.sleep")
    @patch("geobank.downloaders.urllib.request.urlopen")
    def test_retry_on_url_error(self, mock_urlopen, mock_sleep):
        """Test retry mechanism on URLError."""
        mock_response = MagicMock()
        mock_response.read.return_value = b"success"
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)

        # Fail twice, succeed on third attempt
        mock_urlopen.side_effect = [
            URLError("Connection refused"),
            URLError("Timeout"),
            mock_response,
        ]

        result = download_with_retry("http://example.com/test.txt")

        assert result == b"success"
        assert mock_urlopen.call_count == 3
        assert mock_sleep.call_count == 2

    @patch("geobank.downloaders.time.sleep")
    @patch("geobank.downloaders.urllib.request.urlopen")
    def test_retry_on_socket_timeout(self, mock_urlopen, mock_sleep):
        """Test retry mechanism on socket timeout."""
        mock_response = MagicMock()
        mock_response.read.return_value = b"success"
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)

        mock_urlopen.side_effect = [
            socket.timeout("timed out"),
            mock_response,
        ]

        result = download_with_retry("http://example.com/test.txt")

        assert result == b"success"
        assert mock_urlopen.call_count == 2

    @patch("geobank.downloaders.time.sleep")
    @patch("geobank.downloaders.urllib.request.urlopen")
    def test_raises_after_max_retries(self, mock_urlopen, mock_sleep):
        """Test that exception is raised after all retries are exhausted."""
        mock_urlopen.side_effect = URLError("Connection refused")

        with pytest.raises(URLError):
            download_with_retry("http://example.com/test.txt", retries=3)

        assert mock_urlopen.call_count == 3
        assert mock_sleep.call_count == 2

    @patch("geobank.downloaders.urllib.request.urlopen")
    def test_custom_timeout(self, mock_urlopen):
        """Test that custom timeout is passed to urlopen."""
        mock_response = MagicMock()
        mock_response.read.return_value = b"test"
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        download_with_retry("http://example.com/test.txt", timeout=30)

        mock_urlopen.assert_called_once_with("http://example.com/test.txt", timeout=30)
