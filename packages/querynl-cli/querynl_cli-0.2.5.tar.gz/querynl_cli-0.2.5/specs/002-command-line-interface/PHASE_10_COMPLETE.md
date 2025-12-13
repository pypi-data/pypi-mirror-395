# Phase 10 Complete: Configuration Management (User Story 8)

**Completed**: 2025-10-17
**Tasks**: T144-T152 (9 tasks)
**Progress**: 152/178 tasks complete (85%)

## Summary

Phase 10 implements configuration management commands for QueryNL CLI, allowing users to view, modify, and reset settings without manually editing YAML files.

## Features Implemented

### 1. Config Show Command
**Command**: `querynl config show`

Displays current configuration in YAML or table format:

```bash
# YAML format with syntax highlighting
querynl config show

# Table format
querynl config show --format table
```

**Features**:
- Syntax-highlighted YAML output
- Table format with key-value pairs
- Shows configuration file path
- Handles nested configuration

### 2. Config Get Command
**Command**: `querynl config get <key>`

Retrieves specific configuration value:

```bash
# Get default connection
querynl config get default_connection

# Get nested value
querynl config get connections.mydb.host
```

**Features**:
- Supports nested keys with dot notation
- Color-coded output
- Helpful message if key not found

### 3. Config Set Command
**Command**: `querynl config set <key> <value>`

Updates configuration value with validation:

```bash
# Set default connection
querynl config set default_connection my-db

# Set output format
querynl config set default_format json

# Set prompt style
querynl config set prompt_format verbose
```

**Features**:
- **Value Validation**: Checks valid formats, log levels
- **Type Conversion**: Automatically converts booleans, numbers
- **Error Messages**: Shows valid options when validation fails
- **Nested Keys**: Supports dot notation for nested settings

**Validated Settings**:
- `default_format`: table, json, csv, tsv, markdown
- `log_level`: debug, info, warning, error
- `prompt_format`: minimal, verbose
- `default_connection`: Any connection name

**Code**:
```python
# Validate format
if key == "default_format" and value not in valid_formats:
    raise ConfigError(
        f"Invalid format '{value}'",
        f"Valid formats: {', '.join(valid_formats)}"
    )

# Type conversion
if value.lower() in ('true', 'false'):
    value = value.lower() == 'true'
elif value.isdigit():
    value = int(value)
```

### 4. Config Reset Command
**Command**: `querynl config reset`

Restores default configuration:

```bash
# Reset with confirmation prompt
querynl config reset

# Skip confirmation
querynl config reset --confirm
```

**Features**:
- **Confirmation Prompt**: Prevents accidental resets
- **Connection Preservation**: Keeps saved connections
- **Default Values**: Restores sensible defaults

**Default Configuration**:
```yaml
default_connection: null
default_format: table
prompt_format: minimal
log_level: info
connections: {}  # Preserved from current config
```

### 5. Config Path Command
**Command**: `querynl config path`

Shows configuration file location:

```bash
querynl config path
# Output: Configuration file: ~/.querynl/config.yaml
```

## Full Command Reference

### Show Configuration
```bash
querynl config show [--format yaml|table]
```

### Get Value
```bash
querynl config get <key>
```

### Set Value
```bash
querynl config set <key> <value>
```

### Reset Configuration
```bash
querynl config reset [--confirm]
```

### Show Config Path
```bash
querynl config path
```

## Configuration File Structure

**Location**: `~/.querynl/config.yaml`

```yaml
# Default connection to use
default_connection: my-postgres-db

# Default output format for query results
default_format: table  # table, json, csv, tsv, markdown

# REPL prompt style
prompt_format: minimal  # minimal, verbose

# Logging level
log_level: info  # debug, info, warning, error

# Saved database connections
connections:
  my-postgres-db:
    db_type: postgresql
    host: localhost
    port: 5432
    database: myapp
    username: postgres
    ssl_enabled: false

  production:
    db_type: postgresql
    host: prod.example.com
    port: 5432
    database: prod_db
    username: app_user
    ssl_enabled: true
```

## Usage Examples

### Configure Default Output Format
```bash
# Set JSON as default
querynl config set default_format json

# Verify setting
querynl config get default_format
# Output: default_format: json

# Now queries default to JSON
querynl query "count users"
# Returns JSON output
```

### Set Default Connection
```bash
# Configure default connection
querynl config set default_connection my-postgres-db

# No need to specify --connection flag
querynl query "show tables"
```

### View All Settings
```bash
# Pretty YAML view
querynl config show

# Table view
querynl config show --format table
```

### Reset to Defaults
```bash
# With confirmation
querynl config reset

# Skip confirmation (automation)
querynl config reset --confirm
```

## Error Handling

### Invalid Format
```bash
$ querynl config set default_format xml
Error: Invalid format 'xml'
Suggestion: Valid formats: table, json, csv, tsv, markdown
```

### Invalid Log Level
```bash
$ querynl config set log_level trace
Error: Invalid log level 'trace'
Suggestion: Valid levels: debug, info, warning, error
```

### Key Not Found
```bash
$ querynl config get nonexistent_key
Configuration key 'nonexistent_key' not found
```

## Implementation Details

### File Structure
- **File**: `src/cli/commands/config.py` (240 lines)
- **Command Group**: `@click.group()`
- **5 Commands**: show, get, set, reset, path

### Key Functions

**config_show()**: Display configuration
- YAML syntax highlighting with Rich
- Table format with flattened keys
- File existence check

**config_get()**: Retrieve value
- Dot notation parsing
- Nested dictionary traversal
- User-friendly error messages

**config_set()**: Update value
- Value validation (formats, log levels)
- Type conversion (bool, int, float)
- Nested key creation
- YAML serialization

**config_reset()**: Restore defaults
- Confirmation prompt
- Connection preservation
- Default value restoration

### Integration
- **File**: `src/cli/main.py` (line 51)
- Imported and registered with CLI:
```python
from .commands.config import config
cli.add_command(config)
```

## Testing Recommendations

1. **Show Configuration**:
   ```bash
   querynl config show
   querynl config show --format table
   ```

2. **Get/Set Operations**:
   ```bash
   querynl config set default_format json
   querynl config get default_format
   # Should output: default_format: json
   ```

3. **Validation**:
   ```bash
   # Should fail with helpful error
   querynl config set default_format xml
   querynl config set log_level invalid
   ```

4. **Reset**:
   ```bash
   # Add some settings
   querynl config set default_format csv
   querynl config set log_level debug

   # Reset
   querynl config reset --confirm

   # Verify defaults restored
   querynl config show
   ```

5. **Nested Keys**:
   ```bash
   querynl config set custom.nested.key value
   querynl config get custom.nested.key
   ```

## Files Created/Modified

### Created
1. `src/cli/commands/config.py` - Complete configuration management

### Modified
1. `src/cli/main.py` - Added config command group import and registration

## Security Considerations

- **No Password Exposure**: Config commands do not display passwords
- **Validation**: Prevents invalid values from breaking CLI
- **Confirmation**: Reset requires confirmation to prevent accidents
- **Preservation**: Reset preserves connections (including credentials in keyring)

## Next Phase

**Phase 11: Polish & Cross-Cutting Concerns**
- Tasks: T153-T178 (26 tasks)
- Focus: Security audit, UX validation, constitution compliance
- Goal: Production readiness and final quality checks
