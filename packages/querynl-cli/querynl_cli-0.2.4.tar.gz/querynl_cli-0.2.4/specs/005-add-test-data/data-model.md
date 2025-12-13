# Data Model: Test Data Generation

**Feature**: Test Data Generation for Schema Design Mode
**Date**: 2025-11-22

## Overview

This document defines the key entities and data structures for test data generation functionality. The feature uses a **plan-based architecture** where the LLM generates a data generation plan, and Python code executes that plan using the Faker library.

## Core Entities

### 1. TestDataRequest

**Description**: User's natural language request to generate test data, parsed and validated by the system.

**Attributes**:
- `user_query` (str): Original natural language query (e.g., "add 50 sample users")
- `target_tables` (List[str] | None): Specific tables to populate (None = all tables)
- `record_counts` (Dict[str, int] | None): Explicit counts per table (None = use defaults)
- `domain_context` (str | None): Optional domain context for realistic data (e.g., "e-commerce")
- `database_type` (str): Target database type ("mysql", "postgresql", "sqlite")

**Validation Rules**:
- `database_type` must be one of: "mysql", "postgresql", "sqlite"
- `record_counts` values must be positive integers (> 0)
- If `target_tables` specified, all tables must exist in current schema
- Default record count: 10-20 records per table when not specified

**Relationships**:
- Maps to → `SchemaMetadata` (from existing schema introspection)
- Produces → `DataGenerationPlan`

---

### 2. SchemaMetadata

**Description**: Introspected database schema information used for test data generation planning. This entity already exists in the codebase (`src/models/schema.py`) and is reused.

**Attributes**:
- `tables` (List[TableMetadata]): List of all tables in the schema
- `database_type` (str): Database system type
- `relationships` (List[ForeignKeyRelationship]): Foreign key dependencies between tables

**TableMetadata Sub-entity**:
- `name` (str): Table name
- `columns` (List[ColumnMetadata]): Column definitions
- `primary_key` (List[str]): Primary key column names
- `foreign_keys` (List[ForeignKeyMetadata]): Foreign key constraints
- `unique_constraints` (List[UniqueConstraintMetadata]): Unique constraints
- `check_constraints` (List[CheckConstraintMetadata]): Check constraints

**ColumnMetadata Sub-entity**:
- `name` (str): Column name
- `data_type` (str): SQL data type (e.g., "VARCHAR(255)", "INTEGER", "TIMESTAMP")
- `nullable` (bool): Whether column accepts NULL values
- `default_value` (Any | None): Default value if specified
- `is_auto_increment` (bool): Whether column is auto-generated (skip during INSERT)

**ForeignKeyMetadata Sub-entity**:
- `column` (str): Column name in current table
- `referenced_table` (str): Referenced table name
- `referenced_column` (str): Referenced column name in parent table

**State Transitions**:
- Created via schema introspection (existing functionality)
- Read by `TestDataGenerator` to understand structure
- Immutable during test data generation process

---

### 3. DataGenerationPlan

**Description**: LLM-generated plan specifying HOW to generate test data for each table and column. This is the key abstraction that separates planning (LLM) from execution (Python).

**Attributes**:
- `plan_id` (str): Unique identifier (UUID)
- `created_at` (datetime): Timestamp of plan creation
- `database_type` (str): Target database type
- `tables` (List[TableGenerationConfig]): Per-table generation configuration
- `insertion_order` (List[str]): Table names in dependency order (topological sort)
- `rationale` (str): Human-readable explanation of generation strategy
- `estimated_total_records` (int): Total number of records to be generated

**TableGenerationConfig Sub-entity**:
- `table_name` (str): Target table name
- `record_count` (int): Number of records to generate for this table
- `columns` (List[ColumnGenerationConfig]): Per-column generation configuration

**ColumnGenerationConfig Sub-entity**:
- `column_name` (str): Column name
- `faker_provider` (str): Faker method name (e.g., "name", "email", "random_int")
- `provider_params` (Dict[str, Any]): Parameters to pass to Faker method
- `is_primary_key` (bool): Whether this is a primary key column
- `is_foreign_key` (bool): Whether this references another table
- `foreign_key_config` (ForeignKeyConfig | None): FK resolution configuration
- `is_unique` (bool): Whether unique constraint applies
- `is_nullable` (bool): Whether NULL values allowed
- `null_probability` (float): Probability of generating NULL (0.0-1.0) if nullable

