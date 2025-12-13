"""
JSON formatter for QueryNL CLI

Complies with output-formats.json schema for QueryResult structure.
"""

import json
from typing import Dict, Any, Optional, List
from datetime import datetime, date
from decimal import Decimal
from rich.console import Console

console = Console()


def format_query_result_json(
    result: Dict[str, Any],
    natural_language_query: Optional[str] = None,
    generated_sql: Optional[str] = None,
    include_metadata: bool = True
) -> str:
    """
    Format query results as JSON according to QueryResult schema.

    Args:
        result: Query result dictionary with rows, row_count, execution_time_ms
        natural_language_query: Original natural language query
        generated_sql: Generated SQL statement
        include_metadata: Include query metadata (query, sql, execution_time_ms)

    Returns:
        JSON string formatted according to contract
    """
    output = {
        "status": "success",
        "rows": result.get("rows", []),
        "row_count": result.get("row_count", 0),
        "execution_time_ms": result.get("execution_time_ms", 0),
    }

    if include_metadata:
        if natural_language_query:
            output["query"] = natural_language_query
        if generated_sql:
            output["sql"] = generated_sql

    # Check for errors
    if result.get("error"):
        output["status"] = "error"
        output["error"] = {
            "message": str(result.get("error")),
            "code": result.get("error_code", "QUERY_ERROR"),
        }
        if result.get("suggestion"):
            output["error"]["suggestion"] = result["suggestion"]

    return json.dumps(output, indent=2, default=str)


def print_json(
    result: Dict[str, Any],
    natural_language_query: Optional[str] = None,
    generated_sql: Optional[str] = None,
    include_metadata: bool = True
) -> None:
    """
    Print query results as JSON to console.

    Args:
        result: Query result dictionary
        natural_language_query: Original query
        generated_sql: Generated SQL
        include_metadata: Include metadata in output
    """
    json_output = format_query_result_json(
        result,
        natural_language_query,
        generated_sql,
        include_metadata
    )

    # Use Rich's JSON printer for syntax highlighting
    console.print_json(json_output)


def format_connection_list_json(connections: Dict[str, Dict[str, Any]], default_connection: Optional[str] = None) -> str:
    """
    Format connection list as JSON according to ConnectionList schema.

    Args:
        connections: Dictionary of connection configurations
        default_connection: Name of default connection

    Returns:
        JSON string formatted according to contract
    """
    connection_list = []

    for name, conn_data in connections.items():
        connection_obj = {
            "name": name,
            "type": conn_data.get("database_type", "unknown"),
            "database": conn_data.get("database_name", ""),
            "is_default": (name == default_connection),
            "status": "active",  # TODO: Test connection status
        }

        # Optional fields
        if conn_data.get("host"):
            connection_obj["host"] = conn_data["host"]
        if conn_data.get("port"):
            connection_obj["port"] = conn_data["port"]
        if conn_data.get("username"):
            connection_obj["username"] = conn_data["username"]
        if "ssl_enabled" in conn_data:
            connection_obj["ssl_enabled"] = conn_data["ssl_enabled"]
        if conn_data.get("created_at"):
            connection_obj["created_at"] = conn_data["created_at"]
        if conn_data.get("last_used"):
            connection_obj["last_used"] = conn_data["last_used"]

        connection_list.append(connection_obj)

    return json.dumps({"connections": connection_list}, indent=2, default=str)


def format_connection_test_json(
    connection_name: str,
    test_result: Dict[str, Any]
) -> str:
    """
    Format connection test result as JSON according to ConnectionTest schema.

    Args:
        connection_name: Name of tested connection
        test_result: Test result dictionary

    Returns:
        JSON string formatted according to contract
    """
    output = {
        "connection_name": connection_name,
        "status": test_result.get("status", "failed"),
    }

    if test_result.get("status") == "success":
        output["details"] = {
            "latency_ms": test_result.get("latency_ms", 0),
        }
        if test_result.get("version"):
            output["details"]["database_version"] = test_result["version"]
        if test_result.get("server"):
            output["details"]["server"] = test_result["server"]
    else:
        output["error"] = {
            "message": test_result.get("error", "Connection failed"),
        }
        if test_result.get("suggestion"):
            output["error"]["suggestion"] = test_result["suggestion"]

    return json.dumps(output, indent=2, default=str)


def format_error_json(
    error_type: str,
    message: str,
    suggestion: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> str:
    """
    Format error as JSON according to Error schema.

    Args:
        error_type: Error type/code
        message: Error message
        suggestion: Actionable suggestion
        details: Additional error details

    Returns:
        JSON string formatted according to contract
    """
    output = {
        "error": error_type,
        "message": message,
    }

    if suggestion:
        output["suggestion"] = suggestion
    if details:
        output["details"] = details

    return json.dumps(output, indent=2, default=str)


def _serialize_value(obj: Any) -> Any:
    """
    Custom JSON serializer for non-standard types.

    Handles:
    - datetime/date → ISO 8601 string
    - Decimal → float
    - bytes → base64 string
    - Other → str()
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, bytes):
        import base64
        return base64.b64encode(obj).decode('ascii')
    else:
        return str(obj)


def save_json_to_file(
    result: Dict[str, Any],
    file_path: str,
    pretty: bool = True
) -> None:
    """
    Save query results as JSON array to file.

    Args:
        result: Query result dictionary
        file_path: Path to output file
        pretty: Pretty-print JSON (default: True)
    """
    rows = result.get("rows", [])

    with open(file_path, 'w', encoding='utf-8') as f:
        if pretty:
            json.dump(rows, f, indent=2, default=_serialize_value, ensure_ascii=False)
        else:
            json.dump(rows, f, default=_serialize_value, ensure_ascii=False)


class StreamingJSONWriter:
    """
    Streaming JSON array writer for large result sets.

    Writes: [{"row": 1}, {"row": 2}, ...]
    """

    def __init__(self, file_handle, pretty: bool = False):
        self.file = file_handle
        self.pretty = pretty
        self._first_row = True

    def begin(self, columns: List[str]) -> None:
        """Initialize JSON array."""
        self.file.write('[')
        if self.pretty:
            self.file.write('\n')

    def write_row(self, row: Dict[str, Any]) -> None:
        """Write a single row to JSON array."""
        if not self._first_row:
            self.file.write(',')
            if self.pretty:
                self.file.write('\n')

        json_str = json.dumps(row, default=_serialize_value, ensure_ascii=False)

        if self.pretty:
            self.file.write('  ' + json_str)
        else:
            self.file.write(json_str)

        self._first_row = False

    def end(self) -> None:
        """End JSON array."""
        if self.pretty:
            self.file.write('\n')
        self.file.write(']')
        if self.pretty:
            self.file.write('\n')
