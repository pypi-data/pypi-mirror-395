"""
Migration tracking for QueryNL CLI

Manages migration records in SQLite database.
"""

import sqlite3
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from .config import get_config_dir
from .models import MigrationRecord


def get_migrations_db_path() -> Path:
    """Get path to migrations tracking database"""
    config_dir = get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "migrations.db"


def init_migrations_db() -> None:
    """Initialize migrations tracking database"""
    db_path = get_migrations_db_path()
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS migrations (
            migration_id TEXT PRIMARY KEY,
            connection_name TEXT NOT NULL,
            framework TEXT NOT NULL DEFAULT 'raw',
            direction TEXT NOT NULL DEFAULT 'up',
            sql_content TEXT NOT NULL,
            rollback_sql TEXT,
            description TEXT DEFAULT '',
            applied_at DATETIME,
            status TEXT NOT NULL DEFAULT 'pending',
            error_message TEXT,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_connection ON migrations(connection_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON migrations(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_applied_at ON migrations(applied_at)")

    conn.commit()
    conn.close()


def save_migration_record(migration: MigrationRecord) -> None:
    """Save migration record to database"""
    init_migrations_db()
    db_path = get_migrations_db_path()
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO migrations
        (migration_id, connection_name, framework, direction, sql_content, rollback_sql,
         description, applied_at, status, error_message)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        migration.migration_id,
        migration.connection_name,
        migration.framework,
        migration.direction,
        migration.sql_content,
        migration.rollback_sql,
        migration.description,
        migration.applied_at.isoformat() if migration.applied_at else None,
        migration.status,
        migration.error_message
    ))

    conn.commit()
    conn.close()


def get_migration_by_id(migration_id: str) -> Optional[MigrationRecord]:
    """Get migration record by ID"""
    init_migrations_db()
    db_path = get_migrations_db_path()
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM migrations WHERE migration_id = ?
    """, (migration_id,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return MigrationRecord.from_dict(dict(row))
    return None


def get_migrations(
    connection_name: Optional[str] = None,
    status: Optional[str] = None,
    limit: Optional[int] = None
) -> List[MigrationRecord]:
    """Get migration records with optional filters"""
    init_migrations_db()
    db_path = get_migrations_db_path()
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM migrations WHERE 1=1"
    params = []

    if connection_name:
        query += " AND connection_name = ?"
        params.append(connection_name)

    if status:
        query += " AND status = ?"
        params.append(status)

    query += " ORDER BY migration_id DESC"

    if limit:
        query += " LIMIT ?"
        params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [MigrationRecord.from_dict(dict(row)) for row in rows]


def update_migration_status(
    migration_id: str,
    status: str,
    applied_at: Optional[datetime] = None,
    error_message: Optional[str] = None
) -> None:
    """Update migration status"""
    init_migrations_db()
    db_path = get_migrations_db_path()
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE migrations
        SET status = ?, applied_at = ?, error_message = ?
        WHERE migration_id = ?
    """, (
        status,
        applied_at.isoformat() if applied_at else None,
        error_message,
        migration_id
    ))

    conn.commit()
    conn.close()


def delete_migration(migration_id: str) -> None:
    """Delete migration record"""
    init_migrations_db()
    db_path = get_migrations_db_path()
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute("DELETE FROM migrations WHERE migration_id = ?", (migration_id,))

    conn.commit()
    conn.close()
