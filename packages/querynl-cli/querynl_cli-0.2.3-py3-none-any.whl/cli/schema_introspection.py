"""
Schema introspection utilities for QueryNL CLI

Fetches and caches database schema information for intelligent query generation.
"""

import logging
from typing import Dict, List, Any, Optional
from .database import DatabaseConnection
from .models import ConnectionProfile

logger = logging.getLogger(__name__)


class SchemaIntrospector:
    """
    Introspects database schema and provides structured schema information.
    """

    def __init__(self, connection_profile: ConnectionProfile, password: Optional[str] = None):
        """
        Initialize schema introspector.

        Args:
            connection_profile: Database connection profile
            password: Database password
        """
        self.profile = connection_profile
        self.password = password
        self._schema_cache: Optional[Dict[str, Any]] = None

    def get_schema(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Get database schema with table and column information.

        Args:
            force_refresh: Force refresh of cached schema

        Returns:
            Dictionary with schema structure:
            {
                "tables": {
                    "table_name": {
                        "columns": ["col1", "col2", ...],
                        "column_details": [
                            {"name": "col1", "type": "integer", "nullable": False},
                            ...
                        ]
                    }
                }
            }
        """
        if self._schema_cache and not force_refresh:
            return self._schema_cache

        logger.info("Introspecting database schema...")

        try:
            conn_config = self.profile.get_connection_config(self.password)
            db = DatabaseConnection(conn_config)
            db.connect()

            schema = {"tables": {}}

            if self.profile.database_type == "postgresql":
                schema = self._introspect_postgresql(db)
            elif self.profile.database_type == "mysql":
                schema = self._introspect_mysql(db)
            elif self.profile.database_type == "sqlite":
                schema = self._introspect_sqlite(db)
            elif self.profile.database_type == "mongodb":
                schema = self._introspect_mongodb(db)

            db.close()

            self._schema_cache = schema
            logger.info(f"Schema introspection complete: {len(schema.get('tables', {}))} tables found")

            return schema

        except Exception as e:
            logger.error(f"Schema introspection failed: {e}")
            return {"tables": {}}

    def _introspect_postgresql(self, db: DatabaseConnection) -> Dict[str, Any]:
        """Introspect PostgreSQL schema."""
        # Get all tables
        tables_result = db.execute_query("""
            SELECT tablename
            FROM pg_catalog.pg_tables
            WHERE schemaname = 'public'
            ORDER BY tablename;
        """)

        schema = {"tables": {}}

        for row in tables_result.get("rows", []):
            table_name = row["tablename"]

            # Get columns for this table
            columns_result = db.execute_query(f"""
                SELECT
                    column_name,
                    data_type,
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = '{table_name}'
                ORDER BY ordinal_position;
            """)

            columns = []
            column_details = []

            for col_row in columns_result.get("rows", []):
                col_name = col_row["column_name"]
                columns.append(col_name)
                column_details.append({
                    "name": col_name,
                    "type": col_row["data_type"],
                    "nullable": col_row["is_nullable"] == "YES",
                    "default": col_row.get("column_default")
                })

            schema["tables"][table_name] = {
                "columns": columns,
                "column_details": column_details
            }

        return schema

    def _introspect_mysql(self, db: DatabaseConnection) -> Dict[str, Any]:
        """Introspect MySQL schema."""
        # Get all tables
        tables_result = db.execute_query("SHOW TABLES;")

        schema = {"tables": {}}

        # MySQL returns tables with dynamic key name
        for row in tables_result.get("rows", []):
            table_name = list(row.values())[0]

            # Get columns for this table
            columns_result = db.execute_query(f"DESCRIBE {table_name};")

            columns = []
            column_details = []

            for col_row in columns_result.get("rows", []):
                col_name = col_row["Field"]
                columns.append(col_name)
                column_details.append({
                    "name": col_name,
                    "type": col_row["Type"],
                    "nullable": col_row["Null"] == "YES",
                    "default": col_row.get("Default")
                })

            schema["tables"][table_name] = {
                "columns": columns,
                "column_details": column_details
            }

        return schema

    def _introspect_sqlite(self, db: DatabaseConnection) -> Dict[str, Any]:
        """Introspect SQLite schema."""
        # Get all tables
        tables_result = db.execute_query("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name;
        """)

        schema = {"tables": {}}

        for row in tables_result.get("rows", []):
            table_name = row["name"]

            # Get columns for this table
            columns_result = db.execute_query(f"PRAGMA table_info({table_name});")

            columns = []
            column_details = []

            for col_row in columns_result.get("rows", []):
                col_name = col_row["name"]
                columns.append(col_name)
                column_details.append({
                    "name": col_name,
                    "type": col_row["type"],
                    "nullable": col_row["notnull"] == 0,
                    "default": col_row.get("dflt_value")
                })

            schema["tables"][table_name] = {
                "columns": columns,
                "column_details": column_details
            }

        return schema

    def _introspect_mongodb(self, db: DatabaseConnection) -> Dict[str, Any]:
        """Introspect MongoDB schema (collection names only)."""
        # MongoDB is schemaless, so we just list collections
        try:
            collections_result = db.execute_query("db.getCollectionNames()")
            schema = {"tables": {}}

            for collection in collections_result.get("rows", []):
                schema["tables"][collection] = {
                    "columns": [],  # MongoDB has no fixed schema
                    "column_details": []
                }

            return schema
        except Exception:
            return {"tables": {}}

    def format_schema_for_llm(self) -> str:
        """
        Format schema in a compact, LLM-friendly format.

        Returns:
            String representation of schema for LLM prompt
        """
        schema = self.get_schema()
        tables = schema.get("tables", {})

        if not tables:
            return "No schema information available"

        lines = []
        for table_name, table_info in sorted(tables.items()):
            columns = table_info.get("columns", [])
            if columns:
                cols_str = ", ".join(columns)
                lines.append(f"  - {table_name}: {cols_str}")
            else:
                lines.append(f"  - {table_name}")

        return "\n".join(lines)

    def find_best_table_match(self, query_text: str) -> Optional[str]:
        """
        Find the best matching table name from the schema based on query text.

        Handles singular/plural variations and typos.

        Args:
            query_text: User's query text

        Returns:
            Best matching table name or None
        """
        schema = self.get_schema()
        tables = list(schema.get("tables", {}).keys())

        if not tables:
            return None

        query_lower = query_text.lower()

        # Direct match
        for table in tables:
            if table.lower() in query_lower or query_lower in table.lower():
                return table

        # Try singular/plural variations
        import re

        # Extract potential table names from query
        words = re.findall(r'\b\w+\b', query_lower)

        for word in words:
            # Skip common words
            if word in ['the', 'all', 'from', 'in', 'select', 'show', 'get', 'find']:
                continue

            # Check exact match
            if word in [t.lower() for t in tables]:
                return next(t for t in tables if t.lower() == word)

            # Check plural -> singular (threads -> thread)
            if word.endswith('s'):
                singular = word[:-1]
                if singular in [t.lower() for t in tables]:
                    return next(t for t in tables if t.lower() == singular)

            # Check singular -> plural (thread -> threads)
            plural = word + 's'
            if plural in [t.lower() for t in tables]:
                return next(t for t in tables if t.lower() == plural)

        return None
