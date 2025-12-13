"""
Test Data Generator API Contract

This module defines the Python API contract for test data generation functionality.
Since this is a CLI-only feature (not a REST API), these are internal Python class interfaces.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


# ============================================================================
# Request/Response Models
# ============================================================================

class TestDataRequest(BaseModel):
    """User's request to generate test data."""
    user_query: str = Field(..., description="Natural language query")
    target_tables: Optional[List[str]] = Field(None, description="Specific tables to populate")
    record_counts: Optional[Dict[str, int]] = Field(None, description="Explicit counts per table")
    domain_context: Optional[str] = Field(None, description="Domain context for realistic data")
    database_type: str = Field(..., description="Target database type")

    class Config:
        schema_extra = {
            "example": {
                "user_query": "add 100 sample customers and orders",
                "target_tables": ["customers", "orders"],
                "record_counts": {"customers": 100, "orders": 200},
                "domain_context": "e-commerce",
                "database_type": "postgresql"
            }
        }


class ColumnGenerationConfig(BaseModel):
    """Configuration for generating data for a single column."""
    column_name: str
    faker_provider: str
    provider_params: Dict[str, Any] = Field(default_factory=dict)
    is_primary_key: bool = False
    is_foreign_key: bool = False
    foreign_key_table: Optional[str] = None
    foreign_key_column: Optional[str] = None
    is_unique: bool = False
    is_nullable: bool = False
    null_probability: float = Field(default=0.0, ge=0.0, le=1.0)

    class Config:
        schema_extra = {
            "example": {
                "column_name": "email",
                "faker_provider": "email",
                "provider_params": {},
                "is_unique": True,
                "is_nullable": False
            }
        }


class TableGenerationConfig(BaseModel):
    """Configuration for generating data for a single table."""
    table_name: str
    record_count: int = Field(..., gt=0)
    columns: List[ColumnGenerationConfig]

    class Config:
        schema_extra = {
            "example": {
                "table_name": "customers",
                "record_count": 100,
                "columns": [
                    {
                        "column_name": "name",
                        "faker_provider": "name"
                    },
                    {
                        "column_name": "email",
                        "faker_provider": "email",
                        "is_unique": True
                    }
                ]
            }
        }


class DataGenerationPlan(BaseModel):
    """LLM-generated plan for test data generation."""
    plan_id: str
    created_at: datetime
    database_type: str
    tables: List[TableGenerationConfig]
    insertion_order: List[str]
    rationale: str
    estimated_total_records: int

    class Config:
        schema_extra = {
            "example": {
                "plan_id": "550e8400-e29b-41d4-a716-446655440000",
                "created_at": "2025-11-22T10:30:00Z",
                "database_type": "postgresql",
                "tables": [],
                "insertion_order": ["customers", "orders", "order_items"],
                "rationale": "Generate customers first, then orders, then line items to satisfy FK constraints",
                "estimated_total_records": 330
            }
        }


class ErrorType(str, Enum):
    """Classification of insertion errors."""
    CONSTRAINT_VIOLATION = "constraint_violation"
    FOREIGN_KEY_VIOLATION = "foreign_key_violation"
    SYNTAX_ERROR = "syntax_error"
    TIMEOUT = "timeout"
    CONNECTION_ERROR = "connection_error"
    UNKNOWN = "unknown"


class InsertionError(BaseModel):
    """Details of a failed record insertion."""
    table_name: str
    batch_id: str
    record_index: Optional[int] = None
    error_type: ErrorType
    constraint_name: Optional[str] = None
    column_name: Optional[str] = None
    error_message: str
    failed_record: Optional[Dict[str, Any]] = None

    class Config:
        schema_extra = {
            "example": {
                "table_name": "users",
                "batch_id": "batch_001",
                "record_index": 42,
                "error_type": "constraint_violation",
                "constraint_name": "unique_email",
                "column_name": "email",
                "error_message": "Duplicate entry 'john@example.com'",
                "failed_record": {"name": "John Doe", "email": "john@example.com"}
            }
        }


class TableInsertionResult(BaseModel):
    """Results of inserting data into a single table."""
    table_name: str
    records_inserted: int
    records_failed: int
    insertion_duration_seconds: float


