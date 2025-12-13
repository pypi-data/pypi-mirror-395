# Data Model: QueryNL CLI

**Feature**: Command Line Interface Tool
**Branch**: 002-command-line-interface
**Date**: 2025-10-13
**Phase**: 1 - Design & Contracts

## Overview

This document defines the data entities for the QueryNL CLI tool. These entities represent configuration, runtime state, and persistent data structures used by the CLI.

---

## Entity Definitions

### 1. ConnectionProfile

**Description**: Represents a configured database connection with credentials stored in system keychain.

**Fields**:
| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `name` | string | Yes | Unique identifier for the connection | Alphanumeric + hyphens, 1-50 chars |
| `database_type` | enum | Yes | Type of database | One of: postgresql, mysql, sqlite, mongodb |
| `host` | string | Conditional | Database host/IP address | Valid hostname or IP (not required for sqlite) |
| `port` | integer | Conditional | Database port | Valid port number 1-65535 (not required for sqlite) |
| `database_name` | string | Yes | Database/schema name | Non-empty string |
| `username` | string | Conditional | Database username | Non-empty (not required for sqlite) |
| `ssl_enabled` | boolean | No | Whether to use SSL/TLS | Default: true |
| `ssh_tunnel` | SSHTunnel | No | SSH tunnel configuration | Optional nested object |
| `created_at` | datetime | Yes | When connection was added | ISO 8601 format |
| `last_used` | datetime | No | Last time connection was used | ISO 8601 format |

**Relationships**:
- Credentials stored separately in keychain (service: "querynl", account: connection name)
- Referenced by QueryHistory entries

**Storage**: `~/.querynl/config.yaml` (without credentials)

**Example**:
```yaml
connections:
  prod-db:
    database_type: postgresql
    host: prod.example.com
    port: 5432
    database_name: production
    username: app_user
    ssl_enabled: true
    ssh_tunnel: null
    created_at: '2025-10-13T10:30:00Z'
    last_used: '2025-10-13T14:22:15Z'

  local-dev:
    database_type: sqlite
    database_name: ./dev.db
    created_at: '2025-10-12T09:00:00Z'
```

**State Transitions**:
1. Created → Active (after successful connection test)
2. Active → Failed (connection test fails)
3. Failed → Active (connection restored)
4. Any → Deleted (user removes connection)

---

### 2. SSHTunnel

**Description**: SSH tunnel configuration for remote database access.

**Fields**:
| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `ssh_host` | string | Yes | SSH server hostname | Valid hostname or IP |
| `ssh_port` | integer | No | SSH server port | Default: 22 |
| `ssh_username` | string | Yes | SSH username | Non-empty string |
| `ssh_key_path` | string | Conditional | Path to SSH private key | Valid file path (if not using password) |
| `local_bind_port` | integer | No | Local port for tunnel | Valid port 1-65535, default: auto-assign |
| `remote_bind_host` | string | No | Remote database host from SSH server perspective | Default: localhost |
| `remote_bind_port` | integer | Yes | Remote database port | Valid port 1-65535 |

**Relationships**:
- Part of ConnectionProfile
- SSH password (if used) stored in keychain

**Example**:
```yaml
ssh_tunnel:
  ssh_host: bastion.example.com
  ssh_port: 22
  ssh_username: deploy
  ssh_key_path: ~/.ssh/id_rsa
  local_bind_port: 15432
  remote_bind_host: db-internal.example.com
  remote_bind_port: 5432
```

---

### 3. CLIConfiguration

**Description**: User preferences and default settings for the CLI.

**Fields**:
| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `default_connection` | string | No | Default connection name | Must reference existing connection |
| `default_output_format` | enum | No | Default output format | One of: table, json, csv, markdown (default: table) |
| `llm_provider` | enum | No | LLM provider for query generation | One of: openai, anthropic, local (default: from backend) |
| `llm_api_key` | string | No | API key for BYOK users | Stored in keychain if provided |
| `enable_telemetry` | boolean | No | Opt-in telemetry | Default: false |
| `repl_history_size` | integer | No | Number of REPL history entries | Default: 1000, range: 100-10000 |
| `pager` | string | No | Pager for large output | Default: less (Unix) / more (Windows) |
| `confirm_destructive` | boolean | No | Require confirmation for DELETE/DROP | Default: true |
| `color_output` | enum | No | Color output mode | One of: auto, always, never (default: auto) |

