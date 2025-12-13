"""
Schema Proposal Generation

Generates normalized database schema proposals from natural language descriptions
and file analysis results using LLM-powered design expertise.
"""

import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from langchain_core.messages import HumanMessage, SystemMessage

from ..llm import LLMService
from ..models import (
    SchemaProposal, SchemaTable, SchemaColumn, SchemaIndex,
    SchemaConstraint, SchemaRelationship, UploadedFile
)

logger = logging.getLogger(__name__)


# System prompt for schema generation (T013)
SCHEMA_GENERATION_PROMPT = """You are a database schema design expert. Generate a well-structured, normalized database schema based on the requirements provided.

**Output Format:**
Respond with a valid JSON object containing the complete schema definition. Use this exact structure:

```json
{{
  "database_type": "<postgresql|mysql|sqlite|mongodb>",
  "normalization_level": "<1NF|2NF|3NF|denormalized>",
  "tables": [
    {{
      "name": "table_name",
      "description": "Purpose of this table",
      "columns": [
        {{
          "name": "column_name",
          "data_type": "INTEGER|VARCHAR(255)|TEXT|TIMESTAMP|etc",
          "constraints": ["PRIMARY KEY", "NOT NULL", "UNIQUE"],
          "default_value": null,
          "description": "Purpose of this column"
        }}
      ],
      "indexes": [
        {{
          "name": "idx_name",
          "columns": ["col1", "col2"],
          "type": "btree",
          "unique": false
        }}
      ],
      "constraints": [
        {{
          "type": "FOREIGN KEY",
          "definition": "FOREIGN KEY (user_id) REFERENCES users(id)",
          "description": "Rationale for constraint"
        }}
      ]
    }}
  ],
  "relationships": [
    {{
      "from_table": "orders",
      "to_table": "customers",
      "type": "many-to-one",
      "foreign_key": "customer_id",
      "junction_table": null,
      "description": "Each order belongs to one customer"
    }}
  ],
  "rationale": "Overall design explanation and key decisions",
  "warnings": ["List of potential issues or considerations"]
}}
```

**Requirements:**
1. All tables must have a primary key
2. Use appropriate data types for {database_type}
3. Follow {normalization_level} normalization (3NF by default)
4. Include foreign keys for relationships
5. Add indexes for common query patterns
6. Use descriptive rationale for design decisions
7. Include warnings for any assumptions or potential issues

**IMPORTANT:**
- Respond ONLY with the JSON object
- Do not include markdown code blocks or explanations before/after the JSON
- Ensure the JSON is valid and follows the schema exactly
"""


