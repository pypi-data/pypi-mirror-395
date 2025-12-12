# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Location classes for Featureform resources.

This module contains all location-related classes including SQL tables, file stores,
stream channels, and catalog tables.
"""

from abc import ABC
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Tuple

from typeguard import typechecked

from ..enums import OperationType, ResourceType, TableFormat
from ..proto import metadata_pb2 as pb

if TYPE_CHECKING:
    from .mappings import FeaturesSchema
else:
    # At runtime, use Any to avoid circular import issues with typeguard
    FeaturesSchema = Any


class Location(ABC):
    def resource_identifier(self):
        """
        Return the location of the resource.
        :return:
        """
        raise NotImplementedError


@typechecked
@dataclass
class SQLTable(Location):
    name: str
    schema: str = ""
    database: str = ""

    def resource_identifier(self):
        return f"{self.database}.{self.schema}.{self.name}"

    @staticmethod
    def from_proto(source_table):
        return SQLTable(
            schema=source_table.schema,
            database=source_table.database,
            name=source_table.name,
        )


@typechecked
@dataclass
class FileStore(Location):
    """
    Contains the location of a path in a cloud file store (S3, GCS, Azure)
    """

    path_uri: str

    def resource_identifier(self):
        return self.path_uri

    @staticmethod
    def from_proto(source_filestore):
        return FileStore(path_uri=source_filestore.path)


@typechecked
@dataclass
class StreamChannel(Location):
    """
    StreamChannel represents a resource that can be read in a streaming way.

    For example, this can be a Kafka topic.
    """

    name: str
    channel_name: str
    provider: str
    description: str = ""
    owner: str = ""
    created: str = None
    last_updated: str = None

    @staticmethod
    def from_proto(source_stream):
        return StreamChannel(
            name=source_stream.name,
            channel_name=source_stream.channel_name,
            provider=source_stream.provider,
        )

    @staticmethod
    def get_resource_type() -> ResourceType:
        return ResourceType.STREAM_CHANNEL

    @staticmethod
    def operation_type() -> OperationType:
        return OperationType.CREATE

    @staticmethod
    def get(stub, name: str) -> "StreamChannel":
        name_req = pb.NameRequest(name=pb.Name(name=name))
        stream_channel = next(stub.GetStreamChannels(iter([name_req])))

        if not stream_channel:
            raise ValueError(f"Stream channel {name} not found")

        return StreamChannel(
            name=stream_channel.name,
            channel_name=stream_channel.channel_name,
            provider=stream_channel.provider,
            description=stream_channel.description,
            owner=stream_channel.owner,
            created=stream_channel.created,
            last_updated=stream_channel.last_updated,
        )

    def resource_identifier(self):
        return self.name

    def _create(self, req_id, stub) -> Tuple[None, None]:
        serialized = pb.StreamChannelRequest(
            stream_channel=pb.StreamChannel(
                name=self.name,
                channel_name=self.channel_name,
                provider=self.provider,
                description=self.description,
                owner=self.owner,
            ),
            request_id="",
        )

        stub.CreateStreamChannel(serialized)
        return None, None


@typechecked
@dataclass
class GlueCatalogTable(Location):
    database: str
    table: str
    table_format: TableFormat = field(default_factory=lambda: TableFormat.ICEBERG)

    def resource_identifier(self):
        return f"{self.database}.{self.table}"

    @staticmethod
    def from_proto(source_catalog_table):
        return GlueCatalogTable(
            database=source_catalog_table.database,
            table=source_catalog_table.table,
            table_format=TableFormat.get_format(source_catalog_table.table_format),
        )


@typechecked
@dataclass
class UnityCatalogTable(Location):
    database: str
    schema: str
    table: str
    table_format: TableFormat = field(default_factory=lambda: TableFormat.ICEBERG)

    def resource_identifier(self):
        return f"{self.database}.{self.schema}.{self.table}"

    @staticmethod
    def from_proto(source_catalog_table):
        return UnityCatalogTable(
            database=source_catalog_table.database,
            schema=source_catalog_table.schema,
            table=source_catalog_table.table,
            table_format=TableFormat.get_format(source_catalog_table.table_format),
        )


@typechecked
@dataclass
class Directory(Location):
    path: str

    def path(self):
        return self.path


@typechecked
@dataclass
class OnlineLocation(Location):
    """Online location for feature serving."""

    table: str
    version: int
    schema: "FeaturesSchema"  # Forward reference to avoid circular import

    def resource_identifier(self):
        return f"{self.table}__{self.version}"

    @staticmethod
    def from_proto(proto: pb.Location):
        # Import here to avoid circular dependency
        from .mappings import FeaturesSchema

        online_proto = proto.online
        return (
            OnlineLocation(
                table=online_proto.table,
                version=online_proto.version,
                schema=FeaturesSchema.from_proto(online_proto.schema),
            )
            if online_proto
            else None
        )
