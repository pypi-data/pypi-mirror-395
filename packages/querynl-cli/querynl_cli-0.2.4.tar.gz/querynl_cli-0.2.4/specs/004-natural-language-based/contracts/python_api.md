# Python Module API Contracts

**Feature**: 004-natural-language-based
**Date**: 2025-11-03
**Type**: Internal Python API Specification

## Overview

This document defines the Python module interfaces for the schema design feature. These are internal APIs (not public SDK) used within QueryNL CLI.

---

## Module: `schema_design.session`

### Class: `SchemaSessionManager`

Manages schema design session lifecycle (create, save, load, cleanup).

```python
from typing import Optional
from datetime import datetime, timedelta
import uuid

class SchemaSessionManager:
    """Manages schema design session persistence and retrieval."""

    def __init__(self, db_path: str):
        """
        Initialize session manager with SQLite database path.

        Args:
            db_path: Path to sessions database (~/.querynl/schema_sessions.db)
        """
        ...

    def create_session(self) -> SchemaDesignSession:
        """
        Create a new schema design session.

        Returns:
            SchemaDesignSession: New session with UUID, empty state

        Raises:
            DatabaseError: If session storage unavailable
        """
        ...

    def get_active_session(self) -> Optional[SchemaDesignSession]:
        """
        Retrieve the most recently updated active session.

        Returns:
            SchemaDesignSession or None if no active sessions exist
        """
        ...

    def save_session(self, session: SchemaDesignSession) -> None:
        """
        Persist session to database (upsert operation).

        Args:
            session: Session to save

        Raises:
            DatabaseError: If save fails
            ValidationError: If session data invalid
        """
        ...

    def load_session(self, name: str) -> SchemaDesignSession:
        """
        Load a named session from storage.

        Args:
            name: User-assigned session name

        Returns:
            SchemaDesignSession

        Raises:
            SessionNotFoundError: If session name doesn't exist
            DatabaseError: If load fails
        """
        ...

    def list_sessions(self, limit: int = 10) -> list[SessionSummary]:
        """
        List recent sessions.

        Args:
            limit: Maximum number of sessions to return

        Returns:
            List of SessionSummary objects, ordered by updated_at DESC
        """
        ...

    def delete_session(self, session_id: str) -> None:
        """Delete a session by ID."""
        ...

    def cleanup_expired(self) -> int:
        """
        Remove sessions older than 90 days.

        Returns:
            Number of sessions deleted
        """
        ...
```

### Class: `SchemaDesignSession`

Represents a single schema design session with all state.

```python
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class SchemaDesignSession:
    """Schema design session with conversation and schema state."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    status: str = "active"  # active | finalized | implemented

    conversation_history: List[ConversationTurn] = field(default_factory=list)
    current_schema: Optional[SchemaProposal] = None
    schema_versions: List[SchemaProposal] = field(default_factory=list)
    uploaded_files: List[UploadedFile] = field(default_factory=list)

    database_type: Optional[str] = None  # postgresql | mysql | sqlite | mongodb
    target_database_name: Optional[str] = None
    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(days=90))

    def add_conversation_turn(self, role: str, content: str, intent: str = None) -> None:
        """Add a turn to conversation history."""
        ...

    def add_schema_version(self, schema: SchemaProposal) -> None:
        """Add a new schema version and set as current."""
        ...

    def finalize(self) -> None:
        """Mark schema as finalized."""
        if not self.current_schema:
            raise ValueError("No schema to finalize")
        self.status = "finalized"

    def mark_implemented(self) -> None:
        """Mark schema as implemented in database."""
        if self.status != "finalized":
            raise ValueError("Schema must be finalized before implementation")
        self.status = "implemented"
```

---

## Module: `schema_design.conversation`

### Class: `SchemaConversation`

Orchestrates LLM-based conversational schema design.