**Storage**: `~/.querynl/config.yaml`

**Example**:
```yaml
default_connection: prod-db
default_output_format: table
llm_provider: openai
enable_telemetry: false
repl_history_size: 1000
pager: less
confirm_destructive: true
color_output: auto
```

---

### 4. QueryHistory

**Description**: Record of executed queries in REPL/CLI sessions for history recall and analytics.

**Fields**:
| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `id` | integer | Yes | Auto-increment primary key | Unique, auto-generated |
| `session_id` | string | Yes | REPL session identifier | UUID v4 |
| `connection_name` | string | Yes | Connection used for query | References ConnectionProfile |
| `natural_language_input` | string | Yes | User's natural language query | Non-empty |
| `generated_sql` | string | Yes | LLM-generated SQL | Non-empty |
| `executed` | boolean | Yes | Whether query was executed or cancelled | Default: false |
| `execution_time_ms` | integer | No | Query execution time | Milliseconds, null if not executed |
| `row_count` | integer | No | Number of rows returned/affected | Null if not executed |
| `error_message` | string | No | Error message if query failed | Null if successful |
| `timestamp` | datetime | Yes | When query was executed | ISO 8601 format |

**Relationships**:
- References ConnectionProfile by name
- Grouped by session_id

**Storage**: `~/.querynl/history.db` (SQLite)

**Indexes**:
- Primary key on `id`
- Index on `session_id` for session-based queries
- Index on `timestamp` for time-based queries
- Index on `connection_name` for connection-based history

**Schema (SQLite)**:
```sql
CREATE TABLE query_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    connection_name TEXT NOT NULL,
    natural_language_input TEXT NOT NULL,
    generated_sql TEXT NOT NULL,
    executed BOOLEAN NOT NULL DEFAULT 0,
    execution_time_ms INTEGER,
    row_count INTEGER,
    error_message TEXT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_session_id ON query_history(session_id);
CREATE INDEX idx_timestamp ON query_history(timestamp);
CREATE INDEX idx_connection_name ON query_history(connection_name);
```

---

### 5. REPLSession

**Description**: Runtime state for an active REPL session.

**Fields**:
| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `session_id` | string | Yes | Unique session identifier | UUID v4 |
| `connection_name` | string | No | Active connection for session | References ConnectionProfile |
| `start_time` | datetime | Yes | Session start timestamp | ISO 8601 format |
| `conversation_context` | list[dict] | Yes | LLM conversation history | List of {role, content} messages |
| `last_result_rows` | list[dict] | No | Most recent query results | Cached for reference in REPL |
| `variables` | dict | No | User-defined variables | Key-value pairs |

**Relationships**:
- References ConnectionProfile
- Associated with QueryHistory entries via session_id

**Storage**: In-memory during REPL session, session_id persisted to history.db

**Lifecycle**:
1. Created when `querynl repl` starts
2. Active during REPL session
3. Destroyed when REPL exits (Ctrl+D or `exit`)
4. session_id preserved in query_history for analytics

---

### 6. SchemaDesign

**Description**: Saved schema design generated from natural language description.

**Fields**:
| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `id` | string | Yes | Unique identifier for schema | UUID v4 or user-provided name |
| `description` | string | Yes | Original natural language description | Non-empty |
| `tables` | list[TableDesign] | Yes | Table definitions | At least one table |
| `relationships` | list[Relationship] | Yes | Foreign key relationships | Can be empty |
| `created_at` | datetime | Yes | Creation timestamp | ISO 8601 format |
| `modified_at` | datetime | Yes | Last modification timestamp | ISO 8601 format |
| `version` | integer | Yes | Schema version number | Increment on modification |

**Storage**: JSON files in `~/.querynl/schemas/` or project directory

