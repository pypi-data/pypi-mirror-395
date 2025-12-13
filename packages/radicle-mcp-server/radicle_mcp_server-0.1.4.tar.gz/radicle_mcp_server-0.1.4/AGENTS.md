# AGENTS.md - Agent Guide for Radicle MCP Server

This guide provides agent-specific instructions for working with the Radicle MCP Server project, including Context7 MCP integration patterns and development workflows.

## Context7 MCP Integration

**Always use Context7 when you need:**
- Code generation for MCP tools or FastMCP integration
- Setup or configuration steps for dependencies
- Library/API documentation
- Understanding MCP protocol specifications
- Best practices for Python async/await patterns

**Automatic Context7 Usage:**
Use Context7 MCP tools to resolve library IDs and get documentation without explicit prompting when working with:
- FastMCP framework patterns and tool registration
- PyYAML schema validation and loading
- attrs dataclass patterns
- subprocess command execution patterns
- JSON schema generation for MCP tools

## Critical Agent Commands

### MCP Server Development
```bash
# Run server with debugging
just run                    # Stdio transport (default)
just run-http              # HTTP transport on localhost:8000

# Test with specific Radicle version
RAD_VERSION=1.4.0 python -m src.server

# Validate YAML definitions
just validate-yaml

# Test tool generation specifically
python -c "from src.tool_generator import ToolGenerator; from src.yaml_loader import VersionManager; tg = ToolGenerator(VersionManager()); print(list(tg.generate_all_tools().keys()))"
```

### Context7 Integration Examples
```bash
# Get FastMCP documentation for tool registration
# Use Context7: resolve-library-id "fastmcp" -> get-library-docs with topic="tool registration"

# Get PyYAML documentation for schema validation
# Use Context7: resolve-library-id "pyyaml" -> get-library-docs with topic="schema validation"

# Get attrs documentation for dataclass patterns
# Use Context7: resolve-library-id "attrs" -> get-library-docs with topic="dataclass"
```

## MCP Server Development Workflow

### 1. Adding New Radicle Version Support
```bash
# 1. Create new YAML definition file
cp src/definitions/radicle-1.5.0.yaml src/definitions/radicle-1.6.0.yaml

# 2. Update version metadata
# Edit the new file with updated version, release_date, etc.

# 3. Test version loading
python -c "from src.yaml_loader import VersionManager; vm = VersionManager(); print(vm.get_supported_versions())"

# 4. Validate YAML schema
just validate-yaml

# 5. Test tool generation
python -c "from src.tool_generator import ToolGenerator; from src.yaml_loader import VersionManager; import os; os.environ['RAD_VERSION'] = '1.6.0'; tg = ToolGenerator(VersionManager()); print(f'Generated {len(tg.generate_all_tools())} tools')"
```

### 2. Adding New Commands to Existing Versions
```bash
# 1. Edit appropriate YAML definition
# Edit src/definitions/radicle-1.5.0.yaml

# 2. Add command following schema in docs/YAML_SCHEMA.md
# Use Context7 for PyYAML patterns if needed

# 3. Test command definition loading
python -c "from src.yaml_loader import VersionManager; vm = VersionManager(); cmd_def = vm.get_command_definition('new_command'); print(cmd_def.help if cmd_def else 'Not found')"

# 4. Test tool generation for new command
python -c "from src.tool_generator import ToolGenerator; from src.yaml_loader import VersionManager; tg = ToolGenerator(VersionManager()); tools = tg.generate_all_tools(); print(f'rad_new_command: {\"rad_new_command\" in tools}')"
```

### 3. Testing MCP Tool Integration
```bash
# Test server startup and tool registration
python -m src.server --help

# Test specific tool execution (if server is running)
# Use MCP client to call: rad_issue_open, rad_execute, etc.

# Test command execution directly
python -c "from src.command_executor import CommandExecutor; from src.yaml_loader import VersionManager; ce = CommandExecutor(VersionManager()); result = ce.execute_command('issue', 'list'); print(result['stdout'] if result['success'] else result['stderr'])"
```

## FastMCP Integration Patterns

### Tool Registration
```python
# Use Context7 for FastMCP documentation when implementing:
# - Custom tool decorators
# - Error handling patterns
# - Transport configuration
# - Tool metadata and schemas

# Standard pattern from server.py:
@mcp.tool("tool_name")
def tool_function(param1: str, param2: Optional[int] = None) -> str:
    """Tool description following FastMCP patterns."""
    try:
        # Implementation
        return result
    except Exception as e:
        return f"Error: {str(e)}"
```

### Dynamic Tool Generation
```python
# Pattern from tool_generator.py - use Context7 for:
# - Function metadata manipulation
# - Callable creation patterns
# - Type hint preservation
# - Docstring generation

def generate_tool_function(command_name: str) -> Callable:
    def tool_function(**kwargs) -> str:
        # Dynamic implementation
        pass
    
    # Set metadata for FastMCP
    tool_function.__name__ = f"rad_{command_name}"
    tool_function.__doc__ = generate_help_text(command_name)
    return tool_function
```

