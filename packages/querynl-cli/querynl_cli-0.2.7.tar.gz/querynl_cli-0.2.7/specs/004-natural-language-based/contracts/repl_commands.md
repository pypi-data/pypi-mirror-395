# REPL Command Contracts: Schema Design

**Feature**: 004-natural-language-based
**Date**: 2025-11-03
**Type**: CLI Interface Specification

## Overview

This document defines the contract for all `\schema` REPL commands, including syntax, parameters, outputs, and error cases.

---

## Command: `\schema design`

**Purpose**: Start a new schema design conversation or resume the most recent active session.

**Syntax**:
```
\schema design
```

**Parameters**: None

**Behavior**:
1. Check for existing active session
   - If found: Resume with "Resuming schema design session from [timestamp]"
   - If not found: Create new session with UUID
2. Display welcome message with instructions
3. Enter conversational mode (all subsequent inputs are schema design context)

**Output**:
```
Starting schema design session...

Let's design your database schema! What would you like to track?

Example: "I need to track customers and their orders"

Session ID: abc-123-def (auto-saved)
```

**Error Cases**:
- Database connection issue: "Cannot start session: schema storage unavailable"
- LLM service unavailable: "Cannot start session: AI service unavailable"

**Exit Conversational Mode**: Type `\schema show`, `\schema save`, or other `\schema` commands

---

## Command: `\schema upload <file>`

**Purpose**: Upload and analyze a data file (CSV, Excel, JSON) to inform schema design.

**Syntax**:
```
\schema upload <file_path>
\schema upload customers.csv
\schema upload /path/to/orders.xlsx
```

**Parameters**:
- `<file_path>` (required): Path to data file (relative or absolute)

**Behavior**:
1. Validate file exists and is readable
2. Check file size (<= 100MB per NFR-002)
3. Validate file type (CSV, .xlsx, .json)
4. Analyze file structure (columns, data types, sample values)
5. Detect potential entities and relationships
6. Add analysis to current session
7. Ask clarifying questions based on analysis

**Output**:
```
Analyzing customers.csv...
✓ Found 1,234 rows, 5 columns

Detected columns:
- customer_id (integer, appears to be unique)
- name (text)
- email (text)
- order_date (date)
- total_amount (decimal)

I notice this file contains both customer and order information mixed together.
Should I separate these into distinct tables (customers and orders)?
```

**Error Cases**:
- File not found: "Error: File 'customers.csv' not found"
- File too large: "Error: File size (150MB) exceeds maximum (100MB)"
- Invalid format: "Error: File 'data.txt' is not a supported format (csv, xlsx, json)"
- Parse error: "Error: Could not parse CSV file. Check for encoding issues or malformed data."

---

## Command: `\schema show [view]`

**Purpose**: Display the current schema design in various formats.

**Syntax**:
```
\schema show           # Default: text-based summary
\schema show text      # Text summary
\schema show erd       # Entity-relationship diagram (Mermaid)
\schema show ddl       # Database DDL statements
\schema show mapping   # File-to-table column mapping
```

**Parameters**:
- `[view]` (optional): Output format (text | erd | ddl | mapping)
- Default: `text`

**Behavior - `text`**:
```
Schema Design (Version 2)
Database: PostgreSQL

Tables:
┌─────────────┬────────────────────────────────┐
│ Table       │ Columns                        │
├─────────────┼────────────────────────────────┤
│ customers   │ id (INTEGER, PK)               │
│             │ name (VARCHAR(100), NOT NULL)  │
│             │ email (VARCHAR(255), UNIQUE)   │
├─────────────┼────────────────────────────────┤
│ orders      │ id (INTEGER, PK)               │
│             │ customer_id (INTEGER, FK)      │
│             │ order_date (DATE)              │
│             │ total (DECIMAL(10,2))          │
└─────────────┴────────────────────────────────┘

Relationships:
• orders.customer_id → customers.id (one-to-many)

Rationale:
This schema follows 3NF normalization to separate customer information
from order transactions, allowing customers to have multiple orders.
```

