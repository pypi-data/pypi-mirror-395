# CLI Contract Testing

## Overview

CLI Contract Tests validate that our YAML command definitions match the actual `rad` CLI interface. These tests prevent bugs like the `--status` parameter issue where YAML definitions incorrectly described CLI options.

## Purpose

**Problem**: YAML definitions can drift from actual CLI behavior, causing:
- Commands that fail at runtime
- Incorrect tool parameter types
- Confusing user experience

**Solution**: Automated tests that compare YAML against `rad --help` output

## Test Structure

```
tests/cli_contract/
├── __init__.py
├── conftest.py              # Fixtures (rad_cli_available, yaml_command_def)
├── cli_parser.py            # Parser for rad --help output
├── test_issue_contract.py   # Issue command contracts
└── test_patch_contract.py   # Patch command contracts (TODO)
```

## Running Tests

### Run all CLI contract tests:
```bash
uv run python -m pytest tests/cli_contract/ -v
```

### Run specific test class:
```bash
uv run python -m pytest tests/cli_contract/test_issue_contract.py::TestIssueListContract -v
```

### Skip if rad CLI not installed:
Tests automatically skip if `rad` CLI is not available. No configuration needed.

### Filter by marker:
```bash
# Run only CLI contract tests
uv run python -m pytest -m cli_contract

# Run only tests requiring rad CLI
uv run python -m pytest -m requires_rad
```

## Test Coverage

### Current (v1.5.0):

**Issue Command:**
- ✅ `issue list` - Flag types for status filtering
- ✅ `issue list` - Mutually exclusive flags (--all | --closed | --open | --solved)
- ✅ `issue open` - Required title parameter
- ✅ `issue open` - Optional parameters (description, label)
- ✅ `issue state` - Mutually exclusive state flags

**Patch Command:**
- 🔲 `patch list` - Flag types (TODO)
- 🔲 `patch list` - Mutually exclusive flags (TODO)
- 🔲 `patch open` - Required parameters (TODO)

### Future Expansion:
- Additional subcommands (comment, assign, label, etc.)
- Other commands (node, cob, sync, etc.)
- Multiple Radicle versions (1.4.0, 1.6.0, etc.)

## How It Works

### 1. CLI Parser (`cli_parser.py`)

Parses `rad <command> <subcommand> --help` output to extract:
- Option names and types (flag vs string)
- Mutually exclusive option groups
- Positional arguments
- Required vs optional parameters

```python
# Example usage
from cli_parser import CLIHelpParser

cli_spec = CLIHelpParser.parse_command_help("issue", "list")
print(cli_spec.options)  # Dict of OptionSpec objects
print(cli_spec.mutually_exclusive_groups)  # [['all', 'closed', 'open', 'solved']]
```

### 2. Test Fixtures (`conftest.py`)

**`rad_cli_available`**: Checks if rad CLI is installed, skips tests if not

**`rad_version`**: Verifies rad version is 1.5.0+

**`yaml_command_def`**: Helper to load command definitions from YAML

### 3. Contract Tests (`test_issue_contract.py`)

Each test compares YAML against CLI:

```python
def test_issue_list_uses_flag_types(self, rad_version, yaml_command_def):
    yaml_spec = yaml_command_def("issue", "list")
    
    # Verify status flags are type 'flag' not 'string'
    for flag_name in ["all", "closed", "open", "solved"]:
        assert flag_name in yaml_spec.options
        assert yaml_spec.options[flag_name].type == "flag"
```

## Example: Bug Prevention

### The Original Bug

**YAML Definition (Incorrect)**:
```yaml
list:
  options:
    status:
      type: "string"
      choices: ["open", "closed", "all"]
```

**Actual CLI**:
```
rad issue list [--all | --closed | --open | --solved]
```

**Result**: `rad issue list --status open` fails - option doesn't exist!

### How Contract Tests Catch This

```python
def test_issue_list_uses_flag_types(self, rad_version, yaml_command_def):
    yaml_spec = yaml_command_def("issue", "list")
    
    # This assertion would FAIL with incorrect YAML:
    assert yaml_spec.options["open"].type == "flag"
    # Error: KeyError: 'open' (because YAML has 'status' instead)
```

**Test Output**:
```
FAILED test_issue_list_uses_flag_types
AssertionError: Option 'open' should be type 'flag' but is 'string'.
The CLI uses mutually exclusive flags: --all | --closed | --open | --solved

Fix in radicle-1.5.0.yaml:
  list:
    options:
      open:
        type: flag
        description: Show only open issues
```

## Adding New Tests

### 1. Identify High-Risk Commands

Focus on commands with:
- Complex option structures
- Mutually exclusive flags
- Frequently used operations
- Recent changes in Radicle CLI

### 2. Write Test Class

```python
@pytest.mark.cli_contract
@pytest.mark.requires_rad
class TestMyCommandContract:
    """Test my-command contract."""
    
    def test_my_subcommand_options(self, rad_version, yaml_command_def):
        """Verify options match CLI."""
        yaml_spec = yaml_command_def("my-command", "my-subcommand")
        cli_spec = CLIHelpParser.parse_command_help("my-command", "my-subcommand")
        
        # Add your assertions here
        assert "my-option" in yaml_spec.options
```

### 3. Run and Iterate

```bash
uv run python -m pytest tests/cli_contract/test_my_contract.py -xvs
```

## Maintenance

### When rad CLI Updates

1. Run all contract tests: `uv run python -m pytest tests/cli_contract/ -v`
2. Review failures - are they bugs or legitimate changes?
3. Update YAML definitions if CLI changed
4. Add new tests for new commands/options

### When Adding New Commands to YAML

1. Write contract test FIRST
2. Run test (should fail)
3. Implement YAML definition
4. Run test again (should pass)

This TDD approach ensures YAML matches CLI from the start.

## Limitations

### Current Implementation

1. **Parser Brittleness**: Help output format changes could break parser
2. **Version-Specific**: Only tests rad 1.5.0+ currently
3. **Partial Coverage**: Only high-risk commands tested
4. **Option Filtering**: Parser may extract options from wrong sections

### Future Improvements

1. More robust parsing (handle multiple help formats)
2. Test multiple Radicle versions
3. Auto-generate YAML from CLI help
4. Integration with CI/CD
5. Comprehensive coverage of all commands

## Troubleshooting

### Tests Skip with "rad CLI not installed"

**Solution**: Install Radicle CLI or run tests in environment with rad

### Test Fails After Radicle Update

**Expected**: CLI may have changed
**Action**: Review failure message, update YAML if CLI changed

### Parser Errors

**Problem**: Help output format not recognized
**Solution**: Update regex patterns in `cli_parser.py`

### False Positives

**Problem**: Test fails but YAML is correct
**Cause**: Parser extracting wrong options
**Solution**: Refine parser logic or update test assertions

## Benefits

✅ **Prevents bugs** like the --status parameter issue
✅ **Living documentation** of CLI interface
✅ **Confidence** when updating YAML definitions  
✅ **Regression prevention** for future changes
✅ **Guidance** for contributors on YAML structure

## Related Documentation

- [BUG_FIX_STATUS_PARAMETER.md](./BUG_FIX_STATUS_PARAMETER.md) - Original bug that motivated these tests
- [YAML_SCHEMA.md](./YAML_SCHEMA.md) - YAML definition format
- [VERSION_COMPATIBILITY.md](./VERSION_COMPATIBILITY.md) - Version management

## Questions?

- What commands should be tested next?
- Should we test older Radicle versions?
- How can we make the parser more robust?

Discuss in project issues or documentation updates.
