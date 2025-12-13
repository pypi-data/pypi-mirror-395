"""
Data models for QueryNL CLI

Includes ConnectionProfile, SSHTunnel, and other entities from data-model.md
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, field_validator
import uuid


class SSHTunnel(BaseModel):
    """
    SSH tunnel configuration for remote database access.

    Used when database is behind SSH bastion or requires SSH forwarding.
    """
    ssh_host: str = Field(..., description="SSH server hostname or IP")
    ssh_port: int = Field(default=22, description="SSH server port")
    ssh_username: str = Field(..., description="SSH username")
    ssh_key_path: Optional[str] = Field(None, description="Path to SSH private key file")
    local_bind_port: Optional[int] = Field(None, description="Local port for tunnel (auto-assign if None)")
    remote_bind_host: str = Field(default="localhost", description="Remote database host from SSH perspective")
    remote_bind_port: int = Field(..., description="Remote database port")

    @field_validator("ssh_port", "remote_bind_port")
    @classmethod
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError("Port must be between 1 and 65535")
        return v


class ConnectionProfile(BaseModel):
    """
    Database connection configuration.

    Stores connection details (credentials stored separately in system keychain).
    """
    name: str = Field(..., description="Unique connection identifier")
    database_type: str = Field(..., description="Database type: postgresql, mysql, sqlite, mongodb")
    host: Optional[str] = Field(None, description="Database host/IP address")
    port: Optional[int] = Field(None, description="Database port")
    database_name: str = Field(..., description="Database/schema name")
    username: Optional[str] = Field(None, description="Database username")
    ssl_enabled: bool = Field(default=True, description="Use SSL/TLS connection")
    ssh_tunnel: Optional[SSHTunnel] = Field(None, description="SSH tunnel configuration")
    created_at: datetime = Field(default_factory=datetime.now, description="When connection was added")
    last_used: Optional[datetime] = Field(None, description="Last time connection was used")

    @field_validator("database_type")
    @classmethod
    def validate_database_type(cls, v):
        valid_types = ["postgresql", "mysql", "sqlite", "mongodb"]
        if v not in valid_types:
            raise ValueError(f"Database type must be one of: {', '.join(valid_types)}")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v or not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("Connection name must be alphanumeric (hyphens and underscores allowed)")
        if len(v) > 50:
            raise ValueError("Connection name must be 50 characters or less")
        return v

    @field_validator("port")
    @classmethod
    def validate_port(cls, v):
        if v is not None and not 1 <= v <= 65535:
            raise ValueError("Port must be between 1 and 65535")
        return v

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary for storage in config file.

        Returns:
            Dictionary representation (excludes credentials)
        """
        data = self.model_dump()
        # Ensure datetimes are ISO format strings
        if isinstance(data.get("created_at"), datetime):
            data["created_at"] = data["created_at"].isoformat()
        if isinstance(data.get("last_used"), datetime) and data["last_used"]:
            data["last_used"] = data["last_used"].isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConnectionProfile":
        """
        Create ConnectionProfile from dictionary.

        Args:
            data: Dictionary with connection data

        Returns:
            ConnectionProfile instance
        """
        # Parse datetime strings
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("last_used"), str) and data["last_used"]:
            data["last_used"] = datetime.fromisoformat(data["last_used"])

        return cls(**data)

    def get_connection_config(self, password: Optional[str] = None) -> Dict[str, Any]:
        """
        Get connection configuration for database driver.

        Args:
            password: Database password (retrieved from keychain)

        Returns:
            Dictionary with connection parameters
        """
        config = {
            "database_type": self.database_type,
            "database_name": self.database_name,
            "ssl_enabled": self.ssl_enabled,
        }

        if self.host:
            config["host"] = self.host

        if self.port:
            config["port"] = self.port

        if self.username:
            config["username"] = self.username

        if password:
            config["password"] = password

        return config


