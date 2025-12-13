"""
Data File Analysis

Analyzes uploaded CSV, Excel, and JSON files to infer schema structure, detect
entities, and identify relationships across files.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
import pandas as pd

from ..models import FileAnalysis, ColumnInfo, PotentialRelationship, UploadedFile
from . import (
    SchemaDesignError,
    FileTooLargeError,
    UnsupportedFileTypeError,
    FileParseError
)


# Maximum file size (100MB as per NFR-002)
MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024

# Sample size for type inference (first N rows)
SAMPLE_SIZE = 10000


class FileAnalyzer:
    """
    Analyzes data files to infer database schema structure.

    Supports CSV, Excel (.xlsx), and JSON formats. Performs:
    - Column type inference (maps pandas dtypes to database types)
    - Entity detection (identifies multiple entities in denormalized files)
    - Relationship detection (finds common columns across multiple files)
    """

    def __init__(self):
        """Initialize file analyzer."""
        self._uploaded_files: Dict[str, UploadedFile] = {}

    def analyze_file(self, file_path: str) -> UploadedFile:
        """
        Analyze a data file and return analysis results.

        Args:
            file_path: Path to the file to analyze

        Returns:
            UploadedFile with analysis results

        Raises:
            FileTooLargeError: File exceeds 100MB limit
            UnsupportedFileTypeError: File type not supported
            FileParseError: File cannot be parsed
        """
        path = Path(file_path).resolve()

        # Validate file exists
        if not path.exists():
            raise FileParseError(f"File not found: {file_path}")

        # Validate file size
        file_size = path.stat().st_size
        if file_size > MAX_FILE_SIZE_BYTES:
            size_mb = file_size / (1024 * 1024)
            raise FileTooLargeError(
                f"File size {size_mb:.1f}MB exceeds maximum of 100MB"
            )

        # Determine file type
        extension = path.suffix.lower()
        if extension == '.csv':
            file_type = 'csv'
            analysis = self.analyze_csv(path)
        elif extension in ['.xlsx', '.xls']:
            file_type = 'xlsx'
            analysis = self.analyze_excel(path)
        elif extension == '.json':
            file_type = 'json'
            analysis = self.analyze_json(path)
        else:
            raise UnsupportedFileTypeError(
                f"Unsupported file type: {extension}. "
                f"Supported types: .csv, .xlsx, .json"
            )

        # Create UploadedFile object
        uploaded_file = UploadedFile(
            file_path=str(path),
            file_name=path.name,
            file_type=file_type,
            file_size_bytes=file_size,
            analysis=analysis
        )

        # Store for relationship detection
        self._uploaded_files[uploaded_file.file_id] = uploaded_file

        # Detect relationships across all uploaded files
        self._detect_cross_file_relationships()

        return uploaded_file

    def analyze_csv(self, file_path: Path) -> FileAnalysis:
        """
        Analyze a CSV file.

        Args:
            file_path: Path to CSV file

        Returns:
            FileAnalysis with column information

        Raises:
            FileParseError: CSV cannot be parsed
        """
        try:
            # Try reading with different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            df = None

            for encoding in encodings:
                try:
                    df = pd.read_csv(
                        file_path,
                        nrows=SAMPLE_SIZE,
                        encoding=encoding
                    )
                    break
                except UnicodeDecodeError:
                    continue

            if df is None:
                raise FileParseError(
                    f"Could not read CSV with any supported encoding: {', '.join(encodings)}"
                )

            return self._analyze_dataframe(df, file_path.stem)

        except pd.errors.EmptyDataError:
            raise FileParseError("CSV file is empty")
        except pd.errors.ParserError as e:
            raise FileParseError(f"CSV parsing error: {str(e)}")
        except Exception as e:
            raise FileParseError(f"Error analyzing CSV: {str(e)}")

    def analyze_excel(self, file_path: Path) -> FileAnalysis:
        """
        Analyze an Excel file.

        Args:
            file_path: Path to Excel file

        Returns:
            FileAnalysis with column information

        Raises:
            FileParseError: Excel file cannot be parsed
        """
        try:
            # Read first sheet
            df = pd.read_excel(file_path, nrows=SAMPLE_SIZE)
            return self._analyze_dataframe(df, file_path.stem)

        except Exception as e:
            raise FileParseError(f"Error analyzing Excel file: {str(e)}")

    def analyze_json(self, file_path: Path) -> FileAnalysis:
        """
        Analyze a JSON file.

        Supports both array of objects and single object formats.

        Args:
            file_path: Path to JSON file

        Returns:
            FileAnalysis with column information

        Raises:
            FileParseError: JSON cannot be parsed
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Convert to DataFrame
            if isinstance(data, list):
                # Array of objects
                df = pd.DataFrame(data[:SAMPLE_SIZE])
            elif isinstance(data, dict):
                # Single object or nested structure
                # Flatten if necessary
                if all(isinstance(v, (list, dict)) for v in data.values()):
                    # Nested structure - take first level
                    df = pd.json_normalize(data)
                else:
                    # Single record
                    df = pd.DataFrame([data])
            else:
                raise FileParseError(
                    f"JSON must be an array of objects or a single object"
                )

            return self._analyze_dataframe(df, file_path.stem)

        except json.JSONDecodeError as e:
            raise FileParseError(f"Invalid JSON: {str(e)}")
        except Exception as e:
            raise FileParseError(f"Error analyzing JSON file: {str(e)}")

    def _analyze_dataframe(self, df: pd.DataFrame, base_name: str) -> FileAnalysis:
        """
        Analyze a pandas DataFrame and extract schema information.

        Args:
            df: DataFrame to analyze
            base_name: Base name for entity detection

        Returns:
            FileAnalysis with column and entity information
        """
        if df.empty:
            raise FileParseError("File contains no data rows")

        # Analyze columns
        columns = []
        for col_name in df.columns:
            col_info = self._analyze_column(df[col_name], col_name)
            columns.append(col_info)

        # Detect entities
        detected_entities = self.detect_entities(df, base_name)

        return FileAnalysis(
            row_count=len(df),
            column_count=len(df.columns),
            columns=columns,
            detected_entities=detected_entities,
            potential_relationships=[]  # Will be populated by cross-file analysis
        )

    def _analyze_column(self, series: pd.Series, col_name: str) -> ColumnInfo:
        """
        Analyze a single column and infer its database type.

        Args:
            series: Pandas series to analyze
            col_name: Column name

        Returns:
            ColumnInfo with type and statistics
        """
        # Get sample values (first 5 non-null values)
        sample_values = series.dropna().head(5).astype(str).tolist()

        # Infer database type
        inferred_type = self.infer_column_types(series)

        # Calculate statistics
        nullable = series.isnull().any()
        unique_count = series.nunique()

        return ColumnInfo(
            name=col_name,
            inferred_type=inferred_type,
            nullable=nullable,
            unique_values=unique_count,
            sample_values=sample_values
        )

    def infer_column_types(self, series: pd.Series) -> str:
        """
        Infer database column type from pandas Series.

        Maps pandas dtypes to generic database types:
        - object/string → VARCHAR/TEXT
        - int64 → INTEGER
        - float64 → DECIMAL/FLOAT
        - bool → BOOLEAN
        - datetime64 → TIMESTAMP
        - date → DATE

        Args:
            series: Pandas series to analyze

        Returns:
            Generic database type string
        """
        dtype = series.dtype

        # Check for datetime types
        if pd.api.types.is_datetime64_any_dtype(dtype):
            # Check if it's date-only or includes time
            if series.dropna().apply(lambda x: x.time() == pd.Timestamp('00:00:00').time()).all():
                return 'DATE'
            return 'TIMESTAMP'

        # Integer types
        if pd.api.types.is_integer_dtype(dtype):
            # Check if it could be a boolean (only 0 and 1)
            unique_values = series.dropna().unique()
            if len(unique_values) <= 2 and all(v in [0, 1] for v in unique_values):
                return 'BOOLEAN'

            # Check value range to determine integer size
            max_val = series.max()
            if max_val <= 32767:
                return 'SMALLINT'
            elif max_val <= 2147483647:
                return 'INTEGER'
            else:
                return 'BIGINT'

        # Float types
        if pd.api.types.is_float_dtype(dtype):
            return 'DECIMAL'

        # Boolean types
        if pd.api.types.is_bool_dtype(dtype):
            return 'BOOLEAN'

        # String/object types
        if pd.api.types.is_object_dtype(dtype):
            # Try to infer more specific types from content
            non_null = series.dropna()

            if len(non_null) == 0:
                return 'TEXT'

            # Check for date/datetime strings
            sample = non_null.head(100)
            try:
                pd.to_datetime(sample)
                return 'TIMESTAMP'
            except (ValueError, TypeError):
                pass

            # Check for numeric strings
            try:
                pd.to_numeric(sample)
                return 'DECIMAL'
            except (ValueError, TypeError):
                pass

            # Check string length to choose VARCHAR vs TEXT
            max_length = non_null.astype(str).str.len().max()
            if max_length <= 255:
                return f'VARCHAR({min(max_length * 2, 255)})'
            else:
                return 'TEXT'

        # Default to TEXT for unknown types
        return 'TEXT'

    def detect_entities(self, df: pd.DataFrame, base_name: str) -> List[str]:
        """
        Detect potential entity/table names from a DataFrame.

        For denormalized files, detects multiple entities based on:
        - Column name prefixes (e.g., customer_name, order_id)
        - Repeating column patterns
        - Foreign key indicators (columns ending in _id)

        Args:
            df: DataFrame to analyze
            base_name: Base name from filename

        Returns:
            List of detected entity/table names
        """
        entities = set()

        # Always include base name (from filename)
        # Normalize to plural form for table name
        base_entity = self._normalize_table_name(base_name)
        entities.add(base_entity)

        # Extract prefixes from column names
        # e.g., "customer_name" -> "customer"
        for col_name in df.columns:
            # Split on underscore
            parts = col_name.lower().split('_')

            # Look for common prefixes
            if len(parts) >= 2:
                prefix = parts[0]

                # Check if this looks like an entity prefix
                # (not a generic word like "is", "has", "total", etc.)
                generic_words = {'is', 'has', 'total', 'count', 'sum', 'avg', 'max', 'min', 'num', 'date', 'time'}

                if prefix not in generic_words and len(prefix) > 2:
                    # Check if multiple columns share this prefix
                    matching_cols = [c for c in df.columns if c.lower().startswith(prefix + '_')]
                    if len(matching_cols) >= 2:
                        entity_name = self._normalize_table_name(prefix)
                        entities.add(entity_name)

        # Look for foreign key patterns (columns ending in _id)
        for col_name in df.columns:
            if col_name.lower().endswith('_id'):
                # Extract entity name from column name
                # e.g., "customer_id" -> "customer"
                entity_name = col_name.lower()[:-3]  # Remove "_id"
                entity_name = self._normalize_table_name(entity_name)
                entities.add(entity_name)

        return sorted(list(entities))

    def _normalize_table_name(self, name: str) -> str:
        """
        Normalize a name to a valid table name.

        - Convert to lowercase
        - Replace spaces/hyphens with underscores
        - Remove special characters
        - Attempt to pluralize if not already plural

        Args:
            name: Name to normalize

        Returns:
            Normalized table name
        """
        # Convert to lowercase
        name = name.lower()

        # Replace spaces and hyphens with underscores
        name = re.sub(r'[\s\-]+', '_', name)

        # Remove special characters (keep only alphanumeric and underscore)
        name = re.sub(r'[^a-z0-9_]', '', name)

        # Simple pluralization (add 's' if not already plural-like)
        if not name.endswith('s') and not name.endswith('es') and not name.endswith('ies'):
            # Handle special cases
            if name.endswith('y'):
                name = name[:-1] + 'ies'
            elif name.endswith(('s', 'x', 'z', 'ch', 'sh')):
                name += 'es'
            else:
                name += 's'

        return name

    def detect_relationships(self, files: List[UploadedFile]) -> List[PotentialRelationship]:
        """
        Detect potential relationships across multiple uploaded files.

        Looks for:
        - Common column names (exact match)
        - Columns ending in _id that match other table names
        - Value overlap between columns (foreign key candidates)

        Args:
            files: List of uploaded files to analyze

        Returns:
            List of detected relationships
        """
        relationships = []

        if len(files) < 2:
            return relationships

        # Compare each pair of files
        for i, file1 in enumerate(files):
            for file2 in files[i+1:]:
                # Find common columns
                file1_cols = {col.name.lower(): col for col in file1.analysis.columns}
                file2_cols = {col.name.lower(): col for col in file2.analysis.columns}

                common_cols = set(file1_cols.keys()) & set(file2_cols.keys())

                for col_name in common_cols:
                    # Skip generic columns
                    if col_name in {'id', 'created_at', 'updated_at'}:
                        continue

                    col1 = file1_cols[col_name]
                    col2 = file2_cols[col_name]

                    # Check if types match
                    if col1.inferred_type == col2.inferred_type:
                        # High confidence for matching names and types
                        confidence = 0.8

                        # Higher confidence if one column has unique values (potential PK)
                        if col1.unique_values == file1.analysis.row_count or \
                           col2.unique_values == file2.analysis.row_count:
                            confidence = 0.9

                        relationships.append(PotentialRelationship(
                            from_column=col1.name,
                            to_file=file2.file_name,
                            to_column=col2.name,
                            confidence=confidence
                        ))

                # Look for foreign key patterns
                # e.g., "customer_id" in file1 and "customers" entity in file2
                for col_name, col in file1_cols.items():
                    if col_name.endswith('_id'):
                        entity_name = col_name[:-3]  # Remove "_id"

                        # Check if file2 entities match this entity name
                        for entity in file2.analysis.detected_entities:
                            if entity.startswith(entity_name) or entity_name in entity:
                                # Look for "id" column in file2
                                if 'id' in file2_cols:
                                    relationships.append(PotentialRelationship(
                                        from_column=col.name,
                                        to_file=file2.file_name,
                                        to_column='id',
                                        confidence=0.7
                                    ))

        return relationships

    def _detect_cross_file_relationships(self):
        """
        Detect relationships across all uploaded files and update their analyses.

        This is called after each file upload to update relationship information.
        """
        if len(self._uploaded_files) < 2:
            return

        files = list(self._uploaded_files.values())
        relationships = self.detect_relationships(files)

        # Group relationships by source file
        relationships_by_file = {}
        for rel in relationships:
            source_file = None
            for file in files:
                if any(col.name == rel.from_column for col in file.analysis.columns):
                    source_file = file
                    break

            if source_file:
                if source_file.file_id not in relationships_by_file:
                    relationships_by_file[source_file.file_id] = []
                relationships_by_file[source_file.file_id].append(rel)

        # Update each file's analysis with detected relationships
        for file_id, rels in relationships_by_file.items():
            self._uploaded_files[file_id].analysis.potential_relationships = rels
