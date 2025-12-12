"""Tests for configuration management"""

import pytest
import tempfile
import json
from pathlib import Path
from dumpconfluence.config import ConfigManager


def test_config_manager_initialization(monkeypatch, tmp_path):
    """Test ConfigManager creates config directory"""

    # Override config directory to temp path
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

    config = ConfigManager()

    # Check config directory was created
    assert (tmp_path / "dumpconfluence").exists()
    assert config.config_file.exists()


def test_save_and_load_profile(monkeypatch, tmp_path):
    """Test saving and loading profiles"""

    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    config = ConfigManager()

    # Save a profile
    config.save_profile("test", "https://test.atlassian.net", "test@email.com", "test-token")

    # Load the profile
    profile = config.load_profile("test")
    assert profile is not None
    assert profile["url"] == "https://test.atlassian.net"
    assert profile["email"] == "test@email.com"
    assert profile["token"] == "test-token"


def test_list_profiles(monkeypatch, tmp_path):
    """Test listing all profiles"""

    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    config = ConfigManager()

    # Initially empty
    assert config.list_profiles() == []

    # Add profiles
    config.save_profile("work", "https://work.atlassian.net", "work@email.com", "work-token")
    config.save_profile("personal", "https://personal.atlassian.net", "personal@email.com", "personal-token")

    # Check list
    profiles = config.list_profiles()
    assert len(profiles) == 2
    assert "work" in profiles
    assert "personal" in profiles


def test_remove_profile(monkeypatch, tmp_path):
    """Test removing a profile"""

    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    config = ConfigManager()

    # Add and remove
    config.save_profile("temp", "https://temp.atlassian.net", "temp@email.com", "temp-token")
    assert "temp" in config.list_profiles()

    result = config.remove_profile("temp")
    assert result is True
    assert "temp" not in config.list_profiles()

    # Try removing non-existent
    result = config.remove_profile("nonexistent")
    assert result is False