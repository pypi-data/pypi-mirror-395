"""
Query history management for QueryNL CLI

Tracks executed queries in SQLite database for recall and analytics.
"""

import sqlite3
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

from .config import get_history_db_path


def init_history_db() -> None:
    """
    Initialize query history database with schema.

    Creates the query_history table if it doesn't exist.
    """
    db_path = get_history_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS query_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            connection_name TEXT NOT NULL,
            natural_language_input TEXT NOT NULL,
            generated_sql TEXT NOT NULL,
            executed BOOLEAN NOT NULL DEFAULT 0,
            execution_time_ms INTEGER,
            row_count INTEGER,
            error_message TEXT,
            timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_session_id ON query_history(session_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_timestamp ON query_history(timestamp)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_connection_name ON query_history(connection_name)
    """)

    conn.commit()
    conn.close()


def save_query_history(
    session_id: str,
    connection_name: str,
    natural_language_input: str,
    generated_sql: str,
    executed: bool = False,
    execution_time_ms: Optional[int] = None,
    row_count: Optional[int] = None,
    error_message: Optional[str] = None,
) -> int:
    """
    Save query to history database.

    Args:
        session_id: Unique session identifier
        connection_name: Name of connection used
        natural_language_input: User's natural language query
        generated_sql: LLM-generated SQL
        executed: Whether query was executed
        execution_time_ms: Query execution time in milliseconds
        row_count: Number of rows returned/affected
        error_message: Error message if query failed

    Returns:
        History entry ID
    """
    init_history_db()

    db_path = get_history_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO query_history (
            session_id, connection_name, natural_language_input, generated_sql,
            executed, execution_time_ms, row_count, error_message, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session_id,
        connection_name,
        natural_language_input,
        generated_sql,
        executed,
        execution_time_ms,
        row_count,
        error_message,
        datetime.now().isoformat(),
    ))

    history_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return history_id


def get_query_history(
    limit: int = 20,
    connection_name: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Retrieve query history.

    Args:
        limit: Maximum number of entries to return
        connection_name: Filter by connection name (optional)

    Returns:
        List of history entry dictionaries
    """
    init_history_db()

    db_path = get_history_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if connection_name:
        cursor.execute("""
            SELECT * FROM query_history
            WHERE connection_name = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (connection_name, limit))
    else:
        cursor.execute("""
            SELECT * FROM query_history
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def clear_history(connection_name: Optional[str] = None) -> int:
    """
    Clear query history.

    Args:
        connection_name: Clear only for specific connection (optional)

    Returns:
        Number of deleted entries
    """
    init_history_db()

    db_path = get_history_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if connection_name:
        cursor.execute("""
            DELETE FROM query_history
            WHERE connection_name = ?
        """, (connection_name,))
    else:
        cursor.execute("DELETE FROM query_history")

    deleted_count = cursor.rowcount
    conn.commit()
    conn.close()

    return deleted_count


def generate_session_id() -> str:
    """
    Generate a unique session ID for grouping queries.

    Returns:
        UUID v4 string
    """
    return str(uuid.uuid4())
