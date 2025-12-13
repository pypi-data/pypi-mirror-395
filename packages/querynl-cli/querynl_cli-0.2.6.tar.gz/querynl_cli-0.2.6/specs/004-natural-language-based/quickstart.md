# Quickstart: Natural Language Schema Design

**Feature**: 004-natural-language-based
**Audience**: Developers implementing this feature
**Date**: 2025-11-03

## Overview

This guide helps you implement the natural language schema design feature for QueryNL. It covers the essential implementation steps, key decisions, and testing strategies.

---

## Prerequisites

Before starting implementation:

1. **Read Design Documents**:
   - [spec.md](spec.md) - Feature requirements and user stories
   - [plan.md](plan.md) - Technical architecture and structure
   - [data-model.md](data-model.md) - Database schema and entities
   - [research.md](research.md) - Technology decisions

2. **Development Environment**:
   - Python 3.11+
   - QueryNL development environment set up
   - Database clients for PostgreSQL, MySQL, SQLite, MongoDB (for testing)

3. **Dependencies to Add**:
   ```txt
   pandas>=2.0.0        # File parsing
   openpyxl>=3.0.0      # Excel support
   pytest-mock>=3.12.0  # LLM mocking in tests
   ```

---

## Implementation Roadmap

### Phase 1: Foundation (P1 - Conversational Design)

**Goal**: Enable users to design schemas through conversation alone.

**Tasks**:
1. Create session management infrastructure
2. Implement LLM conversation orchestration
3. Build schema generator (from natural language)
4. Add REPL command handlers (`\schema design`, `\schema show`)
5. Implement Mermaid ER diagram generation
6. Write unit tests with mocked LLM

**Deliverables**:
- Users can type `\schema design`, describe requirements, and receive schema proposals
- Schemas can be viewed in text and ERD formats
- Sessions persist across REPL exits

**Success Metric**: User Story 1 acceptance scenarios pass

---

### Phase 2: File Upload (P2 - Data-Driven Design)

**Goal**: Enable schema design from uploaded data files.

**Tasks**:
1. Implement file analyzer for CSV/Excel/JSON
2. Add column type inference logic
3. Build entity detection (multiple tables in one file)
4. Add relationship detection across files
5. Extend schema generator to use file analysis
6. Add `\schema upload` command
7. Write integration tests with sample files

**Deliverables**:
- Users can upload data files and receive schema proposals based on actual data
- System detects relationships across multiple files
- File-to-schema mapping visible via `\schema show mapping`

**Success Metric**: User Story 2 acceptance scenarios pass

---

### Phase 3: Iterative Refinement (P3 - Versioning)

**Goal**: Support iterative schema design with version history.

**Tasks**:
1. Implement schema versioning in session model
2. Add schema refinement logic (LLM-based changes)
3. Add `\schema history`, `\schema finalize`, `\schema save/load` commands
4. Implement trade-off explanation for design alternatives
5. Write workflow tests for iteration scenarios

**Deliverables**:
- Users can refine schemas through conversation
- Version history tracks all iterations
- Named sessions can be saved and restored

**Success Metric**: User Story 3 acceptance scenarios pass

---

### Phase 4: Implementation (P4 - DDL Generation & Execution)

**Goal**: Implement finalized schemas in actual databases.

**Tasks**:
1. Build DDL generators for PostgreSQL, MySQL, SQLite
2. Build MongoDB schema validation generator
3. Add schema validator (compare design vs actual)
4. Add `\schema implement`, `\schema execute`, `\schema validate` commands
5. Implement transactional DDL execution with rollback
6. Write contract tests for each database type

**Deliverables**:
- Users can generate database-specific DDL
- Schemas can be executed against connected databases
- Validation confirms implementation matches design

**Success Metric**: User Story 4 acceptance scenarios pass

---

## Step-by-Step Implementation Guide

### Step 1: Set Up Session Management

**File**: `src/cli/schema_design/session.py`

```python
# 1. Create SchemaDesignSession dataclass (from data-model.md)
# 2. Create SchemaSessionManager class
# 3. Implement SQLite schema (see data-model.md for DDL)
# 4. Write tests

# Quick test:
manager = SchemaSessionManager("~/.querynl/schema_sessions.db")
session = manager.create_session()
assert session.id is not None
manager.save_session(session)
loaded = manager.load_session(session.name)
assert loaded.id == session.id
```

**Testing Checklist**:
- [ ] Create session generates UUID
- [ ] Save/load roundtrip preserves all fields
- [ ] get_active_session returns most recent
- [ ] list_sessions ordered by updated_at
- [ ] cleanup_expired removes old sessions

