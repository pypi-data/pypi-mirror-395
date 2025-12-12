# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Provider resource classes.

This module contains Provider, Properties, ServerStatus, and ErrorInfo classes.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

from google.rpc import error_details_pb2
from typeguard import typechecked

from ..config.compute import EmptyConfig
from ..enums import OperationType, ResourceStatus, ResourceType
from ..proto import metadata_pb2 as pb

Config = object  # Type alias for any config type


@typechecked
@dataclass
class Properties:
    """Properties wrapper for resource metadata."""

    properties: dict

    def __post_init__(self):
        self.serialized = pb.Properties()
        for key, val in self.properties.items():
            self.serialized.property[key].string_value = val


@dataclass
class ErrorInfo:
    """Error information for resource status."""

    code: int
    message: str
    reason: str
    metadata: Dict[str, str]


@dataclass
class ServerStatus:
    """Server-side status information for a resource."""

    status: "ResourceStatus"
    error_info: Optional[ErrorInfo]

    @staticmethod
    def from_proto(resource_status_proto: pb.ResourceStatus) -> "ServerStatus":
        error_info = None
        if resource_status_proto.HasField("error_status"):
            error_status = resource_status_proto.error_status

            # Extract reason and metadata from error details
            reason = ""
            metadata = {}
            for detail in error_status.details:
                error_info_detail = error_details_pb2.ErrorInfo()
                if detail.Unpack(error_info_detail):
                    reason = error_info_detail.reason
                    metadata = dict(error_info_detail.metadata)
                    break

            error_info = ErrorInfo(
                code=error_status.code,
                message=error_status.message,
                reason=reason,
                metadata=metadata,
            )

        return ServerStatus(
            status=ResourceStatus.from_proto(resource_status_proto),
            error_info=error_info,
        )


@typechecked
@dataclass
class Provider:
    """Provider resource for data sources and compute engines."""

    name: str
    description: str
    config: Config
    function: str
    team: str = ""
    status: str = "NO_STATUS"
    tags: list = field(default_factory=list)
    properties: dict = field(default_factory=dict)
    error: Optional[str] = None
    has_health_check: bool = False
    server_status: Optional["ServerStatus"] = None

    def __post_init__(self):
        self.software = self.config.software() if self.config is not None else None
        if self.config.type() in [
            "REDIS_ONLINE",
            "DYNAMODB_ONLINE",
            "POSTGRES_OFFLINE",
            "SPARK_OFFLINE",
            "REDSHIFT_OFFLINE",
            "CLICKHOUSE_OFFLINE",
        ]:
            self.has_health_check = True

    @staticmethod
    def operation_type() -> OperationType:
        return OperationType.CREATE

    @staticmethod
    def get_resource_type() -> ResourceType:
        return ResourceType.PROVIDER

    def get(self, stub) -> "Provider":
        name = pb.NameRequest(name=pb.Name(name=self.name))
        provider = next(stub.GetProviders(iter([name])))

        return Provider(
            name=provider.name,
            description=provider.description,
            function=provider.type,
            team=provider.team,
            config=EmptyConfig(),  # TODO add deserializer to configs
            tags=list(provider.tags.tag),
            properties=dict(provider.properties.property.items()),
            status=provider.status.Status._enum_type.values[
                provider.status.status
            ].name,
            error=provider.status.error_message,
            server_status=ServerStatus.from_proto(provider.status),
        )

    def _create(self, req_id, stub) -> Tuple[None, None]:
        serialized = pb.ProviderRequest(
            provider=pb.Provider(
                name=self.name,
                description=self.description,
                type=self.config.type(),
                software=self.config.software(),
                team=self.team,
                serialized_config=self.config.serialize(),
                tags=pb.Tags(tag=self.tags),
                properties=Properties(self.properties).serialized,
            ),
            request_id="",
        )
        stub.CreateProvider(serialized)
        return None, None

    def to_dictionary(self):
        return {
            "name": self.name,
            "description": self.description,
            "team": self.team,
            "config": "todox",
            "function": "todox",
            "status": self.status,
            "tags": self.tags,
            "properties": self.properties,
            "error": self.error,
        }
