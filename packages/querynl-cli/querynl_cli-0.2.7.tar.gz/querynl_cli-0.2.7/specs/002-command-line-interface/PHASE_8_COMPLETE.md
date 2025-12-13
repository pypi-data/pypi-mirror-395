# Phase 8 Complete: Migration Generation (User Story 4)

**Completed**: 2025-10-16
**Tasks**: T104-T131 (28 tasks)
**Progress**: 131/178 tasks complete (74%)

## Summary

Phase 8 implements a complete database migration workflow for QueryNL CLI, enabling users to generate, preview, apply, and rollback schema migrations with support for multiple migration frameworks.

## Features Implemented

### 1. Migration Tracking System
- **File**: `src/cli/migrations.py` (168 lines)
- SQLite-based migration tracking database
- Functions: `init_migrations_db()`, `save_migration_record()`, `get_migrations()`, `update_migration_status()`, `delete_migration_record()`
- Tracks migration status (pending, applied, failed), timestamps, and error messages

### 2. MigrationRecord Model
- **File**: `src/cli/models.py` (lines 310-363)
- Fields: migration_id, connection_name, framework, direction, sql_content, rollback_sql, description, applied_at, status, error_message
- Validators for framework (alembic/flyway/raw), direction (up/down), status (pending/applied/failed)
- Serialization support with `to_dict()` and `from_dict()` methods

### 3. Migration Commands
- **File**: `src/cli/commands/migrate.py` (700+ lines)

#### `querynl migrate generate`
Generates migrations by diffing two schema files:
```bash
querynl migrate generate \
  --from schema-v1.json \
  --to schema-v2.json \
  --framework raw \
  --message "Add user authentication" \
  --output ./migrations/ \
  --connection mydb
```

Features:
- Schema diffing (detects added/removed/modified tables, columns, indexes)
- Up and down migration SQL generation
- Framework support: Alembic (Python), Flyway (SQL), Raw SQL
- Timestamp-based versioning (YYYYMMDDHHmmss format)
- Automatic migration tracking database entry

#### `querynl migrate preview`
Displays migration SQL with syntax highlighting:
```bash
querynl migrate preview 20251016120000_add_auth.sql
```

Features:
- Rich syntax-highlighted SQL display
- Plain English explanation of changes
- Migration metadata panel (ID, framework, status)

#### `querynl migrate apply`
Applies pending migrations to a database connection:
```bash
querynl migrate apply --connection mydb --confirm
```

Features:
- Transaction-wrapped execution (atomic rollback on error)
- Dry-run mode (`--dry-run`)
- Connection-specific filtering
- Confirmation prompt with affected migrations list
- Automatic status tracking (applied/failed)
- Detailed error messages on failure

#### `querynl migrate status`
Shows migration status table:
```bash
querynl migrate status --connection mydb
```

Features:
- Rich table display with color-coded status
- Columns: Migration ID, Description, Status, Applied At
- Summary statistics (applied/pending/failed counts)

#### `querynl migrate rollback`
Rolls back applied migrations:
```bash
querynl migrate rollback --connection mydb --steps 2 --confirm
```

Features:
- Rollback using down SQL from migration records
- `--steps` flag to rollback multiple migrations (default: 1)
- Transaction-wrapped execution
- Confirmation prompt
- Status tracking updates

## Files Created/Modified

### Created
1. `src/cli/migrations.py` - Migration tracking database
2. `src/cli/commands/migrate.py` - All migrate commands

### Modified
1. `src/cli/models.py` - Added MigrationRecord model
2. `src/cli/main.py` - Wired migrate command group

## Migration Workflow Example

```bash
# 1. Design schemas
querynl schema design "blog with posts and comments" --output schema-v1.json
querynl schema design "blog with posts, comments, and tags" --output schema-v2.json

# 2. Generate migration
querynl migrate generate \
  --from schema-v1.json \
  --to schema-v2.json \
  --framework raw \
  --message "add_tags_table" \
  --connection blog_db

# 3. Preview the migration
querynl migrate preview migrations/20251016120000_add_tags_table_up.sql

# 4. Check current status
querynl migrate status --connection blog_db

# 5. Apply the migration
querynl migrate apply --connection blog_db --confirm

# 6. Rollback if needed
querynl migrate rollback --connection blog_db --steps 1 --confirm
```

