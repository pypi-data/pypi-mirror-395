# QueryNL CLI - Quickstart Guide

**Version**: 1.0.0
**Last Updated**: 2025-10-13
**Target Audience**: Developers, DBAs, DevOps Engineers

## What is QueryNL CLI?

QueryNL CLI is a command-line tool that lets you query databases using natural language instead of SQL. It's perfect for terminal-focused workflows, automation, and quick database exploration.

**Key Features**:
- 🗣️ Natural language queries → SQL
- 🔐 Secure credential storage in OS keychain
- 🎨 Multiple output formats (table, JSON, CSV, markdown)
- 🔄 Interactive REPL mode
- 🏗️ Schema design from descriptions
- 🚀 Migration generation
- 🤖 CI/CD friendly with scriptable commands

---

## Installation

### Option 1: Binary Download (Recommended)

Download the latest release for your platform:

```bash
# macOS (Intel)
curl -L https://github.com/querynl/querynl-cli/releases/download/v1.0.0/querynl-macos-x86_64 -o /usr/local/bin/querynl
chmod +x /usr/local/bin/querynl

# macOS (Apple Silicon)
curl -L https://github.com/querynl/querynl-cli/releases/download/v1.0.0/querynl-macos-arm64 -o /usr/local/bin/querynl
chmod +x /usr/local/bin/querynl

# Linux
curl -L https://github.com/querynl/querynl-cli/releases/download/v1.0.0/querynl-linux-x86_64 -o /usr/local/bin/querynl
chmod +x /usr/local/bin/querynl

# Windows (PowerShell)
Invoke-WebRequest -Uri https://github.com/querynl/querynl-cli/releases/download/v1.0.0/querynl-windows.exe -OutFile querynl.exe
# Add to PATH manually
```

### Option 2: Install via pip

Requires Python 3.11+:

```bash
pip install querynl-cli
```

### Option 3: Homebrew (macOS/Linux)

```bash
brew install querynl
```

### Verify Installation

```bash
querynl --version
# QueryNL CLI v1.0.0
```

---

## 5-Minute Tutorial

### Step 1: Add Your First Connection

```bash
querynl connect add my-db
```

You'll be prompted for connection details:

```
Database type (postgresql, mysql, sqlite, mongodb): postgresql
Host: localhost
Port [5432]:
Database name: myapp
Username: admin
Password: ●●●●●●●●

✓ Connection 'my-db' added successfully
✓ Credentials stored securely in keychain
✓ Set as default connection
```

### Step 2: Run Your First Query

```bash
querynl query "count all users"
```

Output:

```
Generated SQL:
  SELECT COUNT(*) FROM users;

Execute this query? [Y/n]: y

┌───────┐
│ count │
├───────┤
│  1,523│
└───────┘

1 row returned (45ms)
```

### Step 3: Try Different Output Formats

```bash
# JSON format (great for piping to jq)
querynl query --format json "show active users"

# CSV format (import to spreadsheets)
querynl query --format csv "list orders from last week"

# Markdown format (for documentation)
querynl query --format markdown "show database statistics"
```

### Step 4: Enter Interactive Mode

```bash
querynl repl
```

```
QueryNL REPL v1.0.0 - Connected to 'my-db' (postgresql)
Type '\help' for commands, '\exit' or Ctrl+D to quit

querynl [my-db]> show all tables

Generated SQL:
  SELECT tablename FROM pg_tables WHERE schemaname = 'public';

┌──────────────┐
│  tablename   │
├──────────────┤
│ users        │
│ orders       │
│ products     │
└──────────────┘

querynl [my-db]> count orders by status

Generated SQL:
  SELECT status, COUNT(*) FROM orders GROUP BY status;

┌──────────┬───────┐
│  status  │ count │
├──────────┼───────┤
│ pending  │    42 │
│ shipped  │   156 │
│ delivered│   892 │
└──────────┴───────┘

querynl [my-db]> \exit
```

**Congratulations!** You've completed the quickstart tutorial.

---

## Common Use Cases

### Use Case 1: Quick Data Exploration

```bash
# List all tables
querynl query "show all tables"

# See table schema
querynl query "describe users table"

# Count records
querynl query "count orders from last month"

# Find specific data
querynl query "show users who registered today"
```

### Use Case 2: Data Export

