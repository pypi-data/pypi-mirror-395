"""Tests for CLI functionality"""

import pytest
from click.testing import CliRunner
from unittest.mock import patch, Mock
from pathlib import Path

from dumpconfluence.cli import cli
from dumpconfluence.exceptions import ValidationError, AuthenticationError


class TestCLIBasicCommands:
    """Test basic CLI commands"""

    def test_help_command(self):
        """Test help command shows usage"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert "DumpConfluence" in result.output

    def test_version_command(self):
        """Test version command"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert "0.1.0" in result.output


class TestBackupCommand:
    """Test backup command"""

    @patch('dumpconfluence.cli.ConfluenceBackup')
    def test_backup_success(self, mock_backup_class):
        """Test successful backup"""
        mock_backup = Mock()
        mock_backup.backup_page.return_value = "/path/to/backup"
        mock_backup_class.return_value = mock_backup

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                'backup',
                'https://test.atlassian.net/wiki/spaces/TEST/pages/123/Test',
                '--url', 'https://test.atlassian.net',
                '--email', 'test@example.com',
                '--token', 'test-token'
            ])

        assert result.exit_code == 0
        assert "Successfully backed up" in result.output
        mock_backup.backup_page.assert_called_once()

    @patch('dumpconfluence.cli.ConfluenceBackup')
    def test_backup_validation_error(self, mock_backup_class):
        """Test backup with validation error"""
        mock_backup_class.side_effect = ValidationError("Invalid URL")

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                'backup',
                'invalid-url',
                '--url', 'invalid',
                '--email', 'test@example.com',
                '--token', 'test-token'
            ])

        assert result.exit_code == 1
        assert "Validation Error" in result.output

    @patch('dumpconfluence.cli.ConfluenceBackup')
    def test_backup_authentication_error(self, mock_backup_class):
        """Test backup with authentication error"""
        mock_backup_class.side_effect = AuthenticationError("Invalid credentials")

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                'backup',
                'https://test.atlassian.net/wiki/spaces/TEST/pages/123/Test',
                '--url', 'https://test.atlassian.net',
                '--email', 'wrong@example.com',
                '--token', 'wrong-token'
            ])

        assert result.exit_code == 1
        assert "Authentication Error" in result.output


class TestConfigCommands:
    """Test configuration commands"""

    def test_config_help(self):
        """Test config help command"""
        runner = CliRunner()
        result = runner.invoke(cli, ['config', '--help'])
        assert result.exit_code == 0
        assert "Manage configuration" in result.output

    @patch('dumpconfluence.cli.ConfigManager')
    def test_config_list_empty(self, mock_config):
        """Test listing profiles when none exist"""
        mock_config.return_value.list_profiles.return_value = []

        runner = CliRunner()
        result = runner.invoke(cli, ['config', 'list'])

        assert result.exit_code == 0
        assert "No profiles found" in result.output

    @patch('dumpconfluence.cli.ConfigManager')
    def test_config_list_profiles(self, mock_config):
        """Test listing existing profiles"""
        mock_config.return_value.list_profiles.return_value = ['test', 'work']
        mock_config.return_value.load_profile.side_effect = [
            {'email': 'test@example.com', 'url': 'https://test.atlassian.net'},
            {'email': 'work@example.com', 'url': 'https://work.atlassian.net'}
        ]

        runner = CliRunner()
        result = runner.invoke(cli, ['config', 'list'])

        assert result.exit_code == 0
        assert "test@example.com" in result.output
        assert "work@example.com" in result.output

    @patch('dumpconfluence.cli.ConfigManager')
    def test_config_add_profile(self, mock_config):
        """Test adding a new profile"""
        runner = CliRunner()
        result = runner.invoke(cli, [
            'config', 'add', 'test',
            '--url', 'https://test.atlassian.net',
            '--email', 'test@example.com',
            '--token', 'test-token'
        ])

        assert result.exit_code == 0
        assert "Profile 'test' created" in result.output
        mock_config.return_value.save_profile.assert_called_once()

    @patch('dumpconfluence.cli.ConfigManager')
    def test_config_remove_profile(self, mock_config):
        """Test removing a profile"""
        mock_config.return_value.remove_profile.return_value = True

        runner = CliRunner()
        result = runner.invoke(cli, ['config', 'remove', 'test'])

        assert result.exit_code == 0
        assert "Profile 'test' removed" in result.output

    @patch('dumpconfluence.cli.ConfigManager')
    def test_config_remove_nonexistent_profile(self, mock_config):
        """Test removing a non-existent profile"""
        mock_config.return_value.remove_profile.return_value = False

        runner = CliRunner()
        result = runner.invoke(cli, ['config', 'remove', 'nonexistent'])

        assert result.exit_code == 0
        assert "Profile 'nonexistent' not found" in result.output

    @patch('dumpconfluence.cli.ConfigManager')
    def test_config_set_default(self, mock_config):
        """Test setting default profile"""
        mock_config.return_value.set_default_profile.return_value = True

        runner = CliRunner()
        result = runner.invoke(cli, ['config', 'default', 'test'])

        assert result.exit_code == 0
        assert "Profile 'test' set as default" in result.output


class TestProfileAutoSelection:
    """Test automatic profile selection"""

    @patch('dumpconfluence.cli.ConfigManager')
    @patch('dumpconfluence.cli.ConfluenceBackup')
    def test_auto_single_profile(self, mock_backup_class, mock_config):
        """Test auto-selection when only one profile exists"""
        mock_config.return_value.get_auto_profile.return_value = {
            'url': 'https://test.atlassian.net',
            'email': 'test@example.com',
            'token': 'test-token'
        }
        mock_config.return_value.list_profiles.return_value = ['test']

        mock_backup = Mock()
        mock_backup.backup_page.return_value = "/path/to/backup"
        mock_backup_class.return_value = mock_backup

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                'backup',
                'https://test.atlassian.net/wiki/spaces/TEST/pages/123/Test'
            ])

        assert result.exit_code == 0
        assert "Auto-using profile" in result.output

    @patch('dumpconfluence.cli.ConfigManager')
    @patch('dumpconfluence.cli.ConfluenceBackup')
    def test_auto_default_profile(self, mock_backup_class, mock_config):
        """Test auto-selection of default profile"""
        mock_config.return_value.get_auto_profile.return_value = {
            'url': 'https://test.atlassian.net',
            'email': 'test@example.com',
            'token': 'test-token'
        }
        mock_config.return_value.list_profiles.return_value = ['test', 'work']
        mock_config.return_value.get_default_profile.return_value = 'test'

        mock_backup = Mock()
        mock_backup.backup_page.return_value = "/path/to/backup"
        mock_backup_class.return_value = mock_backup

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                'backup',
                'https://test.atlassian.net/wiki/spaces/TEST/pages/123/Test'
            ])

        assert result.exit_code == 0
        assert "Using default profile" in result.output