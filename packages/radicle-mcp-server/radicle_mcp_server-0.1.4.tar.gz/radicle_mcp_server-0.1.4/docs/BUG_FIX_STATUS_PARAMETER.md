# Bug Fix: Issue and Patch List Status Parameter

## Problem

The `rad_issue_list` and `rad_patch_list` commands were failing when the `status` parameter was used. The YAML definitions incorrectly defined status filtering as a single string option with choices, but the actual Radicle CLI uses mutually exclusive flag options.

### Incorrect Definition (Before)

```yaml
list:
  options:
    status:
      type: "string"
      description: "Filter by status"
      required: false
      choices: ["open", "closed", "all"]
```

This would generate commands like:
- `rad issue list --status open` ❌ (fails - option doesn't exist)

### Actual CLI Syntax

According to `rad issue list --help`:
```
rad issue list [--assigned <did>] [--all | --closed | --open | --solved] [<option>...]
```

According to `rad patch list --help`:
```
rad patch list [--all|--merged|--open|--archived|--draft] [<option>...]
```

## Solution

Changed the YAML definitions to use separate flag options for each status value:

### Correct Definition (After)

```yaml
list:
  options:
    all:
      type: "flag"
      description: "Show all issues"
      required: false
    closed:
      type: "flag"
      description: "Show only closed issues"
      required: false
    open:
      type: "flag"
      description: "Show only open issues"
      required: false
    solved:
      type: "flag"
      description: "Show only solved issues"
      required: false
    json:
      type: "flag"
      description: "Output in JSON format"
      required: false
```

This generates the correct commands:
- `rad issue list --open` ✅
- `rad issue list --closed` ✅
- `rad patch list --merged` ✅

## Files Changed

All Radicle version definitions were updated:

- `src/definitions/radicle-1.1.0.yaml` - Fixed issue list and patch list
- `src/definitions/radicle-1.2.0.yaml` - Fixed issue list and patch list  
- `src/definitions/radicle-1.3.0.yaml` - Fixed issue list and patch list
- `src/definitions/radicle-1.4.0.yaml` - Fixed issue list and patch list
- `src/definitions/radicle-1.5.0.yaml` - Fixed issue list and patch list

The fix was applied programmatically using a Python script to ensure consistency across all versions.

## Testing

All existing tests continue to pass after the fix. The `rad_issue_list` and `rad_patch_list` tools now correctly accept flag-based status filtering options that match the actual Radicle CLI interface.

## Root Cause

The YAML definitions were created based on an assumption about how status filtering would work, rather than by examining the actual CLI help output. This highlights the importance of verifying command line interfaces against actual help documentation.
