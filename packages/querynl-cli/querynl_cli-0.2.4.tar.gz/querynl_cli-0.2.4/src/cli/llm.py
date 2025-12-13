"""
LLM service integration for QueryNL CLI

Handles natural language to SQL translation via LLM API.
"""

import logging
import os
from typing import Dict, Any, Optional

try:
    # LangChain 0.1+ uses langchain_core
    from langchain_core.messages import HumanMessage, SystemMessage
except ImportError:
    # Fallback for older versions
    try:
        from langchain.schema import HumanMessage, SystemMessage
    except ImportError:
        # If langchain not installed, we'll handle it in the class
        HumanMessage = None
        SystemMessage = None

try:
    from langchain_openai import ChatOpenAI
except ImportError:
    ChatOpenAI = None

try:
    from langchain_anthropic import ChatAnthropic
except ImportError:
    ChatAnthropic = None

logger = logging.getLogger(__name__)


class LLMService:
    """
    LLM service for query generation using OpenAI or Anthropic.

    Supports multiple LLM providers for natural language to SQL translation.
    """

    def __init__(self, api_key: Optional[str] = None, provider: str = "openai"):
        """
        Initialize LLM service.

        Args:
            api_key: API key for LLM provider (falls back to env vars)
            provider: LLM provider ('openai' or 'anthropic')
        """
        self.provider = provider.lower()
        self.api_key = api_key
        self.llm = None

        # Initialize LLM client
        try:
            if self.provider == "openai":
                if ChatOpenAI is None:
                    logger.warning("langchain-openai not installed. Using pattern matching fallback.")
                    return

                api_key = api_key or os.getenv("OPENAI_API_KEY")
                if not api_key:
                    logger.warning("No OpenAI API key provided. Using pattern matching fallback.")
                    return

                self.llm = ChatOpenAI(
                    api_key=api_key,
                    model="gpt-4",
                    temperature=0.1,  # Low temperature for consistent SQL generation
                )
                logger.info("Initialized OpenAI LLM service with GPT-4")

            elif self.provider == "anthropic":
                if ChatAnthropic is None:
                    logger.warning("langchain-anthropic not installed. Using pattern matching fallback.")
                    return

                api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
                if not api_key:
                    logger.warning("No Anthropic API key provided. Using pattern matching fallback.")
                    return

                self.llm = ChatAnthropic(
                    api_key=api_key,
                    model="claude-3-5-sonnet-20241022",
                    temperature=0.1,
                )
                logger.info("Initialized Anthropic LLM service with Claude 3.5 Sonnet")

            else:
                logger.error(f"Unsupported LLM provider: {provider}")

        except Exception as e:
            logger.error(f"Failed to initialize LLM service: {e}")
            self.llm = None

    def generate_sql(
        self,
        natural_language: str,
        database_type: str,
        schema: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate SQL from natural language query.

        Args:
            natural_language: User's query in natural language
            database_type: Database type (postgresql, mysql, sqlite, mongodb)
            schema: Optional database schema for context

        Returns:
            Dictionary with:
                - sql: Generated SQL query
                - explanation: Human-readable explanation
                - confidence: Confidence score (0-1)
                - destructive: Whether query modifies data
        """
        logger.info(f"Generating SQL for: {natural_language}")

        # Use LLM if available, otherwise fallback to pattern matching
        if self.llm:
            return self._generate_sql_with_llm(natural_language, database_type, schema)
        else:
            logger.warning("LLM not available, using pattern matching fallback")
            return self._generate_sql_pattern_matching(natural_language, database_type, schema)

    def _generate_sql_with_llm(
        self,
        natural_language: str,
        database_type: str,
        schema: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate SQL using LLM API.

        Args:
            natural_language: User's query in natural language
            database_type: Database type
            schema: Optional database schema

        Returns:
            Dictionary with SQL generation results
        """
        try:
            # Build the prompt
            system_prompt = self._build_system_prompt(database_type, schema)
            user_prompt = self._build_user_prompt(natural_language)

            # Call LLM
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]

            logger.debug(f"Sending request to {self.provider} LLM")
            response = self.llm.invoke(messages)

            # Parse the response
            result = self._parse_llm_response(response.content, natural_language)
            logger.info(f"Successfully generated SQL with confidence: {result['confidence']}")

            return result

        except Exception as e:
            logger.error(f"LLM API call failed: {e}")
            # Fallback to pattern matching
            return self._generate_sql_pattern_matching(natural_language, database_type, schema)

    def _build_system_prompt(self, database_type: str, schema: Optional[Dict[str, Any]] = None) -> str:
        """Build the system prompt for SQL generation."""

        schema_context = ""
        if schema:
            schema_context = f"\n\nAvailable tables and columns:\n{self._format_schema(schema)}"

        prompt = f"""You are an expert SQL query generator for {database_type} databases.

Your task is to convert natural language queries into valid SQL queries.

Rules:
1. Generate only valid {database_type} SQL syntax
2. Use appropriate {database_type}-specific features when beneficial
3. **CRITICAL**: Use EXACT table and column names from the schema provided below
4. **CRITICAL**: If user mentions a table in singular/plural (e.g., "thread" or "threads"), use the EXACT table name from schema
5. **CRITICAL**: If user asks for "thread_id" but column is named "id", use the exact column name from schema
6. Always include LIMIT clauses for SELECT queries (default: LIMIT 100)
7. Use parameterized queries when values are needed (use ? for placeholders)
8. Be conservative with destructive operations (DELETE, UPDATE, DROP, TRUNCATE)
9. Add comments to explain complex queries
10. Return results in this exact JSON format:

{{
    "sql": "the generated SQL query",
    "explanation": "brief explanation of what the query does",
    "confidence": 0.95,
    "destructive": false,
    "warning": "optional warning message for destructive operations"
}}

Confidence scoring:
- 0.9-1.0: High confidence, standard query patterns
- 0.7-0.9: Medium confidence, query requires interpretation
- 0.5-0.7: Low confidence, ambiguous query
- Below 0.5: Cannot generate reliable SQL
{schema_context}

Important: Respond ONLY with the JSON object, no additional text."""

        return prompt

    def _build_user_prompt(self, natural_language: str) -> str:
        """Build the user prompt with the natural language query."""
        return f"Generate SQL for this query: {natural_language}"

    def _format_schema(self, schema: Dict[str, Any]) -> str:
        """Format schema information for the prompt."""
        if not schema:
            return "No schema information available"

        # Handle new schema structure from SchemaIntrospector
        if "tables" in schema:
            tables = schema["tables"]
            if not tables:
                return "No schema information available"

            formatted = []
            for table_name, table_info in sorted(tables.items()):
                columns = table_info.get("columns", [])
                column_details = table_info.get("column_details", [])

                if column_details:
                    # Format with column types
                    col_strs = []
                    for col in column_details:
                        col_str = f"{col['name']} ({col['type']})"
                        col_strs.append(col_str)
                    formatted.append(f"  - {table_name}: {', '.join(col_strs)}")
                elif columns:
                    # Simple column list
                    formatted.append(f"  - {table_name}: {', '.join(columns)}")
                else:
                    formatted.append(f"  - {table_name}")

            return "\n".join(formatted)

        # Fallback: Old format (dict of table -> columns)
        formatted = []
        for table_name, columns in schema.items():
            if isinstance(columns, list):
                cols = ", ".join(columns)
                formatted.append(f"  - {table_name}: {cols}")
            else:
                formatted.append(f"  - {table_name}")

        return "\n".join(formatted)

    def _parse_llm_response(self, response_text: str, original_query: str) -> Dict[str, Any]:
        """Parse the LLM response and extract structured data."""
        import json
        import re

        try:
            # Try to extract JSON from response
            # Sometimes LLM adds markdown code blocks
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try to find raw JSON
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                else:
                    raise ValueError("No JSON found in response")

            result = json.loads(json_str)

            # Validate required fields
            required_fields = ["sql", "explanation", "confidence", "destructive"]
            for field in required_fields:
                if field not in result:
                    raise ValueError(f"Missing required field: {field}")

            # Ensure confidence is a float between 0 and 1
            result["confidence"] = max(0.0, min(1.0, float(result["confidence"])))

            # Ensure destructive is boolean
            result["destructive"] = bool(result["destructive"])

            return result

        except Exception as e:
            logger.error(f"Failed to parse LLM response: {e}")
            logger.debug(f"Raw response: {response_text}")

            # Return a fallback response
            return {
                "sql": f"-- Failed to generate SQL for: {original_query}\n-- Error: {str(e)}",
                "explanation": f"Failed to parse LLM response: {str(e)}",
                "confidence": 0.0,
                "destructive": False,
                "error": str(e),
            }

    def _generate_sql_pattern_matching(
        self,
        natural_language: str,
        database_type: str,
        schema: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Fallback pattern matching for common queries when LLM is unavailable.

        This is the original implementation for backwards compatibility.
        """
        nl_lower = natural_language.lower()

        # Pattern matching for common queries
        # Count queries - "how many", "count", "number of"
        if any(phrase in nl_lower for phrase in ["how many", "count", "number of"]):
            # Try to extract table name
            import re

            # Patterns: "count X", "how many X", "records in X", "rows in X"
            table_patterns = [
                r"(?:count|how many|number of)\s+(?:records? in|rows? in|in)?\s+(\w+)",
                r"(?:records? in|rows? in)\s+(\w+)",
                r"(?:count|how many)\s+(\w+)",
            ]

            table_name = None
            for pattern in table_patterns:
                match = re.search(pattern, nl_lower)
                if match:
                    table_name = match.group(1)
                    # Clean up common words
                    if table_name not in ["the", "all", "any", "some", "table", "database"]:
                        break
                    table_name = None

            if table_name:
                return {
                    "sql": f"SELECT COUNT(*) AS count FROM {table_name};",
                    "explanation": f"Count total number of rows in {table_name} table",
                    "confidence": 0.85,
                    "destructive": False,
                }
            # Fallback to users if no specific table found
            elif "user" in nl_lower or "users" in nl_lower:
                return {
                    "sql": "SELECT COUNT(*) AS count FROM users;",
                    "explanation": "Count total number of rows in users table",
                    "confidence": 0.9,
                    "destructive": False,
                }

        elif "show" in nl_lower or "list" in nl_lower or "select" in nl_lower:
            # Show/list tables
            if "table" in nl_lower or "tables" in nl_lower:
                if database_type == "postgresql":
                    sql = "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';"
                elif database_type == "mysql":
                    sql = "SHOW TABLES;"
                elif database_type == "sqlite":
                    sql = "SELECT name FROM sqlite_master WHERE type='table';"
                else:
                    sql = "SHOW TABLES;"

                return {
                    "sql": sql,
                    "explanation": f"List all tables in the {database_type} database",
                    "confidence": 0.95,
                    "destructive": False,
                }

            # Show/list users
            elif "user" in nl_lower or "users" in nl_lower:
                sql = "SELECT * FROM users LIMIT 10;"
                if "active" in nl_lower:
                    sql = "SELECT * FROM users WHERE status = 'active' LIMIT 10;"
                return {
                    "sql": sql,
                    "explanation": "Retrieve user records from users table",
                    "confidence": 0.85,
                    "destructive": False,
                }

            # Generic: show/list [table_name]
            else:
                # Try to extract table name from query
                import re
                # Match patterns like "show all X", "list X", "show X"
                patterns = [
                    r"(?:show|list|select)\s+(?:all\s+)?(?:the\s+)?(\w+)",
                    r"(?:from|in)\s+(?:the\s+)?(\w+)",
                ]

                table_name = None
                for pattern in patterns:
                    match = re.search(pattern, nl_lower)
                    if match:
                        table_name = match.group(1)
                        break

                if table_name:
                    sql = f"SELECT * FROM {table_name} LIMIT 10;"
                    return {
                        "sql": sql,
                        "explanation": f"Retrieve records from {table_name} table",
                        "confidence": 0.75,
                        "destructive": False,
                    }

        elif "delete" in nl_lower:
            # Destructive operation
            if "user" in nl_lower or "users" in nl_lower:
                return {
                    "sql": "DELETE FROM users WHERE id = ?;",
                    "explanation": "Delete user(s) from users table",
                    "confidence": 0.75,
                    "destructive": True,
                    "warning": "This operation will permanently delete data",
                }

        elif "update" in nl_lower:
            # Destructive operation
            return {
                "sql": "UPDATE users SET status = ? WHERE id = ?;",
                "explanation": "Update user record(s) in users table",
                "confidence": 0.7,
                "destructive": True,
                "warning": "This operation will modify existing data",
            }

        elif "create table" in nl_lower or "drop table" in nl_lower:
            # Schema modification
            return {
                "sql": nl_lower.upper(),
                "explanation": "Schema modification operation",
                "confidence": 0.6,
                "destructive": True,
                "warning": "This operation will modify database schema",
            }

        else:
            # Fallback: Try to interpret as direct SQL if it looks SQL-like
            if any(keyword in nl_lower for keyword in ["select", "insert", "update", "delete", "create", "drop"]):
                return {
                    "sql": natural_language,
                    "explanation": "Direct SQL query (interpreted as-is)",
                    "confidence": 0.5,
                    "destructive": any(keyword in nl_lower for keyword in ["insert", "update", "delete", "drop", "alter"]),
                }

            # Unknown query type
            return {
                "sql": f"-- Unable to generate SQL for: {natural_language}\n-- Please try rephrasing your query or use direct SQL",
                "explanation": "Could not interpret query - please try rephrasing",
                "confidence": 0.1,
                "destructive": False,
                "error": "Query interpretation failed",
            }

    def is_destructive(self, sql: str) -> bool:
        """
        Check if SQL query is destructive (modifies data or schema).

        Args:
            sql: SQL query to check

        Returns:
            True if query is destructive, False otherwise
        """
        sql_upper = sql.upper().strip()
        destructive_keywords = ["DELETE", "DROP", "TRUNCATE", "UPDATE", "INSERT", "ALTER", "CREATE"]

        return any(sql_upper.startswith(keyword) for keyword in destructive_keywords)
