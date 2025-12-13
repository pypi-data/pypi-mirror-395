"""Additional error handling tests for Radicle MCP Server."""

import pytest
from unittest.mock import Mock, patch

# Mock imports to avoid dependency issues
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class TestErrorHandling:
    """Test error handling paths."""

    def test_command_execution_timeout(self):
        """Test command execution timeout handling."""
        from src.command_executor import CommandExecutor
        from src.yaml_loader import VersionManager
        from src.exceptions import CommandExecutionError
        from pathlib import Path

        manager = VersionManager()
        executor = CommandExecutor(manager)

        with patch.object(executor, "_detect_working_directory", return_value=Path("/tmp")):
            with patch("subprocess.run") as mock_run:
                from subprocess import TimeoutExpired

                mock_run.side_effect = TimeoutExpired("rad", 30)

                manager.get_command_definition = Mock(
                    return_value=Mock(options={}, subcommands={}, positional_args=[])
                )

                with pytest.raises(CommandExecutionError, match="timed out"):
                    executor.execute_command("test", args={})

    def test_command_execution_subprocess_error(self):
        """Test command execution with subprocess error."""
        from src.command_executor import CommandExecutor
        from src.yaml_loader import VersionManager
        from src.exceptions import CommandExecutionError
        from pathlib import Path

        manager = VersionManager()
        executor = CommandExecutor(manager)

        with patch.object(executor, "_detect_working_directory", return_value=Path("/tmp")):
            with patch("subprocess.run") as mock_run:
                mock_run.side_effect = OSError("Command not found")

                manager.get_command_definition = Mock(
                    return_value=Mock(options={}, subcommands={}, positional_args=[])
                )

                with pytest.raises(CommandExecutionError, match="Command execution failed"):
                    executor.execute_command("test", args={})

    def test_missing_required_argument_validation(self):
        """Test validation of missing required arguments."""
        from src.command_executor import CommandExecutor
        from src.yaml_loader import VersionManager
        from src.exceptions import InvalidArgumentError

        manager = VersionManager()
        executor = CommandExecutor(manager)

        # Mock command definition with required option
        mock_option = Mock(type="string", required=True, description="Required option")
        mock_command = Mock(options={"required_opt": mock_option}, subcommands={})

        with pytest.raises(InvalidArgumentError, match="missing"):
            executor._validate_arguments(mock_command, {})

    def test_output_parsing_invalid_json(self):
        """Test output parsing with invalid JSON."""
        from src.command_executor import CommandExecutor
        from src.yaml_loader import VersionManager

        manager = VersionManager()
        executor = CommandExecutor(manager)

        # Mock command definition
        class MockCommand:
            name = "test"
            options = {}

        # Test invalid JSON with json flag
        invalid_json = '{"invalid": json content}'
        args = {"json": True}
        result = executor._parse_output(invalid_json, MockCommand(), args)

        # Should return None when JSON parsing fails
        assert result is None

    def test_output_parsing_empty_output(self):
        """Test output parsing with empty output."""
        from src.command_executor import CommandExecutor
        from src.yaml_loader import VersionManager

        manager = VersionManager()
        executor = CommandExecutor(manager)

        # Mock command definition
        class MockCommand:
            name = "test"
            options = {}

        # Test empty output
        result = executor._parse_output("", MockCommand(), {})
        assert result is None

        # Test whitespace-only output
        result = executor._parse_output("   \n\t  ", MockCommand(), {})
        assert result is None


class TestVersionManagerEdgeCases:
    """Test version manager edge cases."""

    def test_version_detection_not_installed(self):
        """Test version detection when Radicle is not installed."""
        from src.yaml_loader import VersionManager
        from src.exceptions import RadicleNotInstalledError

        manager = VersionManager()

        # Mock subprocess.run to simulate Radicle not found
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = Mock(returncode=1, stderr="rad: command not found")

            with pytest.raises(RadicleNotInstalledError):
                manager.get_installed_version()

    def test_closest_version_no_supported_versions(self):
        """Test finding closest version when no versions are supported."""
        from src.yaml_loader import VersionManager

        manager = VersionManager()

        # Mock empty supported versions
        with patch.object(manager, "get_supported_versions", return_value=[]):
            result = manager._find_closest_supported_version("1.0.0")
            assert result is None


class TestConfigErrorScenarios:
    """Test configuration error scenarios."""

    def test_config_invalid_yaml_structure(self):
        """Test handling of invalid YAML structure."""
        from src.config import Config
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "invalid_config.yaml"

            # Create invalid YAML structure
            config_file.write_text("invalid: yaml: content: [")

            config = Config(config_file)

            # Should fall back to defaults
            assert config.get("server.host") == "localhost"
            assert config.get("server.port") == 8000


class TestToolGeneratorFallbacks:
    """Test tool generator fallback scenarios."""

    def test_tool_generation_with_version_error(self):
        """Test tool generation when version detection fails."""
        from src.tool_generator import ToolGenerator
        from src.yaml_loader import VersionManager
        from src.command_executor import CommandExecutor
        from src.exceptions import VersionNotSupportedError

        manager = VersionManager()
        executor = CommandExecutor(manager)
        generator = ToolGenerator(manager, executor)

        # Mock version manager to raise error
        with patch.object(
            manager,
            "get_current_definition",
            side_effect=VersionNotSupportedError("Unsupported version"),
        ):
            tools = generator.generate_all_tools()

            # Should return fallback tools
            assert "rad_execute" in tools
            assert "rad_version" in tools
            assert "rad_help" in tools


if __name__ == "__main__":
    pytest.main([__file__])