class REPLSession(BaseModel):
    """
    Interactive REPL session state.

    Tracks conversation context and session metadata for enhanced query experience.
    """
    session_id: str = Field(..., description="Unique session identifier (UUID)")
    connection_name: Optional[str] = Field(None, description="Active connection for this session")
    conversation_context: list[Dict[str, Any]] = Field(default_factory=list, description="Chat history (user/assistant messages)")
    last_result_rows: list[Dict[str, Any]] = Field(default_factory=list, description="Cached results from last query")
    started_at: datetime = Field(default_factory=datetime.now, description="Session start time")
    last_activity: datetime = Field(default_factory=datetime.now, description="Last user interaction time")

    def add_message(self, role: str, content: str) -> None:
        """
        Add message to conversation context.

        Args:
            role: Message role (user or assistant)
            content: Message content
        """
        self.conversation_context.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.last_activity = datetime.now()

    def update_results(self, rows: list[Dict[str, Any]]) -> None:
        """
        Update cached query results.

        Args:
            rows: Query result rows
        """
        self.last_result_rows = rows
        self.last_activity = datetime.now()

    def get_context_summary(self) -> str:
        """
        Get summarized conversation context for LLM.

        Returns:
            Formatted context string
        """
        if not self.conversation_context:
            return ""

        # Keep last 10 messages for context
        recent = self.conversation_context[-10:]
        lines = []
        for msg in recent:
            role = msg["role"].upper()
            content = msg["content"][:200]  # Truncate long messages
            lines.append(f"{role}: {content}")

        return "\n".join(lines)


class ColumnDefinition(BaseModel):
    """
    Column definition for schema design.

    Defines a single column within a table.
    """
    name: str = Field(..., description="Column name (valid SQL identifier)")
    type: str = Field(..., description="Data type (database-specific)")
    nullable: bool = Field(default=True, description="Whether column allows NULL")
    primary_key: bool = Field(default=False, description="Whether column is primary key")
    unique: bool = Field(default=False, description="Whether column has unique constraint")
    default_value: Optional[str] = Field(None, description="Default value expression")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v or not v.replace("_", "").isalnum():
            raise ValueError("Column name must be alphanumeric (underscores allowed)")
        return v


class Relationship(BaseModel):
    """
    Foreign key relationship between tables.

    Defines referential integrity constraints.
    """
    from_table: str = Field(..., description="Source table name")
    from_column: str = Field(..., description="Source column name")
    to_table: str = Field(..., description="Target table name")
    to_column: str = Field(..., description="Target column name")
    on_delete: str = Field(default="RESTRICT", description="ON DELETE action")
    on_update: str = Field(default="RESTRICT", description="ON UPDATE action")

    @field_validator("on_delete", "on_update")
    @classmethod
    def validate_action(cls, v):
        valid_actions = ["CASCADE", "SET NULL", "RESTRICT", "NO ACTION"]
        if v.upper() not in valid_actions:
            raise ValueError(f"Action must be one of: {', '.join(valid_actions)}")
        return v.upper()


class TableDesign(BaseModel):
    """
    Table definition for schema design.

    Defines structure of a single table.
    """
    name: str = Field(..., description="Table name (valid SQL identifier)")
    columns: list[ColumnDefinition] = Field(..., description="Column definitions")
    indexes: list[Dict[str, Any]] = Field(default_factory=list, description="Index definitions")
    constraints: list[Dict[str, Any]] = Field(default_factory=list, description="Additional constraints")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v or not v.replace("_", "").isalnum():
            raise ValueError("Table name must be alphanumeric (underscores allowed)")
        return v

    @field_validator("columns")
    @classmethod
    def validate_columns(cls, v):
        if not v:
            raise ValueError("Table must have at least one column")
        return v


class SchemaDesign(BaseModel):
    """
    Complete schema design from natural language.

    Represents a database schema with tables and relationships.
    """
    id: str = Field(..., description="Unique schema identifier")
    description: str = Field(..., description="Original natural language description")
    tables: list[TableDesign] = Field(..., description="Table definitions")
    relationships: list[Relationship] = Field(default_factory=list, description="Foreign key relationships")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    modified_at: datetime = Field(default_factory=datetime.now, description="Last modification timestamp")
    version: int = Field(default=1, description="Schema version number")

    @field_validator("tables")
    @classmethod
    def validate_tables(cls, v):
        if not v:
            raise ValueError("Schema must have at least one table")
        return v

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = self.model_dump()
        # Ensure datetimes are ISO format strings
        if isinstance(data.get("created_at"), datetime):
            data["created_at"] = data["created_at"].isoformat()
        if isinstance(data.get("modified_at"), datetime):
            data["modified_at"] = data["modified_at"].isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SchemaDesign":
        """Create SchemaDesign from dictionary"""
        # Parse datetime strings
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("modified_at"), str):
            data["modified_at"] = datetime.fromisoformat(data["modified_at"])
        return cls(**data)


