"""Test tool generator schema generation."""

import pytest
import sys
import os

# Mock imports to avoid dependency issues
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from src.definitions.schema import Command, PositionalArg, CommandOption
from src.tool_generator import ToolGenerator
from tests.test_doubles import MockVersionManager, MockCommandExecutor


@pytest.fixture
def tool_generator():
    """Create tool generator fixture."""
    version_manager = MockVersionManager()
    executor = MockCommandExecutor()
    return ToolGenerator(version_manager, executor)

    def test_command_schema_with_positional_args(tool_generator):
        """Test that command schemas include positional args from YAML."""
        # Create command with positional arguments
        command_def = Command(
            name="test",
            help="Test command",
            subcommands={},
            options={},
            positional_args=[
                PositionalArg(
                    name="id", type="string", description="Test ID", required=True
                ),
                PositionalArg(
                    name="optional_arg",
                    type="string",
                    description="Optional argument",
                    required=False,
                ),
            ],
        )

        schema = tool_generator._generate_command_schema("test", command_def)

        # Should include positional arguments from YAML
        assert "id" in schema["properties"]
        assert "optional_arg" in schema["properties"]
        assert "id" in schema["required"]
        assert "optional_arg" not in schema["required"]

        # Check property definitions
        assert schema["properties"]["id"]["type"] == "string"
        assert schema["properties"]["id"]["description"] == "Test ID"
        assert schema["properties"]["optional_arg"]["type"] == "string"
        assert (
            schema["properties"]["optional_arg"]["description"] == "Optional argument"
        )

    def test_subcommand_schema_with_positional_args(self):
        """Test that subcommand schemas include positional args from YAML."""
        # Create parent command
        parent_command = Command(
            name="issue",
            help="Manage issues",
            subcommands={},
            options={
                "repo": CommandOption(
                    name="repo",
                    type="string",
                    description="Repository to operate on",
                    required=False,
                )
            },
        )

        # Create subcommand with positional arguments
        subcommand_def = Command(
            name="show",
            help="Show issue details",
            subcommands={},
            options={},
            positional_args=[
                PositionalArg(
                    name="id", type="string", description="Issue ID", required=True
                )
            ],
        )

        schema = self.tool_generator._generate_subcommand_schema(
            "issue", parent_command, "show", subcommand_def
        )

        # Should include positional arguments from YAML
        assert "id" in schema["properties"]
        assert "id" in schema["required"]

        # Should also inherit parent command options
        assert "repo" in schema["properties"]
        assert "repo" not in schema["required"]  # parent option is not required

        # Check property definitions
        assert schema["properties"]["id"]["type"] == "string"
        assert schema["properties"]["id"]["description"] == "Issue ID"

    def test_issue_show_schema_includes_required_id(self):
        """Test that rad_issue_show schema includes required 'id' parameter."""
        # Get actual command definition from version manager
        definition = self.version_manager.get_current_definition()
        issue_command = definition.commands["issue"]
        show_subcommand = issue_command.subcommands["show"]

        schema = self.tool_generator._generate_subcommand_schema(
            "issue", issue_command, "show", show_subcommand
        )

        # Should have required 'id' parameter from YAML definition
        assert "id" in schema["properties"]
        assert "id" in schema["required"]
        assert schema["properties"]["id"]["type"] == "string"
        assert "Issue ID" in schema["properties"]["id"]["description"]

    def test_issue_edit_schema_includes_required_id(self):
        """Test that rad_issue_edit schema includes required 'id' parameter."""
        definition = self.version_manager.get_current_definition()
        issue_command = definition.commands["issue"]
        edit_subcommand = issue_command.subcommands["edit"]

        schema = self.tool_generator._generate_subcommand_schema(
            "issue", issue_command, "edit", edit_subcommand
        )

        # Should have required 'id' parameter from YAML definition
        assert "id" in schema["properties"]
        assert "id" in schema["required"]

    def test_config_get_schema_includes_required_key(self):
        """Test that rad_config_get schema includes required 'key' parameter."""
        definition = self.version_manager.get_current_definition()
        config_command = definition.commands["config"]
        get_subcommand = config_command.subcommands["get"]

        schema = self.tool_generator._generate_subcommand_schema(
            "config", config_command, "get", get_subcommand
        )

        # Should have required 'key' parameter from YAML definition
        assert "key" in schema["properties"]
        assert "key" in schema["required"]

    def test_config_set_schema_includes_required_key_and_value(self):
        """Test that rad_config_set schema includes required 'key' and 'value' parameters."""
        definition = self.version_manager.get_current_definition()
        config_command = definition.commands["config"]
        set_subcommand = config_command.subcommands["set"]

        schema = self.tool_generator._generate_subcommand_schema(
            "config", config_command, "set", set_subcommand
        )

        # Should have required 'key' and 'value' parameters from YAML definition
        assert "key" in schema["properties"]
        assert "value" in schema["properties"]
        assert "key" in schema["required"]
        assert "value" in schema["required"]

    def test_schema_without_positional_args(self):
        """Test schema generation when no positional args are defined."""
        command_def = Command(
            name="list",
            help="List items",
            subcommands={},
            options={
                "all": CommandOption(
                    name="all",
                    type="flag",
                    description="Show all items",
                    required=False,
                )
            },
        )

        schema = self.tool_generator._generate_command_schema("list", command_def)

        # Should only have options, no positional args
        assert "all" in schema["properties"]
        assert "all" not in schema["required"]
        assert len(schema["properties"]) == 1
        assert len(schema["required"]) == 0

    def test_type_mapping_for_positional_args(tool_generator):
        """Test that positional arg types are correctly mapped to JSON schema types."""
        command_def = Command(
            name="test",
            help="Test command",
            subcommands={},
            options={},
            positional_args=[
                PositionalArg(
                    name="str_arg",
                    type="string",
                    description="String arg",
                    required=True,
                ),
                PositionalArg(
                    name="int_arg", type="int", description="Int arg", required=True
                ),
                PositionalArg(
                    name="flag_arg", type="flag", description="Flag arg", required=True
                ),
                PositionalArg(
                    name="list_arg", type="list", description="List arg", required=True
                ),
            ],
        )

        schema = tool_generator._generate_command_schema("test", command_def)

        assert schema["properties"]["str_arg"]["type"] == "string"
        assert schema["properties"]["int_arg"]["type"] == "integer"
        assert schema["properties"]["flag_arg"]["type"] == "boolean"
        assert schema["properties"]["list_arg"]["type"] == "array"
