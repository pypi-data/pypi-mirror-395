"""Advanced tests for core functionality"""

import pytest
from unittest.mock import Mock, patch
import requests
from pathlib import Path

from dumpconfluence.core import ConfluenceBackup
from dumpconfluence.exceptions import (
    AuthenticationError,
    NetworkError,
    ValidationError,
)


class TestConfluenceBackupInitialization:
    """Test ConfluenceBackup initialization and validation"""

    def test_valid_initialization(self, temp_dir):
        """Test successful initialization with valid parameters"""
        backup = ConfluenceBackup(
            "https://test.atlassian.net",
            "test@example.com",
            "test-token",
            str(temp_dir)
        )
        assert backup.confluence_url == "https://test.atlassian.net"
        assert backup.email == "test@example.com"
        assert backup.api_token == "test-token"
        assert backup.output_dir == temp_dir

    def test_empty_confluence_url(self, temp_dir):
        """Test ValidationError for empty confluence URL"""
        with pytest.raises(ValidationError, match="Confluence URL cannot be empty"):
            ConfluenceBackup("", "test@example.com", "test-token", str(temp_dir))

    def test_invalid_url_format(self, temp_dir):
        """Test ValidationError for invalid URL format"""
        with pytest.raises(ValidationError, match="Confluence URL must start with"):
            ConfluenceBackup("invalid-url", "test@example.com", "test-token", str(temp_dir))

    def test_empty_email(self, temp_dir):
        """Test ValidationError for empty email"""
        with pytest.raises(ValidationError, match="Email cannot be empty"):
            ConfluenceBackup("https://test.atlassian.net", "", "test-token", str(temp_dir))

    def test_invalid_email_format(self, temp_dir):
        """Test ValidationError for invalid email format"""
        with pytest.raises(ValidationError, match="Invalid email format"):
            ConfluenceBackup("https://test.atlassian.net", "invalid-email", "test-token", str(temp_dir))

    def test_empty_api_token(self, temp_dir):
        """Test ValidationError for empty API token"""
        with pytest.raises(ValidationError, match="API token cannot be empty"):
            ConfluenceBackup("https://test.atlassian.net", "test@example.com", "", str(temp_dir))

    def test_output_directory_creation(self, temp_dir):
        """Test that output directory is created if it doesn't exist"""
        new_dir = temp_dir / "new_subdir"
        backup = ConfluenceBackup(
            "https://test.atlassian.net",
            "test@example.com",
            "test-token",
            str(new_dir)
        )
        assert new_dir.exists()


class TestPageIdExtraction:
    """Test page ID extraction from URLs"""

    def test_valid_confluence_url(self):
        """Test extracting page ID from valid Confluence URL"""
        url = "https://company.atlassian.net/wiki/spaces/SPACE/pages/123456/Page+Title"
        assert ConfluenceBackup.extract_page_id(url) == "123456"

    def test_url_with_trailing_slash(self):
        """Test URL with trailing slash"""
        url = "https://company.atlassian.net/wiki/spaces/SPACE/pages/789012/Page+Title/"
        assert ConfluenceBackup.extract_page_id(url) == "789012"

    def test_url_without_pages(self):
        """Test URL without pages section"""
        url = "https://company.atlassian.net/wiki/spaces/SPACE/"
        assert ConfluenceBackup.extract_page_id(url) is None

    def test_invalid_page_id_non_numeric(self):
        """Test URL with non-numeric page ID"""
        url = "https://company.atlassian.net/wiki/spaces/SPACE/pages/invalid/Page+Title"
        assert ConfluenceBackup.extract_page_id(url) is None

    def test_empty_url(self):
        """Test empty URL"""
        assert ConfluenceBackup.extract_page_id("") is None
        assert ConfluenceBackup.extract_page_id(None) is None

    def test_malformed_url(self):
        """Test malformed URL"""
        assert ConfluenceBackup.extract_page_id("not-a-url") is None