class MigrationRecord(BaseModel):
    """
    Migration tracking record.

    Tracks database migrations with up/down SQL and execution status.
    """
    migration_id: str = Field(..., description="Unique migration identifier (timestamp-based)")
    connection_name: str = Field(..., description="Connection where migration was/will be applied")
    framework: str = Field(default="raw", description="Migration framework (alembic, flyway, raw)")
    direction: str = Field(default="up", description="Migration direction (up, down)")
    sql_content: str = Field(..., description="Migration SQL content")
    rollback_sql: Optional[str] = Field(None, description="Rollback SQL for down migration")
    description: str = Field(default="", description="Migration description/message")
    applied_at: Optional[datetime] = Field(None, description="When migration was applied")
    status: str = Field(default="pending", description="Migration status (pending, applied, failed)")
    error_message: Optional[str] = Field(None, description="Error message if failed")

    @field_validator("framework")
    @classmethod
    def validate_framework(cls, v):
        valid_frameworks = ["alembic", "flyway", "raw"]
        if v not in valid_frameworks:
            raise ValueError(f"Framework must be one of: {', '.join(valid_frameworks)}")
        return v

    @field_validator("direction")
    @classmethod
    def validate_direction(cls, v):
        valid_directions = ["up", "down"]
        if v not in valid_directions:
            raise ValueError(f"Direction must be one of: {', '.join(valid_directions)}")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        valid_statuses = ["pending", "applied", "failed"]
        if v not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return v

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        data = self.model_dump()
        if isinstance(data.get("applied_at"), datetime) and data["applied_at"]:
            data["applied_at"] = data["applied_at"].isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MigrationRecord":
        """Create MigrationRecord from dictionary"""
        if isinstance(data.get("applied_at"), str) and data["applied_at"]:
            data["applied_at"] = datetime.fromisoformat(data["applied_at"])
        return cls(**data)


# Schema Design Feature Models (Feature 004)


class ConversationTurn(BaseModel):
    """
    A single exchange in the schema design conversation.

    Part of the schema design session conversation history.
    """
    turn_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique turn identifier")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the turn occurred")
    role: str = Field(..., description="Role: user or assistant")
    content: str = Field(..., description="Message content")
    intent: Optional[str] = Field(None, description="Intent classification")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata (tokens, latency, etc)")

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        if v not in ["user", "assistant"]:
            raise ValueError("Role must be 'user' or 'assistant'")
        return v

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = self.model_dump()
        if isinstance(data.get("timestamp"), datetime):
            data["timestamp"] = data["timestamp"].isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConversationTurn":
        """Create from dictionary"""
        if isinstance(data.get("timestamp"), str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)


class SchemaColumn(BaseModel):
    """Column definition within a schema table."""
    name: str = Field(..., description="Column name")
    data_type: str = Field(..., description="Database-specific data type")
    constraints: List[str] = Field(default_factory=list, description="Constraints (PRIMARY KEY, NOT NULL, etc)")
    default_value: Optional[str] = Field(None, description="Default value")
    description: Optional[str] = Field(None, description="Rationale for this column")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SchemaColumn":
        """Create from dictionary"""
        return cls(**data)


class SchemaIndex(BaseModel):
    """Index definition for a schema table."""
    name: str = Field(..., description="Index name")
    columns: List[str] = Field(..., description="Columns in the index")
    type: str = Field(default="btree", description="Index type")
    unique: bool = Field(default=False, description="Whether index is unique")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SchemaIndex":
        """Create from dictionary"""
        return cls(**data)


class SchemaConstraint(BaseModel):
    """Additional constraint for a schema table."""
    type: str = Field(..., description="Constraint type (FOREIGN KEY, CHECK, UNIQUE)")
    definition: str = Field(..., description="SQL constraint definition")
    description: Optional[str] = Field(None, description="Rationale for constraint")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SchemaConstraint":
        """Create from dictionary"""
        return cls(**data)