---

### Step 2: Implement Conversation Orchestration

**File**: `src/cli/schema_design/conversation.py`

```python
# 1. Create SchemaConversation class
# 2. Build system prompt for schema design expertise
# 3. Implement conversation context building
# 4. Add intent detection (describe_requirement, answer_question, etc.)
# 5. Write tests with mocked LLM

# System prompt structure:
SYSTEM_PROMPT = """
You are a database schema design expert. Your role is to help users design
normalized, efficient database schemas through conversation.

Guidelines:
- Ask clarifying questions about relationships, constraints, cardinality
- Propose schemas in 3NF by default
- Explain trade-offs when denormalization is discussed
- Be concise and actionable
- Use plain language, avoid jargon unless user is technical

Current schema design session:
{session_context}
"""

# Mock LLM in tests:
@patch('src.cli.llm.LLMService.generate')
def test_conversation(mock_llm):
    mock_llm.return_value = "Great! Should customers have multiple addresses?"
    response = conversation.process_user_input("track customers and orders")
    assert "addresses" in response
```

**Testing Checklist**:
- [ ] System prompt includes session context
- [ ] User input appended to conversation history
- [ ] LLM responses parsed and returned
- [ ] Token usage tracked in metadata
- [ ] Error handling for LLM failures

---

### Step 3: Build Schema Generator

**File**: `src/cli/schema_design/schema_generator.py`

```python
# 1. Create SchemaGenerator class
# 2. Implement generate_from_description() using LLM
# 3. Implement schema validation logic
# 4. Write tests with fixture-based schemas

# LLM prompt for schema generation:
SCHEMA_GENERATION_PROMPT = """
Based on this requirement: "{description}"

Generate a {normalization_level} normalized database schema for {database_type}.

Output format (JSON):
{{
  "tables": [
    {{
      "name": "table_name",
      "columns": [
        {{"name": "id", "data_type": "integer", "constraints": ["PRIMARY KEY"]}}
      ]
    }}
  ],
  "relationships": [...],
  "rationale": "Why this design was chosen"
}}
"""

# Test with fixture:
def test_generate_schema():
    schema = generator.generate_from_description(
        "track customers and orders",
        database_type="postgresql"
    )
    assert len(schema.tables) >= 2
    assert any(t.name == "customers" for t in schema.tables)
```

**Testing Checklist**:
- [ ] Generates tables with primary keys
- [ ] Creates foreign key relationships
- [ ] Includes rationale for decisions
- [ ] Validates schema structure
- [ ] Handles LLM errors gracefully

---

### Step 4: Add REPL Commands

**File**: `src/cli/commands/schema.py`

```python
# 1. Create schema command router
# 2. Implement subcommands (design, show, upload, etc.)
# 3. Integrate with existing REPL infrastructure
# 4. Add tab completion support

import click
from ..repl import REPLSession

@click.group()
def schema():
    """Schema design commands."""
    pass

@schema.command()
def design():
    """Start schema design conversation."""
    session = get_or_create_session()
    console.print("Let's design your database schema! What would you like to track?")
    # Enter conversational mode...

@schema.command()
@click.argument('view', default='text')
def show(view):
    """Display current schema."""
    session = get_active_session()
    if view == 'erd':
        erd = MermaidERDGenerator.generate(session.current_schema)
        console.print(Syntax(erd, "mermaid"))
    elif view == 'text':
        # Format as table...
```

**File**: `src/cli/repl.py` (update)

```python
# Add schema commands to REPL completer
repl_commands = [
    "\\help", "\\connect", "\\tables",
    "\\schema design", "\\schema upload", "\\schema show",
    "\\schema history", "\\schema finalize", "\\schema save",
    "\\schema load", "\\schema implement", "\\schema execute",
    "\\exit", "\\quit"
]
```

**Testing Checklist**:
- [ ] Commands registered in REPL
- [ ] Tab completion works
- [ ] Error messages actionable
- [ ] Help text displays correctly
- [ ] State transitions validated

---

### Step 5: Implement File Analyzer

**File**: `src/cli/schema_design/file_analyzer.py`