**ForeignKeyConfig Sub-entity**:
- `referenced_table` (str): Parent table name
- `referenced_column` (str): Parent column name
- `selection_strategy` (str): How to select FK values ("random", "sequential", "weighted")

**Validation Rules**:
- All `faker_provider` values must be valid Faker methods
- `insertion_order` must be topologically sorted (parents before children)
- All foreign key references must point to tables earlier in `insertion_order`
- `null_probability` must be between 0.0 and 1.0
- Tables in `insertion_order` must match tables in `tables` list

**State Transitions**:
1. **Created**: LLM generates plan from `TestDataRequest` and `SchemaMetadata`
2. **Validated**: Plan validated against schema and Faker capabilities
3. **Executing**: Plan being executed by `InsertionExecutor`
4. **Completed**: All records generated and inserted successfully
5. **Failed**: Execution failed with errors

---

### 4. GeneratedRecord

**Description**: A single record generated according to the plan, ready for insertion into the database.

**Attributes**:
- `table_name` (str): Target table name
- `column_values` (Dict[str, Any]): Column name → generated value mapping
- `generated_at` (datetime): Timestamp of record generation
- `primary_key_value` (Any | None): Generated primary key value (tracked for FK references)

**Example**:
```python
GeneratedRecord(
    table_name="customers",
    column_values={
        "id": 1,
        "name": "John Doe",
        "email": "john.doe.1@example.com",
        "created_at": "2025-11-22 10:30:00"
    },
    generated_at=datetime(2025, 11, 22, 10, 30, 0),
    primary_key_value=1
)
```

**Validation Rules**:
- All non-nullable columns must have values
- Values must match column data types
- Foreign key values must reference existing records
- Unique constraint columns must have unique values

---

### 5. InsertionBatch

**Description**: A batch of INSERT statements ready for execution against the database. Batching optimizes performance and enables transaction management.

**Attributes**:
- `batch_id` (str): Unique identifier (UUID)
- `table_name` (str): Target table name
- `insert_statements` (List[str]): SQL INSERT statements with literal values
- `record_count` (int): Number of records in this batch
- `database_type` (str): Target database dialect ("mysql", "postgresql", "sqlite")
- `estimated_size_bytes` (int): Estimated size of batch in bytes (for memory management)

**Validation Rules**:
- `record_count` should match number of INSERT statements
- Batch size should not exceed database limits:
  - MySQL: Limited by `max_allowed_packet` (default 16-64MB)
  - PostgreSQL: Limited by max parameters (32,767 per statement)
  - SQLite: No hard limit (constrained by memory)

**State Transitions**:
1. **Prepared**: Batch created with INSERT statements
2. **Executing**: Being sent to database
3. **Committed**: Successfully inserted and committed
4. **Failed**: Insertion failed with error
5. **Rolled Back**: Reverted due to error or cancellation

---

### 6. InsertionResult

**Description**: Outcome of test data generation operation, including success/failure statistics and detailed error information.

**Attributes**:
- `request_id` (str): Unique identifier linking back to original request
- `started_at` (datetime): Operation start timestamp
- `completed_at` (datetime): Operation completion timestamp
- `duration_seconds` (float): Total operation duration
- `total_records_requested` (int): Total records requested across all tables
- `total_records_inserted` (int): Successfully inserted records
- `total_records_failed` (int): Failed insertions
- `table_results` (Dict[str, TableInsertionResult]): Per-table detailed results
- `errors` (List[InsertionError]): Detailed error information
- `cancelled_by_user` (bool): Whether operation was cancelled via Ctrl+C

**TableInsertionResult Sub-entity**:
- `table_name` (str): Table name
- `records_inserted` (int): Successfully inserted records
- `records_failed` (int): Failed insertions
- `insertion_duration_seconds` (float): Time spent on this table

**InsertionError Sub-entity**:
- `table_name` (str): Table where error occurred
- `batch_id` (str): Batch identifier
- `record_index` (int | None): Index of failed record within batch (if known)
- `error_type` (str): Error classification ("constraint_violation", "syntax_error", "timeout", etc.)
- `constraint_name` (str | None): Violated constraint name (if applicable)
- `column_name` (str | None): Column causing error (if known)
- `error_message` (str): Detailed error message from database
- `failed_record` (Dict[str, Any] | None): The record that failed (if available)