class SchemaTable(BaseModel):
    """Table definition within a schema proposal."""
    name: str = Field(..., description="Table name")
    columns: List[SchemaColumn] = Field(..., description="Column definitions")
    indexes: List[SchemaIndex] = Field(default_factory=list, description="Index definitions")
    constraints: List[SchemaConstraint] = Field(default_factory=list, description="Additional constraints")
    description: Optional[str] = Field(None, description="Purpose of this table")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = self.model_dump()
        data["columns"] = [col.to_dict() for col in self.columns]
        data["indexes"] = [idx.to_dict() for idx in self.indexes]
        data["constraints"] = [con.to_dict() for con in self.constraints]
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SchemaTable":
        """Create from dictionary"""
        if "columns" in data:
            data["columns"] = [SchemaColumn.from_dict(c) if isinstance(c, dict) else c for c in data["columns"]]
        if "indexes" in data:
            data["indexes"] = [SchemaIndex.from_dict(i) if isinstance(i, dict) else i for i in data.get("indexes", [])]
        if "constraints" in data:
            data["constraints"] = [SchemaConstraint.from_dict(c) if isinstance(c, dict) else c for c in data.get("constraints", [])]
        return cls(**data)


class SchemaRelationship(BaseModel):
    """Relationship between schema tables."""
    from_table: str = Field(..., description="Source table")
    to_table: str = Field(..., description="Target table")
    type: str = Field(..., description="Relationship type (one-to-one, one-to-many, many-to-many)")
    foreign_key: str = Field(..., description="Foreign key column name")
    junction_table: Optional[str] = Field(None, description="Junction table for many-to-many")
    description: Optional[str] = Field(None, description="Relationship rationale")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SchemaRelationship":
        """Create from dictionary"""
        return cls(**data)


class SchemaProposal(BaseModel):
    """
    Complete database schema proposal with rationale.

    Represents a versioned schema design with all tables, relationships, and design decisions.
    """
    version: int = Field(..., description="Schema version (1-indexed)")
    created_at: datetime = Field(default_factory=datetime.now, description="When this version was created")
    database_type: str = Field(..., description="Target database type")
    normalization_level: str = Field(default="3NF", description="Normalization level")
    tables: List[SchemaTable] = Field(..., description="Table definitions")
    relationships: List[SchemaRelationship] = Field(default_factory=list, description="Table relationships")
    rationale: str = Field(..., description="Overall design decisions and trade-offs")
    warnings: List[str] = Field(default_factory=list, description="Potential issues or considerations")

    @field_validator("database_type")
    @classmethod
    def validate_database_type(cls, v):
        valid_types = ["postgresql", "mysql", "sqlite", "mongodb"]
        if v not in valid_types:
            raise ValueError(f"Database type must be one of: {', '.join(valid_types)}")
        return v

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = self.model_dump()
        if isinstance(data.get("created_at"), datetime):
            data["created_at"] = data["created_at"].isoformat()
        data["tables"] = [table.to_dict() for table in self.tables]
        data["relationships"] = [rel.to_dict() for rel in self.relationships]
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SchemaProposal":
        """Create from dictionary"""
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if "tables" in data:
            data["tables"] = [SchemaTable.from_dict(t) if isinstance(t, dict) else t for t in data["tables"]]
        if "relationships" in data:
            data["relationships"] = [SchemaRelationship.from_dict(r) if isinstance(r, dict) else r for r in data.get("relationships", [])]
        return cls(**data)


class ColumnInfo(BaseModel):
    """Column information from file analysis."""
    name: str = Field(..., description="Column name")
    inferred_type: str = Field(..., description="Inferred data type")
    nullable: bool = Field(default=True, description="Whether column has null values")
    unique_values: int = Field(..., description="Number of unique values")
    sample_values: List[str] = Field(default_factory=list, description="Sample values")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ColumnInfo":
        """Create from dictionary"""
        return cls(**data)


class PotentialRelationship(BaseModel):
    """Potential relationship detected between files."""
    from_column: str = Field(..., description="Source column")
    to_file: str = Field(..., description="Target file")
    to_column: str = Field(..., description="Target column")
    confidence: float = Field(..., description="Confidence score (0.0-1.0)")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PotentialRelationship":
        """Create from dictionary"""
        return cls(**data)


class FileAnalysis(BaseModel):
    """Analysis results from uploaded data file."""
    row_count: int = Field(..., description="Number of rows")
    column_count: int = Field(..., description="Number of columns")
    columns: List[ColumnInfo] = Field(..., description="Column analysis")
    detected_entities: List[str] = Field(default_factory=list, description="Inferred table names")
    potential_relationships: List[PotentialRelationship] = Field(default_factory=list, description="Detected relationships")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = self.model_dump()
        data["columns"] = [col.to_dict() for col in self.columns]
        data["potential_relationships"] = [rel.to_dict() for rel in self.potential_relationships]
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FileAnalysis":
        """Create from dictionary"""
        if "columns" in data:
            data["columns"] = [ColumnInfo.from_dict(c) if isinstance(c, dict) else c for c in data["columns"]]
        if "potential_relationships" in data:
            data["potential_relationships"] = [PotentialRelationship.from_dict(r) if isinstance(r, dict) else r for r in data.get("potential_relationships", [])]
        return cls(**data)