class InsertionResult(BaseModel):
    """Complete results of test data generation operation."""
    request_id: str
    started_at: datetime
    completed_at: datetime
    duration_seconds: float
    total_records_requested: int
    total_records_inserted: int
    total_records_failed: int
    table_results: Dict[str, TableInsertionResult]
    errors: List[InsertionError]
    cancelled_by_user: bool = False

    class Config:
        schema_extra = {
            "example": {
                "request_id": "req_123",
                "started_at": "2025-11-22T10:30:00Z",
                "completed_at": "2025-11-22T10:30:15Z",
                "duration_seconds": 15.3,
                "total_records_requested": 300,
                "total_records_inserted": 295,
                "total_records_failed": 5,
                "table_results": {
                    "customers": {
                        "table_name": "customers",
                        "records_inserted": 100,
                        "records_failed": 0,
                        "insertion_duration_seconds": 5.1
                    }
                },
                "errors": [],
                "cancelled_by_user": False
            }
        }


# ============================================================================
# Core Service Interfaces
# ============================================================================

class ITestDataGenerator(ABC):
    """
    Core interface for test data generation orchestrator.

    Responsibilities:
    - Accept user requests
    - Coordinate with LLM to generate plans
    - Execute plans via data synthesizer and insertion executor
    - Return results
    """

    @abstractmethod
    async def generate_test_data(
        self,
        request: TestDataRequest,
        progress_callback: Optional[callable] = None,
        cancellation_token: Optional[callable] = None
    ) -> InsertionResult:
        """
        Generate and insert test data based on user request.

        Args:
            request: Test data generation request
            progress_callback: Optional callback for progress updates (completed, total)
            cancellation_token: Optional callback returning True if user cancelled

        Returns:
            InsertionResult with success/failure statistics

        Raises:
            ValueError: If request is invalid
            DatabaseError: If database operations fail
            LLMError: If LLM plan generation fails
        """
        pass

    @abstractmethod
    async def generate_plan(
        self,
        request: TestDataRequest,
        schema_metadata: Any
    ) -> DataGenerationPlan:
        """
        Generate test data plan using LLM.

        Args:
            request: User's test data request
            schema_metadata: Introspected database schema

        Returns:
            DataGenerationPlan ready for execution

        Raises:
            ValueError: If request cannot be fulfilled
            LLMError: If LLM fails to generate valid plan
        """
        pass

    @abstractmethod
    def validate_plan(self, plan: DataGenerationPlan) -> List[str]:
        """
        Validate plan before execution.

        Args:
            plan: Data generation plan to validate

        Returns:
            List of validation errors (empty if valid)
        """
        pass


