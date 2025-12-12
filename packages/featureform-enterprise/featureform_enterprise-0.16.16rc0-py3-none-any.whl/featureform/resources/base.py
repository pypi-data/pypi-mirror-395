# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Base classes and types for Featureform resources.

This module contains base classes, protocols, and the Resource union type that are used
across all resource modules.
"""

from abc import ABC
from typing import TYPE_CHECKING, Protocol, Tuple, Union, runtime_checkable

from typeguard import typechecked

from ..enums import ResourceType

# Type alias for name-variant tuples
NameVariant = Tuple[str, str]


@typechecked
def valid_name_variant(nvar: NameVariant) -> bool:
    """Check if a name-variant tuple is valid (both parts non-empty)."""
    return nvar[0] != "" and nvar[1] != ""


@runtime_checkable
class HasNameVariant(Protocol):
    """Protocol for resources that have a name_variant method."""

    def name_variant(self) -> Tuple[str, str]:
        """Returns the name and variant of the resource"""
        ...


@runtime_checkable
class ResourceVariant(HasNameVariant, Protocol):
    """Protocol for resource variants with name, variant, and status."""

    name: str
    variant: str
    server_status: "ServerStatus"  # Forward reference

    def get_resource_type(self) -> ResourceType:
        """Returns the type of the resource"""
        ...

    def to_key(self) -> Tuple[ResourceType, str, str]:
        """Returns a tuple key of (resource_type, name, variant)"""
        return self.get_resource_type(), self.name, self.variant


if TYPE_CHECKING:
    from .entity import Entity, EntityReference
    from .feature import FeatureVariant, OnDemandFeatureVariant
    from .feature_view import FeatureView
    from .label import LabelVariant
    from .locations import StreamChannel
    from .model import Model
    from .provider import Provider, ServerStatus
    from .schedule import Schedule
    from .source import ProviderReference, SourceReference, SourceVariant
    from .stream import StreamFeature, StreamLabel
    from .training_set import TrainingSetVariant
    from .transformations import PrimaryData
    from .user import User


class Location_Duplicate(ABC):
    """Abstract base class for resources that have a location."""

    def resource_identifier(self):
        """
        Return the location of the resource.
        :return:
        """
        raise NotImplementedError


# Resource union type - defined here to avoid circular imports
# This needs to be defined after all resource classes are imported
Resource = Union[
    "PrimaryData",
    "Provider",
    "Entity",
    "User",
    "FeatureVariant",
    "LabelVariant",
    "TrainingSetVariant",
    "SourceVariant",
    "Schedule",
    "ProviderReference",
    "SourceReference",
    "EntityReference",
    "Model",
    "OnDemandFeatureVariant",
    "StreamFeature",
    "StreamLabel",
    "FeatureView",
    "StreamChannel",
]


# Config union type - includes all provider configuration types
# Import at runtime to avoid circular imports
def _get_config_union():
    """Lazy import to avoid circular dependencies."""
    from ..config import (
        AzureFileStoreConfig,
        BigQueryConfig,
        CassandraConfig,
        ClickHouseConfig,
        DynamodbConfig,
        EmptyConfig,
        FirestoreConfig,
        GCSFileStoreConfig,
        HDFSConfig,
        K8sConfig,
        KafkaConfig,
        MongoDBConfig,
        OnlineBlobConfig,
        PineconeConfig,
        PostgresConfig,
        RedisConfig,
        RedshiftConfig,
        S3StoreConfig,
        SnowflakeConfig,
        SparkConfig,
        VaultConfig,
        WeaviateConfig,
    )

    return Union[
        RedisConfig,
        PineconeConfig,
        SnowflakeConfig,
        PostgresConfig,
        ClickHouseConfig,
        RedshiftConfig,
        BigQueryConfig,
        FirestoreConfig,
        SparkConfig,
        OnlineBlobConfig,
        AzureFileStoreConfig,
        S3StoreConfig,
        K8sConfig,
        MongoDBConfig,
        GCSFileStoreConfig,
        EmptyConfig,
        HDFSConfig,
        WeaviateConfig,
        DynamodbConfig,
        CassandraConfig,
        KafkaConfig,
        VaultConfig,
    ]


# Create the Config type at module level
Config = _get_config_union()