class UploadedFile(BaseModel):
    """Uploaded data file with analysis results."""
    file_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique file identifier")
    file_path: str = Field(..., description="Absolute file path")
    file_name: str = Field(..., description="File basename")
    file_type: str = Field(..., description="File type (csv, xlsx, json)")
    file_size_bytes: int = Field(..., description="File size in bytes")
    uploaded_at: datetime = Field(default_factory=datetime.now, description="Upload timestamp")
    analysis: FileAnalysis = Field(..., description="File analysis results")
    used_in_schema: bool = Field(default=False, description="Whether file influenced current schema")

    @field_validator("file_type")
    @classmethod
    def validate_file_type(cls, v):
        valid_types = ["csv", "xlsx", "json"]
        if v not in valid_types:
            raise ValueError(f"File type must be one of: {', '.join(valid_types)}")
        return v

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = self.model_dump()
        if isinstance(data.get("uploaded_at"), datetime):
            data["uploaded_at"] = data["uploaded_at"].isoformat()
        data["analysis"] = self.analysis.to_dict()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UploadedFile":
        """Create from dictionary"""
        if isinstance(data.get("uploaded_at"), str):
            data["uploaded_at"] = datetime.fromisoformat(data["uploaded_at"])
        if isinstance(data.get("analysis"), dict):
            data["analysis"] = FileAnalysis.from_dict(data["analysis"])
        return cls(**data)


class SchemaDesignSession(BaseModel):
    """
    Schema design session with conversation history and version tracking.

    Manages the complete state of a schema design session including conversation context,
    schema versions, and uploaded files.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique session identifier")
    name: Optional[str] = Field(None, description="User-assigned name")
    created_at: datetime = Field(default_factory=datetime.now, description="Session creation time")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last modification time")
    status: str = Field(default="active", description="Session status")
    conversation_history: List[ConversationTurn] = Field(default_factory=list, description="Conversation turns")
    current_schema: Optional[SchemaProposal] = Field(None, description="Current schema proposal")
    schema_versions: List[SchemaProposal] = Field(default_factory=list, description="Version history")
    uploaded_files: List[UploadedFile] = Field(default_factory=list, description="Uploaded files")
    database_type: Optional[str] = Field(None, description="Target database type")
    target_database_name: Optional[str] = Field(None, description="Target database name")
    expires_at: datetime = Field(default_factory=lambda: datetime.now() + timedelta(days=90), description="Expiration date")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        valid_statuses = ["active", "finalized", "implemented"]
        if v not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return v

    @field_validator("database_type")
    @classmethod
    def validate_database_type(cls, v):
        if v is not None:
            valid_types = ["postgresql", "mysql", "sqlite", "mongodb"]
            if v not in valid_types:
                raise ValueError(f"Database type must be one of: {', '.join(valid_types)}")
        return v

    def add_conversation_turn(self, role: str, content: str, intent: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> ConversationTurn:
        """Add a conversation turn and update session."""
        turn = ConversationTurn(
            role=role,
            content=content,
            intent=intent,
            metadata=metadata or {}
        )
        self.conversation_history.append(turn)
        self.updated_at = datetime.now()
        return turn

    def add_schema_version(self, schema: SchemaProposal) -> None:
        """Add a new schema version."""
        schema.version = len(self.schema_versions) + 1
        self.schema_versions.append(schema)
        self.current_schema = schema
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization and database storage"""
        data = self.model_dump()
        if isinstance(data.get("created_at"), datetime):
            data["created_at"] = data["created_at"].isoformat()
        if isinstance(data.get("updated_at"), datetime):
            data["updated_at"] = data["updated_at"].isoformat()
        if isinstance(data.get("expires_at"), datetime):
            data["expires_at"] = data["expires_at"].isoformat()

        data["conversation_history"] = [turn.to_dict() for turn in self.conversation_history]
        data["schema_versions"] = [schema.to_dict() for schema in self.schema_versions]
        data["uploaded_files"] = [file.to_dict() for file in self.uploaded_files]
        if self.current_schema:
            data["current_schema"] = self.current_schema.to_dict()

        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SchemaDesignSession":
        """Create from dictionary"""
        # Parse datetime strings
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("updated_at"), str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        if isinstance(data.get("expires_at"), str):
            data["expires_at"] = datetime.fromisoformat(data["expires_at"])

        # Parse nested objects
        if "conversation_history" in data:
            data["conversation_history"] = [
                ConversationTurn.from_dict(t) if isinstance(t, dict) else t
                for t in data["conversation_history"]
            ]
        if "schema_versions" in data:
            data["schema_versions"] = [
                SchemaProposal.from_dict(s) if isinstance(s, dict) else s
                for s in data["schema_versions"]
            ]
        if "uploaded_files" in data:
            data["uploaded_files"] = [
                UploadedFile.from_dict(f) if isinstance(f, dict) else f
                for f in data["uploaded_files"]
            ]
        if data.get("current_schema") and isinstance(data["current_schema"], dict):
            data["current_schema"] = SchemaProposal.from_dict(data["current_schema"])

        return cls(**data)