**Behavior - `erd`**:
```
erDiagram
    customers {
        INTEGER id PK
        VARCHAR name
        VARCHAR email UK
    }
    orders {
        INTEGER id PK
        INTEGER customer_id FK
        DATE order_date
        DECIMAL total
    }
    customers ||--o{ orders : places
```

**Behavior - `ddl`**:
```sql
-- PostgreSQL DDL for Schema Design (Version 2)

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE,
    total DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
```

**Behavior - `mapping`**:
```
File-to-Schema Mapping

customers.csv → customers table
  customer_id → id (type changed: text → integer)
  name → name (unchanged)
  email → email (unchanged)

customers.csv → orders table (split entity detected)
  order_date → order_date (unchanged)
  total_amount → total (renamed for clarity)
  customer_id → customer_id (foreign key)
```

**Error Cases**:
- No schema yet: "No schema design in current session. Start with `\schema design` and describe your requirements."
- Invalid view: "Unknown view 'xyz'. Use: text, erd, ddl, or mapping"

---

## Command: `\schema history`

**Purpose**: View previous schema versions and compare changes.

**Syntax**:
```
\schema history
\schema history 2      # Show specific version
```

**Parameters**:
- `[version]` (optional): Version number to display

**Behavior - List**:
```
Schema Version History

Version 3 (current) - 2025-11-03 14:30
  • Added customer_addresses table for multiple addresses
  • Changed customers.address to foreign key

Version 2 - 2025-11-03 14:15
  • Split customers and orders into separate tables
  • Added foreign key relationship

Version 1 - 2025-11-03 14:00
  • Initial proposal with denormalized structure

Use `\schema history <version>` to view details
Use `\schema revert <version>` to restore a previous version
```

**Behavior - Specific Version**:
(Displays `\schema show text` output for that version)

**Error Cases**:
- No versions: "No schema history in current session"
- Invalid version: "Version 5 not found. Available versions: 1-3"

---

## Command: `\schema finalize`

**Purpose**: Mark the current schema design as final and ready for implementation.

**Syntax**:
```
\schema finalize
```

**Parameters**: None

**Behavior**:
1. Run validation checks on current schema
2. Display warnings if any (missing indexes, potential issues)
3. Request confirmation
4. Update session status to 'finalized'
5. Display next steps (`\schema implement`)

**Output**:
```
Validating schema design...
✓ All tables have primary keys
✓ All foreign keys reference existing columns
✓ Data types are appropriate
⚠ Warning: Table 'orders' may benefit from index on 'order_date'

Mark this schema as finalized? (yes/no): yes

✓ Schema finalized (Version 3)

Next steps:
1. Choose target database: \schema implement <postgresql|mysql|sqlite|mongodb>
2. Review DDL: \schema show ddl
3. Execute: \schema execute
```

**Error Cases**:
- No schema: "No schema to finalize. Start with `\schema design`"
- Already finalized: "Schema already finalized. Use `\schema revert <version>` to make changes."

---

## Command: `\schema save <name>`

**Purpose**: Save the current session with a memorable name for later retrieval.

**Syntax**:
```
\schema save <name>
\schema save ecommerce_v1
```

**Parameters**:
- `<name>` (required): Unique name for this session

**Behavior**:
1. Validate name is unique
2. Assign name to current session
3. Persist to database

**Output**:
```
✓ Saved schema design as 'ecommerce_v1'

Load later with: \schema load ecommerce_v1
```

**Error Cases**:
- Name already exists: "Error: Session name 'ecommerce_v1' already exists. Use `\schema load` to open it or choose a different name."
- Invalid name: "Error: Session name must be alphanumeric with underscores/hyphens only"

---

## Command: `\schema load <name>`

**Purpose**: Load a previously saved schema design session.

**Syntax**:
```
\schema load <name>
\schema load ecommerce_v1
```

**Parameters**:
- `<name>` (required): Name of saved session

**Behavior**:
1. Query database for session by name
2. Load session state (conversation history, schema versions, uploaded files)
3. Display session summary
4. Resume conversational mode

**Output**:
```
Loading schema design 'ecommerce_v1'...

Session Details:
- Created: 2025-11-01 10:00
- Last Updated: 2025-11-01 12:30
- Status: finalized
- Database Type: PostgreSQL
- Current Version: 3
- Tables: customers, orders, products

Session loaded. You can continue designing or use:
- \schema show - View current schema
- \schema history - View version history
- \schema implement - Generate DDL for implementation
```

