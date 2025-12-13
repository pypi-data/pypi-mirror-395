# Version Compatibility Guide

This document describes how the Radicle MCP Server handles version compatibility across different Radicle CLI versions.

## Supported Versions

The server supports the following Radicle versions:

### Current Stable (1.5.0)
- **Release Date**: 2025-09-04
- **Code Name**: Lily
- **Breaking Changes**: No
- **Migration Required**: No
- **Key Features**: All current features

### Previous Versions

#### 1.4.0 (Lily)
- **Release Date**: 2025-09-04
- **Breaking Changes**: No
- **Key Features**: 
  - Fixed panics in serialization and SQLite operations
  - Improved bootstrapping with IPv6/IPv4/Tor support
  - Better `rad sync` status output
  - Enhanced `rad cob log` options

#### 1.3.0 (Lily)
- **Release Date**: 2025-08-16
- **Breaking Changes**: No
- **Key Features**:
  - **Native Windows support** (no WSL requirement)
  - **Canonical References** - major governance feature
  - Protocol layer refactor with `radicle-protocol` crate
  - Improved `rad cob log` with `--from` and `--to` options

#### 1.2.0
- **Release Date**: 2025-06-02
- **Breaking Changes**: No
- **Key Features**:
  - **JSON output** for `rad cob` commands
  - **Multiple RIDs** support for `rad seed`/`rad unseed`
  - **Improved sync** with better status symbols
  - `rad config schema` for JSON schema output
  - Enhanced patch management with edit capabilities

#### 1.1.0
- **Release Date**: 2024-12-05
- **Breaking Changes**: **Yes**
- **Migration Required**: **Yes**
- **Key Features**:
  - **Database migration** to COB database version 2
  - `rad cob migrate` command
  - `--edit` flag for `rad id update`
  - `--storage` flag for cache commands
  - Enhanced `rad config` with subcommands
  - New `--remote` option for patch operations

## Version Detection Strategy

The server uses a hierarchical approach to version detection:

### 1. Exact Version Match
- Tries to load YAML definition for exact installed version
- Example: If Radicle 1.4.0 is installed, loads `radicle-1.4.0.yaml`

### 2. Closest Version Match
- If exact version is not supported, finds the closest supported version
- Uses semantic version comparison (major.minor)
- Falls back to older versions for compatibility

### 3. Fallback Mode
- If version detection fails completely, provides generic tools
- Uses `rad_execute`, `rad_version`, `rad_help` tools
- Allows manual command execution without version-specific features

## Feature Availability by Version

### Core Commands (Available in all versions)
- `rad auth` - Identity management
- `rad block` - Peer blocking
- `rad checkout` - Repository checkout
- `rad clone` - Repository cloning
- `rad fork` - Repository forking
- `rad help` - Help system
- `rad id` - Identity operations
- `rad init` - Repository initialization
- `rad inbox` - Notification management
- `rad inspect` - Repository inspection
- `rad issue` - Issue management
- `rad ls` - Repository listing
- `rad node` - Node management
- `rad patch` - Patch management
- `rad path` - Path operations
- `rad clean` - Repository cleaning
- `rad self` - Self information
- `rad seed` - Repository seeding
- `rad follow` - Peer following
- `rad unblock` - Peer unblocking
- `rad unfollow` - Peer unfollowing
- `rad unseed` - Stop seeding
- `rad remote` - Remote management
- `rad stats` - Repository statistics
- `rad sync` - Network synchronization
- `rad cob` - Collaborative objects

### Version-Specific Features

#### 1.1.0+ Features
- `rad id update --edit` - Edit identity in editor
- `rad cob migrate` - Database migration
- `rad patch checkout --remote` - Specify remote for checkout
- `rad patch set --remote` - Set remote for patches
- `rad config` subcommands - Get/set configuration values

#### 1.2.0+ Features
- `rad cob --json` - JSON output for COB commands
- `rad cob create` - Create collaborative objects
- `rad cob update` - Update collaborative objects
- `rad issue --json` - JSON output for issues
- `rad issue list --status` - Filter issues by status
- `rad patch --json` - JSON output for patches
- `rad patch edit` - Edit patch metadata
- `rad node inventory --nid` - Filter inventory by NID
- `rad seed --multiple` - Seed multiple repositories
- `rad unseed --multiple` - Unseed multiple repositories
- `rad config schema` - Output JSON schema

#### 1.3.0+ Features
- `rad cob log --from` - Start log from commit
- `rad cob log --to` - End log at commit
- **Windows support** - Native Windows CLI operation

#### 1.4.0+ Features
- Improved sync status symbols and output
- Enhanced error handling and stability

## Migration Guide

### From 1.0.x to 1.1.0
1. **Database Migration**: Run `rad cob migrate` automatically
2. **Breaking Changes**: None for MCP server usage
3. **New Features**: Access new config subcommands and patch options

### From 1.1.x to 1.2.0
1. **No Breaking Changes**: Direct upgrade
2. **New Features**: JSON output and enhanced patch management
3. **Optional**: Update workflows to use new JSON capabilities

### From 1.2.x to 1.3.0
1. **No Breaking Changes**: Direct upgrade
2. **New Features**: Canonical references and Windows support
3. **Optional**: Explore canonical references for enhanced governance

### From 1.3.x to 1.4.0
1. **No Breaking Changes**: Direct upgrade
2. **Stability Improvements**: Better sync and error handling
3. **Recommended**: Update for improved reliability

## Compatibility Matrix

| Feature | 1.1.0 | 1.2.0 | 1.3.0 | 1.4.0 | 1.5.0 |
|---------|--------|--------|--------|--------|--------|
| JSON Output | ❌ | ✅ | ✅ | ✅ | ✅ |
| Multiple RIDs | ❌ | ✅ | ✅ | ✅ | ✅ |
| Config Subcommands | ✅ | ✅ | ✅ | ✅ | ✅ |
| Patch Edit | ❌ | ✅ | ✅ | ✅ | ✅ |
| COB Create/Update | ❌ | ✅ | ✅ | ✅ | ✅ |
| Canonical References | ❌ | ❌ | ✅ | ✅ | ✅ |
| Windows Support | ❌ | ❌ | ✅ | ✅ | ✅ |
| Enhanced Sync | ❌ | ✅ | ✅ | ✅ | ✅ |

## Error Handling

### Version Not Supported
- Falls back to closest supported version
- Provides warning about version mismatch
- Disables version-specific features gracefully

### Command Not Found
- Returns clear error message
- Suggests available alternatives
- Maintains server stability

### Breaking Changes
- Automatic database migration when detected
- Clear communication about required actions
- Fallback tools always available

## Testing Compatibility

The server includes comprehensive tests for version compatibility:

```bash
# Test all version definitions
python -m pytest tests/test_yaml_definitions.py

# Test version manager functionality
python -m pytest tests/test_definitions.py

# Test with specific version
RAD_VERSION=1.4.0 python -m src.server
```

## Future Compatibility

The server is designed to be forward-compatible:

1. **Semantic Versioning**: Follows semantic versioning for compatibility
2. **Graceful Degradation**: Newer versions work with older server versions
3. **Feature Detection**: Runtime capability detection for new features
4. **Backward Compatibility**: Older versions continue to work with newer servers

This approach ensures the Radicle MCP Server remains useful across different Radicle CLI versions while providing the best possible experience for each version.