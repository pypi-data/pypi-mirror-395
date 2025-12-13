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

            # Only parse main command options if there are no subcommands
            # Commands with subcommands should not have their own options
            main_cmd_options = {}
            if not cmd_data.get("subcommands"):
                main_cmd_options = _parse_options(cmd_data.get("options", {}))

            commands[cmd_name] = Command(
                name=cmd_name,
                help=cmd_data.get("help", ""),
                subcommands=subcommands,
                options=main_cmd_options,
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
            takes_value=opt_data.get("type") != "flag",
        )

    return options


def _parse_positional_args(
    positional_args_data: list[dict[str, Any]],
) -> list[PositionalArg]:
    """Parse YAML positional args data into PositionalArg objects with validation."""
    args = []
    for arg_data in positional_args_data:
        args.append(
            PositionalArg(
                name=arg_data.get("name", ""),
                type=arg_data.get("type", "string"),
                description=arg_data.get("description", ""),
                required=arg_data.get("required", False),
            )
        )

    return args