**Example**:
```json
{
  "id": "blog-schema-v1",
  "description": "blog with posts and comments",
  "tables": [
    {
      "name": "posts",
      "columns": [
        {"name": "id", "type": "integer", "primary_key": true},
        {"name": "title", "type": "varchar(200)", "nullable": false},
        {"name": "content", "type": "text", "nullable": false},
        {"name": "created_at", "type": "timestamp", "nullable": false}
      ]
    },
    {
      "name": "comments",
      "columns": [
        {"name": "id", "type": "integer", "primary_key": true},
        {"name": "post_id", "type": "integer", "nullable": false},
        {"name": "content", "type": "text", "nullable": false},
        {"name": "created_at", "type": "timestamp", "nullable": false}
      ]
    }
  ],
  "relationships": [
    {
      "from_table": "comments",
      "from_column": "post_id",
      "to_table": "posts",
      "to_column": "id",
      "on_delete": "CASCADE"
    }
  ],
  "created_at": "2025-10-13T10:00:00Z",
  "modified_at": "2025-10-13T10:00:00Z",
  "version": 1
}
```

---

### 7. TableDesign

**Description**: Table definition within a schema design.

**Fields**:
| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `name` | string | Yes | Table name | Valid SQL identifier |
| `columns` | list[ColumnDefinition] | Yes | Column definitions | At least one column |
| `indexes` | list[IndexDefinition] | No | Index definitions | Can be empty |
| `constraints` | list[Constraint] | No | Additional constraints | Can be empty |

---

### 8. ColumnDefinition

**Description**: Column definition within a table.

**Fields**:
| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `name` | string | Yes | Column name | Valid SQL identifier |
| `type` | string | Yes | Data type | Database-specific type |
| `nullable` | boolean | No | Whether column allows NULL | Default: true |
| `primary_key` | boolean | No | Whether column is primary key | Default: false |
| `unique` | boolean | No | Whether column has unique constraint | Default: false |
| `default_value` | string | No | Default value expression | Valid SQL expression |

---

### 9. Relationship

**Description**: Foreign key relationship between tables.

**Fields**:
| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `from_table` | string | Yes | Source table name | Must exist in schema |
| `from_column` | string | Yes | Source column name | Must exist in from_table |
| `to_table` | string | Yes | Target table name | Must exist in schema |
| `to_column` | string | Yes | Target column name | Must exist in to_table |
| `on_delete` | enum | No | ON DELETE action | One of: CASCADE, SET NULL, RESTRICT (default: RESTRICT) |
| `on_update` | enum | No | ON UPDATE action | One of: CASCADE, SET NULL, RESTRICT (default: RESTRICT) |

---

### 10. MigrationRecord

**Description**: Tracking record for database migrations.

**Fields**:
| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `migration_id` | string | Yes | Unique migration identifier | Timestamp-based or sequential |
| `connection_name` | string | Yes | Connection where migration applied | References ConnectionProfile |
| `framework` | enum | Yes | Migration framework format | One of: alembic, flyway, raw |
| `direction` | enum | Yes | Migration direction | One of: up, down |
| `sql_content` | string | Yes | Migration SQL content | Non-empty |
| `applied_at` | datetime | No | When migration was applied | ISO 8601 format, null if pending |
| `status` | enum | Yes | Migration status | One of: pending, applied, failed |
| `error_message` | string | No | Error message if failed | Null if successful |
| `rollback_sql` | string | No | Rollback SQL for down migration | Required for safe rollback |

**Storage**: Project-specific migrations table in target database or `.querynl/migrations.db`

**State Transitions**:
1. pending → applied (successful application)
2. pending → failed (application error)
3. applied → pending (rollback via down migration)

---

## Data Flow Diagrams

### Connection Setup Flow
```
User → querynl connect add <name>
  ↓
CLI prompts for connection details
  ↓
CLI prompts for password (hidden input)
  ↓
ConnectionProfile created in config.yaml
  ↓
Password stored in OS keychain (service: querynl, account: <name>)
  ↓
CLI runs connection test
  ↓
Success → Set as default_connection (if first connection)
```

### Query Execution Flow
```
User → querynl query "natural language"
  ↓
Load active ConnectionProfile from config
  ↓
Retrieve credentials from keychain
  ↓
Connect to database
  ↓
Send natural language + schema to LLM
  ↓
Receive generated SQL
  ↓
Display SQL to user (transparency)
  ↓
[If destructive] Prompt for confirmation
  ↓
Execute SQL on database
  ↓
Format results (Rich table/JSON/CSV)
  ↓
Store QueryHistory entry in history.db
  ↓
Display results to user
```

