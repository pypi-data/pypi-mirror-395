"""YAML Schema Documentation for Radicle MCP Server."""

# YAML Schema for Radicle Command Definitions

This document describes the schema used for defining Radicle CLI commands and their behavior across different versions.

## Schema Structure

```yaml
metadata:
  version: string           # Radicle version (e.g., "1.4.0")
  release_date: string      # Release date (e.g., "2025-09-04")
  code_name: string        # Optional code name (e.g., "Lily")
  breaking_changes: bool    # Whether this version has breaking changes
  migration_required: bool  # Whether database migration is required
  minimum_python_version: string  # Minimum Python version required

commands:
  command_name:
    help: string                    # Command description
    subcommands:                  # Optional subcommands
      subcommand_name:
        help: string              # Subcommand description
        options: {}              # Subcommand-specific options
        examples: []             # Usage examples
        added_in: string          # Version when feature was added
        deprecated: bool          # Whether subcommand is deprecated
        deprecated_in: string     # Version when deprecated
    options: {}                    # Command-level options
      option_name:
        type: string              # Option type: "flag", "string", "int", "list"
        description: string        # Option description
        required: bool            # Whether option is required
        default: any             # Default value (optional)
        choices: []              # Valid choices for list/string types
    examples: []                   # Usage examples
    added_in: string              # Version when command was added
    deprecated: bool              # Whether command is deprecated
    deprecated_in: string         # Version when deprecated
```

## Option Types

- **`flag`**: Boolean option that doesn't take a value (e.g., `--json`)
- **`string`**: String value option (e.g., `--title "Bug fix"`)
- **`int`**: Integer value option (e.g., `--timeout 30`)
- **`list`**: Comma-separated list (e.g., `--labels bug,urgent`)

## Version Tracking

### `added_in`
Specifies the version when a command, subcommand, or option was first introduced.

```yaml
options:
  json:
    type: "flag"
    description: "Output in JSON format"
    added_in: "1.2.0"  # This option was added in version 1.2.0
```

### `deprecated_in`
Specifies the version when a command or option was deprecated.

```yaml
subcommands:
  old_command:
    help: "Old command that does something"
    deprecated: true
    deprecated_in: "1.3.0"  # Deprecated in favor of new_command
```

## Examples

### Basic Command Definition

```yaml
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
```

### Command with Subcommands

```yaml
commands:
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
      list:
        help: "List issues"
        options:
          status:
            type: "string"
            description: "Filter by status"
            required: false
            choices: ["open", "closed", "all"]
        examples:
          - "rad issue list"
          - "rad issue list --status open"
    options:
      json:
        type: "flag"
        description: "Output in JSON format"
        required: false
```

### Version-Specific Features

```yaml
commands:
  config:
    help: "Manage configuration"
    subcommands:
      schema:
        help: "Output JSON schema for configuration"
        added_in: "1.2.0"  # Only available in 1.2.0+
        options: {}
        examples:
          - "rad config schema"
```

## Naming Conventions

- **Command names**: Use lowercase, underscore-separated for compound names (e.g., `rad_issue_open`)
- **Option names**: Use lowercase, underscore-separated for compound names
- **Examples**: Show realistic usage with actual arguments
- **Descriptions**: Clear, concise descriptions of functionality

## Validation Rules

1. All commands must have `help` text
2. Required options must be marked as `required: true`
3. Options with choices must include the `choices` array
4. Version tracking must be accurate for new/deprecated features
5. Examples must be valid and testable

## File Organization

- Each Radicle version gets its own YAML file: `radicle-X.Y.Z.yaml`
- Files are stored in the `definitions/` directory
- Version files are loaded automatically based on installed Radicle version

## Migration Guide

When adding new versions:

1. Copy the previous version's YAML file
2. Update the `metadata` section
3. Add new commands, options, or subcommands with appropriate `added_in` versions
4. Mark deprecated items with `deprecated: true` and `deprecated_in`
5. Update examples to reflect new functionality
6. Test the new definition file

This schema ensures consistent command definitions across versions while enabling the MCP server to provide version-aware functionality.