```python
# 1. Create FileAnalyzer class
# 2. Implement CSV/Excel/JSON parsers
# 3. Add type inference logic
# 4. Implement entity detection
# 5. Build relationship detection

import pandas as pd

def analyze_csv(file_path: Path) -> FileAnalysis:
    # Read with pandas
    df = pd.read_csv(file_path, nrows=10000)  # Sample first 10k rows

    # Infer types
    columns = []
    for col in df.columns:
        dtype = df[col].dtype
        inferred_type = map_pandas_to_db_type(dtype)
        columns.append(ColumnInfo(
            name=col,
            inferred_type=inferred_type,
            nullable=df[col].isnull().any(),
            unique_values=df[col].nunique()
        ))

    return FileAnalysis(
        row_count=len(df),
        column_count=len(df.columns),
        columns=columns,
        detected_entities=detect_entities_from_columns(df.columns),
        potential_relationships=[]
    )
```

**Testing Checklist**:
- [ ] Handles CSV with various encodings
- [ ] Parses Excel (.xlsx) files
- [ ] Parses JSON arrays
- [ ] Infers types correctly (string, int, float, date)
- [ ] Detects entities in denormalized files
- [ ] Finds relationships across files

---

### Step 6: Generate DDL

**File**: `src/cli/schema_design/ddl_generator.py`

```python
# 1. Create DDLGenerator class
# 2. Implement database-specific generators
# 3. Map generic types to DB-specific types
# 4. Add constraint generation

def generate_postgresql(schema: SchemaProposal) -> str:
    statements = []

    for table in schema.tables:
        cols = []
        for col in table.columns:
            col_def = f"{col.name} {col.data_type}"
            if col.constraints:
                col_def += " " + " ".join(col.constraints)
            cols.append(col_def)

        create_table = f"CREATE TABLE {table.name} (\n  "
        create_table += ",\n  ".join(cols)
        create_table += "\n);"
        statements.append(create_table)

    # Add foreign keys...
    # Add indexes...

    return "\n\n".join(statements)
```

**Testing Checklist** (Contract Tests):
- [ ] PostgreSQL DDL is syntactically valid
- [ ] MySQL DDL is syntactically valid
- [ ] SQLite DDL is syntactically valid
- [ ] MongoDB schema validation is valid JSON Schema
- [ ] Type mapping correct for each database
- [ ] Constraints generated correctly

---

### Step 7: Implement Validation

**File**: `src/cli/schema_design/validator.py`

```python
# 1. Create SchemaValidator class
# 2. Use existing schema_introspection.py to introspect DB
# 3. Compare expected vs actual schema
# 4. Generate validation report

def validate(schema: SchemaProposal) -> ValidationReport:
    # Introspect database
    actual = self.introspect_database()

    # Compare tables
    table_issues = self.compare_tables(schema.tables, actual)

    # Compare constraints
    constraint_issues = self.compare_constraints(schema, actual)

    return ValidationReport(
        tables_ok=len([t for t in table_issues if not t.issues]),
        tables_with_issues=len([t for t in table_issues if t.issues]),
        discrepancies=table_issues + constraint_issues
    )
```

**Testing Checklist**:
- [ ] Detects missing tables
- [ ] Detects missing columns
- [ ] Detects type mismatches
- [ ] Detects missing constraints
- [ ] Detects missing indexes
- [ ] Reports discrepancies clearly

---

## Testing Strategy

### Unit Tests (Fast, Always Run)

**Mock LLM responses** to avoid API costs:

```python
@pytest.fixture
def mock_llm(mocker):
    mock = mocker.patch('src.cli.llm.LLMService.generate')
    mock.return_value = {
        'content': 'Test response',
        'usage': {'total_tokens': 100}
    }
    return mock

def test_schema_generation(mock_llm):
    generator = SchemaGenerator(llm_service)
    schema = generator.generate_from_description("track users")
    assert schema is not None
    mock_llm.assert_called_once()
```

### Integration Tests (Medium Speed)

**Test workflows** with real file I/O but mocked LLM:

```python
def test_file_upload_workflow(tmp_path):
    # Create test CSV
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("id,name\n1,Alice\n2,Bob")

    # Analyze file
    analyzer = FileAnalyzer()
    file = analyzer.analyze_file(csv_file)

    # Verify analysis
    assert file.analysis.row_count == 2
    assert file.analysis.column_count == 2
```

### Contract Tests (Real Databases)

**Validate DDL** against real databases:

```python
@pytest.mark.integration
def test_postgresql_ddl_execution(pg_connection):
    """Test with real PostgreSQL database."""
    schema = create_test_schema()
    ddl = DDLGenerator.generate(schema, "postgresql")

    # Execute DDL
    pg_connection.execute(ddl)

    # Validate schema exists
    tables = pg_connection.get_tables()
    assert "customers" in tables
```

