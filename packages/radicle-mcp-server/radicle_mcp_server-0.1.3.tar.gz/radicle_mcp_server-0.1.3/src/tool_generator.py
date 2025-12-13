"""Dynamic MCP tool generation from YAML definitions."""

from __future__ import annotations

import keyword
from collections.abc import Callable
from typing import Any, cast

from .definitions.schema import Command
from .exceptions import CommandNotFoundError, VersionNotSupportedError
from .protocols import (
    VersionManagerProtocol,
    CommandExecutorProtocol,
)


class ToolGenerator:
    """Generates MCP tools dynamically from Radicle command definitions."""

    version_manager: VersionManagerProtocol
    executor: CommandExecutorProtocol

    def __init__(
        self, version_manager: VersionManagerProtocol, executor: CommandExecutorProtocol
    ):
        """Initialize tool generator with version manager and command executor."""
        self.version_manager = version_manager
        self.executor = executor

    def generate_all_tools(self) -> dict[str, Callable[..., str]]:
        """Generate MCP tools for all available commands.

        Returns:
            Dictionary mapping tool names to tool functions
        """
        tools = {}

        try:
            definition = self.version_manager.get_current_definition()

            for command_name, command_def in definition.commands.items():
                main_tool = self._generate_command_tool(command_name, command_def)
                tools[f"rad_{command_name}"] = main_tool

                for subcommand_name, subcommand_def in command_def.subcommands.items():
                    subcommand_tool = self._generate_subcommand_tool(
                        command_name, command_def, subcommand_name, subcommand_def
                    )
                    tools[f"rad_{command_name}_{subcommand_name}"] = subcommand_tool

        except (VersionNotSupportedError, CommandNotFoundError):
            # Return basic tools even if version detection fails
            tools.update(self._generate_fallback_tools())

        return cast(dict[str, Callable[..., str]], tools)  # Dynamic tool generation

    def _generate_command_tool(self, command_name: str, command_def: Command):
        """Generate MCP tool function from Radicle command definition.

        Creates Python function dynamically using exec() with explicit parameters
        mapped from command_def options and positional_args. Generated function
        validates arguments, executes via CommandExecutor, and formats output.

        Process:
        1. Build parameter signature from options and positional_args
        2. Generate function code string with validation logic
        3. Execute code to create function object with proper types
        4. Set __name__ and __doc__ attributes for MCP registration

        Note: This method uses dynamic code generation which inherently involves
        Any types and untyped string operations. Type warnings are expected and
        suppressed for dynamic generation sections.
        """
        # Dynamic parameter generation - type warnings expected and suppressed
        param_lines: list[str] = []  # Dynamic code generation

        # Add positional arguments first
        for pos_arg in command_def.positional_args or []:
            param_name = self._sanitize_parameter_name(pos_arg.name)
            python_type = self._map_radicle_type_to_python_type(
                pos_arg.type
            )  # Dynamic type mapping

            if pos_arg.required:
                param_lines.append(f"        {param_name}: {python_type.__name__}")
            else:
                param_lines.append(
                    f"        {param_name}: {python_type.__name__} | None = None"
                )

        # Add command options as parameters
        for opt_name, opt_def in command_def.options.items():
            param_name = self._sanitize_parameter_name(opt_name)
            python_type = self._map_radicle_type_to_python_type(opt_def.type)

            if opt_def.required:
                param_lines.append(f"        {param_name}: {python_type.__name__}")
            else:
                default_val = (
                    repr(opt_def.default) if opt_def.default is not None else "None"
                )
                param_lines.append(
                    f"        {param_name}: {python_type.__name__} | None = {default_val}"
                )

        # Join parameters with type ignore for dynamic string operations
        params_str = ",\n".join(param_lines)
        if params_str:
            params_str = "\n" + params_str + "\n    "

        # Create function with explicit parameters
        option_lines: list[str] = []
        for opt_name in command_def.options.keys():
            param_name = self._sanitize_parameter_name(opt_name)
            option_lines.append(
                f'        if {param_name} is not None:\n            executor_kwargs["{opt_name}"] = {param_name}'
            )

        positional_lines: list[str] = []
        for pos_arg in command_def.positional_args or []:
            param_name = self._sanitize_parameter_name(pos_arg.name)
            positional_lines.append(
                f'        if {param_name} is not None:\n            executor_kwargs["{pos_arg.name}"] = {param_name}'
            )

        # Dynamic function code generation - suppress all type warnings for this section
        function_code = f'''def tool_function({params_str}) -> str:
    """Execute 'rad {command_name}' command."""
    try:
        executor_kwargs = {{}}
        
        # Add positional arguments
{chr(10).join(positional_lines)}  
        
        # Add command options
{chr(10).join(option_lines)}  
        
        result = self.executor.execute_command(
            command="{command_name}",
            args=executor_kwargs,
            cwd=None  # Will auto-detect current Radicle repository
        )

        if result["success"]:
            output = result["stdout"]
            if result["parsed_output"]:
                output += f"\\n\\n[Parsed Output]\\n{{result['parsed_output']}}"
            return output
        else:
            return f"Command failed: {{result['stderr']}}"
            
    except Exception as e:
        return f"Error executing {command_name}: {{str(e)}}"
'''

        local_scope = {"self": self}
        exec(function_code, local_scope)
        tool_function = local_scope["tool_function"]

        setattr(tool_function, "__name__", f"rad_{command_name}")
        setattr(
            tool_function,
            "__doc__",
            self._generate_command_help(command_name, command_def),
        )

        return tool_function

    def _generate_subcommand_tool(
        self, command_name: str, command_def: Command, subcommand_name: str, subcommand_def: Command
    ):
        """Generate MCP tool function for Radicle subcommand.

        Similar to _generate_command_tool but handles subcommand-specific
        parameter mapping and execution. Combines main command with subcommand
        for proper CLI invocation via CommandExecutor.

        Args:
            command_name: Main command name (e.g., "issue", "patch")
            command_def: Main command definition (for inheriting command-level options)
            subcommand_name: Subcommand name (e.g., "open", "list")
            subcommand_def: Subcommand definition with specific options

        Returns:
            Callable function named 'rad_{command}_{subcommand}' with
            proper parameter validation and help text generation
        """
        # Build explicit parameters from subcommand definition
        # Python requires: required params first, then optional params with defaults
        required_param_lines = []
        optional_param_lines = []

        # Add positional arguments first
        for pos_arg in subcommand_def.positional_args or []:
            param_name = self._sanitize_parameter_name(pos_arg.name)
            python_type = self._map_radicle_type_to_python_type(pos_arg.type)

            if pos_arg.required:
                required_param_lines.append(f"        {param_name}: {python_type.__name__}")
            else:
                optional_param_lines.append(
                    f"        {param_name}: {python_type.__name__} | None = None"
                )

        # Merge command-level options with subcommand options
        # Command-level options are inherited by all subcommands
        all_options = {**command_def.options, **subcommand_def.options}

        # Add merged options as parameters, separated by required/optional
        for opt_name, opt_def in all_options.items():
            param_name = self._sanitize_parameter_name(opt_name)
            python_type = self._map_radicle_type_to_python_type(opt_def.type)

            if opt_def.required:
                required_param_lines.append(f"        {param_name}: {python_type.__name__}")
            else:
                default_val = (
                    repr(opt_def.default) if opt_def.default is not None else "None"
                )
                optional_param_lines.append(
                    f"        {param_name}: {python_type.__name__} | None = {default_val}"
                )

        # Combine required params first, then optional params
        param_lines = required_param_lines + optional_param_lines

        # All parameters already include positional args and options in correct order
        all_param_lines = param_lines

        # Join parameters
        params_str = ",\n".join(all_param_lines)
        if params_str:
            params_str = "\n" + params_str + "\n    "

        # Create option lines for function body (includes inherited command-level options)
        option_lines = []
        for opt_name in all_options.keys():
            param_name = self._sanitize_parameter_name(opt_name)
            option_lines.append(
                f'        if {param_name} is not None:\n            executor_kwargs["{opt_name}"] = {param_name}'
            )

        # Create positional arguments for function body
        positional_lines = []
        for pos_arg in subcommand_def.positional_args or []:
            param_name = self._sanitize_parameter_name(pos_arg.name)
            positional_lines.append(
                f'        if {param_name} is not None:\n            executor_kwargs["{pos_arg.name}"] = {param_name}'
            )

        # Create function with explicit parameters
        function_code = f'''def tool_function({params_str}) -> str:
    """Execute 'rad {command_name} {subcommand_name}' command."""
    try:
        executor_kwargs = {{}}
        
        # Add positional arguments
{chr(10).join(positional_lines)}
        
        # Add subcommand options
{chr(10).join(option_lines)}
        
        result = self.executor.execute_command(
            command="{command_name}",
            subcommand="{subcommand_name}",
            args=executor_kwargs,
            cwd=None  # Will auto-detect current Radicle repository
        )
        
        if result["success"]:
            output = result["stdout"]
            if result["parsed_output"]:
                output += f"\\n\\n[Parsed Output]\\n{{result['parsed_output']}}"
            return output
        else:
            return f"Command failed: {{result['stderr']}}"
            
    except Exception as e:
            return f"Error executing {command_name} {subcommand_name}: {{str(e)}}"
'''

        local_scope = {"self": self}
        exec(function_code, local_scope)
        tool_function = local_scope["tool_function"]

        setattr(tool_function, "__name__", f"rad_{command_name}_{subcommand_name}")
        setattr(
            tool_function,
            "__doc__",
            self._generate_subcommand_help(
                command_name, command_def, subcommand_name, subcommand_def
            ),
        )

        return tool_function

    def _generate_command_help(self, command_name: str, command_def: Command) -> str:
        """Generate help text for a command tool.

        Args:
            command_name: Name of command
            command_def: Command definition

        Returns:
            Help text for tool
        """
        help_text = f"Execute 'rad {command_name}' command.\n\n"
        help_text += f"Description: {command_def.help}\n\n"

        if command_def.positional_args:
            help_text += "Positional Arguments:\n"
            for pos_arg in command_def.positional_args:
                required_text = " (required)" if pos_arg.required else ""
                help_text += f"  {pos_arg.name}: {pos_arg.description}{required_text}\n"

        if command_def.options:
            help_text += "\nOptions:\n"
            for opt_name, opt_def in command_def.options.items():
                required_text = " (required)" if opt_def.required else ""
                default_text = (
                    f" (default: {opt_def.default})"
                    if opt_def.default is not None
                    else ""
                )
                help_text += f"  --{opt_name}: {opt_def.description}{required_text}{default_text}\n"

        if command_def.examples:
            help_text += "\nExamples:\n"
            for example in command_def.examples:
                help_text += f"  {example}\n"

        return help_text

    def _generate_subcommand_help(
        self, command_name: str, command_def: Command, subcommand_name: str, subcommand_def: Command
    ) -> str:
        """Generate help text for a subcommand tool.

        Args:
            command_name: Name of main command
            command_def: Main command definition (for inheriting command-level options)
            subcommand_name: Name of subcommand
            subcommand_def: Subcommand definition

        Returns:
            Help text for tool
        """
        help_text = f"Execute 'rad {command_name} {subcommand_name}' subcommand.\n\n"
        help_text += f"Description: {subcommand_def.help}\n\n"

        if subcommand_def.positional_args:
            help_text += "Positional Arguments:\n"
            for pos_arg in subcommand_def.positional_args:
                required_text = " (required)" if pos_arg.required else ""
                help_text += f"  {pos_arg.name}: {pos_arg.description}{required_text}\n"

        # Merge command-level options with subcommand options for help text
        all_options = {**command_def.options, **subcommand_def.options}

        if all_options:
            help_text += "\nOptions:\n"
            for opt_name, opt_def in all_options.items():
                required_text = " (required)" if opt_def.required else ""
                default_text = (
                    f" (default: {opt_def.default})"
                    if opt_def.default is not None
                    else ""
                )
                help_text += f"  --{opt_name}: {opt_def.description}{required_text}{default_text}\n"

        if subcommand_def.examples:
            help_text += "\nExamples:\n"
            for example in subcommand_def.examples:
                help_text += f"  {example}\n"

        return help_text

    def _generate_fallback_tools(self) -> dict[str, Callable[..., str]]:
        """Generate basic fallback tools when version detection fails.

        Returns:
            Dictionary of fallback tool functions
        """

        def rad_execute(
            command: str,
            subcommand: str | None = None,
            args: dict[str, Any] | None = None,  # pyright: ignore[reportExplicitAny]  # External input
        ) -> str:
            """Execute any rad command with given arguments."""
            try:
                if args is None:
                    args = {}

                if subcommand:
                    result = self.executor.execute_command(
                        command=command, subcommand=subcommand, args=args
                    )
                else:
                    result = self.executor.execute_command(command=command, args=args)

                if result["success"]:
                    return result["stdout"]
                else:
                    return f"Command failed: {result['stderr']}"

            except Exception as e:
                return f"Error executing command: {str(e)}"

        def rad_version() -> str:
            """Get Radicle version information."""
            try:
                version = self.version_manager.get_installed_version()
                return f"Radicle version: {version}"
            except Exception as e:
                return f"Error getting version: {str(e)}"

        def rad_help(command: str | None = None) -> str:
            """Get help for rad commands."""
            try:
                if command:
                    result = self.executor.execute_command(
                        command="help", args={"command": command}
                    )
                else:
                    result = self.executor.execute_command(command="help")

                return result["stdout"] if result["success"] else result["stderr"]
            except Exception as e:
                return f"Error getting help: {str(e)}"

        return {
            "rad_execute": rad_execute,
            "rad_version": rad_version,
            "rad_help": rad_help,
        }

    def get_tool_schemas(self) -> dict[str, dict[str, Any]]:  # pyright: ignore[reportExplicitAny]  # MCP schema format
        """Generate JSON schemas for all tools.

        Returns:
            Dictionary mapping tool names to their JSON schemas
        """
        schemas = {}

        try:
            definition = self.version_manager.get_current_definition()

            for command_name, command_def in definition.commands.items():
                # Main command schema
                schemas[f"rad_{command_name}"] = self._generate_command_schema(
                    command_name, command_def
                )

                # Subcommand schemas
                for subcommand_name, subcommand_def in command_def.subcommands.items():
                    schemas[f"rad_{command_name}_{subcommand_name}"] = (
                        self._generate_subcommand_schema(
                            command_name, command_def, subcommand_name, subcommand_def
                        )
                    )

        except (VersionNotSupportedError, CommandNotFoundError):
            # Fallback schemas
            schemas.update(self._generate_fallback_schemas())

        return schemas

    def _generate_command_schema(
        self, command_name: str, command_def: Command
    ) -> dict[str, Any]:  # pyright: ignore[reportExplicitAny]  # JSON schema format
        """Generate JSON schema for a command tool.

        Args:
            command_name: Name of command
            command_def: Command definition

        Returns:
            JSON schema dictionary
        """
        properties: dict[str, Any] = {}  # pyright: ignore[reportExplicitAny]  # JSON schema properties
        required: list[str] = []

        for opt_name, opt_def in command_def.options.items():
            prop_schema: dict[str, Any] = {  # pyright: ignore[reportExplicitAny]  # JSON schema property
                "type": self._map_type_to_json_type(opt_def.type),
                "description": opt_def.description,
            }

            if opt_def.default is not None:
                prop_schema["default"] = opt_def.default

            if opt_def.choices:
                prop_schema["enum"] = opt_def.choices

            properties[opt_name] = prop_schema

            if opt_def.required:
                required.append(opt_name)

        # Add common positional arguments
        if command_name in ["issue", "patch"]:
            properties["id"] = {
                "type": "string",
                "description": f"{command_name.title()} ID",
            }

        if command_name == "node":
            properties["peer"] = {
                "type": "string",
                "description": "Peer address or DID",
            }

        return {"type": "object", "properties": properties, "required": required}

    def _generate_subcommand_schema(
        self, command_name: str, command_def: Command, subcommand_name: str, subcommand_def: Command
    ) -> dict[str, Any]:  # pyright: ignore[reportExplicitAny]  # JSON schema format
        """Generate JSON schema for a subcommand tool.

        Args:
            command_name: Name of main command
            command_def: Main command definition (for inheriting command-level options)
            subcommand_name: Name of subcommand
            subcommand_def: Subcommand definition

        Returns:
            JSON schema dictionary
        """
        properties: dict[str, Any] = {}  # pyright: ignore[reportExplicitAny]  # JSON schema properties
        required: list[str] = []

        # Merge command-level options with subcommand options
        all_options = {**command_def.options, **subcommand_def.options}

        for opt_name, opt_def in all_options.items():
            prop_schema: dict[str, Any] = {  # pyright: ignore[reportExplicitAny]  # JSON schema property
                "type": self._map_type_to_json_type(opt_def.type),
                "description": opt_def.description,
            }

            if opt_def.default is not None:
                prop_schema["default"] = opt_def.default

            if opt_def.choices:
                prop_schema["enum"] = opt_def.choices

            properties[opt_name] = prop_schema

            if opt_def.required:
                required.append(opt_name)

        if subcommand_name in [
            "show",
            "edit",
            "delete",
            "checkout",
            "update",
            "merge",
            "review",
        ]:
            properties["id"] = {
                "type": "string",
                "description": f"{command_name.title()} ID",
            }
            required.append("id")

        if command_name == "config" and subcommand_name in ["get", "set"]:
            if subcommand_name == "get":
                properties["key"] = {
                    "type": "string",
                    "description": "Configuration key",
                }
                required.append("key")
            elif subcommand_name == "set":
                properties["key"] = {
                    "type": "string",
                    "description": "Configuration key",
                }
                properties["value"] = {
                    "type": "string",
                    "description": "Configuration value",
                }
                required.extend(["key", "value"])

        return {"type": "object", "properties": properties, "required": required}

    def _generate_fallback_schemas(self) -> dict[str, dict[str, Any]]:  # pyright: ignore[reportExplicitAny]  # JSON schema format
        """Generate fallback schemas when version detection fails.

        Returns:
            Dictionary of fallback schemas
        """
        return {
            "rad_execute": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Radicle command to execute",
                    },
                    "subcommand": {
                        "type": "string",
                        "description": "Optional subcommand",
                    },
                },
                "required": ["command"],
            },
            "rad_version": {"type": "object", "properties": {}, "required": []},
            "rad_help": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Optional command to get help for",
                    }
                },
                "required": [],
            },
        }

    def _map_type_to_json_type(self, radicle_type: str) -> str:
        """Map Radicle option type to JSON schema type for MCP validation."""
        type_mapping = {
            "string": "string",
            "int": "integer",
            "flag": "boolean",
            "list": "array",
        }

        return type_mapping.get(radicle_type, "string")

    def _map_radicle_type_to_python_type(self, radicle_type: str) -> Any:  # pyright: ignore[reportExplicitAny]  # Dynamic type mapping
        """Map Radicle option type to Python type."""
        type_mapping = {
            "string": str,
            "int": int,
            "flag": bool,
            "list": list[str],
        }
        return type_mapping.get(radicle_type, str)

    def _sanitize_parameter_name(self, param_name: str) -> str:
        """Avoid Python keyword conflicts by appending '_param' suffix."""
        if param_name in keyword.kwlist:
            return f"{param_name}_param"
        return param_name
