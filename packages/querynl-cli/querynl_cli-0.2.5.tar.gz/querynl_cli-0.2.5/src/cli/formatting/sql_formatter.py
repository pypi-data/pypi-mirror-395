"""
SQL INSERT statement formatter for QueryNL CLI

Generates database-specific SQL INSERT statements for data migration.
"""

from datetime import datetime
from typing import Dict, Any, List, TextIO, Optional


def save_sql_to_file(
    result: Dict[str, Any],
    file_path: str,
    table_name: str,
    database_type: str = "postgresql",
    batch_size: int = 1000
) -> None:
    """
    Save query results as SQL INSERT statements.

    Args:
        result: Query result dictionary
        file_path: Path to output file
        table_name: Target table name for INSERT statements
        database_type: Database type (postgresql, mysql, sqlite)
        batch_size: Number of rows per INSERT statement
    """
    rows = result.get("rows", [])

    if not rows:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"-- Empty result set\n-- Table: {table_name}\n")
        return

    with open(file_path, 'w', encoding='utf-8') as f:
        writer = SQLWriter(f, table_name, database_type, batch_size)
        columns = list(rows[0].keys())
        writer.begin(columns)

        for row in rows:
            writer.write_row(row)

        writer.end()


class SQLWriter:
    """
    SQL INSERT statement writer with database-specific escaping.

    Supports:
    - PostgreSQL: double-quote escaping, multi-row INSERTs
    - MySQL: backslash escaping, multi-row INSERTs
    - SQLite: double-quote escaping, multi-row INSERTs
    """

    def __init__(
        self,
        file_handle: TextIO,
        table_name: str,
        database_type: str,
        batch_size: int = 1000
    ):
        self.file = file_handle
        self.table_name = table_name
        self.database_type = database_type.lower()
        self.batch_size = batch_size
        self.batch_buffer: List[Dict[str, Any]] = []
        self.columns: Optional[List[str]] = None
        self.total_rows = 0

    def begin(self, columns: List[str]) -> None:
        """Write file header with metadata."""
        self.columns = columns

        # Write header comments
        self.file.write(f"-- Table: {self.table_name}\n")
        self.file.write(f"-- Database: {self.database_type}\n")
        self.file.write(f"-- Exported: {datetime.now().isoformat()}\n")
        self.file.write(f"-- Columns: {', '.join(columns)}\n")
        self.file.write("\n")

    def write_row(self, row: Dict[str, Any]) -> None:
        """Add row to batch buffer."""
        self.batch_buffer.append(row)
        self.total_rows += 1

        if len(self.batch_buffer) >= self.batch_size:
            self._flush_batch()

    def end(self) -> None:
        """Flush remaining rows and write footer."""
        if self.batch_buffer:
            self._flush_batch()

        self.file.write(f"\n-- Total rows: {self.total_rows}\n")

    def _flush_batch(self) -> None:
        """Write batch as INSERT statement."""
        if not self.batch_buffer or not self.columns:
            return

        # Generate INSERT statement
        column_list = ', '.join(f'"{col}"' for col in self.columns)

        # Build value groups
        value_groups = []
        for row in self.batch_buffer:
            values = [
                self._escape_value(row.get(col))
                for col in self.columns
            ]
            value_group = '(' + ', '.join(values) + ')'
            value_groups.append(value_group)

        # Write INSERT statement
        self.file.write(f"INSERT INTO {self.table_name} ({column_list}) VALUES\n")
        self.file.write(',\n'.join(value_groups))
        self.file.write(';\n\n')

        # Clear buffer
        self.batch_buffer = []

    def _escape_value(self, value: Any) -> str:
        """
        Escape value for SQL with database-specific rules.

        Args:
            value: Value to escape

        Returns:
            SQL-escaped string representation
        """
        if value is None:
            return 'NULL'

        if isinstance(value, bool):
            if self.database_type == 'postgresql':
                return 'TRUE' if value else 'FALSE'
            else:  # MySQL, SQLite
                return '1' if value else '0'

        if isinstance(value, (int, float)):
            return str(value)

        if isinstance(value, datetime):
            return f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'"

        # String escaping (database-specific)
        if self.database_type == 'mysql':
            return self._escape_string_mysql(str(value))
        else:  # PostgreSQL, SQLite
            return self._escape_string_postgres(str(value))

    @staticmethod
    def _escape_string_postgres(s: str) -> str:
        """
        Escape string for PostgreSQL/SQLite.

        Rules:
        - Single quotes → doubled ('')
        - Backslashes → doubled (\\)
        """
        escaped = s.replace("\\", "\\\\").replace("'", "''")
        return f"'{escaped}'"

    @staticmethod
    def _escape_string_mysql(s: str) -> str:
        """
        Escape string for MySQL.

        Rules:
        - Backslashes → doubled (\\)
        - Single quotes → backslash-escaped (\')
        """
        escaped = s.replace("\\", "\\\\").replace("'", "\\'")
        return f"'{escaped}'"
