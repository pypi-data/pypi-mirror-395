"""
Credential management for QueryNL CLI

Handles secure storage and retrieval of database credentials using OS keychain
with fallback to encrypted file storage for headless environments.
"""

import os
import json
from typing import Optional, Dict, Any
import keyring
try:
    from keyring.errors import KeyringError
except ImportError:
    # Fallback for older keyring versions
    KeyringError = Exception
from rich.console import Console

console = Console()

# Service name for keyring
SERVICE_NAME = "querynl"


def _setup_fallback_keyring() -> None:
    """
    Setup keyrings.cryptfile fallback for headless environments.

    Uses QUERYNL_KEYRING_PASSWORD environment variable for encryption.
    """
    try:
        from keyrings.cryptfile.cryptfile import CryptFileKeyring

        kr = CryptFileKeyring()

        # Get password from environment variable
        keyring_password = os.environ.get("QUERYNL_KEYRING_PASSWORD")

        if keyring_password:
            kr.keyring_key = keyring_password
            keyring.set_keyring(kr)
            console.print("[dim]Using encrypted file keyring (headless mode)[/dim]")
        else:
            console.print("[yellow]Warning: QUERYNL_KEYRING_PASSWORD not set for headless environment[/yellow]")
            console.print("[yellow]Falling back to unencrypted file storage (NOT RECOMMENDED)[/yellow]")

    except ImportError:
        console.print("[yellow]Warning: keyrings.cryptfile not available[/yellow]")
        console.print("[yellow]Install with: pip install keyrings.cryptfile[/yellow]")


def _test_keyring_access() -> bool:
    """
    Test if OS keychain is accessible.

    Returns:
        True if keychain works, False otherwise
    """
    try:
        # Try to set and retrieve a test value
        test_account = "__querynl_test__"
        keyring.set_password(SERVICE_NAME, test_account, "test")
        result = keyring.get_password(SERVICE_NAME, test_account)
        keyring.delete_password(SERVICE_NAME, test_account)
        return result == "test"
    except Exception:
        return False


# Check keyring availability on module load
if not _test_keyring_access():
    console.print("[dim]OS keychain not available, setting up fallback...[/dim]")
    _setup_fallback_keyring()


def store_password(connection_name: str, password: str) -> None:
    """
    Store database password in secure credential store.

    Args:
        connection_name: Name of the connection
        password: Password to store

    Raises:
        Exception: If credential storage fails
    """
    try:
        keyring.set_password(SERVICE_NAME, connection_name, password)
    except KeyringError as e:
        raise Exception(f"Failed to store credentials: {e}")


def get_password(connection_name: str) -> Optional[str]:
    """
    Retrieve database password from credential store.

    Args:
        connection_name: Name of the connection

    Returns:
        Password if found, None otherwise
    """
    try:
        return keyring.get_password(SERVICE_NAME, connection_name)
    except KeyringError:
        return None


def delete_password(connection_name: str) -> None:
    """
    Delete password from credential store.

    Args:
        connection_name: Name of the connection

    Raises:
        Exception: If deletion fails
    """
    try:
        keyring.delete_password(SERVICE_NAME, connection_name)
    except KeyringError as e:
        # Don't raise if password doesn't exist
        if "not found" not in str(e).lower():
            raise Exception(f"Failed to delete credentials: {e}")


def store_connection_credentials(connection_name: str, credentials: Dict[str, Any]) -> None:
    """
    Store all connection credentials as JSON.

    Args:
        connection_name: Name of the connection
        credentials: Dictionary of credentials (password, ssh_password, etc.)
    """
    credentials_json = json.dumps(credentials)
    store_password(connection_name, credentials_json)


def get_connection_credentials(connection_name: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve all connection credentials.

    Args:
        connection_name: Name of the connection

    Returns:
        Dictionary of credentials if found, None otherwise
    """
    credentials_json = get_password(connection_name)

    if credentials_json:
        try:
            return json.loads(credentials_json)
        except json.JSONDecodeError:
            # Legacy single password storage
            return {"password": credentials_json}

    return None


def parse_connection_string(connection_string: str) -> Dict[str, Any]:
    """
    Parse database connection string from environment variable.

    Supports standard connection string formats:
    - postgresql://user:password@host:port/database
    - mysql://user:password@host:port/database
    - mongodb://user:password@host:port/database
    - sqlite:///path/to/database.db

    Args:
        connection_string: Connection string to parse

    Returns:
        Dictionary with connection details

    Raises:
        ValueError: If connection string format is invalid
    """
    try:
        # Basic URL parsing (simplified - production would use urllib.parse)
        if connection_string.startswith("sqlite:///"):
            database_path = connection_string.replace("sqlite:///", "")
            return {
                "database_type": "sqlite",
                "database_name": database_path,
            }

        # Parse standard connection string
        # Format: protocol://user:password@host:port/database
        protocol, rest = connection_string.split("://", 1)

        database_type_map = {
            "postgresql": "postgresql",
            "postgres": "postgresql",
            "mysql": "mysql",
            "mongodb": "mongodb",
            "mongo": "mongodb",
        }

        database_type = database_type_map.get(protocol)
        if not database_type:
            raise ValueError(f"Unsupported database type: {protocol}")

        # Split credentials and host
        if "@" in rest:
            credentials, host_part = rest.rsplit("@", 1)
            if ":" in credentials:
                username, password = credentials.split(":", 1)
            else:
                username = credentials
                password = None
        else:
            username = None
            password = None
            host_part = rest

        # Split host/port and database
        if "/" in host_part:
            host_port, database_name = host_part.split("/", 1)
        else:
            host_port = host_part
            database_name = ""

        # Split host and port
        if ":" in host_port:
            host, port_str = host_port.rsplit(":", 1)
            port = int(port_str)
        else:
            host = host_port
            port = {"postgresql": 5432, "mysql": 3306, "mongodb": 27017}.get(database_type, 5432)

        return {
            "database_type": database_type,
            "host": host,
            "port": port,
            "database_name": database_name,
            "username": username,
            "password": password,
        }

    except Exception as e:
        raise ValueError(f"Invalid connection string format: {e}")
