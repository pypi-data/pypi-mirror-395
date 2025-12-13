"""Test data generation orchestration interface and implementations.

This module provides the ITestDataGenerator interface and implementations for orchestrating
the complete test data generation workflow from user request to execution.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

from ..models import (
    TestDataRequest,
    DataGenerationPlan,
    InsertionResult,
    ProgressUpdate,
    CancellationToken
)


class ITestDataGenerator(ABC):
    """Interface for orchestrating test data generation.

    This is the main entry point for the test data generation feature.
    Implementations coordinate between schema introspection, LLM planning,
    data synthesis, and insertion execution.
    """

    @abstractmethod
    def generate_test_data(
        self,
        request: TestDataRequest,
        connection: Any,
        progress_callback: Optional[Callable[[ProgressUpdate], None]] = None,
        cancellation_token: Optional[CancellationToken] = None
    ) -> InsertionResult:
        """Generate and insert test data based on user request.

        This is the main orchestration method that:
        1. Introspects the database schema
        2. Generates a data generation plan using LLM
        3. Synthesizes realistic data values
        4. Executes batch INSERT operations
        5. Returns complete results with statistics

        Args:
            request: User's test data generation request
            connection: Database connection object (DB-API 2.0 compatible)
            progress_callback: Optional callback for progress updates
            cancellation_token: Optional token for checking user cancellation

        Returns:
            InsertionResult with complete execution statistics, errors, and metadata

        Raises:
            ConnectionError: If database connection fails
            ValueError: If request is invalid or schema is incompatible
            LLMError: If LLM service fails to generate plan
        """
        pass

    @abstractmethod
    def create_generation_plan(
        self,
        request: TestDataRequest,
        schema_metadata: dict,
        llm_service: Any
    ) -> DataGenerationPlan:
        """Create a data generation plan using LLM.

        Args:
            request: User's test data generation request
            schema_metadata: Database schema metadata (tables, columns, constraints)
            llm_service: LLM service instance for plan generation

        Returns:
            DataGenerationPlan with table configs, insertion order, and rationale

        Raises:
            ValueError: If schema_metadata is invalid or incomplete
            LLMError: If LLM service fails or returns invalid plan
        """
        pass

    @abstractmethod
    def introspect_schema(
        self,
        connection: Any,
        database_type: str,
        target_tables: Optional[list] = None
    ) -> dict:
        """Introspect database schema to get metadata.

        Args:
            connection: Database connection object
            database_type: Database type ('mysql', 'postgresql', 'sqlite')
            target_tables: Optional list of specific tables to introspect (None = all)

        Returns:
            Dictionary with schema metadata including:
            - tables: List of table names
            - columns: Dict mapping table names to column definitions
            - constraints: Dict mapping table names to constraint definitions
            - foreign_keys: Dict mapping table names to FK relationships

        Raises:
            ConnectionError: If database introspection fails
            ValueError: If database_type is unsupported
        """
        pass

    @abstractmethod
    def validate_plan(
        self,
        plan: DataGenerationPlan,
        schema_metadata: dict
    ) -> tuple[bool, list[str]]:
        """Validate that a generation plan is compatible with schema.

        Args:
            plan: The data generation plan to validate
            schema_metadata: Database schema metadata from introspection

        Returns:
            Tuple of (is_valid, error_messages)
            - is_valid: True if plan is valid, False otherwise
            - error_messages: List of validation error messages (empty if valid)
        """
        pass

    @abstractmethod
    def estimate_duration(
        self,
        plan: DataGenerationPlan,
        database_type: str
    ) -> float:
        """Estimate execution duration in seconds.

        Args:
            plan: The data generation plan to estimate
            database_type: Target database type

        Returns:
            Estimated duration in seconds (rough estimate based on record counts)
        """
        pass

    @abstractmethod
    def preview_sample_data(
        self,
        plan: DataGenerationPlan,
        table_name: str,
        num_rows: int = 5
    ) -> list[dict]:
        """Generate sample rows for preview without inserting.

        Args:
            plan: The data generation plan
            table_name: Name of the table to preview
            num_rows: Number of sample rows to generate (default 5)

        Returns:
            List of row dictionaries showing sample data

        Raises:
            ValueError: If table_name not in plan or num_rows invalid
        """
        pass


class TestDataGenerator(ITestDataGenerator):
    """Implementation of test data generator with LLM-based planning."""

    def __init__(self, llm_service: Any, data_synthesizer: Any, insertion_executor: Any):
        """Initialize TestDataGenerator.

        Args:
            llm_service: LLM service instance for plan generation
            data_synthesizer: IDataSynthesizer implementation
            insertion_executor: IInsertionExecutor implementation
        """
        self.llm_service = llm_service
        self.data_synthesizer = data_synthesizer
        self.insertion_executor = insertion_executor

    def generate_test_data(
        self,
        request: TestDataRequest,
        connection: Any,
        progress_callback: Optional[Callable[[ProgressUpdate], None]] = None,
        cancellation_token: Optional[CancellationToken] = None
    ) -> InsertionResult:
        """Generate and insert test data based on user request.

        Implements ITestDataGenerator.generate_test_data.
        """
        # Check if connection is SQLAlchemy engine
        from sqlalchemy.engine import Engine

        if isinstance(connection, Engine):
            # Use engine for introspection
            engine = connection
            # Get raw connection for insertions
            raw_connection = engine.raw_connection()
        else:
            # Assume it's already a raw connection
            raw_connection = connection
            engine = connection

        # Step 1: Introspect schema (use engine)
        schema_metadata = self.introspect_schema(
            connection=engine,
            database_type=request.database_type,
            target_tables=request.target_tables
        )

        # Step 2: Generate plan using LLM
        plan = self.create_generation_plan(
            request=request,
            schema_metadata=schema_metadata,
            llm_service=self.llm_service
        )

        # Step 3: Validate plan
        is_valid, errors = self.validate_plan(plan, schema_metadata)
        if not is_valid:
            raise ValueError(f"Generated plan is invalid: {'; '.join(errors)}")

        # Step 4: Synthesize data for all tables
        data_rows = {}
        foreign_key_tracker = {}  # Track generated PKs for FK resolution

        for table_config in plan.tables:
            table_name = table_config.table_name
            rows = []

            for row_index in range(table_config.record_count):
                # Check for cancellation
                if cancellation_token and cancellation_token.is_cancelled():
                    break

                # Prepare FK values for this row
                fk_values = {}
                for column_config in table_config.columns:
                    if column_config.is_foreign_key and column_config.foreign_key_table:
                        # Select random FK value from parent table
                        parent_table = column_config.foreign_key_table
                        if parent_table in foreign_key_tracker and foreign_key_tracker[parent_table]:
                            import random
                            fk_values[column_config.column_name] = random.choice(
                                foreign_key_tracker[parent_table]
                            )

                # Generate row
                row_data = self.data_synthesizer.synthesize_row(
                    table_name=table_name,
                    columns=table_config.columns,
                    row_index=row_index,
                    foreign_key_values=fk_values
                )
                rows.append(row_data)

                # Track PK values for FK resolution
                for column_config in table_config.columns:
                    if column_config.is_primary_key and column_config.column_name in row_data:
                        if table_name not in foreign_key_tracker:
                            foreign_key_tracker[table_name] = []
                        foreign_key_tracker[table_name].append(row_data[column_config.column_name])

            data_rows[table_name] = rows

        # Step 5: Execute insertion plan (use raw connection)
        result = self.insertion_executor.execute_insertion_plan(
            plan=plan,
            connection=raw_connection,
            data_rows=data_rows,
            progress_callback=progress_callback,
            cancellation_token=cancellation_token
        )

        return result

    def create_generation_plan(
        self,
        request: TestDataRequest,
        schema_metadata: dict,
        llm_service: Any
    ) -> DataGenerationPlan:
        """Create a data generation plan using LLM.

        Implements ITestDataGenerator.create_generation_plan.
        """
        from ..models import DataGenerationPlan, TableGenerationConfig, ColumnGenerationConfig
        import json
        import uuid
        from datetime import datetime

        # Build LLM prompt
        prompt = self._build_plan_prompt(request, schema_metadata)

        # Call LLM
        try:
            llm_response = llm_service.generate_completion(prompt)

            # Parse JSON response
            plan_data = json.loads(llm_response)

            # Convert to Pydantic models
            tables = []
            for table_data in plan_data.get('tables', []):
                columns = []
                for col_data in table_data.get('columns', []):
                    column_config = ColumnGenerationConfig(
                        column_name=col_data['column_name'],
                        faker_provider=col_data.get('faker_provider', 'word'),
                        provider_params=col_data.get('provider_params', {}),
                        is_primary_key=col_data.get('is_primary_key', False),
                        is_foreign_key=col_data.get('is_foreign_key', False),
                        foreign_key_table=col_data.get('foreign_key_table'),
                        foreign_key_column=col_data.get('foreign_key_column'),
                        is_unique=col_data.get('is_unique', False),
                        is_nullable=col_data.get('is_nullable', False),
                        null_probability=col_data.get('null_probability', 0.15)
                    )
                    columns.append(column_config)

                table_config = TableGenerationConfig(
                    table_name=table_data['table_name'],
                    record_count=table_data.get('record_count', 15),
                    columns=columns
                )
                tables.append(table_config)

            # Calculate insertion order using topological sort
            insertion_order = self._calculate_insertion_order(tables, schema_metadata)

            # Calculate total records
            total_records = sum(t.record_count for t in tables)

            plan = DataGenerationPlan(
                plan_id=str(uuid.uuid4()),
                created_at=datetime.now(),
                database_type=request.database_type,
                tables=tables,
                insertion_order=insertion_order,
                rationale=plan_data.get('rationale', 'LLM-generated test data plan'),
                estimated_total_records=total_records
            )

            return plan

        except Exception as e:
            # Fallback to rule-based plan if LLM fails
            return self._create_fallback_plan(request, schema_metadata)

    def introspect_schema(
        self,
        connection: Any,
        database_type: str,
        target_tables: Optional[list] = None
    ) -> dict:
        """Introspect database schema to get metadata.

        Implements ITestDataGenerator.introspect_schema.
        """
        from sqlalchemy import inspect, MetaData

        # Use SQLAlchemy inspector
        inspector = inspect(connection)

        schema_metadata = {
            'tables': [],
            'columns': {},
            'constraints': {},
            'foreign_keys': {}
        }

        # Get all table names or filter by target_tables
        all_tables = inspector.get_table_names()
        tables_to_process = target_tables if target_tables else all_tables

        schema_metadata['tables'] = tables_to_process

        for table_name in tables_to_process:
            # Get columns
            columns = inspector.get_columns(table_name)
            schema_metadata['columns'][table_name] = columns

            # Get primary keys
            pk = inspector.get_pk_constraint(table_name)

            # Get foreign keys
            fks = inspector.get_foreign_keys(table_name)
            schema_metadata['foreign_keys'][table_name] = fks

            # Get unique constraints
            unique_constraints = inspector.get_unique_constraints(table_name)
            schema_metadata['constraints'][table_name] = {
                'primary_key': pk,
                'unique': unique_constraints
            }

        return schema_metadata

    def validate_plan(
        self,
        plan: DataGenerationPlan,
        schema_metadata: dict
    ) -> tuple[bool, list[str]]:
        """Validate that a generation plan is compatible with schema.

        Implements ITestDataGenerator.validate_plan.
        """
        errors = []

        # Check all tables in plan exist in schema
        for table_config in plan.tables:
            if table_config.table_name not in schema_metadata['tables']:
                errors.append(f"Table '{table_config.table_name}' not found in schema")

        # Check insertion order is valid (all tables present)
        plan_table_names = {t.table_name for t in plan.tables}
        for table_name in plan.insertion_order:
            if table_name not in plan_table_names:
                errors.append(f"Table '{table_name}' in insertion_order but not in plan.tables")

        # Check record counts are positive
        for table_config in plan.tables:
            if table_config.record_count <= 0:
                errors.append(f"Invalid record count for table '{table_config.table_name}': {table_config.record_count}")

        return (len(errors) == 0, errors)

    def estimate_duration(
        self,
        plan: DataGenerationPlan,
        database_type: str
    ) -> float:
        """Estimate execution duration in seconds.

        Implements ITestDataGenerator.estimate_duration.
        """
        # Rough estimates based on benchmarks
        records_per_second = {
            'mysql': 50,
            'postgresql': 40,
            'sqlite': 200
        }

        speed = records_per_second.get(database_type, 50)
        estimated_seconds = plan.estimated_total_records / speed

        # Add overhead for LLM and setup (5 seconds)
        return estimated_seconds + 5.0

    def preview_sample_data(
        self,
        plan: DataGenerationPlan,
        table_name: str,
        num_rows: int = 5
    ) -> list[dict]:
        """Generate sample rows for preview without inserting.

        Implements ITestDataGenerator.preview_sample_data.
        """
        # Find table config
        table_config = None
        for tc in plan.tables:
            if tc.table_name == table_name:
                table_config = tc
                break

        if not table_config:
            raise ValueError(f"Table '{table_name}' not found in plan")

        if num_rows <= 0:
            raise ValueError(f"num_rows must be positive, got {num_rows}")

        # Generate sample rows
        sample_rows = []
        for row_index in range(min(num_rows, table_config.record_count)):
            row_data = self.data_synthesizer.synthesize_row(
                table_name=table_name,
                columns=table_config.columns,
                row_index=row_index,
                foreign_key_values=None
            )
            sample_rows.append(row_data)

        return sample_rows

    def _build_plan_prompt(self, request: TestDataRequest, schema_metadata: dict) -> str:
        """Build LLM prompt for plan generation (T030, T034)."""
        import json

        # Build record count guidance (T030)
        record_count_guidance = ""
        if request.record_counts:
            if '__all__' in request.record_counts:
                record_count_guidance = f"\n**IMPORTANT**: User requested {request.record_counts['__all__']} records per table. Use this count for ALL tables."
            else:
                counts_str = ", ".join([f"{table}: {count}" for table, count in request.record_counts.items()])
                record_count_guidance = f"\n**IMPORTANT**: User specified record counts: {counts_str}. Use these exact counts for the specified tables, and defaults for others."

        # Build domain-specific guidance (T034)
        domain_guidance = ""
        if request.domain_context:
            domain_guides = {
                'e-commerce': """
