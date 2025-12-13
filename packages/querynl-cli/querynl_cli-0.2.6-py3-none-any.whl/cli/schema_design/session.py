"""
Schema Design Session Management

Manages schema design sessions with SQLite persistence, including session creation,
retrieval, saving, and expiration cleanup.
"""

import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

from ..models import SchemaDesignSession
from . import SessionNotFoundError


# SQLite Schema DDL (T005)
CREATE_SESSIONS_TABLE = """
CREATE TABLE IF NOT EXISTS schema_design_sessions (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'finalized', 'implemented')),

    -- JSON serialized fields
    conversation_history TEXT NOT NULL DEFAULT '[]',
    current_schema TEXT,
    schema_versions TEXT NOT NULL DEFAULT '[]',
    uploaded_files TEXT NOT NULL DEFAULT '[]',

    -- Database target
    database_type TEXT CHECK(database_type IN ('postgresql', 'mysql', 'sqlite', 'mongodb')),
    target_database_name TEXT,

    -- Retention
    expires_at TEXT NOT NULL
)
"""

CREATE_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_sessions_updated ON schema_design_sessions(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_sessions_name ON schema_design_sessions(name) WHERE name IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_sessions_status ON schema_design_sessions(status);
CREATE INDEX IF NOT EXISTS idx_sessions_expires ON schema_design_sessions(expires_at);
"""

CREATE_UPDATE_TRIGGER = """
CREATE TRIGGER IF NOT EXISTS update_session_timestamp
AFTER UPDATE ON schema_design_sessions
FOR EACH ROW
BEGIN
    UPDATE schema_design_sessions
    SET updated_at = datetime('now')
    WHERE id = NEW.id;
END;
"""


class SchemaSessionManager:
    """
    Manages schema design sessions with SQLite persistence.

    Handles session creation, retrieval, updates, and cleanup operations.
    """

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize session manager.

        Args:
            db_path: Path to SQLite database file. Defaults to ~/.querynl/schema_sessions.db
        """
        if db_path is None:
            home = Path.home()
            querynl_dir = home / '.querynl'
            querynl_dir.mkdir(exist_ok=True)
            db_path = str(querynl_dir / 'schema_sessions.db')

        self.db_path = db_path
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        """Create database schema if it doesn't exist (T006 - Database Migration)."""
        with self._get_connection() as conn:
            conn.execute(CREATE_SESSIONS_TABLE)
            # Create indexes separately
            for index_sql in CREATE_INDEXES.strip().split(';'):
                if index_sql.strip():
                    conn.execute(index_sql)
            conn.execute(CREATE_UPDATE_TRIGGER)
            conn.commit()

    @contextmanager
    def _get_connection(self):
        """Get database connection context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def create_session(self, database_type: Optional[str] = None) -> SchemaDesignSession:
        """
        Create a new schema design session.

        Args:
            database_type: Target database type (optional)

        Returns:
            New SchemaDesignSession instance
        """
        session = SchemaDesignSession(database_type=database_type)
        self.save_session(session)
        return session

    def save_session(self, session: SchemaDesignSession) -> None:
        """
        Save or update a session in the database.

        Args:
            session: Session to save
        """
        session.updated_at = datetime.now()
        session_dict = session.to_dict()

        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO schema_design_sessions (
                    id, name, created_at, updated_at, status,
                    conversation_history, current_schema, schema_versions,
                    uploaded_files, database_type, target_database_name, expires_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_dict['id'],
                session_dict.get('name'),
                session_dict['created_at'],
                session_dict['updated_at'],
                session_dict['status'],
                json.dumps(session_dict['conversation_history']),
                json.dumps(session_dict['current_schema']) if session_dict.get('current_schema') else None,
                json.dumps(session_dict['schema_versions']),
                json.dumps(session_dict['uploaded_files']),
                session_dict.get('database_type'),
                session_dict.get('target_database_name'),
                session_dict['expires_at']
            ))
            conn.commit()

    def load_session(self, session_id: Optional[str] = None, name: Optional[str] = None) -> SchemaDesignSession:
        """
        Load a session by ID or name.

        Args:
            session_id: Session ID to load
            name: Session name to load (alternative to session_id)

        Returns:
            Loaded SchemaDesignSession

        Raises:
            SessionNotFoundError: If session not found
        """
        with self._get_connection() as conn:
            if session_id:
                row = conn.execute(
                    "SELECT * FROM schema_design_sessions WHERE id = ?",
                    (session_id,)
                ).fetchone()
            elif name:
                row = conn.execute(
                    "SELECT * FROM schema_design_sessions WHERE name = ?",
                    (name,)
                ).fetchone()
            else:
                raise ValueError("Must provide either session_id or name")

            if not row:
                raise SessionNotFoundError(f"Session not found: {session_id or name}")

            return self._row_to_session(row)

    def get_active_session(self) -> Optional[SchemaDesignSession]:
        """
        Get the most recently updated session (any status).

        Returns the most recent session regardless of status, allowing users
        to continue working with active, finalized, or implemented sessions.

        Returns:
            Most recent session, or None if no sessions exist
        """
        with self._get_connection() as conn:
            row = conn.execute("""
                SELECT * FROM schema_design_sessions
                ORDER BY updated_at DESC
                LIMIT 1
            """).fetchone()

            if row:
                return self._row_to_session(row)
            return None

    def list_sessions(self, status: Optional[str] = None, limit: int = 50) -> List[SchemaDesignSession]:
        """
        List sessions, optionally filtered by status.

        Args:
            status: Filter by status (active, finalized, implemented)
            limit: Maximum number of sessions to return

        Returns:
            List of sessions ordered by most recent first
        """
        with self._get_connection() as conn:
            if status:
                rows = conn.execute("""
                    SELECT * FROM schema_design_sessions
                    WHERE status = ?
                    ORDER BY updated_at DESC
                    LIMIT ?
                """, (status, limit)).fetchall()
            else:
                rows = conn.execute("""
                    SELECT * FROM schema_design_sessions
                    ORDER BY updated_at DESC
                    LIMIT ?
                """, (limit,)).fetchall()

            return [self._row_to_session(row) for row in rows]

    def delete_session(self, session_id: str) -> None:
        """
        Delete a session from the database.

        Args:
            session_id: ID of session to delete
        """
        with self._get_connection() as conn:
            conn.execute("DELETE FROM schema_design_sessions WHERE id = ?", (session_id,))
            conn.commit()

    def cleanup_expired(self) -> int:
        """
        Remove expired sessions (older than 90 days).

        Returns:
            Number of sessions deleted
        """
        with self._get_connection() as conn:
            cursor = conn.execute("""
                DELETE FROM schema_design_sessions
                WHERE expires_at < datetime('now')
            """)
            conn.commit()
            return cursor.rowcount

    def _row_to_session(self, row: sqlite3.Row) -> SchemaDesignSession:
        """
        Convert SQLite row to SchemaDesignSession (T010 - JSON Deserialization).

        Args:
            row: SQLite row from query

        Returns:
            SchemaDesignSession instance
        """
        data = {
            'id': row['id'],
            'name': row['name'],
            'created_at': row['created_at'],
            'updated_at': row['updated_at'],
            'status': row['status'],
            'conversation_history': json.loads(row['conversation_history']),
            'current_schema': json.loads(row['current_schema']) if row['current_schema'] else None,
            'schema_versions': json.loads(row['schema_versions']),
            'uploaded_files': json.loads(row['uploaded_files']),
            'database_type': row['database_type'],
            'target_database_name': row['target_database_name'],
            'expires_at': row['expires_at']
        }

        return SchemaDesignSession.from_dict(data)
