# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Registration and client functionality for Featureform.

REFACTORING COMPLETE:
---------------------
This module has been refactored into focused packages. All classes have been moved to:

- Provider classes → providers/
- Column resources → registrar/column_resources.py
- Transformation decorators → registrar/transformation_decorators.py
- Registrar class → registrar/registrar.py
- ResourceClient → client_legacy/resource_client.py
- Entity decorator → registrar/entity_decorator.py

This file now serves as a backwards compatibility shim, re-exporting everything
from the new locations to maintain API compatibility.
"""

# Re-export from providers
# Type union for deletable resources
from typing import Union

# Re-export from client
from .client import ResourceClient

# Re-export from core.exceptions
from .core.exceptions import InvalidSQLQuery

# Re-export from enums
from .enums import ScalarType

# Re-export from parse
from .parse import canonicalize_function_definition
from .providers import (
    FileStoreProvider,
    KafkaProvider,
    OfflineK8sProvider,
    OfflineProvider,
    OfflineSparkProvider,
    OfflineSQLProvider,
    OnlineProvider,
)

# Re-export from registrar
from .registrar import (
    ColumnMapping,
    ColumnResource,
    DFTransformationDecorator,
    EmbeddingColumnResource,
    EntityRegistrar,
    FeatureColumnResource,
    Incremental,
    LabelColumnResource,
    MultiFeatureColumnResource,
    Registrar,
    ResourceRegistrar,
    SQLTransformationDecorator,
    Stream,
    SubscriptableTransformation,
    Variants,
    entity,
    global_registrar,
)

# Re-export from registrar.registrars
from .registrar.registrars import ColumnSourceRegistrar, SourceRegistrar

# Re-export from resources
from .resources import (
    AggregateFeature,
    AttributeFeature,
    DFTransformation,
    Entity,
    FeatureStreamResource,
    FeatureVariant,
    FeatureView,
    LabelStreamResource,
    LabelVariant,
    Model,
    PostgresConfig,
    PrimaryData,
    ResourceVariant,
    SnowflakeConfig,
    SourceVariant,
    SQLTable,
    SQLTransformation,
    TrainingSetVariant,
)

# Re-export from types
from .types import VectorType

# Re-export from utils
from .utils.helpers import get_name_variant

DeletableResourceObjects = Union[
    FeatureColumnResource,
    SubscriptableTransformation,
    LabelColumnResource,
    TrainingSetVariant,
    LabelVariant,
    SourceVariant,
    FeatureVariant,
    ColumnSourceRegistrar,
    OnlineProvider,
    OfflineProvider,
    FeatureView,
]

# Global registrar instance and method exports
state = global_registrar.state
clear_state = global_registrar.clear_state
get_state = global_registrar.get_state
set_run = global_registrar.set_run
set_variant_prefix = global_registrar.set_variant_prefix
get_run = global_registrar.get_run
register_user = global_registrar.register_user
register_redis = global_registrar.register_redis
register_pinecone = global_registrar.register_pinecone
register_weaviate = global_registrar.register_weaviate
register_blob_store = global_registrar.register_blob_store
register_bigquery = global_registrar.register_bigquery
register_clickhouse = global_registrar.register_clickhouse
register_firestore = global_registrar.register_firestore
register_cassandra = global_registrar.register_cassandra
register_dynamodb = global_registrar.register_dynamodb
register_mongodb = global_registrar.register_mongodb
register_snowflake = global_registrar.register_snowflake
register_snowflake_legacy = global_registrar.register_snowflake_legacy
register_postgres = global_registrar.register_postgres
register_redshift = global_registrar.register_redshift
register_spark = global_registrar.register_spark
register_k8s = global_registrar.register_k8s
register_kafka = global_registrar.register_kafka
register_vault = global_registrar.register_vault
register_s3 = global_registrar.register_s3
register_hdfs = global_registrar.register_hdfs
register_gcs = global_registrar.register_gcs
register_entity = global_registrar.register_entity
register_column_resources = global_registrar.register_column_resources
register_feature_stream = global_registrar.register_feature_stream
register_label_stream = global_registrar.register_label_stream
register_training_set = global_registrar.register_training_set
register_feature_view = global_registrar.register_feature_view
register_model = global_registrar.register_model
sql_transformation = global_registrar.sql_transformation
register_sql_transformation = global_registrar.register_sql_transformation
get_entity = global_registrar.get_entity
get_source = global_registrar.get_source
get_redis = global_registrar.get_redis
get_postgres = global_registrar.get_postgres
get_dynamodb = global_registrar.get_dynamodb
get_mongodb = global_registrar.get_mongodb
get_snowflake = global_registrar.get_snowflake
get_snowflake_legacy = global_registrar.get_snowflake_legacy
get_redshift = global_registrar.get_redshift
get_bigquery = global_registrar.get_bigquery
get_clickhouse = global_registrar.get_clickhouse
get_spark = global_registrar.get_spark
get_kubernetes = global_registrar.get_kubernetes
get_blob_store = global_registrar.get_blob_store
get_s3 = global_registrar.get_s3
get_gcs = global_registrar.get_gcs
ondemand_feature = global_registrar.ondemand_feature

# ScalarType enum value exports
Nil = ScalarType.NIL
String = ScalarType.STRING
Int = ScalarType.INT
Int32 = ScalarType.INT32
Int64 = ScalarType.INT64
Float32 = ScalarType.FLOAT32
Float64 = ScalarType.FLOAT64
Bool = ScalarType.BOOL
DateTime = ScalarType.DATETIME

__all__ = [
    # Provider classes
    "OfflineProvider",
    "OfflineSQLProvider",
    "OfflineSparkProvider",
    "OfflineK8sProvider",
    "KafkaProvider",
    "OnlineProvider",
    "FileStoreProvider",
    # Column resources
    "ColumnResource",
    "FeatureColumnResource",
    "LabelColumnResource",
    "EmbeddingColumnResource",
    "MultiFeatureColumnResource",
    # Stream resources
    "FeatureStreamResource",
    "LabelStreamResource",
    # Transformation decorators
    "SubscriptableTransformation",
    "SQLTransformationDecorator",
    "DFTransformationDecorator",
    # Main classes
    "Registrar",
    "ResourceClient",
    "Incremental",
    "Stream",
    "SourceRegistrar",
    "ColumnSourceRegistrar",
    "EntityRegistrar",
    "ResourceRegistrar",
    "ResourceVariant",
    "TrainingSetVariant",
    "Variants",
    "ColumnMapping",
    # Resource classes
    "DFTransformation",
    "SQLTransformation",
    "PrimaryData",
    "SQLTable",
    "Model",
    "Entity",
    "PostgresConfig",
    "SnowflakeConfig",
    "AttributeFeature",
    "AggregateFeature",
    # Exceptions
    "InvalidSQLQuery",
    # Parse functions
    "canonicalize_function_definition",
    # Utility functions
    "get_name_variant",
    # Decorators
    "entity",
    # Type unions
    "DeletableResourceObjects",
    # Global registrar instance and methods
    "global_registrar",
    "state",
    "clear_state",
    "get_state",
    "set_run",
    "set_variant_prefix",
    "get_run",
    "register_user",
    "register_redis",
    "register_pinecone",
    "register_weaviate",
    "register_blob_store",
    "register_bigquery",
    "register_clickhouse",
    "register_firestore",
    "register_cassandra",
    "register_dynamodb",
    "register_mongodb",
    "register_snowflake",
    "register_snowflake_legacy",
    "register_postgres",
    "register_redshift",
    "register_spark",
    "register_k8s",
    "register_kafka",
    "register_vault",
    "register_s3",
    "register_hdfs",
    "register_gcs",
    "register_entity",
    "register_column_resources",
    "register_feature_stream",
    "register_label_stream",
    "register_training_set",
    "register_feature_view",
    "register_model",
    "sql_transformation",
    "register_sql_transformation",
    "get_entity",
    "get_source",
    "get_redis",
    "get_postgres",
    "get_dynamodb",
    "get_mongodb",
    "get_snowflake",
    "get_snowflake_legacy",
    "get_redshift",
    "get_bigquery",
    "get_clickhouse",
    "get_spark",
    "get_kubernetes",
    "get_blob_store",
    "get_s3",
    "get_gcs",
    "ondemand_feature",
    # Type classes
    "ScalarType",
    "VectorType",
    # ScalarType enum values
    "Nil",
    "String",
    "Int",
    "Int32",
    "Int64",
    "Float32",
    "Float64",
    "Bool",
    "DateTime",
]