For e-commerce domain:
- Product names: use company() or catch_phrase()
- Prices: use pydecimal with left_digits=4, right_digits=2
- SKUs: use bothify with pattern like '???-#####'
- Categories: use words(nb=2) or department()
- Order statuses: choose from ['pending', 'processing', 'shipped', 'delivered', 'cancelled']""",
                'blog': """
For blog domain:
- Post titles: use sentence(nb_words=6) or catch_phrase()
- Content/body: use paragraphs(nb=3) or text(max_nb_chars=1000)
- Author names: use name()
- Categories/tags: use words(nb=3)
- Publish dates: use date_between(start_date='-1y', end_date='today')""",
                'social media': """
For social media domain:
- Usernames: use user_name()
- Display names: use name()
- Post content: use text(max_nb_chars=280)
- Hashtags: use words(nb=3) prefixed with #
- Follower counts: use random_int(min=0, max=10000)""",
                'medical': """
For medical domain:
- Patient names: use name()
- Medical record numbers: use bothify(text='MRN-########')
- Diagnoses: use sentence()
- Medications: use words(nb=2)
- Appointment dates: use date_between(start_date='-30d', end_date='+30d')""",
                'financial': """
For financial domain:
- Account numbers: use bothify(text='####-####-####')
- Transaction amounts: use pydecimal with left_digits=6, right_digits=2
- Transaction types: choose from ['debit', 'credit', 'transfer', 'payment']
- Currency codes: use currency_code()""",
            }
            domain_guidance = domain_guides.get(request.domain_context, "")

        prompt = f"""You are a test data generation planner for database schemas.