# Test Data Generation Models (Feature 005 - add-test-data)


from enum import Enum


class ErrorType(str, Enum):
    """Classification of insertion errors for test data generation."""
    CONSTRAINT_VIOLATION = "constraint_violation"
    FOREIGN_KEY_VIOLATION = "foreign_key_violation"
    SYNTAX_ERROR = "syntax_error"
    TIMEOUT = "timeout"
    CONNECTION_ERROR = "connection_error"
    UNKNOWN = "unknown"


class TestDataRequest(BaseModel):
    """
    User's request to generate test data.

    Parsed from natural language input like "add 100 users" or "add sample data".
    """
    user_query: str = Field(..., description="Original natural language query")
    target_tables: Optional[List[str]] = Field(None, description="Specific tables to populate (None = all)")
    record_counts: Optional[Dict[str, int]] = Field(None, description="Explicit counts per table")
    domain_context: Optional[str] = Field(None, description="Domain context for realistic data (e.g., 'e-commerce')")
    database_type: str = Field(..., description="Target database type")

    @field_validator("database_type")
    @classmethod
    def validate_database_type(cls, v):
        valid_types = ["mysql", "postgresql", "sqlite"]
        if v not in valid_types:
            raise ValueError(f"Database type must be one of: {', '.join(valid_types)}")
        return v

    @field_validator("record_counts")
    @classmethod
    def validate_record_counts(cls, v):
        if v:
            for table, count in v.items():
                if count <= 0:
                    raise ValueError(f"Record count for {table} must be positive")
        return v


class ForeignKeyConfig(BaseModel):
    """Foreign key resolution configuration."""
    referenced_table: str = Field(..., description="Parent table name")
    referenced_column: str = Field(..., description="Parent column name")
    selection_strategy: str = Field(default="random", description="How to select FK values")

    @field_validator("selection_strategy")
    @classmethod
    def validate_strategy(cls, v):
        valid_strategies = ["random", "sequential", "weighted"]
        if v not in valid_strategies:
            raise ValueError(f"Selection strategy must be one of: {', '.join(valid_strategies)}")
        return v


class ColumnGenerationConfig(BaseModel):
    """Configuration for generating data for a single column."""
    column_name: str = Field(..., description="Column name")
    faker_provider: str = Field(..., description="Faker method name")
    provider_params: Dict[str, Any] = Field(default_factory=dict, description="Parameters for Faker method")
    is_primary_key: bool = Field(default=False, description="Whether this is a primary key")
    is_foreign_key: bool = Field(default=False, description="Whether this references another table")
    foreign_key_config: Optional[ForeignKeyConfig] = Field(None, description="FK resolution config")
    foreign_key_table: Optional[str] = Field(None, description="Referenced table name (convenience field)")
    foreign_key_column: Optional[str] = Field(None, description="Referenced column name (convenience field)")
    is_unique: bool = Field(default=False, description="Whether unique constraint applies")
    is_nullable: bool = Field(default=False, description="Whether NULL values allowed")
    null_probability: float = Field(default=0.0, ge=0.0, le=1.0, description="Probability of NULL if nullable")


class TableGenerationConfig(BaseModel):
    """Configuration for generating data for a single table."""
    table_name: str = Field(..., description="Target table name")
    record_count: int = Field(..., gt=0, description="Number of records to generate")
    columns: List[ColumnGenerationConfig] = Field(..., description="Per-column configuration")


