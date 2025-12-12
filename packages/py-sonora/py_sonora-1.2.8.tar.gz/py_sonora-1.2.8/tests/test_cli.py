"""Additional tests for CLI commands."""

import pytest

from sonora.cli import doctor_check, handle_autoplay_command, handle_plugin_command, handle_queue_command, profile_performance


class TestCLICommands:
    """Test CLI command handlers."""

    def test_doctor_check(self, capsys, monkeypatch):
        """Test doctor check command."""
        # Mock sys.exit to prevent test termination
        def mock_exit(code):
            pass

        monkeypatch.setattr('sys.exit', mock_exit)

        # Mock args
        class MockArgs:
            host = "127.0.0.1"
            port = 2333

        args = MockArgs()
        doctor_check(args)

        captured = capsys.readouterr()
        assert "Sonora Doctor" in captured.out
        assert "Python:" in captured.out

    def test_handle_plugin_command_list(self, capsys):
        """Test plugin list command."""
        class MockArgs:
            plugin_command = "list"

        args = MockArgs()
        handle_plugin_command(args)

        captured = capsys.readouterr()
        assert "Installed plugins:" in captured.out

    def test_handle_plugin_command_enable(self, capsys):
        """Test plugin enable command."""
        class MockArgs:
            plugin_command = "enable"
            name = "test_plugin"

        args = MockArgs()
        handle_plugin_command(args)

        captured = capsys.readouterr()
        assert "Enabling plugin: test_plugin" in captured.out

    def test_handle_autoplay_command_status(self, capsys):
        """Test autoplay status command."""
        class MockArgs:
            autoplay_command = "status"

        args = MockArgs()
        handle_autoplay_command(args)

        captured = capsys.readouterr()
        assert "Autoplay status:" in captured.out

    def test_handle_queue_command_inspect(self, capsys):
        """Test queue inspect command."""
        class MockArgs:
            queue_command = "inspect"
            guild_id = 123

        args = MockArgs()
        handle_queue_command(args)

        captured = capsys.readouterr()
        assert "Queue inspection for guild 123" in captured.out

    def test_profile_performance(self, capsys):
        """Test profile performance command."""
        class MockArgs:
            pass

        args = MockArgs()
        profile_performance(args)

        captured = capsys.readouterr()
        assert "Sonora Performance Profile" in captured.out