**State Transitions**:
1. **In Progress**: Operation executing
2. **Completed Successfully**: All records inserted (total_records_failed = 0)
3. **Completed with Errors**: Some records failed (total_records_failed > 0)
4. **Cancelled**: User cancelled operation
5. **Failed**: Fatal error occurred

---

### 7. ForeignKeyTracker

**Description**: Runtime state tracker that maintains generated primary key values for foreign key resolution. This is not persisted but maintained in memory during generation.

**Attributes**:
- `table_name` (str): Table name
- `generated_ids` (List[Any]): List of generated primary key values
- `id_index_map` (Dict[Any, int]): Map from ID value to list index (for fast lookup)

**Operations**:
- `add_id(value)`: Record a newly generated primary key
- `get_random_id()`: Retrieve random ID for foreign key reference
- `get_id_by_index(index)`: Retrieve specific ID by position
- `get_all_ids()`: Retrieve all generated IDs

**Example Usage**:
```python
# After inserting customers
customer_tracker = ForeignKeyTracker("customers")
customer_tracker.add_id(1)
customer_tracker.add_id(2)
customer_tracker.add_id(3)

# When generating orders
order_customer_id = customer_tracker.get_random_id()  # Returns 1, 2, or 3
```

---

## Data Flow

```
┌─────────────────────┐
│  User Query         │
│ "add sample data"   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  TestDataRequest    │
│  - tables           │
│  - record_counts    │
└──────────┬──────────┘
           │
           ├───────────────────┐
           │                   │
           ▼                   ▼
┌─────────────────────┐  ┌──────────────────┐
│  SchemaMetadata     │  │  LLM Service     │
│  (introspection)    │  │  (planning)      │
└──────────┬──────────┘  └────────┬─────────┘
           │                      │
           └──────────┬───────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │ DataGenerationPlan  │
           │  - table configs    │
           │  - insertion order  │
           │  - Faker providers  │
           └──────────┬──────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │  Faker + Python     │
           │  (value generation) │
           └──────────┬──────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │  GeneratedRecords   │
           │  - actual values    │
           └──────────┬──────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │  InsertionBatch     │
           │  - INSERT statements│
           │  - literal values   │
           └──────────┬──────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │  Database           │
           │  (execution)        │
           └──────────┬──────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │  InsertionResult    │
           │  - success count    │
           │  - errors           │
           └─────────────────────┘
```

## Key Relationships

**Request → Plan**:
- One `TestDataRequest` generates one `DataGenerationPlan`
- Plan creation involves LLM analysis of schema structure

**Plan → Records**:
- One `DataGenerationPlan` generates many `GeneratedRecord` instances
- Generation follows plan's Faker provider specifications

**Records → Batches**:
- Many `GeneratedRecord` instances grouped into `InsertionBatch` instances
- Batch size optimized per database type (1K-10K records)

**Batches → Result**:
- Many `InsertionBatch` executions produce one `InsertionResult`
- Result aggregates success/failure statistics across all batches

**SchemaMetadata → Plan**:
- Schema metadata informs plan generation
- Constraints and relationships guide Faker provider selection

**ForeignKeyTracker → Records**:
- Tracker maintains state during generation
- Enables foreign key value resolution between related tables

## Constraints and Invariants

### Referential Integrity
- All foreign key values in `GeneratedRecord` must reference existing primary keys in parent tables
- Parent table records must be generated before child table records
- `insertion_order` in `DataGenerationPlan` must be topologically sorted

### Uniqueness
- All unique constraint columns must have distinct values across all `GeneratedRecord` instances for that table
- Primary key values must be unique within each table

### Data Type Compatibility
- Generated values in `GeneratedRecord.column_values` must be compatible with column data types in `SchemaMetadata`
- Database-specific type handling (e.g., MySQL TINYINT for booleans, PostgreSQL BOOLEAN)

### Nullability
- Non-nullable columns must always have non-NULL values in `GeneratedRecord`
- Nullable columns may have NULL values based on `null_probability` in plan

