"""YAML schema validation for Radicle command definitions."""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


class YAMLDefinitionError(Exception):
    """Raised when YAML definition is invalid."""

    pass


@dataclass
class CommandOption:
    """Represents a command option/flag."""

    name: str
    type: str  # "flag", "string", "int", "list"
    description: str
    required: bool = False
    default: Any = None
    choices: Optional[List[str]] = None
    added_in: Optional[str] = None


@dataclass
class PositionalArg:
    """Represents a positional argument for a Radicle command."""

    name: str
    type: str
    description: str
    required: bool = False


@dataclass
class Command:
    """Represents a Radicle command."""

    name: str
    help: str
    subcommands: Dict[str, "Command"]
    options: Dict[str, CommandOption]
    positional_args: Optional[List["PositionalArg"]] = None
    examples: Optional[List[str]] = None
    deprecated: bool = False
    deprecated_in: Optional[str] = None
    added_in: Optional[str] = None


@dataclass
class VersionMetadata:
    """Metadata for a Radicle version."""

    version: str
    release_date: str
    code_name: Optional[str] = None
    breaking_changes: bool = False
    migration_required: bool = False
    minimum_python_version: str = "3.8"


@dataclass
class RadicleVersion:
    """Complete definition for a Radicle version."""

    metadata: VersionMetadata
    commands: Dict[str, Command]


def validate_yaml_schema(yaml_data: Dict[str, Any]) -> RadicleVersion:
    """Validate and parse YAML data into RadicleVersion."""
    try:
        # Validate required top-level fields
        if "metadata" not in yaml_data:
            raise YAMLDefinitionError("Missing required 'metadata' field")

        if "commands" not in yaml_data:
            raise YAMLDefinitionError("Missing required 'commands' field")

        # Validate metadata
        metadata_data = yaml_data["metadata"]

        # Validate required metadata fields
        if "version" not in metadata_data:
            raise YAMLDefinitionError("Missing required 'version' in metadata")

        if "release_date" not in metadata_data:
            raise YAMLDefinitionError("Missing required 'release_date' in metadata")

        metadata = VersionMetadata(
            version=metadata_data["version"],
            release_date=metadata_data["release_date"],
            code_name=metadata_data.get("code_name"),
            breaking_changes=metadata_data.get("breaking_changes", False),
            migration_required=metadata_data.get("migration_required", False),
            minimum_python_version=metadata_data.get("minimum_python_version", "3.8"),
        )

        # Validate commands
        commands_data = yaml_data.get("commands", {})
        commands = {}

        for cmd_name, cmd_data in commands_data.items():
            subcommands = {}
            for sub_name, sub_data in cmd_data.get("subcommands", {}).items():
                subcommands[sub_name] = Command(
                    name=sub_name,
                    help=sub_data.get("help", ""),
                    subcommands={},
                    options=_parse_options(sub_data.get("options", {})),
                    examples=sub_data.get("examples"),
                    deprecated=sub_data.get("deprecated", False),
                    deprecated_in=sub_data.get("deprecated_in"),
                    added_in=sub_data.get("added_in"),
                )

            # Parse main command options - commands can have both subcommands and options
            main_cmd_options = _parse_options(cmd_data.get("options", {}))

            commands[cmd_name] = Command(
                name=cmd_name,
                help=cmd_data.get("help", ""),
                subcommands=subcommands,
                options=main_cmd_options,
                examples=cmd_data.get("examples"),
                deprecated=cmd_data.get("deprecated", False),
                deprecated_in=cmd_data.get("deprecated_in"),
                added_in=cmd_data.get("added_in"),
            )

        return RadicleVersion(metadata=metadata, commands=commands)

    except Exception as e:
        raise YAMLDefinitionError(f"Invalid YAML schema: {e}")


def _parse_options(options_data: Dict[str, Any]) -> Dict[str, CommandOption]:
    """Parse options data into CommandOption objects."""
    options = {}
    if not options_data:
        return options
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