## YAML Definition Management

### Schema Validation Patterns
```python
# Use Context7 for PyYAML documentation when:
# - Adding validation rules
# - Implementing custom validators
# - Handling YAML parsing errors
# - Managing version-specific schemas

# Pattern from yaml_loader.py:
def load_definition(version: str) -> CommandDefinition:
    yaml_path = definitions_dir / f"radicle-{version}.yaml"
    
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    
    # Validate against schema
    return CommandDefinition.from_dict(data)
```

### Version Compatibility Testing
```bash
# Test all supported versions
for version in 1.1.0 1.2.0 1.3.0 1.4.0 1.5.0; do
    echo "Testing version $version"
    RAD_VERSION=$version python -c "
from src.yaml_loader import VersionManager
from src.tool_generator import ToolGenerator
vm = VersionManager()
tg = ToolGenerator(vm)
tools = tg.generate_all_tools()
print(f'Version $version: {len(tools)} tools generated')
"
done
```

## Error Handling and Debugging

### MCP-Specific Error Patterns
```python
# Use Context7 for FastMCP error handling patterns:
# - Tool error responses
# - Transport-level errors
# - Client disconnection handling
# - Timeout management

# Pattern from exceptions.py:
class RadicleMCPError(Exception):
    """Base error for Radicle MCP server."""
    pass

class CommandExecutionError(RadicleMCPError):
    """Raised when Radicle command execution fails."""
    pass
```

### Debugging Commands
```bash
# Enable verbose logging
python -m src.server --log-level DEBUG

# Test version detection
python -c "from src.yaml_loader import VersionManager; vm = VersionManager(); print(f'Installed: {vm.get_installed_version()}'); print(f'Supported: {vm.get_supported_versions()}')"

# Test YAML loading
python -c "from src.yaml_loader import VersionManager; vm = VersionManager(); defn = vm.get_current_definition(); print(f'Loaded version: {defn.metadata.version}'); print(f'Commands: {list(defn.commands.keys())}')"

# Test command execution with debugging
python -c "
from src.command_executor import CommandExecutor
from src.yaml_loader import VersionManager
import logging
logging.basicConfig(level=logging.DEBUG)
ce = CommandExecutor(VersionManager())
result = ce.execute_command('issue', 'list')
print('Success:', result['success'])
print('Output:', result['stdout'][:200] if result['success'] else result['stderr'])
"
```

## Testing and Validation

### MCP Tool Testing
```bash
# Test tool generation and schemas
python -c "
from src.tool_generator import ToolGenerator
from src.yaml_loader import VersionManager
tg = ToolGenerator(VersionManager())
tools = tg.generate_all_tools()
schemas = tg.get_tool_schemas()
print(f'Generated {len(tools)} tools with {len(schemas)} schemas')
for tool_name in list(tools.keys())[:5]:  # First 5 tools
    print(f'  {tool_name}: {tools[tool_name].__doc__.split(chr(10))[0] if tools[tool_name].__doc__ else \"No doc\"}')
"

# Test fallback behavior
python -c "
# Simulate version detection failure
import os
os.environ['RAD_VERSION'] = '999.0.0'
from src.tool_generator import ToolGenerator
from src.yaml_loader import VersionManager
tg = ToolGenerator(VersionManager())
tools = tg.generate_all_tools()
print(f'Fallback tools: {list(tools.keys())}')
"
```

### Integration Testing with Context7
```bash
# When working with new dependencies or patterns:
# 1. Use Context7 to get library documentation
# 2. Implement integration following documented patterns
# 3. Test with actual MCP client if available

# Example: Adding new dependency
# uv add new-library
# Use Context7: resolve-library-id "new-library" -> get-library-docs
# Implement integration following documentation
# just test  # Validate integration
```

## Code Generation Patterns

### Dynamic MCP Tool Creation
```python
# Use Context7 for Python function generation patterns:
# - Callable creation with proper signatures
# - Type hint preservation
# - Docstring generation
# - Metadata attachment

# Pattern for generating tools from YAML:
def generate_command_tool(command_name: str, command_def) -> Callable:
    """Generate MCP tool from Radicle command definition."""
    def tool_function(**kwargs) -> str:
        # Execute command with validated arguments
        result = executor.execute_command(command_name, args=kwargs)
        return format_result(result)
    
    # Set FastMCP-required metadata
    tool_function.__name__ = f"rad_{command_name}"
    tool_function.__doc__ = generate_command_help(command_def)
    
    return tool_function
```

