# CLI Command Contracts

**Feature**: Command Line Interface Tool
**Branch**: 002-command-line-interface
**Date**: 2025-10-13
**Phase**: 1 - Design & Contracts

## Overview

This document defines the command-line interface contracts for QueryNL CLI. All commands follow Unix conventions (lowercase, hyphens, clear verbs) and provide comprehensive help text.

---

## Global Options

Available on all commands:

| Option | Short | Type | Description | Default |
|--------|-------|------|-------------|---------|
| `--help` | `-h` | flag | Show help message and exit | N/A |
| `--version` | `-v` | flag | Show version and exit | N/A |
| `--config` | `-c` | path | Path to config file | Platform-specific |
| `--connection` | `-n` | string | Connection name to use | From config default_connection |
| `--verbose` | | flag | Enable verbose output | false |
| `--quiet` | `-q` | flag | Suppress non-essential output | false |

**Exit Codes**:
- `0`: Success
- `1`: General error
- `2`: Invalid arguments or options
- `3`: Connection error
- `4`: Query execution error
- `5`: Configuration error

---

## Command: `querynl`

**Description**: Main entry point for QueryNL CLI.

**Usage**:
```bash
querynl [GLOBAL OPTIONS] COMMAND [COMMAND OPTIONS] [ARGUMENTS]
```

**Commands**:
- `query` - Execute natural language query
- `connect` - Manage database connections
- `schema` - Schema design commands
- `migrate` - Migration management commands
- `repl` - Start interactive REPL mode
- `config` - Manage configuration
- `history` - View query history

**Examples**:
```bash
querynl --help
querynl --version
querynl query "count all users"
querynl repl
```

---

## Command: `querynl query`

**Description**: Execute a natural language database query.

**Usage**:
```bash
querynl query [OPTIONS] "<natural language query>"
querynl query [OPTIONS] --file <path>
querynl query [OPTIONS] -
```

**Arguments**:
| Argument | Required | Description |
|----------|----------|-------------|
| `query` | Yes* | Natural language query string |

*Either `query` argument, `--file` option, or stdin (`-`) required.

**Options**:
| Option | Short | Type | Description | Default |
|--------|-------|------|-------------|---------|
| `--format` | `-f` | enum | Output format: table, json, csv, markdown | table |
| `--file` | | path | Read query from file | N/A |
| `--non-interactive` | `-y` | flag | Skip confirmation prompts | false |
| `--output` | `-o` | path | Write output to file | stdout |
| `--explain` | `-e` | flag | Show SQL explanation without executing | false |
| `--timeout` | `-t` | int | Query timeout in seconds | 30 |
| `--limit` | `-l` | int | Limit result rows | No limit |

**Exit Codes**:
- `0`: Query executed successfully
- `4`: Query execution error (syntax, timeout, etc.)
- `130`: User cancelled (Ctrl+C)

**Examples**:
```bash
# Basic query
querynl query "show all active users"

# JSON output
querynl query --format json "count orders by status"

# Read from file
querynl query --file queries.txt

# Pipe from stdin
echo "list tables" | querynl query -

# Explain without executing
querynl query --explain "delete old records"

# Non-interactive mode (skip confirmations)
querynl query -y "delete from temp_table"
```

**Output Format - Table** (default):
```
┌────┬───────────┬─────────────────┐
│ ID │ Name      │ Email           │
├────┼───────────┼─────────────────┤
│  1 │ Alice     │ alice@email.com │
│  2 │ Bob       │ bob@email.com   │
└────┴───────────┴─────────────────┘

2 rows returned (123ms)
```

**Output Format - JSON**:
```json
{
  "query": "show all active users",
  "sql": "SELECT id, name, email FROM users WHERE status = 'active'",
  "rows": [
    {"id": 1, "name": "Alice", "email": "alice@email.com"},
    {"id": 2, "name": "Bob", "email": "bob@email.com"}
  ],
  "row_count": 2,
  "execution_time_ms": 123
}
```

**Output Format - CSV**:
```csv
ID,Name,Email
1,Alice,alice@email.com
2,Bob,bob@email.com
```

**Output Format - Markdown**:
```markdown
| ID | Name  | Email           |
|----|-------|-----------------|
| 1  | Alice | alice@email.com |
| 2  | Bob   | bob@email.com   |
```

**Behavior**:
1. Parse natural language query
2. Retrieve active connection from config
3. Fetch database schema
4. Generate SQL using LLM
5. Display generated SQL (transparency requirement)
6. If destructive (DELETE, DROP, TRUNCATE) → prompt for confirmation (unless `-y`)
7. Execute SQL on database
8. Format and display results
9. Record in query history