Generate a test data generation plan in JSON format for the following request:

User Query: "{request.user_query}"
Database Type: {request.database_type}
Domain Context: {request.domain_context or 'general'}{record_count_guidance}

Schema Information:
{json.dumps(schema_metadata, indent=2, default=str)}

Generate a JSON plan with the following structure:
{{
    "tables": [
        {{
            "table_name": "table_name",
            "record_count": 15,
            "columns": [
                {{
                    "column_name": "column_name",
                    "faker_provider": "name|email|phone_number|address|city|text|random_int|date_between|...",
                    "provider_params": {{}},
                    "is_primary_key": false,
                    "is_foreign_key": false,
                    "foreign_key_table": null,
                    "foreign_key_column": null,
                    "is_unique": false,
                    "is_nullable": false,
                    "null_probability": 0.15
                }}
            ]
        }}
    ],
    "rationale": "Explanation of table ordering and data generation strategy"
}}

Guidelines:
1. Use default of 15 records per table unless user specifies otherwise
2. Select appropriate Faker providers based on column names and types{domain_guidance}
3. For email columns: use "email" provider
4. For name columns: use "name", "first_name", or "last_name"
5. For date/time columns: use "date_between" or "date_time_this_year"
6. For text columns: use "text" or "sentence"
7. For numeric columns: use "random_int" with appropriate min/max
8. Set is_unique=true for columns with UNIQUE constraints
9. Set is_nullable=true and null_probability=0.15 for nullable columns
10. Identify foreign key relationships and set is_foreign_key=true