### REPL Session Flow
```
User → querynl repl
  ↓
Create REPLSession with new session_id
  ↓
Load ConnectionProfile + credentials
  ↓
Initialize click-repl with context
  ↓
  [Loop]
    User enters query
      ↓
    Append to conversation_context
      ↓
    Generate SQL (with conversation context)
      ↓
    Display SQL + execute (with confirmation for destructive)
      ↓
    Store QueryHistory entry
      ↓
    Cache results in last_result_rows
  [End Loop on Ctrl+D or 'exit']
  ↓
Persist session_id in history.db
  ↓
Cleanup REPLSession from memory
```

---

## Validation Rules

### Connection Validation
- [ ] Connection name must be unique within config
- [ ] SQLite connections must have valid file path
- [ ] Network connections (PostgreSQL, MySQL, MongoDB) must have host and port
- [ ] Port must be in range 1-65535
- [ ] Username required for network connections
- [ ] SSL enabled by default for network connections

### Credential Security
- [ ] Passwords never stored in config.yaml
- [ ] Keyring fallback to encrypted file if OS keychain unavailable
- [ ] Connection strings in env vars override keychain (for CI/CD)
- [ ] Never log or display credentials in error messages

### Query History
- [ ] Maximum 10,000 entries per connection (auto-prune oldest)
- [ ] Natural language input max length: 10,000 characters
- [ ] Generated SQL max length: 100,000 characters
- [ ] Session ID must be valid UUID v4

### Schema Design
- [ ] Table names must be valid SQL identifiers
- [ ] At least one column with primary key
- [ ] Foreign key relationships must reference existing tables/columns
- [ ] Column types must be valid for target database

---

## Configuration File Structure

**Location**:
- **Unix/Linux**: `~/.querynl/config.yaml`
- **macOS**: `~/Library/Application Support/querynl/config.yaml`
- **Windows**: `%APPDATA%\querynl\config.yaml`

**Schema**:
```yaml
# QueryNL CLI Configuration
version: "1.0"

# Default settings
defaults:
  connection: prod-db
  output_format: table
  llm_provider: openai

# Preferences
preferences:
  enable_telemetry: false
  repl_history_size: 1000
  pager: less
  confirm_destructive: true
  color_output: auto

# Database connections (credentials in keychain)
connections:
  prod-db:
    database_type: postgresql
    host: prod.example.com
    port: 5432
    database_name: production
    username: app_user
    ssl_enabled: true
    created_at: '2025-10-13T10:30:00Z'
    last_used: '2025-10-13T14:22:15Z'

  dev-db:
    database_type: sqlite
    database_name: ./dev.db
    created_at: '2025-10-12T09:00:00Z'
```

---

## Platform-Specific Considerations

### Keychain Storage

**macOS** (via Keychain Access):
```python
import keyring
keyring.set_password("querynl", "prod-db", "secret-password")
password = keyring.get_password("querynl", "prod-db")
```

**Windows** (via Credential Manager):
```python
# Same API, different backend
import keyring
keyring.set_password("querynl", "prod-db", "secret-password")
password = keyring.get_password("querynl", "prod-db")
```

**Linux** (via Secret Service - GNOME Keyring/KWallet):
```python
# Requires D-Bus session
import keyring
keyring.set_password("querynl", "prod-db", "secret-password")
password = keyring.get_password("querynl", "prod-db")
```

**Linux Headless** (via keyrings.cryptfile):
```python
import keyring
from keyrings.cryptfile.cryptfile import CryptFileKeyring

kr = CryptFileKeyring()
kr.keyring_key = os.getenv('QUERYNL_KEYRING_PASSWORD')
keyring.set_keyring(kr)

# Same API, encrypted file backend
keyring.set_password("querynl", "prod-db", "secret-password")
```

---

## Summary

This data model supports the CLI's core requirements:
- **Connection Management**: ConnectionProfile with secure credential storage
- **Query Execution**: QueryHistory tracking with conversation context
- **REPL Mode**: REPLSession with persistent history
- **Schema Design**: SchemaDesign with versioning and relationships
- **Migration Tracking**: MigrationRecord for safe schema evolution

All entities designed with:
- Constitution compliance (Security-First Design, Transparency)
- Multi-database parity (database_type enum)
- Fail-safe defaults (confirm_destructive: true, ssl_enabled: true)
- Cross-platform compatibility (platform-specific config paths, keyring abstraction)

---

**Data Model Complete**: 2025-10-13
**Ready for**: API Contracts generation (Phase 1 continued)