```python
from typing import Dict, Any

class SchemaConversation:
    """Manages conversational schema design flow with LLM."""

    def __init__(self, llm_service: LLMService, session: SchemaDesignSession):
        """
        Initialize conversation manager.

        Args:
            llm_service: LLM service for natural language processing
            session: Current schema design session
        """
        ...

    def process_user_input(self, user_input: str) -> str:
        """
        Process user input and generate LLM response.

        Args:
            user_input: Natural language input from user

        Returns:
            str: LLM-generated response

        Raises:
            LLMServiceError: If LLM unavailable or fails
        """
        ...

    def ask_clarifying_question(self, context: Dict[str, Any]) -> str:
        """
        Generate intelligent clarifying questions based on context.

        Args:
            context: Current schema design context

        Returns:
            str: Clarifying question(s) to ask user
        """
        ...

    def explain_tradeoff(self, design_option: str) -> str:
        """
        Explain trade-offs for a design decision.

        Args:
            design_option: Design choice to explain (e.g., "denormalization")

        Returns:
            str: Explanation of pros/cons
        """
        ...

    def _build_system_prompt(self) -> str:
        """Build LLM system prompt with schema design expertise."""
        ...

    def _build_conversation_context(self) -> List[Dict[str, str]]:
        """Build conversation history for LLM context."""
        ...
```

---

## Module: `schema_design.file_analyzer`

### Class: `FileAnalyzer`

Analyzes uploaded data files to infer schema structure.

```python
from pathlib import Path
from typing import List, Dict

class FileAnalyzer:
    """Analyzes data files to infer database schema."""

    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

    def analyze_file(self, file_path: Path) -> UploadedFile:
        """
        Analyze a data file and infer schema information.

        Args:
            file_path: Path to CSV, Excel, or JSON file

        Returns:
            UploadedFile: Analyzed file metadata

        Raises:
            FileNotFoundError: If file doesn't exist
            FileTooLargeError: If file > 100MB
            UnsupportedFileTypeError: If not CSV/Excel/JSON
            FileParseError: If file cannot be parsed
        """
        ...

    def analyze_csv(self, file_path: Path) -> FileAnalysis:
        """Analyze CSV file structure."""
        ...

    def analyze_excel(self, file_path: Path) -> FileAnalysis:
        """Analyze Excel (.xlsx) file structure."""
        ...

    def analyze_json(self, file_path: Path) -> FileAnalysis:
        """Analyze JSON file structure."""
        ...

    def infer_column_types(self, df: pd.DataFrame) -> List[ColumnInfo]:
        """
        Infer database column types from pandas DataFrame.

        Args:
            df: DataFrame with sample data

        Returns:
            List of ColumnInfo with inferred types
        """
        ...

    def detect_relationships(self, files: List[UploadedFile]) -> List[PotentialRelationship]:
        """
        Detect potential foreign key relationships across files.

        Args:
            files: List of analyzed files

        Returns:
            List of potential relationships with confidence scores
        """
        ...

    def detect_entities(self, file_analysis: FileAnalysis) -> List[str]:
        """
        Detect multiple entities within a single file.

        Args:
            file_analysis: Analyzed file structure

        Returns:
            List of detected entity/table names
        """
        ...
```

---

## Module: `schema_design.schema_generator`

### Class: `SchemaGenerator`

Generates normalized database schemas from requirements and file analysis.

```python
from typing import List, Dict, Optional

class SchemaGenerator:
    """Generates database schema proposals."""

    def __init__(self, llm_service: LLMService):
        """
        Initialize schema generator.

        Args:
            llm_service: LLM service for intelligent schema generation
        """
        ...

    def generate_from_description(
        self,
        description: str,
        database_type: str = "postgresql",
        normalization_level: str = "3NF"
    ) -> SchemaProposal:
        """
        Generate schema from natural language description.

        Args:
            description: User's requirements in natural language
            database_type: Target database (postgresql, mysql, sqlite, mongodb)
            normalization_level: 1NF, 2NF, 3NF, or denormalized

        Returns:
            SchemaProposal: Generated schema with rationale

        Raises:
            LLMServiceError: If schema generation fails
        """
        ...

    def generate_from_files(
        self,
        files: List[UploadedFile],
        database_type: str = "postgresql"
    ) -> SchemaProposal:
        """
        Generate schema from analyzed data files.

        Args:
            files: List of analyzed data files
            database_type: Target database

        Returns:
            SchemaProposal: Inferred schema

        Raises:
            ValueError: If no files provided
        """
        ...

    def refine_schema(
        self,
        current_schema: SchemaProposal,
        user_request: str
    ) -> SchemaProposal:
        """
        Refine existing schema based on user feedback.

        Args:
            current_schema: Current schema proposal
            user_request: User's requested change

        Returns:
            SchemaProposal: Refined schema (new version)
        """
        ...

    def validate_schema(self, schema: SchemaProposal) -> List[ValidationWarning]:
        """
        Validate schema design and return warnings.

        Args:
            schema: Schema to validate

        Returns:
            List of warnings (empty if no issues)
        """
        ...
```