```bash
# Export to JSON for processing
querynl query --format json "all active users" > users.json

# Export to CSV for Excel
querynl query --format csv "sales report by region" > sales.csv

# Pipe to other tools
querynl query --format json "list orders" | jq '.rows[] | select(.status == "pending")'
```

### Use Case 3: CI/CD Integration

```bash
# Check database health (exit code 0 if query succeeds)
querynl query --non-interactive "SELECT 1" || exit 1

# Validate schema
querynl schema validate schema.json || exit 1

# Apply migrations
querynl migrate apply --dry-run
querynl migrate apply
```

### Use Case 4: Schema Design

```bash
# Design a new schema
querynl schema design "blog with posts, comments, and users"

# Visualize schema
querynl schema visualize blog-schema.json --output diagram.md

# Analyze for issues
querynl schema analyze blog-schema.json
```

### Use Case 5: Managing Multiple Databases

```bash
# Add multiple connections
querynl connect add prod-db
querynl connect add staging-db
querynl connect add dev-db

# List connections
querynl connect list

# Switch default
querynl connect use prod-db

# Query specific connection
querynl query --connection staging-db "count users"
```

---

## Connection Management

### Supported Databases

- ✅ PostgreSQL 10+
- ✅ MySQL 5.7+
- ✅ SQLite 3
- ✅ MongoDB 4.0+

### Adding Connections

#### Interactive Mode (Recommended)

```bash
querynl connect add my-connection
# Follow prompts
```

#### With CLI Options

```bash
querynl connect add prod-db \
  --type postgresql \
  --host prod.example.com \
  --port 5432 \
  --database production \
  --username app_user
# Password will be prompted securely
```

#### SQLite

```bash
querynl connect add local-db --type sqlite --database ./myapp.db
```

#### SSH Tunnel

For databases behind SSH bastion:

```bash
querynl connect add remote-db --type postgresql --ssh-tunnel
# You'll be prompted for SSH and database details
```

#### Environment Variables (CI/CD)

```bash
# Skip keychain, use connection string
export QUERYNL_CONNECTION_STRING="postgresql://user:pass@host:5432/db"
querynl query "count users"
```

### Managing Connections

```bash
# List all connections
querynl connect list

# Test connection
querynl connect test prod-db

# Set default connection
querynl connect use prod-db

# Edit connection details
querynl connect edit prod-db

# Remove connection
querynl connect remove dev-db
```

---

## Query Execution

### Basic Queries

```bash
querynl query "your natural language query here"
```

### Query Options

```bash
# JSON output
querynl query --format json "count users"

# Save to file
querynl query --output results.csv --format csv "all orders"

# Non-interactive (skip confirmations)
querynl query --non-interactive "delete from temp_table"

# Explain without executing
querynl query --explain "delete old records"

# Set timeout
querynl query --timeout 60 "complex aggregation query"

# Limit results
querynl query --limit 100 "list all users"
```

### Reading from Files

```bash
# Single query from file
querynl query --file queries.txt

# Multiple queries (one per line)
cat queries.txt | while read query; do
  querynl query "$query"
done
```

### Piping Input

```bash
# From stdin
echo "count all users" | querynl query -

# From heredoc
querynl query - <<EOF
show users who registered in the last 7 days
EOF
```

---

## REPL Mode

### Starting REPL

```bash
querynl repl
```

### REPL Commands

| Command | Description |
|---------|-------------|
| `\help` | Show available commands |
| `\connect <name>` | Switch to different connection |
| `\tables` | List all tables in current database |
| `\schema <table>` | Show table schema |
| `\history [n]` | Show last n queries (default: 10) |
| `\format <type>` | Change output format (table, json, csv) |
| `\clear` | Clear screen |
| `\exit` | Exit REPL (or Ctrl+D) |

### REPL Features

**Tab Completion**:
- Table names
- Column names
- REPL commands

**Command History**:
- Use Up/Down arrows to recall previous queries
- History persists across sessions
- Stored in `~/.querynl/history.db`

**Multi-line Queries**:
```
querynl [my-db]> show users where
             ... registration date is after 2025
             ... and status is active
```

**Context Awareness**:
REPL maintains conversation context, so follow-up queries understand previous results:

```
querynl> count all users
# Result: 1523

querynl> show the most recent 5
# Understands "users" from previous context
```

---

## Output Formats

### Table (Default)

Human-readable ASCII tables:

