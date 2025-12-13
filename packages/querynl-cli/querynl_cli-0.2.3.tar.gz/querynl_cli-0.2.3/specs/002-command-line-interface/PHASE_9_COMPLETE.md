# Phase 9 Complete: Scripting & Automation (User Story 5)

**Completed**: 2025-10-17
**Tasks**: T132-T143 (12 tasks)
**Progress**: 143/178 tasks complete (80%)

## Summary

Phase 9 implements automation-friendly features for QueryNL CLI, enabling reliable use in CI/CD pipelines and shell scripts with proper exit codes, stderr/stdout separation, and non-TTY compatibility.

## Features Implemented

### 1. Exit Code System
- **File**: `src/cli/errors.py` (lines 11-17)
- **Exit Codes**:
  - `0`: Success
  - `1`: General error
  - `2`: Invalid arguments
  - `3`: Connection error
  - `4`: Query/schema/migration error
  - `5`: Configuration error

**Code**:
```python
EXIT_SUCCESS = 0           # Command completed successfully
EXIT_GENERAL_ERROR = 1     # General/unspecified error
EXIT_INVALID_ARGS = 2      # Invalid command-line arguments
EXIT_CONNECTION_ERROR = 3  # Database connection failed
EXIT_QUERY_ERROR = 4       # Query execution failed
EXIT_CONFIG_ERROR = 5      # Configuration error
```

### 2. Exit Code Mapping
- **File**: `src/cli/errors.py` (lines 108-132)
- **Function**: `get_exit_code(exception)`
- Maps Python exceptions to appropriate exit codes
- Handles custom QueryNL exceptions and standard library exceptions

**Code**:
```python
def get_exit_code(exception: Exception) -> int:
    if isinstance(exception, ConfigError):
        return EXIT_CONFIG_ERROR
    elif isinstance(exception, ConnectionError):
        return EXIT_CONNECTION_ERROR
    elif isinstance(exception, (QueryError, SchemaError, MigrationError)):
        return EXIT_QUERY_ERROR
    elif isinstance(exception, (ValueError, TypeError)):
        return EXIT_INVALID_ARGS
    # ...
```

### 3. Main Entry Point with Error Handling
- **File**: `src/cli/main.py` (lines 88-119)
- **Function**: `main()`
- Catches all exceptions and exits with appropriate codes
- Ensures errors go to stderr, not stdout

**Code**:
```python
def main():
    try:
        cli()
        sys.exit(0)
    except click.ClickException as e:
        e.show()
        sys.exit(e.exit_code if hasattr(e, 'exit_code') else 1)
    except click.Abort:
        sys.exit(1)
    except Exception as e:
        exit_code = get_exit_code(e)
        error_msg = format_error_message(e)
        error_console.print(f"[red]Error:[/red] {error_msg}")
        sys.exit(exit_code)
```

### 4. Stderr/Stdout Separation
- **File**: `src/cli/main.py` (lines 16-18)
- **Consoles**:
  - `console`: Normal output → stdout
  - `error_console`: Error output → stderr
- All error messages use `error_console.print()`

**Code**:
```python
console = Console(force_terminal=sys.stdout.isatty())
error_console = Console(stderr=True, force_terminal=sys.stderr.isatty())
```

### 5. TTY Detection
- **Files**:
  - `src/cli/main.py` (lines 17-18)
  - `src/cli/formatting/table.py` (line 14)
- Automatically disables colors and formatting when output is piped
- Uses `sys.stdout.isatty()` to detect terminal presence

**Code**:
```python
# Disable colors when piping
console = Console(force_terminal=sys.stdout.isatty() if hasattr(sys.stdout, 'isatty') else False)
```

### 6. Verbosity Flags
- **File**: `src/cli/main.py` (lines 19-20, 36-37)
- **Flags**:
  - `--verbose`: Enable debug logging
  - `--quiet`: Suppress non-essential output