Return ONLY valid JSON, no additional text.
"""
        return prompt

    def _calculate_insertion_order(self, tables: list, schema_metadata: dict) -> list[str]:
        """Calculate insertion order using topological sort."""
        from toposort import toposort_flatten

        # Build dependency graph
        dependencies = {}

        for table_config in tables:
            table_name = table_config.table_name
            table_deps = set()

            # Get FK dependencies from schema metadata
            if table_name in schema_metadata.get('foreign_keys', {}):
                for fk in schema_metadata['foreign_keys'][table_name]:
                    referred_table = fk.get('referred_table')
                    if referred_table and referred_table != table_name:
                        table_deps.add(referred_table)

            dependencies[table_name] = table_deps

        # Perform topological sort
        try:
            insertion_order = list(toposort_flatten(dependencies))
            return insertion_order
        except Exception as e:
            # Fallback: return tables in original order if toposort fails
            return [t.table_name for t in tables]

    def _create_fallback_plan(self, request: TestDataRequest, schema_metadata: dict) -> DataGenerationPlan:
        """Create a rule-based fallback plan when LLM fails."""
        from ..models import DataGenerationPlan, TableGenerationConfig, ColumnGenerationConfig
        import uuid
        from datetime import datetime

        tables = []
        target_tables = request.target_tables or schema_metadata['tables']

        for table_name in target_tables:
            if table_name not in schema_metadata['columns']:
                continue

            columns_config = []
            for col_info in schema_metadata['columns'][table_name]:
                # Infer Faker provider from column name/type
                col_name = col_info['name'].lower()
                faker_provider = self._infer_faker_provider(col_name, col_info.get('type'))

                column_config = ColumnGenerationConfig(
                    column_name=col_info['name'],
                    faker_provider=faker_provider,
                    provider_params={},
                    is_primary_key=col_info.get('primary_key', False),
                    is_foreign_key=False,  # TODO: detect from schema
                    is_unique=col_info.get('unique', False),
                    is_nullable=col_info.get('nullable', True),
                    null_probability=0.15 if col_info.get('nullable') else 0.0
                )
                columns_config.append(column_config)

            table_config = TableGenerationConfig(
                table_name=table_name,
                record_count=request.record_counts.get(table_name, 15) if request.record_counts else 15,
                columns=columns_config
            )
            tables.append(table_config)

        # Calculate insertion order
        insertion_order = self._calculate_insertion_order(tables, schema_metadata)

        return DataGenerationPlan(
            plan_id=str(uuid.uuid4()),
            created_at=datetime.now(),
            database_type=request.database_type,
            tables=tables,
            insertion_order=insertion_order,
            rationale="Fallback rule-based plan (LLM unavailable)",
            estimated_total_records=sum(t.record_count for t in tables)
        )

    def _infer_faker_provider(self, column_name: str, column_type: Any) -> str:
        """Infer Faker provider from column name and type."""
        name_lower = column_name.lower()

        # Name-based inference
        if 'email' in name_lower:
            return 'email'
        elif 'name' in name_lower:
            if 'first' in name_lower:
                return 'first_name'
            elif 'last' in name_lower:
                return 'last_name'
            else:
                return 'name'
        elif 'phone' in name_lower:
            return 'phone_number'
        elif 'address' in name_lower:
            return 'address'
        elif 'city' in name_lower:
            return 'city'
        elif 'state' in name_lower:
            return 'state'
        elif 'zip' in name_lower or 'postal' in name_lower:
            return 'zipcode'
        elif 'country' in name_lower:
            return 'country'
        elif 'company' in name_lower:
            return 'company'
        elif 'url' in name_lower or 'website' in name_lower:
            return 'url'
        elif 'description' in name_lower or 'bio' in name_lower or 'text' in name_lower:
            return 'text'
        elif 'date' in name_lower:
            return 'date_this_year'
        elif 'time' in name_lower:
            return 'date_time_this_year'

        # Type-based fallback
        type_str = str(column_type).upper() if column_type else ''
        if 'INT' in type_str or 'NUMERIC' in type_str:
            return 'random_int'
        elif 'BOOL' in type_str:
            return 'boolean'
        elif 'DATE' in type_str or 'TIME' in type_str:
            return 'date_this_year'
        elif 'TEXT' in type_str or 'VARCHAR' in type_str or 'CHAR' in type_str:
            return 'word'

        return 'word'  # Ultimate fallback