**Error Cases**:
- Not found: "Error: No saved session named 'xyz'. Use `\schema list` to see available sessions."
- Corrupted session: "Error: Session data corrupted. Cannot load."

---

## Command: `\schema implement <database>`

**Purpose**: Generate database-specific DDL statements for the finalized schema.

**Syntax**:
```
\schema implement <database_type>
\schema implement postgresql
\schema implement mysql
\schema implement sqlite
\schema implement mongodb  # Generates JSON schema
```

**Parameters**:
- `<database_type>` (required): Target database (postgresql | mysql | sqlite | mongodb)

**Behavior**:
1. Validate schema is finalized
2. Generate database-specific DDL
3. Display statements with explanations
4. Save DDL to session for review
5. Offer to execute via `\schema execute`

**Output (PostgreSQL)**:
```sql
-- PostgreSQL DDL for 'ecommerce_v1'
-- Generated: 2025-11-03 14:45

-- Create customers table
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create orders table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    total DECIMAL(10,2) NOT NULL CHECK (total >= 0),
    status VARCHAR(20) DEFAULT 'pending'
);

-- Create indexes for performance
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);

-- Notes:
-- • Foreign key uses ON DELETE CASCADE to remove orders when customer is deleted
-- • CHECK constraint ensures order totals are non-negative
-- • Indexes added on frequently queried columns

Ready to execute? Use: \schema execute
Save DDL to file? Use: \schema export schema.sql
```

**Output (MongoDB - JSON Schema)**:
```json
// MongoDB schema validation for 'ecommerce_v1'

db.createCollection("customers", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "email"],
      properties: {
        name: { bsonType: "string", maxLength: 100 },
        email: { bsonType: "string", pattern: "^.+@.+$" },
        created_at: { bsonType: "date" }
      }
    }
  }
});

db.customers.createIndex({ email: 1 }, { unique: true });
```

**Error Cases**:
- Schema not finalized: "Schema must be finalized before implementation. Use `\schema finalize` first."
- Invalid database type: "Unknown database 'postgres'. Use: postgresql, mysql, sqlite, or mongodb"
- No database connection: "Warning: No active database connection. DDL generated but cannot validate against existing schema."

---

## Command: `\schema execute`

**Purpose**: Execute the generated DDL statements against the connected database.

**Syntax**:
```
\schema execute
```

**Parameters**: None

**Behavior**:
1. Validate database connection exists
2. Check for conflicting tables/schemas in target database
3. Display confirmation prompt with warnings
4. Execute DDL in a transaction
5. Validate created schema matches design
6. Update session status to 'implemented'
7. Offer rollback on errors

**Output**:
```
Executing schema against: PostgreSQL (localhost:5432/ecommerce_dev)

Pre-execution checks:
✓ Database connection active
✓ No conflicting table names
⚠ Warning: This will create 3 new tables in the database

Tables to create:
- customers (3 columns, 1 index)
- orders (5 columns, 2 indexes, 1 foreign key)
- products (4 columns, 1 index)

Continue? (yes/no): yes

Creating tables...
✓ Created table 'customers'
✓ Created table 'orders'
✓ Created table 'products'
✓ Created indexes
✓ Created foreign key constraints

Schema implemented successfully!

Validation:
✓ All tables created
✓ All columns present with correct types
✓ All constraints applied

Session marked as 'implemented'.
```

**Error Cases**:
- No DDL generated: "No DDL to execute. Use `\schema implement <database>` first."
- No database connection: "Error: No active database connection. Use `\connect` to connect."
- Table conflicts: "Error: Table 'customers' already exists in database. Drop existing table or choose different names."
- Execution error: "Error creating table 'orders': [database error message]. Transaction rolled back."

---

## Command: `\schema validate`

**Purpose**: Validate that the implemented schema matches the design specification.

**Syntax**:
```
\schema validate
```

**Parameters**: None

**Behavior**:
1. Connect to target database
2. Introspect actual schema (tables, columns, constraints)
3. Compare with design specification
4. Report discrepancies

