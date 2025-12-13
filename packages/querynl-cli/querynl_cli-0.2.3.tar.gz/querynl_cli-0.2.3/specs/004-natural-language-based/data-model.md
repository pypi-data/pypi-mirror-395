# Data Model: Natural Language Schema Design

**Feature**: 004-natural-language-based
**Date**: 2025-11-03
**Based on**: [spec.md](spec.md), [research.md](research.md)

## Overview

This document defines the data entities for the schema design feature. The model supports conversational schema design sessions with versioning, file uploads, and multi-database DDL generation.

## Storage Strategy

- **Primary Storage**: SQLite database (consistent with existing QueryNL query history)
- **Location**: `~/.querynl/schema_sessions.db`
- **Retention**: 90 days from last update (NFR-004)
- **Serialization**: JSON for complex objects (conversation history, schema proposals)

---

## Entity Definitions

### 1. SchemaDesignSession

Represents an active or historical schema design conversation with all state needed for resumption.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | TEXT (UUID) | PRIMARY KEY | Unique session identifier |
| `name` | TEXT | NULLABLE, UNIQUE | User-assigned name for saved sessions |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW | Session creation time |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW | Last modification time |
| `status` | TEXT | CHECK IN ('active', 'finalized', 'implemented') | Current session state |
| `conversation_history` | TEXT (JSON) | NOT NULL | Array of ConversationTurn objects |
| `current_schema` | TEXT (JSON) | NULLABLE | Current SchemaProposal object |
| `schema_versions` | TEXT (JSON) | NOT NULL | Array of SchemaProposal objects (version history) |
| `uploaded_files` | TEXT (JSON) | NOT NULL | Array of UploadedFile objects |
| `database_type` | TEXT | NULLABLE, CHECK IN ('postgresql', 'mysql', 'sqlite', 'mongodb') | Target database type |
| `target_database_name` | TEXT | NULLABLE | Target database name for implementation |
| `expires_at` | TIMESTAMP | NOT NULL | Expiration date (created_at + 90 days) |

**Indexes**:
- `idx_sessions_updated` ON `updated_at DESC` (for recent session retrieval)
- `idx_sessions_name` ON `name` (for named session lookup)
- `idx_sessions_status` ON `status` (for filtering by state)

**State Transitions**:
```
active → finalized (via \schema finalize)
finalized → implemented (via \schema execute)
active → active (iterative refinement)
```

**Validation Rules**:
- Session name must be unique if provided
- `expires_at` must be >= `created_at`
- `conversation_history` must be valid JSON array
- `current_schema` must match latest entry in `schema_versions`

---

### 2. ConversationTurn (JSON Object)

Represents a single exchange in the schema design conversation.

**Schema** (stored as JSON in `conversation_history` array):
```json
{
  "turn_id": "string (UUID)",
  "timestamp": "ISO 8601 datetime",
  "role": "user | assistant",
  "content": "string (conversation text)",
  "intent": "describe_requirement | answer_question | request_change | ask_clarification | propose_schema | explain_tradeoff",
  "metadata": {
    "tokens_used": "integer (LLM tokens)",
    "latency_ms": "integer (response time)",
    "triggered_action": "schema_generation | file_analysis | schema_refinement | null"
  }
}
```

**Relationships**:
- Parent: SchemaDesignSession (array field)
- Many turns per session (ordered chronologically)

**Validation**:
- `role` must be 'user' or 'assistant'
- `timestamp` must be valid ISO 8601 format
- User and assistant turns should alternate (not strictly enforced)

---

### 3. SchemaProposal (JSON Object)

Represents a complete database schema design with rationale.

