# Research: Natural Language Schema Design

**Feature**: 004-natural-language-based
**Date**: 2025-11-03
**Purpose**: Resolve technical uncertainties identified in Technical Context

## 1. ER Diagram Generation Library

### Decision: Use Mermaid Syntax Generation (Text-Based)

**Rationale**:
- Mermaid is a text-based diagramming syntax that can be rendered in many environments (GitHub, VS Code, browser tools)
- No external library dependency required - we can generate Mermaid syntax strings directly
- Lightweight and suitable for CLI output
- Already familiar format for developers

**Alternatives Considered**:
- **eralchemy2**: Python library for ER diagrams, but requires graphviz installation (heavyweight)
- **pygraphviz**: Requires graphviz binary, platform-dependent installation issues
- **diagrams**: Primarily for architecture diagrams, not optimized for database schemas

**Implementation Approach**:
```python
# Generate Mermaid ER diagram syntax as plain text
def generate_mermaid_erd(schema: SchemaProposal) -> str:
    lines = ["erDiagram"]

    # Define entities
    for table in schema.tables:
        lines.append(f"    {table.name} {{")
        for column in table.columns:
            lines.append(f"        {column.type} {column.name}")
        lines.append(f"    }}")

    # Define relationships
    for rel in schema.relationships:
        lines.append(f"    {rel.from_table} ||--o{{ {rel.to_table} : {rel.name}")

    return "\n".join(lines)
```

**Display Options**:
1. Print Mermaid syntax to terminal (users can copy to renderers)
2. Use Rich library to display in formatted code block
3. Future: Optional rendering to SVG using mermaid-cli if installed

**Dependencies**: None (built-in string generation)

---

## 2. Session State Management

### Decision: SQLite with JSON-Serialized Session Data

**Rationale**:
- QueryNL already uses SQLite for query history - consistent approach
- Mature, reliable, serverless database
- Built-in Python support (no external dependencies)
- Efficient querying for recent sessions, session lookup by ID/name
- JSON fields for flexible schema proposal storage

**Alternatives Considered**:
- **JSON files per session**: Simple but poor query performance for "list recent sessions"
- **Pickle files**: Not human-readable, version compatibility issues
- **In-memory only**: Lost on REPL exit, violates NFR-005

**Database Schema**:
```sql
CREATE TABLE schema_design_sessions (
    id TEXT PRIMARY KEY,  -- UUID
    name TEXT,  -- User-provided name for saved sessions
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT CHECK(status IN ('active', 'finalized', 'implemented')),

    -- Session data (JSON serialized)
    conversation_history TEXT,  -- JSON array of conversation turns
    current_schema TEXT,  -- JSON serialized SchemaProposal
    schema_versions TEXT,  -- JSON array of historical SchemaProposal objects
    uploaded_files TEXT,  -- JSON array of {path, analyzed_at, metadata}

    -- Metadata
    database_type TEXT,  -- postgresql, mysql, sqlite, mongodb
    target_database_name TEXT,

    -- Retention
    expires_at TIMESTAMP  -- created_at + 90 days
);

CREATE INDEX idx_sessions_updated ON schema_design_sessions(updated_at DESC);
CREATE INDEX idx_sessions_name ON schema_design_sessions(name);
CREATE INDEX idx_sessions_status ON schema_design_sessions(status);
```

**Session Management**:
- Auto-create session on `\schema design` if none exists
- Auto-save after each conversation turn
- `\schema save <name>` - assigns a name for easy retrieval
- `\schema load <name>` - loads named session
- Background cleanup task for expired sessions (>90 days)

**File References**:
- Store relative or absolute paths to uploaded files
- Validate file existence on session load
- Warn if uploaded files have been deleted

---

## 3. LLM Integration Testing Strategy

### Decision: Hybrid Approach - Mocked Responses + Optional Real Tests

**Rationale**:
- Fast, deterministic unit tests using mocked LLM responses
- Optional integration tests with real LLM for validation (CI/manual only)
- Validates prompt engineering and response parsing without API costs
- Compatible with existing pytest infrastructure

**Testing Layers**:

#### Layer 1: Unit Tests with Mocked LLM (Fast, Always Run)
```python
# tests/unit/test_schema_conversation.py
from unittest.mock import Mock, patch
import pytest

@patch('src.cli.llm.LLMService.generate')
def test_schema_design_conversation(mock_llm):
    # Mock LLM response
    mock_llm.return_value = {
        'content': 'Great! A few questions:\n1. Should customers have multiple addresses?\n2. Can an order contain multiple products?',
        'usage': {'total_tokens': 150}
    }

    conversation = SchemaConversation()
    response = conversation.process_user_input("I need to track customers and orders")

    # Validate prompt construction
    assert 'customers and orders' in mock_llm.call_args[0][0]
    # Validate response parsing
    assert 'multiple addresses' in response
```

#### Layer 2: Fixture-Based Response Testing (Medium Speed)
```python
# tests/fixtures/llm_responses.json
{
    "schema_design_initial": {
        "prompt_pattern": "track customers and orders",
        "response": "Great! A few questions:\n1. Should customers have multiple addresses?..."
    }
}

# Load fixtures instead of calling real LLM
@pytest.fixture
def llm_responses():
    with open('tests/fixtures/llm_responses.json') as f:
        return json.load(f)
```

#### Layer 3: Optional Real LLM Tests (Slow, Manual/CI Only)
```python
# tests/integration/test_real_llm.py
@pytest.mark.slow
@pytest.mark.skipif(not os.getenv('OPENAI_API_KEY'), reason="API key required")
def test_real_schema_generation():
    """Integration test with real LLM - use sparingly"""
    llm_service = LLMService()
    response = llm_service.generate_schema_proposal("track customers and orders")
    assert 'customers' in response.lower()
    assert 'orders' in response.lower()
```

**Test Organization**:
- `pytest tests/unit/` - Fast mocked tests (run on every commit)
- `pytest tests/integration/ -m "not slow"` - Integration tests without real LLM
- `pytest tests/integration/ -m slow` - Real LLM tests (manual/CI only)

**Mocking Library**: `unittest.mock` (built-in) or `pytest-mock` for cleaner syntax

**Benefits**:
- Fast test suite execution (<10 seconds for unit tests)
- No API costs during development
- Validates prompt construction and response parsing logic
- Option to validate with real LLM when needed

---

## 4. Additional Technology Decisions

### File Parsing Libraries

**Decision**: Use `pandas` for CSV/Excel, built-in `json` module for JSON

**Rationale**:
- pandas already commonly used for data analysis
- Handles CSV/Excel (.xlsx) with consistent API
- Automatic data type inference
- Handles large files efficiently (chunking support)

**Dependencies**:
- `pandas>=2.0.0` (add to requirements.txt)
- `openpyxl>=3.0.0` (Excel support for pandas)

### DDL Generation

**Decision**: Use SQLAlchemy schema objects + dialect-specific compilation

**Rationale**:
- SQLAlchemy already installed (database drivers dependency)
- Mature, well-tested DDL generation for PostgreSQL, MySQL, SQLite
- Handles database-specific syntax differences automatically
- For MongoDB: Custom JSON schema generation (no DDL)

**Example**:
```python
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey

metadata = MetaData()
customers = Table('customers', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100))
)

# Generate PostgreSQL DDL
from sqlalchemy.dialects import postgresql
ddl = CreateTable(customers).compile(dialect=postgresql.dialect())
```

### LLM Token Usage Tracking

**Decision**: Extend existing LLMService to track and display token usage

**Implementation**:
- Add token counter to session state
- Display in session info: `\schema info` command
- Warning when approaching rate limits

---

## Summary of Resolved Clarifications

| Unknown | Decision | Dependencies Added |
|---------|----------|-------------------|
| ER diagram library | Mermaid syntax generation (text-based) | None |
| Session state management | SQLite with JSON-serialized data | None (built-in) |
| LLM testing strategy | Hybrid: mocked responses + optional real tests | pytest-mock (optional) |
| File parsing | pandas for CSV/Excel, json for JSON | pandas>=2.0.0, openpyxl>=3.0.0 |
| DDL generation | SQLAlchemy schema + dialect compilation | sqlalchemy (already installed) |
| Token tracking | Extend LLMService with usage counter | None |

**Updated Technical Context**:
- **ER diagram generation**: Mermaid syntax (text-based, no external library)
- **Session state**: SQLite with JSON-serialized session data
- **LLM testing**: Mocked responses (unit) + optional real LLM (integration)

All "NEEDS CLARIFICATION" items from Technical Context have been resolved.