**Output**:
```
Validating implemented schema against design...

Checking table structure:
✓ customers: 3/3 columns match
✓ orders: 5/5 columns match
✗ products: Missing column 'description' (expected VARCHAR(500))

Checking constraints:
✓ All primary keys present
✓ All foreign keys present
⚠ Missing index 'idx_products_category'

Summary: 2 issues found
- 1 missing column
- 1 missing index

Recommendation: Re-run `\schema execute` or manually add missing elements.
```

**Error Cases**:
- Not implemented: "Schema not yet implemented. Use `\schema execute` first."
- No connection: "Cannot validate: no active database connection"

---

## Command: `\schema export <file>`

**Purpose**: Export schema design or DDL to a file.

**Syntax**:
```
\schema export <output_file>
\schema export schema.json        # Export design as JSON
\schema export schema.sql         # Export DDL (requires \schema implement first)
\schema export schema.md          # Export documentation
```

**Parameters**:
- `<output_file>` (required): Path to output file

**Behavior**:
- `.json` extension: Export SchemaProposal object as JSON
- `.sql` extension: Export generated DDL (requires `\schema implement`)
- `.md` extension: Export human-readable documentation
- Other: Prompt for format

**Output**:
```
Exporting schema design to 'schema.json'...
✓ Exported 3 tables, 2 relationships

File written: /Users/marcus/projects/schema.json
```

**Error Cases**:
- No schema: "No schema to export"
- No DDL for .sql export: "No DDL generated. Use `\schema implement` first."
- File write error: "Error: Cannot write to 'schema.json': Permission denied"

---

## Command: `\schema reset`

**Purpose**: Discard current session and start fresh.

**Syntax**:
```
\schema reset
```

**Parameters**: None

**Behavior**:
1. Display confirmation (destructive action)
2. Delete current session (if not saved with name)
3. Create new empty session

**Output**:
```
⚠ Warning: This will discard the current schema design session.

Current session:
- Version 3 (3 tables)
- Unsaved changes

Are you sure? (yes/no): yes

✓ Session reset. Starting fresh.

Use `\schema design` to begin a new schema design.
```

**Error Cases**:
- None (always succeeds if confirmed)

---

## Command: `\schema help`

**Purpose**: Display help information for schema design commands.

**Syntax**:
```
\schema help
\schema help upload    # Help for specific command
```

**Parameters**:
- `[command]` (optional): Specific command to get help for

**Output**: (Displays command reference with examples)

---

## Common Error Handling

All `\schema` commands follow these error handling principles:

1. **Validation Errors**: Display actionable message with suggested fix
2. **System Errors**: Display user-friendly message + log technical details
3. **Confirmation Prompts**: Used for destructive operations (finalize, execute, reset)
4. **Progressive Disclosure**: Simple commands stay simple, advanced options available via flags
5. **Context-Aware Help**: Suggest next command based on current state

**Example Error Output**:
```
Error: No active schema design session

To get started:
1. \schema design - Start a new schema design
2. \schema load <name> - Load a saved session
3. \schema help - View all schema commands
```

---

## Command State Transitions

```
[No Session]
    ↓ \schema design
[Active Session] ←→ (\schema upload, conversation, \schema show)
    ↓ \schema finalize
[Finalized Session]
    ↓ \schema implement <db>
[DDL Generated]
    ↓ \schema execute
[Implemented Session]
    ↓ \schema validate
[Validated]

At any point:
- \schema save <name> (preserves session)
- \schema reset (returns to No Session)
- \schema load <name> (loads saved session)
```

---

## Testing Contract

Each command must have:
1. **Unit test**: Command parsing and validation
2. **Integration test**: End-to-end workflow with mocked LLM
3. **Error test**: All error cases covered
4. **Output test**: Verify formatted output matches examples

Example test:
```python
def test_schema_upload_command(repl_session, tmp_path):
    # Create test CSV
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("id,name\n1,Alice\n2,Bob")

    # Execute command
    result = repl_session.execute(f"\\schema upload {csv_file}")

    # Assertions
    assert "Analyzing test.csv" in result
    assert "2 rows, 2 columns" in result
    assert len(repl_session.current_session.uploaded_files) == 1
```