**Schema** (stored as JSON in `current_schema` and `schema_versions` array):
```json
{
  "version": "integer (1-indexed)",
  "created_at": "ISO 8601 datetime",
  "database_type": "postgresql | mysql | sqlite | mongodb",
  "normalization_level": "1NF | 2NF | 3NF | denormalized",
  "tables": [
    {
      "name": "string",
      "columns": [
        {
          "name": "string",
          "data_type": "string (database-specific type)",
          "constraints": ["PRIMARY KEY", "NOT NULL", "UNIQUE", "CHECK(...)"],
          "default_value": "string | null",
          "description": "string (rationale for this column)"
        }
      ],
      "indexes": [
        {
          "name": "string",
          "columns": ["string"],
          "type": "btree | hash | gin | gist",
          "unique": "boolean"
        }
      ],
      "constraints": [
        {
          "type": "FOREIGN KEY | CHECK | UNIQUE",
          "definition": "string (SQL constraint definition)",
          "description": "string (rationale)"
        }
      ],
      "description": "string (purpose of this table)"
    }
  ],
  "relationships": [
    {
      "from_table": "string",
      "to_table": "string",
      "type": "one-to-one | one-to-many | many-to-many",
      "foreign_key": "string (column name)",
      "junction_table": "string | null (for many-to-many)",
      "description": "string (relationship rationale)"
    }
  ],
  "rationale": "string (overall design decisions and trade-offs)",
  "warnings": ["string (potential issues or considerations)"]
}
```

**For MongoDB** (document-oriented, no DDL):
```json
{
  "version": "integer",
  "database_type": "mongodb",
  "collections": [
    {
      "name": "string",
      "schema": {
        "fields": [
          {
            "name": "string",
            "type": "string | number | boolean | object | array",
            "required": "boolean",
            "nested_schema": "object | null (for nested documents)"
          }
        ],
        "indexes": [...],
        "validation_rules": "object (JSON Schema validation)"
      },
      "description": "string"
    }
  ],
  "rationale": "string"
}
```

**Relationships**:
- Parent: SchemaDesignSession (versioned array)
- Multiple proposals per session (history tracking)

**Validation**:
- Version numbers must be sequential
- Table/collection names must be unique within proposal
- Foreign key references must point to existing tables
- Data types must be valid for target database_type

---

### 4. UploadedFile (JSON Object)

Represents a data file uploaded for schema analysis.

**Schema** (stored as JSON in `uploaded_files` array):
```json
{
  "file_id": "string (UUID)",
  "file_path": "string (absolute path)",
  "file_name": "string (basename)",
  "file_type": "csv | xlsx | json",
  "file_size_bytes": "integer",
  "uploaded_at": "ISO 8601 datetime",
  "analysis": {
    "row_count": "integer",
    "column_count": "integer",
    "columns": [
      {
        "name": "string",
        "inferred_type": "string | integer | float | boolean | date | datetime",
        "nullable": "boolean",
        "unique_values": "integer",
        "sample_values": ["string (first 5 values)"]
      }
    ],
    "detected_entities": ["string (inferred table names)"],
    "potential_relationships": [
      {
        "from_column": "string",
        "to_file": "string (other uploaded file)",
        "to_column": "string",
        "confidence": "float (0.0-1.0)"
      }
    ]
  },
  "used_in_schema": "boolean (whether file influenced current schema)"
}
```

**Relationships**:
- Parent: SchemaDesignSession (array field)
- Multiple files per session
- Files can reference each other via `potential_relationships`

**Validation**:
- `file_path` must exist at time of upload (warn on session load if deleted)
- `file_type` must match file extension
- `file_size_bytes` must be <= 100MB (NFR-002)

---

## Relationships Diagram

```
SchemaDesignSession (1)
  ├─→ ConversationTurn (many) [embedded JSON array]
  ├─→ SchemaProposal (many versions) [embedded JSON array]
  └─→ UploadedFile (many) [embedded JSON array]
```

**Design Rationale**:
- Embedded JSON arrays avoid complex JOIN queries for session retrieval
- Single table design simplifies session export/import
- Version history maintains audit trail for iterative refinement

---

## Database Schema (SQLite DDL)

```sql
-- Schema design sessions table
CREATE TABLE schema_design_sessions (
    id TEXT PRIMARY KEY,  -- UUID v4
    name TEXT UNIQUE,     -- User-assigned name (nullable)
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'finalized', 'implemented')),

    -- Conversation and schema data (JSON serialized)
    conversation_history TEXT NOT NULL DEFAULT '[]',  -- Array of ConversationTurn
    current_schema TEXT,  -- SchemaProposal object (nullable until first proposal)
    schema_versions TEXT NOT NULL DEFAULT '[]',  -- Array of SchemaProposal (version history)
    uploaded_files TEXT NOT NULL DEFAULT '[]',  -- Array of UploadedFile

    -- Database target configuration
    database_type TEXT CHECK(database_type IN ('postgresql', 'mysql', 'sqlite', 'mongodb')),
    target_database_name TEXT,

    -- Retention
    expires_at TEXT NOT NULL  -- created_at + 90 days
);

-- Indexes for efficient querying
CREATE INDEX idx_sessions_updated ON schema_design_sessions(updated_at DESC);
CREATE INDEX idx_sessions_name ON schema_design_sessions(name) WHERE name IS NOT NULL;
CREATE INDEX idx_sessions_status ON schema_design_sessions(status);
CREATE INDEX idx_sessions_expires ON schema_design_sessions(expires_at);

-- Trigger to auto-update updated_at timestamp
CREATE TRIGGER update_session_timestamp
AFTER UPDATE ON schema_design_sessions
FOR EACH ROW
BEGIN
    UPDATE schema_design_sessions
    SET updated_at = datetime('now')
    WHERE id = NEW.id;
END;
```

