# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Offline provider wrapper classes for Featureform.

This module contains wrapper classes for offline data providers including SQL-based
providers (Postgres, Snowflake, BigQuery, etc.) and Spark-based providers.
"""

from collections.abc import Iterable
from datetime import timedelta
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Union

from ..config.compute import K8sArgs, K8sResourceSpecs
from ..config.offline_stores import ResourceSnowflakeConfig
from ..enums import FilePrefix, ScalarType, TableFormat, TrainingSetType
from ..resources import (
    EntityMapping,
    EntityMappings,
    FileStore,
    GlueCatalogTable,
    LabelVariant,
    PartitionType,
    SQLTable,
    UnityCatalogTable,
)
from ..utils.helpers import set_tags_properties

if TYPE_CHECKING:
    from ..registrar import (
        EntityRegistrar,
        SubscriptableTransformation,
        UserRegistrar,
    )
    from ..resources import Entity, NameVariant, SourceVariant
    from ..resources.feature import AggregateFeature, AttributeFeature


__all__ = [
    "OfflineProvider",
    "OfflineSQLProvider",
    "OfflineSparkProvider",
    "OfflineK8sProvider",
]


class OfflineProvider:
    def __init__(self, registrar, provider):
        self.__registrar = registrar
        self.__provider = provider

    def name(self) -> str:
        return self.__provider.name

    # for testing
    def _provider(self):
        return self.__provider

    def __eq__(self, __value: object) -> bool:
        assert isinstance(__value, OfflineProvider)
        return self.__provider == __value.__provider


class OfflineSQLProvider(OfflineProvider):
    def __init__(self, registrar, provider):
        super().__init__(registrar, provider)
        self.__registrar = registrar
        self.__provider = provider

    def register_table(
        self,
        name: str,
        table: str,
        variant: str = "",
        timestamp_column: str = "",
        owner: Union[str, "UserRegistrar"] = "",
        description: str = "",
        schema: str = "",
        database: str = "",
        tags: List[str] = [],
        properties: dict = {},
    ):
        """Register a SQL table as a primary data source.

        **Example**

        ```
        postgres = client.get_provider("my_postgres")
        table =  postgres.register_table(
            name="transactions",
            variant="july_2023",
            table="transactions_table",
        ):
        ```

        Args:
            name (str): Name of table to be registered
            variant (str): Name of variant to be registered
            table (str): Name of SQL table
            owner (Union[str, "UserRegistrar"]): Owner
            timestamp_column (str): Optional parameter that can be used for incremental reads
            description (str): Description of table to be registered

        Returns:
            source (ColumnSourceRegistrar): source
        """

        location = SQLTable(schema=schema, database=database, name=table)

        return self.__registrar.register_primary_data(
            name=name,
            variant=variant,
            location=location,
            owner=owner,
            provider=self.name(),
            description=description,
            tags=tags,
            properties=properties,
            timestamp_column=timestamp_column,
        )

    def config(self):
        return self.__provider

    def sql_transformation(
        self,
        owner: Union[str, "UserRegistrar"] = "",
        variant: str = "",
        name: str = "",
        schedule: str = "",
        description: str = "",
        inputs: list = None,
        tags: List[str] = None,
        properties: dict = None,
        resource_snowflake_config: Optional[ResourceSnowflakeConfig] = None,
    ):
        """
        Register a SQL transformation source.

        The name of the function is the name of the resulting source.

        Sources for the transformation can be specified by adding the Name and Variant in brackets '{{ name.variant }}'.
        The correct source is substituted when the query is run.

        **Examples**:

        ``` py
        postgres = client.get_provider("my_postgres")
        @postgres.sql_transformation(variant="quickstart")
        def average_user_transaction():
            return "SELECT CustomerID as user_id, avg(TransactionAmount) as avg_transaction_amt from {{transactions.v1}} GROUP BY user_id"
        ```

        Args:
            name (str): Name of source
            variant (str): Name of variant
            schedule (str): The frequency at which the transformation is run as a cron expression
            owner (Union[str, "UserRegistrar"]): Owner
            description (str): Description of primary data to be registered
            inputs (list): A list of Source NameVariant Tuples to input into the transformation


        Returns:
            source (ColumnSourceRegistrar): Source
        """
        tags, properties = set_tags_properties(tags, properties)
        if (
            resource_snowflake_config is not None
            and self.__provider.config.type() != "SNOWFLAKE_OFFLINE"
        ):
            raise ValueError(
                "Dynamic tables are only supported for Snowflake offline providers"
            )
        return self.__registrar.sql_transformation(
            name=name,
            variant=variant,
            owner=owner,
            schedule=schedule,
            provider=self.name(),
            description=description,
            inputs=inputs,
            tags=tags,
            properties=properties,
            resource_snowflake_config=resource_snowflake_config,
        )

    def register_training_set(
        self,
        name: str,
        variant: str = "",
        features: Optional[List] = None,
        label: Optional["NameVariant"] = None,
        resources: Optional[List] = None,
        owner: Union[str, "UserRegistrar"] = "",
        description: str = "",
        schedule: str = "",
        tags: Optional[List[str]] = None,
        properties: Optional[Dict] = None,
        resource_snowflake_config: Optional[ResourceSnowflakeConfig] = None,
        type: TrainingSetType = TrainingSetType.DYNAMIC,
    ):
        return self.__registrar.register_training_set(
            name=name,
            variant=variant,
            features=features if features is not None else [],
            label=label if label is not None else ("", ""),
            resources=resources if resources is not None else [],
            owner=owner,
            description=description,
            schedule=schedule,
            tags=tags if tags is not None else [],
            properties=properties if properties is not None else {},
            provider=self.name(),
            resource_snowflake_config=resource_snowflake_config,
            type=type,
        )

    def __eq__(self, __value: object) -> bool:
        assert isinstance(__value, OfflineSQLProvider)
        return (
            self.__provider == __value.__provider
            and self.__registrar == __value.__registrar
        )

    def register_label(
        self,
        name: str,
        entity_mappings: List[dict],
        value_type: ScalarType,
        dataset: "SubscriptableTransformation",
        value_column: str,
        timestamp_column: Optional[str] = None,
        variant: str = "",
        description: str = "",
        owner: Union[str, "UserRegistrar"] = "",
        resource_snowflake_config: Optional[ResourceSnowflakeConfig] = None,
        tags: Optional[List[str]] = None,
        properties: Optional[dict] = None,
    ):
        """
        Register a multi-entity label on a SQL provider (currently only supported for Snowflake).

        **Examples**:

        ``` py
        snowflake = client.get_provider("my_snowflake")
        label = snowflake.register_label(
            name="total_purchase_amount",
            entity_mappings=[{"column": "user_id", "entity": "user"}, {"column": "product_id", "entity": "product"}],
            value_type=ff.Float32,
            dataset=purchases,
            value_column="final_total",
        )
        ```

        Args:
            name (str): Name of the label
            entity_mappings (List[dict]): A list of dictionaries mapping entity columns to entity names
            value_type (ScalarType): The type of the label
            dataset: The dataset the label is derived from
            value_column (str): The column in the dataset that contains the label values
            timestamp_column (str, optional): The column in the dataset that contains the timestamp
            variant (str, optional): The variant of the label
            description (str, optional): Description of the label
            owner (Union[str, "UserRegistrar"], optional): Owner
            resource_snowflake_config (ResourceSnowflakeConfig, optional): Snowflake specific configuration
            tags (List[str], optional): Tags
            properties (dict, optional): Properties

        Returns:
            label (LabelVariant): The label variant instance
        """
        if self.__provider.config.type() != "SNOWFLAKE_OFFLINE":
            raise ValueError(
                "Registering labels on SQL offline providers is currently only supported for Snowflake"
            )
        if variant == "":
            variant = self.__registrar.get_run()

        if not isinstance(entity_mappings, list) or len(entity_mappings) == 0:
            raise ValueError("entity_mappings must be a non-empty list")

        mappings = []
        for m in entity_mappings:
            if not isinstance(m, dict):
                raise ValueError("entity_mappings must be a list of dictionaries")
            column = m.get("column")
            if not column:
                raise ValueError("missing entity column in mapping")
            entity = m.get("entity")
            if not entity:
                raise ValueError("missing entity name in mapping")
            mappings.append(
                EntityMapping(
                    name=entity,
                    entity_column=column,
                )
            )

        if not ScalarType.has_value(value_type) and not isinstance(
            value_type, ScalarType
        ):
            raise ValueError(
                f"Invalid type for label {name} ({variant}). Must be a ScalarType or one of {ScalarType.get_values()}"
            )
        if isinstance(value_type, ScalarType):
            value_type = value_type.value

        if not hasattr(dataset, "name_variant"):
            raise ValueError("Dataset must have a name_variant method")

        source = dataset.name_variant()

        if not value_column:
            raise ValueError("value_column must be provided")

        tags, properties = set_tags_properties(tags, properties)
        if not isinstance(owner, str):
            owner = owner.name()
        if owner == "":
            owner = self.__registrar.must_get_default_owner()

        label = LabelVariant(
            name=name,
            variant=variant,
            source=source,
            value_type=value_type,
            owner=owner,
            description=description,
            tags=tags,
            properties=properties,
            entity="",
            location=EntityMappings(
                mappings=mappings,
                value_column=value_column,
                timestamp_column=timestamp_column,
            ),
            resource_snowflake_config=resource_snowflake_config,
        )

        self.__registrar.add_resource(label)
        return label


class OfflineSparkProvider(OfflineProvider):
    def __init__(self, registrar, provider):
        super().__init__(registrar, provider)
        self.__registrar = registrar
        self.__provider = provider

    def register_iceberg_table(
        self,
        name: str,
        database: str,
        table: str,
        variant: str = "",
        owner: Union[str, "UserRegistrar"] = "",
        description: str = "",
        tags: Optional[List[str]] = None,
        properties: Optional[dict] = None,
    ):
        """
        Register an Iceberg table as a primary data source.

        **Examples**

        ```
        spark = client.get_provider("my_spark")
        transactions = spark.register_iceberg_table(
            name="transactions",
            database="fraud",
            table="transactions",
            description="A dataset of fraudulent transactions"
        )
        ```

        Args:
            name (str): Name of table to be registered
            database (str): Name of database
            table (str): Name of table
            variant (str): Name of variant to be registered
            owner (Union[str, "UserRegistrar"]): Owner
            description (str): Description of table to be registered
            tags (List[str]): Tags
            properties (dict): Properties
        Returns:
            source (ColumnSourceRegistrar): source
        """
        tags, properties = set_tags_properties(tags, properties)

        return self.__registrar.register_primary_data(
            name=name,
            variant=variant,
            location=GlueCatalogTable(
                database, table, table_format=TableFormat.ICEBERG
            ),
            owner=owner,
            provider=self.name(),
            description=description,
            tags=tags,
            properties=properties,
        )

    def register_delta_table(
        self,
        name: str,
        database: str,
        schema: str,
        table: str,
        variant: str = "",
        owner: Union[str, "UserRegistrar"] = "",
        description: str = "",
        tags: Optional[List[str]] = None,
        properties: Optional[dict] = None,
    ):
        """
        Register a Delta Lake table as a primary data source.

        **Examples**

        ```
        spark = client.get_provider("my_spark")
        transactions = spark.register_delta_table(
            name="transactions",
            database="fraud",
            table="transactions",
            description="A dataset of fraudulent transactions"
        )
        ```

        Args:
            name (str): Name of table to be registered
            database (str): Name of database
            table (str): Name of table
            variant (str): Name of variant to be registered
            owner (Union[str, "UserRegistrar"]): Owner
            description (str): Description of table to be registered
            tags (List[str]): Tags
            properties (dict): Properties
        Returns:
            source (ColumnSourceRegistrar): source
        """
        tags, properties = set_tags_properties(tags, properties)

        return self.__registrar.register_primary_data(
            name=name,
            variant=variant,
            location=UnityCatalogTable(
                database, schema, table, table_format=TableFormat.DELTA
            ),
            owner=owner,
            provider=self.name(),
            description=description,
            tags=tags,
            properties=properties,
        )

    def register_file(
        self,
        name: str,
        file_path: str,
        variant: str = "",
        owner: Union[str, "UserRegistrar"] = "",
        description: str = "",
        tags: List[str] = [],
        properties: dict = {},
    ):
        """Register a Spark data source as a primary data source.

        **Examples**

        ```
        spark = client.get_provider("my_spark")
        transactions = spark.register_file(
            name="transactions",
            variant="quickstart",
            description="A dataset of fraudulent transactions",
            file_path="s3://featureform-spark/featureform/transactions.parquet"
        )
        ```

        Args:
            name (str): Name of table to be registered
            variant (str): Name of variant to be registered
            file_path (str): The URI of the file. Must be the full path
            owner (Union[str, "UserRegistrar"]): Owner
            description (str): Description of table to be registered

        Returns:
            source (ColumnSourceRegistrar): source
        """
        FilePrefix.validate(self.__provider.config.store_type, file_path)

        return self.__registrar.register_primary_data(
            name=name,
            variant=variant,
            location=FileStore(file_path),
            owner=owner,
            provider=self.name(),
            description=description,
            tags=tags,
            properties=properties,
        )

    def register_parquet_file(
        self,
        name: str,
        file_path: str,
        variant: str = "",
        owner: Union[str, "UserRegistrar"] = "",
        description: str = "",
    ):
        if self.__provider.config.executor_type != "EMR" and file_path.startswith(
            FilePrefix.S3.value
        ):
            file_path = file_path.replace(FilePrefix.S3.value, FilePrefix.S3A.value)
        return self.register_file(name, file_path, variant, owner, description)

    def incremental_sql_transformation(
        self,
        variant: str = "",
        owner: Union[str, "UserRegistrar"] = "",
        name: str = "",
        schedule: str = "",
        inputs: Optional[list] = None,
        description: str = "",
        tags: Optional[List[str]] = None,
        properties: Optional[dict] = None,
        partition_options: Optional[PartitionType] = None,
        max_job_duration: timedelta = timedelta(hours=48),
        spark_params: Optional[Dict[str, str]] = None,
        write_options: Optional[Dict[str, str]] = None,
        table_properties: Optional[Dict[str, str]] = None,
    ):
        tags, properties = set_tags_properties(tags, properties)
        # Import here to avoid circular dependency
        from ..registrar import Incremental

        reg_inputs = []
        inc_inputs = []
        inputs = inputs or []
        for i in inputs:
            if isinstance(i, Incremental):
                unwrapped = i.resource
                reg_inputs.append(unwrapped)
                inc_inputs.append(unwrapped)
            else:
                reg_inputs.append(i)

        return self.__registrar.sql_transformation(
            name=name,
            variant=variant,
            owner=owner,
            schedule=schedule,
            provider=self.name(),
            description=description,
            inputs=reg_inputs,
            tags=tags,
            properties=properties,
            incremental=True,
            incremental_inputs=inc_inputs,
            partition_options=partition_options,
            max_job_duration=max_job_duration,
            spark_params=spark_params,
            write_options=write_options,
            table_properties=table_properties,
        )

    def streaming_sql_transformation(
        self,
        variant: str = "",
        owner: Union[str, "UserRegistrar"] = "",
        name: str = "",
        schedule: str = "",
        inputs: Optional[list] = None,
        description: str = "",
        tags: Optional[List[str]] = None,
        properties: Optional[dict] = None,
        spark_params: Optional[Dict[str, str]] = None,
        write_options: Optional[Dict[str, str]] = None,
        table_properties: Optional[Dict[str, str]] = None,
    ):
        # Import here to avoid circular dependency
        from ..registrar import Stream

        tags, properties = set_tags_properties(tags, properties)
        reg_inputs = []
        streaming_inputs = []
        inputs = inputs or []
        for i in inputs:
            if isinstance(i, Stream):
                unwrapped = i.resource
                reg_inputs.append(unwrapped)
                streaming_inputs.append(unwrapped)
            else:
                reg_inputs.append(i)

        return self.__registrar.sql_transformation(
            name=name,
            variant=variant,
            owner=owner,
            schedule=schedule,
            provider=self.name(),
            description=description,
            inputs=reg_inputs,
            tags=tags,
            properties=properties,
            is_streaming=True,
            streaming_inputs=streaming_inputs,
            spark_params=spark_params,
            write_options=write_options,
            table_properties=table_properties,
        )

    def sql_transformation(
        self,
        variant: str = "",
        owner: Union[str, "UserRegistrar"] = "",
        name: str = "",
        schedule: str = "",
        inputs: list = None,
        description: str = "",
        tags: List[str] = [],
        properties: dict = {},
        partition_options: Optional[PartitionType] = None,
        max_job_duration: timedelta = timedelta(hours=48),
        spark_params: Optional[Dict[str, str]] = None,
        write_options: Optional[Dict[str, str]] = None,
        table_properties: Optional[Dict[str, str]] = None,
    ):
        """
        Register a SQL transformation source. The spark.sql_transformation decorator takes the returned string in the
        following function and executes it as a SQL Query.

        The name of the function is the name of the resulting source.

        Sources for the transformation can be specified by adding the Name and Variant in brackets '{{ name.variant }}'.
        The correct source is substituted when the query is run.

        **Examples**:
        ``` py
        @spark.sql_transformation(variant="quickstart")
        def average_user_transaction():
            return "SELECT CustomerID as user_id, avg(TransactionAmount) as avg_transaction_amt from {{transactions.v1}} GROUP BY user_id"
        ```

        Args:
            name (str): Name of source
            variant (str): Name of variant
            owner (Union[str, "UserRegistrar"]): Owner
            description (str): Description of primary data to be registered
            inputs (list[Tuple(str, str)]): A list of Source NameVariant Tuples to input into the transformation
            max_job_duration (timedelta): Maximum duration FeatureForm will wait for the job to complete; default is 48 hours; jobs that exceed this duration will be canceled


        Returns:
            source (ColumnSourceRegistrar): Source
        """
        return self.__registrar.sql_transformation(
            name=name,
            variant=variant,
            owner=owner,
            schedule=schedule,
            provider=self.name(),
            description=description,
            inputs=inputs,
            tags=tags,
            properties=properties,
            partition_options=partition_options,
            max_job_duration=max_job_duration,
            spark_params=spark_params,
            write_options=write_options,
            table_properties=table_properties,
        )

    def sql_feature(
        self,
        *,
        variant: str = "",
        owner: Union[str, "UserRegistrar"] = "",
        name: str = "",
        inputs: Optional[Iterable[Union["NameVariant", "SourceVariant"]]] = None,
        description: str = "",
        tags: Optional[List[str]] = None,
        properties: Optional[dict] = None,
        partition_options: Optional[PartitionType] = None,
        max_job_duration: timedelta = timedelta(hours=48),
        spark_params: Optional[Dict[str, str]] = None,
        write_options: Optional[Dict[str, str]] = None,
        table_properties: Optional[Dict[str, str]] = None,
        entities: Optional[Iterable[Union[str, "EntityRegistrar", "Entity"]]] = None,
        entity_column: str = "",
        timestamp_column: str = "",
        features: Optional[
            Iterable[Union["AttributeFeature", "AggregateFeature", dict]]
        ] = None,
    ):
        """Register a SQL-based feature transformation.

        This decorator pairs a SQL transformation with the feature definitions
        produced by that query. The decorated function must accept one
        positional argument per entry in ``inputs`` (in the same order) and
        return a SQL string whose result set contains the ``entity_column`` and
        every column referenced by the provided ``features`` definitions. The
        argument names are captured as placeholders, so each argument must match
        a ``{{ argument_name }}`` reference in the SQL string. Any
        :class:`AggregateFeature` definitions require the query to include the
        specified ``timestamp_column``.

        **Example:**

        ```py
        @spark.sql_feature(
            name="user_transactions",
            inputs=[("transactions", "v1")],
            entities=["user"],
            entity_column="user_id",
            timestamp_column="event_time",
            features=[
                AttributeFeature(
                    name="total_transactions",
                    input_column="transaction_count",
                    input_type=fftypes.IntType(),
                ),
                AggregateFeature(
                    name="avg_transaction_amt",
                    input_column="avg_amount",
                    input_type=fftypes.FloatType(),
                    time_window=timedelta(days=7),
                ),
            ],
        )
        def user_transactions(transactions):
            return '''
                SELECT
                    CustomerID AS user_id,
                    COUNT(*) AS transaction_count,
                    AVG(TransactionAmount) AS avg_amount,
                    MAX(EventTime) AS event_time
                FROM {{ transactions }}
                GROUP BY CustomerID
            '''
        ```

        Args:
            variant (str): Optional variant to register the transformation under.
            owner (Union[str, "UserRegistrar"]): Owner or namespace for the
                transformation.
            name (str): Name of the transformation; defaults to the decorated
                function name when omitted.
            inputs (Iterable[Union[Tuple[str, str], SourceVariant]], optional):
                Iterable of ``("source", "variant")`` pairs or `SourceVariant`s
                whose outputs are provided to the decorated function as Spark dataframes.
            description (str): Human-readable description of the feature
                transformation.
            tags (List[str], optional): Tags applied to the registered
                transformation.
            properties (dict, optional): Arbitrary metadata stored with the
                transformation.
            partition_options (PartitionType, optional): Partitioning strategy
                for materializing the transformation output.
            max_job_duration (timedelta): Maximum duration Featureform waits
                for the batch job to complete before cancellation. Defaults to
                48 hours.
            spark_params (Dict[str, str], optional): Additional Spark
                configuration passed to the execution environment.
            write_options (Dict[str, str], optional): Storage write options for
                the transformation output.
            table_properties (Dict[str, str], optional): Provider-specific table
                properties applied to the materialized dataset.
            entities (Iterable[Union[str, "EntityRegistrar", "Entity"]]): Entities
                that receive the registered features.
            entity_column (str): Column in the query results containing the
                entity identifier.
            timestamp_column (str): Column containing event timestamps. Required
                when ``features`` includes an :class:`AggregateFeature`.
            features (Iterable[Union["AttributeFeature", "AggregateFeature", dict]]):
                Feature definitions describing the columns produced by the
                transformation. Dictionaries may be used for dynamic feature
                specifications.

        Returns:
            ColumnSourceRegistrar: Registered transformation source.

        Raises:
            ValueError: If required values such as ``entities``, ``features``,
                or ``timestamp_column`` (for aggregate features) are missing, or
                if the function signature does not match the declared inputs.
            TypeError: If ``entities`` or ``features`` are provided with
                unsupported types.
        """

        entities_list = tuple(self._ensure_feature_entities(entities))
        normalized_features, has_aggregate = self._normalize_feature_definitions(
            features, variant
        )

        if has_aggregate and timestamp_column == "":
            raise ValueError(
                "timestamp_column must be provided when AggregateFeature definitions are used"
            )

        transformation_inputs = list(inputs) if inputs else []

        tags, properties = set_tags_properties(tags, properties)

        transformation_decorator = self.sql_transformation(
            variant=variant,
            owner=owner,
            name=name,
            inputs=transformation_inputs,
            description=description,
            tags=tags,
            properties=properties,
            partition_options=partition_options,
            max_job_duration=max_job_duration,
            spark_params=spark_params,
            write_options=write_options,
            table_properties=table_properties,
        )

        def decorator(fn):
            transformation = transformation_decorator(fn)
            self._register_feature_resources(
                transformation=transformation,
                entities=entities_list,
                entity_column=entity_column,
                owner=owner,
                features=normalized_features,
                timestamp_column=timestamp_column,
            )
            return transformation

        return decorator

    def df_transformation(
        self,
        variant: str = "",
        owner: Union[str, "UserRegistrar"] = "",
        name: str = "",
        description: str = "",
        inputs: list = [],
        tags: List[str] = [],
        properties: dict = {},
        partition_options: Optional[PartitionType] = None,
        max_job_duration: timedelta = timedelta(hours=48),
        spark_params: Optional[Dict[str, str]] = None,
        write_options: Optional[Dict[str, str]] = None,
        table_properties: Optional[Dict[str, str]] = None,
    ):
        """
        Register a Dataframe transformation source. The spark.df_transformation decorator takes the contents
        of the following function and executes the code it contains at serving time.

        The name of the function is used as the name of the source when being registered.

        The specified inputs are loaded into dataframes that can be accessed using the function parameters.

        **Examples**:
        ``` py
        @spark.df_transformation(inputs=[("source", "one")])        # Sources are added as inputs
        def average_user_transaction(df):                           # Sources can be manipulated by adding them as params
            return df
        ```

        Args:
            name (str): Name of source
            variant (str): Name of variant
            owner (Union[str, "UserRegistrar"]): Owner
            description (str): Description of primary data to be registered
            inputs (list[Tuple(str, str)]): A list of Source NameVariant Tuples to input into the transformation
            max_job_duration (timedelta): Maximum duration FeatureForm will wait for the job to complete; default is 48 hours; jobs that exceed this duration will be canceled

        Returns:
            source (ColumnSourceRegistrar): Source
        """
        return self.__registrar.df_transformation(
            name=name,
            variant=variant,
            owner=owner,
            provider=self.name(),
            description=description,
            inputs=inputs,
            tags=tags,
            properties=properties,
            partition_options=partition_options,
            max_job_duration=max_job_duration,
            spark_params=spark_params or {},
            write_options=write_options or {},
            table_properties=table_properties or {},
        )

    def df_feature(
        self,
        *,
        variant: str = "",
        owner: Union[str, "UserRegistrar"] = "",
        name: str = "",
        description: str = "",
        inputs: Optional[Iterable[Union["NameVariant", "SourceVariant"]]] = None,
        tags: Optional[List[str]] = None,
        properties: Optional[dict] = None,
        partition_options: Optional[PartitionType] = None,
        max_job_duration: timedelta = timedelta(hours=48),
        spark_params: Optional[Dict[str, str]] = None,
        write_options: Optional[Dict[str, str]] = None,
        table_properties: Optional[Dict[str, str]] = None,
        entities: Optional[Iterable[Union[str, "EntityRegistrar", "Entity"]]] = None,
        entity_column: str = "",
        timestamp_column: str = "",
        features: Optional[
            Iterable[Union["AttributeFeature", "AggregateFeature", dict]]
        ] = None,
    ):
        """Register a dataframe feature transformation.

        This decorator registers both the dataframe transformation and the
        feature definitions that are produced by that transformation in a
        single step. The decorated function must define one positional argument
        for each entry in ``inputs`` (in the declared order); Featureform passes
        Spark dataframes for those inputs when the transformation executes.
        Each argument name should match the dataframe reference used inside the
        function body. The returned dataframe must contain the
        ``entity_column`` and every column referenced by the supplied
        ``features`` definitions. If any :class:`AggregateFeature` definitions
        are provided, the dataframe must also include the ``timestamp_column``.

        **Example:**

        ```py
        @spark.df_feature(
            name="user_transactions",
            inputs=[("transactions", "v1")],
            entities=["user"],
            entity_column="user_id",
            timestamp_column="event_time",
            features=[
                AttributeFeature(
                    name="total_transactions",
                    input_column="transaction_count",
                    input_type=fftypes.IntType(),
                ),
                AggregateFeature(
                    name="avg_transaction_amt",
                    input_column="avg_amount",
                    input_type=fftypes.FloatType(),
                    time_window=timedelta(days=7),
                ),
            ],
        )
        def user_transactions(transactions):
            return (
                transactions.groupBy("user_id")
                .agg(
                    F.count("id").alias("transaction_count"),
                    F.avg("amount").alias("avg_amount"),
                    F.max("event_time").alias("event_time"),
                )
            )
        ```

        Args:
            variant (str): Optional variant to register the transformation under.
            owner (Union[str, "UserRegistrar"]): Owner or namespace for the
                transformation.
            name (str): Name of the transformation; defaults to the decorated
                function name when omitted.
            description (str): Human-readable description of the feature
                transformation.
            inputs (Iterable[Union[Tuple[str, str], SourceVariant]], optional):
                Iterable of ``("source", "variant")`` pairs or `SourceVariant`s
                whose outputs are provided to the decorated function as Spark dataframes.
            tags (List[str], optional): Tags applied to the registered
                transformation.
            properties (dict, optional): Arbitrary metadata stored with the
                transformation.
            partition_options (PartitionType, optional): Partitioning strategy
                for materializing the transformation output.
            max_job_duration (timedelta): Maximum duration Featureform waits
                for the batch job to complete before cancellation. Defaults to
                48 hours.
            spark_params (Dict[str, str], optional): Additional Spark
                configuration passed to the execution environment.
            write_options (Dict[str, str], optional): Storage write options for
                the resulting dataframe.
            table_properties (Dict[str, str], optional): Provider-specific table
                properties applied to the materialized dataset.
            entities (Iterable[Union[str, "EntityRegistrar", "Entity"]]): Entities
                that receive the registered features.
            entity_column (str): Column in the returned dataframe containing the
                entity identifier.
            timestamp_column (str): Column containing event timestamps. Required
                when ``features`` includes an :class:`AggregateFeature`.
            features (Iterable[Union["AttributeFeature", "AggregateFeature", dict]]):
                Feature definitions describing the columns produced by the
                transformation. Dictionaries may be used for dynamic feature
                specifications.

        Returns:
            ColumnSourceRegistrar: Registered transformation source.

        Raises:
            ValueError: If required values such as ``entities``, ``features``,
                or ``timestamp_column`` (for aggregate features) are missing, or
                if the function signature does not match the declared inputs.
            TypeError: If ``entities`` or ``features`` are provided with
                unsupported types.
        """

        entities_list = tuple(self._ensure_feature_entities(entities))
        normalized_features, has_aggregate = self._normalize_feature_definitions(
            features, variant
        )

        if has_aggregate and timestamp_column == "":
            raise ValueError(
                "timestamp_column must be provided when AggregateFeature definitions are used"
            )

        transformation_inputs = list(inputs) if inputs else []

        tags, properties = set_tags_properties(tags, properties)

        transformation_decorator = self.df_transformation(
            variant=variant,
            owner=owner,
            name=name,
            description=description,
            inputs=transformation_inputs,
            tags=tags,
            properties=properties,
            partition_options=partition_options,
            max_job_duration=max_job_duration,
            spark_params=spark_params,
            write_options=write_options,
            table_properties=table_properties,
        )

        def decorator(fn):
            transformation = transformation_decorator(fn)
            self._register_feature_resources(
                transformation=transformation,
                entities=entities_list,
                entity_column=entity_column,
                owner=owner,
                features=normalized_features,
                timestamp_column=timestamp_column,
            )
            return transformation

        return decorator

    @staticmethod
    def _ensure_feature_entities(
        entities: Optional[Iterable[Union[str, "EntityRegistrar", "Entity"]]],
    ) -> List[Union[str, "EntityRegistrar", "Entity"]]:
        # Import here to avoid circular dependency
        from ..registrar import EntityRegistrar
        from ..resources import Entity

        if entities is None:
            raise ValueError("entities must be provided")

        if not isinstance(entities, Iterable):
            raise TypeError(
                "entities must be provided as a non-empty iterable of entity references"
            )

        entity_candidates = list(entities)

        if len(entity_candidates) == 0:
            raise ValueError(
                "entities must be a non-empty iterable of entity references"
            )

        normalized_entities: List[Union[str, "EntityRegistrar", "Entity"]] = []
        for entity in entity_candidates:
            if isinstance(entity, str):
                cleaned = entity.strip()
                if cleaned == "":
                    raise ValueError("entities must contain non-empty entity keys")
                normalized_entities.append(cleaned)
            elif isinstance(entity, (EntityRegistrar, Entity)):
                normalized_entities.append(entity)
            else:
                raise TypeError(
                    "entities must contain only entity keys or Entity references"
                )

        return normalized_entities

    def _normalize_feature_definitions(
        self,
        raw_features: Optional[Iterable],
        default_variant: str,
    ) -> Tuple[List[dict], bool]:
        # Import here to avoid circular dependency
        from ..resources.feature import AggregateFeature, AttributeFeature

        if raw_features is None:
            raise ValueError("features must be provided")

        if isinstance(raw_features, (AttributeFeature, AggregateFeature, dict)):
            feature_iterable = [raw_features]
        elif isinstance(raw_features, Iterable) and not isinstance(
            raw_features, (str, bytes)
        ):
            feature_iterable = list(raw_features)
        else:
            raise TypeError(
                "features must be provided as an iterable of feature definitions"
            )

        if len(feature_iterable) == 0:
            raise ValueError("features must be provided")

        normalized: List[dict] = []
        has_aggregate = False

        for feature in feature_iterable:
            if isinstance(feature, dict):
                feature_dict = dict(feature)
                if "name" not in feature_dict or not isinstance(
                    feature_dict["name"], str
                ):
                    raise ValueError(
                        "Feature dictionaries must include a non-empty 'name' value"
                    )
                feature_name = feature_dict["name"].strip()
                if feature_name == "":
                    raise ValueError(
                        "Feature dictionaries must include a non-empty 'name' value"
                    )
                feature_dict["name"] = feature_name

                column_value = feature_dict.pop(
                    "input_column", feature_dict.get("column")
                )
                if column_value is None:
                    raise ValueError(
                        "Feature dictionaries must include a 'column' or 'input_column' value"
                    )
                feature_dict["column"] = column_value

                if "type" not in feature_dict and "input_type" in feature_dict:
                    feature_dict["type"] = feature_dict.pop("input_type")
                if "type" not in feature_dict:
                    raise ValueError(
                        "Feature dictionaries must include a 'type' or 'input_type' value"
                    )

                if "timestamp_column" in feature_dict:
                    feature_dict["timestamp_column"] = self._normalize_timestamp_column(
                        feature_dict["timestamp_column"]
                    )

                properties = feature_dict.get("properties") or {}
                feature_dict["properties"] = dict(properties)
                if (
                    isinstance(properties, dict)
                    and properties.get("__ff_semantic_type") == "aggregate"
                ):
                    has_aggregate = True
            elif isinstance(feature, AttributeFeature):
                feature_dict = {
                    "name": feature.name,
                    "column": feature.input_column,
                    "type": feature.input_type,
                    "properties": {"__ff_semantic_type": "attribute"},
                }
            elif isinstance(feature, AggregateFeature):
                has_aggregate = True
                if not isinstance(feature.time_window, timedelta):
                    raise TypeError(
                        "AggregateFeature.time_window must be a datetime.timedelta instance"
                    )
                window_seconds = feature.time_window.total_seconds()
                window_value = (
                    str(int(window_seconds))
                    if float(window_seconds).is_integer()
                    else str(window_seconds)
                )
                function_value = (
                    feature.function.value
                    if hasattr(feature.function, "value")
                    else str(feature.function)
                )
                input_type = feature.input_type
                aggregate_properties = {
                    "__ff_semantic_type": "aggregate",
                    "__ff_aggregate_function": str(function_value),
                    "__ff_aggregate_time_window_seconds": window_value,
                    "__ff_aggregate_input_type": (
                        input_type.value
                        if isinstance(input_type, ScalarType)
                        else str(input_type)
                    ),
                }
                feature_dict = {
                    "name": feature.name,
                    "column": feature.input_column,
                    "type": input_type,
                    "properties": aggregate_properties,
                }
            else:
                raise TypeError(
                    "Unsupported feature definition type "
                    f"{type(feature).__name__}. Expected AttributeFeature, AggregateFeature, or dict."
                )

            if default_variant and feature_dict.get("variant", "") == "":
                feature_dict["variant"] = default_variant

            normalized.append(feature_dict)

        return normalized, has_aggregate

    def _register_feature_resources(
        self,
        transformation: "SubscriptableTransformation",
        entities: Iterable,
        entity_column: str,
        owner: Union[str, "UserRegistrar"],
        features: List[dict],
        timestamp_column: str,
    ) -> None:
        # Import here to avoid circular dependency
        from ..registrar import FeatureColumnResource

        for entity in entities:
            for feature in features:
                feature_definition = dict(feature)
                feature_column = feature_definition["column"]
                feature_variant = feature_definition.get("variant", "")
                feature_type = feature_definition["type"]
                feature_description = feature_definition.get("description", "")
                feature_tags = feature_definition.get("tags")
                feature_properties = feature_definition.get("properties")
                feature_resource_config = feature_definition.get(
                    "resource_snowflake_config"
                )

                per_feature_timestamp = feature_definition.get("timestamp_column", "")
                if per_feature_timestamp:
                    per_feature_timestamp = self._normalize_timestamp_column(
                        per_feature_timestamp
                    )

                feature_columns = [entity_column, feature_column]
                if per_feature_timestamp:
                    feature_columns.append(per_feature_timestamp)
                elif timestamp_column:
                    feature_columns.append(timestamp_column)

                transformation_args = transformation[feature_columns]

                feature_resource = FeatureColumnResource(
                    transformation_args=transformation_args,
                    type=feature_type,
                    entity=entity,
                    name=feature_definition["name"],
                    variant=feature_variant,
                    owner=owner,
                    timestamp_column=""
                    if len(feature_columns) == 3
                    else per_feature_timestamp,
                    description=feature_description,
                    tags=feature_tags,
                    properties=feature_properties,
                    resource_snowflake_config=feature_resource_config,
                )

                feature_resource.register()

    def incremental_df_transformation(
        self,
        variant: str = "",
        owner: Union[str, "UserRegistrar"] = "",
        name: str = "",
        schedule: str = "",
        inputs: Optional[list] = None,
        description: str = "",
        tags: Optional[List[str]] = None,
        properties: Optional[dict] = None,
        partition_options: Optional[PartitionType] = None,
        max_job_duration: timedelta = timedelta(hours=48),
        spark_params: Optional[Dict[str, str]] = None,
        write_options: Optional[Dict[str, str]] = None,
        table_properties: Optional[Dict[str, str]] = None,
    ):
        # Import here to avoid circular dependency
        from ..registrar import Incremental

        tags, properties = set_tags_properties(tags, properties)
        reg_inputs = []
        inc_inputs = []
        inputs = inputs or []
        for i in inputs:
            if isinstance(i, Incremental):
                unwrapped = i.resource
                reg_inputs.append(unwrapped)
                inc_inputs.append(unwrapped)
            else:
                reg_inputs.append(i)

        return self.__registrar.df_transformation(
            name=name,
            variant=variant,
            owner=owner,
            provider=self.name(),
            description=description,
            inputs=reg_inputs,
            tags=tags,
            properties=properties,
            incremental=True,
            incremental_inputs=inc_inputs,
            partition_options=partition_options,
            max_job_duration=max_job_duration,
            spark_params=spark_params,
            write_options=write_options,
            table_properties=table_properties,
        )

    def register_training_set(
        self,
        name: str,
        variant: str = "",
        features: list = [],
        label: "NameVariant" = ("", ""),
        resources: list = [],
        owner: Union[str, "UserRegistrar"] = "",
        description: str = "",
        schedule: str = "",
        tags: List[str] = [],
        properties: dict = {},
        type: TrainingSetType = TrainingSetType.DYNAMIC,
    ):
        """Register a training set on the Spark provider.

        **Example**:
        ```
        spark.register_training_set(
            name="my_training_set",
            label=("label", "v1"),
            features=[("feature1", "v1"), ("feature2", "v1")],
        )
        ```

        Args:
            name (str): Name of training set to be registered
            variant (str): Name of variant to be registered
            label (NameVariant): Label of training set
            features (List[NameVariant]): Features of training set
            resources (List[Resource]): A list of previously registered resources
            owner (Union[str, "UserRegistrar"]): Owner
            description (str): Description of training set to be registered
            schedule (str): Kubernetes CronJob schedule string ("* * * * *")
            tags (List[str]): Optional grouping mechanism for resources
            properties (dict): Optional grouping mechanism for resources

        Returns:
            resource (ResourceRegistrar): resource
        """
        return self.__registrar.register_training_set(
            name=name,
            variant=variant,
            features=features,
            label=label,
            resources=resources,
            owner=owner,
            description=description,
            schedule=schedule,
            tags=tags,
            properties=properties,
            provider=self.name(),
            type=type,
        )

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, OfflineSparkProvider):
            return False
        return (
            self.__provider == __value.__provider
            and self.__registrar == __value.__registrar
        )


class OfflineK8sProvider(OfflineProvider):
    def __init__(self, registrar, provider):
        super().__init__(registrar, provider)
        self.__registrar = registrar
        self.__provider = provider

    def register_file(
        self,
        name: str,
        path: str,
        variant: str = "",
        owner: Union[str, "UserRegistrar"] = "",
        description: str = "",
        tags: List[str] = [],
        properties: dict = {},
    ):
        """Register a Kubernetes Runner data source as a primary data source.

        **Examples**

        ```
        k8s = client.get_provider("my_k8s")
        transactions = k8s.register_file(
            name="transactions",
            variant="quickstart",
            description="A dataset of fraudulent transactions",
            file_path="s3://featureform-spark/featureform/transactions.parquet"
        )
        ```

        Args:
            name (str): Name of table to be registered
            variant (str): Name of variant to be registered
            path (str): The path to blob store file
            owner (Union[str, "UserRegistrar"]): Owner
            description (str): Description of table to be registered

        Returns:
            source (ColumnSourceRegistrar): source
        """
        FilePrefix.validate(self.__provider.config.store_type, path)

        return self.__registrar.register_primary_data(
            name=name,
            variant=variant,
            location=SQLTable(path),
            owner=owner,
            provider=self.name(),
            description=description,
            tags=tags,
            properties=properties,
        )

    def sql_transformation(
        self,
        variant: str = "",
        owner: Union[str, "UserRegistrar"] = "",
        name: str = "",
        schedule: str = "",
        inputs: list = None,
        description: str = "",
        docker_image: str = "",
        resource_specs: Union[K8sResourceSpecs, None] = None,
        tags: List[str] = [],
        properties: dict = {},
    ):
        """
        Register a SQL transformation source. The k8s.sql_transformation decorator takes the returned string in the
        following function and executes it as a SQL Query.

        The name of the function is the name of the resulting source.

        Sources for the transformation can be specified by adding the Name and Variant in brackets '{{ name.variant }}'.
        The correct source is substituted when the query is run.

        **Examples**:
        ``` py
        @k8s.sql_transformation(variant="quickstart")
        def average_user_transaction():
            return "SELECT CustomerID as user_id, avg(TransactionAmount) as avg_transaction_amt from {{transactions.v1}} GROUP BY user_id"
        ```

        Args:
            name (str): Name of source
            variant (str): Name of variant
            owner (Union[str, "UserRegistrar"]): Owner
            inputs (list): A list of Source NameVariant Tuples to input into the transformation
            description (str): Description of primary data to be registered
            docker_image (str): A custom Docker image to run the transformation
            resource_specs (K8sResourceSpecs): Custom resource requests and limits


        Returns:
            source (ColumnSourceRegistrar): Source
        """
        return self.__registrar.sql_transformation(
            name=name,
            variant=variant,
            owner=owner,
            schedule=schedule,
            provider=self.name(),
            description=description,
            inputs=inputs,
            args=K8sArgs(docker_image=docker_image, specs=resource_specs),
            tags=tags,
            properties=properties,
        )

    def df_transformation(
        self,
        variant: str = "",
        owner: Union[str, "UserRegistrar"] = "",
        name: str = "",
        description: str = "",
        inputs: list = [],
        docker_image: str = "",
        resource_specs: Union[K8sResourceSpecs, None] = None,
        tags: List[str] = [],
        properties: dict = {},
    ):
        """
        Register a Dataframe transformation source. The k8s.df_transformation decorator takes the contents
        of the following function and executes the code it contains at serving time.

        The name of the function is used as the name of the source when being registered.

        The specified inputs are loaded into dataframes that can be accessed using the function parameters.

        **Examples**:
        ``` py
        @k8s.df_transformation(inputs=[("source", "one")])        # Sources are added as inputs
        def average_user_transaction(df):                         # Sources can be manipulated by adding them as params
            return df
        ```

        Args:
            name (str): Name of source
            variant (str): Name of variant
            owner (Union[str, "UserRegistrar"]): Owner
            description (str): Description of primary data to be registered
            inputs (list[Tuple(str, str)]): A list of Source NameVariant Tuples to input into the transformation
            docker_image (str): A custom Docker image to run the transformation
            resource_specs (K8sResourceSpecs): Custom resource requests and limits

        Returns:
            source (ColumnSourceRegistrar): Source
        """
        return self.__registrar.df_transformation(
            name=name,
            variant=variant,
            owner=owner,
            provider=self.name(),
            description=description,
            inputs=inputs,
            args=K8sArgs(docker_image=docker_image, specs=resource_specs),
            tags=tags,
            properties=properties,
        )
