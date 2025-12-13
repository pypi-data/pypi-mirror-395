"""Insertion execution interfaces and implementations for test data generation.

This module provides the IInsertionExecutor interface and implementations for executing
batch INSERT operations with transaction management, error recovery, and progress tracking.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime

from ..models import (
    TableInsertionResult,
    InsertionResult,
    ProgressUpdate,
    CancellationToken,
    DataGenerationPlan
)


class IInsertionExecutor(ABC):
    """Interface for executing batch INSERT operations.

    Implementations handle database-specific INSERT statement generation,
    transaction management, and error recovery with savepoints.
    """

    @abstractmethod
    def execute_insertion_plan(
        self,
        plan: DataGenerationPlan,
        connection: Any,
        data_rows: Dict[str, List[Dict[str, Any]]],
        progress_callback: Optional[Callable[[ProgressUpdate], None]] = None,
        cancellation_token: Optional[CancellationToken] = None
    ) -> InsertionResult:
        """Execute a complete test data insertion plan.

        Args:
            plan: The data generation plan to execute
            connection: Database connection object (DB-API 2.0 compatible)
            data_rows: Dictionary mapping table names to lists of row dictionaries
            progress_callback: Optional callback for progress updates
            cancellation_token: Optional token for checking cancellation requests

        Returns:
            InsertionResult with complete execution statistics and errors

        Raises:
            ConnectionError: If database connection fails
            ValueError: If plan or data_rows are invalid
        """
        pass

    @abstractmethod
    def build_insert_statement(
        self,
        table_name: str,
        row_data: Dict[str, Any],
        database_type: str
    ) -> str:
        """Build a database-specific INSERT statement with literal values.

        Args:
            table_name: Name of the target table
            row_data: Dictionary of column names to values
            database_type: Database type ('mysql', 'postgresql', 'sqlite')

        Returns:
            Complete INSERT statement with properly escaped literal values
            (NOT parameterized - actual values embedded in SQL)

        Raises:
            ValueError: If database_type is unsupported or row_data is invalid
        """
        pass

    @abstractmethod
    def execute_batch(
        self,
        table_name: str,
        rows: List[Dict[str, Any]],
        connection: Any,
        database_type: str,
        batch_size: int = 100,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        cancellation_token: Optional[CancellationToken] = None
    ) -> TableInsertionResult:
        """Execute a batch of INSERT statements for a single table.

        Args:
            table_name: Name of the table to insert into
            rows: List of row dictionaries to insert
            connection: Database connection object
            database_type: Database type for SQL generation
            batch_size: Number of rows to insert per transaction (default 100)
            progress_callback: Optional callback receiving (completed, total)
            cancellation_token: Optional token for checking cancellation

        Returns:
            TableInsertionResult with statistics for this table

        Raises:
            ConnectionError: If database connection fails during execution
        """
        pass

    @abstractmethod
    def escape_value(
        self,
        value: Any,
        database_type: str
    ) -> str:
        """Escape a value for safe inclusion in SQL statement.

        Args:
            value: The value to escape (can be str, int, float, datetime, None, etc.)
            database_type: Target database type for proper escaping rules

        Returns:
            String representation of the value with proper SQL escaping
            (e.g., 'John''s' for string "John's", NULL for None)

        Raises:
            ValueError: If value type is unsupported
        """
        pass

    @abstractmethod
    def create_savepoint(
        self,
        connection: Any,
        savepoint_name: str
    ) -> None:
        """Create a savepoint for error recovery.

        Args:
            connection: Database connection object
            savepoint_name: Name for the savepoint

        Raises:
            ConnectionError: If savepoint creation fails
        """
        pass

    @abstractmethod
    def rollback_to_savepoint(
        self,
        connection: Any,
        savepoint_name: str
    ) -> None:
        """Rollback to a previously created savepoint.

        Args:
            connection: Database connection object
            savepoint_name: Name of the savepoint to rollback to

        Raises:
            ConnectionError: If rollback fails
        """
        pass

    @abstractmethod
    def get_batch_size_recommendation(
        self,
        database_type: str,
        table_row_count: int
    ) -> int:
        """Get recommended batch size for a table.

        Args:
            database_type: Target database type
            table_row_count: Total number of rows to insert

        Returns:
            Recommended batch size (number of rows per transaction)
        """
        pass


class BaseInsertionExecutor(IInsertionExecutor):
    """Base implementation for database-specific insertion executors."""

    def __init__(self):
        """Initialize base insertion executor."""
        self._batch_sizes = {
            'mysql': 1000,
            'postgresql': 1000,
            'sqlite': 10000,
        }

    def escape_value(self, value: Any, database_type: str) -> str:
        """Escape a value for SQL with database-specific rules.

        Implements IInsertionExecutor.escape_value.
        """
        if value is None:
            return 'NULL'

        # Handle boolean values
        if isinstance(value, bool):
            if database_type == 'postgresql':
                return 'TRUE' if value else 'FALSE'
            else:  # MySQL, SQLite
                return '1' if value else '0'

        # Handle numeric values
        if isinstance(value, (int, float)):
            return str(value)

        # Handle datetime values
        if isinstance(value, datetime):
            return f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'"

        # Handle date values
        if hasattr(value, 'strftime') and not isinstance(value, datetime):
            return f"'{value.strftime('%Y-%m-%d')}'"

        # Handle strings
        if isinstance(value, str):
            if database_type == 'mysql':
                # MySQL uses backslash escaping
                escaped = value.replace('\\', '\\\\').replace("'", "\\'")
            else:  # PostgreSQL, SQLite
                # Double single quotes for escaping
                escaped = value.replace("'", "''")
            return f"'{escaped}'"

        # Fallback: convert to string and escape
        return self.escape_value(str(value), database_type)

    def build_insert_statement(
        self,
        table_name: str,
        row_data: Dict[str, Any],
        database_type: str
    ) -> str:
        """Build INSERT statement with literal values (NOT parameterized).

        Implements IInsertionExecutor.build_insert_statement.
        """
        if not row_data:
            raise ValueError(f"Cannot build INSERT for table '{table_name}': row_data is empty")

        columns = list(row_data.keys())
        values = [self.escape_value(row_data[col], database_type) for col in columns]

        # Build column list
        column_list = ', '.join(columns)

        # Build values list
        values_list = ', '.join(values)

        # Construct INSERT statement
        insert_sql = f"INSERT INTO {table_name} ({column_list}) VALUES ({values_list})"

        return insert_sql

    def execute_batch(
        self,
        table_name: str,
        rows: List[Dict[str, Any]],
        connection: Any,
        database_type: str,
        batch_size: int = 100,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        cancellation_token: Optional[CancellationToken] = None
    ) -> TableInsertionResult:
        """Execute batch INSERT operations for a single table.

        Implements IInsertionExecutor.execute_batch.
        """
        from ..models import TableInsertionResult, InsertionError, ErrorType
        import time

        start_time = time.time()
        total_inserted = 0
        total_failed = 0
        errors = []

        cursor = connection.cursor()

        try:
            # Process rows in batches
            for i in range(0, len(rows), batch_size):
                # Check for cancellation
                if cancellation_token and cancellation_token.is_cancelled():
                    break

                batch = rows[i:i + batch_size]
                batch_id = f"batch_{i // batch_size}"

                # Create savepoint for error recovery
                savepoint_name = f"sp_{batch_id}"
                try:
                    self.create_savepoint(connection, savepoint_name)

                    # Execute each INSERT in the batch
                    for idx, row in enumerate(batch):
                        try:
                            insert_sql = self.build_insert_statement(table_name, row, database_type)
                            cursor.execute(insert_sql)
                            total_inserted += 1

                            # Report progress
                            if progress_callback:
                                progress_callback(total_inserted, len(rows))

                        except Exception as e:
                            # Record error
                            error = InsertionError(
                                table_name=table_name,
                                batch_id=batch_id,
                                record_index=idx,
                                error_type=self._classify_error(e),
                                error_message=str(e),
                                failed_record=row
                            )
                            errors.append(error)
                            total_failed += 1

                    # Commit this batch
                    connection.commit()

                except Exception as batch_error:
                    # Rollback to savepoint if batch fails
                    try:
                        self.rollback_to_savepoint(connection, savepoint_name)
                    except:
                        pass

                    # Record batch-level error
                    error = InsertionError(
                        table_name=table_name,
                        batch_id=batch_id,
                        error_type=ErrorType.UNKNOWN,
                        error_message=f"Batch failed: {str(batch_error)}",
                        failed_record=None
                    )
                    errors.append(error)
                    total_failed += len(batch)

        finally:
            cursor.close()

        duration = time.time() - start_time

        return TableInsertionResult(
            table_name=table_name,
            records_inserted=total_inserted,
            records_failed=total_failed,
            insertion_duration_seconds=duration
        )

    def execute_insertion_plan(
        self,
        plan: DataGenerationPlan,
        connection: Any,
        data_rows: Dict[str, List[Dict[str, Any]]],
        progress_callback: Optional[Callable[[ProgressUpdate], None]] = None,
        cancellation_token: Optional[CancellationToken] = None
    ) -> InsertionResult:
        """Execute complete test data insertion plan.

        Implements IInsertionExecutor.execute_insertion_plan.
        """
        from ..models import InsertionResult
        import time
        import uuid

        start_time = time.time()
        request_id = str(uuid.uuid4())

        table_results = {}
        all_errors = []
        total_inserted = 0
        total_failed = 0

        # Process tables in insertion order
        for table_idx, table_name in enumerate(plan.insertion_order):
            if cancellation_token and cancellation_token.is_cancelled():
                break

            if table_name not in data_rows:
                continue

            rows = data_rows[table_name]
            batch_size = self.get_batch_size_recommendation(plan.database_type, len(rows))

            # Execute batch for this table
            def table_progress(completed, total):
                if progress_callback:
                    from ..models import ProgressUpdate
                    progress = ProgressUpdate(
                        current_table=table_name,
                        table_number=table_idx + 1,
                        total_tables=len(plan.insertion_order),
                        records_completed=total_inserted + completed,
                        records_total=plan.estimated_total_records,
                        estimated_seconds_remaining=0.0,  # TODO: calculate
                        current_speed_records_per_sec=0.0  # TODO: calculate
                    )
                    progress_callback(progress)

            result = self.execute_batch(
                table_name=table_name,
                rows=rows,
                connection=connection,
                database_type=plan.database_type,
                batch_size=batch_size,
                progress_callback=table_progress,
                cancellation_token=cancellation_token
            )

            table_results[table_name] = result
            total_inserted += result.records_inserted
            total_failed += result.records_failed

        end_time = time.time()

        return InsertionResult(
            request_id=request_id,
            started_at=datetime.fromtimestamp(start_time),
            completed_at=datetime.fromtimestamp(end_time),
            duration_seconds=end_time - start_time,
            total_records_requested=plan.estimated_total_records,
            total_records_inserted=total_inserted,
            total_records_failed=total_failed,
            table_results=table_results,
            errors=all_errors,
            cancelled_by_user=cancellation_token.is_cancelled() if cancellation_token else False
        )

    def create_savepoint(self, connection: Any, savepoint_name: str) -> None:
        """Create a savepoint for error recovery.

        Implements IInsertionExecutor.create_savepoint.
        """
        cursor = connection.cursor()
        try:
            cursor.execute(f"SAVEPOINT {savepoint_name}")
        finally:
            cursor.close()

    def rollback_to_savepoint(self, connection: Any, savepoint_name: str) -> None:
        """Rollback to a previously created savepoint.

        Implements IInsertionExecutor.rollback_to_savepoint.
        """
        cursor = connection.cursor()
        try:
            cursor.execute(f"ROLLBACK TO SAVEPOINT {savepoint_name}")
        finally:
            cursor.close()

    def get_batch_size_recommendation(
        self,
        database_type: str,
        table_row_count: int
    ) -> int:
        """Get recommended batch size for a table.

        Implements IInsertionExecutor.get_batch_size_recommendation.
        """
        return self._batch_sizes.get(database_type, 1000)

    def _classify_error(self, exception: Exception) -> 'ErrorType':
        """Classify database error into ErrorType enum."""
        from ..models import ErrorType

        error_msg = str(exception).lower()

        if 'unique' in error_msg or 'duplicate' in error_msg:
            return ErrorType.CONSTRAINT_VIOLATION
        elif 'foreign key' in error_msg or 'fk' in error_msg:
            return ErrorType.FOREIGN_KEY_VIOLATION
        elif 'syntax' in error_msg:
            return ErrorType.SYNTAX_ERROR
        elif 'timeout' in error_msg:
            return ErrorType.TIMEOUT
        elif 'connection' in error_msg:
            return ErrorType.CONNECTION_ERROR
        else:
            return ErrorType.UNKNOWN


class MySQLInsertionExecutor(BaseInsertionExecutor):
    """MySQL-specific insertion executor."""

    def __init__(self):
        """Initialize MySQL insertion executor."""
        super().__init__()


class PostgreSQLInsertionExecutor(BaseInsertionExecutor):
    """PostgreSQL-specific insertion executor."""

    def __init__(self):
        """Initialize PostgreSQL insertion executor."""
        super().__init__()


class SQLiteInsertionExecutor(BaseInsertionExecutor):
    """SQLite-specific insertion executor."""

    def __init__(self):
        """Initialize SQLite insertion executor."""
        super().__init__()
        # SQLite can handle larger batches
        self._batch_sizes['sqlite'] = 10000
