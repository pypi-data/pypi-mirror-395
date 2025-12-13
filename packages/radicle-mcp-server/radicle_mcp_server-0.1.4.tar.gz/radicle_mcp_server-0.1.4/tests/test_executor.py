"""Test command execution functionality."""

import pytest
from unittest.mock import Mock, patch

# Mock imports to avoid dependency issues
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class TestCommandExecutor:
    """Test command execution functionality."""

    def test_argument_validation(self):
        """Test command argument validation."""
        from src.command_executor import CommandExecutor
        from src.yaml_loader import VersionManager

        manager = VersionManager()
        executor = CommandExecutor(manager)

        # Mock command definition
        class MockCommand:
            options = {
                "required_flag": type(
                    "MockOption", (), {"type": "string", "required": True}
                ),
                "optional_flag": type(
                    "MockOption", (), {"type": "flag", "required": False}
                ),
            }

        # Test missing required argument
        with pytest.raises(Exception):  # Should raise InvalidArgumentError
            executor._validate_arguments(MockCommand(), {})

        # Test valid arguments
        args = {"required_flag": "value", "optional_flag": True}
        validated = executor._validate_arguments(MockCommand(), args)
        assert "--required_flag" in validated
        assert "value" in validated
        assert "--optional_flag" in validated

    def test_positional_argument_extraction(self):
        """Test extraction of positional arguments."""
        from src.command_executor import CommandExecutor
        from src.yaml_loader import VersionManager

        manager = VersionManager()
        executor = CommandExecutor(manager)

        # Mock command definition
        class MockPositionalArg:
            def __init__(self, name: str):
                self.name = name

        class MockCommand:
            name = "issue"
            options = {}
            positional_args = [MockPositionalArg("id"), MockPositionalArg("rid")]
            subcommands = {}

        # Test ID extraction
        args = {"id": "123"}
        positional = executor._get_positional_args(MockCommand(), args)
        assert "123" in positional

        # Test RID extraction
        args = {"rid": ["repo1", "repo2"]}
        positional = executor._get_positional_args(MockCommand(), args)
        assert "repo1" in positional
        assert "repo2" in positional

    def test_output_parsing(self):
        """Test output parsing for different commands."""
        from src.command_executor import CommandExecutor
        from src.yaml_loader import VersionManager

        manager = VersionManager()
        executor = CommandExecutor(manager)

        # Mock command definition
        class MockCommand:
            name = "issue"
            options = {}

        # Test JSON parsing
        json_output = '{"id": "123", "title": "Test Issue"}'
        args = {"json": True}
        result = executor._parse_output(json_output, MockCommand(), args)
        assert result == {"id": "123", "title": "Test Issue"}

        # Test issue list parsing
        issue_output = "#123 Test Issue open\n#456 Another Issue closed"
        result = executor._parse_output(issue_output, MockCommand(), {})
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == "123"
        assert result[0]["title"] == "Test Issue"
        assert result[0]["status"] == "open"

    def test_command_execution_success(self):
        """Test successful command execution."""
        from src.command_executor import CommandExecutor
        from src.yaml_loader import VersionManager

        manager = VersionManager()
        executor = CommandExecutor(manager)

        # Mock subprocess.run success
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = Mock(
                returncode=0, stdout="Command output", stderr=""
            )

            # Mock version manager
            manager.get_command_definition = Mock(
                return_value=Mock(options={}, subcommands={}, positional_args=[])
            )

            result = executor.execute_command(command="test", args={})

            assert result["success"] is True
            assert result["returncode"] == 0
            assert result["stdout"] == "Command output"
            assert result["stderr"] == ""

    def test_command_execution_failure(self):
        """Test failed command execution."""
        from src.command_executor import CommandExecutor
        from src.yaml_loader import VersionManager
        from pathlib import Path

        manager = VersionManager()
        executor = CommandExecutor(manager)

        with patch.object(executor, "_detect_working_directory", return_value=Path("/tmp")):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = Mock(
                    returncode=1, stdout="", stderr="Command failed"
                )

                manager.get_command_definition = Mock(
                    return_value=Mock(options={}, subcommands={}, positional_args=[])
                )

                result = executor.execute_command(command="test", args={})

                assert result["success"] is False
                assert result["returncode"] == 1
                assert result["stdout"] == ""
                assert result["stderr"] == "Command failed"


