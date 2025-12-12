"""Basic tests for DumpConfluence core functionality"""

import pytest
from dumpconfluence.core import ConfluenceBackup


def test_extract_page_id():
    """Test page ID extraction from URLs"""

    # Standard Confluence URL
    url = "https://company.atlassian.net/wiki/spaces/SPACE/pages/123456/Page+Title"
    assert ConfluenceBackup.extract_page_id(url) == "123456"

    # URL with trailing slash
    url = "https://company.atlassian.net/wiki/spaces/SPACE/pages/789012/Another+Page/"
    assert ConfluenceBackup.extract_page_id(url) == "789012"

    # Invalid URL
    url = "https://company.atlassian.net/wiki/spaces/SPACE/"
    assert ConfluenceBackup.extract_page_id(url) is None


def test_sanitize_filename():
    """Test filename sanitization"""

    # Normal filename
    assert ConfluenceBackup.sanitize_filename("Normal Title") == "Normal Title"

    # Filename with invalid characters
    assert ConfluenceBackup.sanitize_filename("Title: With / Invalid * Chars") == "Title_ With _ Invalid _ Chars"

    # Very long filename (should truncate at 200 chars)
    long_name = "A" * 250
    assert len(ConfluenceBackup.sanitize_filename(long_name)) == 200