```
┌────┬───────────┬─────────────────┐
│ ID │ Name      │ Email           │
├────┼───────────┼─────────────────┤
│  1 │ Alice     │ alice@email.com │
│  2 │ Bob       │ bob@email.com   │
└────┴───────────┴─────────────────┘
```

### JSON

Machine-readable, perfect for automation:

```json
{
  "query": "show all users",
  "sql": "SELECT * FROM users LIMIT 10",
  "rows": [
    {"id": 1, "name": "Alice", "email": "alice@email.com"},
    {"id": 2, "name": "Bob", "email": "bob@email.com"}
  ],
  "row_count": 2,
  "execution_time_ms": 45
}
```

### CSV

Spreadsheet-compatible:

```csv
ID,Name,Email
1,Alice,alice@email.com
2,Bob,bob@email.com
```

### Markdown

Documentation-friendly:

```markdown
| ID | Name  | Email           |
|----|-------|-----------------|
| 1  | Alice | alice@email.com |
| 2  | Bob   | bob@email.com   |
```

---

## Configuration

### Config File Location

- **macOS**: `~/Library/Application Support/querynl/config.yaml`
- **Linux**: `~/.config/querynl/config.yaml` (or `~/.querynl/config.yaml`)
- **Windows**: `%APPDATA%\querynl\config.yaml`

### Viewing Configuration

```bash
querynl config show
```

### Setting Preferences

```bash
# Set default output format
querynl config set default_output_format json

# Disable destructive query confirmation
querynl config set confirm_destructive false

# Set REPL history size
querynl config set repl_history_size 5000

# Enable telemetry (opt-in)
querynl config set enable_telemetry true
```

### Manual Configuration

Edit `config.yaml` directly:

```yaml
version: "1.0"

defaults:
  connection: prod-db
  output_format: table
  llm_provider: openai

preferences:
  enable_telemetry: false
  repl_history_size: 1000
  pager: less
  confirm_destructive: true
  color_output: auto

connections:
  prod-db:
    database_type: postgresql
    host: prod.example.com
    port: 5432
    database_name: production
    username: app_user
    ssl_enabled: true
```

---

## Security Best Practices

### Credential Storage

✅ **DO**:
- Use OS keychain (automatic)
- Use environment variables for CI/CD
- Set strong master password for headless servers

❌ **DON'T**:
- Store passwords in config files
- Commit credentials to version control
- Share keychain passwords via insecure channels

### Headless Servers (No Keychain)

```bash
# Option 1: Set master password for encrypted file
export QUERYNL_KEYRING_PASSWORD="secure-master-password"
querynl connect add prod-db

# Option 2: Use connection string directly
export QUERYNL_CONNECTION_STRING="postgresql://user:pass@host/db"
querynl query "count users"
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Run database health check
  env:
    QUERYNL_CONNECTION_STRING: ${{ secrets.DB_CONNECTION_STRING }}
  run: |
    querynl query --non-interactive "SELECT 1"
```

### SSH Tunnels

For databases behind SSH bastions:

```bash
querynl connect add secure-db --type postgresql --ssh-tunnel
```

Configure SSH tunnel details when prompted:
- SSH host, port, username
- SSH key path or password
- Remote database host and port

---

## Automation & Scripting

### Exit Codes

- `0`: Success
- `1`: General error
- `2`: Invalid arguments
- `3`: Connection error
- `4`: Query execution error
- `5`: Configuration error

### Scripting Example

```bash
#!/bin/bash
set -e

# Health check
if ! querynl query --non-interactive "SELECT 1" > /dev/null; then
  echo "Database health check failed"
  exit 1
fi

# Export data
querynl query --format json "all active users" > users.json

# Process with jq
jq '.rows | length' users.json

echo "Backup complete"
```

### Non-Interactive Mode

Disable all prompts:

```bash
querynl query --non-interactive "delete from temp_table"
# or
querynl query -y "delete from temp_table"
```

### Piping Results

```bash
# Count results with jq
querynl query --format json "all users" | jq '.row_count'

# Filter results
querynl query --format json "all orders" | jq '.rows[] | select(.status == "pending")'

# CSV processing
querynl query --format csv "sales data" | cut -d, -f1,3 | sort
```

---

## Troubleshooting

### Connection Issues

**Problem**: "Connection refused"

```bash
querynl connect test my-db
```

**Solutions**:
- Check host/port are correct
- Verify database is running
- Check firewall rules
- Test with `telnet <host> <port>`

