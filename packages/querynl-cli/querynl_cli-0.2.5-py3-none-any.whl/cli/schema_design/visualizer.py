"""
Schema Visualization

Generates Mermaid ER diagram syntax from schema proposals for visual representation
of table structures and relationships.
"""

import logging
from typing import List
from ..models import SchemaProposal, SchemaTable, SchemaRelationship

logger = logging.getLogger(__name__)


class MermaidERDGenerator:
    """
    Generates Mermaid ER diagram syntax from schema proposals.

    Creates text-based entity-relationship diagrams that can be rendered
    in GitHub, VS Code, or other Mermaid-compatible viewers.
    """

    @staticmethod
    def generate(schema: SchemaProposal) -> str:
        """
        Generate Mermaid ER diagram from schema proposal (T016).

        Args:
            schema: Schema proposal to visualize

        Returns:
            Mermaid ER diagram syntax as string
        """
        logger.info(f"Generating Mermaid ERD for schema with {len(schema.tables)} tables")

        lines = ["erDiagram"]
        lines.append("")

        # Generate table definitions
        for table in schema.tables:
            table_lines = MermaidERDGenerator._format_table(table)
            lines.extend(table_lines)
            lines.append("")

        # Generate relationships
        for relationship in schema.relationships:
            rel_line = MermaidERDGenerator._format_relationship(relationship)
            lines.append(rel_line)

        # Add metadata as comments
        lines.append("")
        lines.append(f"%% Database Type: {schema.database_type}")
        lines.append(f"%% Normalization: {schema.normalization_level}")
        lines.append(f"%% Version: {schema.version}")

        diagram = "\n".join(lines)
        logger.debug(f"Generated Mermaid ERD with {len(lines)} lines")

        return diagram

    @staticmethod
    def _format_table(table: SchemaTable) -> List[str]:
        """
        Format a single table for Mermaid ERD (T017).

        Args:
            table: Table to format

        Returns:
            List of Mermaid syntax lines for the table
        """
        lines = [f"    {table.name} {{"]

        # Add columns with types and constraints
        for column in table.columns:
            # Determine column type indicator
            type_indicator = MermaidERDGenerator._get_type_indicator(column.data_type)

            # Build constraint markers
            constraint_markers = []
            if "PRIMARY KEY" in column.constraints or "PK" in column.constraints:
                constraint_markers.append("PK")
            if "FOREIGN KEY" in column.constraints or "FK" in column.constraints:
                constraint_markers.append("FK")
            if "UNIQUE" in column.constraints:
                constraint_markers.append("UK")
            if "NOT NULL" in column.constraints:
                constraint_markers.append("NOT NULL")

            # Format column line
            constraint_suffix = f" {','.join(constraint_markers)}" if constraint_markers else ""
            column_line = f"        {type_indicator} {column.name}{constraint_suffix}"

            # Add comment if description exists
            if column.description:
                # Truncate long descriptions
                desc = column.description[:50] + "..." if len(column.description) > 50 else column.description
                column_line += f" \"{desc}\""

            lines.append(column_line)

        lines.append("    }")

        return lines

    @staticmethod
    def _format_relationship(relationship: SchemaRelationship) -> str:
        """
        Format a relationship for Mermaid ERD (T017).

        Args:
            relationship: Relationship to format

        Returns:
            Mermaid relationship syntax line
        """
        # Map relationship types to Mermaid cardinality syntax
        cardinality_map = {
            "one-to-one": "||--||",
            "one-to-many": "||--o{",
            "many-to-one": "}o--||",
            "many-to-many": "}o--o{"
        }

        cardinality = cardinality_map.get(relationship.type, "||--||")

        # Build relationship line
        # Format: TABLE1 ||--o{ TABLE2 : "label"
        label = relationship.description or f"has {relationship.type}"

        return f"    {relationship.from_table} {cardinality} {relationship.to_table} : \"{label}\""

    @staticmethod
    def _get_type_indicator(data_type: str) -> str:
        """
        Get Mermaid type indicator for a data type.

        Args:
            data_type: Database-specific data type

        Returns:
            Mermaid type indicator (string, int, etc.)
        """
        data_type_lower = data_type.lower()

        # Map common data types to Mermaid type indicators
        if any(t in data_type_lower for t in ["int", "serial", "bigint", "smallint"]):
            return "int"
        elif any(t in data_type_lower for t in ["varchar", "char", "text", "string"]):
            return "string"
        elif any(t in data_type_lower for t in ["float", "double", "decimal", "numeric", "real"]):
            return "float"
        elif any(t in data_type_lower for t in ["bool", "boolean"]):
            return "boolean"
        elif any(t in data_type_lower for t in ["date", "time", "timestamp"]):
            return "datetime"
        elif any(t in data_type_lower for t in ["json", "jsonb"]):
            return "json"
        elif any(t in data_type_lower for t in ["uuid"]):
            return "uuid"
        elif any(t in data_type_lower for t in ["blob", "binary", "bytea"]):
            return "blob"
        else:
            # Default to string for unknown types
            return "string"