class TestVersionManager:
    """Test version management functionality."""

    def test_version_parsing(self):
        """Test version string parsing."""
        from src.yaml_loader import VersionManager

        manager = VersionManager()

        # Test version key generation
        key = manager._version_key("1.4.0")
        assert key == (1, 4, 0)

        key = manager._version_key("1.10.2")
        assert key == (1, 10, 2)

    def test_closest_version_finding(self):
        """Test finding closest supported version."""
        from src.yaml_loader import VersionManager

        manager = VersionManager()

        # Mock supported versions
        manager.get_supported_versions = lambda: ["1.4.0", "1.3.0", "1.2.0"]

        # Test exact match
        closest = manager._find_closest_supported_version("1.3.0")
        assert closest == "1.3.0"

        # Test closest match
        closest = manager._find_closest_supported_version("1.3.5")
        assert closest == "1.3.0"  # Should find 1.3.0 as closest


class TestToolGenerator:
    """Test tool generation functionality."""

    def test_fallback_tools_generation(self):
        """Test generation of fallback tools."""
        from src.tool_generator import ToolGenerator
        from src.yaml_loader import VersionManager
        from src.command_executor import CommandExecutor

        manager = VersionManager()
        executor = CommandExecutor(manager)
        generator = ToolGenerator(manager, executor)

        tools = generator._generate_fallback_tools()

        assert "rad_execute" in tools
        assert "rad_version" in tools
        assert "rad_help" in tools

        # Test tool function signatures
        assert callable(tools["rad_execute"])
        assert callable(tools["rad_version"])
        assert callable(tools["rad_help"])

    def test_type_mapping(self):
        """Test mapping of Radicle types to JSON schema types."""
        from src.tool_generator import ToolGenerator
        from src.yaml_loader import VersionManager
        from src.command_executor import CommandExecutor

        manager = VersionManager()
        executor = CommandExecutor(manager)
        generator = ToolGenerator(manager, executor)

        # Test type mapping
        assert generator._map_type_to_json_type("string") == "string"
        assert generator._map_type_to_json_type("int") == "integer"
        assert generator._map_type_to_json_type("flag") == "boolean"
        assert generator._map_type_to_json_type("list") == "array"
        assert generator._map_type_to_json_type("unknown") == "string"  # Default


if __name__ == "__main__":
    pytest.main([__file__])

    def test_explicit_parameter_generation(self):
        """Test explicit parameter generation from command definitions."""
        from src.tool_generator import ToolGenerator
        from src.yaml_loader import VersionManager
        from src.command_executor import CommandExecutor
        import inspect

        manager = VersionManager()
        executor = CommandExecutor(manager)
        generator = ToolGenerator(manager, executor)

        # Test that tools are generated with explicit parameters (no **kwargs)
        tools = generator.generate_all_tools()

        # Check that we have tools with explicit parameters (no **kwargs)
        auth_tool = tools.get("rad_auth")
        assert auth_tool is not None

        # Check signature has explicit parameters
        sig = inspect.signature(auth_tool)
        assert "stdin" in sig.parameters
        assert sig.parameters["stdin"].annotation == bool | None
        assert sig.parameters["stdin"].default is None  # Optional parameter

        # Check required parameter tool
        block_tool = tools.get("rad_block")
        assert block_tool is not None
        block_sig = inspect.signature(block_tool)
        assert "did" in block_sig.parameters
        assert block_sig.parameters["did"].annotation is str
        assert (
            block_sig.parameters["did"].default == inspect.Parameter.empty
        )  # Required

        # Check subcommand tool
        config_get_tool = tools.get("rad_config_get")
        assert config_get_tool is not None
        config_get_sig = inspect.signature(config_get_tool)
        assert "key" in config_get_sig.parameters
        assert config_get_sig.parameters["key"].annotation is str