class TestFilenameSanitization:
    """Test filename sanitization"""

    def test_normal_filename(self):
        """Test normal filename without special characters"""
        assert ConfluenceBackup.sanitize_filename("Normal File") == "Normal File"

    def test_invalid_characters(self):
        """Test filename with invalid characters"""
        result = ConfluenceBackup.sanitize_filename("File: With / Invalid * Chars")
        assert result == "File_ With _ Invalid _ Chars"

    def test_control_characters(self):
        """Test filename with control characters"""
        result = ConfluenceBackup.sanitize_filename("File\x00\x1fWith\x0aControl")
        assert result == "File_With_Control"

    def test_multiple_underscores(self):
        """Test that multiple consecutive underscores are collapsed"""
        result = ConfluenceBackup.sanitize_filename("File___With___Multiple")
        assert result == "File_With_Multiple"

    def test_long_filename(self):
        """Test very long filename is truncated"""
        long_name = "A" * 250
        result = ConfluenceBackup.sanitize_filename(long_name)
        assert len(result) == 200

    def test_empty_filename(self):
        """Test empty filename returns default"""
        assert ConfluenceBackup.sanitize_filename("") == "untitled"
        assert ConfluenceBackup.sanitize_filename(None) == "untitled"

    def test_only_invalid_chars(self):
        """Test filename with only invalid characters"""
        result = ConfluenceBackup.sanitize_filename("*/<>:|?")
        assert result == "untitled"


class TestAPIRequests:
    """Test API request handling"""

    def test_get_page_details_success(self, confluence_backup, mock_requests, mock_confluence_response):
        """Test successful page details retrieval"""
        mock_requests.get.return_value.json.return_value = mock_confluence_response
        mock_requests.get.return_value.status_code = 200

        result = confluence_backup.get_page_details("123456")
        assert result["id"] == "123456"
        assert result["title"] == "Test Page"

    def test_get_page_details_invalid_id(self, confluence_backup):
        """Test ValidationError for invalid page ID"""
        with pytest.raises(ValidationError, match="Invalid page ID"):
            confluence_backup.get_page_details("invalid")

        with pytest.raises(ValidationError, match="Invalid page ID"):
            confluence_backup.get_page_details("")

    def test_get_page_details_authentication_error(self, confluence_backup, mock_requests):
        """Test AuthenticationError for 401 response"""
        mock_requests.get.return_value.status_code = 401
        mock_requests.get.return_value.raise_for_status.side_effect = requests.HTTPError()

        with pytest.raises(AuthenticationError, match="Authentication failed"):
            confluence_backup.get_page_details("123456")

    def test_get_page_details_permission_error(self, confluence_backup, mock_requests):
        """Test AuthenticationError for 403 response"""
        mock_requests.get.return_value.status_code = 403
        mock_requests.get.return_value.raise_for_status.side_effect = requests.HTTPError()

        with pytest.raises(AuthenticationError, match="Access denied"):
            confluence_backup.get_page_details("123456")

    def test_get_page_details_not_found(self, confluence_backup, mock_requests):
        """Test ValidationError for 404 response"""
        mock_requests.get.return_value.status_code = 404
        mock_requests.get.return_value.raise_for_status.side_effect = requests.HTTPError()

        with pytest.raises(ValidationError, match="Page with ID '123456' not found"):
            confluence_backup.get_page_details("123456")

    def test_get_page_details_timeout(self, confluence_backup, mock_requests):
        """Test NetworkError for timeout"""
        mock_requests.get.side_effect = requests.exceptions.Timeout()

        with pytest.raises(NetworkError, match="Request timeout"):
            confluence_backup.get_page_details("123456")

    def test_get_page_details_connection_error(self, confluence_backup, mock_requests):
        """Test NetworkError for connection error"""
        mock_requests.get.side_effect = requests.exceptions.ConnectionError()

        with pytest.raises(NetworkError, match="Cannot connect"):
            confluence_backup.get_page_details("123456")

    def test_get_page_details_invalid_json(self, confluence_backup, mock_requests):
        """Test NetworkError for invalid JSON response"""
        mock_requests.get.return_value.status_code = 200
        mock_requests.get.return_value.json.side_effect = ValueError()

        with pytest.raises(NetworkError, match="Invalid response"):
            confluence_backup.get_page_details("123456")