**Run contract tests**:
```bash
# Fast tests only
pytest tests/unit/

# Include integration (no real LLM)
pytest tests/integration/ -m "not slow"

# Full suite (real databases, optional real LLM)
pytest tests/ -m slow
```

---

## Database-Specific Considerations

### PostgreSQL
- Use `SERIAL` for auto-incrementing primary keys
- Support `JSONB` for flexible schemas
- Use `ON DELETE CASCADE` for foreign keys
- Generate indexes on foreign key columns

### MySQL
- Use `AUTO_INCREMENT` for primary keys
- Map `text` to `VARCHAR(255)` or `TEXT`
- Use `InnoDB` engine (default)
- Be careful with index key length limits

### SQLite
- Use `INTEGER PRIMARY KEY` for auto-increment
- Limited ALTER TABLE support (recreate tables for changes)
- Foreign keys disabled by default (PRAGMA foreign_keys = ON)
- No DECIMAL type (use REAL or TEXT)

### MongoDB
- No DDL, use JSON Schema validation
- Use nested documents for one-to-many relationships
- Denormalization often preferred
- Generate compound indexes for queries

---

## Common Pitfalls & Solutions

### Pitfall 1: LLM Responses Are Non-Deterministic

**Problem**: Schema generation varies between runs, making tests flaky.

**Solution**:
- Use fixtures with predefined LLM responses for unit tests
- Test the response parsing logic, not the LLM itself
- Use contract tests to validate final output, not intermediate steps

### Pitfall 2: File Parsing Errors

**Problem**: User files have encoding issues, missing headers, etc.

**Solution**:
- Try multiple encodings (utf-8, latin-1, cp1252)
- Detect missing headers (numeric column names like "0", "1")
- Provide helpful error messages with suggested fixes

### Pitfall 3: Large Conversation Histories

**Problem**: Sessions with 100+ turns use excessive tokens/memory.

**Solution**:
- Summarize old conversation turns (keep last 10 full, summarize rest)
- Warn user when conversation is getting long
- Offer `\schema reset` to start fresh

### Pitfall 4: Database Connection Issues During Execution

**Problem**: DDL execution fails mid-way, leaving partial schema.

**Solution**:
- Always use transactions for DDL execution
- Rollback on any error
- Validate connection before starting execution
- Show dry-run option (`\schema show ddl`)

---

## Performance Targets

| Operation | Target | Measurement |
|-----------|--------|-------------|
| Session load | <100ms | Time from command to display |
| File analysis (10MB CSV) | <5s | Time to analyze and display results |
| Schema generation (LLM) | <5s | Time to receive LLM response (95th %ile) |
| DDL generation | <500ms | Time to generate SQL from schema |
| DDL execution (3 tables) | <2s | Time to create tables in database |
| Mermaid ERD generation | <200ms | Time to generate diagram syntax |

**Monitoring**:
- Add timing logs to key operations
- Track LLM token usage per session
- Monitor session database size

---

## Debugging Tips

### Enable Debug Logging

```python
# In src/cli/logging.py
import logging
logging.basicConfig(level=logging.DEBUG)

# Add debug logs in key places:
logger.debug(f"Generated schema with {len(tables)} tables")
logger.debug(f"LLM response: {response[:200]}...")
```

### Inspect Sessions

```bash
# SQLite CLI
sqlite3 ~/.querynl/schema_sessions.db
.tables
SELECT id, name, status, updated_at FROM schema_design_sessions;
SELECT conversation_history FROM schema_design_sessions WHERE id = 'abc-123';
```

### Test LLM Prompts

```python
# Standalone script to test LLM prompts
from src.cli.llm import LLMService

llm = LLMService()
response = llm.generate("""
<your system prompt>

User: I need to track customers and orders
""")
print(response)
```

---

## Next Steps After Implementation

1. **Run `/speckit.tasks`** to generate detailed task breakdown
2. **Implement in priority order**: P1 → P2 → P3 → P4
3. **Test incrementally**: Unit tests with each feature
4. **Manual testing**: Use REPL to design real schemas
5. **Update documentation**: Add examples to README

---

## Questions & Support

Refer to these documents for details:
- [spec.md](spec.md) - User requirements and acceptance criteria
- [plan.md](plan.md) - Architecture and technical decisions
- [data-model.md](data-model.md) - Database schema reference
- [contracts/repl_commands.md](contracts/repl_commands.md) - Command specifications
- [contracts/python_api.md](contracts/python_api.md) - Module API reference

Good luck with implementation! 🚀