---

## Module: `schema_design.ddl_generator`

### Class: `DDLGenerator`

Generates database-specific DDL statements from schema proposals.

```python
from typing import List

class DDLGenerator:
    """Generates database-specific DDL from schema proposals."""

    @staticmethod
    def generate(schema: SchemaProposal, database_type: str) -> str:
        """
        Generate DDL statements for a schema.

        Args:
            schema: Schema proposal
            database_type: Target database (postgresql, mysql, sqlite, mongodb)

        Returns:
            str: DDL statements (SQL or MongoDB commands)

        Raises:
            UnsupportedDatabaseError: If database type not supported
        """
        ...

    @staticmethod
    def generate_postgresql(schema: SchemaProposal) -> str:
        """Generate PostgreSQL DDL."""
        ...

    @staticmethod
    def generate_mysql(schema: SchemaProposal) -> str:
        """Generate MySQL DDL."""
        ...

    @staticmethod
    def generate_sqlite(schema: SchemaProposal) -> str:
        """Generate SQLite DDL."""
        ...

    @staticmethod
    def generate_mongodb(schema: SchemaProposal) -> str:
        """Generate MongoDB schema validation (JSON Schema)."""
        ...

    @staticmethod
    def _map_type_to_database(column_type: str, database_type: str) -> str:
        """
        Map generic type to database-specific type.

        Args:
            column_type: Generic type (string, integer, decimal, etc.)
            database_type: Target database

        Returns:
            str: Database-specific type (VARCHAR, INT, etc.)
        """
        ...
```

---

## Module: `schema_design.visualizer`

### Class: `MermaidERDGenerator`

Generates Mermaid ER diagrams from schema proposals.

```python
class MermaidERDGenerator:
    """Generates Mermaid ER diagram syntax."""

    @staticmethod
    def generate(schema: SchemaProposal) -> str:
        """
        Generate Mermaid ER diagram syntax.

        Args:
            schema: Schema proposal

        Returns:
            str: Mermaid ER diagram (text-based)

        Example output:
            erDiagram
                customers {
                    INTEGER id PK
                    VARCHAR name
                    VARCHAR email UK
                }
                orders {
                    INTEGER id PK
                    INTEGER customer_id FK
                }
                customers ||--o{ orders : places
        """
        ...

    @staticmethod
    def _format_table(table: SchemaTable) -> str:
        """Format a single table for Mermaid."""
        ...

    @staticmethod
    def _format_relationship(rel: SchemaRelationship) -> str:
        """Format a relationship for Mermaid."""
        ...
```

---

## Module: `schema_design.validator`

### Class: `SchemaValidator`

Validates implemented schemas against design specifications.

```python
from typing import List, Dict

class SchemaValidator:
    """Validates implemented database schemas."""

    def __init__(self, db_connection: DatabaseConnection):
        """
        Initialize validator with database connection.

        Args:
            db_connection: Active database connection
        """
        ...

    def validate(self, schema: SchemaProposal) -> ValidationReport:
        """
        Validate that implemented schema matches design.

        Args:
            schema: Schema proposal to validate against

        Returns:
            ValidationReport: Comparison results

        Raises:
            DatabaseError: If introspection fails
        """
        ...

    def introspect_database(self) -> Dict[str, Any]:
        """
        Introspect current database schema.

        Returns:
            Dict with tables, columns, constraints, indexes
        """
        ...

    def compare_tables(
        self,
        expected: List[SchemaTable],
        actual: Dict[str, Any]
    ) -> List[TableDiscrepancy]:
        """Compare expected vs actual tables."""
        ...

    def compare_constraints(
        self,
        expected: List[SchemaConstraint],
        actual: Dict[str, Any]
    ) -> List[ConstraintDiscrepancy]:
        """Compare expected vs actual constraints."""
        ...
```

---

## Data Transfer Objects

### ConversationTurn

```python
@dataclass
class ConversationTurn:
    """A single conversation exchange."""
    turn_id: str
    timestamp: datetime
    role: str  # "user" | "assistant"
    content: str
    intent: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
```

### SchemaProposal

```python
@dataclass
class SchemaProposal:
    """A complete database schema proposal."""
    version: int
    created_at: datetime
    database_type: str
    normalization_level: str
    tables: List[SchemaTable]
    relationships: List[SchemaRelationship]
    rationale: str
    warnings: List[str] = field(default_factory=list)
```