---

## Command Group: `querynl connect`

**Description**: Manage database connections.

**Subcommands**:
- `add` - Add a new connection
- `list` - List all connections
- `test` - Test a connection
- `use` - Set default connection
- `remove` - Remove a connection
- `edit` - Edit connection details

### `querynl connect add`

**Usage**:
```bash
querynl connect add [OPTIONS] <name>
```

**Arguments**:
| Argument | Required | Description |
|----------|----------|-------------|
| `name` | Yes | Unique name for the connection |

**Options**:
| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `--type` | enum | Database type: postgresql, mysql, sqlite, mongodb | Interactive prompt |
| `--host` | string | Database host | Interactive prompt |
| `--port` | int | Database port | Type-specific default |
| `--database` | string | Database name | Interactive prompt |
| `--username` | string | Database username | Interactive prompt |
| `--ssl` / `--no-ssl` | flag | Enable/disable SSL | true |
| `--ssh-tunnel` | flag | Configure SSH tunnel | false |
| `--set-default` | flag | Set as default connection | false (true if first) |

**Examples**:
```bash
# Interactive mode
querynl connect add prod-db

# With options (password still prompted securely)
querynl connect add prod-db \
  --type postgresql \
  --host prod.example.com \
  --port 5432 \
  --database production \
  --username app_user

# SQLite connection
querynl connect add dev-db --type sqlite --database ./dev.db

# With SSH tunnel
querynl connect add remote-db --type postgresql --ssh-tunnel
```

**Behavior**:
1. Prompt for connection details (type, host, port, database, username)
2. Prompt for password (hidden input)
3. Store connection config in `~/.querynl/config.yaml` (without password)
4. Store password in OS keychain (service: "querynl", account: name)
5. Test connection
6. If successful, set as default if first connection
7. Display success message with connection details

### `querynl connect list`

**Usage**:
```bash
querynl connect list [OPTIONS]
```

**Options**:
| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `--format` | enum | Output format: table, json | table |
| `--verbose` | flag | Show additional details | false |

**Examples**:
```bash
querynl connect list
querynl connect list --format json
```

**Output - Table**:
```
NAME      TYPE        HOST              DATABASE    STATUS
prod-db   postgresql  prod.example.com  production  ● Active (default)
dev-db    sqlite      ./dev.db          dev.db      ● Active
test-db   mysql       test.example.com  test        ○ Inactive
```

**Output - JSON**:
```json
{
  "connections": [
    {
      "name": "prod-db",
      "type": "postgresql",
      "host": "prod.example.com",
      "port": 5432,
      "database": "production",
      "username": "app_user",
      "ssl_enabled": true,
      "is_default": true,
      "last_used": "2025-10-13T14:22:15Z"
    }
  ]
}
```

### `querynl connect test`

**Usage**:
```bash
querynl connect test [OPTIONS] <name>
```

**Arguments**:
| Argument | Required | Description |
|----------|----------|-------------|
| `name` | Yes | Connection name to test |

**Examples**:
```bash
querynl connect test prod-db
```

**Output**:
```
Testing connection 'prod-db'...
✓ Connection successful
  Database: PostgreSQL 15.2
  Server: prod.example.com:5432
  Latency: 23ms
```

**Behavior**:
1. Retrieve connection config from `~/.querynl/config.yaml`
2. Retrieve password from keychain
3. Attempt database connection
4. Display connection details and latency
5. Exit 0 for success, 3 for failure

### `querynl connect use`

**Usage**:
```bash
querynl connect use <name>
```

**Arguments**:
| Argument | Required | Description |
|----------|----------|-------------|
| `name` | Yes | Connection name to set as default |

**Examples**:
```bash
querynl connect use prod-db
```

**Output**:
```
Default connection set to 'prod-db'
```

**Behavior**:
1. Validate connection exists
2. Update `default_connection` in config.yaml
3. Display confirmation

### `querynl connect remove`

**Usage**:
```bash
querynl connect remove [OPTIONS] <name>
```

**Arguments**:
| Argument | Required | Description |
|----------|----------|-------------|
| `name` | Yes | Connection name to remove |

**Options**:
| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `--confirm` | flag | Skip confirmation prompt | false (prompt) |

**Examples**:
```bash
querynl connect remove dev-db
querynl connect remove dev-db --confirm
```

**Output**:
```
Remove connection 'dev-db'? [y/N]: y
✓ Connection 'dev-db' removed
✓ Credentials deleted from keychain
```

