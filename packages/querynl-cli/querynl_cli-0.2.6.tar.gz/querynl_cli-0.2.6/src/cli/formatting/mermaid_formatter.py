"""
Mermaid ER diagram formatter for QueryNL CLI

Generates Mermaid syntax for database schema visualization.
"""

from typing import Dict, Any, List, Optional


def save_mermaid_to_file(
    schema_data: Dict[str, Any],
    file_path: str,
    database_type: str = "postgresql"
) -> None:
    """
    Save database schema as Mermaid ER diagram.

    Args:
        schema_data: Schema introspection data with tables and relationships
        file_path: Path to output file
        database_type: Database type for type mapping
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = MermaidWriter(f, database_type)
        writer.write_diagram(schema_data)


class MermaidWriter:
    """
    Mermaid ER diagram writer.

    Generates Entity-Relationship diagrams from schema data.
    """

    def __init__(self, file_handle, database_type: str = "postgresql"):
        self.file = file_handle
        self.database_type = database_type

    def write_diagram(self, schema_data: Dict[str, Any]) -> None:
        """
        Write complete Mermaid ER diagram.

        Args:
            schema_data: Schema with 'tables' and optionally 'relationships'
        """
        self.file.write("erDiagram\n")

        # Write entities
        tables = schema_data.get("tables", [])
        for table in tables:
            self._write_entity(table)

        # Write relationships if available
        relationships = schema_data.get("relationships", [])
        if relationships:
            self.file.write("\n  %% Relationships\n")
            for rel in relationships:
                self._write_relationship(rel)

    def _write_entity(self, table: Dict[str, Any]) -> None:
        """
        Write a single entity (table) definition.

        Args:
            table: Table data with name and columns
        """
        table_name = self._sanitize_name(table.get("name", "UNKNOWN"))
        columns = table.get("columns", [])

        self.file.write(f"  {table_name.upper()} {{\n")

        for col in columns:
            col_name = self._sanitize_name(col.get("name", ""))
            col_type = self._map_type(col.get("type", ""))

            # Determine markers
            markers = []
            if col.get("primary_key") or col_name == "id":
                markers.append("PK")
            if col_name.endswith("_id") and col_name != "id":
                markers.append("FK")
            if col.get("unique"):
                markers.append("UK")

            marker_str = " " + " ".join(markers) if markers else ""

            self.file.write(f"    {col_type} {col_name}{marker_str}\n")

        self.file.write("  }\n\n")

    def _write_relationship(self, relationship: Dict[str, Any]) -> None:
        """
        Write a relationship between entities.

        Args:
            relationship: Relationship data with from/to tables and cardinality
        """
        from_table = self._sanitize_name(relationship.get("from_table", ""))
        to_table = self._sanitize_name(relationship.get("to_table", ""))

        # Determine cardinality notation
        cardinality = relationship.get("cardinality", "one-to-many")

        if cardinality == "one-to-one":
            notation = "||--||"
        elif cardinality == "one-to-many":
            notation = "||--o{"
        elif cardinality == "many-to-many":
            notation = "}o--o{"
        else:
            notation = "||--o{"  # default to one-to-many

        rel_name = relationship.get("name", "has")

        self.file.write(
            f"  {from_table.upper()} {notation} {to_table.upper()} : \"{rel_name}\"\n"
        )

    def _map_type(self, db_type: str) -> str:
        """
        Map database type to Mermaid-friendly type.

        Args:
            db_type: Database-specific type

        Returns:
            Simplified Mermaid type
        """
        db_type_lower = db_type.lower()

        # Integer types
        if any(t in db_type_lower for t in ['int', 'serial', 'bigserial']):
            return 'int'

        # String types
        if any(t in db_type_lower for t in ['char', 'varchar', 'text', 'string']):
            return 'string'

        # Numeric types
        if any(t in db_type_lower for t in ['decimal', 'numeric', 'float', 'double', 'real']):
            return 'decimal'

        # Date/time types
        if any(t in db_type_lower for t in ['date', 'time', 'timestamp']):
            return 'datetime'

        # Boolean
        if 'bool' in db_type_lower:
            return 'boolean'

        # JSON
        if 'json' in db_type_lower:
            return 'json'

        # UUID
        if 'uuid' in db_type_lower:
            return 'uuid'

        # Binary
        if any(t in db_type_lower for t in ['blob', 'binary', 'bytea']):
            return 'binary'

        # Default
        return 'string'

    @staticmethod
    def _sanitize_name(name: str) -> str:
        """
        Sanitize entity/column name for Mermaid syntax.

        Args:
            name: Original name

        Returns:
            Sanitized name (underscores for spaces/special chars)
        """
        # Replace spaces and special characters with underscores
        sanitized = name.replace(' ', '_').replace('-', '_')

        # Remove other special characters
        sanitized = ''.join(c if c.isalnum() or c == '_' else '_' for c in sanitized)

        return sanitized