### Transaction Atomicity
- Each `InsertionBatch` is a transactional unit (commit or rollback together)
- Failed batches can be retried independently without affecting successful batches

## State Management

### Generation Session State
During a test data generation session, the system maintains:

1. **ForeignKeyTrackers**: One per table with foreign keys, tracking generated IDs
2. **UniqueValueSets**: One per unique constraint, tracking generated values to prevent duplicates
3. **BatchQueue**: Queue of prepared `InsertionBatch` instances awaiting execution
4. **ProgressState**: Current progress (tables completed, records inserted, estimated remaining)

### Error Recovery State
On constraint violations or errors:

1. **FailedRecords**: Collection of `GeneratedRecord` instances that failed insertion
2. **BatchSavepoints**: Database savepoint names for rollback capability
3. **RetryQueue**: Records eligible for retry after user intervention

## Examples

### Example 1: Simple Two-Table Schema

**Request**:
```json
{
  "user_query": "add 10 customers and 20 orders",
  "target_tables": ["customers", "orders"],
  "record_counts": {"customers": 10, "orders": 20},
  "database_type": "postgresql"
}
```

**Generated Plan**:
```json
{
  "tables": [
    {
      "table_name": "customers",
      "record_count": 10,
      "columns": [
        {"column_name": "id", "faker_provider": "uuid4", "is_primary_key": true},
        {"column_name": "name", "faker_provider": "name"},
        {"column_name": "email", "faker_provider": "email", "is_unique": true}
      ]
    },
    {
      "table_name": "orders",
      "record_count": 20,
      "columns": [
        {"column_name": "id", "faker_provider": "uuid4", "is_primary_key": true},
        {"column_name": "customer_id", "is_foreign_key": true,
         "foreign_key_config": {"referenced_table": "customers", "referenced_column": "id"}},
        {"column_name": "total", "faker_provider": "pydecimal",
         "provider_params": {"left_digits": 4, "right_digits": 2, "positive": true}}
      ]
    }
  ],
  "insertion_order": ["customers", "orders"],
  "rationale": "Generate 10 customers first, then 20 orders referencing those customers"
}
```

**Result**:
```json
{
  "total_records_inserted": 30,
  "total_records_failed": 0,
  "table_results": {
    "customers": {"records_inserted": 10, "records_failed": 0},
    "orders": {"records_inserted": 20, "records_failed": 0}
  },
  "duration_seconds": 3.45,
  "errors": []
}
```

### Example 2: Error Scenario

**Request**:
```json
{
  "user_query": "add 100 users",
  "target_tables": ["users"],
  "record_counts": {"users": 100},
  "database_type": "mysql"
}
```

**Result with Errors**:
```json
{
  "total_records_inserted": 95,
  "total_records_failed": 5,
  "table_results": {
    "users": {"records_inserted": 95, "records_failed": 5}
  },
  "errors": [
    {
      "table_name": "users",
      "error_type": "constraint_violation",
      "constraint_name": "unique_email",
      "column_name": "email",
      "error_message": "Duplicate entry 'john@example.com' for key 'unique_email'",
      "failed_record": {"name": "John Doe", "email": "john@example.com"}
    }
  ],
  "duration_seconds": 5.23
}
```

## Implementation Notes

### Pydantic Models

All entities should be implemented as Pydantic models for:
- Automatic validation
- JSON serialization/deserialization
- Type safety
- Clear error messages

Example:
```python
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from datetime import datetime

class ColumnGenerationConfig(BaseModel):
    column_name: str
    faker_provider: str
    provider_params: Dict[str, Any] = Field(default_factory=dict)
    is_primary_key: bool = False
    is_foreign_key: bool = False
    is_unique: bool = False
    is_nullable: bool = False
    null_probability: float = Field(default=0.0, ge=0.0, le=1.0)

    @validator('faker_provider')
    def validate_faker_provider(cls, v):
        from faker import Faker
        fake = Faker()
        if not hasattr(fake, v):
            raise ValueError(f"Invalid Faker provider: {v}")
        return v
```

### Schema Versioning

The data model should support evolution:
- Plan format versioning (e.g., `plan_version: "1.0"`)
- Backward compatibility for reading older plans
- Migration utilities for upgrading plan formats
