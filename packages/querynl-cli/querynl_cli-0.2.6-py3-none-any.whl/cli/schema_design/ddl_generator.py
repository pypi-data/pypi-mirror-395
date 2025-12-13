"""
Database-Specific DDL Generation

Generates CREATE TABLE, INDEX, and CONSTRAINT statements for PostgreSQL, MySQL,
SQLite, and MongoDB schema validation rules.
"""

import json
from typing import List, Dict, Any
from ..models import SchemaProposal, SchemaTable, SchemaColumn, SchemaIndex, SchemaRelationship


class DDLGenerator:
    """
    Generates database-specific DDL statements from schema proposals.

    Supports PostgreSQL, MySQL, SQLite, and MongoDB (as JSON Schema validation).
    """

    @staticmethod
    def generate(schema: SchemaProposal, database_type: str = None) -> str:
        """
        Generate DDL for specified database type (T057).

        Args:
            schema: Schema proposal to convert to DDL
            database_type: Database type (defaults to schema.database_type)

        Returns:
            DDL statements as string

        Raises:
            ValueError: If database type is unsupported
        """
        db_type = database_type or schema.database_type

        if db_type == "postgresql":
            return DDLGenerator.generate_postgresql(schema)
        elif db_type == "mysql":
            return DDLGenerator.generate_mysql(schema)
        elif db_type == "sqlite":
            return DDLGenerator.generate_sqlite(schema)
        elif db_type == "mongodb":
            return DDLGenerator.generate_mongodb(schema)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    @staticmethod
    def generate_postgresql(schema: SchemaProposal) -> str:
        """
        Generate PostgreSQL DDL statements (T052).

        Args:
            schema: Schema proposal

        Returns:
            PostgreSQL CREATE TABLE, INDEX, and ALTER TABLE statements
        """
        ddl_parts = [
            "-- PostgreSQL DDL",
            f"-- Generated from schema version {schema.version}",
            f"-- Database: {schema.database_type}",
            f"-- Normalization: {schema.normalization_level}",
            ""
        ]

        # Create tables
        for table in schema.tables:
            ddl_parts.append(f"-- Table: {table.name}")
            if table.description:
                ddl_parts.append(f"-- {table.description}")

            columns_ddl = []
            for col in table.columns:
                col_ddl = DDLGenerator._column_to_postgresql(col)
                columns_ddl.append(f"    {col_ddl}")

            create_table = f"CREATE TABLE {table.name} (\n"
            create_table += ",\n".join(columns_ddl)
            create_table += "\n);"

            ddl_parts.append(create_table)
            ddl_parts.append("")

        # Create indexes
        for table in schema.tables:
            if table.indexes:
                ddl_parts.append(f"-- Indexes for {table.name}")
                for idx in table.indexes:
                    idx_ddl = DDLGenerator._index_to_postgresql(table.name, idx)
                    ddl_parts.append(idx_ddl)
                ddl_parts.append("")

        # Add foreign keys (T069: database-specific constraints)
        for rel in schema.relationships:
            ddl_parts.append(f"-- Relationship: {rel.from_table} -> {rel.to_table}")

            # Determine ON DELETE behavior based on column nullability and relationship type
            is_nullable = DDLGenerator._is_column_nullable(schema, rel.from_table, rel.foreign_key)
            if rel.type == "one-to-many":
                on_delete = "CASCADE"
            elif is_nullable:
                on_delete = "SET NULL"
            else:
                on_delete = "RESTRICT"  # Can't delete parent if child exists

            # Find the primary key column in the referenced table
            referenced_pk = DDLGenerator._get_primary_key_column(schema, rel.to_table)

            alter_table = f"ALTER TABLE {rel.from_table}\n"
            alter_table += f"    ADD CONSTRAINT fk_{rel.from_table}_{rel.foreign_key}\n"
            alter_table += f"    FOREIGN KEY ({rel.foreign_key})\n"
            alter_table += f"    REFERENCES {rel.to_table}({referenced_pk})\n"
            alter_table += f"    ON DELETE {on_delete};"

            ddl_parts.append(alter_table)
            ddl_parts.append("")

        # Add comments with rationale
        if schema.rationale:
            ddl_parts.append("-- Design Rationale:")
            for line in schema.rationale.split('\n'):
                ddl_parts.append(f"-- {line}")

        return "\n".join(ddl_parts)

    @staticmethod
    def generate_mysql(schema: SchemaProposal) -> str:
        """
        Generate MySQL DDL statements (T053).

        Args:
            schema: Schema proposal

        Returns:
            MySQL CREATE TABLE and INDEX statements
        """
        ddl_parts = [
            "-- MySQL DDL",
            f"-- Generated from schema version {schema.version}",
            f"-- Database: {schema.database_type}",
            f"-- Normalization: {schema.normalization_level}",
            ""
        ]

        # Create tables
        for table in schema.tables:
            ddl_parts.append(f"-- Table: {table.name}")
            if table.description:
                ddl_parts.append(f"-- {table.description}")

            columns_ddl = []
            for col in table.columns:
                col_ddl = DDLGenerator._column_to_mysql(col)
                columns_ddl.append(f"    {col_ddl}")

            # Add indexes inline
            if table.indexes:
                for idx in table.indexes:
                    idx_ddl = DDLGenerator._index_to_mysql_inline(idx)
                    columns_ddl.append(f"    {idx_ddl}")

            create_table = f"CREATE TABLE {table.name} (\n"
            create_table += ",\n".join(columns_ddl)
            create_table += "\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"

            ddl_parts.append(create_table)
            ddl_parts.append("")

        # Add foreign keys
        for rel in schema.relationships:
            ddl_parts.append(f"-- Relationship: {rel.from_table} -> {rel.to_table}")

            # Determine ON DELETE behavior based on column nullability and relationship type
            is_nullable = DDLGenerator._is_column_nullable(schema, rel.from_table, rel.foreign_key)
            if rel.type == "one-to-many":
                on_delete = "CASCADE"
            elif is_nullable:
                on_delete = "SET NULL"
            else:
                on_delete = "RESTRICT"  # Can't delete parent if child exists

            # Find the primary key column in the referenced table
            referenced_pk = DDLGenerator._get_primary_key_column(schema, rel.to_table)

            alter_table = f"ALTER TABLE {rel.from_table}\n"
            alter_table += f"    ADD CONSTRAINT fk_{rel.from_table}_{rel.foreign_key}\n"
            alter_table += f"    FOREIGN KEY ({rel.foreign_key})\n"
            alter_table += f"    REFERENCES {rel.to_table}({referenced_pk})\n"
            alter_table += f"    ON DELETE {on_delete};"

            ddl_parts.append(alter_table)
            ddl_parts.append("")

        # Add comments
        if schema.rationale:
            ddl_parts.append("-- Design Rationale:")
            for line in schema.rationale.split('\n'):
                ddl_parts.append(f"-- {line}")

        return "\n".join(ddl_parts)

    @staticmethod
    def generate_sqlite(schema: SchemaProposal) -> str:
        """
        Generate SQLite DDL statements (T054).

        Args:
            schema: Schema proposal

        Returns:
            SQLite CREATE TABLE and INDEX statements
        """
        ddl_parts = [
            "-- SQLite DDL",
            f"-- Generated from schema version {schema.version}",
            f"-- Database: {schema.database_type}",
            f"-- Normalization: {schema.normalization_level}",
            "",
            "-- Enable foreign keys",
            "PRAGMA foreign_keys = ON;",
            ""
        ]

        # Create tables
        for table in schema.tables:
            ddl_parts.append(f"-- Table: {table.name}")
            if table.description:
                ddl_parts.append(f"-- {table.description}")

            columns_ddl = []
            for col in table.columns:
                col_ddl = DDLGenerator._column_to_sqlite(col)
                columns_ddl.append(f"    {col_ddl}")

            # Add foreign keys inline (SQLite prefers inline foreign keys)
            for rel in schema.relationships:
                if rel.from_table == table.name:
                    referenced_pk = DDLGenerator._get_primary_key_column(schema, rel.to_table)
                    fk_ddl = f"    FOREIGN KEY ({rel.foreign_key}) REFERENCES {rel.to_table}({referenced_pk})"
                    columns_ddl.append(fk_ddl)

            create_table = f"CREATE TABLE {table.name} (\n"
            create_table += ",\n".join(columns_ddl)
            create_table += "\n);"

            ddl_parts.append(create_table)
            ddl_parts.append("")

        # Create indexes
        for table in schema.tables:
            if table.indexes:
                ddl_parts.append(f"-- Indexes for {table.name}")
                for idx in table.indexes:
                    idx_ddl = DDLGenerator._index_to_sqlite(table.name, idx)
                    ddl_parts.append(idx_ddl)
                ddl_parts.append("")

        # Add comments
        if schema.rationale:
            ddl_parts.append("-- Design Rationale:")
            for line in schema.rationale.split('\n'):
                ddl_parts.append(f"-- {line}")

        return "\n".join(ddl_parts)

    @staticmethod
    def generate_mongodb(schema: SchemaProposal) -> str:
        """
        Generate MongoDB schema validation rules (T055).

        Args:
            schema: Schema proposal

        Returns:
            MongoDB createCollection commands with JSON Schema validation
        """
        commands = []

        commands.append("// MongoDB Schema Validation")
        commands.append(f"// Generated from schema version {schema.version}")
        commands.append(f"// Database: {schema.database_type}")
        commands.append(f"// Normalization: {schema.normalization_level}")
        commands.append("")

        for table in schema.tables:
            commands.append(f"// Collection: {table.name}")
            if table.description:
                commands.append(f"// {table.description}")

            # Build JSON Schema validator
            validator = {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": [],
                    "properties": {}
                }
            }

            for col in table.columns:
                # Determine if required
                if "NOT NULL" in col.constraints or "PRIMARY KEY" in col.constraints:
                    validator["$jsonSchema"]["required"].append(col.name)

                # Map type
                bson_type = DDLGenerator._map_type_to_mongodb(col.data_type)
                field_schema = {"bsonType": bson_type}

                if col.description:
                    field_schema["description"] = col.description

                validator["$jsonSchema"]["properties"][col.name] = field_schema

            # Create collection command
            create_cmd = {
                "createCollection": table.name,
                "validator": validator
            }

            commands.append(f"db.createCollection({json.dumps(table.name)}, {json.dumps(create_cmd, indent=2)})")
            commands.append("")

            # Create indexes
            if table.indexes:
                commands.append(f"// Indexes for {table.name}")
                for idx in table.indexes:
                    index_spec = {col: 1 for col in idx.columns}
                    index_options = {"name": idx.name}
                    if idx.unique:
                        index_options["unique"] = True

                    commands.append(f"db.{table.name}.createIndex({json.dumps(index_spec)}, {json.dumps(index_options)})")
                commands.append("")

        # Add comments
        if schema.rationale:
            commands.append("// Design Rationale:")
            for line in schema.rationale.split('\n'):
                commands.append(f"// {line}")

        return "\n".join(commands)

    # Helper methods for type mapping and schema introspection

    @staticmethod
    def _get_primary_key_column(schema: SchemaProposal, table_name: str) -> str:
        """
        Get the primary key column name for a table.

        Args:
            schema: Schema proposal
            table_name: Name of the table

        Returns:
            Primary key column name (defaults to 'id' if not found)
        """
        for table in schema.tables:
            if table.name == table_name:
                for col in table.columns:
                    # Check if PRIMARY KEY is in the constraints list
                    if "PRIMARY KEY" in col.constraints or "PRIMARY" in col.constraints:
                        return col.name
        # Fallback to 'id' if no primary key found
        return "id"

    @staticmethod
    def _is_column_nullable(schema: SchemaProposal, table_name: str, column_name: str) -> bool:
        """
        Check if a column allows NULL values.

        Args:
            schema: Schema proposal
            table_name: Name of the table
            column_name: Name of the column

        Returns:
            True if column is nullable, False if NOT NULL
        """
        for table in schema.tables:
            if table.name == table_name:
                for col in table.columns:
                    if col.name == column_name:
                        # Check if NOT NULL is in constraints
                        return "NOT NULL" not in col.constraints
        # Default to nullable if column not found
        return True

    @staticmethod
    def _map_type_to_database(generic_type: str, database_type: str) -> str:
        """
        Map generic type to database-specific type (T056).

        Args:
            generic_type: Generic type (VARCHAR, INTEGER, etc.)
            database_type: Target database

        Returns:
            Database-specific type
        """
        # Extract base type and size
        base_type = generic_type.split('(')[0].upper()

        type_mapping = {
            "postgresql": {
                "INTEGER": "INTEGER",
                "BIGINT": "BIGINT",
                "SMALLINT": "SMALLINT",
                "DECIMAL": "NUMERIC",
                "FLOAT": "DOUBLE PRECISION",
                "TEXT": "TEXT",
                "VARCHAR": generic_type,  # Preserve size
                "BOOLEAN": "BOOLEAN",
                "DATE": "DATE",
                "TIMESTAMP": "TIMESTAMP",
                "JSON": "JSONB"
            },
            "mysql": {
                "INTEGER": "INT",
                "BIGINT": "BIGINT",
                "SMALLINT": "SMALLINT",
                "DECIMAL": "DECIMAL(10,2)",
                "FLOAT": "DOUBLE",
                "TEXT": "TEXT",
                "VARCHAR": generic_type,  # Preserve size
                "BOOLEAN": "TINYINT(1)",
                "DATE": "DATE",
                "TIMESTAMP": "TIMESTAMP",
                "JSON": "JSON"
            },
            "sqlite": {
                "INTEGER": "INTEGER",
                "BIGINT": "INTEGER",
                "SMALLINT": "INTEGER",
                "DECIMAL": "REAL",
                "FLOAT": "REAL",
                "TEXT": "TEXT",
                "VARCHAR": "TEXT",  # SQLite uses TEXT for varchar
                "BOOLEAN": "INTEGER",  # 0 or 1
                "DATE": "TEXT",  # ISO 8601
                "TIMESTAMP": "TEXT",  # ISO 8601
                "JSON": "TEXT"
            }
        }

        db_map = type_mapping.get(database_type, {})
        return db_map.get(base_type, generic_type)

    @staticmethod
    def _map_type_to_mongodb(generic_type: str) -> str:
        """Map generic type to MongoDB BSON type."""
        base_type = generic_type.split('(')[0].upper()

        mapping = {
            "INTEGER": "int",
            "BIGINT": "long",
            "SMALLINT": "int",
            "DECIMAL": "decimal",
            "FLOAT": "double",
            "TEXT": "string",
            "VARCHAR": "string",
            "BOOLEAN": "bool",
            "DATE": "date",
            "TIMESTAMP": "date",
            "JSON": "object"
        }

        return mapping.get(base_type, "string")

    @staticmethod
    def _column_to_postgresql(col: SchemaColumn) -> str:
        """Convert column to PostgreSQL DDL."""
        parts = [col.name]

        # Map type
        col_type = DDLGenerator._map_type_to_database(col.data_type, "postgresql")

        # Handle auto-increment for primary keys
        if "PRIMARY KEY" in col.constraints and col_type in ["INTEGER", "BIGINT"]:
            col_type = "SERIAL" if col_type == "INTEGER" else "BIGSERIAL"
            # Remove PRIMARY KEY from constraints as it will be added separately
            constraints = [c for c in col.constraints if c != "PRIMARY KEY"]
            constraints.append("PRIMARY KEY")
        else:
            constraints = col.constraints

        parts.append(col_type)

        # Add constraints
        if constraints:
            parts.extend(constraints)

        # Add default value
        if col.default_value is not None:
            if isinstance(col.default_value, str):
                parts.append(f"DEFAULT '{col.default_value}'")
            else:
                parts.append(f"DEFAULT {col.default_value}")

        return " ".join(parts)

    @staticmethod
    def _column_to_mysql(col: SchemaColumn) -> str:
        """Convert column to MySQL DDL."""
        parts = [col.name]

        # Map type
        col_type = DDLGenerator._map_type_to_database(col.data_type, "mysql")

        # Handle auto-increment for primary keys
        if "PRIMARY KEY" in col.constraints and col_type in ["INT", "BIGINT"]:
            parts.append(col_type)
            parts.append("AUTO_INCREMENT")
            parts.append("PRIMARY KEY")
        else:
            parts.append(col_type)
            if col.constraints:
                parts.extend(col.constraints)

        # Add default value
        if col.default_value is not None:
            if isinstance(col.default_value, str):
                parts.append(f"DEFAULT '{col.default_value}'")
            else:
                parts.append(f"DEFAULT {col.default_value}")

        return " ".join(parts)

    @staticmethod
    def _column_to_sqlite(col: SchemaColumn) -> str:
        """Convert column to SQLite DDL."""
        parts = [col.name]

        # Map type
        col_type = DDLGenerator._map_type_to_database(col.data_type, "sqlite")

        # Handle auto-increment for primary keys (SQLite uses INTEGER PRIMARY KEY)
        if "PRIMARY KEY" in col.constraints and col_type == "INTEGER":
            parts.append("INTEGER")
            parts.append("PRIMARY KEY")
            parts.append("AUTOINCREMENT")
        else:
            parts.append(col_type)
            if col.constraints:
                parts.extend(col.constraints)

        # Add default value
        if col.default_value is not None:
            if isinstance(col.default_value, str):
                parts.append(f"DEFAULT '{col.default_value}'")
            else:
                parts.append(f"DEFAULT {col.default_value}")

        return " ".join(parts)

    @staticmethod
    def _index_to_postgresql(table_name: str, idx: SchemaIndex) -> str:
        """Convert index to PostgreSQL DDL."""
        unique = "UNIQUE " if idx.unique else ""
        index_type = f"USING {idx.type.upper()}" if idx.type and idx.type != "btree" else ""
        columns = ", ".join(idx.columns)

        return f"CREATE {unique}INDEX {idx.name} ON {table_name} ({columns}) {index_type};".strip()

    @staticmethod
    def _index_to_mysql_inline(idx: SchemaIndex) -> str:
        """Convert index to MySQL inline DDL."""
        unique = "UNIQUE " if idx.unique else ""
        columns = ", ".join(idx.columns)

        return f"{unique}INDEX {idx.name} ({columns})"

    @staticmethod
    def _index_to_sqlite(table_name: str, idx: SchemaIndex) -> str:
        """Convert index to SQLite DDL."""
        unique = "UNIQUE " if idx.unique else ""
        columns = ", ".join(idx.columns)

        return f"CREATE {unique}INDEX {idx.name} ON {table_name} ({columns});"