**Behavior**:
1. Prompt for confirmation (unless `--confirm`)
2. Remove connection from config.yaml
3. Delete credentials from keychain
4. If was default connection, unset default (or set to first remaining)
5. Display confirmation

---

## Command Group: `querynl schema`

**Description**: Schema design commands.

**Subcommands**:
- `design` - Generate schema from natural language
- `visualize` - Generate ER diagram
- `analyze` - Analyze schema for issues
- `modify` - Modify existing schema
- `apply` - Apply schema to database

### `querynl schema design`

**Usage**:
```bash
querynl schema design [OPTIONS] "<description>"
```

**Arguments**:
| Argument | Required | Description |
|----------|----------|-------------|
| `description` | Yes | Natural language schema description |

**Options**:
| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `--output` | path | Save schema to file | Auto-generate name |
| `--format` | enum | Output format: json, yaml | json |
| `--visualize` | flag | Generate ER diagram | false |

**Examples**:
```bash
querynl schema design "blog with posts and comments"
querynl schema design "e-commerce with users products orders" --output schema.json
```

**Output**:
```
Generated schema: blog-schema-v1

Tables:
  posts (3 columns)
    - id (integer, primary key)
    - title (varchar(200), not null)
    - content (text)

  comments (4 columns)
    - id (integer, primary key)
    - post_id (integer, foreign key → posts.id)
    - content (text)
    - created_at (timestamp)

Relationships:
  comments.post_id → posts.id (CASCADE)

Schema saved to: ~/.querynl/schemas/blog-schema-v1.json
```

### `querynl schema visualize`

**Usage**:
```bash
querynl schema visualize [OPTIONS] <schema-file>
```

**Arguments**:
| Argument | Required | Description |
|----------|----------|-------------|
| `schema-file` | Yes | Path to schema JSON file |

**Options**:
| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `--output` | path | Output file for diagram | stdout |
| `--format` | enum | Diagram format: mermaid, ascii | mermaid |

**Examples**:
```bash
querynl schema visualize schema.json
querynl schema visualize schema.json --output diagram.md
```

**Output (Mermaid)**:
```mermaid
erDiagram
    posts ||--o{ comments : has
    posts {
        int id PK
        varchar title
        text content
    }
    comments {
        int id PK
        int post_id FK
        text content
        timestamp created_at
    }
```

---

## Command Group: `querynl migrate`

**Description**: Migration management commands.

**Subcommands**:
- `generate` - Generate migration from schema changes
- `preview` - Preview migration SQL
- `apply` - Apply pending migrations
- `rollback` - Rollback last migration
- `status` - Show migration status

### `querynl migrate generate`

**Usage**:
```bash
querynl migrate generate [OPTIONS]
```

**Options**:
| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `--from` | path | Source schema file | Current database schema |
| `--to` | path | Target schema file | Required |
| `--message` | string | Migration description | Auto-generated |
| `--framework` | enum | Migration framework: alembic, flyway, raw | raw |
| `--output` | path | Output directory | ./migrations/ |

**Examples**:
```bash
querynl migrate generate --to new-schema.json --message "add indexes"
querynl migrate generate --from old.json --to new.json --framework alembic
```

**Output**:
```
Generated migration: 20251013_142230_add_indexes

Up migration:
  CREATE INDEX idx_posts_created_at ON posts(created_at);
  CREATE INDEX idx_comments_post_id ON comments(post_id);

Down migration:
  DROP INDEX idx_comments_post_id;
  DROP INDEX idx_posts_created_at;

Files created:
  migrations/20251013_142230_add_indexes_up.sql
  migrations/20251013_142230_add_indexes_down.sql
```

### `querynl migrate apply`

**Usage**:
```bash
querynl migrate apply [OPTIONS]
```

**Options**:
| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `--dry-run` | flag | Show SQL without executing | false |
| `--count` | int | Number of migrations to apply | All pending |

**Examples**:
```bash
querynl migrate apply
querynl migrate apply --dry-run
querynl migrate apply --count 1
```

**Output**:
```
Applying migrations to 'prod-db'...

● 20251013_142230_add_indexes
  ✓ Executed (142ms)

1 migration applied successfully
```

---

## Command: `querynl repl`

**Description**: Start interactive REPL mode.

**Usage**:
```bash
querynl repl [OPTIONS]
```

**Options**:
| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `--connection` | string | Connection to use | From config default_connection |
| `--history-file` | path | Custom history file | ~/.querynl/history.db |

