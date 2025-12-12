"""Custom exceptions for Radicle MCP Server."""


class RadicleMCPError(Exception):
    """Base exception for all Radicle MCP Server operations.

    All specific errors inherit from this class to enable unified
    exception handling in MCP client integrations.
    """


class VersionNotSupportedError(RadicleMCPError):
    """Raised when installed Radicle version lacks definition file.

    Triggers fallback tool registration with basic rad_execute functionality.
    """


class CommandNotFoundError(RadicleMCPError):
    """Raised when requested command not found in current version definition.

    Indicates command may be deprecated, added in newer version, or misnamed.
    """


class InvalidArgumentError(RadicleMCPError):
    """Raised when command arguments fail validation against definition.

    Covers missing required options, invalid types, or unknown parameters.
    """


class CommandExecutionError(RadicleMCPError):
    """Raised when Radicle CLI command execution fails.

    Covers subprocess failures, timeouts, and non-zero return codes.
    """


class YAMLDefinitionError(RadicleMCPError):
    """Raised when YAML definition file has syntax or schema errors.

    Indicates malformed YAML, missing required fields, or invalid structure.
    """


class RadicleNotInstalledError(RadicleMCPError):
    """Raised when Radicle CLI not found or not functioning properly.

    Covers missing binary, PATH issues, or version command failures.
    """