class SchemaGenerator:
    """
    Generates database schema proposals from requirements.

    Uses LLM to create normalized, well-structured schemas with proper
    relationships, constraints, and indexing strategies.
    """

    def __init__(self, llm_service: LLMService):
        """
        Initialize schema generator.

        Args:
            llm_service: LLM service for schema generation
        """
        self.llm = llm_service
        self.logger = logging.getLogger(self.__class__.__name__)

    def generate_from_description(
        self,
        description: str,
        database_type: str = "postgresql",
        normalization_level: str = "3NF",
        additional_context: Optional[str] = None
    ) -> SchemaProposal:
        """
        Generate schema proposal from natural language description (T013).

        Args:
            description: Natural language description of requirements
            database_type: Target database type
            normalization_level: Desired normalization level
            additional_context: Optional additional context from conversation

        Returns:
            SchemaProposal with tables, relationships, and rationale

        Raises:
            Exception: If LLM call fails or response is invalid
        """
        self.logger.info(f"Generating schema from description for {database_type}")

        # Build the generation prompt
        system_prompt = SCHEMA_GENERATION_PROMPT.format(
            database_type=database_type,
            normalization_level=normalization_level
        )

        # Build user prompt with requirements
        user_prompt_parts = [
            f"Generate a database schema for the following requirements:",
            f"",
            f"Description: {description}",
            f"",
            f"Target Database: {database_type}",
            f"Normalization Level: {normalization_level}"
        ]

        if additional_context:
            user_prompt_parts.extend([
                f"",
                f"Additional Context:",
                additional_context
            ])

        user_prompt = "\n".join(user_prompt_parts)

        try:
            # Call LLM
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]

            self.logger.debug("Calling LLM for schema generation")
            response = self.llm.llm.invoke(messages)
            response_text = response.content.strip()

            # Extract JSON from response (handle potential markdown wrapping)
            json_text = self._extract_json(response_text)

            # Parse JSON response
            schema_dict = json.loads(json_text)

            # Validate schema structure
            self._validate_schema_dict(schema_dict)

            # Convert to SchemaProposal model
            schema_proposal = self._dict_to_schema_proposal(schema_dict)

            self.logger.info(f"Successfully generated schema with {len(schema_proposal.tables)} tables")
            return schema_proposal

        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse schema JSON: {e}")
            self.logger.error(f"Response was: {response_text[:500]}")
            raise Exception(f"LLM returned invalid JSON: {str(e)}")

        except Exception as e:
            self.logger.error(f"Schema generation failed: {e}")
            raise Exception(f"Failed to generate schema: {str(e)}")

    def generate_from_files(
        self,
        uploaded_files: List[UploadedFile],
        database_type: str = "postgresql",
        normalization_level: str = "3NF",
        additional_context: Optional[str] = None
    ) -> SchemaProposal:
        """
        Generate schema proposal from uploaded data files (T034).

        Uses file analysis results (column types, detected entities, relationships)
        to create a database schema that represents the uploaded data structure.

        Args:
            uploaded_files: List of analyzed files
            database_type: Target database type
            normalization_level: Desired normalization level
            additional_context: Optional additional context from conversation

        Returns:
            SchemaProposal based on file analysis

        Raises:
            Exception: If LLM call fails or response is invalid
        """
        self.logger.info(f"Generating schema from {len(uploaded_files)} files for {database_type}")

        # Build context from file analyses
        file_context_parts = []
        for file in uploaded_files:
            analysis = file.analysis
            file_context_parts.append(f"File: {file.file_name}")
            file_context_parts.append(f"  Rows: {analysis.row_count}, Columns: {analysis.column_count}")
            file_context_parts.append(f"  Detected Entities: {', '.join(analysis.detected_entities)}")
            file_context_parts.append(f"  Columns:")

            for col in analysis.columns:
                nullable_str = "nullable" if col.nullable else "not null"
                unique_str = f", {col.unique_values} unique values" if col.unique_values else ""
                sample_str = f", samples: {col.sample_values[:3]}" if col.sample_values else ""
                file_context_parts.append(
                    f"    - {col.name}: {col.inferred_type} ({nullable_str}{unique_str}{sample_str})"
                )

            if analysis.potential_relationships:
                file_context_parts.append(f"  Potential Relationships:")
                for rel in analysis.potential_relationships:
                    file_context_parts.append(
                        f"    - {rel.from_column} -> {rel.to_file}.{rel.to_column} (confidence: {rel.confidence:.2f})"
                    )

            file_context_parts.append("")  # Blank line between files

        file_context = "\n".join(file_context_parts)

        # Build the generation prompt
        system_prompt = SCHEMA_GENERATION_PROMPT.format(
            database_type=database_type,
            normalization_level=normalization_level
        )

        # Build user prompt with file analysis
        user_prompt_parts = [
            f"Generate a database schema based on the following uploaded data files:",
            f"",
            file_context,
            f"",
            f"Target Database: {database_type}",
            f"Normalization Level: {normalization_level}",
            f"",
            f"Instructions:",
            f"1. Use the detected entities as table names",
            f"2. Use the inferred column types from the file analysis",
            f"3. Create foreign key relationships based on detected relationships",
            f"4. Add primary keys (id columns) where missing",
            f"5. Consider normalization: denormalized file data may need to be split into multiple tables",
            f"6. Add appropriate indexes for foreign keys and common query patterns"
        ]

        if additional_context:
            user_prompt_parts.extend([
                f"",
                f"Additional Context:",
                additional_context
            ])

        user_prompt = "\n".join(user_prompt_parts)

        try:
            # Call LLM
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]

            self.logger.debug("Calling LLM for schema generation from files")
            response = self.llm.llm.invoke(messages)
            response_text = response.content.strip()

            # Extract JSON from response
            json_text = self._extract_json(response_text)

            # Parse JSON response
            schema_dict = json.loads(json_text)

            # Validate schema structure
            self._validate_schema_dict(schema_dict)

            # Convert to SchemaProposal model
            schema_proposal = self._dict_to_schema_proposal(schema_dict)

            self.logger.info(f"Successfully generated schema with {len(schema_proposal.tables)} tables from files")
            return schema_proposal

        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse schema JSON: {e}")
            self.logger.error(f"Response was: {response_text[:500]}")
            raise Exception(f"LLM returned invalid JSON: {str(e)}")

        except Exception as e:
            self.logger.error(f"Schema generation from files failed: {e}")
            raise Exception(f"Failed to generate schema from files: {str(e)}")

    def refine_schema(
        self,
        current_schema: SchemaProposal,
        refinement_request: str,
        conversation_context: Optional[str] = None
    ) -> SchemaProposal:
        """
        Refine existing schema based on user requests (T041).

        Modifies an existing schema based on user feedback such as:
        - "Add an index on the email column"
        - "Denormalize the address table into users"
        - "Add a created_at timestamp to all tables"
        - "Split the users table to separate profile information"

        Args:
            current_schema: Existing schema to refine
            refinement_request: Natural language refinement request
            conversation_context: Optional conversation history for context

        Returns:
            SchemaProposal with requested modifications

        Raises:
            Exception: If LLM call fails or response is invalid
        """
        self.logger.info(f"Refining schema based on request: {refinement_request[:100]}...")

        # Build current schema summary for LLM
        current_schema_summary = self._schema_to_summary(current_schema)

        # Build refinement prompt
        system_prompt = SCHEMA_GENERATION_PROMPT.format(
            database_type=current_schema.database_type,
            normalization_level=current_schema.normalization_level
        )

        # Build user prompt
        user_prompt_parts = [
            f"I have an existing database schema that needs refinement.",
            f"",
            f"**Current Schema Summary:**",
            current_schema_summary,
            f"",
            f"**Current Design Rationale:**",
            current_schema.rationale,
            f"",
            f"**Refinement Request:**",
            refinement_request,
            f"",
            f"**Instructions:**",
            f"1. Apply the requested changes to the current schema",
            f"2. Maintain consistency with the target database type ({current_schema.database_type})",
            f"3. Preserve existing tables/columns unless explicitly asked to change them",
            f"4. Update the rationale to explain the changes made",
            f"5. Add warnings if the changes introduce potential issues",
            f"6. Ensure all foreign key references are still valid after changes",
            f"",
            f"Generate the COMPLETE refined schema (not just the changes) in JSON format."
        ]

        if conversation_context:
            user_prompt_parts.extend([
                f"",
                f"**Conversation Context:**",
                conversation_context
            ])

        user_prompt = "\n".join(user_prompt_parts)

        try:
            # Call LLM
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]

            self.logger.debug("Calling LLM for schema refinement")
            response = self.llm.llm.invoke(messages)
            response_text = response.content.strip()

            # Extract JSON from response
            json_text = self._extract_json(response_text)

            # Parse JSON response
            schema_dict = json.loads(json_text)

            # Validate schema structure
            self._validate_schema_dict(schema_dict)

            # Convert to SchemaProposal model
            refined_schema = self._dict_to_schema_proposal(schema_dict)

            # Preserve version (will be incremented by session.add_schema_version())
            refined_schema.version = current_schema.version + 1

            self.logger.info(f"Successfully refined schema (version {current_schema.version} -> {refined_schema.version})")
            return refined_schema

        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse refined schema JSON: {e}")
            self.logger.error(f"Response was: {response_text[:500]}")
            raise Exception(f"LLM returned invalid JSON during refinement: {str(e)}")

        except Exception as e:
            self.logger.error(f"Schema refinement failed: {e}")
            raise Exception(f"Failed to refine schema: {str(e)}")

    def _schema_to_summary(self, schema: SchemaProposal) -> str:
        """
        Convert schema to text summary for LLM context.

        Args:
            schema: Schema to summarize

        Returns:
            Text summary of schema structure
        """
        summary_parts = [
            f"Database: {schema.database_type}",
            f"Normalization: {schema.normalization_level}",
            f"Version: {schema.version}",
            f"",
            f"Tables ({len(schema.tables)}):"
        ]

        for table in schema.tables:
            summary_parts.append(f"")
            summary_parts.append(f"  {table.name}:")
            if table.description:
                summary_parts.append(f"    Description: {table.description}")

            summary_parts.append(f"    Columns:")
            for col in table.columns:
                constraints_str = ", ".join(col.constraints) if col.constraints else ""
                col_summary = f"      - {col.name}: {col.data_type}"
                if constraints_str:
                    col_summary += f" [{constraints_str}]"
                if col.description:
                    col_summary += f" - {col.description}"
                summary_parts.append(col_summary)

            if table.indexes:
                summary_parts.append(f"    Indexes:")
                for idx in table.indexes:
                    unique_str = "UNIQUE " if idx.unique else ""
                    summary_parts.append(f"      - {unique_str}{idx.name} on ({', '.join(idx.columns)})")

            if table.constraints:
                summary_parts.append(f"    Constraints:")
                for con in table.constraints:
                    summary_parts.append(f"      - {con.type}: {con.definition}")

        if schema.relationships:
            summary_parts.append(f"")
            summary_parts.append(f"Relationships ({len(schema.relationships)}):")
            for rel in schema.relationships:
                rel_type = rel.type.upper()
                summary_parts.append(
                    f"  - {rel.from_table}.{rel.foreign_key} -> {rel.to_table} ({rel_type})"
                )

        return "\n".join(summary_parts)

    def validate_schema(self, schema: SchemaProposal) -> Dict[str, Any]:
        """
        Validate schema structure and constraints (T014).

        Args:
            schema: Schema proposal to validate

        Returns:
            Dictionary with validation results:
                - valid: bool
                - errors: List[str] (fatal issues)
                - warnings: List[str] (potential issues)
        """
        self.logger.info(f"Validating schema with {len(schema.tables)} tables")

        errors = []
        warnings = []

        # Check: All tables have at least one column
        for table in schema.tables:
            if not table.columns:
                errors.append(f"Table '{table.name}' has no columns")

            # Check: All tables have a primary key
            has_pk = any("PRIMARY KEY" in col.constraints for col in table.columns)
            if not has_pk:
                errors.append(f"Table '{table.name}' has no primary key")

            # Check: Column names are unique within table
            column_names = [col.name for col in table.columns]
            if len(column_names) != len(set(column_names)):
                errors.append(f"Table '{table.name}' has duplicate column names")

        # Check: Table names are unique
        table_names = [t.name for t in schema.tables]
        if len(table_names) != len(set(table_names)):
            errors.append("Schema has duplicate table names")

        # Check: Foreign key references point to existing tables
        for rel in schema.relationships:
            if rel.from_table not in table_names:
                errors.append(f"Relationship references non-existent table '{rel.from_table}'")
            if rel.to_table not in table_names:
                errors.append(f"Relationship references non-existent table '{rel.to_table}'")

            # Check: Foreign key column exists in from_table
            from_table = next((t for t in schema.tables if t.name == rel.from_table), None)
            if from_table:
                fk_col_names = [col.name for col in from_table.columns]
                if rel.foreign_key not in fk_col_names:
                    errors.append(f"Foreign key column '{rel.foreign_key}' not found in table '{rel.from_table}'")

        # Warnings: Check for potential issues
        for table in schema.tables:
            # Warn if table has no indexes besides PK
            if len(table.indexes) == 0 and len(table.columns) > 3:
                warnings.append(f"Table '{table.name}' has no indexes (consider adding for performance)")

            # Warn if table has many columns (possible denormalization)
            if len(table.columns) > 20:
                warnings.append(f"Table '{table.name}' has {len(table.columns)} columns (consider normalization)")

        # Warn if many-to-many relationships don't have junction tables
        for rel in schema.relationships:
            if rel.type == "many-to-many" and not rel.junction_table:
                warnings.append(f"Many-to-many relationship between '{rel.from_table}' and '{rel.to_table}' should have junction table")

        is_valid = len(errors) == 0

        self.logger.info(f"Validation complete: {len(errors)} errors, {len(warnings)} warnings")

        return {
            "valid": is_valid,
            "errors": errors,
            "warnings": warnings
        }

    def _extract_json(self, text: str) -> str:
        """
        Extract JSON from LLM response (handles markdown code blocks).

        Args:
            text: Response text potentially containing JSON

        Returns:
            Extracted JSON string
        """
        # Remove markdown code blocks if present
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            return text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            return text[start:end].strip()
        else:
            return text.strip()

    def _validate_schema_dict(self, schema_dict: Dict[str, Any]) -> None:
        """
        Validate schema dictionary structure.

        Args:
            schema_dict: Parsed JSON schema dictionary

        Raises:
            ValueError: If schema structure is invalid
        """
        required_keys = ["database_type", "tables", "rationale"]
        for key in required_keys:
            if key not in schema_dict:
                raise ValueError(f"Schema missing required key: {key}")

        if not isinstance(schema_dict["tables"], list):
            raise ValueError("Schema 'tables' must be a list")

        if len(schema_dict["tables"]) == 0:
            raise ValueError("Schema must have at least one table")

    def _dict_to_schema_proposal(self, schema_dict: Dict[str, Any]) -> SchemaProposal:
        """
        Convert schema dictionary to SchemaProposal model.

        Args:
            schema_dict: Parsed schema dictionary

        Returns:
            SchemaProposal instance
        """
        # Parse tables
        tables = []
        for table_dict in schema_dict["tables"]:
            columns = [
                SchemaColumn(
                    name=col["name"],
                    data_type=col["data_type"],
                    constraints=col.get("constraints", []),
                    default_value=col.get("default_value"),
                    description=col.get("description")
                )
                for col in table_dict.get("columns", [])
            ]

            indexes = [
                SchemaIndex(
                    name=idx["name"],
                    columns=idx["columns"],
                    type=idx.get("type", "btree"),
                    unique=idx.get("unique", False)
                )
                for idx in table_dict.get("indexes", [])
            ]

            constraints = [
                SchemaConstraint(
                    type=con["type"],
                    definition=con["definition"],
                    description=con.get("description")
                )
                for con in table_dict.get("constraints", [])
            ]

            tables.append(SchemaTable(
                name=table_dict["name"],
                columns=columns,
                indexes=indexes,
                constraints=constraints,
                description=table_dict.get("description")
            ))

        # Parse relationships
        relationships = [
            SchemaRelationship(
                from_table=rel["from_table"],
                to_table=rel["to_table"],
                type=rel["type"],
                foreign_key=rel["foreign_key"],
                junction_table=rel.get("junction_table"),
                description=rel.get("description")
            )
            for rel in schema_dict.get("relationships", [])
        ]

        # Create SchemaProposal
        return SchemaProposal(
            version=1,  # Will be set properly by session.add_schema_version()
            database_type=schema_dict["database_type"],
            normalization_level=schema_dict.get("normalization_level", "3NF"),
            tables=tables,
            relationships=relationships,
            rationale=schema_dict["rationale"],
            warnings=schema_dict.get("warnings", [])
        )