---

## Data Access Patterns

### 1. Create New Session
```python
session = SchemaDesignSession(
    id=str(uuid.uuid4()),
    created_at=datetime.now(),
    expires_at=datetime.now() + timedelta(days=90),
    status='active',
    conversation_history=[],
    schema_versions=[],
    uploaded_files=[]
)
```

### 2. Resume Recent Session
```sql
SELECT * FROM schema_design_sessions
WHERE status = 'active'
ORDER BY updated_at DESC
LIMIT 1;
```

### 3. Load Named Session
```sql
SELECT * FROM schema_design_sessions
WHERE name = ?;
```

### 4. Add Conversation Turn
```python
turn = ConversationTurn(
    turn_id=str(uuid.uuid4()),
    timestamp=datetime.now().isoformat(),
    role='user',
    content=user_input,
    intent='describe_requirement'
)
session.conversation_history.append(turn)
# Serialize and save
```

### 5. Save New Schema Version
```python
new_version = SchemaProposal(
    version=len(session.schema_versions) + 1,
    created_at=datetime.now().isoformat(),
    tables=[...],
    relationships=[...]
)
session.schema_versions.append(new_version)
session.current_schema = new_version
# Serialize and save
```

### 6. Cleanup Expired Sessions
```sql
DELETE FROM schema_design_sessions
WHERE expires_at < datetime('now');
```

---

## Migration Strategy

**Initial Migration** (v1):
- Create `schema_design_sessions` table with full schema
- Create indexes
- Create update trigger

**Future Migrations**:
- Schema changes will use Alembic or similar migration tool
- JSON field evolution can happen transparently (add new fields with defaults)

---

## Validation Rules Summary

| Entity | Validation Rule | Error Handling |
|--------|----------------|----------------|
| SchemaDesignSession | Session name must be unique | Raise error on duplicate save |
| SchemaDesignSession | expires_at >= created_at | Auto-calculate on creation |
| ConversationTurn | role in ['user', 'assistant'] | Validate before append |
| SchemaProposal | Version numbers sequential | Auto-increment from array length |
| SchemaProposal | Foreign keys reference existing tables | Validate during schema generation |
| UploadedFile | File size <= 100MB | Reject upload with error message |
| UploadedFile | File exists at upload time | Warn on load if deleted |

---

## Performance Considerations

- **Session Load**: Single row query with JSON deserialization (~10ms for typical session)
- **Recent Sessions List**: Index on `updated_at DESC` ensures fast retrieval
- **Named Session Lookup**: Index on `name` for O(log n) lookup
- **Conversation History Growth**: Limit to 100 turns per session (warn user if exceeded)
- **File Analysis**: Stream large CSV files in chunks (pandas `chunksize` parameter)

---

## Security Considerations

- **File Path Validation**: Sanitize uploaded file paths to prevent directory traversal
- **SQL Injection**: Use parameterized queries for all database operations
- **Session Isolation**: Session IDs are UUIDs (not sequential) to prevent enumeration
- **Sensitive Data**: Do not store database credentials in sessions (use connection names)
- **File Content**: Do not store full file contents in database (only metadata and analysis results)

---

## Testing Strategy

**Unit Tests**:
- Session creation, save, load operations
- JSON serialization/deserialization
- Validation rules enforcement

**Integration Tests**:
- End-to-end session workflow (create → upload → propose → finalize → implement)
- Session persistence across process restarts
- Expired session cleanup

**Data Fixtures**:
- Sample sessions with various states (active, finalized, implemented)
- Sample schema proposals for each database type
- Sample uploaded file analysis results