class DataGenerationPlan(BaseModel):
    """
    LLM-generated plan for test data generation.

    Specifies HOW to generate data (not the actual SQL).
    """
    plan_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique plan identifier")
    created_at: datetime = Field(default_factory=datetime.now, description="Plan creation timestamp")
    database_type: str = Field(..., description="Target database type")
    tables: List[TableGenerationConfig] = Field(..., description="Per-table generation config")
    insertion_order: List[str] = Field(..., description="Table names in dependency order")
    rationale: str = Field(..., description="Human-readable explanation of strategy")
    estimated_total_records: int = Field(..., description="Total records to generate")

    @field_validator("database_type")
    @classmethod
    def validate_database_type(cls, v):
        valid_types = ["mysql", "postgresql", "sqlite"]
        if v not in valid_types:
            raise ValueError(f"Database type must be one of: {', '.join(valid_types)}")
        return v

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = self.model_dump()
        if isinstance(data.get("created_at"), datetime):
            data["created_at"] = data["created_at"].isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DataGenerationPlan":
        """Create from dictionary"""
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)


class InsertionError(BaseModel):
    """Details of a failed record insertion."""
    table_name: str = Field(..., description="Table where error occurred")
    batch_id: str = Field(..., description="Batch identifier")
    record_index: Optional[int] = Field(None, description="Index of failed record in batch")
    error_type: ErrorType = Field(..., description="Error classification")
    constraint_name: Optional[str] = Field(None, description="Violated constraint name")
    column_name: Optional[str] = Field(None, description="Column causing error")
    error_message: str = Field(..., description="Detailed error message")
    failed_record: Optional[Dict[str, Any]] = Field(None, description="The record that failed")


class TableInsertionResult(BaseModel):
    """Results of inserting data into a single table."""
    table_name: str = Field(..., description="Table name")
    records_inserted: int = Field(..., description="Successfully inserted records")
    records_failed: int = Field(..., description="Failed insertions")
    insertion_duration_seconds: float = Field(..., description="Time spent on this table")


class InsertionResult(BaseModel):
    """
    Complete results of test data generation operation.

    Includes success/failure statistics and detailed error information.
    """
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Request identifier")
    started_at: datetime = Field(default_factory=datetime.now, description="Operation start time")
    completed_at: datetime = Field(default_factory=datetime.now, description="Operation completion time")
    duration_seconds: float = Field(..., description="Total operation duration")
    total_records_requested: int = Field(..., description="Total records requested")
    total_records_inserted: int = Field(..., description="Successfully inserted records")
    total_records_failed: int = Field(..., description="Failed insertions")
    table_results: Dict[str, TableInsertionResult] = Field(default_factory=dict, description="Per-table results")
    errors: List[InsertionError] = Field(default_factory=list, description="Detailed error information")
    cancelled_by_user: bool = Field(default=False, description="Whether operation was cancelled")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = self.model_dump()
        if isinstance(data.get("started_at"), datetime):
            data["started_at"] = data["started_at"].isoformat()
        if isinstance(data.get("completed_at"), datetime):
            data["completed_at"] = data["completed_at"].isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InsertionResult":
        """Create from dictionary"""
        if isinstance(data.get("started_at"), str):
            data["started_at"] = datetime.fromisoformat(data["started_at"])
        if isinstance(data.get("completed_at"), str):
            data["completed_at"] = datetime.fromisoformat(data["completed_at"])
        return cls(**data)


class ProgressUpdate(BaseModel):
    """Progress update during test data generation."""
    current_table: str = Field(..., description="Table currently being processed")
    table_number: int = Field(..., description="Current table number")
    total_tables: int = Field(..., description="Total number of tables")
    records_completed: int = Field(..., description="Records completed so far")
    records_total: int = Field(..., description="Total records to generate")
    estimated_seconds_remaining: float = Field(..., description="Estimated time remaining")
    current_speed_records_per_sec: float = Field(..., description="Current generation speed")


class CancellationToken:
    """Token for checking if user cancelled operation."""

    def __init__(self):
        self._cancelled = False

    def cancel(self):
        """Mark operation as cancelled."""
        self._cancelled = True

    def is_cancelled(self) -> bool:
        """Check if operation was cancelled."""
        return self._cancelled

    def reset(self):
        """Reset cancellation state."""
        self._cancelled = False