class IDataSynthesizer(ABC):
    """
    Interface for generating realistic sample data values.

    Responsibilities:
    - Generate values using Faker based on plan
    - Handle unique constraints
    - Respect data types and constraints
    - Track generated IDs for FK resolution
    """

    @abstractmethod
    def generate_value(
        self,
        column_config: ColumnGenerationConfig,
        existing_values: Optional[set] = None
    ) -> Any:
        """
        Generate a single value for a column.

        Args:
            column_config: Column configuration from plan
            existing_values: Set of already-generated values (for uniqueness)

        Returns:
            Generated value appropriate for column type

        Raises:
            ValueError: If unable to generate valid value
        """
        pass

    @abstractmethod
    def generate_table_data(
        self,
        table_config: TableGenerationConfig,
        foreign_key_refs: Dict[str, List[Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate all data for a single table.

        Args:
            table_config: Table configuration from plan
            foreign_key_refs: Map of table_name -> list of generated IDs

        Returns:
            List of record dictionaries (column_name -> value)

        Raises:
            ValueError: If unable to generate data
        """
        pass

    @abstractmethod
    def clear_unique_cache(self):
        """Clear Faker's unique value cache."""
        pass


class IInsertionExecutor(ABC):
    """
    Interface for executing INSERT statements against the database.

    Responsibilities:
    - Build database-specific INSERT statements
    - Execute with transaction management
    - Handle errors and rollbacks
    - Track progress
    """

    @abstractmethod
    async def execute_insertion(
        self,
        table_name: str,
        records: List[Dict[str, Any]],
        batch_size: int = 1000,
        progress_callback: Optional[callable] = None
    ) -> TableInsertionResult:
        """
        Insert records into a table.

        Args:
            table_name: Target table name
            records: List of record dictionaries
            batch_size: Number of records per batch
            progress_callback: Optional progress callback

        Returns:
            TableInsertionResult with success/failure stats

        Raises:
            DatabaseError: If insertion fails critically
        """
        pass

    @abstractmethod
    def build_insert_statement(
        self,
        table_name: str,
        columns: List[str],
        values: List[Any]
    ) -> str:
        """
        Build database-specific INSERT statement with literal values.

        Args:
            table_name: Target table
            columns: Column names
            values: Column values

        Returns:
            SQL INSERT statement string with escaped literal values
        """
        pass

    @abstractmethod
    def escape_value(self, value: Any, database_type: str) -> str:
        """
        Escape value for database-specific SQL syntax.

        Args:
            value: Value to escape
            database_type: Target database ("mysql", "postgresql", "sqlite")

        Returns:
            Escaped value as string ready for SQL
        """
        pass


class ISchemaIntrospector(ABC):
    """
    Interface for database schema introspection.

    Note: This likely already exists in the codebase. This defines
    the minimum required interface for test data generation.
    """

    @abstractmethod
    async def introspect_schema(self, database_connection: Any) -> Any:
        """
        Introspect database schema.

        Args:
            database_connection: Active database connection

        Returns:
            SchemaMetadata object (from existing codebase)
        """
        pass

    @abstractmethod
    def get_table_dependencies(self, schema: Any) -> Dict[str, List[str]]:
        """
        Extract foreign key dependencies from schema.

        Args:
            schema: SchemaMetadata object

        Returns:
            Dict mapping table_name -> [list of tables it depends on]
        """
        pass

    @abstractmethod
    def topological_sort_tables(self, dependencies: Dict[str, List[str]]) -> List[str]:
        """
        Sort tables in dependency order (parents before children).

        Args:
            dependencies: Table dependency graph

        Returns:
            List of table names in insertion order

        Raises:
            ValueError: If circular dependencies detected
        """
        pass


# ============================================================================
# REPL Command Handler Interface
# ============================================================================

class ITestDataCommandHandler(ABC):
    """
    Interface for handling test data generation commands in the REPL.

    Integrates with existing REPL command structure.
    """

    @abstractmethod
    async def handle_generate_command(
        self,
        user_input: str,
        repl_session: Any
    ) -> None:
        """
        Handle user command to generate test data.

        Args:
            user_input: Raw user input (e.g., "add 100 sample users")
            repl_session: Active REPL session

        Side effects:
            - Displays generated SQL
            - Prompts for confirmation
            - Executes insertion
            - Shows progress and results
        """
        pass

    @abstractmethod
    def parse_test_data_request(self, user_input: str) -> TestDataRequest:
        """
        Parse natural language input into TestDataRequest.

        Args:
            user_input: User's natural language query

        Returns:
            Parsed TestDataRequest

        Raises:
            ValueError: If input cannot be parsed
        """
        pass

    @abstractmethod
    def detect_test_data_intent(self, user_input: str) -> bool:
        """
        Detect if user input is requesting test data generation.

        Args:
            user_input: User's input string

        Returns:
            True if test data generation intent detected
        """
        pass


# ============================================================================
# Factory/Builder Interfaces
# ============================================================================

class ITestDataGeneratorFactory(ABC):
    """Factory for creating test data generator instances."""

    @abstractmethod
    def create_generator(
        self,
        database_type: str,
        llm_service: Any,
        database_connection: Any
    ) -> ITestDataGenerator:
        """
        Create test data generator for specific database type.

        Args:
            database_type: "mysql", "postgresql", or "sqlite"
            llm_service: LLM service instance
            database_connection: Active database connection

        Returns:
            Configured ITestDataGenerator instance
        """
        pass


# ============================================================================
# Utility Types
# ============================================================================

class ProgressUpdate(BaseModel):
    """Progress update during test data generation."""
    current_table: str
    table_number: int
    total_tables: int
    records_completed: int
    records_total: int
    estimated_seconds_remaining: float
    current_speed_records_per_sec: float


class CancellationToken:
    """Token for checking if user cancelled operation."""

    def __init__(self):
        self._cancelled = False

    def cancel(self):
        """Mark operation as cancelled."""
        self._cancelled = True

    def is_cancelled(self) -> bool:
        """Check if operation was cancelled."""
        return self._cancelled

    def reset(self):
        """Reset cancellation state."""
        self._cancelled = False


# ============================================================================
# Usage Example
# ============================================================================

"""
Example usage flow:

# 1. User types in REPL
user_input = "add 100 sample customers and 200 orders"

# 2. Command handler detects test data intent
handler = TestDataCommandHandler(...)
if handler.detect_test_data_intent(user_input):
    request = handler.parse_test_data_request(user_input)

    # 3. Generate and execute
    generator = TestDataGenerator(llm_service, db_connection)

    cancellation_token = CancellationToken()

    def progress_callback(update: ProgressUpdate):
        print(f"Progress: {update.records_completed}/{update.records_total}")

    result = await generator.generate_test_data(
        request=request,
        progress_callback=progress_callback,
        cancellation_token=cancellation_token.is_cancelled
    )

    # 4. Display results
    print(f"Inserted {result.total_records_inserted} records")
    if result.total_records_failed > 0:
        print(f"Failed: {result.total_records_failed} records")
        for error in result.errors:
            print(f"  - {error.error_message}")
"""
