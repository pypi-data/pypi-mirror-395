"""
Database driver integration for QueryNL CLI

Wraps existing database drivers from src/lib/ for CLI use.
"""

from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """
    Database connection wrapper.

    Provides unified interface for all supported database types.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize database connection.

        Args:
            config: Connection configuration dictionary
        """
        self.config = config
        self.database_type = config.get("database_type")
        self._connection = None

    def connect(self) -> None:
        """
        Establish database connection.

        Raises:
            Exception: If connection fails
        """
        logger.info(f"Connecting to {self.database_type} database")

        try:
            if self.database_type == "postgresql":
                import psycopg2
                self._connection = psycopg2.connect(
                    host=self.config.get("host"),
                    port=self.config.get("port", 5432),
                    database=self.config.get("database_name"),
                    user=self.config.get("username"),
                    password=self.config.get("password"),
                    sslmode="require" if self.config.get("ssl_enabled", True) else "disable",
                )

            elif self.database_type == "mysql":
                import pymysql
                self._connection = pymysql.connect(
                    host=self.config.get("host"),
                    port=self.config.get("port", 3306),
                    database=self.config.get("database_name"),
                    user=self.config.get("username"),
                    password=self.config.get("password"),
                    ssl={"ssl": True} if self.config.get("ssl_enabled", True) else None,
                )

            elif self.database_type == "sqlite":
                import sqlite3
                self._connection = sqlite3.connect(self.config.get("database_name"))
                # Enable row factory for dict-like access
                self._connection.row_factory = sqlite3.Row

            elif self.database_type == "mongodb":
                from pymongo import MongoClient
                connection_string = f"mongodb://{self.config.get('username')}:{self.config.get('password')}@{self.config.get('host')}:{self.config.get('port', 27017)}"
                self._connection = MongoClient(connection_string)

            else:
                raise ValueError(f"Unsupported database type: {self.database_type}")

            logger.info("Database connection established")

        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def test_connection(self) -> Dict[str, Any]:
        """
        Test database connection and return server info.

        Returns:
            Dictionary with connection details (version, latency, etc.)

        Raises:
            Exception: If connection test fails
        """
        import time

        start_time = time.time()

        try:
            self.connect()

            result = {
                "status": "success",
                "database_type": self.database_type,
                "latency_ms": int((time.time() - start_time) * 1000),
            }

            # Get database version
            if self.database_type == "postgresql":
                cursor = self._connection.cursor()
                cursor.execute("SELECT version()")
                version = cursor.fetchone()[0]
                result["version"] = version.split(",")[0]
                cursor.close()

            elif self.database_type == "mysql":
                cursor = self._connection.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()[0]
                result["version"] = f"MySQL {version}"
                cursor.close()

            elif self.database_type == "sqlite":
                cursor = self._connection.cursor()
                cursor.execute("SELECT sqlite_version()")
                version = cursor.fetchone()[0]
                result["version"] = f"SQLite {version}"
                cursor.close()

            elif self.database_type == "mongodb":
                server_info = self._connection.server_info()
                result["version"] = f"MongoDB {server_info.get('version')}"

            self.close()
            return result

        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "database_type": self.database_type,
            }

    def execute_query(self, sql: str) -> Dict[str, Any]:
        """
        Execute SQL query and return results.

        Args:
            sql: SQL query to execute

        Returns:
            Dictionary with rows, row_count, and execution metadata

        Raises:
            Exception: If query execution fails
        """
        import time

        if not self._connection:
            self.connect()

        start_time = time.time()
        cursor = self._connection.cursor()

        try:
            cursor.execute(sql)

            # Handle different query types
            if sql.strip().upper().startswith(("SELECT", "SHOW", "DESCRIBE", "EXPLAIN")):
                # Query returns rows
                if self.database_type == "sqlite":
                    rows = [dict(row) for row in cursor.fetchall()]
                else:
                    columns = [desc[0] for desc in cursor.description] if cursor.description else []
                    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

                return {
                    "rows": rows,
                    "row_count": len(rows),
                    "execution_time_ms": int((time.time() - start_time) * 1000),
                }
            else:
                # DML query (INSERT, UPDATE, DELETE)
                self._connection.commit()
                row_count = cursor.rowcount

                return {
                    "rows": [],
                    "row_count": row_count,
                    "execution_time_ms": int((time.time() - start_time) * 1000),
                    "affected_rows": row_count,
                }

        except Exception:
            self._connection.rollback()
            raise

        finally:
            cursor.close()

    def close(self) -> None:
        """Close database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
            logger.info("Database connection closed")

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
