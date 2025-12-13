#!/usr/bin/env python3
"""Test schema generation fix."""

import sys
import os

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

from tool_generator import ToolGenerator
from yaml_loader import VersionManager

# Test that issue show schema includes positional args
vm = VersionManager()
tg = ToolGenerator(vm, None)
definition = vm.get_current_definition()
issue_cmd = definition.commands["issue"]
show_subcmd = issue_cmd.subcommands["show"]

schema = tg._generate_subcommand_schema("issue", issue_cmd, "show", show_subcmd)

print("SUCCESS: Schema properties:", list(schema["properties"].keys()))
print("SUCCESS: Required:", schema["required"])
print("SUCCESS: Has id:", "id" in schema["properties"])
print("SUCCESS: Id required:", "id" in schema["required"])
