"""Test configuration and utilities for Radicle MCP Server."""

import pytest
import tempfile
import yaml
from pathlib import Path

from src.definitions.schema import validate_yaml_schema, YAMLDefinitionError


class TestYAMLSchema:
    """Test YAML schema validation."""

    def test_valid_schema(self):
        """Test validation of valid YAML schema."""
        valid_yaml = {
            "metadata": {
                "version": "1.4.0",
                "release_date": "2025-09-04",
                "code_name": "Lily",
                "breaking_changes": False,
                "migration_required": False,
                "minimum_python_version": "3.8",
            },
            "commands": {
                "test": {
                    "help": "Test command",
                    "subcommands": {},
                    "options": {
                        "flag": {
                            "type": "flag",
                            "description": "Test flag",
                            "required": False,
                        }
                    },
                    "examples": ["rad test --flag"],
                }
            },
        }

        # Should not raise exception
        result = validate_yaml_schema(valid_yaml)
        assert result.metadata.version == "1.4.0"
        assert "test" in result.commands

    def test_invalid_schema_missing_metadata(self):
        """Test validation fails with missing metadata."""
        invalid_yaml = {"commands": {}}

        with pytest.raises(YAMLDefinitionError):
            validate_yaml_schema(invalid_yaml)

    def test_invalid_schema_missing_version(self):
        """Test validation fails with missing version."""
        invalid_yaml = {"metadata": {"release_date": "2025-09-04"}, "commands": {}}

        with pytest.raises(YAMLDefinitionError):
            validate_yaml_schema(invalid_yaml)


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


class TestConfig:
    """Test configuration management."""

    def test_default_config_loading(self):
        """Test loading of default configuration."""
        from src.config import Config

        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "test_config.yaml"
            config = Config(config_file)

            # Test default values
            assert config.get("server.host") == "localhost"
            assert config.get("server.port") == 8000
            assert config.get("server.transport") == "stdio"
            assert config.get("radicle.timeout") == 30

    def test_config_merging(self):
        """Test configuration merging."""
        from src.config import Config

        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "test_config.yaml"

            # Create custom config
            custom_config = {
                "server": {"port": 9000, "transport": "http"},
                "radicle": {"timeout": 60},
            }

            with open(config_file, "w") as f:
                yaml.dump(custom_config, f)

            config = Config(config_file)

            # Test merged values
            assert config.get("server.host") == "localhost"  # Default
            assert config.get("server.port") == 9000  # Custom
            assert config.get("server.transport") == "http"  # Custom
            assert config.get("radicle.timeout") == 60  # Custom

    def test_config_dot_notation(self):
        """Test configuration access with dot notation."""
        from src.config import Config

        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "test_config.yaml"
            config = Config(config_file)

            # Test dot notation
            assert config.get("server.host") == "localhost"
            assert config.get("radicle.timeout") == 30

            # Test setting with dot notation
            config.set("server.host", "example.com")
            assert config.get("server.host") == "example.com"

            config.set("new.nested.key", "value")
            assert config.get("new.nested.key") == "value"


if __name__ == "__main__":
    pytest.main([__file__])