### Schema Generation for MCP
```python
# Use Context7 for JSON schema patterns:
# - Type mapping from Python to JSON Schema
# - Validation rule generation
# - Required field handling
# - Enum and default value patterns

def generate_command_schema(command_def) -> Dict[str, Any]:
    """Generate JSON schema for MCP tool validation."""
    properties = {}
    required = []
    
    for opt_name, opt_def in command_def.options.items():
        prop_schema = {
            "type": map_type_to_json(opt_def.type),
            "description": opt_def.description,
        }
        
        if opt_def.choices:
            prop_schema["enum"] = opt_def.choices
        
        properties[opt_name] = prop_schema
        
        if opt_def.required:
            required.append(opt_name)
    
    return {"type": "object", "properties": properties, "required": required}
```

## Common Agent Tasks

### Adding New MCP Tools
1. **Define command in YAML** - Edit appropriate version file
2. **Test definition loading** - Use validation commands above
3. **Generate tool function** - ToolGenerator handles this automatically
4. **Test tool registration** - Run server and check tool list
5. **Test tool execution** - Use MCP client or test functions

### Adding Custom Tools (Beyond YAML Definitions)
For tools that combine multiple Radicle commands or provide custom functionality:

1. **Add to server.py fallback section** - Custom tools go in `_register_fallback_tools()`
2. **Use existing infrastructure** - Leverage `CommandExecutor` and `VersionManager`
3. **Implement comprehensive error handling** - Follow existing patterns with specific error messages
4. **Use declarative code style** - Prefer comprehensions, data structures, and clear naming over comments
5. **Test with edge cases** - No repository, auth issues, network problems, empty results

Example custom tool pattern:
```python
@self.mcp.tool("rad_custom_tool")
def rad_custom_tool() -> str:
    """Custom tool description."""
    
    def validate_environment() -> str | None:
        # Environment validation logic
        return None
    
    def execute_safely() -> Dict[str, Any]:
        # Safe command execution with error handling
        return {}
    
    def format_results(data: Dict[str, Any]) -> str:
        # Clean, declarative result formatting
        return ""
    
    # Main execution flow
    validation_error = validate_environment()
    if validation_error:
        return validation_error
    
    result = execute_safely()
    return format_results(result)
```

### Debugging Version Issues
1. **Check installed Radicle version** - `rad --version`
2. **Verify version detection** - Use VersionManager test commands
3. **Check YAML definition exists** - Look in `src/definitions/`
4. **Validate YAML syntax** - `just validate-yaml`
5. **Test fallback behavior** - Simulate unsupported version

### Performance Optimization
1. **Profile tool generation** - Time the `generate_all_tools()` call
2. **Cache YAML definitions** - VersionManager already handles this
3. **Optimize command execution** - Review CommandExecutor patterns
4. **Test with large repositories** - Ensure sync commands work properly

## Context7 Usage Examples

### When Working with FastMCP
```bash
# Get tool registration patterns
context7_resolve-library-id "fastmcp"
context7_get-library-docs "/fastmcp/fastmcp" topic="tool registration"

# Get error handling patterns
context7_get-library-docs "/fastmcp/fastmcp" topic="error handling"

# Get transport configuration
context7_get-library-docs "/fastmcp/fastmcp" topic="transport configuration"
```

### When Working with PyYAML
```bash
# Get schema validation patterns
context7_resolve-library-id "pyyaml"
context7_get-library-docs "/pyyaml/pyyaml" topic="schema validation"

# Get custom tag handling
context7_get-library-docs "/pyyaml/pyyaml" topic="custom tags"
```

### When Working with attrs
```bash
# Get dataclass patterns
context7_resolve-library-id "attrs"
context7_get-library-docs "/python-attrs/attrs" topic="dataclass"

# Get validation patterns
context7_get-library-docs "/python-attrs/attrs" topic="validation"
```

## Code Quality Standards

### Comments Policy
**Use comments sparingly.** Only add comments when:
- The intention of the code is not immediately clear from reading it
- An obvious-looking alternative approach is not actually suitable (explain why)

**Prefer these alternatives to comments:**
1. **Proper variable naming**: Use descriptive names that explain purpose
2. **Refactor into named functions**: Extract complex logic into well-named functions
3. **Docstrings**: Document public APIs, function parameters, return values, and exceptions

Good code should be self-documenting through clear structure and naming. Comments should be reserved for explaining "why" not "what" when the "why" isn't obvious.

### Declarative Code Patterns
- **Use comprehensions** instead of loops with append statements
- **Prefer data structures** over imperative building
- **Use pattern matching** and conditional expressions
- **Extract complex logic** into well-named helper functions
- **Avoid unnecessary intermediate variables** when expressions are clear

### Error Handling Standards
- **Provide specific error messages** with actionable solutions
- **Use consistent formatting** with emoji and markdown for clarity
- **Include diagnostic information** for advanced users
- **Implement graceful degradation** when possible
- **Follow existing exception hierarchy** and error patterns

This guide enables agents to effectively work with the Radicle MCP Server while leveraging Context7 for library documentation and code generation needs.
