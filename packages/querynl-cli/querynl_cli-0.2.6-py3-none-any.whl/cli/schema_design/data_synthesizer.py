"""Data synthesis interfaces and implementations for test data generation.

This module provides the IDataSynthesizer interface and implementations for generating
realistic sample data values based on column definitions and database types.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime

from ..models import ColumnGenerationConfig


class IDataSynthesizer(ABC):
    """Interface for generating realistic test data values.

    Implementations use Faker library to generate contextually appropriate
    data based on column names, data types, and constraints.
    """

    @abstractmethod
    def synthesize_value(
        self,
        column_config: ColumnGenerationConfig,
        row_index: int,
        context: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Generate a single value for a column.

        Args:
            column_config: Configuration for the column to generate data for
            row_index: Zero-based index of the row being generated (for uniqueness)
            context: Optional context with values from other columns in the same row
                    (e.g., for generating related data like matching first/last names)

        Returns:
            Generated value appropriate for the column's data type and constraints

        Raises:
            ValueError: If column_config is invalid or unsupported
        """
        pass

    @abstractmethod
    def synthesize_row(
        self,
        table_name: str,
        columns: List[ColumnGenerationConfig],
        row_index: int,
        foreign_key_values: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a complete row of data for a table.

        Args:
            table_name: Name of the table (used for contextual generation)
            columns: List of column configurations
            row_index: Zero-based index of the row being generated
            foreign_key_values: Optional dict of {column_name: value} for FK columns

        Returns:
            Dictionary mapping column names to generated values

        Raises:
            ValueError: If columns list is empty or invalid
        """
        pass

    @abstractmethod
    def validate_constraints(
        self,
        value: Any,
        column_config: ColumnGenerationConfig
    ) -> bool:
        """Validate that a generated value meets column constraints.

        Args:
            value: The generated value to validate
            column_config: Column configuration with constraints

        Returns:
            True if value meets all constraints, False otherwise
        """
        pass

    @abstractmethod
    def get_supported_data_types(self) -> List[str]:
        """Get list of supported database data types.

        Returns:
            List of data type strings (e.g., ['VARCHAR', 'INT', 'TIMESTAMP'])
        """
        pass


class FakerDataSynthesizer(IDataSynthesizer):
    """Faker-based implementation of IDataSynthesizer.

    Uses the Faker library to generate realistic sample data for various
    column types and constraints.
    """

    def __init__(self, locale: str = 'en_US', seed: Optional[int] = None):
        """Initialize FakerDataSynthesizer.

        Args:
            locale: Faker locale for data generation (default: en_US)
            seed: Optional random seed for reproducible generation
        """
        from faker import Faker
        import random

        self.fake = Faker(locale)
        if seed is not None:
            Faker.seed(seed)
            random.seed(seed)

        # Track unique values per column to avoid duplicates
        self._unique_trackers: Dict[str, set] = {}

        # Provider mapping for common column names
        self._column_name_hints = {
            'email': 'email',
            'name': 'name',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': 'phone_number',
            'phone_number': 'phone_number',
            'address': 'address',
            'street': 'street_address',
            'city': 'city',
            'state': 'state',
            'zip': 'zipcode',
            'zipcode': 'zipcode',
            'country': 'country',
            'company': 'company',
            'job': 'job',
            'title': 'job',
            'description': 'text',
            'bio': 'text',
            'url': 'url',
            'username': 'user_name',
            'password': 'password',
        }

    def synthesize_value(
        self,
        column_config: ColumnGenerationConfig,
        row_index: int,
        context: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Generate a single value for a column using Faker.

        Implements IDataSynthesizer.synthesize_value.
        """
        # Handle NULL values for nullable columns
        if column_config.is_nullable:
            import random
            if random.random() < column_config.null_probability:
                return None

        # Skip primary keys if auto-increment (handled by database)
        if column_config.is_primary_key and not column_config.faker_provider:
            return None

        # Handle foreign keys
        if column_config.is_foreign_key and column_config.foreign_key_config:
            # This should be handled by the caller providing the FK value
            # Return None here as placeholder
            return None

        # Get the Faker provider method
        provider_name = column_config.faker_provider
        if not provider_name:
            # Try to infer from column name
            column_lower = column_config.column_name.lower()
            provider_name = self._column_name_hints.get(column_lower, 'word')

        # Get the provider method
        if not hasattr(self.fake, provider_name):
            raise ValueError(f"Invalid Faker provider: {provider_name}")

        provider_method = getattr(self.fake, provider_name)
        params = column_config.provider_params or {}

        # Handle uniqueness constraint
        if column_config.is_unique:
            tracker_key = f"{column_config.column_name}"
            if tracker_key not in self._unique_trackers:
                self._unique_trackers[tracker_key] = set()

            max_attempts = 100
            for attempt in range(max_attempts):
                try:
                    value = provider_method(**params)

                    # For unique constraints, try using Faker's unique property
                    if value not in self._unique_trackers[tracker_key]:
                        self._unique_trackers[tracker_key].add(value)
                        return value
                except Exception:
                    pass

            # Fallback: append row index to ensure uniqueness
            import uuid
            base_value = provider_method(**params) if callable(provider_method) else str(provider_method)
            unique_value = f"{base_value}_{uuid.uuid4().hex[:8]}"
            self._unique_trackers[tracker_key].add(unique_value)
            return unique_value

        # Normal value generation
        try:
            return provider_method(**params)
        except TypeError:
            # Provider doesn't accept parameters
            return provider_method()

    def synthesize_row(
        self,
        table_name: str,
        columns: List[ColumnGenerationConfig],
        row_index: int,
        foreign_key_values: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a complete row of data for a table.

        Implements IDataSynthesizer.synthesize_row.
        """
        if not columns:
            raise ValueError(f"Cannot synthesize row for table '{table_name}': columns list is empty")

        row_data = {}
        fk_values = foreign_key_values or {}

        for column_config in columns:
            # Use provided FK value if available
            if column_config.is_foreign_key and column_config.column_name in fk_values:
                row_data[column_config.column_name] = fk_values[column_config.column_name]
            else:
                # Generate value
                value = self.synthesize_value(column_config, row_index, context=row_data)
                if value is not None:  # Only include non-None values (skips auto-increment PKs)
                    row_data[column_config.column_name] = value

        return row_data

    def validate_constraints(
        self,
        value: Any,
        column_config: ColumnGenerationConfig
    ) -> bool:
        """Validate that a generated value meets column constraints.

        Implements IDataSynthesizer.validate_constraints.
        """
        # Check nullable constraint
        if not column_config.is_nullable and value is None:
            return False

        # Check unique constraint (already handled during generation)
        if column_config.is_unique and value is not None:
            tracker_key = f"{column_config.column_name}"
            if tracker_key in self._unique_trackers:
                if value in self._unique_trackers[tracker_key]:
                    # Value already used
                    return False

        return True

    def get_supported_data_types(self) -> List[str]:
        """Get list of supported database data types.

        Implements IDataSynthesizer.get_supported_data_types.
        """
        return [
            'VARCHAR', 'CHAR', 'TEXT',
            'INT', 'INTEGER', 'BIGINT', 'SMALLINT', 'TINYINT',
            'FLOAT', 'DOUBLE', 'DECIMAL', 'NUMERIC',
            'BOOLEAN', 'BOOL',
            'DATE', 'DATETIME', 'TIMESTAMP', 'TIME',
            'UUID', 'GUID',
            'JSON', 'JSONB',
            'ENUM',
        ]

    def clear_unique_cache(self):
        """Clear the unique value trackers for fresh generation."""
        self._unique_trackers.clear()
        # Reset Faker's unique provider
        self.fake.unique.clear()