- Available on all commands via Click context

## Automation Examples

### Shell Script with Exit Code Handling
```bash
#!/bin/bash

# Execute query and handle different error types
if querynl query "count all users" --format json --connection prod; then
    echo "Query succeeded"
else
    EXIT_CODE=$?
    case $EXIT_CODE in
        2) echo "Invalid arguments" ;;
        3) echo "Connection failed" ;;
        4) echo "Query execution failed" ;;
        5) echo "Configuration error" ;;
        *) echo "General error" ;;
    esac
    exit $EXIT_CODE
fi
```

### CI/CD Pipeline (GitHub Actions)
```yaml
- name: Test database connection
  run: |
    querynl connect test prod-db
  continue-on-error: false

- name: Execute migration
  run: |
    querynl migrate apply --connection prod-db --confirm --quiet
```

### JSON Output Parsing
```bash
# Parse JSON with jq
querynl query "show all users" --format json --connection mydb | jq '.rows | length'

# Parse with Python
python << EOF
import json
import subprocess
result = subprocess.run(['querynl', 'query', 'count users', '--format', 'json'],
                       capture_output=True, text=True)
data = json.loads(result.stdout)
print(f"Row count: {data['row_count']}")
EOF
```

### Non-TTY Environment (Docker)
```dockerfile
FROM python:3.11-slim
RUN pip install querynl-cli
CMD ["querynl", "query", "SELECT 1", "--format", "json"]
```

The CLI automatically detects non-TTY environment and disables formatting:
- No colors in output
- No interactive prompts
- Clean text output for parsing

## Testing Recommendations

1. **Exit Codes**:
   ```bash
   # Test success
   querynl --version
   echo $?  # Should be 0

   # Test invalid arguments
   querynl query --invalid-flag 2>/dev/null
   echo $?  # Should be 2

   # Test connection error
   querynl connect test nonexistent 2>/dev/null
   echo $?  # Should be 3
   ```

2. **Stderr/Stdout Separation**:
   ```bash
   # Errors should go to stderr
   querynl query "invalid sql" 2>errors.log 1>output.log
   # errors.log should contain error message
   # output.log should be empty
   ```

3. **TTY Detection**:
   ```bash
   # With TTY (colors enabled)
   querynl query "select 1"

   # Piped (colors disabled)
   querynl query "select 1" | cat
   ```

4. **JSON Parsing**:
   ```bash
   # Validate JSON schema
   querynl query "select 1" --format json | jq .
   ```

## Files Created/Modified

### Modified
1. `src/cli/errors.py` - Added exit code constants and mapping function
2. `src/cli/main.py` - Added main() wrapper with exit code handling, TTY detection
3. `src/cli/formatting/table.py` - Added TTY detection for formatting
4. `setup.py` - Changed entry point from `cli` to `main`

## Exit Code Documentation

The QueryNL CLI follows Unix conventions for exit codes:

| Code | Meaning | Example |
|------|---------|---------|
| 0 | Success | Command completed successfully |
| 1 | General error | Unexpected exception or user abort |
| 2 | Invalid arguments | Wrong command syntax or missing required options |
| 3 | Connection error | Database connection failed |
| 4 | Query/execution error | SQL error, schema validation error, migration failed |
| 5 | Configuration error | Invalid config file or missing settings |

## Environment Variables

QueryNL CLI respects the following environment variables for CI/CD:

- `QUERYNL_CONNECTION_STRING`: Override connection configuration
- `QUERYNL_LLM_API_KEY`: Set LLM API key for natural language queries
- `NO_COLOR`: Disable colors (standard Unix convention)
- `TERM`: Terminal type detection

## Next Phase

**Phase 10: User Story 8 - Configuration Management**
- Tasks: T144-T152 (9 tasks)
- Focus: Config commands (show, get, set, reset)
- Goal: Manage CLI settings without manual YAML editing