### SchemaTable

```python
@dataclass
class SchemaTable:
    """A database table definition."""
    name: str
    columns: List[SchemaColumn]
    indexes: List[SchemaIndex]
    constraints: List[SchemaConstraint]
    description: str
```

### SchemaColumn

```python
@dataclass
class SchemaColumn:
    """A table column definition."""
    name: str
    data_type: str
    constraints: List[str]
    default_value: Optional[str] = None
    description: str = ""
```

### UploadedFile

```python
@dataclass
class UploadedFile:
    """Metadata for an uploaded data file."""
    file_id: str
    file_path: Path
    file_name: str
    file_type: str  # "csv" | "xlsx" | "json"
    file_size_bytes: int
    uploaded_at: datetime
    analysis: FileAnalysis
    used_in_schema: bool = False
```

### FileAnalysis

```python
@dataclass
class FileAnalysis:
    """Results of file structure analysis."""
    row_count: int
    column_count: int
    columns: List[ColumnInfo]
    detected_entities: List[str]
    potential_relationships: List[PotentialRelationship]
```

---

## Exception Hierarchy

```python
class SchemaDesignError(Exception):
    """Base exception for schema design errors."""
    pass

class SessionNotFoundError(SchemaDesignError):
    """Raised when session name doesn't exist."""
    pass

class FileTooLargeError(SchemaDesignError):
    """Raised when uploaded file exceeds 100MB."""
    pass

class UnsupportedFileTypeError(SchemaDesignError):
    """Raised when file type not CSV/Excel/JSON."""
    pass

class FileParseError(SchemaDesignError):
    """Raised when file cannot be parsed."""
    pass

class UnsupportedDatabaseError(SchemaDesignError):
    """Raised when database type not supported."""
    pass

class ValidationError(SchemaDesignError):
    """Raised when schema validation fails."""
    pass

class LLMServiceError(SchemaDesignError):
    """Raised when LLM service unavailable or fails."""
    pass
```

---

## Testing Contracts

### Unit Test Requirements

Each class must have:
1. Test for successful happy path
2. Tests for all error conditions
3. Tests for edge cases (empty input, large input, etc.)
4. Mock external dependencies (LLM, database)

### Integration Test Requirements

1. End-to-end workflow tests (design → upload → propose → implement)
2. Multi-file upload and relationship detection
3. Database-specific DDL generation and execution
4. Session persistence across restarts

### Contract Test Requirements

1. DDL syntax validation for each database type
2. Schema validation against real databases
3. Mermaid syntax validation (can be parsed by Mermaid parsers)

---

## Usage Examples

### Creating and Managing Sessions

```python
# Create new session
manager = SchemaSessionManager("~/.querynl/schema_sessions.db")
session = manager.create_session()

# Resume active session
session = manager.get_active_session()
if not session:
    session = manager.create_session()

# Save session with name
session.name = "ecommerce_v1"
manager.save_session(session)

# Load named session
session = manager.load_session("ecommerce_v1")
```

### Conversational Schema Design

```python
# Initialize conversation
conversation = SchemaConversation(llm_service, session)

# Process user input
response = conversation.process_user_input(
    "I need to track customers and their orders"
)
print(response)  # LLM-generated clarifying questions

# Continue conversation
response = conversation.process_user_input(
    "yes, customers can have multiple addresses"
)
```

### File Analysis

```python
# Analyze uploaded file
analyzer = FileAnalyzer()
uploaded_file = analyzer.analyze_file(Path("customers.csv"))

# Add to session
session.uploaded_files.append(uploaded_file)

# Detect relationships across files
relationships = analyzer.detect_relationships(session.uploaded_files)
```

### Schema Generation

```python
# Generate from description
generator = SchemaGenerator(llm_service)
schema = generator.generate_from_description(
    "I need to track customers and orders",
    database_type="postgresql",
    normalization_level="3NF"
)

# Add to session
session.add_schema_version(schema)

# Refine schema
refined = generator.refine_schema(
    schema,
    "add support for multiple shipping addresses"
)
session.add_schema_version(refined)
```

### DDL Generation and Execution

```python
# Generate DDL
ddl = DDLGenerator.generate(schema, "postgresql")
print(ddl)

# Execute DDL (via database connection)
db_connection.execute(ddl)

# Validate implementation
validator = SchemaValidator(db_connection)
report = validator.validate(schema)
print(report.summary())
```
