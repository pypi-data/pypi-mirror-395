"""YAML schema validation for Radicle command definitions."""

from __future__ import annotations

from typing import Any
from dataclasses import dataclass


class YAMLDefinitionError(Exception):
    """Raised when YAML definition is invalid."""


@dataclass
class CommandOption:
    """Command-line option definition for Radicle commands.

    Defines structure and validation rules for options like --title, --json.
    Used by ToolGenerator to create MCP tool schemas with type validation.
    """

    name: str
    type: str  # "flag", "string", "int", "list"
    description: str
    required: bool = False
    default: Any = None  # pyright: ignore[reportExplicitAny]  # YAML config value
    choices: list[str] | None = None
    added_in: str | None = None


@dataclass
class PositionalArg:
    """Positional argument definition for Radicle commands.

    Represents required or optional positional args like issue IDs or file paths.
    """

    name: str
    type: str  # "string", "int", "list"
    description: str
    required: bool = True
    choices: list[str] | None = None
    added_in: str | None = None


@dataclass
class Command:
    """Complete Radicle command definition with options and subcommands.

    Central data structure representing a command's help text, options,
    positional arguments, subcommands, and usage examples.
    """

    name: str
    help: str
    subcommands: dict[str, "Command"]
    options: dict[str, CommandOption]
    positional_args: list[PositionalArg] | None = None
    examples: list[str] | None = None
    deprecated: bool = False
    deprecated_in: str | None = None
    added_in: str | None = None


@dataclass
class VersionMetadata:
    """Metadata about a Radicle version release.

    Contains version number, release date, and compatibility information
    for version-specific command definitions.
    """

    version: str
    release_date: str
    code_name: str | None = None
    breaking_changes: bool = False
    migration_required: bool = False
    minimum_python_version: str = "3.8"


@dataclass
class RadicleVersion:
    """Complete version definition with metadata and commands.

    Top-level structure combining version metadata with all available
    commands and their definitions for that Radicle release.
    """

    metadata: VersionMetadata
    commands: dict[str, Command]


def validate_yaml_schema(yaml_data: dict[str, Any]) -> RadicleVersion:  # pyright: ignore[reportExplicitAny]  # YAML parsing
    """Validate and parse YAML data into RadicleVersion."""
    try:
        # Validate required top-level fields
        if "metadata" not in yaml_data:
            raise YAMLDefinitionError("Missing required 'metadata' field")

        if "commands" not in yaml_data:
            raise YAMLDefinitionError("Missing required 'commands' field")

        # Validate metadata
        metadata_data = yaml_data["metadata"]  # YAML metadata access

        # Validate required metadata fields
        if "version" not in metadata_data:
            raise YAMLDefinitionError("Missing required 'version' in metadata")

        if "release_date" not in metadata_data:
            raise YAMLDefinitionError("Missing required 'release_date' in metadata")

        metadata = VersionMetadata(
            version=metadata_data["version"],  # YAML field access
            release_date=metadata_data["release_date"],  # YAML field access
            code_name=metadata_data.get("code_name"),  # YAML field access with default
            breaking_changes=metadata_data.get(
                "breaking_changes", False
            ),  # YAML field access with default
            migration_required=metadata_data.get(
                "migration_required", False
            ),  # YAML field access with default
            minimum_python_version=metadata_data.get(
                "minimum_python_version", "3.8"
            ),  # YAML field access with default
        )

        # Validate commands
        commands_data = yaml_data.get("commands", {})  # YAML commands access
        commands = {}

        for cmd_name, cmd_data in commands_data.items():
            subcommands = {}
            for sub_name, sub_data in cmd_data.get("subcommands", {}).items():
                subcommands[sub_name] = Command(
                    name=sub_name,
                    help=sub_data.get("help", ""),
                    subcommands={},
                    options=_parse_options(sub_data.get("options", {})),
                    positional_args=_parse_positional_args(
                        sub_data.get("positional_args", [])
                    ),
                    examples=sub_data.get("examples"),
                    deprecated=sub_data.get("deprecated", False),
                    deprecated_in=sub_data.get("deprecated_in"),
                    added_in=sub_data.get("added_in"),
                )

            commands[cmd_name] = Command(
                name=cmd_name,
                help=cmd_data.get("help", ""),
                subcommands=subcommands,
                options=_parse_options(cmd_data.get("options", {})),
                positional_args=_parse_positional_args(
                    cmd_data.get("positional_args", [])
                ),
                examples=cmd_data.get("examples"),
                deprecated=cmd_data.get("deprecated", False),
                deprecated_in=cmd_data.get("deprecated_in"),
                added_in=cmd_data.get("added_in"),
            )

        return RadicleVersion(metadata=metadata, commands=commands)

    except Exception as e:
        raise YAMLDefinitionError(f"Invalid YAML schema: {e}")


def _parse_options(options_data: dict[str, Any]) -> dict[str, CommandOption]:  # pyright: ignore[reportExplicitAny]  # YAML parsing
    """Parse YAML options data into CommandOption objects with validation."""
    options = {}
    for opt_name, opt_data in options_data.items():
        options[opt_name] = CommandOption(
            name=opt_name,
            type=opt_data.get("type", "string"),
            description=opt_data.get("description", ""),
            required=opt_data.get("required", False),
            default=opt_data.get("default"),
            choices=opt_data.get("choices"),
            added_in=opt_data.get("added_in"),
        )
    return options


def _parse_positional_args(
    positional_data: list[dict[str, Any]],  # pyright: ignore[reportExplicitAny]  # YAML parsing
) -> list[PositionalArg]:
    """Parse YAML positional arguments data into PositionalArg objects."""
    positional_args = []
    for pos_data in positional_data:
        positional_args.append(
            PositionalArg(
                name=pos_data.get("name", ""),
                type=pos_data.get("type", "string"),
                description=pos_data.get("description", ""),
                required=pos_data.get("required", True),
                choices=pos_data.get("choices"),
                added_in=pos_data.get("added_in"),
            )
        )
    return positional_args


def get_yaml_schema_template() -> str:
    """Get a template for YAML command definitions."""
    return """
metadata:
  version: "1.5.0"
  release_date: "2025-09-04"
  code_name: "Lily"
  breaking_changes: false
  migration_required: false
  minimum_python_version: "3.8"

commands:
  auth:
    help: "Manage identities and profiles"
    subcommands: {}
    options:
      stdin:
        type: "flag"
        description: "Read passphrase from stdin"
        required: false
    examples:
      - "rad auth"
      - "rad auth --stdin"

  issue:
    help: "Manage issues"
    subcommands:
      open:
        help: "Create a new issue"
        options:
          title:
            type: "string"
            description: "Issue title"
            required: true
          description:
            type: "string"
            description: "Issue description"
            required: false
        examples:
          - "rad issue open --title 'Bug fix' --description 'Fixes the issue'"
    options:
      json:
        type: "flag"
        description: "Output in JSON format"
        required: false
    examples:
      - "rad issue list"
      - "rad issue list --json"
"""
