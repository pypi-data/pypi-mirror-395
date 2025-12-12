# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Main Registrar class for Featureform.

This module contains the Registrar class which is the core registration engine
for all Featureform resources.
"""

import warnings
from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from ..config import *
from ..config.compute import K8sArgs
from ..config.offline_stores import ResourceSnowflakeConfig
from ..enums import (
    ScalarType,
    TrainingSetType,
)
from ..resources import *
from ..secret_provider import Secret
from ..state import ResourceRedefinedError, ResourceState
from ..types import VectorType
from ..utils.helpers import set_tags_properties
from ..variant_names_generator import get_current_timestamp_variant

if TYPE_CHECKING:
    from ..resources import Resource

# Import from other registrar modules
# Import provider classes
from ..providers import (
    FileStoreProvider,
    KafkaProvider,
    OfflineK8sProvider,
    OfflineProvider,
    OfflineSparkProvider,
    OfflineSQLProvider,
    OnlineProvider,
)
from .column_mapping import ColumnMapping
from .column_resources import (
    FeatureColumnResource,
    LabelColumnResource,
    MultiFeatureColumnResource,
)
from .registrars import (
    ColumnSourceRegistrar,
    EntityRegistrar,
    ResourceRegistrar,
    SourceRegistrar,
    UserRegistrar,
)
from .transformation_decorators import (
    DFTransformationDecorator,
    SQLTransformationDecorator,
)

__all__ = ["Registrar", "Incremental", "Stream"]

# Constants for provider configuration
s3_config = S3StoreConfig("", "", AWSStaticCredentials("id", "secret"))
NON_INFERENCE_STORES = [s3_config.type()]
ONE_DAY_TARGET_LAG = "1 days"


@dataclass
class Incremental:
    resource: "Resource"


@dataclass
class Stream:
    resource: "Resource"


class Registrar:
    """These functions are used to register new resources and retrieving existing resources.
    Retrieved resources can be used to register additional resources.

    ``` py title="definitions.py"
    import featureform as ff

    # e.g. registering a new provider
    redis = ff.register_redis(
        name="redis-quickstart",
        host="quickstart-redis",  # The internal dns name for redis
        port=6379,
        description="A Redis deployment we created for the Featureform quickstart"
    )
    ```
    """

    def __init__(self):
        self.__state = ResourceState()
        self.__resources = []
        self.__default_owner = ""
        self.__variant_prefix = ""
        self.__run = get_current_timestamp_variant(prefix=self.__variant_prefix)

        """
        maps client objects (feature object, label object, source decorators) to their resource in the event we want 
        to update the client object after the resource was created
        
        Introduced for timestamp variants where updates during a resource create ensures that the client object
        has the correct variant when being used as a dependency other resources
        """
        self.__client_obj_to_resource_map = {}

    def add_resource(self, resource):
        self.__resources.append(resource)

    def map_client_object_to_resource(
        self, client_obj, resource_variant: ResourceVariant
    ):
        self.__client_obj_to_resource_map[resource_variant.to_key()] = client_obj

    def get_client_objects_for_resource(self):
        return self.__client_obj_to_resource_map

    def get_resources(self):
        return self.__resources

    @staticmethod
    def _normalize_entity_reference(entity: Union[str, EntityRegistrar, Entity]) -> str:
        if isinstance(entity, str):
            cleaned = entity.strip()
            if cleaned == "":
                raise ValueError("Entity references must be non-empty strings")
            return cleaned
        if isinstance(entity, EntityRegistrar):
            return entity.name()
        if isinstance(entity, Entity):
            if not isinstance(entity.name, str) or entity.name.strip() == "":
                raise ValueError("Entity references must have a non-empty name")
            return entity.name
        raise TypeError(
            "Entity references must be provided as a key string, EntityRegistrar, or Entity"
        )

    def register_user(
        self, name: str, tags: List[str] = [], properties: dict = {}
    ) -> UserRegistrar:
        """Register a user.

        Args:
            name (str): User to be registered.

        Returns:
            UserRegistrar: User
        """
        user = User(name=name, tags=tags, properties=properties)
        self.__resources.append(user)
        return UserRegistrar(self, user)

    def set_default_owner(self, user: str):
        """Set default owner.

        Args:
            user (str): User to be set as default owner of resources.
        """
        self.__default_owner = user

    def default_owner(self) -> str:
        return self.__default_owner

    def must_get_default_owner(self) -> str:
        owner = self.default_owner()
        if owner == "":
            raise ValueError("Owner must be set or a default owner must be specified.")
        return owner

    def set_variant_prefix(self, variant_prefix: str = ""):
        """Set variant prefix.

        Args:
            variant_prefix (str): variant prefix to be set.
        """
        self.__variant_prefix = variant_prefix
        self.set_run()

    def set_run(self, run: str = ""):
        """

        **Example 1**: Using set_run() without arguments will generate a timestamp run name.
        ``` py
        import featureform as ff
        ff.set_run()

        postgres.register_table(
            name="transactions",
            table="transactions_table",
        )

        # Applying will register the source as name=transactions, variant=2025-10-31t06-05-32

        ```

        **Example 2**: Using set_run() with arguments will set the variant to the provided name.
        ``` py
        import featureform as ff
        ff.set_run("last_30_days")

        postgres.register_table(
            name="transactions",
            table="transactions_table",
        )

        # Applying will register the source as name=transactions, variant=last_30_days
        ```

        **Example 3**: Generated and set variant names can be used together
        ``` py
        import featureform as ff
        ff.set_run()

        file = spark.register_file(
            name="transactions",
            path="my/transactions.parquet",
            variant="last_30_days"
        )

        @spark.df_transformation(inputs=[file]):
        def customer_count(transactions):
            return transactions.groupBy("CustomerID").count()


        # Applying without a variant for the dataframe transformation will result in
        # the transactions source having a variant of last_30_days and the transformation
        # having a timestamp variant (e.g. 2025-10-31t06-05-32)
        ```

        **Example 4**: This also works within SQL Transformations
        ``` py
        import featureform as ff
        ff.set_run("last_30_days")

        @postgres.sql_transformation():
        def my_transformation():
            return "SELECT CustomerID, Amount FROM {{ transactions }}"

        # The variant will be autofilled so the SQL query is returned as:
        # "SELECT CustomerID, Amount FROM {{ transactions.last_30_days }}"
        ```

        Args:
            run (str): Name of a run to be set.
        """
        if run == "":
            self.__run = get_current_timestamp_variant(prefix=self.__variant_prefix)
        else:
            self.__run = run

    def get_run(self) -> str:
        """
        Get the current run name.

        **Examples**:
        ``` py
        import featureform as ff

        client = ff.Client()
        f = client.features(("avg_transaction_amount", ff.get_run()), {"user": "123"})

        ```

        Returns:
            run: The name of the current run
        """
        return self.__run

    def get_source(self, name, variant, local=False):
        """
        get_source() can be used to get a reference to an already registered primary source or transformation.
        The returned object can be used to register features and labels or be extended off of to create additional
        transformations.

        **Examples**:

        Registering a transformation from an existing source.
        ``` py
        spark = ff.get_spark("prod-spark")
        transactions = ff.get_source("transactions","kaggle")

        @spark.df_transformation(inputs=[transactions]):
        def customer_count(transactions):
            return transactions.groupBy("CustomerID").count()
        ```

        Registering a feature from an existing source.
        ``` py
        transactions = ff.get_source("transactions","kaggle")

        transactions.register_resources(
            entity=user,
            entity_column="customerid",
            labels=[
                {"name": "fraudulent", "variant": "quickstart", "column": "isfraud", "type": "bool"},
            ],
        )
        ```

        Args:
            name (str): Name of source to be retrieved
            variant (str): Name of variant of source to be retrieved
            local (bool): If localmode is being used

        Returns:
            source (ColumnSourceRegistrar): Source
        """
        if local:
            raise Exception(
                "Localmode is not supported; please try featureform <= 1.12.0"
            )
        else:
            mock_definition = PrimaryData(location=SQLTable(name=""))
            mock_source = SourceVariant(
                created=None,
                name=name,
                variant=variant,
                definition=mock_definition,
                owner="",
                provider="",
                description="",
                tags=[],
                properties={},
            )
            return ColumnSourceRegistrar(self, mock_source)

    def get_redis(self, name):
        """Get a Redis provider. The returned object can be used to register additional resources.

        **Examples**:
        ``` py
        redis = ff.get_redis("redis-quickstart")

        average_user_transaction.register_resources(
            entity=user,
            entity_column="user_id",
            inference_store=redis,
            features=[
                {"name": "avg_transactions", "variant": "quickstart", "column": "avg_transaction_amt", "type": "float32"},
            ],
        )
        ```

        Args:
            name (str): Name of Redis provider to be retrieved

        Returns:
            redis (OnlineProvider): Provider
        """
        warnings.warn(
            "Use client.get_redis instead",
            DeprecationWarning,
        )
        mock_config = RedisConfig(host="", port=123, password="", db=123)
        mock_provider = Provider(
            name=name, function="ONLINE", description="", team="", config=mock_config
        )
        return OnlineProvider(self, mock_provider)

    def get_dynamodb(self, name: str):
        """Get a DynamoDB provider. The returned object can be used as an inference store in feature registration.

        **Examples**:
        ``` py
        dynamodb = ff.get_dynamodb("dynamodb-quickstart")

        @ff.entity
        class User:
            avg_transactions = ff.Feature(
                average_user_transaction[["user_id", "avg_transaction_amt"]],
                type=ff.Float32,
                inference_store=dynamodb,
            )
        ```

        Args:
            name (str): Name of DynamoDB provider to be retrieved

        Returns:
            dynamodb (OnlineProvider): Provider
        """
        warnings.warn(
            "Use client.get_dynamodb instead",
            DeprecationWarning,
        )
        mock_config = DynamodbConfig(
            region="",
            access_key="",
            secret_key="",
        )
        mock_provider = Provider(
            name=name, function="ONLINE", description="", team="", config=mock_config
        )
        return OnlineProvider(self, mock_provider)

    def get_mongodb(self, name: str):
        """Get a MongoDB provider. The returned object can be used to register additional resources.

        **Examples**:
        ``` py
        mongodb = ff.get_mongodb("mongodb-quickstart")

        average_user_transaction.register_resources(
            entity=user,
            entity_column="user_id",
            inference_store=mongodb,
            features=[
                {"name": "avg_transactions", "variant": "quickstart", "column": "avg_transaction_amt", "type": "float32"},
            ],
        )
        ```

        Args:
            name (str): Name of MongoDB provider to be retrieved

        Returns:
            mongodb (OnlineProvider): Provider
        """
        warnings.warn(
            "Use client.get_mongodb instead",
            DeprecationWarning,
        )
        mock_config = MongoDBConfig(
            username="", password="", host="", port="", database="", throughput=1
        )
        mock_provider = Provider(
            name=name, function="ONLINE", description="", team="", config=mock_config
        )
        return OnlineProvider(self, mock_provider)

    def get_blob_store(self, name):
        """Get an Azure Blob provider. The returned object can be used to register additional resources.

        **Examples**:
        ``` py
        azure_blob = ff.get_blob_store("azure-blob-quickstart")

        average_user_transaction.register_resources(
            entity=user,
            entity_column="user_id",
            inference_store=azure_blob,
            features=[
                {"name": "avg_transactions", "variant": "quickstart", "column": "avg_transaction_amt", "type": "float32"},
            ],
        )
        ```

        Args:
            name (str): Name of Azure blob provider to be retrieved

        Returns:
            azure_blob (FileStoreProvider): Provider
        """
        warnings.warn(
            "Use client.get_blob_store instead",
            DeprecationWarning,
        )
        fake_azure_config = AzureFileStoreConfig(
            account_name="", account_key="", container_name="", root_path=""
        )
        fake_config = OnlineBlobConfig(
            store_type="AZURE", store_config=fake_azure_config.config()
        )
        mock_provider = Provider(
            name=name, function="ONLINE", description="", team="", config=fake_config
        )
        return FileStoreProvider(self, mock_provider, fake_config, "AZURE")

    def get_postgres(self, name):
        """Get a Postgres provider. The returned object can be used to register additional resources.

        **Examples**:
        ``` py
        postgres = ff.get_postgres("postgres-quickstart")
        transactions = postgres.register_table(
            name="transactions",
            variant="kaggle",
            description="Fraud Dataset From Kaggle",
            table="Transactions",  # This is the table's name in Postgres
        )
        ```

        Args:
            name (str): Name of Postgres provider to be retrieved

        Returns:
            postgres (OfflineSQLProvider): Provider
        """
        warnings.warn(
            "Use client.get_postgres instead",
            DeprecationWarning,
        )
        mock_config = PostgresConfig(
            host="",
            port="",
            database="",
            user="",
            password="",
            sslmode="",
        )
        mock_provider = Provider(
            name=name, function="OFFLINE", description="", team="", config=mock_config
        )
        return OfflineSQLProvider(self, mock_provider)

    def get_clickhouse(self, name):
        """Get a ClickHouse provider. The returned object can be used to register additional resources.

        **Examples**:
        ``` py
        clickhouse = ff.get_clickhouse("clickhouse-quickstart")
        transactions = clickhouse.register_table(
            name="transactions",
            variant="kaggle",
            description="Fraud Dataset From Kaggle",
            table="Transactions",  # This is the table's name in ClickHouse
        )
        ```

        Args:
            name (str): Name of ClickHouse provider to be retrieved

        Returns:
            clickhouse (OfflineSQLProvider): Provider
        """
        warnings.warn(
            "Use client.get_clickhouse instead",
            DeprecationWarning,
        )
        mock_config = ClickHouseConfig(
            host="",
            port=9000,
            database="",
            user="",
            password="",
            ssl=False,
        )
        mock_provider = Provider(
            name=name, function="OFFLINE", description="", team="", config=mock_config
        )
        return OfflineSQLProvider(self, mock_provider)

    def get_snowflake(self, name):
        """Get a Snowflake provider. The returned object can be used to register additional resources.

        **Examples**:
        ``` py
        snowflake = ff.get_snowflake("snowflake-quickstart")
        transactions = snowflake.register_table(
            name="transactions",
            variant="kaggle",
            description="Fraud Dataset From Kaggle",
            table="Transactions",  # This is the table's name in Postgres
        )
        ```

        Args:
            name (str): Name of Snowflake provider to be retrieved

        Returns:
            snowflake (OfflineSQLProvider): Provider
        """
        warnings.warn(
            "Use client.get_snowflake instead",
            DeprecationWarning,
        )
        mock_config = SnowflakeConfig(
            account="ff_fake",
            database="ff_fake",
            organization="ff_fake",
            username="ff_fake",
            password="ff_fake",
            schema="ff_fake",
        )
        mock_provider = Provider(
            name=name, function="OFFLINE", description="", team="", config=mock_config
        )
        return OfflineSQLProvider(self, mock_provider)

    def get_snowflake_legacy(self, name: str):
        """Get a Snowflake provider. The returned object can be used to register additional resources.

        **Examples**:
        ``` py
        snowflake = ff.get_snowflake_legacy("snowflake-quickstart")
        transactions = snowflake.register_table(
            name="transactions",
            variant="kaggle",
            description="Fraud Dataset From Kaggle",
            table="Transactions",  # This is the table's name in Postgres
        )
        ```

        Args:
            name (str): Name of Snowflake provider to be retrieved

        Returns:
            snowflake_legacy (OfflineSQLProvider): Provider
        """
        warnings.warn(
            "Use client.get_snowflake_legacy instead",
            DeprecationWarning,
        )
        mock_config = SnowflakeConfig(
            account_locator="ff_fake",
            database="ff_fake",
            username="ff_fake",
            password="ff_fake",
            schema="ff_fake",
            warehouse="ff_fake",
            role="ff_fake",
        )
        mock_provider = Provider(
            name=name, function="OFFLINE", description="", team="", config=mock_config
        )
        return OfflineSQLProvider(self, mock_provider)

    def get_redshift(self, name):
        """Get a Redshift provider. The returned object can be used to register additional resources.

        **Examples**:
        ``` py
        redshift = ff.get_redshift("redshift-quickstart")
        transactions = redshift.register_table(
            name="transactions",
            variant="kaggle",
            description="Fraud Dataset From Kaggle",
            table="Transactions",  # This is the table's name in Postgres
        )
        ```

        Args:
            name (str): Name of Redshift provider to be retrieved

        Returns:
            redshift (OfflineSQLProvider): Provider
        """
        warnings.warn(
            "Use client.get_redshift instead",
            DeprecationWarning,
        )
        mock_config = RedshiftConfig(
            host="", port="5439", database="", user="", password="", sslmode=""
        )
        mock_provider = Provider(
            name=name, function="OFFLINE", description="", team="", config=mock_config
        )
        return OfflineSQLProvider(self, mock_provider)

    def get_bigquery(self, name):
        """Get a BigQuery provider. The returned object can be used to register additional resources.

        **Examples**:
        ``` py
        bigquery = ff.get_bigquery("bigquery-quickstart")
        transactions = bigquery.register_table(
            name="transactions",
            variant="kaggle",
            description="Fraud Dataset From Kaggle",
            table="Transactions",  # This is the table's name in BigQuery
        )
        ```

        Args:
            name (str): Name of BigQuery provider to be retrieved

        Returns:
            bigquery (OfflineSQLProvider): Provider
        """
        warnings.warn(
            "Use client.get_bigquery instead",
            DeprecationWarning,
        )
        mock_config = BigQueryConfig(
            project_id="mock_project",
            dataset_id="mock_dataset",
            credentials=GCPCredentials(
                project_id="mock_project",
                credentials_path="client/tests/test_files/bigquery_dummy_credentials.json",
            ),
        )
        mock_provider = Provider(
            name=name, function="OFFLINE", description="", team="", config=mock_config
        )
        return OfflineSQLProvider(self, mock_provider)

    def get_spark(self, name):
        """Get a Spark provider. The returned object can be used to register additional resources.

        **Examples**:
        ``` py
        spark = ff.get_spark("spark-quickstart")
        transactions = spark.register_file(
            name="transactions",
            variant="kaggle",
            description="Fraud Dataset From Kaggle",
            file_path="s3://bucket/path/to/file/transactions.parquet",  # This is the path to file
        )
        ```

        Args:
            name (str): Name of Spark provider to be retrieved

        Returns:
            spark (OfflineSQLProvider): Provider
        """
        warnings.warn(
            "Use client.get_spark instead",
            DeprecationWarning,
        )
        mock_config = SparkConfig(
            executor_type="", executor_config={}, store_type="", store_config={}
        )
        mock_provider = Provider(
            name=name, function="OFFLINE", description="", team="", config=mock_config
        )
        return OfflineSparkProvider(self, mock_provider)

    def get_kubernetes(self, name):
        """
        Get a k8s provider. The returned object can be used to register additional resources.

        **Examples**:
        ``` py

        k8s = ff.get_kubernetes("k8s-azure-quickstart")
        transactions = k8s.register_file(
            name="transactions",
            variant="kaggle",
            description="Fraud Dataset From Kaggle",
            path="path/to/blob",
        )
        ```

        Args:
            name (str): Name of k8s provider to be retrieved

        Returns:
            k8s (OfflineK8sProvider): Provider
        """
        warnings.warn(
            "Use client.get_kubernetes instead",
            DeprecationWarning,
        )
        mock_config = K8sConfig(store_type="", store_config={})
        mock_provider = Provider(
            name=name, function="OFFLINE", description="", team="", config=mock_config
        )
        return OfflineK8sProvider(self, mock_provider)

    def get_s3(self, name):
        """
        Get a S3 provider. The returned object can be used with other providers such as Spark and Databricks.

        **Examples**:

        ``` py

        s3 = ff.get_s3("s3-quickstart")
        spark = ff.register_spark(
            name=f"spark-emr-s3",
            description="A Spark deployment we created for the Featureform quickstart",
            team="featureform-team",
            executor=emr,
            filestore=s3,
        )
        ```

        Args:
            name (str): Name of S3 to be retrieved

        Returns:
            s3 (FileStore): Provider
        """
        warnings.warn(
            "Use client.get_s3 instead",
            DeprecationWarning,
        )
        provider = Provider(
            name=name,
            function="OFFLINE",
            description="description",
            team="team",
            config=s3_config,
        )
        return FileStoreProvider(
            registrar=self,
            provider=provider,
            config=s3_config,
            store_type=s3_config.type(),
        )

    def get_gcs(self, name):
        warnings.warn(
            "Use client.get_gcs instead",
            DeprecationWarning,
        )
        filePath = "provider/connection/mock_credentials.json"
        fake_creds = GCPCredentials(project_id="id", credentials_path=filePath)
        mock_config = GCSFileStoreConfig(
            bucket_name="", bucket_path="", credentials=fake_creds
        )
        mock_provider = Provider(
            name=name, function="OFFLINE", description="", team="", config=mock_config
        )
        return OfflineK8sProvider(self, mock_provider)

    def _create_mock_creds_file(self, filename, json_data):
        with open(filename, "w") as f:
            json.dumps(json_data, f)

    def get_entity(self, name: str):
        """Get an entity. The returned object can be used to register additional resources.

        **Examples**:

        ``` py
        entity = get_entity("user")
        transactions.register_resources(
            entity=entity,
            entity_column="customerid",
            labels=[
                {"name": "fraudulent", "variant": "quickstart", "column": "isfraud", "type": "bool"},
            ],
        )
        ```

        Args:
            name (str): Name of entity to be retrieved
        Returns:
            entity (EntityRegistrar): Entity
        """
        fakeEntity = Entity(
            name=name, description="", status="", tags=[], properties={}
        )
        return EntityRegistrar(self, fakeEntity)

    def register_redis(
        self,
        name: str,
        host: str,
        port: int = 6379,
        db: int = 0,
        password: str = "",
        ssl_mode: bool = False,
        description: str = "",
        team: str = "",
        tags: Optional[List[str]] = None,
        properties: Optional[dict] = None,
    ):
        """Register a Redis provider.

        **Examples**:
        ```
        redis = ff.register_redis(
            name="redis-quickstart",
            host="quickstart-redis",
            port=6379,
            password="password",
            description="A Redis deployment we created for the Featureform quickstart"
        )
        ```

        Args:
            name (str): (Immutable) Name of Redis provider to be registered
            host (str): (Immutable) Hostname for Redis
            db (str): (Immutable) Redis database number
            port (int): (Mutable) Redis port
            password (str): (Mutable) Redis password
            ssl_mode (bool): (Mutable) Enable SSL for Redis connection
            description (str): (Mutable) Description of Redis provider to be registered
            team (str): (Mutable) Name of team
            tags (Optional[List[str]]): (Mutable) Optional grouping mechanism for resources
            properties (Optional[dict]): (Mutable) Optional grouping mechanism for resources

        Returns:
            redis (OnlineProvider): Provider
        """
        tags, properties = set_tags_properties(tags, properties)
        config = RedisConfig(
            host=host, port=port, password=password, db=db, ssl_mode=ssl_mode
        )
        provider = Provider(
            name=name,
            function="ONLINE",
            description=description,
            team=team,
            config=config,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(provider)
        return OnlineProvider(self, provider)

    def register_pinecone(
        self,
        name: str,
        project_id: str,
        environment: str,
        api_key: str,
        description: str = "",
        team: str = "",
        tags: List[str] = [],
        properties: dict = {},
    ):
        """Register a Pinecone provider.

        **Examples**:
        ```
        pinecone = ff.register_pinecone(
            name="pinecone-quickstart",
            project_id="2g13ek7",
            environment="us-west4-gcp-free",
            api_key="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        )
        ```

        Args:
            name (str): (Immutable) Name of Pinecone provider to be registered
            project_id (str): (Immutable) Pinecone project id
            environment (str): (Immutable) Pinecone environment
            api_key (str): (Mutable) Pinecone api key
            description (str): (Mutable) Description of Pinecone provider to be registered
            team (str): (Mutable) Name of team
            tags (List[str]): (Mutable) Optional grouping mechanism for resources
            properties (dict): (Mutable) Optional grouping mechanism for resources

        Returns:
            pinecone (OnlineProvider): Provider
        """

        tags, properties = set_tags_properties(tags, properties)
        config = PineconeConfig(
            project_id=project_id, environment=environment, api_key=api_key
        )
        provider = Provider(
            name=name,
            function="ONLINE",
            description=description,
            team=team,
            config=config,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(provider)
        return OnlineProvider(self, provider)

    def register_weaviate(
        self,
        name: str,
        url: str,
        api_key: str,
        description: str = "",
        team: str = "",
        tags: List[str] = [],
        properties: dict = {},
    ):
        """Register a Weaviate provider.

        **Examples**:
        ```
        weaviate = ff.register_weaviate(
            name="weaviate-quickstart",
            url="https://<CLUSTER NAME>.weaviate.network",
            api_key="<API KEY>"
            description="A Weaviate project for using embeddings in Featureform"
        )
        ```

        Args:
            name (str): (Immutable) Name of Weaviate provider to be registered
            url (str): (Immutable) Endpoint of Weaviate cluster, either in the cloud or via another deployment operation
            api_key (str): (Mutable) Weaviate api key
            description (str): (Mutable) Description of Weaviate provider to be registered
            team (str): (Mutable) Name of team
            tags (List[str]): (Mutable) Optional grouping mechanism for resources
            properties (dict): (Mutable) Optional grouping mechanism for resources

        Returns:
            weaviate (OnlineProvider): Provider
        """
        config = WeaviateConfig(url=url, api_key=api_key)
        provider = Provider(
            name=name,
            function="ONLINE",
            description=description,
            team=team,
            config=config,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(provider)
        return OnlineProvider(self, provider)

    def register_blob_store(
        self,
        name: str,
        account_name: str,
        account_key: str,
        container_name: str,
        root_path: str,
        description: str = "",
        team: str = "",
        tags=None,
        properties=None,
    ):
        """Register an Azure Blob Store provider.

        Azure Blob Storage can be used as the storage component for Spark or the Featureform Pandas Runner.

        **Examples**:
        ```
        blob = ff.register_blob_store(
            name="azure-quickstart",
            container_name="my_company_container"
            root_path="custom/path/in/container"
            account_name=<azure_account_name>
            account_key=<azure_account_key>
            description="An azure blob store provider to store offline and inference data"
        )
        ```

        Args:
            name (str): (Immutable) Name of Azure blob store to be registered
            container_name (str): (Immutable) Azure container name
            root_path (str): (Immutable) A custom path in container to store data
            account_name (str): (Immutable) Azure account name
            account_key (str):  (Mutable) Secret azure account key
            description (str): (Mutable) Description of Azure Blob provider to be registered
            team (str): (Mutable) The name of the team registering the filestore
            tags (List[str]): (Mutable) Optional grouping mechanism for resources
            properties (dict): (Mutable) Optional grouping mechanism for resources

        Returns:
            blob (StorageProvider): Provider
                has all the functionality of OnlineProvider
        """

        tags, properties = set_tags_properties(tags, properties)

        container_name = container_name.replace("abfss://", "")
        if "/" in container_name:
            raise ValueError(
                "container_name cannot contain '/'. container_name should be the name of the Azure Blobstore container only."
            )

        azure_config = AzureFileStoreConfig(
            account_name=account_name,
            account_key=account_key,
            container_name=container_name,
            root_path=root_path,
        )
        config = OnlineBlobConfig(
            store_type="AZURE", store_config=azure_config.config()
        )

        provider = Provider(
            name=name,
            function="ONLINE",
            description=description,
            team=team,
            config=config,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(provider)
        return FileStoreProvider(self, provider, azure_config, "AZURE")

    def register_kafka(
        self,
        name: str,
        kafka_config: KafkaConfig,
        description: str = "",
        tags: Optional[List[str]] = None,
        properties: Optional[dict] = None,
    ) -> KafkaProvider:
        """
        Register a Kafka provider.

        Kafka can be used as a source for Spark

        **Examples**:
        ```
        kafka = ff.register_kafka(
            name="kafka-quickstart",
            bootstrap_servers="localhost:9092",
            description="A Kafka provider to stream data into Spark"
        )
        ```
        """

        tags, properties = set_tags_properties(tags, properties)

        provider = Provider(
            name=name,
            function="OFFLINE",
            description=description,
            config=kafka_config,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(provider)
        return KafkaProvider(self, provider)

    def register_vault(
        self,
        name: str,
        address: str,
        token: str,
        description: str = "",
        mount_path: str = "secret",
        default_secret_path: str = "",
    ):
        config = VaultConfig(
            address=address,
            token=token,
            mount_path=mount_path,
            default_secret_path=default_secret_path,
        )
        provider = Provider(
            name=name,
            function="SECRETS",
            description=description,
            config=config,
        )

        self.__resources.append(provider)
        return VaultSecretProvider(config.default_secret_path, name)

    def register_s3(
        self,
        name: str,
        credentials: Union[AWSStaticCredentials, AWSAssumeRoleCredentials],
        bucket_region: str,
        bucket_name: str,
        path: str = "",
        description: str = "",
        team: str = "",
        tags: Optional[List[str]] = None,
        properties: Optional[dict] = None,
    ):
        """Register a S3 store provider.

        This has the functionality of an offline store and can be used as a parameter
        to a k8s or spark provider

        **Examples**:
        ```
        s3 = ff.register_s3(
            name="s3-quickstart",
            credentials=aws_creds,
            bucket_name="bucket_name",
            bucket_region=<bucket_region>,
            path="path/to/store/featureform_files/in/",
            description="An s3 store provider to store offline"
        )
        ```

        Args:
            name (str): (Immutable) Name of S3 store to be registered
            bucket_name (str): (Immutable) AWS Bucket Name
            bucket_region (str): (Immutable) AWS region the bucket is located in
            path (str): (Immutable) The path used to store featureform files in
            credentials (Union[AWSStaticCredentials, AWSAssumeRoleCredentials]): (Mutable) AWS credentials to access the bucket
            description (str): (Mutable) Description of S3 provider to be registered
            team (str): (Mutable) The name of the team registering the filestore
            tags (List[str]): (Mutable) Optional grouping mechanism for resources
            properties (dict): (Mutable) Optional grouping mechanism for resources

        Returns:
            s3 (FileStoreProvider): Provider
                has all the functionality of OfflineProvider
        """
        tags, properties = set_tags_properties(tags, properties)

        if bucket_name == "":
            raise ValueError("bucket_name is required and cannot be empty string")

        # TODO: add verification into S3StoreConfig
        bucket_name = bucket_name.replace("s3://", "").replace("s3a://", "")

        if "/" in bucket_name:
            raise ValueError(
                "bucket_name cannot contain '/'. bucket_name should be the name of the AWS S3 bucket only."
            )

        s3_config = S3StoreConfig(
            bucket_path=bucket_name,
            bucket_region=bucket_region,
            credentials=credentials,
            path=path,
        )

        provider = Provider(
            name=name,
            function="OFFLINE",
            description=description,
            team=team,
            config=s3_config,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(provider)
        return FileStoreProvider(self, provider, s3_config, s3_config.type())

    def register_gcs(
        self,
        name: str,
        bucket_name: str,
        root_path: str,
        credentials: GCPCredentials,
        description: str = "",
        team: str = "",
        tags: List[str] = [],
        properties: dict = {},
    ):
        """Register a GCS store provider.

        **Examples**:
        ```
        gcs = ff.register_gcs(
            name="gcs-quickstart",
            credentials=ff.GCPCredentials(...),
            bucket_name="bucket_name",
            root_path="featureform/path/",
            description="An gcs store provider to store offline"
        )
        ```

        Args:
            name (str): (Immutable) Name of GCS store to be registered
            bucket_name (str): (Immutable) The bucket name
            root_path (str): (Immutable) Custom path to be used by featureform
            credentials (GCPCredentials): (Mutable) GCP credentials to access the bucket
            description (str): (Mutable) Description of GCS provider to be registered
            team (str): (Mutable) The name of the team registering the filestore
            tags (List[str]): (Mutable) Optional grouping mechanism for resources
            properties (dict): (Mutable) Optional grouping mechanism for resources

        Returns:
            gcs (FileStoreProvider): Provider
                has all the functionality of OfflineProvider
        """
        tags, properties = set_tags_properties(tags, properties)

        if bucket_name == "":
            raise ValueError("bucket_name is required and cannot be empty string")

        bucket_name = bucket_name.replace("gs://", "")
        if "/" in bucket_name:
            raise ValueError(
                "bucket_name cannot contain '/'. bucket_name should be the name of the GCS bucket only."
            )

        gcs_config = GCSFileStoreConfig(
            bucket_name=bucket_name, bucket_path=root_path, credentials=credentials
        )
        provider = Provider(
            name=name,
            function="OFFLINE",
            description=description,
            team=team,
            config=gcs_config,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(provider)
        return FileStoreProvider(self, provider, gcs_config, gcs_config.type())

    def register_hdfs(
        self,
        name: str,
        host: str,
        port: str,
        path: str = "",
        hdfs_site_file: str = "",
        core_site_file: str = "",
        credentials: Union[BasicCredentials, KerberosCredentials] = None,
        description: str = "",
        team: str = "",
        tags: List[str] = [],
        properties: dict = {},
    ):
        """Register a HDFS store provider with support for Kerberos if needed.

        This has the functionality of an offline store and can be used as a parameter
        to a k8s or spark provider

        **Examples**:
        ```
        hdfs = ff.register_hdfs(
            name="hdfs-quickstart",
            host="<host>",
            port="<port>",
            path="<path>",
            credentials=<ff.BasicCredentials or ff.KerberosCredentials>,
            description="An hdfs store provider to store offline"
        )
        ```
        Args:
            name (str): Name of HDFS store to be registered
            host (str): The hostname for HDFS
            port (str): The IPC port for the Namenode for HDFS. (Typically 8020 or 9000)
            path (str): A storage path within HDFS
            core_site_file (str): A path to a core_site config file
            hdfs_site_file (str): A path to a hdfs_site config file
            credentials (Union[BasicCredentials, KerberosCredentials]): Credentials to access HDFS
            description (str): Description of HDFS provider to be registered
            team (str): The name of the team registering HDFS
        Returns:
            hdfs (FileStoreProvider): Provider
        """

        hdfs_config = HDFSConfig(
            host=host,
            port=port,
            path=path,
            credentials=credentials,
            hdfs_site_file=hdfs_site_file,
            core_site_file=core_site_file,
        )

        provider = Provider(
            name=name,
            function="OFFLINE",
            description=description,
            team=team,
            config=hdfs_config,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(provider)
        return FileStoreProvider(self, provider, hdfs_config, hdfs_config.type())

    # TODO: Set Deprecation Warning For Credentials Path
    def register_firestore(
        self,
        name: str,
        collection: str,
        project_id: str,
        credentials: GCPCredentials,
        credentials_path: str = "",
        description: str = "",
        team: str = "",
        tags: List[str] = [],
        properties: dict = {},
    ):
        """Register a Firestore provider.

        **Examples**:
        ```
        firestore = ff.register_firestore(
            name="firestore-quickstart",
            description="A Firestore deployment we created for the Featureform quickstart",
            project_id="quickstart-project",
            collection="quickstart-collection",
            credentials=ff.GCPCredentials(...)
        )
        ```

        Args:
            name (str): (Immutable) Name of Firestore provider to be registered
            project_id (str): (Immutable) The Project name in GCP
            collection (str): (Immutable) The Collection name in Firestore under the given project ID
            credentials (GCPCredentials): (Mutable) GCP credentials to access Firestore
            description (str): (Mutable) Description of Firestore provider to be registered
            team (str): (Mutable) The name of the team registering the filestore
            tags (List[str]): (Mutable) Optional grouping mechanism for resources
            properties (dict): (Mutable) Optional grouping mechanism for resources

        Returns:
            firestore (OfflineSQLProvider): Provider
        """
        tags, properties = set_tags_properties(tags, properties)
        config = FirestoreConfig(
            collection=collection,
            project_id=project_id,
            credentials=credentials,
        )
        provider = Provider(
            name=name,
            function="ONLINE",
            description=description,
            team=team,
            config=config,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(provider)
        return OnlineProvider(self, provider)

    # TODO: Check these fields
    def register_cassandra(
        self,
        name: str,
        host: str,
        port: int,
        username: str,
        password: str,
        keyspace: str,
        consistency: str = "THREE",
        replication: int = 3,
        description: str = "",
        team: str = "",
        tags: List[str] = [],
        properties: dict = {},
    ):
        """Register a Cassandra provider.

        **Examples**:
        ```
        cassandra = ff.register_cassandra(
                name = "cassandra",
                description = "Example inference store",
                team = "Featureform",
                host = "0.0.0.0",
                port = 9042,
                username = "cassandra",
                password = "cassandra",
                consistency = "THREE",
                replication = 3
            )
        ```

        Args:
            name (str): (Immutable) Name of Cassandra provider to be registered
            host (str): (Immutable) DNS name of Cassandra
            port (str): (Mutable) Port
            username (str): (Mutable) Username
            password (str): (Mutable) Password
            consistency (str): (Mutable) Consistency
            replication (int): (Mutable) Replication
            description (str): (Mutable) Description of Cassandra provider to be registered
            team (str): (Mutable) Name of team
            tags (List[str]): (Mutable) Optional grouping mechanism for resources
            properties (dict): (Mutable) Optional grouping mechanism for resources

        Returns:
            cassandra (OnlineProvider): Provider
        """
        config = CassandraConfig(
            host=host,
            port=port,
            username=username,
            password=password,
            keyspace=keyspace,
            consistency=consistency,
            replication=replication,
        )
        provider = Provider(
            name=name,
            function="ONLINE",
            description=description,
            team=team,
            config=config,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(provider)
        return OnlineProvider(self, provider)

    def register_dynamodb(
        self,
        name: str,
        credentials: Union[AWSStaticCredentials, AWSAssumeRoleCredentials],
        region: str,
        description: str = "",
        team: str = "",
        tags: Optional[List[str]] = None,
        properties: Optional[dict] = None,
        table_tags: Optional[dict] = None,
    ):
        """Register a DynamoDB provider.

        **Examples**:
        ```
        dynamodb = ff.register_dynamodb(
            name="dynamodb-quickstart",
            description="A Dynamodb deployment we created for the Featureform quickstart",
            credentials=aws_creds,
            region="us-east-1"
            table_tags={"owner": "featureform"}
        )
        ```

        Args:
            name (str): (Immutable) Name of DynamoDB provider to be registered
            region (str): (Immutable) Region to create dynamo tables
            credentials (Union[AWSStaticCredentials, AWSAssumeRoleCredentials]): (Mutable) AWS credentials with permissions to create DynamoDB tables
            description (str): (Mutable) Description of DynamoDB provider to be registered
            team (str): (Mutable) Name of team
            tags (List[str]): (Mutable) Optional grouping mechanism for resources
            properties (dict): (Mutable) Optional grouping mechanism for resources
            table_tags (dict): (Mutable) Tags to be added to the DynamoDB tables

        Returns:
            dynamodb (OnlineProvider): Provider
        """
        tags, properties = set_tags_properties(tags, properties)

        config = DynamodbConfig(
            credentials=credentials,
            region=region,
            table_tags=table_tags if table_tags else {},
        )
        provider = Provider(
            name=name,
            function="ONLINE",
            description=description,
            team=team,
            config=config,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(provider)
        return OnlineProvider(self, provider)

    def register_mongodb(
        self,
        name: str,
        username: str,
        password: str,
        database: str,
        host: str,
        port: str,
        throughput: int = 1000,
        description: str = "",
        team: str = "",
        tags: List[str] = [],
        properties: dict = {},
    ):
        """Register a MongoDB provider.

        **Examples**:
        ```
        mongodb = ff.register_mongodb(
            name="mongodb-quickstart",
            description="A MongoDB deployment",
            username="my_username",
            password="myPassword",
            database="featureform_database"
            host="my-mongodb.host.com",
            port="10225",
            throughput=10000
        )
        ```

        Args:
            name (str): (Immutable) Name of MongoDB provider to be registered
            database (str): (Immutable) MongoDB database
            host (str): (Immutable) MongoDB hostname
            port (str): (Immutable) MongoDB port
            username (str): (Mutable) MongoDB username
            password (str): (Mutable) MongoDB password
            throughput (int): (Mutable) The maximum RU limit for autoscaling in CosmosDB
            description (str): (Mutable) Description of MongoDB provider to be registered
            team (str): (Mutable) Name of team
            tags (List[str]): (Mutable) Optional grouping mechanism for resources
            properties (dict): (Mutable) Optional grouping mechanism for resources

        Returns:
            mongodb (OnlineProvider): Provider
        """
        tags, properties = set_tags_properties(tags, properties)
        config = MongoDBConfig(
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
            throughput=throughput,
        )
        provider = Provider(
            name=name,
            function="ONLINE",
            description=description,
            team=team,
            config=config,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(provider)
        return OnlineProvider(self, provider)

    def register_snowflake_legacy(
        self,
        name: str,
        username: str,
        password: str,
        account_locator: str,
        database: str,
        schema: str = "PUBLIC",
        description: str = "",
        team: str = "",
        warehouse: str = "",
        role: str = "",
        tags: List[str] = [],
        properties: dict = {},
        catalog: Optional[SnowflakeCatalog] = None,
    ):
        """Register a Snowflake provider using legacy credentials.

        **Examples**:
        ```
        snowflake = ff.register_snowflake_legacy(
            name="snowflake-quickstart",
            username="snowflake",
            password="password",
            account_locator="account-locator",
            database="snowflake",
            schema="PUBLIC",
            description="A Snowflake deployment we created for the Featureform quickstart"
        )
        ```

        Args:
            name (str): (Immutable) Name of Snowflake provider to be registered
            account_locator (str): (Immutable) Account Locator
            schema (str): (Immutable) Schema
            database (str): (Immutable) Database
            username (str): (Mutable) Username
            password (str): (Mutable) Password
            warehouse (str): (Mutable) Specifies the virtual warehouse to use by default for queries, loading, etc.
            role (str): (Mutable) Specifies the role to use by default for accessing Snowflake objects in the client session
            description (str): (Mutable) Description of Snowflake provider to be registered
            team (str): (Mutable) Name of team
            tags (List[str]): (Mutable) Optional grouping mechanism for resources
            properties (dict): (Mutable) Optional grouping mechanism for resources

        Returns:
            snowflake (OfflineSQLProvider): Provider
        """
        tags, properties = set_tags_properties(tags, properties)
        config = SnowflakeConfig(
            account_locator=account_locator,
            database=database,
            username=username,
            password=password,
            schema=schema,
            warehouse=warehouse,
            role=role,
            catalog=catalog,
        )
        provider = Provider(
            name=name,
            function="OFFLINE",
            description=description,
            team=team,
            config=config,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(provider)
        return OfflineSQLProvider(self, provider)

    # TODO: Recheck mutable fields
    def register_snowflake(
        self,
        name: str,
        username: str,
        password: str,
        account: str,
        organization: str,
        database: str,
        schema: str = "PUBLIC",
        description: str = "",
        team: str = "",
        warehouse: str = "",
        role: str = "",
        tags: List[str] = [],
        properties: dict = {},
        catalog: Optional[SnowflakeCatalog] = None,
        session_params: Optional[Dict[str, str]] = None,
    ):
        """Register a Snowflake provider.

        **Examples**:
        ```
        snowflake = ff.register_snowflake(
            name="snowflake-quickstart",
            username="snowflake",
            password="password", #pragma: allowlist secret
            account="account",
            organization="organization",
            database="snowflake",
            schema="PUBLIC",
            description="A Snowflake deployment we created for the Featureform quickstart"
        )
        ```

        Args:
            name (str): (Immutable) Name of Snowflake provider to be registered
            account (str): (Immutable) Account
            organization (str): (Immutable) Organization
            database (str): (Immutable) Database
            schema (str): (Immutable) Schema
            username (str): (Mutable) Username
            password (str): (Mutable) Password
            warehouse (str): (Mutable) Specifies the virtual warehouse to use by default for queries, loading, etc.
            role (str): (Mutable) Specifies the role to use by default for accessing Snowflake objects in the client session
            description (str): (Mutable) Description of Snowflake provider to be registered
            team (str): (Mutable) Name of team
            tags (List[str]): (Mutable) Optional grouping mechanism for resources
            properties (dict): (Mutable) Optional grouping mechanism for resources

        Returns:
            snowflake (OfflineSQLProvider): Provider
        """
        tags, properties = set_tags_properties(tags, properties)
        config = SnowflakeConfig(
            account=account,
            database=database,
            organization=organization,
            username=username,
            password=password,
            schema=schema,
            warehouse=warehouse,
            role=role,
            catalog=catalog,
            session_params=session_params,
        )
        provider = Provider(
            name=name,
            function="OFFLINE",
            description=description,
            team=team,
            config=config,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(provider)
        return OfflineSQLProvider(self, provider)

    def register_postgres(
        self,
        name: str,
        host: str,
        user: str,
        password: Union[str, Secret],
        database: str,
        port: str = "5432",
        description: str = "",
        team: str = "",
        sslmode: str = "disable",
        tags: List[str] = [],
        properties: dict = {},
    ) -> OfflineSQLProvider:
        """Register a Postgres provider.

        **Examples**:
        ```
        postgres = ff.register_postgres(
            name="postgres-quickstart",
            description="A Postgres deployment we created for the Featureform quickstart",
            host="quickstart-postgres",  # The internal dns name for postgres
            port="5432",
            user="postgres",
            password="password", #pragma: allowlist secret
            database="postgres"
        )
        ```

        Args:
            name (str): (Immutable) Name of Postgres provider to be registered
            host (str): (Immutable) Hostname for Postgres
            database (str): (Immutable) Database
            port (str): (Mutable) Port
            user (str): (Mutable) User
            password (str): (Mutable) Password
            sslmode (str): (Mutable) SSL mode
            description (str): (Mutable) Description of Postgres provider to be registered
            team (str): (Mutable) Name of team
            tags (List[str]): (Mutable) Optional grouping mechanism for resources
            properties (dict): (Mutable) Optional grouping mechanism for resources

        Returns:
            postgres (OfflineSQLProvider): Provider
        """
        tags, properties = set_tags_properties(tags, properties)
        config = PostgresConfig(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            sslmode=sslmode,
        )
        provider = Provider(
            name=name,
            function="OFFLINE",
            description=description,
            team=team,
            config=config,
            tags=tags or [],
            properties=properties or {},
        )

        self.__resources.append(provider)
        return OfflineSQLProvider(self, provider)

    def register_clickhouse(
        self,
        name: str,
        host: str,
        user: str,
        password: str,
        database: str,
        port: int = 9000,
        description: str = "",
        team: str = "",
        ssl: bool = False,
        tags: List[str] = [],
        properties: dict = {},
    ):
        """Register a ClickHouse provider.

        **Examples**:
        ```
        clickhouse = ff.register_clickhouse(
            name="clickhouse-quickstart",
            description="A ClickHouse deployment we created for the Featureform quickstart",
            host="quickstart-clickhouse",  # The internal dns name for clickhouse
            port=9000,
            user="default",
            password="", #pragma: allowlist secret
            database="default"
        )
        ```

        Args:
            name (str): (Immutable) Name of ClickHouse provider to be registered
            host (str): (Immutable) Hostname for ClickHouse
            database (str): (Immutable) ClickHouse database
            port (int): (Mutable) Port
            ssl (bool): (Mutable) Enable SSL
            user (str): (Mutable) User
            password (str): (Mutable) ClickHouse password
            description (str): (Mutable) Description of ClickHouse provider to be registered
            team (str): (Mutable) Name of team
            tags (List[str]): (Mutable) Optional grouping mechanism for resources
            properties (dict): (Mutable) Optional grouping mechanism for resources

        Returns:
            clickhouse (OfflineSQLProvider): Provider
        """
        tags, properties = set_tags_properties(tags, properties)
        config = ClickHouseConfig(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            ssl=ssl,
        )
        provider = Provider(
            name=name,
            function="OFFLINE",
            description=description,
            team=team,
            config=config,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(provider)
        return OfflineSQLProvider(self, provider)

    def register_redshift(
        self,
        name: str,
        host: str,
        port: str,
        user: str,
        password: str,
        database: str,
        description: str = "",
        team: str = "",
        sslmode: str = "disable",
        tags: List[str] = [],
        properties: dict = {},
    ):
        """Register a Redshift provider.

        **Examples**:
        ```
        redshift = ff.register_redshift(
            name="redshift-quickstart",
            description="A Redshift deployment we created for the Featureform quickstart",
            host="quickstart-redshift",  # The internal dns name for redshift
            port="5432",
            user="redshift",
            password="password", #pragma: allowlist secret
            database="dev"
        )
        ```

        Args:
            name (str): (Immutable) Name of Redshift provider to be registered
            host (str): (Immutable) Hostname for Redshift
            database (str): (Immutable) Redshift database
            port (str): (Mutable) Port
            user (str): (Mutable) User
            password (str): (Mutable) Redshift password
            sslmode (str): (Mutable) SSL mode
            description (str): (Mutable) Description of Redshift provider to be registered
            team (str): (Mutable) Name of team
            tags (List[str]): (Mutable) Optional grouping mechanism for resources
            properties (dict): (Mutable) Optional grouping mechanism for resources

        Returns:
            redshift (OfflineSQLProvider): Provider
        """
        tags, properties = set_tags_properties(tags, properties)
        config = RedshiftConfig(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            sslmode=sslmode,
        )
        provider = Provider(
            name=name,
            function="OFFLINE",
            description=description,
            team=team,
            config=config,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(provider)
        return OfflineSQLProvider(self, provider)

    # TODO: Add deprecated warning for credentials_path
    def register_bigquery(
        self,
        name: str,
        project_id: str,
        dataset_id: str,
        credentials: GCPCredentials,
        credentials_path: str = "",
        description: str = "",
        team: str = "",
        tags: List[str] = [],
        properties: dict = {},
    ):
        """Register a BigQuery provider.

        **Examples**:
        ```
        bigquery = ff.register_bigquery(
            name="bigquery-quickstart",
            description="A BigQuery deployment we created for the Featureform quickstart",
            project_id="quickstart-project",
            dataset_id="quickstart-dataset",
            credentials=GCPCredentials(...)
        )
        ```

        Args:
            name (str): (Immutable) Name of BigQuery provider to be registered
            project_id (str): (Immutable) The Project name in GCP
            dataset_id (str): (Immutable) The Dataset name in GCP under the Project Id
            credentials (GCPCredentials): (Mutable) GCP credentials to access BigQuery
            description (str): (Mutable) Description of BigQuery provider to be registered
            team (str): (Mutable) Name of team
            tags (List[str]): (Mutable) Optional grouping mechanism for resources
            properties (dict): (Mutable) Optional grouping mechanism for resources

        Returns:
            bigquery (OfflineSQLProvider): Provider
        """
        tags, properties = set_tags_properties(tags, properties)

        config = BigQueryConfig(
            project_id=project_id,
            dataset_id=dataset_id,
            credentials=credentials,
        )
        provider = Provider(
            name=name,
            function="OFFLINE",
            description=description,
            team=team,
            config=config,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(provider)
        return OfflineSQLProvider(self, provider)

    def register_spark(
        self,
        name: str,
        executor: ExecutorCredentials,
        filestore: FileStoreProvider,
        kafka_config: Optional[KafkaConfig] = None,
        catalog: Optional[Catalog] = None,
        description: str = "",
        team: str = "",
        tags: List[str] = [],
        properties: dict = {},
        spark_params: Optional[Dict[str, str]] = None,
        write_options: Optional[Dict[str, str]] = None,
        table_properties: Optional[Dict[str, str]] = None,
    ):
        """Register a Spark on Executor provider.

        **Examples**:
        ```
        spark = ff.register_spark(
            name="spark-quickstart",
            description="A Spark deployment we created for the Featureform quickstart",
            team="featureform-team",
            executor=databricks,
            filestore=azure_blob_store
        )
        ```

        Args:
            name (str): (Immutable) Name of Spark provider to be registered
            executor (ExecutorCredentials): (Mutable) An Executor Provider used for the compute power
            filestore (FileStoreProvider): (Mutable) A FileStoreProvider used for storage of data
            catalog (Optional[Catalog]): (Mutable) A Catalog Provider used for metadata storage
            description (str): (Mutable) Description of Spark provider to be registered
            team (str): (Mutable) Name of team
            tags (List[str]): (Mutable) Optional grouping mechanism for resources
            properties (dict): (Mutable) Optional grouping mechanism for resources

        Returns:
            spark (OfflineSparkProvider): Provider
        """
        tags, properties = set_tags_properties(tags, properties)
        config = SparkConfig(
            executor_type=executor.type(),
            executor_config=executor.config(),
            store_type=filestore.store_type(),
            store_config=filestore.config(),
            catalog_type=catalog.type() if catalog else None,
            catalog_config=catalog.config() if catalog else None,
            kafka_config=kafka_config.config() if kafka_config is not None else None,
            spark_flags=SparkFlags(
                spark_params=spark_params or {},
                write_options=write_options or {},
                table_properties=table_properties or {},
            ),
        )

        provider = Provider(
            name=name,
            function="OFFLINE",
            description=description,
            team=team,
            config=config,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(provider)
        return OfflineSparkProvider(self, provider)

    # TODO: Change things to either filestore or store
    def register_k8s(
        self,
        name: str,
        store: FileStoreProvider,
        description: str = "",
        team: str = "",
        docker_image: str = "",
        tags: List[str] = [],
        properties: dict = {},
    ):
        """
        Register an offline store provider to run on Featureform's own k8s deployment.
        **Examples**:
        ```
        spark = ff.register_k8s(
            name="k8s",
            store=AzureBlobStore(),
            docker_image="my-repo/image:version"
        )
        ```

        Args:
            name (str): (Immutable) Name of provider
            store (FileStoreProvider): (Mutable) Reference to registered file store provider
            docker_image (str): (Mutable) A custom docker image using the base image featureformcom/k8s_runner
            description (str): (Mutable) Description of primary data to be registered
            team (str): (Mutable) A string parameter describing the team that owns the provider
            tags (List[str]): (Mutable) Optional grouping mechanism for resources
            properties (dict): (Mutable) Optional grouping mechanism for resources
        """

        tags, properties = set_tags_properties(tags, properties)
        config = K8sConfig(
            store_type=store.store_type(),
            store_config=store.config(),
            docker_image=docker_image,
        )

        provider = Provider(
            name=name,
            function="OFFLINE",
            description=description,
            team=team,
            config=config,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(provider)
        return OfflineK8sProvider(self, provider)

    def register_primary_data(
        self,
        name: str,
        location: Location,
        provider: Union[str, OfflineProvider],
        tags: List[str],
        properties: dict,
        variant: str = "",
        timestamp_column: str = "",
        owner: Union[str, UserRegistrar] = "",
        description: str = "",
    ):
        """Register a primary data source.

        Args:
            name (str): Name of source
            variant (str): Name of variant
            location (Location): Location of primary data
            provider (Union[str, OfflineProvider]): Provider
            timestamp_column (str): Optionally include timestamp column for append-only tables.
            owner (Union[str, UserRegistrar]): Owner
            description (str): Description of primary data to be registered

        Returns:
            source (ColumnSourceRegistrar): Source
        """
        if not isinstance(owner, str):
            owner = owner.name()
        if owner == "":
            owner = self.must_get_default_owner()
        if variant == "":
            variant = self.__run
        if not isinstance(provider, str):
            provider = provider.name()
        source = SourceVariant(
            created=None,
            name=name,
            variant=variant,
            definition=PrimaryData(
                location=location, timestamp_column=timestamp_column
            ),
            owner=owner,
            provider=provider,
            description=description,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(source)
        column_source_registrar = ColumnSourceRegistrar(self, source)
        self.map_client_object_to_resource(column_source_registrar, source)
        return column_source_registrar

    def register_sql_transformation(
        self,
        name: str,
        query: str,
        provider: Union[str, OfflineProvider],
        variant: str = "",
        owner: Union[str, UserRegistrar] = "",
        description: str = "",
        schedule: str = "",
        args: K8sArgs = None,
        inputs: Union[List[NameVariant], List[str], List[ColumnSourceRegistrar]] = None,
        tags: List[str] = [],
        properties: dict = {},
    ):
        """Register a SQL transformation source.

        Args:
            name (str): Name of source
            variant (str): Name of variant
            query (str): SQL query
            provider (Union[str, OfflineProvider]): Provider
            owner (Union[str, UserRegistrar]): Owner
            description (str): Description of primary data to be registered
            schedule (str): Kubernetes CronJob schedule string ("* * * * *")
            args (K8sArgs): Additional transformation arguments
            tags (List[str]): Optional grouping mechanism for resources
            properties (dict): Optional grouping mechanism for resources

        Returns:
            source (ColumnSourceRegistrar): Source
        """
        if not isinstance(owner, str):
            owner = owner.name()
        if owner == "":
            owner = self.must_get_default_owner()
        if variant == "":
            variant = self.__run
        if not isinstance(provider, str):
            provider = provider.name()
        source = SourceVariant(
            created=None,
            name=name,
            variant=variant,
            definition=SQLTransformation(query, args),
            owner=owner,
            schedule=schedule,
            provider=provider,
            description=description,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(source)
        return ColumnSourceRegistrar(self, source)

    def sql_transformation(
        self,
        provider: Union[str, OfflineProvider],
        variant: str = "",
        name: str = "",
        schedule: str = "",
        owner: Union[str, UserRegistrar] = "",
        inputs: Union[List[NameVariant], List[str], List[ColumnSourceRegistrar]] = None,
        incremental: bool = False,
        incremental_inputs: Union[
            List[NameVariant], List[str], List[ColumnSourceRegistrar]
        ] = None,
        is_streaming: bool = False,
        streaming_inputs: Union[
            List[NameVariant], List[str], List[ColumnSourceRegistrar]
        ] = None,
        description: str = "",
        args: K8sArgs = None,
        tags: List[str] = [],
        properties: dict = {},
        partition_options: Optional[PartitionType] = None,
        max_job_duration: timedelta = timedelta(hours=48),
        spark_params: Optional[Dict[str, str]] = None,
        write_options: Optional[Dict[str, str]] = None,
        table_properties: Optional[Dict[str, str]] = None,
        resource_snowflake_config: Optional[ResourceSnowflakeConfig] = None,
    ):
        """SQL transformation decorator.

        Args:
            variant (str): Name of variant
            provider (Union[str, OfflineProvider]): Provider
            name (str): Name of source
            schedule (str): Kubernetes CronJob schedule string ("* * * * *")
            owner (Union[str, UserRegistrar]): Owner
            inputs (list): Inputs to transformation
            description (str): Description of SQL transformation
            args (K8sArgs): Additional transformation arguments
            tags (List[str]): Optional grouping mechanism for resources
            properties (dict): Optional grouping mechanism for resources
            max_job_duration (timedelta): Maximum duration FeatureForm will wait for the job to complete; default is 48 hours; jobs that exceed this duration will be canceled

        Returns:
            decorator (SQLTransformationDecorator): decorator
        """
        if not isinstance(owner, str):
            owner = owner.name()
        if owner == "":
            owner = self.must_get_default_owner()
        if variant == "":
            variant = self.__run
        if not isinstance(provider, str):
            provider = provider.name()
        decorator = SQLTransformationDecorator(
            registrar=self,
            name=name,
            run=self.__run,
            variant=variant,
            provider=provider,
            schedule=schedule,
            owner=owner,
            description=description,
            incremental=incremental,
            incremental_inputs=incremental_inputs,
            is_streaming=is_streaming,
            streaming_inputs=streaming_inputs,
            inputs=inputs,
            args=args,
            tags=tags,
            properties=properties,
            partition_options=partition_options,
            max_job_duration=max_job_duration,
            spark_flags=SparkFlags(
                spark_params=spark_params or {},
                write_options=write_options or {},
                table_properties=table_properties or {},
            ),
            resource_snowflake_config=resource_snowflake_config,
        )
        return decorator

    def register_df_transformation(
        self,
        name: str,
        query: str,
        provider: Union[str, OfflineProvider],
        variant: str = "",
        owner: Union[str, UserRegistrar] = "",
        description: str = "",
        inputs: list = [],
        schedule: str = "",
        args: K8sArgs = None,
        tags: List[str] = [],
        properties: dict = {},
    ):
        """Register a Dataframe transformation source.

        Args:
            name (str): Name of source
            variant (str): Name of variant
            query (str): SQL query
            provider (Union[str, OfflineProvider]): Provider
            name (str): Name of source
            owner (Union[str, UserRegistrar]): Owner
            description (str): Description of SQL transformation
            inputs (list): Inputs to transformation
            schedule (str): Kubernetes CronJob schedule string ("* * * * *")
            args (K8sArgs): Additional transformation arguments
            tags (List[str]): Optional grouping mechanism for resources
            properties (dict): Optional grouping mechanism for resources

        Returns:
            source (ColumnSourceRegistrar): Source
        """
        if not isinstance(owner, str):
            owner = owner.name()
        if owner == "":
            owner = self.must_get_default_owner()
        if variant == "":
            variant = self.__run
        if not isinstance(provider, str):
            provider = provider.name()
        source = SourceVariant(
            created=None,
            name=name,
            variant=variant,
            definition=DFTransformation(query, inputs, args),
            owner=owner,
            schedule=schedule,
            provider=provider,
            description=description,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(source)
        return ColumnSourceRegistrar(self, source)

    def df_transformation(
        self,
        provider: Union[str, OfflineProvider],
        tags: List[str],
        properties: dict,
        variant: str = "",
        name: str = "",
        owner: Union[str, UserRegistrar] = "",
        description: str = "",
        inputs: Union[List[NameVariant], List[str], List[ColumnSourceRegistrar]] = [],
        incremental: bool = False,
        incremental_inputs: Union[
            List[NameVariant], List[str], List[ColumnSourceRegistrar]
        ] = None,
        args: K8sArgs = None,
        partition_options: Optional[PartitionType] = None,
        max_job_duration: timedelta = timedelta(hours=48),
        spark_params: Optional[Dict[str, str]] = None,
        write_options: Optional[Dict[str, str]] = None,
        table_properties: Optional[Dict[str, str]] = None,
    ):
        """Dataframe transformation decorator.

        Args:
            variant (str): Name of variant
            provider (Union[str, OfflineProvider]): Provider
            name (str): Name of source
            owner (Union[str, UserRegistrar]): Owner
            description (str): Description of SQL transformation
            inputs (list): Inputs to transformation
            args (K8sArgs): Additional transformation arguments
            tags (List[str]): Optional grouping mechanism for resources
            properties (dict): Optional grouping mechanism for resources
            max_job_duration (timedelta): Maximum duration FeatureForm will wait for the job to complete; default is 48 hours; jobs that exceed this duration will be canceled

        Returns:
            decorator (DFTransformationDecorator): decorator
        """

        if not isinstance(owner, str):
            owner = owner.name()
        if owner == "":
            owner = self.must_get_default_owner()
        if variant == "":
            variant = self.__run
        if not isinstance(provider, str):
            provider = provider.name()
        if not isinstance(inputs, list):
            raise ValueError("Dataframe transformation inputs must be a list")
        for i, nv in enumerate(inputs):
            if isinstance(nv, str):  # TODO remove this functionality
                inputs[i] = (nv, self.__run)
            elif isinstance(nv, tuple):
                try:
                    self._verify_tuple(nv)
                except TypeError as e:
                    transformation_message = f"'{name}:{variant}'"
                    if name == "":
                        transformation_message = f"with '{variant}' variant"

                    raise TypeError(
                        f"DF transformation {transformation_message} requires correct inputs "
                        f" '{nv}' is not a valid tuple: {e}"
                    )
                if inputs[i][1] == "":
                    inputs[i] = (inputs[i][0], self.__run)

        decorator = DFTransformationDecorator(
            registrar=self,
            name=name,
            variant=variant,
            provider=provider,
            owner=owner,
            description=description,
            incremental=incremental,
            incremental_inputs=incremental_inputs if incremental_inputs else [],
            inputs=inputs,
            args=args,
            tags=tags,
            properties=properties,
            max_job_duration=max_job_duration,
            partition_options=partition_options,
            spark_flags=SparkFlags(
                spark_params=spark_params or {},
                write_options=write_options or {},
                table_properties=table_properties or {},
            ),
        )
        return decorator

    def _verify_tuple(self, nv_tuple):
        if not isinstance(nv_tuple, tuple):
            raise TypeError(f"not a tuple; received: '{type(nv_tuple).__name__}' type")

        if len(nv_tuple) != 2:
            raise TypeError(
                "Tuple must be of length 2, got length {}".format(len(nv_tuple))
            )
        if len(nv_tuple) == 2:
            not_string_tuples = not (
                isinstance(nv_tuple[0], str) and isinstance(nv_tuple[1], str)
            )
            if not_string_tuples:
                first_position_type = type(nv_tuple[0]).__name__
                second_position_type = type(nv_tuple[1]).__name__
                raise TypeError(
                    f"Tuple must be of type (str, str); got ({first_position_type}, {second_position_type})"
                )

    def ondemand_feature(
        self,
        fn=None,
        *,
        tags: List[str] = [],
        properties: dict = {},
        variant: str = "",
        name: str = "",
        owner: Union[str, UserRegistrar] = "",
        description: str = "",
    ):
        """On Demand Feature decorator.

        **Examples**
        ```python
        import featureform as ff

        @ff.ondemand_feature()
        def avg_user_transactions(client, params, entities):
            pass
        ```

        Args:
            variant (str): Name of variant
            name (str): Name of source
            owner (Union[str, UserRegistrar]): Owner
            description (str): Description of on demand feature
            tags (List[str]): Optional grouping mechanism for resources
            properties (dict): Optional grouping mechanism for resources

        Returns:
            decorator (OnDemandFeature): decorator

        """

        if not isinstance(owner, str):
            owner = owner.name()
        if owner == "":
            owner = self.must_get_default_owner()
        if variant == "":
            variant = self.__run
        decorator = OnDemandFeatureVariant(
            name=name,
            variant=variant,
            owner=owner,
            description=description,
            tags=tags or [],
            properties=properties or {},
        )

        self.__resources.append(decorator)

        if fn is None:
            return decorator
        else:
            return decorator(fn)

    def state(self):
        for resource in self.__resources:
            try:
                self.__state.add(resource)

            except ResourceRedefinedError:
                raise
            except Exception as e:
                resource_variant = (
                    f" ({resource.variant})" if hasattr(resource, "variant") else ""
                )
                raise Exception(
                    f"Could not add apply {resource.name}{resource_variant}: {e}"
                )
        self.__resources = []
        return self.__state

    def clear_state(self):
        self.__state = ResourceState()
        self.__client_obj_to_resource_map = {}
        self.__resources = []

    def get_state(self):
        """
        Get the state of the resources to be registered.

        Returns:
            resources (List[str]): List of resources to be registered ex. "{type} - {name} ({variant})"
        """
        if len(self.__resources) == 0:
            return "No resources to be registered"

        resources = [["Type", "Name", "Variant"]]
        for resource in self.__resources:
            if hasattr(resource, "variant"):
                resources.append(
                    [resource.__class__.__name__, resource.name, resource.variant]
                )
            else:
                resources.append([resource.__class__.__name__, resource.name, ""])

        print("Resources to be registered:")
        self.__print_state(resources)

    def __print_state(self, data):
        # Calculate the maximum width for each column
        max_widths = [max(len(str(item)) for item in col) for col in zip(*data)]

        # Format the table headers
        headers = " | ".join(
            f"{header:{width}}" for header, width in zip(data[0], max_widths)
        )

        # Generate the separator line
        separator = "-" * len(headers)

        # Format the table rows
        rows = [
            f" | ".join(f"{data[i][j]:{max_widths[j]}}" for j in range(len(data[i])))
            for i in range(1, len(data))
        ]

        # Combine the headers, separator, and rows
        table = headers + "\n" + separator + "\n" + "\n".join(rows)

        print(table)

    def register_entity(
        self,
        name: str,
        description: str = "",
        tags: List[str] = [],
        properties: dict = {},
    ):
        """Register an entity.

        **Examples**:
        ``` py
            user = ff.register_entity("user")
        ```

        Args:
            name (str): Name of entity to be registered
            description (str): Description of entity to be registered
            tags (List[str]): Optional grouping mechanism for resources
            properties (dict): Optional grouping mechanism for resources

        Returns:
            entity (EntityRegistrar): Entity
        """
        entity = Entity(
            name=name,
            description=description,
            status="",
            tags=tags,
            properties=properties,
        )
        self.__resources.append(entity)
        return EntityRegistrar(self, entity)

    def register_column_resources(
        self,
        source: Union[
            NameVariant,
            SourceRegistrar,
            SQLTransformationDecorator,
            DFTransformationDecorator,
        ],
        entity: Union[str, EntityRegistrar],
        entity_column: str,
        owner: Union[str, UserRegistrar] = "",
        inference_store: Union[str, OnlineProvider, FileStoreProvider] = "",
        features: List[ColumnMapping] = None,
        labels: List[ColumnMapping] = None,
        timestamp_column: str = "",
        description: str = "",
        schedule: str = "",
        client_object=None,
    ):
        """Create features and labels from a source. Used in the register_resources function.

        Args:
            source (Union[NameVariant, SourceRegistrar, SQLTransformationDecorator]): Source of features, labels, entity
            entity (Union[str, EntityRegistrar]): Entity
            entity_column (str): Column of entity in source
            owner (Union[str, UserRegistrar]): Owner
            inference_store (Union[str, OnlineProvider]): Online provider
            features (List[ColumnMapping]): List of ColumnMapping objects (dictionaries containing the keys: name, variant, column, resource_type)
            labels (List[ColumnMapping]): List of ColumnMapping objects (dictionaries containing the keys: name, variant, column, resource_type)
            description (str): Description
            schedule (str): Kubernetes CronJob schedule string ("* * * * *")

        Returns:
            resource (ResourceRegistrar): resource
        """

        if (
            type(inference_store) == FileStoreProvider
            and inference_store.store_type() in NON_INFERENCE_STORES
        ):
            raise Exception(
                f"cannot use '{inference_store.store_type()}' as an inference store."
            )

        if features is None:
            features = []
        if labels is None:
            labels = []
        if len(features) == 0 and len(labels) == 0:
            raise ValueError("No features or labels set")
        if isinstance(source, tuple) and source[1] == "":
            source = source[0], self.__run
        entity_name = self._normalize_entity_reference(entity)
        if not isinstance(inference_store, str):
            inference_store = inference_store.name()
        if not isinstance(owner, str):
            owner = owner.name()
        if owner == "":
            owner = self.must_get_default_owner()
        feature_resources = []
        label_resources = []
        for feature in features:
            variant = feature.get("variant", "")
            if variant == "":
                variant = self.__run
            if not ScalarType.has_value(feature["type"]) and not isinstance(
                feature["type"], ScalarType
            ):
                raise ValueError(
                    f"Invalid type for feature {feature['name']} ({variant}). Must be a ScalarType or one of {ScalarType.get_values()}"
                )
            if isinstance(feature["type"], ScalarType):
                feature["type"] = feature["type"].value
            desc = feature.get("description", "")
            feature_tags = feature.get("tags", [])
            feature_properties = feature.get("properties", {})
            additional_Parameters = self._get_additional_parameters(feature)
            is_embedding = feature.get("is_embedding", False)
            dims = feature.get("dims", 0)
            value_type = ScalarType(feature["type"])
            if dims > 0:
                value_type = VectorType(value_type, dims, is_embedding)
            resource = FeatureVariant(
                created=None,
                name=feature["name"],
                variant=variant,
                source=source,
                value_type=value_type,
                entity=entity_name,
                owner=owner,
                provider=inference_store,
                description=desc,
                schedule=schedule,
                location=ResourceColumnMapping(
                    entity=entity_column,
                    value=feature["column"],
                    timestamp=timestamp_column,
                ),
                tags=feature_tags,
                properties=feature_properties,
                additional_parameters=additional_Parameters,
                resource_snowflake_config=feature.get("resource_snowflake_config"),
            )
            self.__resources.append(resource)
            self.map_client_object_to_resource(client_object, resource)
            feature_resources.append(resource)

        for label in labels:
            variant = label.get("variant", "")
            if variant == "":
                variant = self.__run
            if not ScalarType.has_value(label["type"]) and not isinstance(
                label["type"], ScalarType
            ):
                raise ValueError(
                    f"Invalid type for label {label['name']} ({variant}). Must be a ScalarType or one of {ScalarType.get_values()}"
                )
            if isinstance(label["type"], ScalarType):
                label["type"] = label["type"].value
            desc = label.get("description", "")
            label_tags = label.get("tags", [])
            label_properties = label.get("properties", {})
            resource = LabelVariant(
                name=label["name"],
                variant=variant,
                source=source,
                value_type=label["type"],
                entity=entity_name,
                owner=owner,
                provider=inference_store,
                description=desc,
                location=ResourceColumnMapping(
                    entity=entity_column,
                    value=label["column"],
                    timestamp=timestamp_column,
                ),
                tags=label_tags,
                properties=label_properties,
            )
            self.__resources.append(resource)
            self.map_client_object_to_resource(client_object, resource)
            label_resources.append(resource)
        return ResourceRegistrar(self, features, labels)

    def _get_additional_parameters(self, feature):
        return OndemandFeatureParameters(definition="() => REGISTER")

    def register_feature_stream(
        self,
        name: str,
        entity: Union[str, EntityRegistrar],
        type: Union[ScalarType, str],
        offline_provider: Union[str, OfflineProvider],
        inference_store: Union[str, OnlineProvider],
        variant: str = "",
        owner: str = "",
        description: str = "",
        tags: Union[List[str], None] = None,
        properties: Union[Dict[str, str], None] = None,
    ):
        if not isinstance(entity, str):
            entity = entity.name()
        if not isinstance(inference_store, str):
            inference_store = inference_store.name()
        if not isinstance(offline_provider, str):
            offline_provider = offline_provider.name()
        if not isinstance(owner, str):
            owner = owner.name()
        if owner == "":
            owner = self.must_get_default_owner()
        if not isinstance(type, str):
            type = type.value
        if variant == "":
            variant = self.__run

        stream_feature = StreamFeature(
            name=name,
            entity=entity,
            value_type=type,
            offline_provider=offline_provider,
            inference_store=inference_store,
            variant=variant,
            owner=owner,
            description=description,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(stream_feature)
        return ResourceRegistrar(self, [stream_feature], [])

    def register_label_stream(
        self,
        name: str,
        entity: Union[str, EntityRegistrar],
        type: Union[ScalarType, str],
        offline_provider: Union[str, OfflineProvider],
        variant: str = "",
        owner: str = "",
        description: str = "",
        tags: Union[List[str], None] = None,
        properties: Union[Dict[str, str], None] = None,
    ):
        if not isinstance(entity, str):
            entity = entity.name()
            if not isinstance(offline_provider, str):
                offline_provider = offline_provider.name()
            if not isinstance(owner, str):
                owner = owner.name()
            if owner == "":
                owner = self.must_get_default_owner()
            if not isinstance(type, str):
                type = type.value
            if variant == "":
                variant = self.__run

        stream_label = StreamLabel(
            name=name,
            entity=entity,
            value_type=type,
            offline_provider=offline_provider,
            variant=variant,
            owner=owner,
            description=description,
            tags=tags,
            properties=properties,
        )
        self.__resources.append(stream_label)
        return ResourceRegistrar(self, [], [stream_label])

    def __register_stream(self, stream: BaseStream):
        self.__resources.append(stream)
        return ResourceRegistrar(self, [stream], [])

    def __get_feature_nv(self, features, run):
        feature_nv_list = []
        feature_lags = []
        for feature in features:
            if isinstance(feature, str):
                feature_nv_list.append((feature, run))
            elif isinstance(feature, dict):
                lag = feature.get("lag")
                if "variant" not in feature:
                    feature["variant"] = run
                if lag:
                    required_lag_keys = set(["lag", "feature", "variant"])
                    received_lag_keys = set(feature.keys())
                    if (
                        required_lag_keys.intersection(received_lag_keys)
                        != required_lag_keys
                    ):
                        raise ValueError(
                            f"feature lags require 'lag', 'feature', 'variant' fields. Received: {feature.keys()}"
                        )

                    if not isinstance(lag, timedelta):
                        raise ValueError(
                            f"the lag, '{lag}', needs to be of type 'datetime.timedelta'. Received: {type(lag)}."
                        )

                    feature_name_variant = (feature["feature"], feature["variant"])
                    if feature_name_variant not in feature_nv_list:
                        feature_nv_list.append(feature_name_variant)

                    lag_name = f"{feature['feature']}_{feature['variant']}_lag_{lag}"
                    sanitized_lag_name = (
                        lag_name.replace(" ", "").replace(",", "_").replace(":", "_")
                    )
                    feature["name"] = feature.get("name", sanitized_lag_name)

                    feature_lags.append(feature)
                else:
                    feature_nv = (feature["name"], feature["variant"])
                    feature_nv_list.append(feature_nv)
            elif isinstance(feature, list):
                feature_nv, feature_lags_list = self.__get_feature_nv(feature, run)
                if len(feature_nv) != 0:
                    feature_nv_list.extend(feature_nv)

                if len(feature_lags_list) != 0:
                    feature_lags.extend(feature_lags_list)
            else:
                feature_nv_list.append(feature)

        return feature_nv_list, feature_lags

    def register_feature_view(
        self,
        view_name: str,
        inference_store: Union[str, OnlineProvider],
        features: Optional[List[Union[str, tuple, HasNameVariant]]] = None,
        description: Optional[str] = None,
        table_opts=None,
        materialization_opts: Optional[
            Union[MaterializationOptions, Dict[str, Any]]
        ] = None,
        materialization_engine: Optional[Union[str, OfflineSparkProvider]] = None,
        owner: Optional[Union[str, User]] = None,
        use_super_admin_delete_override: bool = False,
    ):
        """Register feature view to the inference store.

        Args:
            view_name (str): The name of the view to materialize.
            inference_store (Union[str, OnlineProvider]): The inference store to materialize into.
            features (Optional[List[Union[str, tuple, FeatureColumnResource]]]): A list of features to materialize.
            description (Optional[str]): Description of the feature view.
            table_opts: Additional options for the materialization table.
            materialization_opts: Additional options for the materialization process (e.g. join_strategy).
            materialization_engine: The engine to use for materialization, either a K8s, which uses the offline provider of the features
                                    or an OfflineSparkProvider, which can accept varied offline providers for features (e.g. Snowflake, BigQuery, etc.)
            owner (Optional[Union[str, User]]): The owner of the feature view.
            use_super_admin_delete_override (bool): Flag to override delete permissions for super admin.

        Returns:
            FeatureView: The created feature view.

        **Example:**
        ```py
        feature_view = client.register_feature_view(
            view_name="my_view",
            inference_store="my_inference_store",
            features=[
                ("feature1", "variant1"),
                ("feature2", "variant2"),
            ],
            description="My feature view",
        )
        """
        if not features:
            features = []

        if isinstance(inference_store, str) and inference_store:
            provider = inference_store
        elif isinstance(inference_store, OnlineProvider):
            provider = inference_store.name()
        else:
            raise ValueError("Invalid inference store type.")

        if isinstance(owner, User):
            owner = owner.name()
        elif owner == "" or owner is None:
            owner = self.must_get_default_owner()

        features_list = []
        for feature in features:
            if isinstance(feature, HasNameVariant):
                features_list.append(feature)
            elif isinstance(feature, tuple):
                features_list.append(
                    (feature[0], feature[1] if feature[1] else self.__run)
                )
            else:
                raise ValueError("Invalid feature type.")

        # Create unique features dict, handling both tuples and Feature Object
        unique_features = {}
        for feature in features_list:
            if isinstance(feature, HasNameVariant):
                key = (feature.name, feature.variant)
                unique_features[key] = feature
            else:
                key = (feature[0], feature[1])
                unique_features[key] = feature

        if isinstance(materialization_engine, OfflineSparkProvider):
            engine = materialization_engine.name()
        else:
            engine = materialization_engine

        materialization_opts = MaterializationOptions.from_input(materialization_opts)

        feature_view = FeatureView(
            name=view_name,
            provider=provider,
            features=list(
                unique_features.values()
            ),  # Pass the actual objects (FeatureColumnResource or tuples)
            description=description,
            owner=owner,
            materialization_engine=engine,
            materialization_options=materialization_opts,
            use_super_admin_delete_override=use_super_admin_delete_override,
        )

        self.map_client_object_to_resource(feature_view, feature_view)
        self.__resources.append(feature_view)
        return feature_view

    def register_training_set(
        self,
        name: str,
        variant: str = "",
        features: Union[
            list, List[FeatureColumnResource], MultiFeatureColumnResource
        ] = [],
        label: Union[NameVariant, LabelColumnResource] = ("", ""),
        resources: list = [],
        owner: Union[str, UserRegistrar] = "",
        description: str = "",
        schedule: str = "",
        tags: List[str] = [],
        properties: dict = {},
        provider: str = "",
        resource_snowflake_config: Optional[ResourceSnowflakeConfig] = None,
        type: TrainingSetType = TrainingSetType.DYNAMIC,
    ):
        """Register a training set.

        **Example**:
        ```
        ff.register_training_set(
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
            owner (Union[str, UserRegistrar]): Owner
            description (str): Description of training set to be registered
            schedule (str): Kubernetes CronJob schedule string ("* * * * *")
            tags (List[str]): Optional grouping mechanism for resources
            properties (dict): Optional grouping mechanism for resources

        Returns:
            resource (ResourceRegistrar): resource
        """
        if not isinstance(owner, str):
            owner = owner.name()
        if owner == "":
            owner = self.must_get_default_owner()
        if variant == "":
            variant = self.__run

        if not isinstance(features, (list, MultiFeatureColumnResource)):
            raise ValueError(
                f"Invalid features type: {type(features)} "
                "Features must be entered as a list of name-variant tuples (e.g. [('feature1', 'quickstart'), ('feature2', 'quickstart')]) or a list of FeatureColumnResource instances."
            )
        if not isinstance(label, (tuple, str, LabelColumnResource, LabelVariant)):
            raise ValueError(
                f"Invalid label type: {type(label)} "
                "Label must be entered as a name-variant tuple (e.g. ('fraudulent', 'quickstart')), a resource name, or an instance of LabelColumnResource."
            )

        for resource in resources:
            features += resource.features()
            resource_label = resource.label()
            # label == () if it is NOT manually entered
            if label == ("", ""):
                label = resource_label
            # Elif: If label was updated to store resource_label it will not check the following elif
            elif resource_label != ():
                raise ValueError("A training set can only have one label")

        features, feature_lags = self.__get_feature_nv(features, self.__run)
        if label == ():
            raise ValueError("Label must be set")
        if features == []:
            raise ValueError("A training-set must have at least one feature")
        if isinstance(label, str):
            label = (label, self.__run)
        elif isinstance(label, LabelVariant):
            label = (
                label.name,
                (
                    self.__run
                    if label.name_variant()[1] == ""
                    else label.name_variant()[1]
                ),
            )
        elif isinstance(label, tuple) and label[1] == "":
            label = (label[0], self.__run)
        elif not isinstance(label, LabelColumnResource) and label[1] == "":
            label = (label.name, self.__run)

        processed_features = []
        for feature in features:
            if isinstance(feature, tuple) and feature[1] == "":
                feature = (feature[0], self.__run)
            processed_features.append(feature)
        if not isinstance(type, TrainingSetType):
            raise TypeError(
                'Expected Training Set "type" to be TrainingSetType.DYNAMIC|STATIC|VIEW'
            )
        resource = TrainingSetVariant(
            created=None,
            name=name,
            variant=variant,
            description=description,
            owner=owner,
            schedule=schedule,
            label=label,
            features=processed_features,
            feature_lags=feature_lags,
            tags=tags,
            properties=properties,
            provider=provider,
            resource_snowflake_config=resource_snowflake_config,
            type=type,
        )
        self.map_client_object_to_resource(resource, resource)
        self.__resources.append(resource)
        return resource

    def register_model(
        self, name: str, tags: List[str] = [], properties: dict = {}
    ) -> Model:
        """Register a model.

        Args:
            name (str): Model to be registered
            tags (List[str]): Optional grouping mechanism for resources
            properties (dict): Optional grouping mechanism for resources

        Returns:
            ModelRegistrar: Model
        """
        model = Model(name, description="", tags=tags, properties=properties)
        self.__resources.append(model)
        return model