**Examples**:
```bash
querynl repl
querynl repl --connection prod-db
```

**REPL Commands**:
| Command | Description |
|---------|-------------|
| `\help` | Show REPL commands |
| `\connect <name>` | Switch connection |
| `\tables` | List all tables |
| `\schema <table>` | Show table schema |
| `\history [n]` | Show last n queries |
| `\clear` | Clear screen |
| `\exit` or `Ctrl+D` | Exit REPL |

**REPL Prompt**:
```
querynl [prod-db]> count all users
```

**Features**:
- Tab completion for commands and table names
- Command history with Up/Down arrows
- Multi-line input for complex queries
- Persistent conversation context
- Ctrl+C cancels current query (doesn't exit)
- Ctrl+D exits REPL

---

## Command Group: `querynl config`

**Description**: Manage CLI configuration.

**Subcommands**:
- `show` - Display current configuration
- `set` - Set configuration value
- `get` - Get configuration value
- `reset` - Reset to defaults

### `querynl config show`

**Usage**:
```bash
querynl config show [OPTIONS]
```

**Options**:
| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `--format` | enum | Output format: yaml, json | yaml |

**Examples**:
```bash
querynl config show
querynl config show --format json
```

**Output**:
```yaml
default_connection: prod-db
default_output_format: table
llm_provider: openai
enable_telemetry: false
repl_history_size: 1000
confirm_destructive: true
```

### `querynl config set`

**Usage**:
```bash
querynl config set <key> <value>
```

**Examples**:
```bash
querynl config set default_output_format json
querynl config set confirm_destructive false
```

---

## Command Group: `querynl history`

**Description**: View query history.

**Subcommands**:
- `show` - Display query history
- `search` - Search query history
- `clear` - Clear history

### `querynl history show`

**Usage**:
```bash
querynl history show [OPTIONS]
```

**Options**:
| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `--limit` | int | Number of entries to show | 20 |
| `--connection` | string | Filter by connection | All connections |
| `--format` | enum | Output format: table, json | table |

**Examples**:
```bash
querynl history show
querynl history show --limit 50 --connection prod-db
```

**Output**:
```
TIMESTAMP            CONNECTION  QUERY                       ROWS  TIME
2025-10-13 14:22:15  prod-db     count all users             1     123ms
2025-10-13 14:18:32  prod-db     show active orders          42    234ms
2025-10-13 13:45:10  dev-db      list tables                 8     12ms
```

---

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `QUERYNL_CONFIG` | Path to config file | `/custom/path/config.yaml` |
| `QUERYNL_CONNECTION_STRING` | Database connection string (bypasses keychain) | `postgresql://user:pass@host/db` |
| `QUERYNL_KEYRING_PASSWORD` | Master password for encrypted keyring fallback | `secure-master-password` |
| `QUERYNL_LLM_API_KEY` | LLM API key (bypasses keychain) | `sk-...` |
| `QUERYNL_NO_COLOR` | Disable color output | `1` |
| `QUERYNL_PAGER` | Custom pager for large output | `less -R` |

---

## Configuration File Format

**Location**:
- **Unix/Linux**: `~/.querynl/config.yaml`
- **macOS**: `~/Library/Application Support/querynl/config.yaml`
- **Windows**: `%APPDATA%\querynl\config.yaml`

**Schema**: See [data-model.md](../data-model.md#configuration-file-structure)

---

## Error Messages

All error messages follow the format:
```
Error: <description>
Suggestion: <actionable fix>
```

**Examples**:
```
Error: Connection 'prod-db' not found
Suggestion: Run 'querynl connect list' to see available connections

Error: Query execution failed: relation "userss" does not exist
Suggestion: Check table name spelling. Run '\tables' in REPL to see all tables

Error: Permission denied to access keychain
Suggestion: Grant keychain access or use QUERYNL_CONNECTION_STRING environment variable
```

---

## Contract Validation Checklist

- [x] All commands follow Unix conventions (lowercase, hyphens)
- [x] Comprehensive `--help` text for all commands (FR-005)
- [x] Appropriate exit codes for scriptability (FR-006)
- [x] Non-interactive mode support (FR-035)
- [x] Multiple output formats (FR-026, FR-027, FR-028)
- [x] Confirmation for destructive operations (FR-003, FR-040)
- [x] Environment variable configuration support (FR-014)
- [x] Credentials never in logs/output (FR-040)
- [x] Error messages are actionable (SC-006)

---

**CLI Contracts Complete**: 2025-10-13
**Ready for**: Configuration contracts and implementation (Phase 2)