---

**Problem**: "Authentication failed"

**Solutions**:
- Verify username/password are correct
- Check database user permissions
- Re-add connection: `querynl connect remove my-db && querynl connect add my-db`

---

### Keychain Issues

**Problem**: "Permission denied to access keychain" (macOS)

**Solutions**:
1. Open Keychain Access app
2. Find "querynl" entry
3. Right-click → Get Info → Access Control
4. Allow querynl to access this item

---

**Problem**: "D-Bus session not available" (Linux headless)

**Solution**: Use encrypted file fallback:

```bash
export QUERYNL_KEYRING_PASSWORD="your-master-password"
querynl connect add my-db
```

---

### Query Issues

**Problem**: "Table not found" but table exists

**Solutions**:
- Check schema/database name
- Run `\tables` in REPL to see all tables
- Try explicit schema: `querynl query "show rows from public.users"`

---

**Problem**: Generated SQL is incorrect

**Solutions**:
- Use `--explain` flag to see SQL without executing
- Provide more context in query: "show users from users table where status is active"
- Use REPL mode for iterative refinement

---

### Performance Issues

**Problem**: Slow query generation

**Solutions**:
- Check internet connection (LLM API calls)
- Verify LLM provider status
- Use `--timeout` to set limits

---

**Problem**: Large result sets freeze terminal

**Solutions**:
- Use `--limit` flag: `querynl query --limit 100 "all users"`
- Use `--output` to file: `querynl query --output results.txt "all users"`
- Use JSON format for programmatic processing

---

## Advanced Features

### Schema Design

```bash
# Design schema from description
querynl schema design "e-commerce with users, products, orders, and reviews"

# Visualize as ER diagram
querynl schema visualize ecommerce-schema.json --output diagram.md

# Analyze for issues
querynl schema analyze ecommerce-schema.json

# Modify schema
querynl schema modify ecommerce-schema.json "add wishlist feature"

# Apply to database
querynl schema apply ecommerce-schema.json --connection dev-db
```

### Migration Management

```bash
# Generate migration from schema changes
querynl migrate generate \
  --from old-schema.json \
  --to new-schema.json \
  --message "add indexes" \
  --framework alembic

# Preview migration
querynl migrate preview 20251013_add_indexes.sql

# Apply migrations
querynl migrate apply

# Check status
querynl migrate status

# Rollback last migration
querynl migrate rollback
```

### Query History

```bash
# Show recent queries
querynl history show --limit 20

# Search history
querynl history search "users"

# Export history
querynl history show --format json > query-history.json

# Clear history
querynl history clear --confirm
```

---

## Keyboard Shortcuts (REPL)

| Shortcut | Action |
|----------|--------|
| `Up/Down` | Navigate command history |
| `Tab` | Auto-complete commands/tables |
| `Ctrl+C` | Cancel current query (don't exit) |
| `Ctrl+D` | Exit REPL |
| `Ctrl+L` | Clear screen |
| `Ctrl+R` | Reverse history search |
| `Ctrl+A` | Move to start of line |
| `Ctrl+E` | Move to end of line |

---

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `QUERYNL_CONFIG` | Custom config file path | `/custom/config.yaml` |
| `QUERYNL_CONNECTION_STRING` | Direct connection string | `postgresql://user:pass@host/db` |
| `QUERYNL_KEYRING_PASSWORD` | Master password for encrypted file keyring | `secure-password` |
| `QUERYNL_LLM_API_KEY` | LLM API key (BYOK) | `sk-...` |
| `QUERYNL_NO_COLOR` | Disable color output | `1` |
| `QUERYNL_PAGER` | Custom pager command | `less -R` |

---

## Getting Help

### Built-in Help

```bash
# General help
querynl --help

# Command-specific help
querynl query --help
querynl connect --help
querynl schema --help
```

### Community & Support

- **Documentation**: https://docs.querynl.com
- **GitHub Issues**: https://github.com/querynl/querynl-cli/issues
- **Discord**: https://discord.gg/querynl
- **Email**: support@querynl.com

---

## Next Steps

Now that you've learned the basics:

1. **Add your production databases** and start querying
2. **Explore REPL mode** for interactive data exploration
3. **Try schema design** for your next project
4. **Integrate with CI/CD** for automated database tasks
5. **Share feedback** to help improve QueryNL

---

**Happy Querying!** 🚀
