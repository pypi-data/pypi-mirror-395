# Radicle MCP Server

A version-aware MCP (Model Context Protocol) server for the Radicle decentralized code forge.

## Features

- **Version-Aware**: Automatically detects installed Radicle version and loads appropriate command definitions
- **Dynamic Tool Generation**: Generates MCP tools from YAML definitions, supporting multiple Radicle versions
- **Generic Command Execution**: Unified interface for executing any Radicle command with validation
- **Output Parsing**: Intelligent parsing of command outputs into structured data
- **Fallback Support**: Graceful degradation when version detection fails
- **Comprehensive Coverage**: Supports all major Radicle commands: issue, patch, node, sync, config, and more

## Architecture

The server is built around a **YAML-based version definition system**:

```
definitions/
├── radicle-1.1.0.yaml  # Breaking changes release
├── radicle-1.2.0.yaml  # JSON output support
├── radicle-1.3.0.yaml  # Windows support + canonical references
├── radicle-1.4.0.yaml  # Stability fixes
└── radicle-1.5.0.yaml  # Latest features
```

Each YAML file contains:
- Command metadata and help text
- Available options with types and validation
- Subcommands and their arguments
- Version-specific additions and deprecations
- Usage examples

## Installation

```bash
# Install dependencies
pip install fastmcp pyyaml

# Run the server
python -m src.server
```

## Usage

### Basic Commands

```python
# Get Radicle version
await client.call_tool("rad_version", {})

# Get node status
await client.call_tool("rad_node_status", {})

# List issues
await client.call_tool("rad_issue_list", {"json": True})
```

### Advanced Commands

```python
# Create an issue
await client.call_tool("rad_issue_open", {
    "title": "Bug report",
    "description": "Found a bug in the code"
})

# Create a patch
await client.call_tool("rad_patch_open", {
    "title": "Fix the bug",
    "description": "Addresses the issue reported"
})

# Execute any command
await client.call_tool("rad_execute", {
    "command": "sync",
    "subcommand": "status"
})
```

### Configuration

The server supports configuration via `~/.radicle-mcp-server.yaml`:

```yaml
server:
  host: localhost
  port: 8000
  transport: stdio

radicle:
  timeout: 30
  definitions_dir: /path/to/definitions

logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

## Supported Radicle Versions

- **1.5.0** (Latest) - Full feature support
- **1.4.0** - Stability fixes and improved sync
- **1.3.0** - Windows support and canonical references
- **1.2.0** - JSON output and improved sync
- **1.1.0** - Database migration and config subcommands

## Version Compatibility

The server automatically:
1. Detects the installed Radicle version
2. Loads the appropriate YAML definition
3. Falls back to the closest supported version if exact match not found
4. Provides generic tools when version detection fails

## Development

### Adding New Version Support

1. Create new YAML file: `definitions/radicle-X.Y.Z.yaml`
2. Define commands following the schema in `definitions/schema.py`
3. Test with the new version

### Extending Functionality

The modular architecture allows easy extension:
- **YAML Definitions**: Add new commands by updating YAML files
- **Output Parsers**: Extend `_parse_output()` methods for new formats
- **Tool Generation**: Customize tool generation in `ToolGenerator`

## Error Handling

The server provides comprehensive error handling:
- **Version Detection**: Graceful fallback when Radicle is not installed
- **Command Validation**: Validates arguments against command definitions
- **Execution Errors**: Clear error messages for failed commands
- **Network Issues**: Timeout handling and connection error reporting

## Testing

```bash
# Run tests
python -m pytest tests/

# Test with specific Radicle version
RAD_VERSION=1.4.0 python -m src.server
```

## License

MIT License - see LICENSE file for details.