## Schema Diffing Logic

The migration generator detects:

### Added Tables
- Generates: `CREATE TABLE` statements with all columns
- Down SQL: `DROP TABLE` statements

### Removed Tables
- Generates: `DROP TABLE` statements
- Down SQL: `CREATE TABLE` statements (restore)

### Modified Tables
- Added columns: `ALTER TABLE ADD COLUMN`
- Removed columns: `ALTER TABLE DROP COLUMN`
- Modified columns: `ALTER TABLE ALTER COLUMN` (type/constraints)

### Added Indexes
- Generates: `CREATE INDEX` statements
- Down SQL: `DROP INDEX` statements

### Framework-Specific Output

**Alembic** (Python):
```python
# migrations/20251016120000_add_tags_table.py
def upgrade():
    op.create_table('tags', ...)

def downgrade():
    op.drop_table('tags')
```

**Flyway** (SQL):
```sql
-- migrations/V20251016120000__add_tags_table.sql
CREATE TABLE tags (...);
```

**Raw SQL**:
```
migrations/
  20251016120000_add_tags_table_up.sql
  20251016120000_add_tags_table_down.sql
```

## Database-Specific SQL Generation

The migration generator supports multiple database types:

- **PostgreSQL**: `SERIAL`, `TEXT`, `BOOLEAN`, `TIMESTAMPTZ`
- **MySQL**: `INT AUTO_INCREMENT`, `VARCHAR`, `TINYINT(1)`, `DATETIME`
- **SQLite**: `INTEGER PRIMARY KEY AUTOINCREMENT`, `TEXT`, `INTEGER`

## Migration Tracking Schema

```sql
CREATE TABLE migrations (
    migration_id TEXT PRIMARY KEY,
    connection_name TEXT NOT NULL,
    framework TEXT NOT NULL DEFAULT 'raw',
    direction TEXT NOT NULL DEFAULT 'up',
    sql_content TEXT NOT NULL,
    rollback_sql TEXT,
    description TEXT DEFAULT '',
    applied_at DATETIME,
    status TEXT NOT NULL DEFAULT 'pending',
    error_message TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_migrations_connection ON migrations(connection_name);
CREATE INDEX idx_migrations_status ON migrations(status);
```

## Testing Recommendations

1. **Schema Diffing**:
   ```bash
   # Create two schema versions
   querynl schema design "simple blog" --output v1.json
   querynl schema design "blog with tags and categories" --output v2.json

   # Generate migration
   querynl migrate generate --from v1.json --to v2.json --message "add_taxonomy"
   ```

2. **Migration Application**:
   ```bash
   # Connect to test database
   querynl connect add testdb --db-type postgresql --host localhost

   # Apply migration
   querynl migrate apply --connection testdb --confirm

   # Verify status
   querynl migrate status --connection testdb
   ```

3. **Rollback**:
   ```bash
   # Rollback last migration
   querynl migrate rollback --connection testdb --steps 1 --confirm

   # Verify tables removed
   querynl query tables --connection testdb
   ```

4. **Dry Run**:
   ```bash
   # Preview without executing
   querynl migrate apply --connection testdb --dry-run
   ```

## Known Limitations (MVP)

1. **Column Modifications**: Complex column alterations (e.g., changing NOT NULL to NULLABLE) may require manual SQL editing
2. **Data Migrations**: Only schema migrations supported; data transformations not included
3. **Framework Testing**: Alembic/Flyway outputs generated but not tested with actual framework tools
4. **Concurrent Migrations**: No locking mechanism for simultaneous migration applications

## Next Phase

**Phase 9: User Story 5 - Scriptable Commands for Automation**
- Tasks: T132-T143 (12 tasks)
- Focus: Exit codes, stderr/stdout separation, non-TTY compatibility
- Goal: Enable CI/CD integration with proper automation support

## Progress Update

- **Total Tasks**: 178
- **Completed**: 131 (74%)
- **Remaining**: 47 (26%)
  - Phase 9: 12 tasks (Scripting & Automation)
  - Phase 10: 13 tasks (Configuration Management)
  - Phase 11: 22 tasks (Polish & Validation)
