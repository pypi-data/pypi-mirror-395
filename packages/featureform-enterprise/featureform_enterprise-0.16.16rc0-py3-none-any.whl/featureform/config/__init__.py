# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Configuration classes for Featureform providers.

This module contains all configuration classes for:
- Credentials (AWS, GCP, Databricks, EMR, Spark, etc.)
- Online stores (Redis, Pinecone, Weaviate, Firestore, Cassandra, DynamoDB, MongoDB)
- Offline stores (Postgres, Clickhouse, Redshift, BigQuery, Snowflake)
- File stores (S3, GCS, Azure, HDFS, Vault, Kafka)
- Compute providers (Spark, K8s)
- Catalogs (Glue, Unity, Snowflake)
"""

# Credentials
# Catalogs
from .catalogs import (
    Catalog,
    GlueCatalog,
    SnowflakeCatalog,
    SnowflakeDynamicTableConfig,
    UnityCatalog,
)

# Compute
from .compute import (
    EmptyConfig,
    EmptySparkFlags,
    K8sArgs,
    K8sConfig,
    K8sResourceSpecs,
    SparkConfig,
    SparkFlags,
)
from .credentials import (
    AWSAssumeRoleCredentials,
    AWSStaticCredentials,
    BasicCredentials,
    DatabricksCredentials,
    EMRCredentials,
    ExecutorCredentials,
    GCPCredentials,
    KerberosCredentials,
    SparkCredentials,
)

# File stores
from .file_stores import (
    AzureFileStoreConfig,
    GCSFileStoreConfig,
    HDFSConfig,
    KafkaConfig,
    OnlineBlobConfig,
    S3StoreConfig,
    VaultConfig,
)

# Offline stores
from .offline_stores import (
    BigQueryConfig,
    ClickHouseConfig,
    PostgresConfig,
    RedshiftConfig,
    ResourceSnowflakeConfig,
    SnowflakeConfig,
)

# Online stores
from .online_stores import (
    CassandraConfig,
    DynamodbConfig,
    FirestoreConfig,
    MongoDBConfig,
    PineconeConfig,
    RedisConfig,
    WeaviateConfig,
)

__all__ = [
    # Credentials
    "AWSStaticCredentials",
    "AWSAssumeRoleCredentials",
    "GCPCredentials",
    "BasicCredentials",
    "KerberosCredentials",
    "DatabricksCredentials",
    "EMRCredentials",
    "SparkCredentials",
    "ExecutorCredentials",
    # Online stores
    "RedisConfig",
    "PineconeConfig",
    "WeaviateConfig",
    "FirestoreConfig",
    "CassandraConfig",
    "DynamodbConfig",
    "MongoDBConfig",
    # Offline stores
    "PostgresConfig",
    "ClickHouseConfig",
    "RedshiftConfig",
    "BigQueryConfig",
    "SnowflakeConfig",
    "SnowflakeDynamicTableConfig",
    "ResourceSnowflakeConfig",
    # File stores
    "S3StoreConfig",
    "GCSFileStoreConfig",
    "AzureFileStoreConfig",
    "HDFSConfig",
    "VaultConfig",
    "KafkaConfig",
    "OnlineBlobConfig",
    # Compute
    "SparkConfig",
    "SparkFlags",
    "EmptySparkFlags",
    "K8sConfig",
    "K8sResourceSpecs",
    "K8sArgs",
    "EmptyConfig",
    # Catalogs
    "Catalog",
    "GlueCatalog",
    "UnityCatalog",
    "SnowflakeCatalog",
]
